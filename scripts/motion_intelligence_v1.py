#!/usr/bin/env python3
"""
motion_intelligence_v1.py

背景運動と対象候補運動の分離エンジン v1

Frame Delta v2（画素差分中心）の補完として、カメラ/機体移動による
背景流動を推定・除外し、背景と異なる相対運動を持つ局所領域を候補化する。

設計書: docs/motion_intelligence_engine_v1.md

アルゴリズム（v1 実装: Phase Correlation + 局所残差 MAD）:
  1. FFT Phase Correlation でフレーム間グローバルシフト (dx, dy) を推定
     → 大変位（100px 超）にも対応（ブロックマッチングの探索窓制限を排除）
  2. グローバルシフト適用後の局所残差 MAD を全グリッドセルで計算
     → グローバルシフトと異なる動きをした領域を高残差として検出
  3. 残差閾値以上のセルを候補として抽出
  4. クラスタリング（4連結 Union-Find）
  5. 照明・影・マスキング除外フィルタ
  6. イベント分類（9種）
  7. motion_events.csv / .jsonl / summary.md 出力

使用ライブラリ: Pillow + numpy のみ（OpenCV 不要）

v1 の制限（設計書 § 8参照）:
  - ZOOM_OR_CROP 検出は Phase Correlation では困難（v1 では LSC で代替）
  - candidate_direction は対象の空間的位置から推定（運動ベクトルではない）

使用方法:
  # dry-run（先頭3ペアのみプレビュー）
  python3 scripts/motion_intelligence_v1.py \\
    --frames-dir data/adaptive_frames/20260627/<source_id>/ \\
    --delta-csv  data/frame_delta_runs/20260627_v2/<source_id>/frame_delta.csv \\
    --article-id R02-053 \\
    --source-id  DOW-UAP-PR061_...

  # 実行
  python3 scripts/motion_intelligence_v1.py [上記] --execute
"""

import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

import numpy as np
from PIL import Image

# ── バージョン ──────────────────────────────────────────────────────────────
VERSION = "motion_intelligence_v1"

# ── CLI デフォルト閾値 ──────────────────────────────────────────────────────
GRID_SIZE_DEFAULT           = 32    # グリッドセルサイズ (px)
RESIDUAL_THRESH_DEFAULT     = 12.0  # 候補セル判定: 残差 MAD がこれ以上
MIN_CANDIDATE_CELLS_DEFAULT = 2     # 最大クラスタの最小セル数

# ── 固定パラメータ ──────────────────────────────────────────────────────────
TEXTURE_STD_MIN     = 5.0   # セル内輝度 std がこれ未満 → 低コントラスト除外
MASK_EDGE_RATIO     = 0.12  # 上下 12% をマスキング境界として解析除外
LOW_RES_THRESH      = 12.0  # 残差 MAD < これ → グローバルシフトで説明できる（均一）
STATIC_BG_THRESH    = 2.0   # bg_magnitude < これ → STATIC 候補
CAMERA_TRACK_BG_MIN = 20.0  # bg_magnitude ≥ これ + 均一 → CAMERA_TRACK
UNIFORMITY_THRESH   = 0.60  # セル均一率がこれ以上 → CAMERA_TRACK
# LSC vs ROM の区別:
#   - 最大クラスタのバウンディングボックス面積 ≥ BBOX_LSC_RATIO → LSC（広域変化）
#   - バウンディングボックス面積 < BBOX_ROM_MAX → ROM/PTA（局所物体）
LIGHTING_WIDE_RATIO = 0.15   # 全候補 / valid_total 閾値（二次条件）
BBOX_LSC_RATIO      = 0.08   # bbox/total_cells ≥ この値 → LSC（地形・照明変化）
BBOX_ROM_MAX        = 0.08   # bbox/total_cells < この値 → ROM/PTA 候補

# ── CSV フィールド ──────────────────────────────────────────────────────────
CSV_FIELDS = [
    "pair_id", "frame_prev", "frame_curr",
    "timestamp_prev_s", "timestamp_curr_s",
    "bg_motion_x", "bg_motion_y", "bg_motion_magnitude",
    "candidate_cells", "total_valid_cells",
    "candidate_bbox_x", "candidate_bbox_y",
    "mean_residual_mad", "candidate_direction",
    "frame_delta_event",
    "event_type",
]

