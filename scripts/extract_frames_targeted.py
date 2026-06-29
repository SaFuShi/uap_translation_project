#!/usr/bin/env python3
"""
extract_frames_targeted.py — Precision Sampler (Media Inspector v4)

設計書: docs/media_inspector_v4_architecture.md  §3.5 サンプリング戦略

【役割】
  粗解析（3秒間隔）の結果から必要区間だけを 0.25〜0.1 秒の高密度サンプリングで
  追加抽出する。Media Inspector v4 の全 Agent が利用する共通ツール。

【トリガーソース（複数同時指定可）】
  --manual-windows    "22:30,49:57,253:263"  手動区間（直接指定）
  --camera-events-csv  camera_events.csv      Camera Analyzer 出力
  --motion-events-csv  motion_events.csv      Motion Intelligence 出力
  --track-events-csv   track_events.csv       Object Tracker 出力
  --delta-csv          frame_delta.csv        旧形式（後方互換）

【利用例】
  # 手動区間指定（PR062 精密抽出）
  python3 scripts/extract_frames_targeted.py \\
    --video raw_media/video/DOW-UAP-PR062_....mp4 \\
    --manual-windows "22:30,49:57,121:129,246:255,253:263" \\
    --existing-frames-dir data/adaptive_frames/20260628/DOW-UAP-PR062_.../ \\
    --interval 0.25 \\
    --execute

  # Camera Analyzer トリガー
  python3 scripts/extract_frames_targeted.py \\
    --video <video> \\
    --camera-events-csv .../camera_analysis/camera_events.csv \\
    --camera-trigger-events FOV_IN,FOV_OUT,EDGE_SURGE \\
    --existing-frames-dir <adaptive_frames_dir> \\
    --interval 0.25 --window 5 --execute

  # 後方互換（旧 frame_delta.csv モード）
  python3 scripts/extract_frames_targeted.py \\
    --video <video> \\
    --delta-csv .../frame_delta.csv \\
    --events DISAPPEAR,APPEAR,OBJECT_MOVE \\
    --interval 1.0 --execute
"""

import argparse
import csv
import json
import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

VERSION = "precision_sampler_v1"

DEFAULT_INTERVAL      = 0.25
DEFAULT_WINDOW        = 5.0
DEFAULT_MERGE_GAP     = 2.0   # 2秒以内に隣接するレンジをマージ
DEFAULT_POS_DELTA_MIN = 100.0 # frame_delta 旧モード用


# ── ファイル名 ───────────────────────────────────────────────────

def ts_to_filename(ts: float, interval: float) -> str:
    """
    タイムスタンプ → フレームファイル名。
    ・ interval ≥ 1.0 秒: frame_00025.png    （秒の整数値、5桁）
    ・ interval <  1.0 秒: frame_000250d.png  （秒×10 の整数値、6桁+"d"）
    """
    if interval >= 1.0:
        return f"frame_{int(round(ts)):05d}.png"
    else:
        return f"frame_{int(round(ts * 10)):06d}d.png"


def parse_existing_timestamps(frames_dir: Path) -> set:
    """
    既存フレームディレクトリから全タイムスタンプを取得。
    命名規則:
      frame_00025.png    → ts = 25.0 秒
      frame_000250d.png  → ts = 25.0 秒 (250/10)
    """
    timestamps = set()
    for p in sorted(frames_dir.glob("*.png")):
        stem = p.stem  # e.g. "frame_00025" or "frame_000250d"
        parts = stem.rsplit("_", 1)
        if len(parts) < 2:
            continue
        code = parts[-1]
        try:
            if code.endswith("d"):
                ts = round(int(code[:-1]) / 10.0, 3)
            else:
                ts = float(int(code))
            timestamps.add(ts)
        except ValueError:
            pass
    return timestamps


# ── ffmpeg / ffprobe ─────────────────────────────────────────────

def get_video_duration(video_path: Path) -> float:
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


def extract_frame(video_path: Path, ts: float, output_path: Path) -> bool:
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


# ── トリガーソース読み込み ─────────────────────────────────────

