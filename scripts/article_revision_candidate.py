#!/usr/bin/env python3
"""
article_revision_candidate.py

Compare VLM / human-ground-truth against note_drafts and surface
text passages that may conflict with visual evidence.

Output
──────
  review_reports/article_revision_candidates_<date>.md
  <run_dir>/article_revision_candidates.csv

Safety
──────
  - Read-only on note_drafts, workflow.db, source_registry, manifest.
  - Writes only to --output and --csv paths.
  - Never auto-modifies article text.
  - No external API calls.
  - S_CLASS guard via ground_truth / manifest category exclusion.
"""

from __future__ import annotations

import argparse
import csv
import re
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

# ── NEG pattern definitions ────────────────────────────────────────────────────

# Patterns that specifically indicate the UAP object is not visible
UAP_OBJECT_NEG_PATTERNS = [
    "対象物は確認困難",
    "UAP対象物は確認できません",
    "映像からは確認できません",
    "直接確認できません",
    "判別できません",
]

# Patterns that appear in "secondary" context (sensor type, identity, etc.)
# These are lower-risk — they say we can't confirm sensor type or object identity,
# not that the object is absent.
SECONDARY_NEG_PATTERNS = [
    "確認できません",   # broad — needs context analysis
]

# Context words that indicate the NEG is about a secondary aspect (lower risk)
SECONDARY_CONTEXT_WORDS = [
    "IRセンサー", "センサー種別", "センサーと推定", "カメラと推定",
    "正体", "種別", "性質", "撮影状況", "乗員", "機材", "プラットフォーム",
    "コールサイン", "確認できません）", "推定されるが確認できません",
]

# Context words that indicate the NEG is about UAP object visibility (higher risk)
UAP_OBJECT_CONTEXT_WORDS = [
    "対象物", "対象が", "対象は", "UAPとされる", "不明物体",
    "飛行物体", "発光体", "輝点", "光体", "物体", "対象候補",
]

CONF_THRESHOLD = 0.6

COMPARISON_LABELS_INCLUDE = {
    "Partial Match",
    "Description Gap",
    "Missed Secondary Objects",
    "False Negative",
    "Label Error",
}

RISK_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "SKIP": 3}


# ── Data structures ────────────────────────────────────────────────────────────

@dataclass
class NegHit:
    line_no: int
    pattern: str
    line_text: str
    is_secondary: bool


@dataclass
class Candidate:
    sample_id: str
    article_id: str
    h2_number: str
    category: str
    frame_path: str
    draft_path: str
    vlm_visible: bool | None
    vlm_confidence: float | None
    vlm_location: str
    vlm_description: str
    human_visible: bool | None
    human_confidence: float | None
    human_verdict: str
    comparison_label: str
    neg_hits: list[NegHit]
    revision_suggestion: str
    risk_level: str          # HIGH / MEDIUM / LOW / SKIP
    human_review_required: bool
    next_action: str
    notes: str


# ── Loaders ───────────────────────────────────────────────────────────────────

