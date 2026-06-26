#!/usr/bin/env python3
"""
run_vlm_on_adaptive.py - Run Qwen2.5-VL on adaptive-extracted frames via LM Studio.

Purpose:
  Evaluate UAP visibility in frames from data/adaptive_frames/<run_date>/<slug>/
  using the same JSON output schema as Phase 3 VLM results.

Safety:
  - Never modifies thumbnails/, note_drafts/, workflow.db, or source_registry.csv
  - Writes only to data/vlm_runs/<run_id>/
  - Requires --execute flag; default is dry-run
  - No external API calls (LM Studio local only)
  - Excludes S_CLASS records
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "qwen2.5-vl-7b-instruct"
MAX_TOKENS = 512
TEMPERATURE = 0.1

PROMPT_SYSTEM = (
    "あなたはUAP（未確認航空現象）映像解析の専門家です。"
    "提供された映像フレームを客観的に分析し、UAP候補となりうる対象物が存在するかを判定してください。"
)

PROMPT_USER = """以下の映像フレームを解析してください。

判定基準：
- visible_candidate: UAP候補となりうる対象物（光点・黒点・不明飛翔体・通常では説明できない動きの痕跡など）が確認できる場合 true
- confidence: 確信度 0.0〜1.0（0.0=全く見えない, 1.0=明確に見える）
- location: 対象の位置（画面上の位置を日本語で記述。例：中央、左上、右下）。対象なしの場合は "なし"
- description: 見えるもの・見えないものを客観的に記述（50文字以内）
- visual_confirmation_only: 目視確認のみ（推測なし）の場合 true
- speculation: 推測・解釈が含まれる場合 true