def _clamp(ts: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, ts))


def load_manual_windows(
    windows_str: str,
    video_duration: float,
) -> list:
    """
    "22:30,49:57,121:129" → [{"start":22,"end":30,"source":"manual","label":"win_0"}, ...]
    フォーマット: "START:END" 秒指定（整数または小数）
    """
    ranges = []
    for i, token in enumerate(windows_str.split(",")):
        token = token.strip()
        if not token:
            continue
        parts = token.split(":")
        if len(parts) != 2:
            print(f"  [WARN] --manual-windows のフォーマット誤り: '{token}' はスキップ", file=sys.stderr)
            continue
        try:
            start = float(parts[0])
            end   = float(parts[1])
        except ValueError:
            print(f"  [WARN] --manual-windows の数値変換失敗: '{token}' はスキップ", file=sys.stderr)
            continue
        if start >= end:
            print(f"  [WARN] start >= end: '{token}' はスキップ", file=sys.stderr)
            continue
        ranges.append({
            "start":  _clamp(start, 0.0, video_duration),
            "end":    _clamp(end,   0.0, video_duration),
            "source": "manual",
            "label":  f"win_{i}",
            "triggers": [{"type": "manual", "token": token}],
        })
    return ranges


def _csv_load_event_ranges(
    csv_path: Path,
    ts_col: str,
    event_col: str,
    target_events: set,
    window: float,
    video_duration: float,
    source_name: str,
) -> list:
    """汎用 CSV → トリガーレンジ変換。ts_col が中心タイムスタンプ。"""
    if not csv_path.exists():
        print(f"  [ERROR] CSV が見つかりません: {csv_path}", file=sys.stderr)
        return []

    ranges = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ev = row.get(event_col, "").strip()
            if ev not in target_events:
                continue
            ts_raw = row.get(ts_col, "")
            try:
                ts = float(ts_raw)
            except ValueError:
                continue
            start = _clamp(ts - window, 0.0, video_duration)
            end   = _clamp(ts + window, 0.0, video_duration)
            pair_id = row.get("pair_id", "?")
            ranges.append({
                "start":  start,
                "end":    end,
                "source": source_name,
                "label":  f"{source_name}_{ev}_{int(ts)}s",
                "triggers": [{"type": source_name, "event": ev, "ts": ts, "pair_id": pair_id}],
            })
    return ranges


def load_camera_events(
    csv_path: Path,
    target_events: set,
    window: float,
    video_duration: float,
) -> list:
    """
    Camera Analyzer 出力 (camera_events.csv) をトリガーソースとして読み込む。
    timestamp_s 列を中心に ±window 秒の区間を生成。
    """
    return _csv_load_event_ranges(
        csv_path, "timestamp_s", "camera_event",
        target_events, window, video_duration, "camera"
    )


def load_motion_events(
    csv_path: Path,
    target_events: set,
    window: float,
    video_duration: float,
) -> list:
    """
    Motion Intelligence 出力 (motion_events.csv) をトリガーソースとして読み込む。
    timestamp_s 列を中心に ±window 秒の区間を生成。
    （Motion Intelligence v4 の出力フォーマットに対応予定）
    """
    return _csv_load_event_ranges(
        csv_path, "timestamp_s", "event_type",
        target_events, window, video_duration, "motion"
    )


def load_track_events(
    csv_path: Path,
    target_events: set,
    window: float,
    video_duration: float,
) -> list:
    """
    Object Tracker 出力 (track_events.csv) をトリガーソースとして読み込む。
    timestamp_s 列を中心に ±window 秒の区間を生成。
    （Object Tracker 実装後に対応予定）
    """
    return _csv_load_event_ranges(
        csv_path, "timestamp_s", "frame_status",
        target_events, window, video_duration, "track"
    )


