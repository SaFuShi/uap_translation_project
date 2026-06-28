#!/usr/bin/env python3
"""
frame_delta_analyzer.py

Adaptive Frame ディレクトリ内の連続フレームを比較し、
フレーム間の差分・変化イベント・輝点移動を分析する。

使用方法:
  python3 scripts/frame_delta_analyzer.py \\
    --frames-dir data/adaptive_frames/20260626/<slug>/ \\
    --article-id R02-044 \\
    --source-id DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022 \\
    --output-dir data/frame_delta_runs/20260626/ \\
    [--interval 3.0] \\
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
# 閾値定数（映像の性質に応じて調整可能）
# ============================================================
CUT_THRESHOLD     = 35.0   # mean_diff ≥ → CUT（全体が急変）
CAMERA_THRESHOLD  = 12.0   # mean_diff ≥ & 集中度低 → CAMERA_MOTION
OBJECT_THRESHOLD  =  5.0   # mean_diff ≥ & 集中度高 → OBJECT_MOVE
STATIC_THRESHOLD  =  2.0   # mean_diff < → STATIC
CONC_RATIO        =  4.0   # max_diff / mean_diff ≥ → 局所集中と判定
BRIGHT_PX_TH      = 220    # 輝点とみなす輝度閾値（0-255）
BRIGHT_COUNT_MIN  =  20    # 輝点ピクセル数の最小（超えたら「輝点あり」と判定）
APPEAR_RATIO      =  4.0   # 輝点数が前フレームの X 倍以上増えたら APPEAR
DISAPPEAR_RATIO   =  0.25  # 輝点数が前フレームの X 倍以下になったら DISAPPEAR
POS_DELTA_REVIEW  = 80.0   # 輝点重心の移動量(px) ≥ → REVIEW_REQUIRED
GRID_N            =  4     # ホットスポット検出グリッド分割数（N×N）

# ============================================================
# フレーム単体の特徴量
# ============================================================

def count_bright_pixels(img_gray: Image.Image) -> int:
    """閾値以上の輝度ピクセル数（高速：point + histogram）"""
    mask = img_gray.point(lambda v: 255 if v >= BRIGHT_PX_TH else 0, "1")
    return mask.histogram()[255]


def bright_centroid(img_gray: Image.Image, bc: int) -> tuple:
    """
    輝度閾値以上のピクセルの重心座標を返す。
    輝点が十分でない場合は (None, None)。
    重心計算が必要な場合のみ呼ぶこと（低速）。
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
    """
    差分画像を n×n グリッドに分割し、
    最大平均差分タイルの中心座標と tile mean を返す。
    """
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
    """
    2フレームの特徴量 dict を受け取り、差分メトリクスを返す。
    fa / fb は analyze_frame() の返り値。
    """
    img_a, img_b = fa["img"], fb["img"]

    diff = ImageChops.difference(img_a, img_b)
    stat = ImageStat.Stat(diff)

    mean_diff = round(stat.mean[0],   3)
    std_diff  = round(stat.stddev[0], 3)
    max_diff  = int(diff.getextrema()[1])

    # 中央 50% 領域の差分
    w, h = diff.size
    cx1, cy1, cx2, cy2 = w // 4, h // 4, 3 * w // 4, 3 * h // 4
    center_stat  = ImageStat.Stat(diff.crop((cx1, cy1, cx2, cy2)))
    center_mean  = round(center_stat.mean[0], 3)

    # ホットスポット（グリッドベース）
    hx, hy, htile_mean = find_hotspot_grid(diff)

    # 集中度
    conc = round(max_diff / (mean_diff + 1e-6), 2)

    # 輝点
    bc_a, bc_b  = fa["bc"], fb["bc"]
    cx_a, cy_a  = fa["cx"], fa["cy"]
    cx_b, cy_b  = fb["cx"], fb["cy"]

    # 輝点重心の移動量
    if cx_a is not None and cx_b is not None:
        pos_delta = round(((cx_b - cx_a) ** 2 + (cy_b - cy_a) ** 2) ** 0.5, 1)
    else:
        pos_delta = None

    event = classify_event(mean_diff, max_diff, conc, bc_a, bc_b, pos_delta)

    return {
        "mean_diff":          mean_diff,
        "std_diff":           std_diff,
        "max_diff":           max_diff,
        "center_mean":        center_mean,
        "hotspot_x":          hx,
        "hotspot_y":          hy,
        "hotspot_tile_mean":  htile_mean,
        "concentration":      conc,
        "bright_count_prev":  bc_a,
        "bright_count_curr":  bc_b,
        "bright_cx_prev":     cx_a,
        "bright_cy_prev":     cy_a,
        "bright_cx_curr":     cx_b,
        "bright_cy_curr":     cy_b,
        "position_delta_px":  pos_delta,
        "event_type":         event,
    }


