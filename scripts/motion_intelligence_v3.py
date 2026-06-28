#!/usr/bin/env python3
"""
motion_intelligence_v3.py  —  Motion Intelligence Engine v3

v2 からの改善点:
  1. sticky tracking: アクティブ track に最近傍の COMPACT クラスタを継続選択
  2. SEED_RES_THRESH: track 開始時の最小残差フィルタ（noise seed 排除）
  3. TRAIL_CLUSTER 検出: n_cells≥20 AND bbox_ratio≤0.20 を trail 証拠として記録
  4. select_mode フィールド: sticky / seed / lost / no_seed の選択根拠を出力
  5. trail_detected フィールド: per-pair の trail 検出フラグ

設計書:  docs/motion_intelligence_engine_v3.md
レビュー: review_reports/motion_intelligence_v3_design_20260627.md
"""
import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict, deque
from datetime import date, datetime
from pathlib import Path

import numpy as np
from PIL import Image

VERSION = "motion_intelligence_v3"

# ── デフォルトパラメータ (Adaptive Mode) ────────────────────────────────────
GRID_SIZE_DEFAULT        = 32
PERCENTILE_DEFAULT       = 90.0
MIN_RESIDUAL_DEFAULT     = 8.0
TEMPORAL_WINDOW_DEFAULT  = 3
TEMPORAL_MIN_DEFAULT     = 2
ZONE_GAP_THRESH_DEFAULT  = 10.0

# ── 固定パラメータ (v2 から継続) ─────────────────────────────────────────────
BBOX_LSC_RATIO         = 0.08
STATIC_BG_THRESH       = 2.0
CAMERA_TRACK_BG_MIN    = 20.0
UNIFORMITY_THRESH      = 0.60
TEXTURE_STD_MIN        = 5.0
MASK_EDGE_RATIO        = 0.12
DRIFT_LINEAR_MIN       = 0.5
R2_LINEAR_THRESH       = 0.45

# ── v3 パラメータ ─────────────────────────────────────────────────────────────
SEED_RES_THRESH    = 35.0   # track 開始時の最小 mean_residual（noise≈25 を排除）
MIN_CELLS_SEED     = 2      # track 開始時の最小セル数
MIN_CELLS_CONT     = 1      # track 継続時の最小セル数（sticky 時）
MAX_STICKY_DIST    = 5      # sticky 追跡の最大距離（cell 単位 = 80px）
TRAIL_MIN_CELLS    = 20     # TRAIL_CLUSTER 判定の最小セル数
TRAIL_BRATIO_MAX   = 0.20   # TRAIL_CLUSTER の最大 bbox_ratio（細長い形状）
TRACK_MISS_TOLERANCE = 2    # track 中断を許容する連続 miss 数

# ── Targeted Mode パラメータ ────────────────────────────────────────────────
TARGETED_OVERRIDES = {
    "grid_size":       16,
    "percentile":      85.0,
    "min_residual":    5.0,
    "temporal_window": 5,
    "temporal_min":    2,
    "zone_gap_thresh": 3.0,
}

# ── CSV フィールド定義 ───────────────────────────────────────────────────────
CSV_PAIR_FIELDS = [
    "pair_id", "frame_prev", "frame_curr",
    "timestamp_prev_s", "timestamp_curr_s",
    "bg_motion_x", "bg_motion_y", "bg_motion_magnitude",
    "adaptive_threshold",
    "candidate_cells", "total_valid_cells",
    "candidate_bbox_x", "candidate_bbox_y",
    "mean_residual_mad", "candidate_direction",
    "frame_delta_event",
    "event_type",
    "track_id",
    "track_consecutive_count",
    "track_drift_px_per_s",
    "detection_confidence",
    # v3 新規フィールド
    "select_mode",
    "trail_detected",
    "trail_cells",
    "seed_residual",
]

CSV_TRACK_FIELDS = [
    "track_id",
    "start_pair_id", "end_pair_id",
    "start_ts_s", "end_ts_s", "duration_s",
    "n_pairs_detected",
    "start_bbox_x", "start_bbox_y",
    "end_bbox_x", "end_bbox_y",
    "drift_x_per_s", "drift_y_per_s", "drift_mag_per_s",
    "r_squared",
    "track_event_type",
    "track_direction",
    "mean_detection_confidence",
]

EVENT_DESC = {
    "STATIC":                    "変化なし",
    "BACKGROUND_FLOW":           "背景流動",
    "CAMERA_TRACK":              "カメラ追跡",
    "LIGHTING_SHADOW_CHANGE":    "照明・影・日照変化",
    "POSSIBLE_TARGET_APPEAR":    "対象候補出現",
    "POSSIBLE_TARGET_DISAPPEAR": "対象候補消失",
    "RELATIVE_OBJECT_MOTION":    "対象候補相対運動",
    "REVIEW_REQUIRED":           "要人間確認",
}

