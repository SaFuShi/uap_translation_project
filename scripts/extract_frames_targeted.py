#!/usr/bin/env python3
"""
extract_frames_targeted.py

Frame Delta 分析結果（frame_delta.csv）を基に、
指定イベントの前後区間を細かい間隔で追加抽出する。

フロー:
  1. frame_delta.csv を読み込み、指定イベントを検出
  2. イベント前後 ±window 秒の時間範囲を算出
  3. 重複・隣接する範囲をマージ
  4. 範囲内で --interval ごとのタイムスタンプを生成
  5. 既存フレームと重複するタイムスタンプをスキップ
  6. ffmpeg で各タイムスタンプのフレームを抽出
  7. targeted_extraction_log.csv を出力

出力ディレクトリ: <existing-frames-dir>_targeted/
フレーム命名規則: frame_{timestamp_in_seconds:05d}.png
  例) 141s → frame_00141.png（5桁・整数秒）
  サブ秒対応: frame_{int(ts*10):06d}d.png（0.1s精度の場合）

使用方法:
  python3 scripts/extract_frames_targeted.py \\
    --video raw_media/video/DOW-UAP-PR054_....mp4 \\
    --delta-csv data/frame_delta_runs/20260626/<slug>/frame_delta.csv \\
    --existing-frames-dir data/adaptive_frames/20260626/<slug>/ \\
    --original-interval 3.0 \\
    --events DISAPPEAR,APPEAR,OBJECT_MOVE \\
    --pos-delta-min 100 \\
    --window 6 \\
    --interval 1.0 \\
    [--execute]
"""

import argparse
import csv
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ============================================================
# デフォルト値
# ============================================================
DEFAULT_WINDOW        = 6.0    # イベント前後の抽出範囲（秒）
DEFAULT_INTERVAL      = 1.0    # 再抽出間隔（秒）
DEFAULT_POS_DELTA_MIN = 100.0  # OBJECT_MOVE トリガーの最小移動量（px）
DEFAULT_EVENTS        = {"DISAPPEAR", "APPEAR", "OBJECT_MOVE"}

LOG_FIELDS = [
    "trigger_pair_id",
    "trigger_event_type",
    "trigger_ts_prev_s",
    "trigger_ts_curr_s",
    "trigger_pos_delta_px",
    "range_start_s",
    "range_end_s",
    "timestamps_targeted",
    "frames_extracted",
    "frames_skipped_existing",
    "frames_failed",
]

# ============================================================
# 既存フレームのタイムスタンプ取得
# ============================================================

def parse_existing_timestamps(frames_dir: Path, original_interval: float) -> set:
    """
    既存フレームディレクトリ内の PNG を読み取り、
    各フレームのタイムスタンプ（秒）を float のセットで返す。
    frame_NNNN.png → (N - 1) × original_interval
    """
    timestamps = set()
    for p in sorted(frames_dir.glob("*.png")):
        stem = p.stem  # e.g. "frame_0042"
        try:
            n = int(stem.split("_")[-1])
            ts = round((n - 1) * original_interval, 3)
            timestamps.add(ts)
        except (ValueError, IndexError):
            pass
    return timestamps


# ============================================================
# Delta CSV 読み込みとトリガー検出
# ============================================================

def read_delta_csv(csv_path: Path) -> list:
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def identify_triggers(
    rows:          list,
    target_events: set,
    pos_delta_min: float,
) -> list:
    """
    Delta CSV の各行を精査し、抽出トリガーになる行を返す。
    OBJECT_MOVE は pos_delta_px ≥ pos_delta_min の場合のみ対象。
    """
    triggers = []
    for row in rows:
        ev = row["event_type"]
        if ev not in target_events:
            continue

        ts_prev = float(row["timestamp_prev_s"])
        ts_curr = float(row["timestamp_curr_s"])

        if ev == "OBJECT_MOVE":
            pos = row.get("position_delta_px", "")
            try:
                pos_val = float(pos) if pos not in ("", "None", "null") else 0.0
            except ValueError:
                pos_val = 0.0
            if pos_val < pos_delta_min:
                continue
        else:
            pos_val = None

        triggers.append({
            "pair_id":       row["pair_id"],
            "event_type":    ev,
            "ts_prev":       ts_prev,
            "ts_curr":       ts_curr,
            "pos_delta_px":  pos_val,
        })

    return triggers


# ============================================================
# 時間範囲の構築とマージ
# ============================================================

def build_and_merge_ranges(
    triggers:       list,
    window:         float,
    video_duration: float,
    merge_gap:      float = 1.5,
) -> list:
    """
    各トリガーに ±window を加えた範囲を構築し、
    merge_gap 秒以内に隣接する範囲をマージする。
    返す各要素: {"start": float, "end": float, "triggers": list}
    """
    raw = []
    for t in triggers:
        start = max(0.0, t["ts_prev"] - window)
        end   = min(video_duration, t["ts_curr"] + window)
        raw.append({"start": start, "end": end, "triggers": [t]})

    raw.sort(key=lambda r: r["start"])

    merged = []
    for r in raw:
        if merged and r["start"] <= merged[-1]["end"] + merge_gap:
            merged[-1]["end"] = max(merged[-1]["end"], r["end"])
            merged[-1]["triggers"].extend(r["triggers"])
        else:
            merged.append({
                "start":    r["start"],
                "end":      r["end"],
                "triggers": list(r["triggers"]),
            })

    return merged


