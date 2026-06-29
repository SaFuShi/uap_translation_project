#!/usr/bin/env python3
"""
camera_analyzer.py — Camera Analyzer (Media Inspector v4 Agent 2)

設計書: docs/media_inspector_v4_architecture.md  §3.5 サンプリング戦略

【サンプリング間隔と検出能力】
  粗パス (3秒間隔):
    - カメラパン方向の推定 ✅
    - FOV変化候補区間の特定 ✅ (hf_ratio 使用、false positive あり)
    - ブラックアウト/ホワイトアウトの直接検出 ⚠️ (3秒未満の事象は検出不能)

  精密パス (0.25〜0.5秒間隔):
    - ブラックアウト/ホワイトアウトの直接検出 ✅
    - FOV切替タイムコードの精密確定 ✅
    → 粗パスで特定した候補区間に対して extract_frames_targeted.py で
      0.25s 間隔フレームを追加抽出し、本スクリプトを再実行すること。

【推奨フロー】
  Step 1: 粗パス実行（本スクリプトを adaptive_frames で実行）
           候補区間: camera_event ∈ {FOV_IN, FOV_OUT, EDGE_SURGE}
  Step 2: 精密フレーム抽出（extract_frames_targeted.py --interval 0.25）
  Step 3: 精密パス実行（本スクリプトを _targeted/ フレームで実行）
  Step 4: 粗パス + 精密パス結果を統合して Motion Intelligence v4 へ
"""
import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

import numpy as np
from PIL import Image

VERSION = "camera_analyzer_v1"

# ── 輝度・マスク ────────────────────────────────────────────────
BLACK_THRESH  = 15     # 有効ピクセル下限（マスク生成）
BLACKOUT_BRIGHT = 10   # フレーム平均輝度 < この値 → BLACKOUT
WHITEOUT_BRIGHT = 245  # フレーム平均輝度 > この値 → WHITEOUT

# ── FOV 変化（空間周波数比） ────────────────────────────────────
# spatial_freq_ratio(curr) / spatial_freq_ratio(prev) のしきい値
# ・ズームイン: 被写体が拡大 → テクスチャが粗くなる → 高周波成分が増える
# ・ズームアウト: 被写体が縮小 → テクスチャが細かくなる → 高周波成分が減る
#
# PR062 での実測値:
#   全ペア hf_ratio 分布: mean=1.19, std=0.72, 95th=2.60, 99th=3.11
#   地形テクスチャの自然変化でも ratio=2〜3 が生じるため信頼度は低め (0.40)
#   FOV_IN  しきい値=2.00: GT ZIN@52s(2.85) ✓ / GT ZIN@124s(2.14) ✓
#   FOV_OUT しきい値=0.40: 自然変化の下位 3% 以下のみ捕捉
FOV_IN_RATIO   = 2.00  # hf_ratio > これ → FOV_IN (ズームイン方向)
FOV_OUT_RATIO  = 0.40  # hf_ratio < これ → FOV_OUT (ズームアウト方向)
FOV_MIN_HF     = 0.030 # 比計算に使う最低 hf（ゼロ除算・ノイズ回避）
FOV_CONF       = 0.40  # FOV 系イベントのベース confidence（ノイズが多いため低め）

# ── エッジ密度急増（ブラックアウト復帰 / 大きな切り替え後） ──
EDGE_SURGE_RATIO = 3.0  # ed_curr/ed_prev > これ → EDGE_SURGE
EDGE_MIN_CURR    = 0.015 # EDGE_SURGE の最低 ed 値（ノイズ排除）
EDGE_SURGE_CONF  = 0.55

# ── カメラパン（位相相関） ──────────────────────────────────────
PAN_MIN_PX      = 15   # パンとみなす最低変位 (px)
PAN_MAX_PX      = 80   # これ以上の変位は位相相関の誤ピーク疑い (unreliable)
PAN_CONF_MIN    = 0.25 # パン判定に使う最低 phase-corr confidence
CENTER_EXCL_FRAC = 0.40 # 中心除外率（クロスヘア除外のため）