EVENT_DESC = {
    "STATIC":                    "変化なし",
    "BACKGROUND_FLOW":           "背景流動（カメラ/機体移動）",
    "CAMERA_TRACK":              "カメラ追跡（大きな均一移動）",
    "ZOOM_OR_CROP":              "ズーム/クロップ変化",
    "LIGHTING_SHADOW_CHANGE":    "照明・影・日照変化",
    "RELATIVE_OBJECT_MOTION":    "対象候補の相対運動",
    "POSSIBLE_TARGET_APPEAR":    "対象候補出現",
    "POSSIBLE_TARGET_DISAPPEAR": "対象候補消失",
    "REVIEW_REQUIRED":           "要人間確認",
}

EVENT_SHORT = {ev: abbr for abbr, ev in [
    ("S",   "STATIC"),
    ("BF",  "BACKGROUND_FLOW"),
    ("CT",  "CAMERA_TRACK"),
    ("ZC",  "ZOOM_OR_CROP"),
    ("LSC", "LIGHTING_SHADOW_CHANGE"),
    ("ROM", "RELATIVE_OBJECT_MOTION"),
    ("PTA", "POSSIBLE_TARGET_APPEAR"),
    ("PTD", "POSSIBLE_TARGET_DISAPPEAR"),
    ("RR",  "REVIEW_REQUIRED"),
]}


# ════════════════════════════════════════════════════════════════════════════
# 画像ロード
# ════════════════════════════════════════════════════════════════════════════

def load_gray_uint8(path: Path) -> np.ndarray:
    """Pillow でグレースケール読み込み → uint8 numpy 配列"""
    return np.array(Image.open(path).convert("L"), dtype=np.uint8)


# ════════════════════════════════════════════════════════════════════════════
# FFT Phase Correlation（グローバルシフト推定）
# ════════════════════════════════════════════════════════════════════════════

def phase_correlation_shift(prev: np.ndarray, curr: np.ndarray) -> tuple[int, int]:
    """
    FFT Phase Correlation でフレーム間のグローバル平行移動量 (dx, dy) を推定。

    大変位（100px超）にも対応。ブロックマッチングの探索窓制限なし。

    Returns:
        (dx, dy): 正 → curr が prev より右/下にシフト
    """
    h, w = prev.shape
    f1 = np.fft.fft2(prev.astype(np.float32))
    f2 = np.fft.fft2(curr.astype(np.float32))
    cross = f1 * np.conj(f2)
    denom = np.abs(cross) + 1e-10
    cc = np.real(np.fft.ifft2(cross / denom))

    y, x = np.unravel_index(np.argmax(cc), cc.shape)

    # 符号付き変位に変換（折り返し処理）
    if y > h // 2:
        y -= h
    if x > w // 2:
        x -= w

    return int(x), int(y)   # (dx, dy)


# ════════════════════════════════════════════════════════════════════════════
# グリッドユーティリティ
# ════════════════════════════════════════════════════════════════════════════