# ============================================================
# 抽出タイムスタンプ生成
# ============================================================

def generate_timestamps(
    ranges:       list,
    interval:     float,
    existing_ts:  set,
    skip_margin:  float = None,
) -> list:
    """
    各範囲について interval ごとのタイムスタンプを生成し、
    既存タイムスタンプと近接（±skip_margin）するものをスキップする。

    skip_margin のデフォルト = interval × 0.4
    返す: [{"ts": float, "range_idx": int, "skipped": bool}]
    """
    if skip_margin is None:
        skip_margin = interval * 0.4

    results = []
    for idx, rng in enumerate(ranges):
        ts = rng["start"]
        while ts <= rng["end"] + 1e-6:
            ts_r = round(ts, 3)
            # 既存フレームと近接していればスキップ
            skip = any(abs(ts_r - ex) <= skip_margin for ex in existing_ts)
            results.append({"ts": ts_r, "range_idx": idx, "skipped": skip})
            ts = round(ts + interval, 3)

    return results


# ============================================================
# フレーム命名
# ============================================================

def ts_to_filename(ts: float, interval: float) -> str:
    """
    タイムスタンプ → フレームファイル名。
    整数秒（interval ≥ 1.0）: frame_00141.png
    サブ秒（interval < 1.0）: frame_001410d.png（1/10秒単位）
    """
    if interval >= 1.0:
        return f"frame_{int(round(ts)):05d}.png"
    else:
        return f"frame_{int(round(ts * 10)):06d}d.png"


# ============================================================
# ffmpeg による単一フレーム抽出
# ============================================================

