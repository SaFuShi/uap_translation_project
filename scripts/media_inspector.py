#!/usr/bin/env python3
"""
media_inspector.py - Release video draft frame review candidate reporter.

Purpose:
  Reduce Claude token use by listing unpublished video drafts that should be
  checked with local frame/VLM tooling before human/Claude review.

Safety:
  - dry-run only
  - does not modify note_drafts, workflow.db, or source_registry.csv
  - does not publish notes or call external APIs
  - excludes S_CLASS records
"""

from __future__ import annotations

import argparse
import csv
import re
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_publish_package import MAPPING, find_draft, find_frames, find_thumbnail_dir

DB_PATH = Path("workflow.db")
REGISTRY_PATH = Path("review_logs/source_registry.csv")
REPORTS_DIR = Path("review_reports")

NEG_PATTERNS = [
    "確認できません",
    "明確に識別できません",
    "判別できません",
    "対象物は確認困難",
    "UAP対象物は確認できません",
    "直接確認できません",
]

EXCLUDED_STATUS_WORDS = {"hold", "skip", "published", "withdrawn_duplicate"}
FRAME_RE = re.compile(r"frame_(\d+)\.png$")


@dataclass
class DbInfo:
    status: str = ""
    classification: str = ""
    publish_blocked: int = 0
    publish_block_reason: str = ""
    note_url: str = ""
    pub_path: str = ""
    draft_path: str = ""
    article_id: str = ""


@dataclass
class RegistryInfo:
    status: str = ""
    note_url: str = ""
    published_path: str = ""
    draft_path: str = ""
    filename: str = ""
    remarks: str = ""


@dataclass
class NegLine:
    line_no: int
    pattern: str
    text: str


@dataclass
class Candidate:
    article_id: str
    h2_number: str
    publish_order: int
    glob_key: str
    slug: str
    draft_path: Path
    frames: list[Path]
    neg_lines: list[NegLine]
    db: DbInfo
    registry: RegistryInfo
    recommended_frames: list[Path] = field(default_factory=list)

    @property
    def has_neg(self) -> bool:
        return bool(self.neg_lines)

    @property
    def has_frames(self) -> bool:
        return bool(self.frames)


def normalize_article_id(value: str) -> str:
    return value.strip().lstrip("#")


def slug_from_draft(path: Path) -> str:
    return path.stem.removeprefix("ai_summary_").removesuffix("_note_version")


def load_registry(path: Path) -> dict[str, RegistryInfo]:
    if not path.exists():
        return {}

    rows: dict[str, RegistryInfo] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            article_id = normalize_article_id(row.get("article_id", ""))
            if not article_id:
                continue
            rows[article_id] = RegistryInfo(
                status=row.get("status", "").strip(),
                note_url=row.get("note_url", "").strip(),
                published_path=row.get("published_path", "").strip(),
                draft_path=row.get("draft_path", "").strip(),
                filename=row.get("pdf_file_name", "").strip(),
                remarks=row.get("remarks", "").strip(),
            )
    return rows


def load_db_rows(path: Path) -> list[sqlite3.Row]:
    if not path.exists():
        return []
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    try:
        return list(
            conn.execute(
                """
                SELECT slug, status, classification, publish_order,
                       publish_blocked, publish_block_reason,
                       note_url, pub_path, draft_path, article_id
                FROM articles
                """
            )
        )
    finally:
        conn.close()


def db_info_for(rows: list[sqlite3.Row], glob_key: str, article_id: str, publish_order: int) -> DbInfo:
    normalized = normalize_article_id(article_id)
    for row in rows:
        row_article_id = normalize_article_id(row["article_id"] or "")
        if (
            row["publish_order"] == publish_order
            or row_article_id == normalized
            or (row["slug"] or "").startswith(glob_key)
        ):
            return DbInfo(
                status=row["status"] or "",
                classification=row["classification"] or "",
                publish_blocked=row["publish_blocked"] or 0,
                publish_block_reason=row["publish_block_reason"] or "",
                note_url=row["note_url"] or "",
                pub_path=row["pub_path"] or "",
                draft_path=row["draft_path"] or "",
                article_id=row["article_id"] or "",
            )
    return DbInfo()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def is_vid_article(draft_text: str, registry: RegistryInfo) -> bool:
    filename = registry.filename.lower()
    if filename.endswith(".mp4") or filename.endswith(".mov"):
        return True
    if re.search(r"File Type：\*\*\s*VID", draft_text):
        return True
    return "動画" in draft_text[:1200] or "映像" in draft_text[:1200]