必ず以下のJSON形式のみで回答してください（説明文不要）：
{
  "visible_candidate": true/false,
  "confidence": 0.0〜1.0,
  "location": "位置の記述",
  "description": "対象の説明",
  "visual_confirmation_only": true/false,
  "speculation": false
}"""


def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def call_vlm(image_path: Path) -> tuple[dict, float, str]:
    import urllib.request

    b64 = encode_image(image_path)
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": PROMPT_SYSTEM},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64}"},
                    },
                    {"type": "text", "text": PROMPT_USER},
                ],
            },
        ],
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        LM_STUDIO_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    elapsed = time.time() - t0
    raw = result["choices"][0]["message"]["content"].strip()
    return result, elapsed, raw


def parse_vlm_response(raw: str) -> tuple[dict | None, bool]:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(
            l for l in lines if not l.startswith("```")
        ).strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        return None, False
    try:
        parsed = json.loads(text[start:end])
        return parsed, True
    except json.JSONDecodeError:
        return None, False


def baseline_timestamps(slug: str, frames: list[Path]) -> set[str]:
    """Return filenames that correspond to simulated baseline extraction."""
    frame_nums = sorted(int(f.stem.split("_")[1]) for f in frames)
    duration = max(frame_nums) if frame_nums else 0
    if duration <= 60:
        interval = 5
    else:
        interval = 30
    baseline = set()
    t = 0
    while t <= duration:
        nearest = min(frame_nums, key=lambda n: abs(n - t))
        baseline.add(f"frame_{nearest:04d}.png")
        t += interval
    return baseline


RESULTS_FIELDNAMES = [
    "sample_id", "article_id", "slug", "image_path", "frame_name",
    "is_baseline_equivalent",
    "visible_candidate", "confidence", "location", "description",
    "visual_confirmation_only", "speculation",
    "response_time_sec", "parse_success", "raw_response",
]


def run_article(
    slug: str,
    article_id: str,
    frames_dir: Path,
    out_dir: Path,
    execute: bool,
    verbose: bool,
) -> list[dict]:
    frames = sorted(frames_dir.glob("frame_*.png"))
    if not frames:
        print(f"  [SKIP] フレームなし: {frames_dir}")
        return []

    baseline = baseline_timestamps(slug, frames)
    print(f"  frames: {len(frames)}枚  baseline相当: {len(baseline)}枚")

    if not execute:
        print(f"  [DRY-RUN] 実際のVLM呼び出しはスキップ")
        return []

    rows: list[dict] = []
    for i, frame in enumerate(frames, start=1):
        sample_id = f"{article_id}_{frame.stem}"
        is_baseline = frame.name in baseline
        marker = "[B]" if is_baseline else "   "
        print(f"  {marker} {i:3d}/{len(frames)} {frame.name} ...", end="", flush=True)

        try:
            _, elapsed, raw = call_vlm(frame)
            parsed, ok = parse_vlm_response(raw)
        except Exception as e:
            print(f" ERROR: {e}")
            rows.append({
                "sample_id": sample_id,
                "article_id": article_id,
                "slug": slug,
                "image_path": str(frame),
                "frame_name": frame.name,
                "is_baseline_equivalent": is_baseline,
                "visible_candidate": None,
                "confidence": None,
                "location": None,
                "description": None,
                "visual_confirmation_only": None,
                "speculation": None,
                "response_time_sec": None,
                "parse_success": False,
                "raw_response": str(e),
            })
            continue

        if parsed:
            vc = parsed.get("visible_candidate", False)
            conf = parsed.get("confidence", 0.0)
            loc = parsed.get("location", "")
            desc = parsed.get("description", "")
            vco = parsed.get("visual_confirmation_only", True)
            spec = parsed.get("speculation", False)
        else:
            vc = conf = loc = desc = vco = spec = None

        flag = "✓" if (ok and vc) else ("·" if ok else "✗")
        print(f" {flag} conf={conf} {elapsed:.1f}s")
        if verbose and desc:
            print(f"         {desc}")

        rows.append({
            "sample_id": sample_id,
            "article_id": article_id,
            "slug": slug,
            "image_path": str(frame),
            "frame_name": frame.name,
            "is_baseline_equivalent": is_baseline,
            "visible_candidate": vc,
            "confidence": conf,
            "location": loc,
            "description": desc,
            "visual_confirmation_only": vco,
            "speculation": spec,
            "response_time_sec": round(elapsed, 2) if elapsed else None,
            "parse_success": ok,
            "raw_response": raw,
        })

    if rows and execute:
        csv_path = out_dir / f"{article_id}_results.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=RESULTS_FIELDNAMES)
            w.writeheader()
            w.writerows(rows)
        print(f"  → {csv_path}")

    return rows


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run VLM on adaptive-extracted frames.")
    p.add_argument("--run-date", default="20260626", help="Frame extraction run date")
    p.add_argument(
        "--articles",
        nargs="+",
        default=["R02-043", "R02-044", "R02-045", "R02-046"],
        help="Article IDs to process",
    )
    p.add_argument(
        "--slugs",
        nargs="+",
        default=[
            "DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025",
            "DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020",
            "DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020",
            "DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024",
        ],
    )
    p.add_argument("--frames-root", type=Path, default=Path("data/adaptive_frames"))
    p.add_argument("--output-root", type=Path, default=Path("data/vlm_runs"))
    p.add_argument("--run-id", default="adaptive_poc_20260626")
    p.add_argument("--execute", action="store_true")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if len(args.articles) != len(args.slugs):
        print("ERROR: --articles と --slugs の件数が一致しません", file=sys.stderr)
        return 2

    out_dir = args.output_root / args.run_id
    if args.execute:
        out_dir.mkdir(parents=True, exist_ok=True)

    mode = "[EXECUTE]" if args.execute else "[DRY-RUN]"
    print(f"{'─'*64}")
    print(f"[run_vlm_on_adaptive] {mode}")
    print(f"  run_date : {args.run_date}")
    print(f"  run_id   : {args.run_id}")
    print(f"  出力先   : {out_dir}")
    print(f"{'─'*64}")

    all_rows: list[dict] = []
    for article_id, slug in zip(args.articles, args.slugs):
        frames_dir = args.frames_root / args.run_date / slug
        print(f"\n[{article_id}] {slug}")
        rows = run_article(slug, article_id, frames_dir, out_dir, args.execute, args.verbose)
        all_rows.extend(rows)

    if args.execute and all_rows:
        combined_path = out_dir / "all_results.csv"
        with combined_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=RESULTS_FIELDNAMES)
            w.writeheader()
            w.writerows(all_rows)
        print(f"\n[完了] 全{len(all_rows)}件 → {combined_path}")

        # Summary
        detected = [r for r in all_rows if r["visible_candidate"]]
        baseline = [r for r in all_rows if r["is_baseline_equivalent"]]
        baseline_det = [r for r in detected if r["is_baseline_equivalent"]]
        new_only = [r for r in detected if not r["is_baseline_equivalent"]]
        print(f"\n--- 集計 ---")
        print(f"  処理フレーム数    : {len(all_rows)}")
        print(f"  ベースライン相当  : {len(baseline)}")
        print(f"  VLM検出件数       : {len(detected)}")
        print(f"  ベースライン検出  : {len(baseline_det)}")
        print(f"  新規検出（Adaptive only）: {len(new_only)}")
    elif not args.execute:
        print(f"\n[DRY-RUN完了] --execute を付けて再実行してください。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
