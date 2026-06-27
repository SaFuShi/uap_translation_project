#!/usr/bin/env python3
"""
frame_delta_v2.py

Adaptive Frame ディレクトリ内の連続フレームを比較し、
フレーム間の差分・変化イベント・輝点移動を分析する。
v1 (frame_delta_analyzer.py) からの主な変更点:

  v1 の問題:
    mean_diff >= 35 だけで CUT と判定していたため、
    大型・高輝度オブジェクト（bc > 5000）が移動する際の高 mean_diff を
    CUT と誤分類していた（PR060 で CUT=41 の誤検出を確認）。

  v2 の改善:
    1. CUT = brightness急変 AND object_track不可 AND scene_structure破綻 の3条件AND
       → 大型オブジェクト移動によるCUT誤分類を根本解決
    2. 新分類: ZOOM_BLOOM（輝度の急激な拡大/縮小）を追加
    3. CAMERA_MOTION を CAMERA_TRACK にリネーム
    4. bc は CUT 判定基準に直接使用しない（OBJECT_TRACKING 補助のみ）
    5. APPEAR/DISAPPEAR に「相対的 APPEAR」を追加
       （bc_prev が非ゼロでも bc_curr が20倍以上増 → APPEAR）

使用方法:
  python3 scripts/frame_delta_v2.py \\
    --frames-dir data/adaptive_frames/20260627/<slug>/ \\
    --article-id R02-052 \\
    --source-id DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2 \\
    --output-dir data/frame_delta_runs/20260627_v2/ \\
    [--ts-mode seconds] \\
    [--execute]

--execute なし: dry-run（読み込み対象と出力予定のみ確認）
--execute あり: CSV / JSONL / summary.md を生成
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError:
    print("ERROR: Pillow が必要です: pip install pillow", file=sys.stderr)
    sys.exit(1)

# ============================================================
# v2 閾値定数
# ============================================================

# 輝点（bright pixel）検出
BRIGHT_PX_TH        = 220    # 輝点とみなす輝度閾値（0-255）
BRIGHT_COUNT_MIN    =  20    # 輝点ピクセル数がこれ未満 → 「輝点なし」と判定

# STATIC
STATIC_THRESHOLD    =  2.0   # mean_diff < → STATIC

# APPEAR / DISAPPEAR
APPEAR_RATIO        =  4.0   # bc_curr >= BRIGHT_COUNT_MIN * APPEAR_RATIO → APPEAR（標準）
APPEAR_BC_RATIO     = 20.0   # bc_curr / bc_prev >= この倍率 → 相対的APPEAR
DISAPPEAR_RATIO     =  0.25  # bc_curr < bc_prev * この比率 → DISAPPEAR

# ZOOM_BLOOM: 輝度の急激な拡大（bloom/露出）または縮小（zoom-out）
ZOOM_BLOOM_EXPAND   =  5.0   # bc_curr/bc_prev がこの倍率以上 → ZOOM_BLOOM（拡大）
ZOOM_BLOOM_STABLE   = 80.0   # ZOOM_BLOOM 判定時の centroid 最大移動量(px)
ZOOM_BLOOM_DIFF_MIN =  5.0   # ZOOM_BLOOM に必要な最小 mean_diff

# CUT（3条件 AND）
# 条件A: brightness急変
CUT_ABS_THRESHOLD   = 30.0   # mean_diff ≥ → brightness急変
# 条件B: object_track不可 → prev_has / curr_has で判定（bc補助使用は許容）
# 条件C: scene_structure破綻（変化が広域的・非局所集中）
CUT_CONC_THRESHOLD  =  5.5   # conc < → scene_structure破綻

# OBJECT_MOVE
OBJECT_MOVE_MIN_PX  =  5.0   # pos_delta ≥ → OBJECT_MOVE（centroid 移動あり）
OBJECT_THRESHOLD    =  3.0   # 輝点ありでpos_delta不明でもmean_diff≥ならOBJECT_MOVE

# CAMERA_TRACK: 対象物 centroid が安定し、背景が移動
CAMERA_STABLE_PX    =  5.0   # centroid 移動量がこれ未満 → 対象物は安定（カメラ追従）
CAMERA_THRESHOLD    =  5.0   # mean_diff ≥ → CAMERA_TRACK（背景移動あり）

# ホットスポット検出
GRID_N              =  4     # グリッド分割数（N×N）


# ============================================================
# フレーム単体の特徴量
# ============================================================

def count_bright_pixels(img_gray: Image.Image) -> int:
    """閾値以上の輝度ピクセル数（高速: point + histogram）"""
    mask = img_gray.point(lambda v: 255 if v >= BRIGHT_PX_TH else 0, "1")
    return mask.histogram()[255]


def bright_centroid(img_gray: Image.Image, bc: int) -> tuple:
    """
    輝度閾値以上のピクセルの重心座標を返す。
    輝点が BRIGHT_COUNT_MIN 未満の場合は (None, None)。
    """
    if bc < BRIGHT_COUNT_MIN:
        return None, None
    w, h = img_gray.size
    data = img_gray.getdata()
    sx = sy = cnt = 0
    for i, v in enumerate(data):
        if v >= BRIGHT_PX_TH:
            sx += i % w
            sy += i // w
            cnt += 1
    if cnt == 0:
        return None, None
    return sx // cnt, sy // cnt


def analyze_frame(path: Path) -> dict:
    """フレーム1枚の特徴量を計算してキャッシュ用 dict を返す。"""
    img = Image.open(path).convert("L")
    bc  = count_bright_pixels(img)
    cx, cy = bright_centroid(img, bc)
    return {"img": img, "bc": bc, "cx": cx, "cy": cy}


# ============================================================
# フレームペア差分分析
# ============================================================

def find_hotspot_grid(diff: Image.Image, n: int = GRID_N) -> tuple:
    """差分画像を n×n グリッドに分割し、最大平均差分タイルの中心座標と mean を返す。"""
    w, h = diff.size
    tw, th = max(w // n, 1), max(h // n, 1)
    best_mean, best_cx, best_cy = -1.0, w // 2, h // 2
    for gy in range(n):
        for gx in range(n):
            x1 = gx * tw
            y1 = gy * th
            x2 = min(x1 + tw, w)
            y2 = min(y1 + th, h)
            tile = diff.crop((x1, y1, x2, y2))
            m = ImageStat.Stat(tile).mean[0]
            if m > best_mean:
                best_mean = m
                best_cx = (x1 + x2) // 2
                best_cy = (y1 + y2) // 2
    return best_cx, best_cy, round(best_mean, 2)


def analyze_pair(fa: dict, fb: dict) -> dict:
    """2フレームの特徴量 dict を受け取り、差分メトリクスを返す。"""
    img_a, img_b = fa["img"], fb["img"]

    diff  = ImageChops.difference(img_a, img_b)
    stat  = ImageStat.Stat(diff)

    mean_diff = round(stat.mean[0],   3)
    std_diff  = round(stat.stddev[0], 3)
    max_diff  = int(diff.getextrema()[1])

    w, h = diff.size
    cx1, cy1, cx2, cy2 = w // 4, h // 4, 3 * w // 4, 3 * h // 4
    center_stat = ImageStat.Stat(diff.crop((cx1, cy1, cx2, cy2)))
    center_mean = round(center_stat.mean[0], 3)

    hx, hy, htile_mean = find_hotspot_grid(diff)

    conc = round(max_diff / (mean_diff + 1e-6), 2)

    bc_a, bc_b = fa["bc"], fb["bc"]
    cx_a, cy_a = fa["cx"], fa["cy"]
    cx_b, cy_b = fb["cx"], fb["cy"]

    if cx_a is not None and cx_b is not None:
        pos_delta = round(((cx_b - cx_a) ** 2 + (cy_b - cy_a) ** 2) ** 0.5, 1)
    else:
        pos_delta = None

    event = classify_event_v2(mean_diff, max_diff, conc, bc_a, bc_b, pos_delta)

    return {
        "mean_diff":         mean_diff,
        "std_diff":          std_diff,
        "max_diff":          max_diff,
        "center_mean":       center_mean,
        "hotspot_x":         hx,
        "hotspot_y":         hy,
        "hotspot_tile_mean": htile_mean,
        "concentration":     conc,
        "bright_count_prev": bc_a,
        "bright_count_curr": bc_b,
        "bright_cx_prev":    cx_a,
        "bright_cy_prev":    cy_a,
        "bright_cx_curr":    cx_b,
        "bright_cy_curr":    cy_b,
        "position_delta_px": pos_delta,
        "event_type":        event,
    }


# ============================================================
# v2 イベント分類器
# ============================================================

def classify_event_v2(
    mean_diff: float,
    max_diff:  int,
    conc:      float,
    bc_prev:   int,
    bc_curr:   int,
    pos_delta,         # float or None
) -> str:
    """
    v2 分類器。

    分類優先順位:
      STATIC > APPEAR > DISAPPEAR > ZOOM_BLOOM > CUT > OBJECT_MOVE
      > CAMERA_TRACK > REVIEW_REQUIRED > STATIC (fallback)

    CUT の3条件:
      A. brightness急変: mean_diff >= CUT_ABS_THRESHOLD
      B. object_track不可: prev_has=False OR curr_has=False
         （bc は OBJECT_TRACKING 補助として prev_has/curr_has の判定にのみ使用。
           CUT の可否を bc 値の絶対値で直接決めてはいない）
      C. scene_structure破綻: conc < CUT_CONC_THRESHOLD
         （変化が局所集中していない = 広域的・均一な変化）

    3条件がすべて真の場合のみ CUT。
    大型・高輝度オブジェクト（bc >> BRIGHT_COUNT_MIN）が移動しても
    B の条件（track_fail=False）が成立しないため CUT とならない。
    """
    prev_has = bc_prev >= BRIGHT_COUNT_MIN
    curr_has = bc_curr >= BRIGHT_COUNT_MIN

    # ── 1. STATIC ──
    if mean_diff < STATIC_THRESHOLD:
        return "STATIC"

    # ── 2. APPEAR ──
    # (標準) bc_prev がほぼゼロ → bc_curr が大幅に増加
    if not prev_has and curr_has and bc_curr >= BRIGHT_COUNT_MIN * APPEAR_RATIO:
        return "APPEAR"

    # (相対) bc_prev が非ゼロでも bc_curr が APPEAR_BC_RATIO 倍以上増 → 実質出現
    # 例: bc_prev=28, bc_curr=2573 (比率91.9) → APPEAR
    if prev_has and curr_has:
        bc_ratio_ap = bc_curr / (bc_prev + 1e-6)
        if bc_ratio_ap >= APPEAR_BC_RATIO and bc_curr >= BRIGHT_COUNT_MIN * APPEAR_RATIO:
            return "APPEAR"

    # ── 3. DISAPPEAR ──
    if prev_has and not curr_has:
        return "DISAPPEAR"
    if prev_has and curr_has and bc_curr < bc_prev * DISAPPEAR_RATIO:
        return "DISAPPEAR"

    # ── 4. ZOOM_BLOOM ──
    # 輝度が大幅に拡大（bloom/露出上昇）または縮小（zoom-out/露出低下）
    # centroid が安定している場合のみ（純粋な輝度変化として扱う）
    if prev_has and curr_has:
        bc_ratio_zb = bc_curr / (bc_prev + 1e-6)
        centroid_stable_zb = (pos_delta is None or pos_delta < ZOOM_BLOOM_STABLE)
        if centroid_stable_zb and mean_diff >= ZOOM_BLOOM_DIFF_MIN:
            if bc_ratio_zb >= ZOOM_BLOOM_EXPAND or bc_ratio_zb <= (1.0 / ZOOM_BLOOM_EXPAND):
                return "ZOOM_BLOOM"

    # ── 5. CUT ──
    # 3条件すべて成立する場合のみ CUT と判定
    #
    # 条件A: brightness急変（absolute mean_diff、bc正規化なし）
    brightness_shock = mean_diff >= CUT_ABS_THRESHOLD

    # 条件B: object_track不可
    # pos_delta=None ⟺ bc_prev<MIN OR bc_curr<MIN（centroid が計算できない）
    # この条件が False（=tracking成功）なら大型オブジェクト移動の可能性が高い
    track_fail = (not prev_has) or (not curr_has) or (pos_delta is None)

    # 条件C: scene_structure破綻（変化が広域的 = 局所集中していない）
    structure_collapse = conc < CUT_CONC_THRESHOLD

    if brightness_shock and track_fail and structure_collapse:
        return "CUT"

    # ── 6. OBJECT_MOVE ──
    # 輝点が両フレームに存在し、centroid が移動している
    if prev_has and curr_has:
        if pos_delta is not None and pos_delta >= OBJECT_MOVE_MIN_PX:
            return "OBJECT_MOVE"
        # pos_delta は小さいが輝度変化があり対象物の内部変化・微小移動と判断
        if mean_diff >= OBJECT_THRESHOLD:
            return "OBJECT_MOVE"

    # ── 7. CAMERA_TRACK ──
    # 対象物 centroid が安定しており（カメラ追従）、背景が移動している
    if prev_has and curr_has:
        centroid_stable = (pos_delta is None or pos_delta < CAMERA_STABLE_PX)
        if centroid_stable and mean_diff >= CAMERA_THRESHOLD:
            return "CAMERA_TRACK"

    # ── 8. REVIEW_REQUIRED ──
    if mean_diff >= OBJECT_THRESHOLD:
        return "REVIEW_REQUIRED"

    return "STATIC"


# ============================================================
# 出力
# ============================================================

CSV_FIELDS = [
    "pair_id",
    "frame_prev", "frame_curr",
    "timestamp_prev_s", "timestamp_curr_s",
    "mean_diff", "std_diff", "max_diff", "center_mean",
    "hotspot_x", "hotspot_y", "hotspot_tile_mean", "concentration",
    "bright_count_prev", "bright_count_curr",
    "bright_cx_prev", "bright_cy_prev",
    "bright_cx_curr", "bright_cy_curr",
    "position_delta_px",
    "event_type",
]

# v1 との互換性のため列順・列名は同一に保つ
ALL_EVENT_TYPES = [
    "CUT", "APPEAR", "DISAPPEAR",
    "ZOOM_BLOOM", "CAMERA_TRACK",
    "OBJECT_MOVE", "REVIEW_REQUIRED", "STATIC",
]


def write_csv(rows: list, out_path: Path):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(rows)


def write_jsonl(rows: list, out_path: Path):
    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def write_summary(
    rows:       list,
    article_id: str,
    source_id:  str,
    frames_dir: str,
    out_path:   Path,
    run_at:     str,
):
    from collections import Counter
    total_pairs  = len(rows)
    total_frames = total_pairs + 1
    event_counts = Counter(r["event_type"] for r in rows)

    cut_rows    = [r for r in rows if r["event_type"] == "CUT"]
    appear_rows = [r for r in rows if r["event_type"] == "APPEAR"]
    disapp_rows = [r for r in rows if r["event_type"] == "DISAPPEAR"]
    zoom_rows   = [r for r in rows if r["event_type"] == "ZOOM_BLOOM"]
    cam_rows    = [r for r in rows if r["event_type"] == "CAMERA_TRACK"]
    obj_rows    = [r for r in rows if r["event_type"] == "OBJECT_MOVE"]
    rev_rows    = [r for r in rows if r["event_type"] == "REVIEW_REQUIRED"]

    top_diff = sorted(rows, key=lambda r: r["mean_diff"], reverse=True)[:10]

    priority_types = {"CUT", "APPEAR", "DISAPPEAR", "ZOOM_BLOOM", "OBJECT_MOVE", "REVIEW_REQUIRED"}
    priority_rows  = [r for r in rows if r["event_type"] in priority_types]

    lines = [
        "# Frame Delta Analysis Summary (v2)",
        "",
        f"- 実行日時: {run_at}",
        f"- article_id: {article_id}",
        f"- source_id: {source_id}",
        f"- frames_dir: {frames_dir}",
        f"- 分類器バージョン: frame_delta_v2.py",
        "",
        "---",
        "",
        "## 基本統計",
        "",
        "| 項目 | 値 |",
        "|------|-----|",
        f"| 総フレーム数 | {total_frames} |",
        f"| 比較ペア数 | {total_pairs} |",
        "",
        "## イベント別件数",
        "",
        "| イベント | 件数 | 説明 |",
        "|---------|------|------|",
    ]
    event_desc = {
        "CUT":             "シーン構造崩壊（brightness急変+tracking失敗+広域変化の3条件）",
        "APPEAR":          "輝点出現（bc_prev≈0 → bc_curr 大または相対20倍増）",
        "DISAPPEAR":       "輝点消失（bc_curr → 0 またはbc_prev比で75%減）",
        "ZOOM_BLOOM":      "輝度急拡大/縮小（bc比5倍以上、centroid安定）",
        "CAMERA_TRACK":    "カメラ追従（centroid安定 + 背景移動）",
        "OBJECT_MOVE":     "対象物移動（centroid移動5px以上または輝度変化）",
        "REVIEW_REQUIRED": "自動判定困難（要人間確認）",
        "STATIC":          "変化なし（mean_diff < 2.0）",
    }
    for ev in ALL_EVENT_TYPES:
        lines.append(f"| {ev} | {event_counts.get(ev, 0)} | {event_desc.get(ev, '')} |")

    lines += [
        "",
        "---",
        "",
        "## 人間確認推奨フレーム",
        "",
        f"### CUT（scene_structure崩壊）{len(cut_rows)} 件",
        "*(v2: brightness急変 AND tracking失敗 AND 広域変化の3条件すべて必須)*",
    ]
    if cut_rows:
        lines.append("| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | mean_diff | conc |")
        lines.append("|---------|-----------|-----------|---------|---------|-----------|------|")
        for r in cut_rows:
            lines.append(
                f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
                f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
                f"| {r['mean_diff']} | {r['concentration']} |"
            )
    else:
        lines.append("（なし）")

    lines += ["", f"### APPEAR（輝点出現）{len(appear_rows)} 件"]
    if appear_rows:
        lines.append("| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | bc_prev | bc_curr |")
        lines.append("|---------|-----------|-----------|---------|---------|---------|---------|")
        for r in appear_rows:
            lines.append(
                f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
                f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
                f"| {r['bright_count_prev']} | {r['bright_count_curr']} |"
            )
    else:
        lines.append("（なし）")

    lines += ["", f"### DISAPPEAR（輝点消失）{len(disapp_rows)} 件"]
    if disapp_rows:
        lines.append("| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | bc_prev | bc_curr |")
        lines.append("|---------|-----------|-----------|---------|---------|---------|---------|")
        for r in disapp_rows:
            lines.append(
                f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
                f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
                f"| {r['bright_count_prev']} | {r['bright_count_curr']} |"
            )
    else:
        lines.append("（なし）")

    lines += ["", f"### ZOOM_BLOOM（輝度急変化）{len(zoom_rows)} 件"]
    if zoom_rows:
        lines.append("| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | bc_prev | bc_curr | pos_delta |")
        lines.append("|---------|-----------|-----------|---------|---------|---------|---------|-----------|")
        for r in zoom_rows:
            lines.append(
                f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
                f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
                f"| {r['bright_count_prev']} | {r['bright_count_curr']} | {r['position_delta_px']} |"
            )
    else:
        lines.append("（なし）")

    lines += ["", f"### OBJECT_MOVE（対象物移動）{len(obj_rows)} 件"]
    if obj_rows:
        lines.append("| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | pos_delta_px | mean_diff |")
        lines.append("|---------|-----------|-----------|---------|---------|-------------|-----------|")
        for r in obj_rows:
            lines.append(
                f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
                f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
                f"| {r['position_delta_px']} | {r['mean_diff']} |"
            )
    else:
        lines.append("（なし）")

    lines += ["", f"### CAMERA_TRACK（カメラ追従）{len(cam_rows)} 件"]
    if cam_rows:
        lines.append("| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | mean_diff | pos_delta |")
        lines.append("|---------|-----------|-----------|---------|---------|-----------|-----------|")
        for r in cam_rows:
            lines.append(
                f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
                f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
                f"| {r['mean_diff']} | {r['position_delta_px']} |"
            )
    else:
        lines.append("（なし）")

    lines += ["", f"### REVIEW_REQUIRED（要確認）{len(rev_rows)} 件"]
    if rev_rows:
        lines.append("| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | mean_diff | pos_delta |")
        lines.append("|---------|-----------|-----------|---------|---------|-----------|-----------|")
        for r in rev_rows:
            lines.append(
                f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
                f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
                f"| {r['mean_diff']} | {r['position_delta_px']} |"
            )
    else:
        lines.append("（なし）")

    lines += [
        "",
        "---",
        "",
        "## 高変化量区間（mean_diff 上位10件）",
        "",
        "| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | mean_diff | event_type |",
        "|---------|-----------|-----------|---------|---------|-----------|------------|",
    ]
    for r in top_diff:
        lines.append(
            f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
            f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
            f"| {r['mean_diff']} | {r['event_type']} |"
        )

    lines += [
        "",
        "---",
        "",
        "## VLM 解析推奨フレーム候補",
        "",
        f"以下のフレームを優先的に VLM へ渡すことを推奨します（{len(priority_rows)} 件）。",
        "",
        "| frame | timestamp_s | event_type |",
        "|-------|------------|------------|",
    ]
    seen = set()
    for r in priority_rows:
        for fname, ts in [
            (r["frame_prev"], r["timestamp_prev_s"]),
            (r["frame_curr"], r["timestamp_curr_s"]),
        ]:
            if fname not in seen:
                lines.append(f"| {fname} | {ts}s | {r['event_type']} |")
                seen.add(fname)

    lines += [
        "",
        "---",
        "",
        "## CUT 判定ロジック（v2）",
        "",
        "```",
        "CUT = (mean_diff >= 30.0)          # 条件A: brightness急変",
        "    AND (not prev_has OR not curr_has)  # 条件B: object tracking 失敗",
        "    AND (conc < 5.5)               # 条件C: scene_structure破綻（広域変化）",
        "",
        "大型オブジェクト（bc >> 20）が両フレームに存在 → track_fail=False → CUT不成立",
        "bc は CUT 判定基準に直接使用しない（OBJECT_TRACKING 補助のみ）",
        "```",
    ]

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ============================================================
# メイン
# ============================================================

def parse_frame_number(path: Path) -> int:
    """
    フレームファイル名から数値部分を返す。
    frame_0042.png   → 42  (index モード)
    frame_00141.png  → 141 (seconds モード)
    frame_001410d.png → 1410 (deciseconds モード)
    """
    stem = path.stem
    raw  = stem.split("_")[-1]
    if raw.endswith("d"):
        raw = raw[:-1]
    return int(raw)


def frame_to_timestamp(path: Path, ts_mode: str, interval: float) -> float:
    """ts_mode に応じてフレームのタイムスタンプ（秒）を返す。"""
    n = parse_frame_number(path)
    if ts_mode == "seconds":
        return float(n)
    elif ts_mode == "deciseconds":
        return n / 10.0
    else:  # index
        return (n - 1) * interval


def main():
    parser = argparse.ArgumentParser(
        description="Adaptive Frame 間の差分分析スクリプト（v2: CUT誤分類修正版）"
    )
    parser.add_argument("--frames-dir",  required=True,
                        help="Adaptive Frame が格納されたディレクトリ")
    parser.add_argument("--article-id",  required=True,
                        help="例: R02-052")
    parser.add_argument("--source-id",   required=True,
                        help="例: DOW-UAP-PR060_Spherical_UAP_...")
    parser.add_argument("--output-dir",  default="data/frame_delta_runs/20260627_v2/",
                        help="出力先ルートディレクトリ")
    parser.add_argument("--interval",    type=float, default=3.0,
                        help="フレーム間の秒数（デフォルト: 3.0）")
    parser.add_argument("--ts-mode",     default="index",
                        choices=["index", "seconds", "deciseconds"],
                        help="タイムスタンプ計算モード: "
                             "index=(N-1)×interval（デフォルト）/ "
                             "seconds=N秒（targeted整数秒フォーマット）/ "
                             "deciseconds=N/10秒")
    parser.add_argument("--execute",     action="store_true",
                        help="実行モード（なければ dry-run）")
    parser.add_argument("--verbose",     action="store_true",
                        help="詳細ログを表示")
    args = parser.parse_args()

    frames_dir = Path(args.frames_dir)
    if not frames_dir.exists():
        print(f"ERROR: frames-dir が存在しません: {frames_dir}", file=sys.stderr)
        sys.exit(1)

    ts_mode = args.ts_mode
    frame_paths = sorted(
        frames_dir.glob("*.png"),
        key=lambda p: frame_to_timestamp(p, ts_mode, args.interval)
    )
    n_frames = len(frame_paths)

    if n_frames < 2:
        print(f"ERROR: フレームが2枚以上必要です（現在: {n_frames}枚）", file=sys.stderr)
        sys.exit(1)

    n_pairs  = n_frames - 1
    out_dir  = Path(args.output_dir) / args.source_id
    csv_path     = out_dir / "frame_delta.csv"
    jsonl_path   = out_dir / "frame_delta.jsonl"
    summary_path = out_dir / "summary.md"

    ts_end   = round(frame_to_timestamp(frame_paths[-1],  ts_mode, args.interval), 1)
    ts_start = round(frame_to_timestamp(frame_paths[0],   ts_mode, args.interval), 1)

    print(f"[frame_delta_v2.py] mode={'EXECUTE' if args.execute else 'DRY-RUN'}")
    print(f"  article_id : {args.article_id}")
    print(f"  source_id  : {args.source_id}")
    print(f"  frames_dir : {frames_dir}")
    print(f"  ts_mode    : {ts_mode}")
    print(f"  フレーム数 : {n_frames}")
    print(f"  比較ペア数 : {n_pairs}")
    print(f"  間隔       : {args.interval}s")
    print(f"  時間範囲   : {ts_start}s 〜 {ts_end}s")
    print(f"  出力先     : {out_dir}/")
    print(f"    - {csv_path.name}")
    print(f"    - {jsonl_path.name}")
    print(f"    - {summary_path.name}")

    if not args.execute:
        print(f"\n[DRY-RUN 完了] --execute を付けると分析を実行します。")
        return

    # --- EXECUTE ---
    out_dir.mkdir(parents=True, exist_ok=True)
    run_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n[1/3] フレーム読み込み中... ({n_frames}枚)")
    frame_cache = {}
    for i, p in enumerate(frame_paths):
        frame_cache[p] = analyze_frame(p)
        if args.verbose:
            print(f"  {p.name}: bc={frame_cache[p]['bc']}")
        elif (i + 1) % 20 == 0:
            print(f"  {i + 1}/{n_frames} 完了")

    print(f"[2/3] ペア差分分析中... ({n_pairs}ペア)")
    rows = []
    for i in range(n_pairs):
        pa = frame_paths[i]
        pb = frame_paths[i + 1]
        fa = frame_cache[pa]
        fb = frame_cache[pb]

        ts_a = round(frame_to_timestamp(pa, ts_mode, args.interval), 3)
        ts_b = round(frame_to_timestamp(pb, ts_mode, args.interval), 3)

        metrics = analyze_pair(fa, fb)

        row = {
            "pair_id":          i + 1,
            "frame_prev":       pa.name,
            "frame_curr":       pb.name,
            "timestamp_prev_s": ts_a,
            "timestamp_curr_s": ts_b,
        }
        row.update(metrics)
        rows.append(row)

        if args.verbose:
            print(
                f"  pair {i+1:3d}: {pa.name} → {pb.name} "
                f"mean={metrics['mean_diff']:.1f} "
                f"conc={metrics['concentration']:.1f} "
                f"bc_prev={metrics['bright_count_prev']} "
                f"bc_curr={metrics['bright_count_curr']} "
                f"pos={metrics['position_delta_px']} "
                f"ev={metrics['event_type']}"
            )
        elif (i + 1) % 20 == 0:
            print(f"  {i + 1}/{n_pairs} 完了")

    print(f"[3/3] 出力中...")
    write_csv(rows,   csv_path)
    write_jsonl(rows, jsonl_path)
    write_summary(
        rows, args.article_id, args.source_id,
        str(frames_dir), summary_path, run_at
    )

    from collections import Counter
    ec = Counter(r["event_type"] for r in rows)
    priority = sum(ec.get(e, 0) for e in ["CUT", "APPEAR", "DISAPPEAR", "ZOOM_BLOOM", "OBJECT_MOVE", "REVIEW_REQUIRED"])

    print(f"\n[完了] {args.article_id} / {args.source_id}")
    print(f"  総フレーム: {n_frames}  比較ペア: {n_pairs}")
    for ev in ALL_EVENT_TYPES:
        count = ec.get(ev, 0)
        if count > 0 or ev in ("CUT", "OBJECT_MOVE"):
            print(f"  {ev:20s}: {count}")
    print(f"  人間確認推奨: {priority} 件")
    print(f"  出力: {out_dir}/")


if __name__ == "__main__":
    main()