TRACK_EVENT_DESC = {
    "LINEAR_MOTION":      "線形運動（高信頼度）",
    "STATIONARY_ANOMALY": "定常異常（位置変化なし）",
    "ERRATIC_MOTION":     "不規則運動（ノイズ可能性）",
    "SINGLE_APPEARANCE":  "単独出現（低信頼度）",
    "SHORT_TRACK":        "短距離トラック（2ペアのみ）",
}

EV_SHORT = {
    "LIGHTING_SHADOW_CHANGE":    "LSC",
    "POSSIBLE_TARGET_APPEAR":    "PTA",
    "POSSIBLE_TARGET_DISAPPEAR": "PTD",
    "RELATIVE_OBJECT_MOTION":    "ROM",
    "BACKGROUND_FLOW":           "BF",
    "CAMERA_TRACK":              "CT",
    "STATIC":                    "S--",
    "REVIEW_REQUIRED":           "RR",
}


# ════════════════════════════════════════════════════════════════════════════
# 画像ユーティリティ (v2 から継続)
# ════════════════════════════════════════════════════════════════════════════

def load_gray(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("L"), dtype=np.uint8)


def phase_correlation_shift(prev: np.ndarray, curr: np.ndarray) -> tuple:
    h, w = prev.shape
    f1 = np.fft.fft2(prev.astype(np.float32))
    f2 = np.fft.fft2(curr.astype(np.float32))
    cross = f1 * np.conj(f2)
    cc = np.real(np.fft.ifft2(cross / (np.abs(cross) + 1e-10)))
    y, x = np.unravel_index(np.argmax(cc), cc.shape)
    if y > h // 2: y -= h
    if x > w // 2: x -= w
    return int(x), int(y)