def extract_frame(video_path: Path, ts: float, output_path: Path) -> bool:
    """
    ffmpeg で指定タイムスタンプの1フレームを抽出する。
    成功時 True、失敗時 False。
    """
    cmd = [
        "ffmpeg",
        "-ss", f"{ts:.3f}",
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        "-y",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0 and output_path.exists()


# ============================================================
# ログ出力
# ============================================================

def write_log(log_entries: list, out_path: Path):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        writer.writeheader()
        writer.writerows(log_entries)


# ============================================================
# メイン
# ============================================================

def get_video_duration(video_path: Path) -> float:
    """ffprobe で映像の再生時間を取得する。"""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 9999.0


def main():
    parser = argparse.ArgumentParser(
        description="Delta 分析結果を基にイベント前後区間を細かい間隔で追加抽出する"
    )
    parser.add_argument("--video",                required=True,
                        help="元動画ファイルパス")
    parser.add_argument("--delta-csv",            required=True,
                        help="frame_delta.csv のパス")
    parser.add_argument("--existing-frames-dir",  required=True,
                        help="既存 Adaptive Frame ディレクトリ（重複スキップ用）")
    parser.add_argument("--original-interval",    type=float, default=3.0,
                        help="既存フレームの抽出間隔（秒・デフォルト 3.0）")
    parser.add_argument("--events",               default="DISAPPEAR,APPEAR,OBJECT_MOVE",
                        help="トリガーとするイベント種別（カンマ区切り）")
    parser.add_argument("--pos-delta-min",        type=float, default=DEFAULT_POS_DELTA_MIN,
                        help="OBJECT_MOVE のトリガー最小移動量（px・デフォルト 100）")
    parser.add_argument("--window",               type=float, default=DEFAULT_WINDOW,
                        help="イベント前後の抽出範囲（秒・デフォルト 6）")
    parser.add_argument("--interval",             type=float, default=DEFAULT_INTERVAL,
                        help="再抽出間隔（秒・デフォルト 1.0）")
    parser.add_argument("--execute",              action="store_true",
                        help="実行モード（なければ dry-run）")
    parser.add_argument("--verbose",              action="store_true",
                        help="詳細ログを表示")
    args = parser.parse_args()

    video_path       = Path(args.video)
    delta_csv_path   = Path(args.delta_csv)
    existing_dir     = Path(args.existing_frames_dir)
    target_events    = set(e.strip() for e in args.events.split(","))
    output_dir       = Path(str(existing_dir).rstrip("/") + "_targeted")
    log_path         = output_dir / "targeted_extraction_log.csv"

    mode = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"[extract_frames_targeted.py] mode={mode}")
    print(f"  video            : {video_path}")
    print(f"  delta_csv        : {delta_csv_path}")
    print(f"  existing_dir     : {existing_dir}")
    print(f"  original_interval: {args.original_interval}s")
    print(f"  target_events    : {sorted(target_events)}")
    print(f"  pos_delta_min    : {args.pos_delta_min}px (OBJECT_MOVE 用)")
    print(f"  window           : ±{args.window}s")
    print(f"  interval         : {args.interval}s")
    print(f"  output_dir       : {output_dir}/")

    # 検証
    for p, label in [(video_path, "video"), (delta_csv_path, "delta-csv"), (existing_dir, "existing-frames-dir")]:
        if not p.exists():
            print(f"ERROR: {label} が存在しません: {p}", file=sys.stderr)
            sys.exit(1)

    # 映像時間取得
    video_duration = get_video_duration(video_path)
    print(f"  video_duration   : {video_duration:.1f}s")

    # 既存タイムスタンプ
    existing_ts = parse_existing_timestamps(existing_dir, args.original_interval)
    print(f"  既存フレーム     : {len(existing_ts)}枚")

    # Delta CSV 読み込みとトリガー検出
    rows = read_delta_csv(delta_csv_path)
    triggers = identify_triggers(rows, target_events, args.pos_delta_min)
    print(f"\n  検出トリガー     : {len(triggers)}件")
    for t in triggers:
        print(f"    pair{t['pair_id']:>4s}: {t['event_type']:15s} "
              f"{t['ts_prev']}s→{t['ts_curr']}s "
              f"(pos_delta={t['pos_delta_px']})")

    if not triggers:
        print("\n[DRY-RUN 完了] トリガーが0件のため抽出なし。")
        return

    # 時間範囲構築とマージ
    ranges = build_and_merge_ranges(triggers, args.window, video_duration)
    print(f"\n  マージ後の時間範囲: {len(ranges)}区間")
    for i, r in enumerate(ranges):
        trig_ids = [t["pair_id"] for t in r["triggers"]]
        print(f"    区間{i+1}: {r['start']:.1f}s 〜 {r['end']:.1f}s "
              f"(pair: {', '.join(trig_ids)})")

    # 抽出タイムスタンプ生成
    ts_entries = generate_timestamps(ranges, args.interval, existing_ts)
    new_ts     = [e for e in ts_entries if not e["skipped"]]
    skip_ts    = [e for e in ts_entries if e["skipped"]]

    print(f"\n  抽出対象タイムスタンプ: {len(new_ts)}個")
    print(f"  スキップ（既存重複）  : {len(skip_ts)}個")
    if args.verbose:
        for e in new_ts:
            print(f"    → {e['ts']}s: {ts_to_filename(e['ts'], args.interval)}")
        for e in skip_ts:
            print(f"    skip {e['ts']}s (既存あり)")

    # タイムスタンプ範囲サマリー
    if new_ts:
        ts_list = [e["ts"] for e in new_ts]
        print(f"  抽出タイムスタンプ範囲: {min(ts_list):.1f}s 〜 {max(ts_list):.1f}s")

    print(f"\n  出力先: {output_dir}/")
    print(f"  ログ  : {log_path}")

    if not args.execute:
        print(f"\n[DRY-RUN 完了] --execute を付けると {len(new_ts)} フレームを抽出します。")
        return

    # === EXECUTE ===
    output_dir.mkdir(parents=True, exist_ok=True)

    extracted  = 0
    failed     = 0
    log_rows   = []

    print(f"\n[EXECUTE] {len(new_ts)} フレームを抽出中...")
    for entry in new_ts:
        ts        = entry["ts"]
        filename  = ts_to_filename(ts, args.interval)
        out_path  = output_dir / filename
        ok        = extract_frame(video_path, ts, out_path)

        if ok:
            extracted += 1
            if args.verbose:
                print(f"  ✓ {filename} ({ts}s)")
        else:
            failed += 1
            print(f"  ✗ {filename} ({ts}s) — ffmpeg 失敗", file=sys.stderr)

    # ログ生成（範囲ごと）
    for rng in ranges:
        range_ts = [
            e["ts"] for e in ts_entries
            if e["range_idx"] == ranges.index(rng)
        ]
        extracted_in_range = [
            ts_to_filename(e["ts"], args.interval)
            for e in ts_entries
            if e["range_idx"] == ranges.index(rng) and not e["skipped"]
        ]
        skipped_in_range = sum(
            1 for e in ts_entries
            if e["range_idx"] == ranges.index(rng) and e["skipped"]
        )

        for trig in rng["triggers"]:
            log_rows.append({
                "trigger_pair_id":         trig["pair_id"],
                "trigger_event_type":      trig["event_type"],
                "trigger_ts_prev_s":       trig["ts_prev"],
                "trigger_ts_curr_s":       trig["ts_curr"],
                "trigger_pos_delta_px":    trig["pos_delta_px"],
                "range_start_s":           rng["start"],
                "range_end_s":             rng["end"],
                "timestamps_targeted":     len(range_ts),
                "frames_extracted":        len(extracted_in_range),
                "frames_skipped_existing": skipped_in_range,
                "frames_failed":           failed,
            })

    write_log(log_rows, log_path)

    print(f"\n[完了]")
    print(f"  抽出成功: {extracted} フレーム")
    print(f"  スキップ: {len(skip_ts)} フレーム（既存）")
    print(f"  失敗    : {failed} フレーム")
    print(f"  出力先  : {output_dir}/")
    print(f"  ログ    : {log_path}")


if __name__ == "__main__":
    main()