def classify_event(
    mean_diff: float,
    max_diff:  int,
    conc:      float,
    bc_prev:   int,
    bc_curr:   int,
    pos_delta,
) -> str:
    """
    優先順位付きの階層分類。
    CUT > APPEAR > DISAPPEAR > STATIC > CAMERA_MOTION > OBJECT_MOVE
    > REVIEW_REQUIRED > STATIC (fallback)
    """
    # 1. カット（全体急変）
    if mean_diff >= CUT_THRESHOLD:
        return "CUT"

    # 2. 輝点出現（前フレームにほぼなく、現フレームに急増）
    prev_has = bc_prev >= BRIGHT_COUNT_MIN
    curr_has = bc_curr >= BRIGHT_COUNT_MIN
    if not prev_has and curr_has and bc_curr >= BRIGHT_COUNT_MIN * APPEAR_RATIO:
        return "APPEAR"

    # 3. 輝点消失（前フレームにあり、現フレームに激減）
    if prev_has and not curr_has:
        return "DISAPPEAR"
    if prev_has and curr_has and bc_curr < bc_prev * DISAPPEAR_RATIO:
        return "DISAPPEAR"

    # 4. 静止
    if mean_diff < STATIC_THRESHOLD:
        return "STATIC"

    # 5. カメラ動き（広範囲に分散した変化）
    if mean_diff >= CAMERA_THRESHOLD and conc < CONC_RATIO:
        return "CAMERA_MOTION"

    # 6. 局所的な対象物移動（集中度高）
    if conc >= CONC_RATIO and mean_diff >= OBJECT_THRESHOLD:
        return "OBJECT_MOVE"

    # 7. 輝点が大きく移動（位置変化大）
    if pos_delta is not None and pos_delta >= POS_DELTA_REVIEW:
        return "REVIEW_REQUIRED"

    # 8. 微小〜中程度の変化で分類困難
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
    total_pairs  = len(rows)
    total_frames = total_pairs + 1

    # イベント集計
    from collections import Counter
    event_counts = Counter(r["event_type"] for r in rows)

    # REVIEW_REQUIRED / 注目フレーム
    review_rows = [r for r in rows if r["event_type"] == "REVIEW_REQUIRED"]
    cut_rows    = [r for r in rows if r["event_type"] == "CUT"]
    appear_rows = [r for r in rows if r["event_type"] == "APPEAR"]
    disapp_rows = [r for r in rows if r["event_type"] == "DISAPPEAR"]
    obj_rows    = [r for r in rows if r["event_type"] == "OBJECT_MOVE"]

    # 高変化量区間（mean_diff 上位10件）
    top_diff = sorted(rows, key=lambda r: r["mean_diff"], reverse=True)[:10]

    # 人間確認推奨フレーム（CUT / APPEAR / DISAPPEAR / REVIEW_REQUIRED / OBJECT_MOVE）
    priority_events = {"CUT", "APPEAR", "DISAPPEAR", "REVIEW_REQUIRED", "OBJECT_MOVE"}
    priority_rows = [r for r in rows if r["event_type"] in priority_events]

    lines = [
        f"# Frame Delta Analysis Summary",
        f"",
        f"- 実行日時: {run_at}",
        f"- article_id: {article_id}",
        f"- source_id: {source_id}",
        f"- frames_dir: {frames_dir}",
        f"",
        f"---",
        f"",
        f"## 基本統計",
        f"",
        f"| 項目 | 値 |",
        f"|------|-----|",
        f"| 総フレーム数 | {total_frames} |",
        f"| 比較ペア数 | {total_pairs} |",
        f"| 分析済みイベント | {total_pairs} |",
        f"",
        f"## イベント別件数",
        f"",
        f"| イベント | 件数 |",
        f"|---------|------|",
    ]
    for ev in ["CUT", "APPEAR", "DISAPPEAR", "CAMERA_MOTION", "OBJECT_MOVE",
               "REVIEW_REQUIRED", "STATIC"]:
        lines.append(f"| {ev} | {event_counts.get(ev, 0)} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## 人間確認推奨フレーム",
        f"",
        f"### CUT（場面転換）{len(cut_rows)} 件",
    ]
    if cut_rows:
        lines.append("| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | mean_diff |")
        lines.append("|---------|-----------|-----------|---------|---------|-----------|")
        for r in cut_rows:
            lines.append(
                f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
                f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
                f"| {r['mean_diff']} |"
            )
    else:
        lines.append("（なし）")

    lines += [f"", f"### APPEAR（輝点出現）{len(appear_rows)} 件"]
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

    lines += [f"", f"### DISAPPEAR（輝点消失）{len(disapp_rows)} 件"]
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

    lines += [f"", f"### OBJECT_MOVE（局所移動）{len(obj_rows)} 件"]
    if obj_rows:
        lines.append("| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | pos_delta_px | hotspot_x | hotspot_y |")
        lines.append("|---------|-----------|-----------|---------|---------|-------------|-----------|-----------|")
        for r in obj_rows:
            lines.append(
                f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
                f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
                f"| {r['position_delta_px']} | {r['hotspot_x']} | {r['hotspot_y']} |"
            )
    else:
        lines.append("（なし）")

    lines += [f"", f"### REVIEW_REQUIRED（要確認）{len(review_rows)} 件"]
    if review_rows:
        lines.append("| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | mean_diff | pos_delta_px |")
        lines.append("|---------|-----------|-----------|---------|---------|-----------|-------------|")
        for r in review_rows:
            lines.append(
                f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
                f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
                f"| {r['mean_diff']} | {r['position_delta_px']} |"
            )
    else:
        lines.append("（なし）")

    lines += [
        f"",
        f"---",
        f"",
        f"## 高変化量区間（mean_diff 上位10件）",
        f"",
        f"| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | mean_diff | event_type |",
        f"|---------|-----------|-----------|---------|---------|-----------|------------|",
    ]
    for r in top_diff:
        lines.append(
            f"| {r['pair_id']} | {r['frame_prev']} | {r['frame_curr']} "
            f"| {r['timestamp_prev_s']}s | {r['timestamp_curr_s']}s "
            f"| {r['mean_diff']} | {r['event_type']} |"
        )

    lines += [
        f"",
        f"---",
        f"",
        f"## VLM 解析推奨フレーム候補",
        f"",
        f"以下のフレームを優先的に VLM へ渡すことを推奨します（{len(priority_rows)} 件）。",
        f"",
        f"| frame | timestamp_s | event_type |",
        f"|-------|------------|------------|",
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

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ============================================================
# メイン
# ============================================================

def parse_frame_number(path: Path) -> int:
    """
    フレームファイル名から数値部分を返す。
    frame_0042.png     → 42     (index モード用)
    frame_00141.png    → 141    (seconds モード用)
    frame_001410d.png  → 1410   (deciseconds モード用: 末尾 d を除去)
    """
    stem = path.stem  # e.g. "frame_0042" / "frame_00141" / "frame_001410d"
    raw  = stem.split("_")[-1]
    if raw.endswith("d"):
        raw = raw[:-1]  # deciseconds suffix を除去
    return int(raw)


def frame_to_timestamp(path: Path, ts_mode: str, interval: float) -> float:
    """
    ts_mode に応じてフレームのタイムスタンプ（秒）を返す。
    - index:       (N - 1) × interval
    - seconds:     N
    - deciseconds: N / 10.0
    """
    n = parse_frame_number(path)
    if ts_mode == "seconds":
        return float(n)
    elif ts_mode == "deciseconds":
        return n / 10.0
    else:  # index (default)
        return (n - 1) * interval


def main():
    parser = argparse.ArgumentParser(
        description="Adaptive Frame 間の差分分析スクリプト"
    )
    parser.add_argument("--frames-dir",  required=True,
                        help="Adaptive Frame が格納されたディレクトリ")
    parser.add_argument("--article-id",  required=True,
                        help="例: R02-044")
    parser.add_argument("--source-id",   required=True,
                        help="例: DOW-UAP-PR054_Spherical_UAP_...")
    parser.add_argument("--output-dir",  default="data/frame_delta_runs/20260626/",
                        help="出力先ルートディレクトリ")
    parser.add_argument("--interval",    type=float, default=3.0,
                        help="フレーム間の秒数（デフォルト: 3.0）")
    parser.add_argument("--ts-mode",    default="index",
                        choices=["index", "seconds", "deciseconds"],
                        help="タイムスタンプ計算モード: "
                             "index=(N-1)×interval（デフォルト）/ "
                             "seconds=N秒（targeted整数秒フォーマット）/ "
                             "deciseconds=N/10秒（targeted 0.1s フォーマット）")
    parser.add_argument("--execute",     action="store_true",
                        help="実行モード（なければ dry-run）")
    parser.add_argument("--verbose",     action="store_true",
                        help="詳細ログを表示")
    args = parser.parse_args()

    frames_dir = Path(args.frames_dir)
    if not frames_dir.exists():
        print(f"ERROR: frames-dir が存在しません: {frames_dir}", file=sys.stderr)
        sys.exit(1)

    # フレームリスト（時刻順）
    ts_mode = args.ts_mode
    frame_paths = sorted(
        frames_dir.glob("*.png"),
        key=lambda p: frame_to_timestamp(p, ts_mode, args.interval)
    )
    n_frames = len(frame_paths)

    if n_frames < 2:
        print(f"ERROR: フレームが2枚以上必要です（現在: {n_frames}枚）", file=sys.stderr)
        sys.exit(1)

    n_pairs = n_frames - 1

    # 出力先
    out_dir = Path(args.output_dir) / args.source_id
    csv_path     = out_dir / "frame_delta.csv"
    jsonl_path   = out_dir / "frame_delta.jsonl"
    summary_path = out_dir / "summary.md"

    # --- DRY-RUN ---
    ts_end = round(frame_to_timestamp(frame_paths[-1], ts_mode, args.interval), 1)
    ts_start = round(frame_to_timestamp(frame_paths[0], ts_mode, args.interval), 1)
    print(f"[frame_delta_analyzer.py] mode={'EXECUTE' if args.execute else 'DRY-RUN'}")
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

    # フレームキャッシュ（各フレームを1回だけ読み込む）
    print(f"\n[1/3] フレーム読み込み中... ({n_frames}枚)")
    frame_cache = {}
    for i, p in enumerate(frame_paths):
        frame_cache[p] = analyze_frame(p)
        if args.verbose:
            print(f"  {p.name}: bc={frame_cache[p]['bc']}")
        elif (i + 1) % 20 == 0:
            print(f"  {i + 1}/{n_frames} 完了")

    # ペア分析
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
            "pair_id":           i + 1,
            "frame_prev":        pa.name,
            "frame_curr":        pb.name,
            "timestamp_prev_s":  ts_a,
            "timestamp_curr_s":  ts_b,
        }
        row.update(metrics)
        rows.append(row)

        if args.verbose:
            print(
                f"  pair {i+1:3d}: {pa.name} → {pb.name} "
                f"mean={metrics['mean_diff']:.1f} "
                f"conc={metrics['concentration']:.1f} "
                f"ev={metrics['event_type']}"
            )
        elif (i + 1) % 20 == 0:
            print(f"  {i + 1}/{n_pairs} 完了")

    # 出力
    print(f"[3/3] 出力中...")
    write_csv(rows,   csv_path)
    write_jsonl(rows, jsonl_path)
    write_summary(
        rows, args.article_id, args.source_id,
        str(frames_dir), summary_path, run_at
    )

    # 集計
    from collections import Counter
    ec = Counter(r["event_type"] for r in rows)
    priority = sum(ec.get(e, 0) for e in ["CUT","APPEAR","DISAPPEAR","OBJECT_MOVE","REVIEW_REQUIRED"])

    print(f"\n[完了] {args.article_id} / {args.source_id}")
    print(f"  総フレーム: {n_frames}  比較ペア: {n_pairs}")
    for ev in ["CUT","APPEAR","DISAPPEAR","CAMERA_MOTION","OBJECT_MOVE","REVIEW_REQUIRED","STATIC"]:
        print(f"  {ev:20s}: {ec.get(ev, 0)}")
    print(f"  人間確認推奨: {priority} 件")
    print(f"  出力: {out_dir}/")


if __name__ == "__main__":
    main()