def is_excluded(db: DbInfo, registry: RegistryInfo, draft_text: str) -> tuple[bool, str]:
    db_status = db.status.lower()
    registry_status = registry.status.lower()
    combined = " ".join(
        [
            db_status,
            registry_status,
            db.publish_block_reason.lower(),
            registry.remarks.lower(),
        ]
    )

    if db.classification == "S_CLASS" or "classification: S_CLASS" in draft_text:
        return True, "S_CLASS"
    if db_status == "published" or registry_status == "published":
        return True, "published"
    if db.note_url or db.pub_path or registry.note_url or registry.published_path:
        return True, "published artifact present"
    if any(word in combined for word in EXCLUDED_STATUS_WORDS):
        return True, "HOLD/SKIP/published marker"
    if db.publish_blocked and re.search(r"\b(hold|skip)\b|HOLD|SKIP", db.publish_block_reason):
        return True, "blocked HOLD/SKIP"
    return False, ""


def find_neg_lines(text: str) -> list[NegLine]:
    found: list[NegLine] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pattern in NEG_PATTERNS:
            if pattern in line:
                found.append(NegLine(line_no=line_no, pattern=pattern, text=line.strip()))
    return found


def frame_number(path: Path) -> int:
    m = FRAME_RE.search(path.name)
    return int(m.group(1)) if m else -1