def iter_valid_cells(h: int, w: int, gs: int, mask_top: int, mask_bot: int):
    """有効グリッドセル (gi, gj, y0, x0) を yield（マスキング境界を除外）"""
    for gi in range(h // gs):
        y0 = gi * gs
        if y0 < mask_top:
            continue
        if y0 + gs > h - mask_bot:
            continue
        for gj in range(w // gs):
            yield gi, gj, y0, gj * gs


def residual_mad(
    prev: np.ndarray, curr: np.ndarray,
    y0: int, x0: int, gs: int, dx: int, dy: int,
) -> float:
    """
    グローバルシフト (dx, dy) 適用後の局所残差 MAD を返す。

    prev の (y0, x0) ブロックと curr の (y0+dy, x0+dx) ブロックを比較。
    境界外の場合は np.nan を返す。
    """
    h, w = curr.shape
    y1, x1 = y0 + dy, x0 + dx
    if y1 < 0 or y1 + gs > h or x1 < 0 or x1 + gs > w:
        return float("nan")
    block_p = prev[y0:y0 + gs, x0:x0 + gs].astype(np.int16)
    block_c = curr[y1:y1 + gs, x1:x1 + gs].astype(np.int16)
    return float(np.mean(np.abs(block_p - block_c)))


# ════════════════════════════════════════════════════════════════════════════
# クラスタリング（4連結 Union-Find）
# ════════════════════════════════════════════════════════════════════════════

def cluster_candidates(candidate_set: set) -> list[list]:
    if not candidate_set:
        return []
    parent = {c: c for c in candidate_set}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for gi, gj in candidate_set:
        for nb in ((gi - 1, gj), (gi + 1, gj), (gi, gj - 1), (gi, gj + 1)):
            if nb in candidate_set:
                union((gi, gj), nb)

    groups: dict = defaultdict(list)
    for c in candidate_set:
        groups[find(c)].append(c)
    return list(groups.values())


def centroid_px(cells: list, gs: int) -> tuple[float, float]:
    xs = [(gj * gs + gs / 2) for _, gj in cells]
    ys = [(gi * gs + gs / 2) for gi, _ in cells]
    return float(np.mean(xs)), float(np.mean(ys))


def spatial_direction(cx: float, cy: float, fw: float, fh: float) -> str:
    """候補クラスタの空間的位置（フレーム中心との相対方向）"""
    dx = cx - fw / 2
    dy = cy - fh / 2   # 画像座標は下が正
    if abs(dx) < fw * 0.15 and abs(dy) < fh * 0.15:
        return "CENTER"
    angle = math.degrees(math.atan2(-dy, dx))  # UP が正
    if   -22.5 <= angle <  22.5:  return "RIGHT"
    elif  22.5 <= angle <  67.5:  return "UP_RIGHT"
    elif  67.5 <= angle < 112.5:  return "UP"
    elif 112.5 <= angle < 157.5:  return "UP_LEFT"
    elif angle >=  157.5 or angle < -157.5: return "LEFT"
    elif -157.5 <= angle < -112.5: return "DOWN_LEFT"
    elif -112.5 <= angle <  -67.5: return "DOWN"
    else:                          return "DOWN_RIGHT"


# ════════════════════════════════════════════════════════════════════════════
# イベント分類
# ════════════════════════════════════════════════════════════════════════════

def classify_event(
    bg_mag: float,
    uniformity: float,
    n_candidates: int,        # 最大クラスタのセル数
    n_total_candidates: int,  # 全候補セル数
    total_valid: int,
    cluster_bbox_ratio: float,  # クラスタ bbox / total_cells
    prev_had_candidates: bool,
    min_cells: int,
) -> str:
    """
    LSC vs ROM の区別:
      cluster_bbox_ratio = (クラスタのバウンディングボックスセル数) / (全グリッドセル数)
      大きなバウンディングボックス → 地形・照明変化（LSC）
      小さなバウンディングボックス → 局所的な物体運動（ROM/PTA）
    """
    has_cand    = n_candidates >= min_cells
    wide_ratio  = n_total_candidates / max(total_valid, 1)

    # 1. STATIC
    if bg_mag < STATIC_BG_THRESH and not has_cand:
        return "STATIC"

    # 2. LIGHTING_SHADOW_CHANGE: クラスタが広域 OR 候補が全体に散在
    # 広い bbox → 地形の照明変化・影変化・ズームが原因
    if has_cand and cluster_bbox_ratio >= BBOX_LSC_RATIO:
        return "LIGHTING_SHADOW_CHANGE"
    if wide_ratio >= LIGHTING_WIDE_RATIO and not has_cand:
        return "LIGHTING_SHADOW_CHANGE"

    # 3. POSSIBLE_TARGET_APPEAR: 前フレーム候補なし → コンパクトな候補出現
    if (not prev_had_candidates) and has_cand:
        return "POSSIBLE_TARGET_APPEAR"

    # 4. POSSIBLE_TARGET_DISAPPEAR: 前フレーム候補あり → 候補消失
    if prev_had_candidates and (not has_cand):
        return "POSSIBLE_TARGET_DISAPPEAR"

    # 5. CAMERA_TRACK: 大きなグローバルシフト + 高均一性
    if bg_mag >= CAMERA_TRACK_BG_MIN and uniformity >= UNIFORMITY_THRESH:
        return "CAMERA_TRACK"

    # 6. RELATIVE_OBJECT_MOTION: コンパクトな候補あり
    if has_cand:
        return "RELATIVE_OBJECT_MOTION"

    # 7. BACKGROUND_FLOW
    if bg_mag >= STATIC_BG_THRESH:
        return "BACKGROUND_FLOW"

    # 8. REVIEW_REQUIRED
    return "REVIEW_REQUIRED"


# ════════════════════════════════════════════════════════════════════════════
# 1ペア解析
# ════════════════════════════════════════════════════════════════════════════

def analyze_pair(
    prev_path: Path,
    curr_path: Path,
    gs: int,
    residual_thresh: float,
    min_cells: int,
    fd_event: str,
    prev_had_candidates: bool,
) -> dict:
    prev = load_gray_uint8(prev_path)
    curr = load_gray_uint8(curr_path)
    h, w = prev.shape

    mask_top = int(h * MASK_EDGE_RATIO)
    mask_bot = int(h * MASK_EDGE_RATIO)

    # ── Step 1: Phase Correlation でグローバルシフト推定 ─────────────────────
    bg_dx, bg_dy = phase_correlation_shift(prev, curr)
    bg_mag = math.sqrt(bg_dx ** 2 + bg_dy ** 2)

    # ── Step 2: 全グリッドセルの残差 MAD 計算 ──────────────────────────────
    candidate_set: set  = set()
    cand_residuals: list = []   # candidate 各セルの残差
    n_valid    = 0
    n_low_res  = 0              # グローバルシフトで「説明できる」セル数

    for gi, gj, y0, x0 in iter_valid_cells(h, w, gs, mask_top, mask_bot):
        block = prev[y0:y0 + gs, x0:x0 + gs]
        # 低コントラスト（空・黒塗り・一様領域）除外
        if float(np.std(block)) < TEXTURE_STD_MIN:
            continue

        rmad = residual_mad(prev, curr, y0, x0, gs, bg_dx, bg_dy)
        if math.isnan(rmad):
            # 境界外 → グローバルシフト適用後にフレーム外 → 候補として記録
            candidate_set.add((gi, gj))
            cand_residuals.append(residual_thresh)  # 境界セルは閾値相当として扱う
            n_valid += 1
            continue

        n_valid += 1
        if rmad < LOW_RES_THRESH:
            n_low_res += 1

        if rmad >= residual_thresh:
            candidate_set.add((gi, gj))
            cand_residuals.append(rmad)

    if n_valid == 0:
        return _null_result(fd_event, "STATIC", False)

    uniformity = n_low_res / n_valid

    # ── Step 3: クラスタリング ──────────────────────────────────────────────
    clusters = cluster_candidates(candidate_set)
    largest  = max(clusters, key=len) if clusters else []
    n_largest = len(largest)

    if n_largest >= min_cells:
        cx, cy = centroid_px(largest, gs)
        cand_dir = spatial_direction(cx, cy, float(w), float(h))
        # 最大クラスタのバウンディングボックス
        gis = [gi for gi, _ in largest]
        gjs = [gj for _, gj in largest]
        bbox_rows = max(gis) - min(gis) + 1
        bbox_cols = max(gjs) - min(gjs) + 1
        total_grid_cells = (h // gs) * (w // gs)
        bbox_ratio = (bbox_rows * bbox_cols) / max(total_grid_cells, 1)
        # 最大クラスタ内の平均残差
        cluster_set = set(map(tuple, largest))
        cluster_residuals = [
            r for (gi, gj), r in zip(candidate_set, cand_residuals)
            if (gi, gj) in cluster_set
        ]
        mean_residual = float(np.mean(cluster_residuals)) if cluster_residuals else 0.0
        n_final = n_largest
    else:
        cx, cy = 0.0, 0.0
        cand_dir = "NONE"
        mean_residual = 0.0
        n_final = 0
        bbox_ratio = 0.0
        total_grid_cells = (h // gs) * (w // gs)

    wide_mean_residual = (
        float(np.mean(cand_residuals)) if cand_residuals else 0.0
    )

    # ── Step 4: イベント分類 ─────────────────────────────────────────────────
    n_total_cands = len(candidate_set)
    event = classify_event(
        bg_mag=bg_mag,
        uniformity=uniformity,
        n_candidates=n_final,
        n_total_candidates=n_total_cands,
        total_valid=n_valid,
        cluster_bbox_ratio=bbox_ratio,
        prev_had_candidates=prev_had_candidates,
        min_cells=min_cells,
    )

    has_cand = n_final >= min_cells

    return {
        "bg_motion_x":         round(float(bg_dx),        2),
        "bg_motion_y":         round(float(bg_dy),        2),
        "bg_motion_magnitude": round(bg_mag,               2),
        "candidate_cells":     n_final,
        "total_valid_cells":   n_valid,
        "candidate_bbox_x":    round(cx,                   1),
        "candidate_bbox_y":    round(cy,                   1),
        "mean_residual_mad":   round(mean_residual,        2),
        "candidate_direction": cand_dir,
        "frame_delta_event":   fd_event,
        "event_type":          event,
        "_has_candidates":     has_cand,
        "_uniformity":         round(uniformity, 3),
        "_wide_residual":      round(wide_mean_residual, 2),
        "_n_all_candidates":   n_total_cands,
        "_bbox_ratio":         round(bbox_ratio, 3),
    }


def _null_result(fd_event: str, event: str, has_cand: bool) -> dict:
    return {
        "bg_motion_x": 0.0, "bg_motion_y": 0.0, "bg_motion_magnitude": 0.0,
        "candidate_cells": 0, "total_valid_cells": 0,
        "candidate_bbox_x": 0.0, "candidate_bbox_y": 0.0,
        "mean_residual_mad": 0.0, "candidate_direction": "NONE",
        "frame_delta_event": fd_event, "event_type": event,
        "_has_candidates": has_cand,
        "_uniformity": 0.0, "_wide_residual": 0.0, "_n_all_candidates": 0,
        "_bbox_ratio": 0.0,
    }


# ════════════════════════════════════════════════════════════════════════════
# Delta CSV ロード
# ════════════════════════════════════════════════════════════════════════════

def load_delta_csv(path: Path) -> dict[int, dict]:
    rows: dict[int, dict] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[int(row["pair_id"])] = row
    return rows


def collect_frames(frames_dir: Path) -> list[Path]:
    return sorted(frames_dir.glob("frame_*.png"), key=lambda p: p.name)


def ts_from_name(name: str) -> float:
    """frame_0183.png → 183.0"""
    return float(int(Path(name).stem.split("_", 1)[1]))


# ════════════════════════════════════════════════════════════════════════════
# サマリー生成
# ════════════════════════════════════════════════════════════════════════════

def build_summary(
    results: list[dict],
    source_id: str,
    article_id: str,
    frames_dir: Path,
    delta_csv: Path,
) -> str:
    counts = Counter(r["event_type"] for r in results)

    lines = [
        "# Motion Intelligence Summary (v1)",
        "",
        f"- 実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- article_id: {article_id}",
        f"- source_id: {source_id}",
        f"- frames_dir: {frames_dir}",
        f"- delta_csv: {delta_csv}",
        f"- 分類器バージョン: {VERSION}",
        f"- 背景推定方式: FFT Phase Correlation（探索窓制限なし）",
        "",
        "---", "",
        "## イベント別件数", "",
        "| イベント | 件数 | 説明 |",
        "|---------|------|------|",
    ]
    for ev, desc in EVENT_DESC.items():
        lines.append(f"| {ev} | {counts.get(ev, 0)} | {desc} |")

    def section(title: str, rows: list[dict], headers: list[str], row_fn):
        lines.append(f"")
        lines.append(f"### {title}")
        if rows:
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("|" + "|".join(["---"] * len(headers)) + "|")
            for r in rows:
                lines.append("| " + " | ".join(row_fn(r)) + " |")
        else:
            lines.append("（なし）")

    lines += ["", "---", "", "## 人間確認推奨フレーム"]

    section(
        "POSSIBLE_TARGET_APPEAR（対象候補出現）",
        [r for r in results if r["event_type"] == "POSSIBLE_TARGET_APPEAR"],
        ["pair_id", "frame_prev", "frame_curr", "ts_prev", "ts_curr", "residual_mad", "pos"],
        lambda r: [
            str(r["pair_id"]), r["frame_prev"], r["frame_curr"],
            f"{r['timestamp_prev_s']}s", f"{r['timestamp_curr_s']}s",
            str(r["mean_residual_mad"]), r["candidate_direction"],
        ],
    )

    section(
        "POSSIBLE_TARGET_DISAPPEAR（対象候補消失）",
        [r for r in results if r["event_type"] == "POSSIBLE_TARGET_DISAPPEAR"],
        ["pair_id", "frame_prev", "frame_curr", "ts_prev", "ts_curr"],
        lambda r: [
            str(r["pair_id"]), r["frame_prev"], r["frame_curr"],
            f"{r['timestamp_prev_s']}s", f"{r['timestamp_curr_s']}s",
        ],
    )

    section(
        "RELATIVE_OBJECT_MOTION（対象候補相対運動）上位10件",
        sorted(
            [r for r in results if r["event_type"] == "RELATIVE_OBJECT_MOTION"],
            key=lambda r: r["mean_residual_mad"], reverse=True,
        )[:10],
        ["pair_id", "frame_prev", "frame_curr", "ts_prev", "ts_curr", "residual_mad", "pos"],
        lambda r: [
            str(r["pair_id"]), r["frame_prev"], r["frame_curr"],
            f"{r['timestamp_prev_s']}s", f"{r['timestamp_curr_s']}s",
            str(r["mean_residual_mad"]), r["candidate_direction"],
        ],
    )

    section(
        "REVIEW_REQUIRED（要人間確認）",
        [r for r in results if r["event_type"] == "REVIEW_REQUIRED"],
        ["pair_id", "ts_prev", "ts_curr", "bg_mag", "uniformity"],
        lambda r: [
            str(r["pair_id"]),
            f"{r['timestamp_prev_s']}s", f"{r['timestamp_curr_s']}s",
            str(r["bg_motion_magnitude"]), str(r.get("_uniformity", "N/A")),
        ],
    )

    lines += ["", "---", "", "## 背景主運動が大きい区間（bg_magnitude 上位10件）", ""]
    top_bg = sorted(results, key=lambda r: r["bg_motion_magnitude"], reverse=True)[:10]
    lines += [
        "| pair_id | ts_prev | ts_curr | bg_dx | bg_dy | bg_mag | uniformity | event_type |",
        "|---------|---------|---------|-------|-------|--------|------------|-----------|",
    ]
    for r in top_bg:
        lines.append(
            f"| {r['pair_id']} | {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s | "
            f"{r['bg_motion_x']} | {r['bg_motion_y']} | {r['bg_motion_magnitude']} | "
            f"{r.get('_uniformity','?')} | {r['event_type']} |"
        )

    lines += ["", "---", "", "## Frame Delta v2 との比較", ""]
    fd_counts = Counter(r["frame_delta_event"] for r in results)
    lines += [
        "| frame_delta_event | 件数 | MI v1 分類（支配的） |",
        "|------------------|------|---------------------|",
    ]
    for fd_ev, cnt in sorted(fd_counts.items(), key=lambda x: -x[1]):
        mi = Counter(
            r["event_type"] for r in results if r["frame_delta_event"] == fd_ev
        ).most_common(1)
        top = mi[0][0] if mi else "N/A"
        lines.append(f"| {fd_ev} | {cnt} | {top} |")

    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════════════════
# 引数解析
# ════════════════════════════════════════════════════════════════════════════

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=f"{VERSION} — 背景運動と対象候補運動の分離（Phase Correlation）"
    )
    p.add_argument("--frames-dir",   required=True, help="adaptive frames ディレクトリ")
    p.add_argument("--delta-csv",    required=True, help="frame_delta_v2.csv パス")
    p.add_argument("--article-id",   required=True, help="記事ID")
    p.add_argument("--source-id",    required=True, help="ソースID")
    p.add_argument("--output-dir",   default="",    help="出力先（省略時: data/motion_intelligence_runs/<今日>/<source_id>/）")
    p.add_argument("--grid-size",    type=int,   default=GRID_SIZE_DEFAULT,
                   help=f"グリッドサイズ px（デフォルト: {GRID_SIZE_DEFAULT}）")
    p.add_argument("--residual-thresh", type=float, default=RESIDUAL_THRESH_DEFAULT,
                   help=f"候補セル判定: 残差 MAD 閾値（デフォルト: {RESIDUAL_THRESH_DEFAULT}）")
    p.add_argument("--min-candidate-cells", type=int, default=MIN_CANDIDATE_CELLS_DEFAULT,
                   help=f"候補クラスタ最小セル数（デフォルト: {MIN_CANDIDATE_CELLS_DEFAULT}）")
    p.add_argument("--execute",  action="store_true", help="実行モード（省略時: dry-run）")
    p.add_argument("--verbose",  action="store_true", help="詳細ログ（全ペア表示）")
    return p.parse_args()


# ════════════════════════════════════════════════════════════════════════════
# メイン
# ════════════════════════════════════════════════════════════════════════════

def main() -> None:
    args = parse_args()
    mode = "EXECUTE" if args.execute else "DRY-RUN"

    frames_dir = Path(args.frames_dir)
    delta_csv  = Path(args.delta_csv)

    if not frames_dir.exists():
        print(f"[ERROR] frames_dir not found: {frames_dir}", file=sys.stderr)
        sys.exit(1)
    if not delta_csv.exists():
        print(f"[ERROR] delta_csv not found: {delta_csv}", file=sys.stderr)
        sys.exit(1)

    if args.output_dir:
        output_dir = Path(args.output_dir) / args.source_id
    else:
        run_date   = date.today().strftime("%Y%m%d")
        output_dir = Path("data") / "motion_intelligence_runs" / run_date / args.source_id

    frames   = collect_frames(frames_dir)
    n_frames = len(frames)
    n_pairs  = n_frames - 1
    if n_frames < 2:
        print("[ERROR] フレームが2枚未満です。", file=sys.stderr)
        sys.exit(1)

    delta_rows = load_delta_csv(delta_csv)

    print(f"[{VERSION}] mode={mode}")
    print(f"  article_id      : {args.article_id}")
    print(f"  source_id       : {args.source_id}")
    print(f"  frames_dir      : {frames_dir}")
    print(f"  delta_csv       : {delta_csv}")
    print(f"  grid_size       : {args.grid_size}px")
    print(f"  residual_thresh : {args.residual_thresh}")
    print(f"  min_cells       : {args.min_candidate_cells}")
    print(f"  背景推定方式    : FFT Phase Correlation")
    print(f"  フレーム数      : {n_frames}")
    print(f"  比較ペア数      : {n_pairs}")
    print(f"  出力先          : {output_dir}/")

    # ── DRY-RUN ──────────────────────────────────────────────────────────────
    if not args.execute:
        print(f"\n[DRY-RUN] 先頭5ペアのみプレビュー実行...")
        prev_had = False
        for i in range(min(5, n_pairs)):
            prev_p = frames[i]
            curr_p = frames[i + 1]
            pid    = i + 1
            fd_ev  = delta_rows.get(pid, {}).get("event_type", "UNKNOWN")
            res = analyze_pair(
                prev_p, curr_p,
                args.grid_size, args.residual_thresh,
                args.min_candidate_cells, fd_ev, prev_had,
            )
            prev_had = res["_has_candidates"]
            ev_s = EVENT_SHORT.get(res["event_type"], res["event_type"])
            print(
                f"  pair {pid:3d}: {prev_p.name} → {curr_p.name}"
                f"  bg=({res['bg_motion_x']:+.0f},{res['bg_motion_y']:+.0f})"
                f"  mag={res['bg_motion_magnitude']:.1f}px"
                f"  uni={res['_uniformity']:.2f}"
                f"  cands={res['candidate_cells']}(tot={res['_n_all_candidates']})"
                f"  bbox={res['_bbox_ratio']:.2f}"
                f"  res={res['mean_residual_mad']:.1f}"
                f"  [{ev_s}] (fd:{fd_ev})"
            )
        print(f"\n[DRY-RUN] 完了（ファイル出力なし）")
        print(f"  実行するには --execute を付けてください。")
        return

    # ── EXECUTE ──────────────────────────────────────────────────────────────
    output_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    prev_had = False

    print(f"\n[1/2] ペア分析中... ({n_pairs}ペア)")

    for i in range(n_pairs):
        prev_p  = frames[i]
        curr_p  = frames[i + 1]
        pair_id = i + 1
        ts_prev = ts_from_name(prev_p.name)
        ts_curr = ts_from_name(curr_p.name)

        fd_ev  = delta_rows.get(pair_id, {}).get("event_type", "UNKNOWN")

        res = analyze_pair(
            prev_p, curr_p,
            args.grid_size, args.residual_thresh,
            args.min_candidate_cells, fd_ev, prev_had,
        )
        prev_had = res["_has_candidates"]

        row = {
            "pair_id":          pair_id,
            "frame_prev":       prev_p.name,
            "frame_curr":       curr_p.name,
            "timestamp_prev_s": ts_prev,
            "timestamp_curr_s": ts_curr,
            **{k: res[k] for k in [
                "bg_motion_x", "bg_motion_y", "bg_motion_magnitude",
                "candidate_cells", "total_valid_cells",
                "candidate_bbox_x", "candidate_bbox_y",
                "mean_residual_mad", "candidate_direction",
                "frame_delta_event", "event_type",
            ]},
            # 内部フィールド（summary 用）
            "_uniformity":      res["_uniformity"],
            "_wide_residual":   res["_wide_residual"],
            "_n_all_candidates": res["_n_all_candidates"],
        }
        results.append(row)

        if args.verbose or pair_id % 20 == 0:
            ev_s = EVENT_SHORT.get(res["event_type"], res["event_type"])
            print(
                f"  {pair_id:3d}/{n_pairs}: "
                f"bg=({res['bg_motion_x']:+.0f},{res['bg_motion_y']:+.0f})"
                f" mag={res['bg_motion_magnitude']:.0f}px"
                f" uni={res['_uniformity']:.2f}"
                f" cands={res['candidate_cells']}"
                f" [{ev_s}]"
            )

    print(f"\n[2/2] 出力中...")

    # CSV（内部フィールド除外）
    with open(output_dir / "motion_events.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for r in results:
            writer.writerow({k: r[k] for k in CSV_FIELDS})

    # JSONL（全フィールド）
    with open(output_dir / "motion_events.jsonl", "w", encoding="utf-8") as f:
        for r in results:
            out = {k: r[k] for k in CSV_FIELDS}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")

    # summary.md
    summary_text = build_summary(
        results, args.source_id, args.article_id, frames_dir, delta_csv
    )
    with open(output_dir / "summary.md", "w", encoding="utf-8") as f:
        f.write(summary_text)

    # ── 結果表示 ─────────────────────────────────────────────────────────────
    counts = Counter(r["event_type"] for r in results)
    print(f"\n[完了] {args.article_id} / {args.source_id}")
    print(f"  総フレーム: {n_frames}  比較ペア: {n_pairs}")
    for ev, desc in EVENT_DESC.items():
        cnt = counts.get(ev, 0)
        if cnt > 0:
            print(f"  {ev:<28}: {cnt:3d}件  ({desc})")
    review = sum(counts.get(e, 0) for e in (
        "POSSIBLE_TARGET_APPEAR", "POSSIBLE_TARGET_DISAPPEAR",
        "RELATIVE_OBJECT_MOTION", "REVIEW_REQUIRED"
    ))
    print(f"  人間確認推奨合計          : {review}件")
    print(f"  出力: {output_dir}/")


if __name__ == "__main__":
    main()