def load_frame_delta(
    csv_path: Path,
    target_events: set,
    pos_delta_min: float,
    window: float,
    video_duration: float,
) -> list:
    """
    旧 frame_delta.csv 形式のトリガーソース（後方互換）。
    OBJECT_MOVE は pos_delta_min 以上の場合のみトリガー。
    """
    if not csv_path.exists():
        print(f"  [ERROR] delta-csv が見つかりません: {csv_path}", file=sys.stderr)
        return []

    ranges = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ev = row.get("event_type", "").strip()
            if ev not in target_events:
                continue
            if ev == "OBJECT_MOVE":
                try:
                    pos_val = float(row.get("position_delta_px", 0) or 0)
                except ValueError:
                    pos_val = 0.0
                if pos_val < pos_delta_min:
                    continue
            try:
                ts_prev = float(row.get("timestamp_prev_s", 0))
                ts_curr = float(row.get("timestamp_curr_s", ts_prev))
            except ValueError:
                continue
            ts_center = (ts_prev + ts_curr) / 2.0
            start = _clamp(ts_center - window, 0.0, video_duration)
            end   = _clamp(ts_center + window, 0.0, video_duration)
            pair_id = row.get("pair_id", "?")
            ranges.append({
                "start":  start,
                "end":    end,
                "source": "delta",
                "label":  f"delta_{ev}_{int(ts_curr)}s",
                "triggers": [{"type": "delta", "event": ev, "ts_curr": ts_curr, "pair_id": pair_id}],
            })
    return ranges


# ── レンジマージ ─────────────────────────────────────────────────

def merge_ranges(raw_ranges: list, merge_gap: float = DEFAULT_MERGE_GAP) -> list:
    """
    重複・近接するレンジをマージする。
    merge_gap 秒以内に隣接するレンジは1つにまとめる。
    """
    if not raw_ranges:
        return []
    sorted_ranges = sorted(raw_ranges, key=lambda r: r["start"])
    merged = [dict(sorted_ranges[0])]

    for r in sorted_ranges[1:]:
        last = merged[-1]
        if r["start"] <= last["end"] + merge_gap:
            last["end"] = max(last["end"], r["end"])
            last["triggers"] = last.get("triggers", []) + r.get("triggers", [])
            last["source"]   = "merged"
        else:
            merged.append(dict(r))

    return merged


# ── タイムスタンプ生成 ───────────────────────────────────────────

def generate_timestamps(
    merged_ranges: list,
    interval: float,
    existing_ts: set,
    skip_margin: float = None,
) -> list:
    """
    各レンジについて interval ごとのタイムスタンプを生成。
    既存タイムスタンプと ±skip_margin 秒以内に近接するものはスキップ。
    Returns: [{"ts": float, "range_idx": int, "skipped": bool}, ...]
    """
    if skip_margin is None:
        skip_margin = interval * 0.40

    results = []
    for idx, rng in enumerate(merged_ranges):
        ts = rng["start"]
        while ts <= rng["end"] + 1e-6:
            ts_r = round(ts, 3)
            skip = any(abs(ts_r - ex) <= skip_margin for ex in existing_ts)
            results.append({"ts": ts_r, "range_idx": idx, "skipped": skip})
            ts = round(ts + interval, 3)

    return results


# ── ログ出力（JSON） ─────────────────────────────────────────────

def write_precision_log(log_data: dict, out_path: Path):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


# ── CLI ─────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description=f"{VERSION}: 粗解析結果から必要区間を高密度抽出する Precision Sampler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
トリガーソースは複数同時指定可。指定なしの場合はエラー。

例 (手動区間):
  %(prog)s --video video.mp4 \\
    --manual-windows "22:30,49:57,253:263" \\
    --existing-frames-dir data/adaptive_frames/.../ \\
    --interval 0.25 --execute

例 (Camera Analyzer トリガー):
  %(prog)s --video video.mp4 \\
    --camera-events-csv .../camera_events.csv \\
    --camera-trigger-events FOV_IN,FOV_OUT,EDGE_SURGE \\
    --existing-frames-dir data/adaptive_frames/.../ \\
    --interval 0.25 --execute
