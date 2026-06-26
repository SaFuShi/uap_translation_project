#!/usr/bin/env python3
"""
extract_frames_adaptive.py — 映像内容に応じた高密度・可変フレーム抽出 PoC

設計方針:
  - 動画尺に応じてフレーム抽出間隔を自動選択（Adaptive）
  - --max-frames 上限を設けない（既存スクリプトの10枚制限を排除）
  - 出力先は data/adaptive_frames/<run_date>/<slug>/ （thumbnails/ を汚染しない）
  - 既存 thumbnails/ は一切変更しない
  - --dry-run でファイル生成なし・計画のみ表示
  - --interval で手動指定も可能

Adaptive 間隔ルール:
  duration < 15s  → 2秒間隔（超短尺・全体カバー）
  15s ≤ duration < 60s → 3秒間隔（短尺・全体カバー）
  60s ≤ duration < 180s → 5秒間隔（中尺）
  180s ≤ duration      → 10秒間隔（長尺・コスト重視）

  ※ --mode scene を指定するとシーン変化検出（ffmpeg select filter）を使用

使い方:
  # dry-run（自動間隔）
  python3 scripts/extract_frames_adaptive.py \\
    --input raw_media/video/DOW-UAP-PR044_*.mp4 \\
    --slug DOW-UAP-PR044 --dry-run

  # dry-run（間隔を手動指定）
  python3 scripts/extract_frames_adaptive.py \\
    --input raw_media/video/DOW-UAP-PR043_*.mp4 \\
    --slug DOW-UAP-PR043 --interval 2 --dry-run

  # 実行（出力先を明示）
  python3 scripts/extract_frames_adaptive.py \\
    --input raw_media/video/DOW-UAP-PR044_*.mp4 \\
    --slug DOW-UAP-PR044 \\
    --run-date 20260626 --execute

引数:
  --input       入力動画ファイルパス（必須）
  --slug        出力スラッグ（省略時: ファイル名から自動生成）
  --interval    固定間隔（秒）。省略時は動画尺から自動決定
  --mode        fixed（デフォルト）/ scene（シーン変化検出）
  --scene-thresh シーン変化閾値（0.0〜1.0、デフォルト: 0.4）
  --max-frames  最大フレーム数（デフォルト: 無制限）
  --run-date    出力ディレクトリの日付キー（デフォルト: 今日）
  --output-dir  出力先を明示指定（省略時: data/adaptive_frames/<run_date>/<slug>/）
  --dry-run     ファイル生成せず計画のみ表示（デフォルト: dry-run）
  --execute     実際にファイルを生成する（明示的に指定が必要）
  --compare     既存 thumbnails/ との比較サマリーを表示
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

# S_CLASS ガード
_S_CLASS_RE = re.compile(r"S[_-]?CLASS", re.IGNORECASE)

# Adaptive 間隔ルール
# UAP動画では対象物が短時間のみ出現・不規則移動の可能性があるため
# 間隔上限を3秒とし、10秒・5秒間隔は使用しない
ADAPTIVE_RULES = [
    (0,   15,  2,  "超短尺(<15s): 2秒間隔・全体カバー"),
    (15,  float("inf"), 3, "中〜長尺(≥15s): 3秒間隔（UAP取り逃がし防止）"),
]


# ── ガード ────────────────────────────────────────────────────────────────────

def _check_s_class(*values: str) -> None:
    for val in values:
        if _S_CLASS_RE.search(str(val)):
            sys.exit(f"[HARD STOP] S_CLASS 検出: '{val}' — 処理を停止します。")


# ── ffprobe ───────────────────────────────────────────────────────────────────

def run_ffprobe(input_path: str) -> dict:
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
           "-show_format", "-show_streams", input_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        sys.exit("[ERROR] ffprobe が見つかりません。brew install ffmpeg を実行してください。")
    if result.returncode != 0:
        sys.exit(f"[ERROR] ffprobe 失敗:\n{result.stderr.strip()}")
    return json.loads(result.stdout)


def get_duration(probe: dict) -> float:
    fmt = probe.get("format", {})
    if "duration" in fmt:
        return float(fmt["duration"])
    for s in probe.get("streams", []):
        if "duration" in s:
            return float(s["duration"])
    return 0.0


def get_video_stream(probe: dict) -> dict:
    for s in probe.get("streams", []):
        if s.get("codec_type") == "video":
            return s
    return {}


# ── Adaptive 間隔決定 ─────────────────────────────────────────────────────────

def adaptive_interval(duration: float) -> tuple[int, str]:
    """動画尺に応じた推奨抽出間隔（秒）とルール説明を返す。"""
    for lo, hi, interval, desc in ADAPTIVE_RULES:
        if lo <= duration < hi:
            return interval, desc
    return 10, "デフォルト: 10秒間隔"


# ── タイムスタンプ計算 ─────────────────────────────────────────────────────────

def compute_timestamps_fixed(duration: float, interval: int,
                              max_frames: int = 0) -> list[int]:
    """固定間隔でタイムスタンプ（整数秒）を計算。max_frames=0 は無制限。"""
    timestamps = []
    t = 0
    while t < duration:
        if max_frames > 0 and len(timestamps) >= max_frames:
            break
        timestamps.append(int(t))
        t += interval
    return timestamps or [0]


def compute_timestamps_scene(input_path: str, thresh: float,
                              max_frames: int = 0) -> list[int]:
    """ffmpeg select filter でシーン変化点のタイムスタンプを取得。"""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_frames",
        "-select_streams", "v",
        "-skip_frame", "noref",
        "-f", "lavfi",
        f"movie={input_path},select='gt(scene\\,{thresh})'",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as e:
        print(f"[WARN] シーン検出失敗 ({e})。固定間隔にフォールバック。")
        return []

    if result.returncode != 0:
        print(f"[WARN] シーン検出 ffprobe 失敗。固定間隔にフォールバック。")
        return []

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

    timestamps = []
    for frame in data.get("frames", []):
        pts = frame.get("best_effort_timestamp_time") or frame.get("pkt_pts_time")
        if pts is not None:
            ts = int(float(pts))
            if ts not in timestamps:
                timestamps.append(ts)
                if max_frames > 0 and len(timestamps) >= max_frames:
                    break
    return sorted(timestamps)


# ── フォーマット ──────────────────────────────────────────────────────────────

def fmt_duration(secs: float) -> str:
    h = int(secs) // 3600
    m = (int(secs) % 3600) // 60
    s = int(secs) % 60
    return f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"


def fmt_ts(sec: int) -> str:
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


# ── ffmpeg フレーム抽出 ───────────────────────────────────────────────────────

def extract_frame(input_path: str, out_path: Path, ts_sec: int) -> bool:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-ss", fmt_ts(ts_sec),
        "-i", input_path,
        "-vframes", "1",
        "-y",  # adaptive出力は新規ディレクトリなので上書き許可
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0


# ── 既存 thumbnails/ との比較 ─────────────────────────────────────────────────

def compare_with_existing(slug: str, adaptive_timestamps: list[int]) -> dict:
    thumb_dir = Path("thumbnails") / slug
    if not thumb_dir.exists():
        return {"existing_dir": None, "existing_frames": [], "coverage_gap": []}

    existing = sorted([
        int(p.stem.replace("frame_", ""))
        for p in thumb_dir.glob("frame_*.png")
    ])

    # 既存フレームに含まれていないタイムスタンプ（新規カバレッジ）
    existing_set = set(existing)
    new_coverage = [ts for ts in adaptive_timestamps if ts not in existing_set]

    # 既存メタデータから間隔を取得
    meta_path = thumb_dir / "metadata.json"
    existing_interval = None
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text())
            existing_interval = meta.get("extraction_interval_sec")
        except Exception:
            pass

    return {
        "existing_dir": str(thumb_dir),
        "existing_frames": existing,
        "existing_interval": existing_interval,
        "adaptive_timestamps": adaptive_timestamps,
        "new_coverage_count": len(new_coverage),
        "new_coverage_timestamps": new_coverage[:10],  # 最初の10件のみ表示
    }


# ── 解決 ─────────────────────────────────────────────────────────────────────

def resolve_input(path_str: str) -> Path:
    p = Path(path_str)
    if p.exists():
        return p
    matches = sorted(Path(".").glob(path_str))
    if not matches:
        sys.exit(f"[ERROR] 入力ファイルが見つかりません: {path_str}")
    if len(matches) > 1:
        print(f"[WARN] 複数ファイルが一致。先頭を使用: {matches[0]}")
    return matches[0]


def derive_slug(input_path: Path) -> str:
    return input_path.stem.split("_")[0] + "_" + "_".join(input_path.stem.split("_")[1:4])


# ── メイン ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Adaptive Frame Extraction — 映像尺に応じた可変フレーム抽出",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input",        required=True, help="入力動画ファイルパス")
    parser.add_argument("--slug",         default="",   help="出力スラッグ（省略時: ファイル名から生成）")
    parser.add_argument("--interval",     type=int, default=0,
                        help="固定間隔（秒）。省略時は動画尺から自動決定")
    parser.add_argument("--mode",         default="fixed", choices=["fixed", "scene"],
                        help="fixed（デフォルト）/ scene（シーン変化検出）")
    parser.add_argument("--scene-thresh", type=float, default=0.4,
                        help="シーン変化閾値（0.0〜1.0、デフォルト: 0.4）")
    parser.add_argument("--max-frames",   type=int, default=0,
                        help="最大フレーム数（デフォルト: 0=無制限）")
    parser.add_argument("--run-date",     default=date.today().strftime("%Y%m%d"),
                        help="出力ディレクトリの日付キー（デフォルト: 今日）")
    parser.add_argument("--output-dir",   default="",
                        help="出力先を明示指定（省略時: data/adaptive_frames/<run-date>/<slug>/）")
    parser.add_argument("--dry-run",      action="store_true", default=False,
                        help="計画のみ表示・ファイル生成しない（--execute がない場合はデフォルト）")
    parser.add_argument("--execute",      action="store_true", default=False,
                        help="実際にファイルを生成する（明示的に指定が必要）")
    parser.add_argument("--compare",      action="store_true", default=False,
                        help="既存 thumbnails/ との比較サマリーを表示")
    args = parser.parse_args()

    # --execute なければ dry-run 強制
    if not args.execute:
        args.dry_run = True

    # 入力解決
    input_path = resolve_input(args.input)

    # スラッグ確定
    slug = args.slug or derive_slug(input_path)

    # S_CLASS ガード
    _check_s_class(slug, str(input_path))

    # 出力先（thumbnails/ とは別の新規ディレクトリ）
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path("data") / "adaptive_frames" / args.run_date / slug

    SEP = "─" * 65
    print(SEP)
    print("[extract_frames_adaptive]")
    print(f"  入力        : {input_path}  ({input_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"  スラッグ    : {slug}")
    print(f"  出力先      : {output_dir}/")
    print(f"  mode        : {args.mode}")
    print(f"  max-frames  : {'無制限' if args.max_frames == 0 else args.max_frames}")
    print(f"  {'[DRY-RUN]' if args.dry_run else '[EXECUTE]'}")
    print(SEP)

    # ── Step 1: ffprobe ──────────────────────────────────────────────────────
    print("\n[Step 1] ffprobe メタデータ取得...")
    probe    = run_ffprobe(str(input_path))
    duration = get_duration(probe)
    vstm     = get_video_stream(probe)
    fmt      = probe.get("format", {})

    file_size_mb  = int(fmt.get("size", 0)) / 1024 / 1024
    bit_rate_kbps = int(fmt.get("bit_rate", 0)) // 1000
    codec_name    = vstm.get("codec_name", "不明")
    width         = vstm.get("width", "?")
    height        = vstm.get("height", "?")
    r_frame_rate  = vstm.get("r_frame_rate", "?")
    has_audio     = any(s.get("codec_type") == "audio" for s in probe.get("streams", []))

    print(f"  再生時間    : {duration:.2f}秒 ({fmt_duration(duration)})")
    print(f"  解像度      : {width}x{height}  {codec_name}  {r_frame_rate} fps")
    print(f"  ファイルサイズ: {file_size_mb:.2f} MB  {bit_rate_kbps} kbps")
    print(f"  音声        : {'あり' if has_audio else 'なし'}")

    # ── Step 2: 間隔決定 ────────────────────────────────────────────────────
    if args.interval > 0:
        interval = args.interval
        interval_desc = f"手動指定: {interval}秒"
    else:
        interval, interval_desc = adaptive_interval(duration)

    print(f"\n[Step 2] 抽出間隔決定:")
    print(f"  → {interval}秒間隔  ({interval_desc})")

    # ── Step 3: タイムスタンプ計算 ──────────────────────────────────────────
    print(f"\n[Step 3] タイムスタンプ計算 (mode={args.mode})...")
    if args.mode == "scene":
        print(f"  シーン変化検出 (thresh={args.scene_thresh})...")
        timestamps = compute_timestamps_scene(
            str(input_path), args.scene_thresh, args.max_frames
        )
        if not timestamps:
            print(f"  [WARN] シーン検出で取得できず。固定間隔({interval}s)にフォールバック。")
            timestamps = compute_timestamps_fixed(duration, interval, args.max_frames)
    else:
        timestamps = compute_timestamps_fixed(duration, interval, args.max_frames)

    frame_plan = [(ts, output_dir / f"frame_{ts:04d}.png") for ts in timestamps]

    print(f"  抽出予定: {len(frame_plan)}枚 (動画長: {fmt_duration(duration)})")

    print(f"\n[Step 4] フレーム一覧:")
    show_max = 20
    for i, (ts, out_path) in enumerate(frame_plan):
        if i < show_max:
            print(f"  frame_{ts:04d}.png  ({fmt_ts(ts)})")
        elif i == show_max:
            print(f"  ... (残り {len(frame_plan) - show_max} 枚省略)")

    # ── 既存 thumbnails/ との比較 ────────────────────────────────────────────
    if args.compare:
        print(f"\n[Step 5] 既存 thumbnails/ との比較:")
        comp = compare_with_existing(slug, timestamps)
        if comp["existing_dir"]:
            print(f"  既存ディレクトリ  : {comp['existing_dir']}")
            print(f"  既存間隔          : {comp.get('existing_interval')}秒")
            print(f"  既存フレーム数    : {len(comp['existing_frames'])}枚")
            print(f"  Adaptive フレーム : {len(timestamps)}枚")
            print(f"  新規カバレッジ数  : {comp['new_coverage_count']}枚（既存に存在しないタイムスタンプ）")
            if comp['new_coverage_timestamps']:
                print(f"  新規カバレッジ例  : {comp['new_coverage_timestamps']}")
        else:
            print(f"  既存 thumbnails/ なし ({Path('thumbnails') / slug})")

    # metadata プレビュー
    metadata = {
        "source_file":         str(input_path),
        "slug":                slug,
        "duration_sec":        round(duration, 2),
        "duration_fmt":        fmt_duration(duration),
        "file_size_mb":        round(file_size_mb, 2),
        "bit_rate_kbps":       bit_rate_kbps,
        "video_codec":         codec_name,
        "resolution":          f"{width}x{height}",
        "frame_rate":          r_frame_rate,
        "has_audio":           has_audio,
        "extraction_mode":     args.mode,
        "extraction_interval_sec": interval if args.mode == "fixed" else None,
        "scene_threshold":     args.scene_thresh if args.mode == "scene" else None,
        "max_frames_limit":    args.max_frames if args.max_frames > 0 else "unlimited",
        "frame_count":         len(timestamps),
        "frames":              [f"frame_{ts:04d}.png" for ts in timestamps],
        "output_dir":          str(output_dir),
        "adaptive_rule":       interval_desc,
    }

    # ── dry-run ──────────────────────────────────────────────────────────────
    if args.dry_run:
        print(f"\n[DRY-RUN] 生成予定ファイル:")
        print(f"  {output_dir}/metadata.json")
        for ts, out_path in frame_plan[:5]:
            print(f"  {out_path}")
        if len(frame_plan) > 5:
            print(f"  ... (他 {len(frame_plan) - 5} 件)")
        print(f"\n[DRY-RUN] metadata preview (抜粋):")
        preview = {k: v for k, v in metadata.items() if k != "frames"}
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        print(f"\n[DRY-RUN] 完了。--execute を追加するとフレーム抽出を実施します。")
        return

    # ── 実行 ─────────────────────────────────────────────────────────────────
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n[EXECUTE] フレーム抽出開始...")
    extracted = failed = 0
    for ts, out_path in frame_plan:
        ok = extract_frame(str(input_path), out_path, ts)
        if ok:
            sz = out_path.stat().st_size / 1024
            print(f"  ✓ frame_{ts:04d}.png  ({sz:.0f} KB)")
            extracted += 1
        else:
            print(f"  ✗ [FAIL] frame_{ts:04d}.png")
            failed += 1

    # metadata.json 保存
    meta_path = output_dir / "metadata.json"
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n[完了] 抽出={extracted}  失敗={failed}")
    print(f"  出力先: {output_dir}/")
    print(f"  metadata: {meta_path}")


if __name__ == "__main__":
    main()