def load_csv(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sid = row.get("sample_id", "").strip()
            if sid:
                rows[sid] = row
    return rows


def parse_bool(v: str | None) -> bool | None:
    if v is None:
        return None
    s = str(v).strip().lower()
    if s in ("true", "1", "yes"):
        return True
    if s in ("false", "0", "no"):
        return False
    return None


def parse_float(v: str | None) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ── NEG analysis ──────────────────────────────────────────────────────────────

def classify_neg_hit(line: str, pattern: str) -> bool:
    """Return True if the NEG hit is about a secondary aspect (lower risk)."""
    return any(w in line for w in SECONDARY_CONTEXT_WORDS)


def find_neg_hits(draft_text: str) -> list[NegHit]:
    hits: list[NegHit] = []
    seen_lines: set[int] = set()
    lines = draft_text.splitlines()

    all_patterns = UAP_OBJECT_NEG_PATTERNS + SECONDARY_NEG_PATTERNS
    for line_no, line in enumerate(lines, start=1):
        for pattern in all_patterns:
            if pattern in line and line_no not in seen_lines:
                is_secondary = classify_neg_hit(line, pattern)
                hits.append(NegHit(
                    line_no=line_no,
                    pattern=pattern,
                    line_text=line.strip()[:200],
                    is_secondary=is_secondary,
                ))
                seen_lines.add(line_no)
                break
    return hits


def has_uap_object_neg(hits: list[NegHit]) -> bool:
    """True if any NEG hit is specifically about UAP object visibility."""
    for h in hits:
        if not h.is_secondary:
            return True
        # broad "確認できません" with UAP object context = also counts
        if any(w in h.line_text for w in UAP_OBJECT_CONTEXT_WORDS):
            return True
    return False


# ── Revision suggestion generator ─────────────────────────────────────────────

def generate_suggestion(
    vlm_visible: bool | None,
    vlm_location: str,
    vlm_description: str,
    human_visible: bool | None,
    human_verdict: str,
    category: str,
    neg_hits: list[NegHit],
) -> str:
    """Generate a cautious revision suggestion in Japanese."""

    # Determine the primary evidence source
    if human_visible is True and human_verdict == "label_error":
        # Human confirmed object is visible
        loc = vlm_location or "画面内"
        desc = vlm_description or "対象が確認できます"
        return (
            f"【修正候補】{loc}付近に対象候補が確認できます。"
            "ただし、単一または少数フレームの目視確認であり、"
            "対象の性質・移動・正体を断定することはできません。"
            "追加フレームおよび専門的分析が必要です。"
        )
    elif human_visible is False and human_verdict == "false_positive":
        # Human confirmed VLM is wrong — no revision needed
        return "（VLM誤検出確定のため修正不要）"
    elif vlm_visible is True and human_visible is None:
        # VLM-only evidence
        loc = vlm_location or "画面内"
        desc = vlm_description or "対象候補"
        return (
            f"【修正候補（VLMのみ）】{loc}付近に{desc}が確認される可能性があります。"
            "ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、"
            "人間による目視確認が必要です。断定的な記述は避けてください。"
        )
    else:
        return "（修正候補なし）"


# ── Risk assessment ───────────────────────────────────────────────────────────

def assess_risk(
    vlm_visible: bool | None,
    vlm_conf: float | None,
    human_visible: bool | None,
    human_verdict: str,
    comparison_label: str,
    neg_hits: list[NegHit],
) -> tuple[str, bool, str]:
    """Return (risk_level, human_review_required, next_action)."""

    uap_neg = has_uap_object_neg(neg_hits)

    # SKIP: VLM wrong per human GT
    if human_verdict == "false_positive":
        return ("SKIP", False,
                "VLM誤検出確定。記事修正不要。評価セットのカテゴリラベルは正しい。")

    # HIGH: human confirmed visible + article has UAP object NEG
    if human_visible is True and human_verdict == "label_error" and uap_neg:
        return ("HIGH", True,
                "人間目視確認済み。記事内NEG表現と矛盾。"
                "note_draftのNEG表現を人間が確認し、必要に応じて慎重表現で修正。")

    # HIGH: human confirmed visible + article conflict (even without UAP-specific NEG)
    if human_visible is True and human_verdict == "label_error":
        return ("HIGH", True,
                "人間目視確認済み（label_error）。記事との整合性を確認。"
                "NEG表現の文脈を精査し、対象物の記述精度を検討。")

    # MEDIUM: VLM visible + UAP object NEG in draft (no human GT)
    if vlm_visible is True and (vlm_conf or 0) >= CONF_THRESHOLD and uap_neg:
        return ("MEDIUM", True,
                "VLM検出あり + 記事にUAP対象NEG表現。"
                "人間目視確認後、矛盾があれば慎重表現で修正候補を検討。")

    # MEDIUM: comparison_label indicates quality issue
    if comparison_label and any(lbl in comparison_label for lbl in COMPARISON_LABELS_INCLUDE):
        return ("MEDIUM", True,
                "comparison_labelが品質課題を示す。人間目視確認を推奨。")

    # LOW: VLM visible + NEG is secondary only
    if vlm_visible is True and (vlm_conf or 0) >= CONF_THRESHOLD and neg_hits:
        return ("LOW", False,
                "VLM検出あり。NEG表現は二次的側面（センサー種別・正体等）のみ。"
                "記事本文の矛盾は限定的。参考情報として記録。")

    # LOW: VLM visible + no NEG in draft
    if vlm_visible is True and (vlm_conf or 0) >= CONF_THRESHOLD:
        return ("LOW", False,
                "VLM検出あり。記事内にNEG表現なし。矛盾なし。参考情報として記録。")

    return ("SKIP", False, "条件に合致しない。スキップ。")


# ── Main logic ────────────────────────────────────────────────────────────────

def build_candidates(
    results: dict[str, dict],
    ground_truth: dict[str, dict],
    manifest: dict[str, dict],
    drafts_dir: Path,
) -> list[Candidate]:

    candidates: list[Candidate] = []
    draft_cache: dict[str, str] = {}

    # Group manifest by sample_id
    for sid, res in results.items():
        vlm_visible = parse_bool(res.get("visible_candidate"))
        vlm_conf    = parse_float(res.get("confidence"))
        parse_ok    = parse_bool(res.get("parse_success"))

        # Only process visible=true, conf>=threshold, parse success
        if vlm_visible is not True:
            continue
        if (vlm_conf or 0) < CONF_THRESHOLD:
            continue
        if not parse_ok:
            continue

        # Get manifest entry
        mf = manifest.get(sid, {})
        draft_path = mf.get("draft_path", "").strip()
        article_id = res.get("article_id", mf.get("article_id", ""))
        h2_number  = res.get("h2_number", mf.get("h2_number", ""))
        category   = res.get("category", mf.get("category", ""))
        frame_path = res.get("image_path", mf.get("copied_image_path", ""))

        # Get ground truth if available
        gt = ground_truth.get(sid, {})
        human_visible  = parse_bool(gt.get("human_visible_candidate"))
        human_conf     = parse_float(gt.get("human_confidence"))
        human_verdict  = gt.get("human_verdict", "")
        comparison_label = gt.get("comparison_label", "")

        # Skip if human confirmed VLM is wrong
        if human_verdict == "false_positive":
            # Still record as SKIP
            pass

        # Load draft text
        draft_text = ""
        if draft_path and draft_path not in draft_cache:
            p = Path(draft_path)
            if p.exists():
                draft_cache[draft_path] = p.read_text(encoding="utf-8")
            else:
                draft_cache[draft_path] = ""
        draft_text = draft_cache.get(draft_path, "")

        # Find NEG hits
        neg_hits = find_neg_hits(draft_text) if draft_text else []

        # Risk assessment
        risk_level, review_required, next_action = assess_risk(
            vlm_visible=vlm_visible,
            vlm_conf=vlm_conf,
            human_visible=human_visible,
            human_verdict=human_verdict,
            comparison_label=comparison_label,
            neg_hits=neg_hits,
        )

        # Skip truly irrelevant entries
        if risk_level == "SKIP" and human_verdict not in ("false_positive",):
            continue
        if risk_level == "SKIP" and human_verdict == "false_positive":
            # Record false_positive as SKIP for completeness
            pass

        # Generate revision suggestion
        suggestion = generate_suggestion(
            vlm_visible=vlm_visible,
            vlm_location=res.get("location", ""),
            vlm_description=res.get("description", ""),
            human_visible=human_visible,
            human_verdict=human_verdict,
            category=category,
            neg_hits=neg_hits,
        )

        notes_parts = []
        if not draft_path:
            notes_parts.append("draft_path not in manifest")
        if not draft_text:
            notes_parts.append("draft file not found or empty")
        if not neg_hits:
            notes_parts.append("no NEG patterns found in draft")

        candidates.append(Candidate(
            sample_id=sid,
            article_id=article_id,
            h2_number=h2_number,
            category=category,
            frame_path=str(frame_path),
            draft_path=draft_path,
            vlm_visible=vlm_visible,
            vlm_confidence=vlm_conf,
            vlm_location=res.get("location", ""),
            vlm_description=res.get("description", ""),
            human_visible=human_visible,
            human_confidence=human_conf,
            human_verdict=human_verdict,
            comparison_label=comparison_label,
            neg_hits=neg_hits,
            revision_suggestion=suggestion,
            risk_level=risk_level,
            human_review_required=review_required,
            next_action=next_action,
            notes="; ".join(notes_parts),
        ))

    # Sort: HIGH first, then MEDIUM, LOW, SKIP; within tier by article_id
    candidates.sort(key=lambda c: (RISK_ORDER.get(c.risk_level, 9), c.article_id, c.sample_id))
    return candidates


# ── Output writers ────────────────────────────────────────────────────────────

CSV_FIELDS = [
    "sample_id", "article_id", "h2_number", "category",
    "frame_path", "draft_path",
    "vlm_visible", "vlm_confidence", "vlm_location", "vlm_description",
    "human_visible", "human_confidence", "human_verdict", "comparison_label",
    "neg_hit_count", "has_uap_object_neg",
    "revision_suggestion", "risk_level", "human_review_required", "next_action", "notes",
]


def write_csv(candidates: list[Candidate], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for c in candidates:
            writer.writerow({
                "sample_id": c.sample_id,
                "article_id": c.article_id,
                "h2_number": c.h2_number,
                "category": c.category,
                "frame_path": c.frame_path,
                "draft_path": c.draft_path,
                "vlm_visible": c.vlm_visible,
                "vlm_confidence": c.vlm_confidence,
                "vlm_location": c.vlm_location,
                "vlm_description": c.vlm_description,
                "human_visible": c.human_visible,
                "human_confidence": c.human_confidence,
                "human_verdict": c.human_verdict,
                "comparison_label": c.comparison_label,
                "neg_hit_count": len(c.neg_hits),
                "has_uap_object_neg": has_uap_object_neg(c.neg_hits),
                "revision_suggestion": c.revision_suggestion,
                "risk_level": c.risk_level,
                "human_review_required": c.human_review_required,
                "next_action": c.next_action,
                "notes": c.notes,
            })


def _md_escape(s: str) -> str:
    return s.replace("|", "｜").replace("\n", " ").strip()


def write_md(candidates: list[Candidate], output: Path, model: str, run_id: str,
             gt_path: Path, results_path: Path) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    by_risk: dict[str, list[Candidate]] = defaultdict(list)
    for c in candidates:
        by_risk[c.risk_level].append(c)

    high_count   = len(by_risk.get("HIGH", []))
    medium_count = len(by_risk.get("MEDIUM", []))
    low_count    = len(by_risk.get("LOW", []))
    skip_count   = len(by_risk.get("SKIP", []))

    lines: list[str] = [
        "# Article Revision Candidates",
        "",
        f"- 生成日時: {now}",
        f"- モデル: `{model}`",
        f"- run_id: `{run_id}`",
        f"- ground_truth: `{gt_path}`",
        f"- results: `{results_path}`",
        "",
        "> **注意**: このレポートは記事修正を自動実行しません。",
        "> 人間・Claudeが確認し、必要な場合にのみ note_drafts を手動修正してください。",
        "",
        "---",
        "",
        "## サマリー",
        "",
        f"| risk_level | 件数 |",
        f"|------------|------|",
        f"| HIGH | {high_count} |",
        f"| MEDIUM | {medium_count} |",
        f"| LOW | {low_count} |",
        f"| SKIP（VLM誤検出確定等） | {skip_count} |",
        f"| **合計** | **{len(candidates)}** |",
        "",
        "### risk_level の定義",
        "",
        "| level | 条件 |",
        "|-------|------|",
        "| HIGH | 人間目視確認済み（label_error）かつ記事と矛盾 |",
        "| MEDIUM | VLM検出あり + 記事にUAP対象NEG表現、または comparison_label に品質課題 |",
        "| LOW | VLM検出あり。NEG表現は二次的側面のみ、または NEG なし |",
        "| SKIP | VLM誤検出確定（false_positive）または条件非該当 |",
        "",
        "---",
    ]

    for risk in ("HIGH", "MEDIUM", "LOW", "SKIP"):
        group = by_risk.get(risk, [])
        if not group:
            continue
        lines += [
            "",
            f"## {risk} — {len(group)}件",
            "",
        ]
        for c in group:
            lines += [
                f"### {c.sample_id} | {c.article_id} | {c.h2_number}",
                "",
                f"- **category**: {c.category}",
                f"- **frame**: `{c.frame_path}`",
                f"- **draft**: `{c.draft_path}`",
                "",
                "**VLM判定:**",
                "",
                f"- visible: {c.vlm_visible} / confidence: {c.vlm_confidence}",
                f"- location: {c.vlm_location}",
                f"- description: {c.vlm_description}",
                "",
            ]
            if c.human_visible is not None:
                lines += [
                    "**人間判定（ground truth）:**",
                    "",
                    f"- visible: {c.human_visible} / confidence: {c.human_confidence}",
                    f"- human_verdict: {c.human_verdict}",
                    f"- comparison_label: {c.comparison_label}",
                    "",
                ]
            if c.neg_hits:
                lines += ["**記事内 NEG 表現:**", ""]
                for h in c.neg_hits[:5]:
                    secondary_tag = "〔二次的〕" if h.is_secondary else "〔対象候補〕"
                    lines.append(
                        f"- L{h.line_no} {secondary_tag} `{h.pattern}` : "
                        f"{_md_escape(h.line_text[:120])}"
                    )
                if len(c.neg_hits) > 5:
                    lines.append(f"- … 他 {len(c.neg_hits)-5} 件")
                lines.append("")
            else:
                lines += ["**記事内 NEG 表現:** なし", ""]

            lines += [
                "**修正候補文:**",
                "",
                f"> {c.revision_suggestion}",
                "",
                f"- **risk_level**: {c.risk_level}",
                f"- **human_review_required**: {c.human_review_required}",
                f"- **next_action**: {c.next_action}",
            ]
            if c.notes:
                lines.append(f"- **notes**: {c.notes}")
            lines.append("")

    lines += [
        "---",
        "",
        "## 修正手順（human_review_required=true の場合）",
        "",
        "1. `frame_path` の画像を目視確認",
        "2. `draft` の該当行を確認",
        "3. VLM・人間判定と記事記述が矛盾している場合、`修正候補文` を参考に慎重表現で修正",
        "4. 修正後に `ground_truth.csv` の `notes` に修正内容を記録",
        "5. 記事公開フロー（publish workflow）は別途実施",
        "",
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate article revision candidates from VLM results.")
    p.add_argument("--results",      type=Path, required=True, help="VLM results CSV")
    p.add_argument("--ground-truth", type=Path, required=True, help="Human ground truth CSV")
    p.add_argument("--manifest",     type=Path, required=True, help="Eval set manifest CSV")
    p.add_argument("--drafts-dir",   type=Path, default=Path("note_drafts"))
    p.add_argument("--model",        type=str,  default="qwen2.5-vl-7b-instruct")
    p.add_argument("--run-id",       type=str,  default="")
    p.add_argument("--output",       type=Path, required=True, help="Markdown report output path")
    p.add_argument("--csv",          type=Path, default=None,  help="CSV output path")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    for path, label in [
        (args.results,      "--results"),
        (args.ground_truth, "--ground-truth"),
        (args.manifest,     "--manifest"),
    ]:
        if not path.exists():
            print(f"ERROR: {label} not found: {path}")
            return 1

    csv_out = args.csv or (args.results.parent / "article_revision_candidates.csv")
    run_id  = args.run_id or args.results.parent.name

    print(f"Loading results      : {args.results}")
    results = load_csv(args.results)
    print(f"  → {len(results)} samples")

    print(f"Loading ground truth : {args.ground_truth}")
    ground_truth = load_csv(args.ground_truth)
    print(f"  → {len(ground_truth)} samples")

    print(f"Loading manifest     : {args.manifest}")
    manifest = load_csv(args.manifest)
    print(f"  → {len(manifest)} samples")

    print("Building candidates ...")
    candidates = build_candidates(results, ground_truth, manifest, args.drafts_dir)

    by_risk: dict[str, list] = defaultdict(list)
    for c in candidates:
        by_risk[c.risk_level].append(c)

    print(f"  HIGH   : {len(by_risk.get('HIGH', []))}")
    print(f"  MEDIUM : {len(by_risk.get('MEDIUM', []))}")
    print(f"  LOW    : {len(by_risk.get('LOW', []))}")
    print(f"  SKIP   : {len(by_risk.get('SKIP', []))}")
    print(f"  total  : {len(candidates)}")

    print(f"Writing CSV     : {csv_out}")
    write_csv(candidates, csv_out)

    print(f"Writing Markdown: {args.output}")
    write_md(candidates, args.output,
             model=args.model, run_id=run_id,
             gt_path=args.ground_truth, results_path=args.results)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