# ── CSV 列 ──────────────────────────────────────────────────────
CSV_FIELDS = [
    "pair_id", "frame_prev", "frame_curr", "timestamp_s",
    "camera_event",
    "cam_dx_px", "cam_dy_px", "pan_confidence",
    "hf_prev", "hf_curr", "hf_ratio",
    "ed_prev", "ed_curr", "ed_ratio",
    "brightness_prev", "brightness_curr",
    "blackout_curr", "whiteout_curr",
    "camera_confidence",
    "camera_notes",
]

# ── 検出限界の説明 ───────────────────────────────────────────────
DETECTION_LIMITS = (
    "3秒サンプリング時の検出限界: ブラックアウト/ホワイトアウトが3秒未満の場合、"
    "サンプルフレームに現れず直接検出不能。FOV切替は空間周波数比の変化で検出するが、"
    "地形テクスチャの自然変化と混同する場合がある。"
)

# ── ユーティリティ ───────────────────────────────────────────────

def load_rgb(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"), dtype=np.uint8)


def to_gray(rgb: np.ndarray) -> np.ndarray:
    return (
        0.299 * rgb[:, :, 0]
        + 0.587 * rgb[:, :, 1]
        + 0.114 * rgb[:, :, 2]
    ).astype(np.uint8)


def build_valid_mask(gray: np.ndarray) -> np.ndarray:
    return gray > BLACK_THRESH


def mean_brightness(gray: np.ndarray, mask: np.ndarray) -> float:
    valid = gray[mask]
    return float(np.mean(valid)) if valid.size > 0 else 0.0


# ── 空間周波数比（scene_analyzer と同アルゴリズム） ──────────────

def _spatial_freq_ratio(gray: np.ndarray, mask: np.ndarray, crop_size: int = 256) -> float:
    h, w = gray.shape
    cy, cx = h // 2, w // 2
    half = crop_size // 2
    y0 = max(cy - half, 0)
    x0 = max(cx - half, 0)
    crop = gray[y0:y0 + crop_size, x0:x0 + crop_size].astype(np.float32)
    crop_mask = mask[y0:y0 + crop_size, x0:x0 + crop_size]

    valid = crop[crop_mask]
    if valid.size < crop_size * crop_size * 0.20:
        return 0.0

    crop[~crop_mask] = float(np.mean(valid))
    crop -= crop.mean()

    fft_shifted = np.fft.fftshift(np.fft.fft2(crop))
    power = np.abs(fft_shifted) ** 2

    ch, cw = crop.shape
    y_idx, x_idx = np.mgrid[0:ch, 0:cw]
    max_dist = min(ch, cw) / 2.0
    dist = np.sqrt((y_idx - ch / 2.0) ** 2 + (x_idx - cw / 2.0) ** 2)

    lo_mask = (dist > 1) & (dist <= max_dist * 0.20)
    hi_mask = dist > max_dist * 0.35

    lo_power = float(np.sum(power[lo_mask]))
    hi_power = float(np.sum(power[hi_mask]))
    total = lo_power + hi_power
    return float(hi_power / total) if total > 1e-10 else 0.0


# ── Sobel エッジ密度（scene_analyzer と同アルゴリズム） ──────────

def _sobel_edge_density(gray: np.ndarray, mask: np.ndarray) -> float:
    img = gray.astype(np.float32)

    gx = (
        -img[:-2, :-2] + img[:-2, 2:]
        - 2 * img[1:-1, :-2] + 2 * img[1:-1, 2:]
        - img[2:, :-2] + img[2:, 2:]
    )
    gy = (
        -img[:-2, :-2] - 2 * img[:-2, 1:-1] - img[:-2, 2:]
        + img[2:, :-2] + 2 * img[2:, 1:-1] + img[2:, 2:]
    )
    magnitude = np.sqrt(gx ** 2 + gy ** 2)

    m = mask.astype(np.float32)
    neigh = (
        m[:-2, :-2] + m[:-2, 1:-1] + m[:-2, 2:]
        + m[1:-1, :-2] + m[1:-1, 1:-1] + m[1:-1, 2:]
        + m[2:, :-2] + m[2:, 1:-1] + m[2:, 2:]
    )
    safe = neigh == 9

    valid_mag = magnitude[safe]
    if valid_mag.size == 0:
        return 0.0
    return float(np.mean(valid_mag) / 1442.0)


# ── 位相相関（中心クロスヘア除外版） ────────────────────────────

def phase_correlation_outer(
    gray1: np.ndarray,
    gray2: np.ndarray,
    mask1: np.ndarray,
    mask2: np.ndarray,
    center_excl: float = CENTER_EXCL_FRAC,
    max_shift: float = 0.25,
) -> tuple:
    """
    中央 center_excl 割合を除外して位相相関でカメラパンを推定する。

    クロスヘア (UI) が中心に固定されているとフレーム全体では
    常に dx=0 がピークになる。外縁部分のみで計算することで回避する。

    Returns:
        dx (int): 背景の水平変位 (正=右移動 → カメラは左パン)
        dy (int): 背景の垂直変位 (正=下移動 → カメラは上チルト)
        confidence (float): 0-1 の信頼度
    """
    h, w = gray1.shape
    cy, cx = h // 2, w // 2
    ey = int(h * center_excl / 2)
    ex = int(w * center_excl / 2)

    def fill_center(gray, mask):
        f = gray.astype(np.float32)
        # 中心除外マスク
        outer = np.ones((h, w), dtype=bool)
        outer[cy - ey:cy + ey, cx - ex:cx + ex] = False
        valid = mask & outer
        mu = float(np.mean(f[valid])) if valid.any() else 128.0
        f[~mask] = mu
        f[cy - ey:cy + ey, cx - ex:cx + ex] = mu  # 中心を平均で埋める
        return f

    i1 = fill_center(gray1, mask1)
    i2 = fill_center(gray2, mask2)

    # Hann ウィンドウ
    wy = np.hanning(h).reshape(-1, 1)
    wx = np.hanning(w).reshape(1, -1)
    win = wy * wx
    i1 = i1 * win
    i2 = i2 * win

    F1 = np.fft.fft2(i1)
    F2 = np.fft.fft2(i2)
    cross = F1 * np.conj(F2)
    cross /= np.abs(cross) + 1e-10
    corr = np.real(np.fft.ifft2(cross))
    corr_s = np.fft.fftshift(corr)

    mdy = max(1, int(h * max_shift))
    mdx = max(1, int(w * max_shift))
    y0 = max(cy - mdy, 0)
    y1 = min(cy + mdy + 1, h)
    x0 = max(cx - mdx, 0)
    x1 = min(cx + mdx + 1, w)
    search = corr_s[y0:y1, x0:x1]

    if search.size == 0:
        return 0, 0, 0.0

    py, px = np.unravel_index(np.argmax(search), search.shape)
    peak_val = float(search[py, px])
    mean_abs = float(np.mean(np.abs(corr_s)))
    confidence = float(np.clip(peak_val / (mean_abs + 1e-10) / 30.0, 0.0, 1.0))

    dy = (y0 + py) - cy
    dx = (x0 + px) - cx

    return int(dx), int(dy), confidence


# ── イベント分類 ─────────────────────────────────────────────────

def classify_camera_event(
    blackout_curr: bool,
    whiteout_curr: bool,
    hf_prev: float,
    hf_curr: float,
    ed_prev: float,
    ed_curr: float,
    cam_dx: int,
    cam_dy: int,
    pan_conf: float,
) -> tuple:
    """
    Returns (camera_event, confidence, notes_list)
    """
    notes = []
    events = []

    # ① ブラックアウト / ホワイトアウト
    if blackout_curr:
        events.append("BLACKOUT")
        notes.append("現フレームが全黒（ブラックアウト）")
    if whiteout_curr:
        events.append("WHITEOUT")
        notes.append("現フレームが全白（ホワイトアウト）")

    # ② FOV変化（空間周波数比）
    hf_ratio = 0.0
    if hf_prev >= FOV_MIN_HF and hf_curr >= FOV_MIN_HF:
        hf_ratio = hf_curr / hf_prev
        if hf_ratio > FOV_IN_RATIO:
            events.append("FOV_IN")
            notes.append(
                f"高周波比↑ ({hf_prev:.3f}→{hf_curr:.3f} ×{hf_ratio:.2f}): ズームイン方向 FOV 変化候補"
                "（地形テクスチャ変化との混同注意・要目視確認）"
            )
        elif hf_ratio < FOV_OUT_RATIO:
            events.append("FOV_OUT")
            notes.append(
                f"高周波比↓ ({hf_prev:.3f}→{hf_curr:.3f} ×{hf_ratio:.2f}): ズームアウト方向 FOV 変化候補"
                "（地形テクスチャ変化との混同注意・要目視確認）"
            )
    else:
        notes.append(f"hf 値が低いため FOV 比較スキップ (prev={hf_prev:.3f}, curr={hf_curr:.3f})")

    # ③ エッジ密度急増（ブラックアウト復帰・シーン急変後）
    ed_ratio = 0.0
    if ed_prev > 0 and ed_curr >= EDGE_MIN_CURR:
        ed_ratio = ed_curr / ed_prev
        if ed_ratio > EDGE_SURGE_RATIO:
            events.append("EDGE_SURGE")
            notes.append(
                f"エッジ密度急増 ({ed_prev:.4f}→{ed_curr:.4f} ×{ed_ratio:.1f}): シーン急変またはFOV切替後"
            )

    # ④ カメラパン / チルト（位相相関）
    # FOV 変化検出時は位相相関が不安定になるため PAN/TILT 判定をスキップ
    fov_detected = any(e in ("FOV_IN", "FOV_OUT") for e in events)
    if pan_conf >= PAN_CONF_MIN and not fov_detected:
        disp = max(abs(cam_dx), abs(cam_dy))
        if PAN_MIN_PX <= disp <= PAN_MAX_PX:
            if abs(cam_dx) >= abs(cam_dy):
                events.append("PAN")
                notes.append(f"カメラパン dx={cam_dx:+d}px (conf={pan_conf:.2f})")
            else:
                events.append("TILT")
                notes.append(f"カメラチルト dy={cam_dy:+d}px (conf={pan_conf:.2f})")
        elif disp > PAN_MAX_PX:
            notes.append(
                f"変位過大 ({cam_dx:+d},{cam_dy:+d}px): 位相相関の誤ピーク疑い・MI v4 では利用しない"
            )

    # ⑤ 統合判定
    if not events:
        return "STATIC", 0.80, ["前後フレーム間で有意な変化なし"]

    if len(events) == 1:
        ev = events[0]
        if ev in ("BLACKOUT", "WHITEOUT"):
            conf = 0.95
        elif ev in ("FOV_IN", "FOV_OUT"):
            conf = FOV_CONF
        elif ev == "EDGE_SURGE":
            conf = EDGE_SURGE_CONF
        elif ev in ("PAN", "TILT"):
            conf = min(pan_conf, 0.70)
        else:
            conf = 0.45
        return ev, conf, notes

    # 複数イベント
    # 優先度: BLACKOUT/WHITEOUT > FOV > EDGE_SURGE > PAN/TILT
    priority = {"BLACKOUT": 5, "WHITEOUT": 5, "FOV_IN": 4, "FOV_OUT": 4,
                "EDGE_SURGE": 3, "PAN": 2, "TILT": 2}
    primary = max(events, key=lambda e: priority.get(e, 0))
    conf = max(FOV_CONF, EDGE_SURGE_CONF) if len(events) > 1 else 0.50
    return "COMBINED", conf, notes


# ── フレームペア解析 ─────────────────────────────────────────────

def analyze_pair(
    prev_path: Path,
    curr_path: Path,
    pair_id: int,
) -> dict:
    prev_rgb = load_rgb(prev_path)
    curr_rgb = load_rgb(curr_path)

    prev_gray = to_gray(prev_rgb)
    curr_gray = to_gray(curr_rgb)

    mask_prev = build_valid_mask(prev_gray)
    mask_curr = build_valid_mask(curr_gray)

    br_prev = mean_brightness(prev_gray, mask_prev)
    br_curr = mean_brightness(curr_gray, mask_curr)

    blackout_curr = br_curr < BLACKOUT_BRIGHT
    whiteout_curr = br_curr > WHITEOUT_BRIGHT

    hf_prev = _spatial_freq_ratio(prev_gray, mask_prev)
    hf_curr = _spatial_freq_ratio(curr_gray, mask_curr)

    ed_prev = _sobel_edge_density(prev_gray, mask_prev)
    ed_curr = _sobel_edge_density(curr_gray, mask_curr)

    cam_dx, cam_dy, pan_conf = phase_correlation_outer(
        prev_gray, curr_gray, mask_prev, mask_curr
    )

    camera_event, cam_conf, notes = classify_camera_event(
        blackout_curr, whiteout_curr,
        hf_prev, hf_curr,
        ed_prev, ed_curr,
        cam_dx, cam_dy, pan_conf,
    )

    hf_ratio = (hf_curr / hf_prev) if hf_prev >= FOV_MIN_HF else 0.0
    ed_ratio = (ed_curr / ed_prev) if ed_prev > 0 else 0.0

    ts = _ts_from_name(curr_path.name)

    return {
        "pair_id":          pair_id,
        "frame_prev":       prev_path.name,
        "frame_curr":       curr_path.name,
        "timestamp_s":      ts,
        "camera_event":     camera_event,
        "cam_dx_px":        cam_dx,
        "cam_dy_px":        cam_dy,
        "pan_confidence":   round(pan_conf, 3),
        "hf_prev":          round(hf_prev, 5),
        "hf_curr":          round(hf_curr, 5),
        "hf_ratio":         round(hf_ratio, 3),
        "ed_prev":          round(ed_prev, 5),
        "ed_curr":          round(ed_curr, 5),
        "ed_ratio":         round(ed_ratio, 3),
        "brightness_prev":  round(br_prev, 1),
        "brightness_curr":  round(br_curr, 1),
        "blackout_curr":    blackout_curr,
        "whiteout_curr":    whiteout_curr,
        "camera_confidence": round(cam_conf, 3),
        "camera_notes":     "; ".join(notes),
    }


def _ts_from_name(name: str) -> float:
    """
    フレームファイル名からタイムスタンプ（秒）を返す。
      frame_00025.png   → 25.0  秒
      frame_000250d.png → 25.0  秒  (1/10 秒単位の "d" サフィックス → /10)
    """
    stem = Path(name).stem
    suffix_d = stem.endswith("d")
    nums = "".join(c for c in stem if c.isdigit())
    if not nums:
        return 0.0
    n = int(nums)
    return round(n / 10.0, 3) if suffix_d else float(n)


# ── サマリー生成 ─────────────────────────────────────────────────

def build_summary(
    results: list,
    source_id: str,
    article_id: str,
    frames_dir: Path,
) -> str:
    n = len(results)
    event_counts = Counter(r["camera_event"] for r in results)
    non_static = [r for r in results if r["camera_event"] != "STATIC"]
    blackout_rows = [r for r in results if r["blackout_curr"]]
    whiteout_rows = [r for r in results if r["whiteout_curr"]]
    fov_in_rows   = [r for r in results if "FOV_IN" in r["camera_event"]]
    fov_out_rows  = [r for r in results if "FOV_OUT" in r["camera_event"]]
    edge_rows     = [r for r in results if "EDGE_SURGE" in r["camera_event"]]
    combined_rows = [r for r in results if r["camera_event"] == "COMBINED"]

    # パン統計
    pan_xs = [r["cam_dx_px"] for r in results if r["pan_confidence"] >= PAN_CONF_MIN]
    pan_ys = [r["cam_dy_px"] for r in results if r["pan_confidence"] >= PAN_CONF_MIN]
    mean_dx = float(np.mean(pan_xs)) if pan_xs else 0.0
    mean_dy = float(np.mean(pan_ys)) if pan_ys else 0.0

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Camera Analyzer Summary",
        "",
        f"- 実行日時   : {now}",
        f"- article_id : {article_id}",
        f"- source_id  : {source_id}",
        f"- frames_dir : {frames_dir}",
        f"- 分類器     : {VERSION}",
        f"- 解析ペア数 : {n}",
        "",
        "---",
        "",
        "## カメライベント 集計",
        "",
        "| camera_event | 件数 | 割合 |",
        "|-------------|------|------|",
    ]
    for ev, cnt in sorted(event_counts.items(), key=lambda x: -x[1]):
        pct = cnt / n * 100
        lines.append(f"| {ev} | {cnt} | {pct:.1f}% |")

    lines += [
        "",
        "## 検出イベント詳細",
        "",
    ]

    def _event_table(rows, label, cols=None):
        if not rows:
            return [f"**{label}**: 検出なし", ""]
        out = [f"**{label}** ({len(rows)} 件)", ""]
        out += ["| 時刻 (s) | フレーム | camera_event | 指標 | notes |",
                "|---------|---------|-------------|------|-------|"]
        for r in sorted(rows, key=lambda x: x["timestamp_s"]):
            metric = ""
            if "hf_ratio" in r and r["hf_ratio"] > 0:
                metric += f"hf_ratio={r['hf_ratio']:.2f} "
            if "ed_ratio" in r and r["ed_ratio"] > 0:
                metric += f"ed_ratio={r['ed_ratio']:.1f}"
            note = r["camera_notes"][:60] + ("…" if len(r["camera_notes"]) > 60 else "")
            out.append(
                f"| {r['timestamp_s']:.2f} | {r['frame_curr']} "
                f"| {r['camera_event']} | {metric.strip()} | {note} |"
            )
        out.append("")
        return out

    lines += _event_table(blackout_rows, "BLACKOUT 検出")
    lines += _event_table(whiteout_rows, "WHITEOUT 検出")
    lines += _event_table(fov_in_rows, "FOV_IN 検出（ズームイン方向）")
    lines += _event_table(fov_out_rows, "FOV_OUT 検出（ズームアウト方向）")
    lines += _event_table(edge_rows, "EDGE_SURGE 検出（エッジ密度急増）")
    lines += _event_table(combined_rows, "COMBINED 検出（複合イベント）")

    # パン統計
    lines += [
        "## カメラパン統計",
        "",
        f"- 解析ペア数 (pan_conf ≥ {PAN_CONF_MIN:.2f}): {len(pan_xs)} 件",
        f"- 平均背景変位 dx={mean_dx:+.1f}px, dy={mean_dy:+.1f}px",
        "",
        "> 正の dx = 背景が右へ移動 = カメラが左へパン（UAP が左方向へ移動中に追跡している場合に発生）",
        "> 正の dy = 背景が下へ移動 = カメラが上へチルト",
        "",
    ]

    # PR062 Ground Truth 比較
    lines += [
        "## PR062 期待値との比較（Ground Truth 対応）",
        "",
        "| GT イベント | 期待検出 | 本結果 | 判定 |",
        "|-----------|---------|--------|------|",
    ]
    gt_checks = [
        (27, "FOV_SWITCH@25s (ワイド切替)", {"FOV_IN", "FOV_OUT", "COMBINED"}),
        (54, "ZOOM_IN@52s (ズーム画角)", {"FOV_IN", "COMBINED"}),
        (126, "ZOOM_IN@124s (ズーム画角)", {"FOV_IN", "COMBINED"}),
        (249, "ZOOM_OUT@249s (望遠→ワイド)", {"FOV_OUT", "COMBINED"}),
        (252, "ZOOM_OUT@249s (望遠→ワイド)", {"FOV_OUT", "COMBINED"}),
        (258, "BLACKOUT+WHITEOUT@256s", {"BLACKOUT", "WHITEOUT", "EDGE_SURGE", "COMBINED"}),
    ]
    ts_map = {r["timestamp_s"]: r for r in results}
    for ts, label, expected_events in gt_checks:
        r = ts_map.get(ts)
        if r is None:
            lines.append(f"| {label} | {', '.join(expected_events)} | フレームなし | — |")
            continue
        detected = r["camera_event"]
        matched = any(e in detected for e in expected_events)
        mark = "✅" if matched else "⚠️"
        lines.append(f"| {label} | {', '.join(sorted(expected_events))} | {detected} | {mark} |")

    lines += [
        "",
        "## 検出限界 (3秒サンプリング)",
        "",
        f"> {DETECTION_LIMITS}",
        "",
        "## Motion Intelligence v4 連携メモ",
        "",
        "- `cam_dx_px`, `cam_dy_px`: フレームペアごとの背景変位推定。MI v4 の `camera_compensated` モード入力として利用可能。",
        "- `camera_event = FOV_IN / FOV_OUT / COMBINED`: 当該ペアの Motion 解析を **スキップまたは要注意** とマーク推奨。",
        "- `camera_event = STATIC / PAN / TILT` かつ `pan_confidence ≥ 0.5`: 信頼できるパン補正ベクトルとして利用可能。",
    ]

    return "\n".join(lines) + "\n"