def choose_recommended_frames(frames: list[Path], limit: int = 5) -> list[Path]:
    if len(frames) <= limit:
        return frames
    picks = [frames[0], frames[len(frames) // 2], frames[-1]]
    for frame in sorted(frames, key=frame_number):
        if frame not in picks:
            picks.append(frame)
        if len(picks) >= limit:
            break
    return sorted(picks, key=frame_number)


def collect_candidates(release: str) -> tuple[list[Candidate], list[tuple[str, str, Path | None]]]:
    if release != "02":
        raise ValueError("Only Release 02 is supported by this PoC.")

    registry_rows = load_registry(REGISTRY_PATH)
    db_rows = load_db_rows(DB_PATH)
    candidates: list[Candidate] = []
    skipped: list[tuple[str, str, Path | None]] = []

    for glob_key, r02_num, publish_order in sorted(MAPPING, key=lambda item: item[2]):
        article_id = f"R02-{r02_num:03d}"
        draft = find_draft(glob_key)
        if draft is None:
            skipped.append((article_id, "draft missing", None))
            continue

        text = read_text(draft)
        registry = registry_rows.get(article_id, RegistryInfo())
        db = db_info_for(db_rows, glob_key, article_id, publish_order)

        excluded, reason = is_excluded(db, registry, text)
        if excluded:
            skipped.append((article_id, reason, draft))
            continue
        if not is_vid_article(text, registry):
            skipped.append((article_id, "not VID", draft))
            continue

        thumb_dir = find_thumbnail_dir(glob_key)
        frames = find_frames(thumb_dir) if thumb_dir else []
        neg_lines = find_neg_lines(text)
        candidates.append(
            Candidate(
                article_id=article_id,
                h2_number=f"#2_{r02_num:03d}",
                publish_order=publish_order,
                glob_key=glob_key,
                slug=slug_from_draft(draft),
                draft_path=draft,
                frames=frames,
                neg_lines=neg_lines,
                db=db,
                registry=registry,
                recommended_frames=choose_recommended_frames(frames),
            )
        )

    return candidates, skipped


def md_escape(text: str) -> str:
    return text.replace("\n", " ").strip()


def render_report(candidates: list[Candidate], skipped: list[tuple[str, str, Path | None]], vlm_cmd: str) -> str:
    neg_candidates = [c for c in candidates if c.has_neg]
    frame_candidates = [c for c in candidates if c.has_frames]
    frame_missing = [c for c in candidates if not c.has_frames]
    priority = sorted(candidates, key=lambda c: (not c.has_neg, not c.has_frames, c.publish_order))

    lines: list[str] = []
    lines.append("# Media Inspector Candidates")
    lines.append("")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("- Mode: dry-run")
    lines.append("- Release: 02")
    lines.append(f"- VLM command: `{vlm_cmd}`" if vlm_cmd else "- VLM command: not configured")
    lines.append("- VLM execution: not run")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Target articles: {len(candidates)}")
    lines.append(f"- Articles with NEG expressions: {len(neg_candidates)}")
    lines.append(f"- Articles with frames: {len(frame_candidates)}")
    lines.append(f"- Articles missing frames: {len(frame_missing)}")
    lines.append(f"- Skipped by guards/status: {len(skipped)}")
    lines.append("")

    lines.append("## Frame Missing Articles")
    lines.append("")
    if frame_missing:
        for c in frame_missing:
            lines.append(f"- {c.article_id} / {c.h2_number} / {c.slug} / {c.draft_path}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Priority Review Candidates")
    lines.append("")
    if not priority:
        lines.append("- None")
    for idx, c in enumerate(priority, start=1):
        lines.append(f"### {idx}. {c.article_id} / {c.h2_number} / {c.slug}")
        lines.append("")
        lines.append(f"- publish_order: {c.publish_order}")
        lines.append(f"- draft path: `{c.draft_path}`")
        lines.append(f"- frame count: {len(c.frames)}")
        lines.append("- frame paths:")
        if c.frames:
            for frame in c.frames:
                lines.append(f"  - `{frame}`")
        else:
            lines.append("  - None")
        lines.append("- NEG expression lines:")
        if c.neg_lines:
            for neg in c.neg_lines:
                lines.append(
                    f"  - L{neg.line_no} `{neg.pattern}`: {md_escape(neg.text)}"
                )
        else:
            lines.append("  - None")
        lines.append("- recommended review frames:")
        if c.recommended_frames:
            for frame in c.recommended_frames:
                lines.append(f"  - `{frame}`")
        else:
            lines.append("  - None")
        lines.append("")

    lines.append("## Skipped")
    lines.append("")
    if skipped:
        for article_id, reason, path in skipped:
            suffix = f" / {path}" if path else ""
            lines.append(f"- {article_id}: {reason}{suffix}")
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def write_report(markdown: str, output: Path | None) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = output or REPORTS_DIR / f"media_inspector_candidates_{datetime.now().strftime('%Y%m%d')}.md"
    path.write_text(markdown + "\n", encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List local media inspection candidates.")
    parser.add_argument("--release", default="02", help="Release number. PoC supports 02 only.")
    parser.add_argument("--dry-run", action="store_true", help="Required; no image analysis is run.")
    parser.add_argument("--vlm-cmd", default="", help="Future local VLM command template; not executed in dry-run.")
    parser.add_argument("--output", type=Path, help="Optional markdown report path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.dry_run:
        print("ERROR: This PoC is dry-run only. Re-run with --dry-run.", file=sys.stderr)
        return 2

    release = args.release.zfill(2)
    candidates, skipped = collect_candidates(release)
    report = render_report(candidates, skipped, args.vlm_cmd)
    report_path = write_report(report, args.output)

    print(f"mode: dry-run")
    print(f"release: {release}")
    print(f"target_articles: {len(candidates)}")
    print(f"neg_articles: {sum(1 for c in candidates if c.has_neg)}")
    print(f"frame_articles: {sum(1 for c in candidates if c.has_frames)}")
    print(f"frame_missing_articles: {sum(1 for c in candidates if not c.has_frames)}")
    print(f"report: {report_path}")
    if args.vlm_cmd:
        print("vlm: configured but not executed in dry-run")
    else:
        print("vlm: not configured")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