def iter_valid_cells(h: int, w: int, gs: int, mask_top: int, mask_bot: int):
    for gi in range(h // gs):
        y0 = gi * gs
        if y0 < mask_top: continue
        if y0 + gs > h - mask_bot: continue
        for gj in range(w // gs):
            yield gi, gj, y0, gj * gs


def residual_mad(prev: np.ndarray, curr: np.ndarray,
                 y0: int, x0: int, gs: int, dx: int, dy: int) -> float:
    h, w = curr.shape
    y1, x1 = y0 + dy, x0 + dx
    if y1 < 0 or y1 + gs > h or x1 < 0 or x1 + gs > w:
        return float("nan")
    return float(np.mean(np.abs(
        prev[y0:y0+gs, x0:x0+gs].astype(np.int16)
        - curr[y1:y1+gs, x1:x1+gs].astype(np.int16)
    )))


# ════════════════════════════════════════════════════════════════════════════
# グリッドユーティリティ (v2 から継続)
# ════════════════════════════════════════════════════════════════════════════

def cluster_cells(cell_set: set) -> list:
    if not cell_set:
        return []
    parent = {c: c for c in cell_set}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb

    for gi, gj in cell_set:
        for nb in ((gi-1,gj),(gi+1,gj),(gi,gj-1),(gi,gj+1)):
            if nb in cell_set:
                union((gi,gj), nb)

    groups = defaultdict(list)
    for c in cell_set:
        groups[find(c)].append(c)
    return list(groups.values())


def centroid_px(cells: list, gs: int) -> tuple:
    return (
        float(np.mean([gj * gs + gs / 2 for _, gj in cells])),
        float(np.mean([gi * gs + gs / 2 for gi, _ in cells])),
    )


def bbox_ratio(cells: list, gs: int, h: int, w: int) -> float:
    if not cells: return 0.0
    gis = [gi for gi, _ in cells]
    gjs = [gj for _, gj in cells]
    return ((max(gis)-min(gis)+1) * (max(gjs)-min(gjs)+1)) / max((h//gs)*(w//gs), 1)


def spatial_direction(cx: float, cy: float, fw: float, fh: float) -> str:
    dx, dy = cx - fw / 2, cy - fh / 2
    if abs(dx) < fw * 0.15 and abs(dy) < fh * 0.15:
        return "CENTER"
    a = math.degrees(math.atan2(-dy, dx))
    if   -22.5 <= a <  22.5: return "RIGHT"
    elif  22.5 <= a <  67.5: return "UP_RIGHT"
    elif  67.5 <= a < 112.5: return "UP"
    elif 112.5 <= a < 157.5: return "UP_LEFT"
    elif a >= 157.5 or a < -157.5: return "LEFT"
    elif -157.5 <= a < -112.5: return "DOWN_LEFT"
    elif -112.5 <= a <  -67.5: return "DOWN"
    else: return "DOWN_RIGHT"


# ════════════════════════════════════════════════════════════════════════════
# Phase 1: 適応的閾値 + 候補セル抽出 (v2 から継続)
# ════════════════════════════════════════════════════════════════════════════

def phase1_analyze(prev: np.ndarray, curr: np.ndarray,
                   gs: int, percentile: float, min_residual: float) -> dict:
    h, w = prev.shape
    mask_top = int(h * MASK_EDGE_RATIO)
    mask_bot = int(h * MASK_EDGE_RATIO)

    bg_dx, bg_dy = phase_correlation_shift(prev, curr)
    bg_mag = math.sqrt(bg_dx**2 + bg_dy**2)

    all_rmads = []
    n_valid = 0
    n_low   = 0

    for gi, gj, y0, x0 in iter_valid_cells(h, w, gs, mask_top, mask_bot):
        block = prev[y0:y0+gs, x0:x0+gs]
        if float(np.std(block)) < TEXTURE_STD_MIN:
            continue
        r = residual_mad(prev, curr, y0, x0, gs, bg_dx, bg_dy)
        if math.isnan(r):
            continue
        n_valid += 1
        if r < 12.0:
            n_low += 1
        all_rmads.append((gi, gj, r))

    uniformity = n_low / max(n_valid, 1)
    raw_r = [r for _, _, r in all_rmads]
    adaptive_thresh = (
        max(float(np.percentile(raw_r, percentile)), min_residual)
        if raw_r else min_residual
    )

    all_candidates = {
        (gi, gj): r
        for gi, gj, r in all_rmads
        if r >= adaptive_thresh
    }

    return {
        "bg_dx": bg_dx, "bg_dy": bg_dy, "bg_mag": bg_mag,
        "uniformity": uniformity,
        "adaptive_thresh": adaptive_thresh,
        "all_candidates": all_candidates,
        "n_valid": n_valid,
        "frame_h": h, "frame_w": w,
    }


# ════════════════════════════════════════════════════════════════════════════
# Phase 2: 時間的一貫性 (v2 から継続)
# ════════════════════════════════════════════════════════════════════════════

def get_persistent(cell_history: deque, t_min: int) -> set:
    if not cell_history:
        return set()
    counter = Counter()
    for frame_dict in cell_history:
        counter.update(frame_dict.keys())
    return {c for c, n in counter.items() if n >= t_min}


def get_persistent_residuals(persistent: set, cell_history: deque) -> dict:
    result = {}
    for cell in persistent:
        vals = [fd[cell] for fd in cell_history if cell in fd]
        result[cell] = max(vals) if vals else 0.0
    return result


# ════════════════════════════════════════════════════════════════════════════
# v3: クラスタ分類 + select_primary_v3
# ════════════════════════════════════════════════════════════════════════════

def classify_cluster_type(n_cells: int, bratio: float) -> str:
    """クラスタを TRAIL_CLUSTER / COMPACT / TINY に分類"""
    if n_cells >= TRAIL_MIN_CELLS and bratio <= TRAIL_BRATIO_MAX:
        return "TRAIL_CLUSTER"
    if n_cells < MIN_CELLS_CONT:
        return "TINY"
    return "COMPACT"


def select_primary_v3(clusters: list, h: int, w: int, gs: int,
                      cell_residuals: dict,
                      active_track_centroid) -> tuple:
    """
    v3 sticky / seed 二段階選択。TRAIL_CLUSTER は追跡対象から除外。

    Returns:
      (cells, cx, cy, mean_res, bratio, select_mode, seed_residual)
      select_mode: "sticky" / "seed" / "lost" / "no_seed"
      seed_residual: seed 選択時の mean_residual（sticky 時は nan）
    """
    compact_candidates = []
    for cl in clusters:
        n  = len(cl)
        br = bbox_ratio(cl, gs, h, w)
        if classify_cluster_type(n, br) != "COMPACT":
            continue
        res = [cell_residuals.get(c, 0.0) for c in cl]
        mr  = float(np.mean(res)) if res else 0.0
        compact_candidates.append({
            "cells":    cl,
            "br":       br,
            "mr":       mr,
            "n":        n,
            "centroid": centroid_px(cl, gs),
        })

    if active_track_centroid is not None:
        # sticky モード: アクティブ track に最近傍の COMPACT クラスタ
        if not compact_candidates:
            return [], 0.0, 0.0, 0.0, 0.0, "lost", float("nan")

        ax, ay = active_track_centroid

        def dist_cells(c):
            cx2, cy2 = c["centroid"]
            return math.sqrt(((cx2 - ax) / gs) ** 2 + ((cy2 - ay) / gs) ** 2)

        nearest = min(compact_candidates, key=dist_cells)
        d = dist_cells(nearest)

        if d <= MAX_STICKY_DIST:
            cx, cy = nearest["centroid"]
            return nearest["cells"], cx, cy, nearest["mr"], nearest["br"], "sticky", float("nan")
        else:
            return [], 0.0, 0.0, 0.0, 0.0, "lost", float("nan")

    else:
        # seed モード: SEED_RES_THRESH + MIN_CELLS_SEED でフィルタ
        seeds = [
            c for c in compact_candidates
            if c["mr"] >= SEED_RES_THRESH and c["n"] >= MIN_CELLS_SEED
        ]
        if seeds:
            best = max(seeds, key=lambda c: c["mr"])
            cx, cy = best["centroid"]
            return best["cells"], cx, cy, best["mr"], best["br"], "seed", best["mr"]
        else:
            return [], 0.0, 0.0, 0.0, 0.0, "no_seed", float("nan")


# ════════════════════════════════════════════════════════════════════════════
# イベント分類 (v2 から継続)
# ════════════════════════════════════════════════════════════════════════════

def classify_pair_event(
    bg_mag: float,
    uniformity: float,
    has_primary: bool,
    n_persistent: int,
    n_total_cands: int,
    track_id: int,
    track_consec: int,
    prev_had_track: bool,
) -> str:
    all_lsc = (n_persistent > 0) and (not has_primary)

    if bg_mag < STATIC_BG_THRESH and not has_primary and n_persistent == 0:
        return "STATIC"

    if all_lsc:
        return "LIGHTING_SHADOW_CHANGE"

    if has_primary and track_id > 0 and track_consec == 1 and not prev_had_track:
        return "POSSIBLE_TARGET_APPEAR"

    if prev_had_track and not has_primary and track_id < 0:
        return "POSSIBLE_TARGET_DISAPPEAR"

    if bg_mag >= CAMERA_TRACK_BG_MIN and uniformity >= UNIFORMITY_THRESH:
        return "CAMERA_TRACK"

    if has_primary and track_id > 0 and track_consec > 1:
        return "RELATIVE_OBJECT_MOTION"

    if bg_mag >= STATIC_BG_THRESH and not has_primary:
        return "BACKGROUND_FLOW"

    if has_primary:
        return "REVIEW_REQUIRED"

    return "STATIC"


# ════════════════════════════════════════════════════════════════════════════
# 線形回帰・トラック分類 (v2 から継続)
# ════════════════════════════════════════════════════════════════════════════

def r_squared(x: np.ndarray, y: np.ndarray, coeffs) -> float:
    y_pred = np.polyval(coeffs, x)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1.0 if ss_tot < 1e-10 else float(1.0 - ss_res / ss_tot)


def fit_track(points: list) -> dict:
    if len(points) < 2:
        return {"drift_x": 0.0, "drift_y": 0.0, "drift_mag": 0.0, "r2": 0.0}
    ts = np.array([p[1] for p in points], dtype=float)
    cx = np.array([p[2] for p in points], dtype=float)
    cy = np.array([p[3] for p in points], dtype=float)
    px = np.polyfit(ts, cx, 1)
    py = np.polyfit(ts, cy, 1)
    r2 = (r_squared(ts, cx, px) + r_squared(ts, cy, py)) / 2
    dx, dy = float(px[0]), float(py[0])
    return {
        "drift_x":   round(dx, 2),
        "drift_y":   round(dy, 2),
        "drift_mag": round(math.sqrt(dx**2 + dy**2), 2),
        "r2":        round(r2, 3),
    }


def classify_track_event(n_pairs: int, drift_mag: float, r2: float) -> str:
    if n_pairs == 1: return "SINGLE_APPEARANCE"
    if n_pairs == 2: return "SHORT_TRACK"
    if drift_mag < DRIFT_LINEAR_MIN: return "STATIONARY_ANOMALY"
    if r2 >= R2_LINEAR_THRESH: return "LINEAR_MOTION"
    return "ERRATIC_MOTION"


def detection_confidence(n_pairs: int, r2: float,
                          drift_mag: float, bratio: float) -> float:
    s  = 0.30 * min(1.0, n_pairs / 5)
    s += 0.30 * max(0.0, min(1.0, r2))
    s += 0.20 * min(1.0, drift_mag / 10.0)
    s += 0.20 * max(0.0, 1.0 - bratio / BBOX_LSC_RATIO)
    return round(s, 3)


# ════════════════════════════════════════════════════════════════════════════
# フレーム収集 (v2 から継続)
# ════════════════════════════════════════════════════════════════════════════

def collect_frames(d: Path) -> list:
    return sorted(d.glob("frame_*.png"), key=lambda p: p.name)


def ts_from_name(name: str) -> float:
    return float(int(Path(name).stem.split("_", 1)[1]))


# ════════════════════════════════════════════════════════════════════════════
# サマリー生成 (v3 更新)
# ════════════════════════════════════════════════════════════════════════════

def build_summary(results: list, track_results: list,
                  source_id: str, article_id: str,
                  frames_dir: Path, mode: str) -> str:
    ec = Counter(r["event_type"] for r in results)
    sm = Counter(r["select_mode"] for r in results)
    trail_pairs = sum(1 for r in results if r["trail_detected"])

    lines = [
        "# Motion Intelligence Summary (v3)",
        "",
        f"- 実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- article_id: {article_id}",
        f"- source_id: {source_id}",
        f"- frames_dir: {frames_dir}",
        f"- 分類器: {VERSION} / mode={mode}",
        "",
        "---", "",
        "## イベント別件数", "",
        "| イベント | 件数 | 説明 |",
        "|---------|------|------|",
    ]
    for ev, desc in EVENT_DESC.items():
        lines.append(f"| {ev} | {ec.get(ev, 0)} | {desc} |")

    lines += [
        "", "---", "", "## v3 select_mode 内訳", "",
        "| select_mode | 件数 |",
        "|-------------|------|",
        f"| sticky  | {sm.get('sticky', 0)} |",
        f"| seed    | {sm.get('seed', 0)} |",
        f"| lost    | {sm.get('lost', 0)} |",
        f"| no_seed | {sm.get('no_seed', 0)} |",
        "",
        f"- trail_detected ペア数: {trail_pairs}",
    ]

    lines += ["", "---", "", "## トラック一覧", ""]
    if track_results:
        lines += [
            "| track_id | start_ts | end_ts | n_pairs | drift(px/s) | R² | track_event | direction |",
            "|----------|---------|--------|---------|------------|-----|------------|-----------|",
        ]
        for t in sorted(track_results, key=lambda x: x["start_ts_s"]):
            lines.append(
                f"| {t['track_id']} | {t['start_ts_s']}s | {t['end_ts_s']}s | "
                f"{t['n_pairs_detected']} | {t['drift_mag_per_s']} | {t['r_squared']} | "
                f"{t['track_event_type']} | {t['track_direction']} |"
            )
    else:
        lines.append("（トラックなし）")

    for ev_filter, title in [
        (["POSSIBLE_TARGET_APPEAR"],    "POSSIBLE_TARGET_APPEAR（候補出現）"),
        (["POSSIBLE_TARGET_DISAPPEAR"], "POSSIBLE_TARGET_DISAPPEAR（候補消失）"),
        (["RELATIVE_OBJECT_MOTION"],    "RELATIVE_OBJECT_MOTION 上位10件"),
        (["REVIEW_REQUIRED"],           "REVIEW_REQUIRED（要確認）"),
    ]:
        rows = [r for r in results if r["event_type"] in ev_filter]
        if ev_filter == ["RELATIVE_OBJECT_MOTION"]:
            rows = sorted(rows, key=lambda r: r["detection_confidence"], reverse=True)[:10]
        lines += ["", f"### {title}"]
        if rows:
            lines += [
                "| pair_id | ts_prev→curr | cands | track_id | consec | conf | mode | trail |",
                "|---------|-------------|-------|----------|--------|------|------|-------|",
            ]
            for r in rows:
                lines.append(
                    f"| {r['pair_id']} | {r['timestamp_prev_s']}→{r['timestamp_curr_s']}s | "
                    f"{r['candidate_cells']} | {r['track_id']} | "
                    f"{r['track_consecutive_count']} | {r['detection_confidence']} | "
                    f"{r['select_mode']} | {r['trail_detected']} |"
                )
        else:
            lines.append("（なし）")

    lsc = ec.get("LIGHTING_SHADOW_CHANGE", 0)
    lines += [
        "", "---", "", "## v2 との比較", "",
        f"- 総ペア数: {len(results)}",
        f"- LSC: {lsc} 件（v1 では全件 LSC）",
        f"- 非 LSC: {len(results) - lsc} 件",
        f"- トラック数: {len(track_results)}（v2: 63 / 目標: ≤25）",
        f"- trail_detected ペア: {trail_pairs}",
    ]
    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════════════════
# 引数解析
# ════════════════════════════════════════════════════════════════════════════

def parse_args():
    p = argparse.ArgumentParser(
        description=f"{VERSION} — sticky tracking + seed filter + trail detection"
    )
    p.add_argument("--frames-dir",       required=True,
                   help="フレーム画像ディレクトリ (frame_NNNNN.png)")
    p.add_argument("--delta-csv",        default="",
                   help="frame_delta_v2.csv（イベント参照用・オプション）")
    p.add_argument("--article-id",       default="UNKNOWN")
    p.add_argument("--source-id",        required=True)
    p.add_argument("--output-dir",       default="",
                   help="出力先ディレクトリ（省略時は自動生成）")
    p.add_argument("--mode",             choices=["adaptive", "targeted"],
                   default="adaptive")
    p.add_argument("--grid-size",        type=int,   default=0)
    p.add_argument("--percentile",       type=float, default=0)
    p.add_argument("--min-residual",     type=float, default=0)
    p.add_argument("--temporal-window",  type=int,   default=0)
    p.add_argument("--temporal-min",     type=int,   default=0)
    p.add_argument("--execute",          action="store_true",
                   help="ファイル出力あり（省略時は dry-run）")
    p.add_argument("--verbose",          action="store_true",
                   help="全ペアの詳細ログ（クラスタ情報含む）")
    return p.parse_args()


# ════════════════════════════════════════════════════════════════════════════
# メイン
# ════════════════════════════════════════════════════════════════════════════

def main():
    args = parse_args()
    is_targeted = (args.mode == "targeted")

    def pick(attr, default, override_key):
        val = getattr(args, attr, 0) or 0
        if val: return val
        return TARGETED_OVERRIDES[override_key] if is_targeted else default

    gs       = pick("grid_size",       GRID_SIZE_DEFAULT,       "grid_size")
    pct      = pick("percentile",      PERCENTILE_DEFAULT,      "percentile")
    min_res  = pick("min_residual",    MIN_RESIDUAL_DEFAULT,    "min_residual")
    t_win    = pick("temporal_window", TEMPORAL_WINDOW_DEFAULT, "temporal_window")
    t_min    = pick("temporal_min",    TEMPORAL_MIN_DEFAULT,    "temporal_min")
    zone_gap = TARGETED_OVERRIDES["zone_gap_thresh"] if is_targeted else ZONE_GAP_THRESH_DEFAULT

    frames_dir = Path(args.frames_dir)
    if not frames_dir.exists():
        sys.exit(f"[ERROR] frames_dir が存在しない: {frames_dir}")

    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        run_date = date.today().strftime("%Y%m%d")
        out_dir  = Path("data") / "motion_intelligence_runs" / run_date / args.source_id / "v3"

    delta_rows: dict = {}
    if args.delta_csv:
        dp = Path(args.delta_csv)
        if dp.exists():
            with open(dp, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    delta_rows[int(row["pair_id"])] = row

    frames  = collect_frames(frames_dir)
    n_frames = len(frames)
    n_pairs  = n_frames - 1
    if n_frames < 2:
        sys.exit("[ERROR] フレームが 2 枚未満")

    mode_label = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"[{VERSION}] mode={mode_label} ({args.mode})")
    print(f"  article_id      : {args.article_id}")
    print(f"  source_id       : {args.source_id}")
    print(f"  frames_dir      : {frames_dir}")
    print(f"  grid_size       : {gs}px")
    print(f"  percentile      : p{pct}")
    print(f"  min_residual    : {min_res}")
    print(f"  temporal_window : W={t_win}")
    print(f"  temporal_min    : T={t_min}")
    print(f"  zone_gap_thresh : {zone_gap}s")
    print(f"  SEED_RES_THRESH : {SEED_RES_THRESH}")
    print(f"  MAX_STICKY_DIST : {MAX_STICKY_DIST} cells ({MAX_STICKY_DIST * gs}px)")
    print(f"  TRAIL_MIN_CELLS : {TRAIL_MIN_CELLS}")
    print(f"  TRACK_MISS_TOL  : {TRACK_MISS_TOLERANCE}")
    print(f"  フレーム数      : {n_frames}")
    print(f"  ペア数          : {n_pairs}")
    print(f"  出力先          : {out_dir}/")

    # ────────────────────────────────────────────────────────────────────────
    # process_all
    # ────────────────────────────────────────────────────────────────────────
    def process_all(n_max: int):
        cell_history          = deque(maxlen=t_win)
        track_registry        = {}
        next_tid              = [1]
        current_tid           = -1
        track_consec          = 0
        track_miss            = 0
        prev_had_track        = False
        active_track_centroid = None   # v3: sticky 追跡用

        frame_ts = [ts_from_name(f.name) for f in frames]
        rows = []

        for i in range(min(n_max, n_pairs)):
            prev_p  = frames[i]
            curr_p  = frames[i + 1]
            pair_id = i + 1
            ts_prev = frame_ts[i]
            ts_curr = frame_ts[i + 1]
            fd_ev   = delta_rows.get(pair_id, {}).get("event_type", "UNKNOWN")

            # ゾーン境界リセット
            if i > 0 and (frame_ts[i] - frame_ts[i - 1]) > zone_gap:
                cell_history.clear()
                current_tid           = -1
                track_consec          = 0
                track_miss            = 0
                prev_had_track        = False
                active_track_centroid = None
                if args.verbose or not args.execute:
                    print(f"  [ZONE_BOUNDARY] pair {pair_id}: "
                          f"frames[{i-1}]({frame_ts[i-1]:.0f}s)→"
                          f"frames[{i}]({frame_ts[i]:.0f}s) "
                          f"gap={frame_ts[i]-frame_ts[i-1]:.0f}s → reset")

            # Phase 1: 適応的閾値
            prev_arr = load_gray(prev_p)
            curr_arr = load_gray(curr_p)
            p1 = phase1_analyze(prev_arr, curr_arr, gs, pct, min_res)

            # Phase 2: 時間的一貫性
            cell_history.append(p1["all_candidates"])
            persistent = get_persistent(cell_history, t_min)
            pers_res   = get_persistent_residuals(persistent, cell_history)
            clusters   = cluster_cells(persistent)

            # v3: TRAIL_CLUSTER 検出
            trail_detected    = False
            trail_cells_count = 0
            for cl in clusters:
                n  = len(cl)
                br = bbox_ratio(cl, gs, p1["frame_h"], p1["frame_w"])
                if n >= TRAIL_MIN_CELLS and br <= TRAIL_BRATIO_MAX:
                    trail_detected = True
                    if n > trail_cells_count:
                        trail_cells_count = n

            # verbose: クラスタ詳細
            if args.verbose and clusters:
                for cl in sorted(clusters, key=lambda c: -len(c)):
                    n  = len(cl)
                    br = bbox_ratio(cl, gs, p1["frame_h"], p1["frame_w"])
                    mr = float(np.mean([pers_res.get(c, 0.0) for c in cl]))
                    ct = classify_cluster_type(n, br)
                    print(f"       [cluster] n={n:3d} br={br:.3f} mr={mr:5.1f} {ct}")

            # v3: select_primary_v3
            primary, cx, cy, mean_res, pbratio, select_mode, seed_res = select_primary_v3(
                clusters, p1["frame_h"], p1["frame_w"], gs, pers_res,
                active_track_centroid,
            )
            has_primary = len(primary) >= 1

            # Track 更新 (v3)
            if has_primary:
                if select_mode == "sticky" and current_tid > 0:
                    # 既存 track を継続
                    track_consec += 1
                    track_miss    = 0
                else:
                    # 新規 track 開始（seed / sticky だが current_tid なし）
                    current_tid  = next_tid[0]; next_tid[0] += 1
                    track_consec = 1
                    track_miss   = 0

                active_track_centroid = (cx, cy)
                track_registry.setdefault(current_tid, []).append(
                    (pair_id, ts_curr, cx, cy, len(primary), mean_res, pbratio)
                )
                eff_tid = current_tid
            else:
                track_miss += 1
                if track_miss > TRACK_MISS_TOLERANCE:
                    current_tid           = -1
                    track_consec          = 0
                    active_track_centroid = None
                # miss 許容内: active_track_centroid を維持（sticky 継続候補）
                eff_tid = -1

            # イベント分類
            event = classify_pair_event(
                bg_mag         = p1["bg_mag"],
                uniformity     = p1["uniformity"],
                has_primary    = has_primary,
                n_persistent   = len(persistent),
                n_total_cands  = len(p1["all_candidates"]),
                track_id       = eff_tid,
                track_consec   = track_consec if has_primary else 0,
                prev_had_track = prev_had_track,
            )

            cand_dir = (
                spatial_direction(cx, cy, p1["frame_w"], p1["frame_h"])
                if has_primary else "NONE"
            )
            conf = detection_confidence(
                track_consec if has_primary else 0,
                0.0, 0.0, pbratio
            ) if has_primary else 0.0

            seed_res_out = "" if (isinstance(seed_res, float) and math.isnan(seed_res)) else (
                round(seed_res, 2) if not isinstance(seed_res, float) or not math.isnan(seed_res) else ""
            )

            rows.append({
                "pair_id":                 pair_id,
                "frame_prev":              prev_p.name,
                "frame_curr":              curr_p.name,
                "timestamp_prev_s":        ts_prev,
                "timestamp_curr_s":        ts_curr,
                "bg_motion_x":             round(float(p1["bg_dx"]), 2),
                "bg_motion_y":             round(float(p1["bg_dy"]), 2),
                "bg_motion_magnitude":     round(p1["bg_mag"], 2),
                "adaptive_threshold":      round(p1["adaptive_thresh"], 2),
                "candidate_cells":         len(primary),
                "total_valid_cells":       p1["n_valid"],
                "candidate_bbox_x":        round(cx, 1),
                "candidate_bbox_y":        round(cy, 1),
                "mean_residual_mad":       round(mean_res, 2),
                "candidate_direction":     cand_dir,
                "frame_delta_event":       fd_ev,
                "event_type":              event,
                "track_id":                eff_tid,
                "track_consecutive_count": track_consec if has_primary else 0,
                "track_drift_px_per_s":    0.0,
                "detection_confidence":    conf,
                # v3
                "select_mode":   select_mode,
                "trail_detected": trail_detected,
                "trail_cells":    trail_cells_count,
                "seed_residual":  seed_res_out,
                "_pbratio":       pbratio,
            })
            prev_had_track = has_primary and eff_tid > 0

            # ログ出力
            should_log = args.verbose or (not args.execute and i < 10)
            if should_log or (args.execute and not args.verbose and pair_id % 20 == 0):
                ev_s    = EV_SHORT.get(event, event[:3])
                trail_s = " TRAIL!" if trail_detected else ""
                atc_s   = f"({active_track_centroid[0]:.0f},{active_track_centroid[1]:.0f})" \
                          if active_track_centroid else "None"
                print(
                    f"  {pair_id:4d}/{n_pairs}: "
                    f"{ts_prev:.0f}→{ts_curr:.0f}s "
                    f"thr={p1['adaptive_thresh']:.0f} "
                    f"raw={len(p1['all_candidates'])} "
                    f"pers={len(persistent)} "
                    f"prim={len(primary)} "
                    f"mode={select_mode:<7} "
                    f"tid={eff_tid if has_primary else '-':>3} "
                    f"mr={mean_res:.1f} "
                    f"atc={atc_s} "
                    f"[{ev_s}]{trail_s}"
                )

        return rows, track_registry

    # ── DRY-RUN ─────────────────────────────────────────────────────────────
    if not args.execute:
        print(f"\n[DRY-RUN] 先頭 10 ペアをプレビュー...")
        process_all(n_max=10)
        print(f"\n[DRY-RUN] 完了。--execute を付けると全件実行。")
        return

    # ── EXECUTE ─────────────────────────────────────────────────────────────
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[1/3] 全ペア解析中 ({n_pairs} ペア)...")
    results, track_registry = process_all(n_max=n_pairs)

    print(f"\n[2/3] Track 後処理中...")
    track_results = []
    for tid, points in track_registry.items():
        pts     = sorted(points, key=lambda p: p[0])
        lin     = fit_track(pts)
        n_pts   = len(pts)
        mean_br = float(np.mean([p[6] for p in pts]))
        tev     = classify_track_event(n_pts, lin["drift_mag"], lin["r2"])
        mconf   = detection_confidence(n_pts, lin["r2"], lin["drift_mag"], mean_br)

        s, e = pts[0], pts[-1]
        mid_cx = (s[2] + e[2]) / 2
        mid_cy = (s[3] + e[3]) / 2
        tr = {
            "track_id":                  tid,
            "start_pair_id":             s[0],
            "end_pair_id":               e[0],
            "start_ts_s":                s[1],
            "end_ts_s":                  e[1],
            "duration_s":                round(e[1] - s[1], 1),
            "n_pairs_detected":          n_pts,
            "start_bbox_x":              round(s[2], 1),
            "start_bbox_y":              round(s[3], 1),
            "end_bbox_x":                round(e[2], 1),
            "end_bbox_y":                round(e[3], 1),
            "drift_x_per_s":             lin["drift_x"],
            "drift_y_per_s":             lin["drift_y"],
            "drift_mag_per_s":           lin["drift_mag"],
            "r_squared":                 lin["r2"],
            "track_event_type":          tev,
            "track_direction":           spatial_direction(mid_cx, mid_cy, 1280.0, 720.0),
            "mean_detection_confidence": round(mconf, 3),
        }
        track_results.append(tr)

        for row in results:
            if row["track_id"] == tid:
                row["track_drift_px_per_s"] = lin["drift_mag"]
                row["detection_confidence"] = round(mconf, 3)

    track_results.sort(key=lambda t: t["start_ts_s"])
    print(f"  検出トラック数: {len(track_results)}")
    for t in track_results:
        print(
            f"  track_{t['track_id']}: "
            f"{t['start_ts_s']}s→{t['end_ts_s']}s "
            f"n={t['n_pairs_detected']} "
            f"drift={t['drift_mag_per_s']:.1f}px/s "
            f"R²={t['r_squared']} "
            f"[{t['track_event_type']}] {t['track_direction']}"
        )

    print(f"\n[3/3] ファイル出力中...")

    with open(out_dir / "motion_events.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_PAIR_FIELDS)
        w.writeheader()
        for r in results:
            w.writerow({k: r[k] for k in CSV_PAIR_FIELDS})

    with open(out_dir / "motion_events.jsonl", "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps({k: r[k] for k in CSV_PAIR_FIELDS},
                               ensure_ascii=False) + "\n")

    with open(out_dir / "track_events.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_TRACK_FIELDS)
        w.writeheader()
        for t in track_results:
            w.writerow({k: t[k] for k in CSV_TRACK_FIELDS})

    summary_txt = build_summary(
        results, track_results,
        args.source_id, args.article_id, frames_dir, args.mode,
    )
    with open(out_dir / "summary.md", "w", encoding="utf-8") as f:
        f.write(summary_txt)

    ec  = Counter(r["event_type"] for r in results)
    sm  = Counter(r["select_mode"] for r in results)
    trail_pairs = sum(1 for r in results if r["trail_detected"])
    print(f"\n[完了]")
    for ev, desc in EVENT_DESC.items():
        cnt = ec.get(ev, 0)
        if cnt:
            print(f"  {ev:<28}: {cnt:3d} 件")
    print(f"  トラック数                  : {len(track_results)}")
    print(f"  select_mode                 : "
          f"sticky={sm.get('sticky',0)} seed={sm.get('seed',0)} "
          f"lost={sm.get('lost',0)} no_seed={sm.get('no_seed',0)}")
    print(f"  trail_detected ペア         : {trail_pairs}")
    print(f"  出力: {out_dir}/")


if __name__ == "__main__":
    main()
