#!/usr/bin/env python3
"""
extract_frames_for_article.py — 記事用動画メタデータ取得 & フレーム抽出

設計根拠: docs/release02_audio_video_pipeline_design.md Section 11
出力形式: thumbnails/<slug>/frame_XXXX.png（4桁秒数ゼロ埋め）+ metadata.json

使い方:
  # dry-run（既存動画で抽出計画を確認）
  python3 scripts/extract_frames_for_article.py \
    --input "raw_media/video/DOW-UAP-PR050_*.mp4" --slug DOW-UAP-PR050 --dry-run

  # 新規動画から抽出
  python3 scripts/extract_frames_for_article.py \
    --input raw_media/video/DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission.mp4 \
    --slug DOW-UAP-PR052 --article-id "#R02-010" --interval 30 --max-frames 8

引数:
  --input       入力動画ファイルパス（必須）
  --article-id  記事ID（例: #R02-010）
  --slug        出力スラッグ（thumbnails/<slug>/ のフォルダ名）
  --output-dir  出力先ディレクトリ（デフォルト: thumbnails/<slug>/）
  --interval    フレーム抽出間隔（秒、デフォルト: 30）
  --max-frames  最大フレーム数（デフォルト: 10）
  --dry-run     ファイル生成せず抽出予定を表示
  --force       既存フレームを上書き（デフォルト: スキップ）
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# S_CLASS ガード（§3-B、codex_request_gen.py と同一パターン）
_S_CLASS_RE = re.compile(r"S[_-]?CLASS", re.IGNORECASE)

DEFAULT_INTERVAL = 30
DEFAULT_MAX_FRAMES = 10


# ── ガード ────────────────────────────────────────────────────────────────────

def _check_s_class(*values: str) -> None:
    for val in values:
        if _S_CLASS_RE.search(val):
            sys.exit(f"[HARD STOP] S_CLASS 検出: '{val}' — 処理を停止します。")


# ── ffprobe ───────────────────────────────────────────────────────────────────

def run_ffprobe(input_path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        input_path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        sys.exit("[ERROR] ffprobe が見つかりません。brew install ffmpeg を実行してください。")
    if result.returncode != 0:
        sys.exit(f"[ERROR] ffprobe 失敗:\n{result.stderr.strip()}")
    return json.loads(result.stdout)


def _get_duration(probe: dict) -> float:
    fmt = probe.get("format", {})
    if "duration" in fmt:
        return float(fmt["duration"])
    for s in probe.get("streams", []):
        if "duration" in s:
            return float(s["duration"])
    return 0.0


def _get_video_stream(probe: dict) -> dict:
    for s in probe.get("streams", []):
        if s.get("codec_type") == "video":
            return s
    return {}


# ── フレーム計算 ──────────────────────────────────────────────────────────────

def compute_timestamps(duration: float, interval: int, max_frames: int) -> list:
    """固定間隔でタイムスタンプ（整数秒）を計算。最低1フレームを保証。"""
    if duration <= 0:
        return [0]
    timestamps = []
    t = 0
    while t < duration and len(timestamps) < max_frames:
        timestamps.append(int(t))
        t += interval
    return timestamps or [0]


def _fmt_duration(secs: float) -> str:
    h = int(secs) // 3600
    m = (int(secs) % 3600) // 60
    s = int(secs) % 60
    return f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"


def _fmt_ts(sec: int) -> str:
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


# ── ffmpeg ────────────────────────────────────────────────────────────────────

def extract_frame(input_path: str, out_path: Path, ts_sec: int, force: bool) -> bool:
    overwrite = "-y" if force else "-n"
    cmd = [
        "ffmpeg",
        "-ss", _fmt_ts(ts_sec),
        "-i", input_path,
        "-vframes", "1",
        overwrite,
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0


# ── メイン ────────────────────────────────────────────────────────────────────

def resolve_input(path_str: str) -> Path:
    """glob を含むパスを解決して Path を返す。"""
    p = Path(path_str)
    if p.exists():
        return p
    matches = sorted(Path(".").glob(path_str))
    if not matches:
        sys.exit(f"[ERROR] 入力ファイルが見つかりません: {path_str}")
    if len(matches) > 1:
        print(f"[WARN] 複数ファイルが一致しました。先頭を使用: {matches[0]}")
    return matches[0]


def derive_slug(input_path: Path) -> str:
    """ファイル名から catalog_id 相当のスラッグを生成する。

    例: DOW-UAP-PR050_4_UAP_Formation... → DOW-UAP-PR050
        NASA-UAP-D009_Apollo_17_...      → NASA-UAP-D009
    """
    return input_path.stem.split("_")[0]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="記事用動画フレーム抽出スクリプト",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input",       required=True, help="入力動画ファイルパス")
    parser.add_argument("--article-id",  default="",   help="記事ID（例: #R02-010）")
    parser.add_argument("--slug",        default="",   help="出力スラッグ（省略時はファイル名から自動生成）")
    parser.add_argument("--output-dir",  default="",   help="出力先ディレクトリ（省略時: thumbnails/<slug>/）")
    parser.add_argument("--interval",    type=int, default=DEFAULT_INTERVAL,
                        help=f"フレーム抽出間隔（秒、デフォルト: {DEFAULT_INTERVAL}）")
    parser.add_argument("--max-frames",  type=int, default=DEFAULT_MAX_FRAMES,
                        help=f"最大フレーム数（デフォルト: {DEFAULT_MAX_FRAMES}）")
    parser.add_argument("--dry-run",     action="store_true", help="ファイル生成せず抽出予定を表示")
    parser.add_argument("--force",       action="store_true", help="既存フレームを上書き")
    args = parser.parse_args()

    # 入力解決
    input_path = resolve_input(args.input)

    # スラッグ確定
    slug = args.slug or derive_slug(input_path)

    # S_CLASS ガード
    _check_s_class(slug, str(input_path))

    # 出力先
    output_dir = Path(args.output_dir) if args.output_dir else Path("thumbnails") / slug

    SEP = "─" * 60
    print(SEP)
    print("[extract_frames_for_article]")
    print(f"  入力        : {input_path}  ({input_path.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"  スラッグ    : {slug}")
    print(f"  出力先      : {output_dir}/")
    print(f"  間隔        : {args.interval}秒")
    print(f"  最大フレーム: {args.max_frames}枚")
    print(f"  dry-run     : {args.dry_run}")
    print(f"  force       : {args.force}")
    if args.article_id:
        print(f"  記事ID      : {args.article_id}")
    print(SEP)

    # ── Step 1: ffprobe ──────────────────────────────────────────────────────
    print("\n[Step 1] ffprobe メタデータ取得...")
    probe     = run_ffprobe(str(input_path))
    duration  = _get_duration(probe)
    fmt       = probe.get("format", {})
    vstm      = _get_video_stream(probe)

    file_size_mb   = int(fmt.get("size", 0)) / 1024 / 1024
    bit_rate_kbps  = int(fmt.get("bit_rate", 0)) // 1000
    codec_name     = vstm.get("codec_name", "不明")
    width          = vstm.get("width", "?")
    height         = vstm.get("height", "?")
    r_frame_rate   = vstm.get("r_frame_rate", "?")
    has_audio      = any(s.get("codec_type") == "audio" for s in probe.get("streams", []))
    nb_streams     = len(probe.get("streams", []))

    print(f"  再生時間    : {duration:.2f}秒 ({_fmt_duration(duration)})")
    print(f"  ファイルサイズ : {file_size_mb:.2f} MB")
    print(f"  ビットレート  : {bit_rate_kbps} kbps")
    print(f"  映像コーデック: {codec_name} / {width}x{height} / {r_frame_rate} fps")
    print(f"  音声トラック  : {'あり' if has_audio else 'なし'}")
    print(f"  ストリーム数  : {nb_streams}")

    # ── Step 2: タイムスタンプ計算 ──────────────────────────────────────────
    timestamps = compute_timestamps(duration, args.interval, args.max_frames)

    # フレームパスと状態を計算
    frame_plan = []
    for ts in timestamps:
        fname    = f"frame_{ts:04d}.png"
        out_path = output_dir / fname
        exists   = out_path.exists()
        frame_plan.append((ts, out_path, exists))

    print(f"\n[Step 2] 抽出予定フレーム（{len(frame_plan)}枚 / 動画長 {_fmt_duration(duration)}）:")
    for ts, out_path, exists in frame_plan:
        note = ""
        if exists and not args.force:
            note = "  ← スキップ（既存）"
        elif exists and args.force:
            note = "  ← 上書き"
        print(f"  frame_{ts:04d}.png  ({_fmt_ts(ts)}){note}")

    # metadata.json の構造
    metadata = {
        "source_file":          str(input_path),
        "slug":                 slug,
        "article_id":           args.article_id,
        "duration_sec":         round(duration, 2),
        "duration_fmt":         _fmt_duration(duration),
        "file_size_mb":         round(file_size_mb, 2),
        "bit_rate_kbps":        bit_rate_kbps,
        "video_codec":          codec_name,
        "resolution":           f"{width}x{height}",
        "frame_rate":           r_frame_rate,
        "has_audio":            has_audio,
        "stream_count":         nb_streams,
        "extraction_interval_sec": args.interval,
        "max_frames":           args.max_frames,
        "frame_count":          len(timestamps),
        "frames":               [f"frame_{ts:04d}.png" for ts in timestamps],
        "extracted_at":         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # ── dry-run ──────────────────────────────────────────────────────────────
    if args.dry_run:
        print(f"\n[dry-run] 生成予定ファイル:")
        print(f"  {output_dir}/metadata.json")
        for _, out_path, _ in frame_plan:
            print(f"  {out_path}")
        print(f"\n[dry-run] metadata.json プレビュー:")
        print(json.dumps(metadata, ensure_ascii=False, indent=2))
        print(f"\n[dry-run] 完了。--dry-run を外して実行するとフレーム抽出を実施します。")
        return

    # ── Step 3: フレーム抽出 ─────────────────────────────────────────────────
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n[Step 3] フレーム抽出...")
    extracted = skipped = failed = 0

    for ts, out_path, exists in frame_plan:
        if exists and not args.force:
            print(f"  スキップ : {out_path.name}")
            skipped += 1
            continue
        ok = extract_frame(str(input_path), out_path, ts, args.force)
        if ok:
            sz = out_path.stat().st_size / 1024
            print(f"  抽出済み : {out_path.name}  ({sz:.0f} KB)")
            extracted += 1
        else:
            print(f"  [FAIL]   : {out_path.name}")
            failed += 1

    # metadata.json 保存
    meta_path = output_dir / "metadata.json"
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  保存済み : {meta_path}")

    print(f"\n[完了] 抽出={extracted}  スキップ={skipped}  失敗={failed}")
    print(f"  出力先: {output_dir}/")

    # note 記事参照例（初回抽出のみ表示）
    if extracted > 0:
        print(f"\n  note 記事ドラフトでの参照例:")
        for ts, out_path, exists in frame_plan[:2]:
            if not exists or args.force:
                print(f"    【画像①】{out_path}")
                break


if __name__ == "__main__":
    main()
