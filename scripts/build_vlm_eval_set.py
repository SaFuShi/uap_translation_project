#!/usr/bin/env python3
"""
build_vlm_eval_set.py - Build a local VLM evaluation image set.

Purpose:
  Create a fixed sample set from existing UAP project frames so local VLM
  candidates can be compared on the same inputs.

Safety:
  - --dry-run only prints the planned output; it does not create files
  - --execute copies images and writes manifests/README
  - never modifies source thumbnails, note_drafts, workflow.db, or registry CSV
  - excludes S_CLASS records
  - no external API calls
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sqlite3
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

REPORT_PATH = Path("review_reports/media_inspector_candidates_20260625.md")
DB_PATH = Path("workflow.db")
REGISTRY_PATH = Path("review_logs/source_registry.csv")
OUTPUT_ROOT = Path("data/vlm_eval_set")

CATEGORY_DESCRIPTIONS = {
    "A_clear_candidate": "UAPらしき対象が比較的明確に映っている可能性があるフレーム",
    "B_small_unclear": "小さい点・輝点・黒点・不鮮明対象の可能性があるフレーム",
    "C_no_visible_target": "対象が見えない、または地形・建物・センサー画面のみの可能性があるフレーム",
    "D_sensor_ui_background": "センサーUI、地形、建物、雲、海面など背景理解用",
    "E_known_miss_case": "人間が見落としを発見した既知ケース",
}

HEADER_RE = re.compile(r"^###\s+\d+\.\s+(R02-\d{3})\s+/\s+(#2_\d{3})\s+/\s+(.+)$")
PATH_RE = re.compile(r"`([^`]+)`")
FRAME_RE = re.compile(r"frame_(\d+)\.png$")


@dataclass
class ArticleBlock:
    article_id: str
    h2_number: str
    slug: str
    draft_path: str = ""
    frame_paths: list[str] | None = None
    recommended_frames: list[str] | None = None
    neg_expressions: list[str] | None = None


@dataclass
class Sample:
    sample_id: str
    category: str
    article_id: str
    h2_number: str
    slug: str
    source_frame_path: str
    copied_image_path: str
    draft_path: str
    neg_expression: str
    expected_human_label: str
    notes: str


def parse_report(path: Path) -> list[ArticleBlock]:
    if not path.exists():
        raise FileNotFoundError(f"Report not found: {path}")

    blocks: list[ArticleBlock] = []
    current: ArticleBlock | None = None
    section = ""

    for line in path.read_text(encoding="utf-8").splitlines():
        header = HEADER_RE.match(line)
        if header:
            current = ArticleBlock(
                article_id=header.group(1),
                h2_number=header.group(2),
                slug=header.group(3).strip(),
                frame_paths=[],
                recommended_frames=[],
                neg_expressions=[],
            )
            blocks.append(current)
            section = ""
            continue

        if current is None:
            continue

        stripped = line.strip()
        if stripped.startswith("- draft path:"):
            match = PATH_RE.search(stripped)
            current.draft_path = match.group(1) if match else ""
            section = ""
        elif stripped == "- frame paths:":
            section = "frames"
        elif stripped == "- NEG expression lines:":
            section = "neg"
        elif stripped == "- recommended review frames:":
            section = "recommended"
        elif stripped.startswith("- ") and section == "frames":
            match = PATH_RE.search(stripped)
            if match:
                current.frame_paths.append(match.group(1))
        elif stripped.startswith("- ") and section == "recommended":
            match = PATH_RE.search(stripped)
            if match:
                current.recommended_frames.append(match.group(1))
        elif stripped.startswith("- L") and section == "neg":
            current.neg_expressions.append(stripped.removeprefix("- ").strip())

    return blocks


def load_s_class_guards() -> tuple[set[str], set[str]]:
    s_class_article_ids: set[str] = set()
    s_class_slugs: set[str] = set()
    if not DB_PATH.exists():
        return s_class_article_ids, s_class_slugs

    conn = sqlite3.connect(str(DB_PATH))
    try:
        for slug, article_id in conn.execute(
            "SELECT slug, article_id FROM articles WHERE classification='S_CLASS'"
        ):
            if slug:
                s_class_slugs.add(slug)
            if article_id:
                s_class_article_ids.add(article_id.strip().lstrip("#"))
    finally:
        conn.close()
    return s_class_article_ids, s_class_slugs


def assert_input_sidecars_exist() -> None:
    missing = [str(p) for p in (REPORT_PATH, DB_PATH, REGISTRY_PATH, Path("thumbnails"), Path("note_drafts")) if not p.exists()]
    if missing:
        raise FileNotFoundError("Required input missing: " + ", ".join(missing))


def frame_number(path: str) -> int:
    match = FRAME_RE.search(Path(path).name)
    return int(match.group(1)) if match else -1


def choose_frames(block: ArticleBlock, per_article: int) -> list[str]:
    recommended = list(dict.fromkeys(block.recommended_frames or []))
    frames = list(dict.fromkeys(block.frame_paths or []))

    selected: list[str] = []
    for frame in recommended:
        if frame not in selected:
            selected.append(frame)
        if len(selected) >= per_article:
            return selected

    if frames:
        ordered = sorted(frames, key=frame_number)
        fallback = [ordered[0], ordered[len(ordered) // 2], ordered[-1]]
        for frame in fallback:
            if frame not in selected:
                selected.append(frame)
            if len(selected) >= per_article:
                return selected
    return selected[:per_article]


def best_neg(block: ArticleBlock) -> str:
    expressions = block.neg_expressions or []
    priority_words = [
        "強い輝点",
        "UAP候補",
        "小さな点",
        "対象物は確認困難",
        "明確に識別できません",
        "確認できませんでした",
    ]
    for word in priority_words:
        for expr in expressions:
            if word in expr:
                return expr
    return expressions[0] if expressions else ""


def infer_category(block: ArticleBlock, frame_path: str, known_miss: bool = False) -> str:
    if known_miss:
        return "E_known_miss_case"

    text = " ".join(block.neg_expressions or [])
    frame_no = frame_number(frame_path)
    if re.search(r"強い輝点|ハロー状|明確.*確認できます|対象が確認できます", text):
        return "A_clear_candidate"
    if re.search(r"小さな点|白い点|黒点|輝点|不鮮明|ドット状", text):
        return "B_small_unclear"
    if re.search(r"確認できませんでした|明確に識別できません|対象物は確認困難|確認困難|見えない", text):
        return "C_no_visible_target"
    if re.search(r"クロスヘア|マーカー|黒塗り|地形|建物|雲|海面|センサー|HUD|背景", text):
        return "D_sensor_ui_background"
    return "D_sensor_ui_background" if frame_no <= 0 else "B_small_unclear"


def copied_image_name(sample_id: str, source_frame_path: str) -> str:
    source = Path(source_frame_path)
    safe_parent = re.sub(r"[^A-Za-z0-9_.-]+", "_", source.parent.name)[:90]
    return f"{sample_id}_{safe_parent}_{source.name}"


def make_sample(
    index: int,
    block: ArticleBlock,
    frame_path: str,
    output_dir: Path,
    known_miss: bool = False,
) -> Sample:
    sample_id = f"vlm_{index:04d}"
    category = infer_category(block, frame_path, known_miss=known_miss)
    image_name = copied_image_name(sample_id, frame_path)
    notes = "known miss frame supplied by --known-miss-frame" if known_miss else "rule-based placeholder label; review manually"
    return Sample(
        sample_id=sample_id,
        category=category,
        article_id=block.article_id,
        h2_number=block.h2_number,
        slug=block.slug,
        source_frame_path=frame_path,
        copied_image_path=str(output_dir / "images" / image_name),
        draft_path=block.draft_path,
        neg_expression=best_neg(block),
        expected_human_label="TBD",
        notes=notes,
    )


def block_for_known_frame(blocks: list[ArticleBlock], frame_path: str) -> ArticleBlock:
    normalized = str(Path(frame_path))
    for block in blocks:
        all_frames = set((block.frame_paths or []) + (block.recommended_frames or []))
        if normalized in all_frames:
            return block

    parent_slug = Path(frame_path).parent.name
    draft_candidates = list(Path("note_drafts").glob(f"ai_summary_{parent_slug}*_note_version.md"))
    draft_path = str(draft_candidates[0]) if draft_candidates else ""
    return ArticleBlock(
        article_id="MANUAL",
        h2_number="MANUAL",
        slug=parent_slug,
        draft_path=draft_path,
        frame_paths=[normalized],
        recommended_frames=[normalized],
        neg_expressions=["manual known miss frame; label required"],
    )


def build_samples(
    blocks: list[ArticleBlock],
    max_samples: int,
    per_article: int,
    known_miss_frames: list[str],
    output_dir: Path,
) -> list[Sample]:
    s_class_article_ids, s_class_slugs = load_s_class_guards()
    samples: list[Sample] = []
    seen_frames: set[str] = set()

    for raw_frame in known_miss_frames:
        frame = str(Path(raw_frame))
        if not Path(frame).exists():
            raise FileNotFoundError(f"Known miss frame not found: {frame}")
        block = block_for_known_frame(blocks, frame)
        if block.article_id in s_class_article_ids or block.slug in s_class_slugs:
            continue
        samples.append(make_sample(len(samples) + 1, block, frame, output_dir, known_miss=True))
        seen_frames.add(frame)

    per_article_counts: dict[str, int] = defaultdict(int)
    for block in blocks:
        if len(samples) >= max_samples:
            break
        if block.article_id in s_class_article_ids or block.slug in s_class_slugs:
            continue
        for frame in choose_frames(block, per_article):
            if len(samples) >= max_samples:
                break
            if frame in seen_frames:
                continue
            if per_article_counts[block.article_id] >= per_article:
                break
            if not Path(frame).exists():
                continue
            samples.append(make_sample(len(samples) + 1, block, frame, output_dir))
            seen_frames.add(frame)
            per_article_counts[block.article_id] += 1

    return samples[:max_samples]


def write_manifest_csv(samples: list[Sample], path: Path) -> None:
    fields = [
        "sample_id",
        "category",
        "article_id",
        "h2_number",
        "slug",
        "source_frame_path",
        "copied_image_path",
        "draft_path",
        "neg_expression",
        "expected_human_label",
        "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for sample in samples:
            writer.writerow(asdict(sample))


def write_manifest_json(samples: list[Sample], path: Path) -> None:
    payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_report": str(REPORT_PATH),
        "sample_count": len(samples),
        "categories": CATEGORY_DESCRIPTIONS,
        "samples": [asdict(sample) for sample in samples],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def readme_text(samples: list[Sample]) -> str:
    counts = Counter(sample.category for sample in samples)
    prompt = (
        "この画像をUAP動画フレームとして観察してください。"
        "対象物候補が見えるか、位置、形状、明るさ、背景/センサーUIとの区別、"
        "不確実性を日本語で簡潔に答えてください。断定できない場合は断定しないでください。"
    )
    lines = [
        "# VLM Evaluation Set",
        "",
        "## Purpose",
        "",
        "Mac Studio上のローカルVLM候補を、同一のUAPフレーム画像セットで比較するための評価セットです。",
        "",
        "## Categories",
        "",
    ]
    for category, description in CATEGORY_DESCRIPTIONS.items():
        lines.append(f"- {category}: {description} ({counts.get(category, 0)} samples)")
    lines.extend(
        [
            "",
            "## Evaluation Method",
            "",
            "1. `manifest.csv` または `manifest.json` の順に `images/` 配下の画像をローカルVLMへ渡す。",
            "2. 各モデルの出力を sample_id 単位で保存する。",
            "3. 対象物の有無、位置説明、背景/UIとの区別、不確実性表現を比較する。",
            "4. `expected_human_label` は初期値 `TBD` のため、人間確認後に補正する。",
            "",
            "## Suggested Prompt",
            "",
            f"> {prompt}",
            "",
            "## Notes",
            "",
            "- このセットは rule-based placeholder ラベルで作成されており、正解ラベルではありません。",
            "- 元画像、note_drafts、workflow.db、source_registry.csv は変更していません。",
            "- S_CLASS レコードは除外対象です。",
            "- 外部API評価ではなく、ローカルVLM比較用です。",
            "",
            "## Human Label Correction",
            "",
            "`manifest.csv` の `expected_human_label` を `visible_candidate`, `small_unclear`, `not_visible`, `ui_background`, `known_miss` などに手動更新してください。補足は `notes` に追記します。",
            "",
        ]
    )
    return "\n".join(lines)


def execute_write(samples: list[Sample], output_dir: Path) -> None:
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    for sample in samples:
        shutil.copy2(sample.source_frame_path, sample.copied_image_path)
    write_manifest_csv(samples, output_dir / "manifest.csv")
    write_manifest_json(samples, output_dir / "manifest.json")
    (output_dir / "README.md").write_text(readme_text(samples), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local VLM evaluation sample set.")
    parser.add_argument("--max-samples", type=int, default=50)
    parser.add_argument("--per-article", type=int, default=3)
    parser.add_argument("--known-miss-frame", action="append", default=[])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_samples <= 0 or args.per_article <= 0:
        print("ERROR: --max-samples and --per-article must be positive.", file=sys.stderr)
        return 2

    assert_input_sidecars_exist()
    output_dir = OUTPUT_ROOT / datetime.now().strftime("%Y%m%d")
    blocks = parse_report(REPORT_PATH)
    samples = build_samples(
        blocks=blocks,
        max_samples=args.max_samples,
        per_article=args.per_article,
        known_miss_frames=args.known_miss_frame,
        output_dir=output_dir,
    )
    counts = Counter(sample.category for sample in samples)

    print(f"mode: {'execute' if args.execute else 'dry-run'}")
    print(f"source_report: {REPORT_PATH}")
    print(f"output_dir: {output_dir}")
    print(f"candidate_samples: {len(samples)}")
    print("category_counts:")
    for category in CATEGORY_DESCRIPTIONS:
        print(f"  {category}: {counts.get(category, 0)}")
    print(f"manifest_csv: {output_dir / 'manifest.csv'}")
    print(f"manifest_json: {output_dir / 'manifest.json'}")
    print(f"readme: {output_dir / 'README.md'}")
    if args.dry_run:
        print("dry_run: no files created and no images copied")
        return 0

    execute_write(samples, output_dir)
    print("execute: images copied and manifests written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