""",
    )

    # 動画・既存フレーム
    p.add_argument("--video",               required=True, type=Path,
                   help="元動画ファイルパス")
    p.add_argument("--existing-frames-dir", required=True, type=Path,
                   help="既存 Adaptive Frame ディレクトリ（重複スキップ用）")
    p.add_argument("--output-dir",          type=Path,
                   help="出力先（省略時: <existing-frames-dir>_targeted/）")

    # ── トリガーソース ──────────────────────────────
    trig = p.add_argument_group("トリガーソース（1つ以上必須、複数指定可）")

    trig.add_argument("--manual-windows", default="",
                      help='手動区間 "START:END,START:END,..." (秒指定)')

    trig.add_argument("--camera-events-csv", type=Path,
                      help="Camera Analyzer 出力 (camera_events.csv)")
    trig.add_argument("--camera-trigger-events",
                      default="FOV_IN,FOV_OUT,EDGE_SURGE,COMBINED,BLACKOUT,WHITEOUT",
                      help="Camera Analyzer のトリガーイベント種別（カンマ区切り）")

    trig.add_argument("--motion-events-csv", type=Path,
                      help="Motion Intelligence 出力 (motion_events.csv)")
    trig.add_argument("--motion-trigger-events",
                      default="DISAPPEAR,APPEAR,LARGE_MOVE,ERRATIC",
                      help="Motion Intelligence のトリガーイベント種別（カンマ区切り）")

    trig.add_argument("--track-events-csv", type=Path,
                      help="Object Tracker 出力 (track_events.csv)")
    trig.add_argument("--track-trigger-events",
                      default="FRAMEOUT,REAPPEARED,MASKED_ENTRY,MASKED_EXIT",
                      help="Object Tracker のトリガーイベント種別（カンマ区切り）")

    # 後方互換: frame_delta.csv モード
    trig.add_argument("--delta-csv", type=Path,
                      help="【後方互換】frame_delta.csv (旧フォーマット)")
    trig.add_argument("--events", default="DISAPPEAR,APPEAR,OBJECT_MOVE",
                      help="【後方互換】delta-csv のトリガーイベント（カンマ区切り）")
    trig.add_argument("--pos-delta-min", type=float, default=DEFAULT_POS_DELTA_MIN,
                      help="【後方互換】OBJECT_MOVE の最小移動量 px（デフォルト 100）")

    # ── サンプリング設定 ────────────────────────────
    samp = p.add_argument_group("サンプリング設定")
    samp.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                      help=f"抽出間隔（秒、デフォルト {DEFAULT_INTERVAL}）推奨: 0.25 または 0.1")
    samp.add_argument("--window",   type=float, default=DEFAULT_WINDOW,
                      help=f"トリガー前後の抽出範囲（秒、デフォルト ±{DEFAULT_WINDOW}）")
    samp.add_argument("--merge-gap", type=float, default=DEFAULT_MERGE_GAP,
                      help=f"近接レンジのマージ閾値（秒、デフォルト {DEFAULT_MERGE_GAP}）")

    # ── 実行制御 ────────────────────────────────────
    p.add_argument("--execute", action="store_true",
                   help="実行モード（省略時は dry-run）")
    p.add_argument("--verbose", action="store_true",
                   help="詳細ログを表示")

    return p.parse_args()


def main():
    args = parse_args()

    video_path    = args.video
    existing_dir  = args.existing_frames_dir
    output_dir    = args.output_dir or Path(str(existing_dir).rstrip("/") + "_targeted")
    log_json_path = output_dir / "precision_sampling_log.json"

    # ── 入力検証 ─────────────────────────────────────
    for p, label in [(video_path, "--video"), (existing_dir, "--existing-frames-dir")]:
        if not p.exists():
            sys.exit(f"[ERROR] {label} が見つかりません: {p}")

    # トリガーソースが1つ以上指定されているか
    has_trigger = (
        args.manual_windows.strip()
        or args.camera_events_csv
        or args.motion_events_csv
        or args.track_events_csv
        or args.delta_csv
    )
    if not has_trigger:
        sys.exit(
            "[ERROR] トリガーソースが1つも指定されていません。\n"
            "  --manual-windows, --camera-events-csv, --motion-events-csv, "
            "--track-events-csv, --delta-csv のいずれかを指定してください。"
        )

    mode = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"[{VERSION}] mode={mode}")
    print(f"  video             : {video_path}")
    print(f"  existing_dir      : {existing_dir}")
    print(f"  output_dir        : {output_dir}/")
    print(f"  interval          : {args.interval}s")
    print(f"  window            : ±{args.window}s")
    print(f"  merge_gap         : {args.merge_gap}s")
    print()

    # ── 映像情報 ────────────────────────────────────
    video_duration = get_video_duration(video_path)
    print(f"  video_duration    : {video_duration:.1f}s")

    # ── 既存フレーム ─────────────────────────────────
    existing_ts = parse_existing_timestamps(existing_dir)
    print(f"  既存フレーム      : {len(existing_ts)} 枚")
    print()

    # ── トリガーソース読み込み ────────────────────────
    all_raw_ranges = []
    trigger_source_log = []

    # 1. 手動区間
    if args.manual_windows.strip():
        windows = load_manual_windows(args.manual_windows, video_duration)
        print(f"[手動区間] {len(windows)} 区間を読み込みました")
        for w in windows:
            print(f"  {w['label']}: {w['start']:.1f}s 〜 {w['end']:.1f}s")
        all_raw_ranges.extend(windows)
        trigger_source_log.append({
            "type": "manual_windows",
            "spec": args.manual_windows,
            "count": len(windows),
        })
        print()

    # 2. Camera Analyzer
    if args.camera_events_csv:
        cam_events = set(e.strip() for e in args.camera_trigger_events.split(","))
        cam_ranges = load_camera_events(
            args.camera_events_csv, cam_events, args.window, video_duration
        )
        print(f"[Camera Events] {len(cam_ranges)} トリガーを検出 (events={sorted(cam_events)})")
        for r in cam_ranges:
            print(f"  {r['label']}: {r['start']:.1f}s 〜 {r['end']:.1f}s")
        all_raw_ranges.extend(cam_ranges)
        trigger_source_log.append({
            "type": "camera_events",
            "csv": str(args.camera_events_csv),
            "events": sorted(cam_events),
            "count": len(cam_ranges),
        })
        print()

    # 3. Motion Intelligence
    if args.motion_events_csv:
        mot_events = set(e.strip() for e in args.motion_trigger_events.split(","))
        mot_ranges = load_motion_events(
            args.motion_events_csv, mot_events, args.window, video_duration
        )
        print(f"[Motion Events] {len(mot_ranges)} トリガーを検出 (events={sorted(mot_events)})")
        all_raw_ranges.extend(mot_ranges)
        trigger_source_log.append({
            "type": "motion_events",
            "csv": str(args.motion_events_csv),
            "events": sorted(mot_events),
            "count": len(mot_ranges),
        })
        print()

    # 4. Object Tracker
    if args.track_events_csv:
        trk_events = set(e.strip() for e in args.track_trigger_events.split(","))
        trk_ranges = load_track_events(
            args.track_events_csv, trk_events, args.window, video_duration
        )
        print(f"[Track Events] {len(trk_ranges)} トリガーを検出 (events={sorted(trk_events)})")
        all_raw_ranges.extend(trk_ranges)
        trigger_source_log.append({
            "type": "track_events",
            "csv": str(args.track_events_csv),
            "events": sorted(trk_events),
            "count": len(trk_ranges),
        })
        print()

    # 5. 後方互換: frame_delta.csv
    if args.delta_csv:
        delta_events = set(e.strip() for e in args.events.split(","))
        delta_ranges = load_frame_delta(
            args.delta_csv, delta_events, args.pos_delta_min, args.window, video_duration
        )
        print(f"[Delta CSV] {len(delta_ranges)} トリガーを検出 (events={sorted(delta_events)})")
        all_raw_ranges.extend(delta_ranges)
        trigger_source_log.append({
            "type": "frame_delta",
            "csv": str(args.delta_csv),
            "events": sorted(delta_events),
            "pos_delta_min": args.pos_delta_min,
            "count": len(delta_ranges),
        })
        print()

    if not all_raw_ranges:
        print("[結果] 有効なトリガーが0件のため、抽出対象なし。終了します。")
        return

    # ── レンジマージ ─────────────────────────────────
    merged = merge_ranges(all_raw_ranges, args.merge_gap)
    total_sec = sum(r["end"] - r["start"] for r in merged)
    print(f"[レンジマージ後] {len(merged)} 区間 (合計 {total_sec:.1f}s)")
    for i, r in enumerate(merged):
        n_trigs = len(r.get("triggers", []))
        sources = sorted(set(t.get("type", "?") for t in r.get("triggers", [])))
        print(
            f"  区間 {i+1}: {r['start']:.2f}s 〜 {r['end']:.2f}s"
            f"  (トリガー {n_trigs}件, sources={sources})"
        )

    # ── タイムスタンプ生成 ────────────────────────────
    print()
    ts_entries = generate_timestamps(merged, args.interval, existing_ts)
    new_ts  = [e for e in ts_entries if not e["skipped"]]
    skip_ts = [e for e in ts_entries if e["skipped"]]

    print(f"[タイムスタンプ] 合計 {len(ts_entries)} 個")
    print(f"  抽出対象: {len(new_ts)} 個")
    print(f"  スキップ（既存と重複）: {len(skip_ts)} 個")

    if args.verbose and new_ts:
        print("  抽出予定タイムスタンプ（先頭20個）:")
        for e in new_ts[:20]:
            print(f"    {e['ts']:.3f}s → {ts_to_filename(e['ts'], args.interval)}")
        if len(new_ts) > 20:
            print(f"    ... 他 {len(new_ts)-20} 個")

    if not args.execute:
        print()
        print(
            f"[DRY-RUN 完了]"
            f" --execute を付けると {len(new_ts)} フレームを"
            f" {output_dir}/ に抽出します。"
        )
        return

    # ── EXECUTE ──────────────────────────────────────
    output_dir.mkdir(parents=True, exist_ok=True)
    extracted = 0
    failed    = 0

    print(f"\n[EXECUTE] {len(new_ts)} フレームを抽出中...")
    for entry in new_ts:
        ts       = entry["ts"]
        filename = ts_to_filename(ts, args.interval)
        out_path = output_dir / filename
        ok       = extract_frame(video_path, ts, out_path)
        if ok:
            extracted += 1
            if args.verbose:
                print(f"  ✓ {filename} ({ts:.3f}s)")
        else:
            failed += 1
            print(f"  ✗ {filename} ({ts:.3f}s) — ffmpeg 失敗", file=sys.stderr)

    # ── ログ出力 ─────────────────────────────────────
    log_data = {
        "version":         VERSION,
        "run_date":        date.today().isoformat(),
        "run_timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "video":           str(video_path),
        "existing_dir":    str(existing_dir),
        "output_dir":      str(output_dir),
        "interval_sec":    args.interval,
        "window_sec":      args.window,
        "merge_gap_sec":   args.merge_gap,
        "video_duration_sec": video_duration,
        "trigger_sources": trigger_source_log,
        "merged_ranges": [
            {
                "start":    r["start"],
                "end":      r["end"],
                "source":   r["source"],
                "n_triggers": len(r.get("triggers", [])),
                "trigger_sources": sorted(set(
                    t.get("type", "?") for t in r.get("triggers", [])
                )),
            }
            for r in merged
        ],
        "statistics": {
            "n_ranges":          len(merged),
            "total_window_sec":  round(total_sec, 1),
            "n_timestamps_total": len(ts_entries),
            "n_timestamps_new":  len(new_ts),
            "n_timestamps_skipped": len(skip_ts),
            "n_frames_extracted": extracted,
            "n_frames_failed":   failed,
        },
    }
    write_precision_log(log_data, log_json_path)

    print()
    print("[完了]")
    print(f"  抽出成功: {extracted} フレーム")
    print(f"  スキップ: {len(skip_ts)} フレーム（既存と重複）")
    print(f"  失敗    : {failed} フレーム")
    print(f"  出力先  : {output_dir}/")
    print(f"  ログ    : {log_json_path}")


if __name__ == "__main__":
    main()