# ── フレーム収集 ─────────────────────────────────────────────────

def collect_frames(frames_dir: Path) -> list:
    return sorted(frames_dir.glob("frame_*.png"))


# ── CLI ─────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description=f"{VERSION}: カメライベント解析")
    p.add_argument("--frames-dir",  required=True, type=Path,
                   help="frame_*.png が入ったディレクトリ")
    p.add_argument("--source-id",   required=True,
                   help="例: DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1")
    p.add_argument("--article-id",  required=True,
                   help="例: R02-054")
    p.add_argument("--output-dir",  type=Path,
                   help="出力先 (省略時: data/media_inspector_runs/<today>/<source_id>/camera_analysis/)")
    p.add_argument("--execute",     action="store_true",
                   help="ファイル出力あり（省略時は dry-run）")
    p.add_argument("--verbose",     action="store_true",
                   help="全ペアの詳細ログを表示")
    return p.parse_args()


def main():
    args = parse_args()
    frames_dir = args.frames_dir
    if not frames_dir.exists():
        sys.exit(f"[ERROR] frames_dir が見つかりません: {frames_dir}")

    run_date = date.today().strftime("%Y%m%d")

    if args.output_dir:
        out_dir = args.output_dir
    else:
        out_dir = (
            Path("data/media_inspector_runs")
            / run_date / args.source_id / "camera_analysis"
        )

    frames = collect_frames(frames_dir)
    n = len(frames)
    if n < 2:
        sys.exit("[ERROR] frame_*.png が 2 枚以上必要です")

    n_pairs = n - 1
    mode_label = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"[{VERSION}] mode={mode_label}")
    print(f"  article_id  : {args.article_id}")
    print(f"  source_id   : {args.source_id}")
    print(f"  frames_dir  : {frames_dir}")
    print(f"  フレーム数  : {n}  →  ペア数: {n_pairs}")
    print(f"  出力先      : {out_dir}/")
    print()

    # ── DRY-RUN ────────────────────────────────────────────────
    if not args.execute:
        print("[DRY-RUN] 先頭 5 ペアをプレビュー...")
        for i in range(min(5, n_pairs)):
            r = analyze_pair(frames[i], frames[i + 1], i)
            print(
                f"  pair_{i:03d}: {r['frame_prev']}→{r['frame_curr']}"
                f"  event={r['camera_event']:<14}"
                f"  hf_ratio={r['hf_ratio']:.2f}"
                f"  ed_ratio={r['ed_ratio']:.2f}"
                f"  pan=({r['cam_dx_px']:+d},{r['cam_dy_px']:+d})"
                f"  conf={r['camera_confidence']:.2f}"
            )
        print()
        print(f"[DRY-RUN] 完了。--execute を付けると全 {n_pairs} ペアを処理・出力します。")
        return

    # ── EXECUTE ────────────────────────────────────────────────
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    print(f"[1/2] 全ペア解析中 ({n_pairs} ペア)...")
    for i in range(n_pairs):
        r = analyze_pair(frames[i], frames[i + 1], i)
        results.append(r)

        if args.verbose or i % 20 == 0 or i == 0:
            print(
                f"  pair_{i:03d}: {r['frame_curr']}"
                f"  {r['camera_event']:<14}"
                f"  hf={r['hf_ratio']:.2f}"
                f"  ed={r['ed_ratio']:.2f}"
                f"  pan=({r['cam_dx_px']:+d},{r['cam_dy_px']:+d})"
                f"  conf={r['camera_confidence']:.2f}"
            )

    print(f"\n[2/2] ファイル出力中...")

    # CSV
    csv_path = out_dir / "camera_events.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in results:
            w.writerow({k: r[k] for k in CSV_FIELDS})

    # サマリー
    summary_txt = build_summary(results, args.source_id, args.article_id, frames_dir)
    md_path = out_dir / "camera_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(summary_txt)

    # メタデータ JSON
    event_counts = Counter(r["camera_event"] for r in results)
    non_static = [r for r in results if r["camera_event"] != "STATIC"]
    notable_events = [
        {"timestamp_s": r["timestamp_s"], "camera_event": r["camera_event"],
         "hf_ratio": r["hf_ratio"], "ed_ratio": r["ed_ratio"]}
        for r in non_static
    ]
    pan_xs = [r["cam_dx_px"] for r in results if r["pan_confidence"] >= PAN_CONF_MIN]
    pan_ys = [r["cam_dy_px"] for r in results if r["pan_confidence"] >= PAN_CONF_MIN]
    meta = {
        "version":           VERSION,
        "run_date":          date.today().isoformat(),
        "source_id":         args.source_id,
        "article_id":        args.article_id,
        "n_frames":          n,
        "n_pairs":           n_pairs,
        "event_counts":      dict(event_counts),
        "blackout_detected": any(r["blackout_curr"] for r in results),
        "whiteout_detected": any(r["whiteout_curr"] for r in results),
        "fov_in_count":      sum(1 for r in results if "FOV_IN" in r["camera_event"]),
        "fov_out_count":     sum(1 for r in results if "FOV_OUT" in r["camera_event"]),
        "edge_surge_count":  sum(1 for r in results if "EDGE_SURGE" in r["camera_event"]),
        "pan_mean_dx":       round(float(np.mean(pan_xs)), 1) if pan_xs else 0.0,
        "pan_mean_dy":       round(float(np.mean(pan_ys)), 1) if pan_ys else 0.0,
        "notable_events":    notable_events,
        "detection_limits":  DETECTION_LIMITS,
    }
    with open(out_dir / "camera_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # 集計表示
    print()
    print("[完了] camera_event 集計:")
    for ev, cnt in sorted(event_counts.items(), key=lambda x: -x[1]):
        pct = cnt / n_pairs * 100
        print(f"  {ev:<16}: {cnt:3d} 件 ({pct:.1f}%)")
    print(f"\n  出力: {out_dir}/")
    print(f"  CSV : {csv_path}")
    print(f"  MD  : {md_path}")


if __name__ == "__main__":
    main()
