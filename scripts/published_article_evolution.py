#!/usr/bin/env python3
"""
Published Article Evolution Agent v1

公開済み記事の修正・改善候補を自動分類する。

Decision:
  Immediate Fix    - 記事に明確な記述欠落。即時修正推奨。
  Detailed Edition - 詳細解析版で反映する知見。
  No Change        - 修正不要。記事本文は妥当。

判定ルール:
  R1: human_verdict=false_positive → No Change
  R2: Missed Secondary Objects + confidence≥0.8 + 記事未記載 → Immediate Fix
  R3: label_error + Description Gap + confidence<0.8 → No Change
  R4: label_error + Match (複数フレーム一致) → Detailed Edition
  R5: label_error + Partial Match + confidence<0.8 → Detailed Edition
  R6: label_error + confidence≥0.8 + 記述欠落 → Immediate Fix
  R7: GT未確認 + risk_level=MEDIUM → Detailed Edition
  R8: GT未確認 + risk_level=SKIP → No Change
"""

import argparse
import csv
import os
import re
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


# ─────────────────────────────────────────────────────────────────
# Data class
# ─────────────────────────────────────────────────────────────────

@dataclass
class EvolutionRecord:
    article_id: str
    h2_number: str
    sample_ids: str
    published_date: str
    published_url: str
    evolution_status: str        # pending / no_change / confirmed / done
    decision: str                # Immediate Fix / Detailed Edition / No Change
    priority: str                # High / Medium / Low
    human_review_required: str   # true / false
    human_review_done: str       # true / false
    human_review_date: str
    vlm_visible: str
    human_visible: str
    human_confidence: str
    comparison_label: str
    has_uap_object_neg: str
    risk_level: str
    modification_target_section: str
    modification_draft: str
    next_action: str
    notes: str


# ─────────────────────────────────────────────────────────────────
# Loaders
# ─────────────────────────────────────────────────────────────────

def load_candidates(path: str) -> dict[str, list[dict]]:
    """article_id → list of candidate rows (sorted by sample_id)"""
    result: dict[str, list[dict]] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            result.setdefault(row["article_id"], []).append(row)
    return result


def load_ground_truth(path: str) -> dict[str, dict]:
    """sample_id → GT row"""
    result: dict[str, dict] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            result[row["sample_id"]] = row
    return result


def load_source_registry(path: str) -> dict[str, dict]:
    """article_id → registry row (published only, '#' prefix stripped)"""
    result: dict[str, dict] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            aid = row["article_id"].lstrip("#")
            if row.get("status") == "published":
                result[aid] = row
    return result


def load_article_text(published_path: str) -> str:
    if published_path and os.path.exists(published_path):
        return Path(published_path).read_text(encoding="utf-8")
    return ""


# ─────────────────────────────────────────────────────────────────
# Article description checks
# ─────────────────────────────────────────────────────────────────

def _extract_chunks(text: str, min_len: int = 2) -> list[str]:
    """Japanese/ASCII word chunks of min_len or more chars."""
    return re.findall(r"[぀-ゟ゠-ヿ一-鿿ｦ-ﾟa-zA-Z]{%d,}" % min_len, text)


def article_has_secondary_description(article_text: str, human_objects: str) -> bool:
    """
    「Missed Secondary Objects」ケースで副次対象物が記事に記述済みか確認する。
    human_objects の「・」「+」区切りで2番目以降を副次対象物とみなす。
    副次対象物のキーワード2個以上が記事テキストに存在すれば True。
    """
    if not article_text or not human_objects:
        return False
    parts = re.split(r"[・+]", human_objects)
    if len(parts) < 2:
        return False
    first_secondary = parts[1].strip()
    chunks = _extract_chunks(first_secondary, min_len=2)
    if not chunks:
        return False
    matches = sum(1 for c in chunks if c in article_text)
    return matches >= min(2, len(chunks))


def article_has_positive_description(article_text: str, human_objects: str) -> bool:
    """
    記事本文に主対象物についての肯定的な記述が存在するか確認する。
    主対象物（parts[0]）のキーワードが記事内に存在し、
    かつ肯定表現が1つ以上あれば True。
    """
    if not article_text or not human_objects:
        return False
    primary = re.split(r"[・+]", human_objects)[0].strip()
    chunks = _extract_chunks(primary, min_len=2)
    if not chunks:
        return False
    positive_patterns = ["確認できます", "確認できる", "視認できる", "確認されました", "明確に"]
    has_keywords = any(c in article_text for c in chunks)
    has_positive = any(p in article_text for p in positive_patterns)
    return has_keywords and has_positive


# ─────────────────────────────────────────────────────────────────
# Single GT record classification
# ─────────────────────────────────────────────────────────────────

def classify_single_gt(gt: dict, article_text: str) -> str:
    """
    1件のGTレコードを判定。
    Returns: 'immediate_fix' / 'detailed' / 'no_change'
    """
    verdict = gt.get("human_verdict", "")
    comparison_label = gt.get("comparison_label", "")
    human_objects = gt.get("human_objects", "")
    confidence = float(gt.get("human_confidence", 0) or 0)

    # R1: false_positive
    if verdict == "false_positive":
        return "no_change"

    if verdict == "label_error":
        # R2: Missed Secondary Objects + high confidence
        if "Missed Secondary Objects" in comparison_label and confidence >= 0.8:
            has_sec = article_has_secondary_description(article_text, human_objects)
            return "no_change" if has_sec else "immediate_fix"

        # R3: Description Gap + low confidence
        if "Description Gap" in comparison_label and confidence < 0.8:
            return "no_change"

        # R4: Match (no Missed Secondary)
        if "Match" in comparison_label and "Missed Secondary Objects" not in comparison_label:
            return "detailed"

        # R5: low confidence (Partial Match etc.)
        if confidence < 0.8:
            return "detailed"

        # R6: high confidence, check article
        has_pos = article_has_positive_description(article_text, human_objects)
        return "no_change" if has_pos else "immediate_fix"

    return "detailed"


# ─────────────────────────────────────────────────────────────────
# Article-level decision
# ─────────────────────────────────────────────────────────────────

def decide_evolution(
    candidates: list[dict],
    gt_map: dict[str, dict],
    article_text: str,
) -> tuple[str, str, bool, str, str, str, str, str, str]:
    """
    Returns:
      decision, priority, human_review_required,
      next_action, notes, evolution_status,
      mod_section, mod_draft, agg_comparison_label
    """
    # GT records available for this article
    gt_records = [gt_map[c["sample_id"]] for c in candidates if c["sample_id"] in gt_map]

    # Per-GT classification
    if gt_records:
        single_decisions = [classify_single_gt(g, article_text) for g in gt_records]

        # Aggregate comparison labels
        agg_comparison = " | ".join(sorted({g.get("comparison_label", "") for g in gt_records if g.get("comparison_label")}))

        # Aggregate human objects (from Missed Secondary Objects records)
        missed_gts = [g for g in gt_records if "Missed Secondary Objects" in g.get("comparison_label", "")]
        agg_human_objects = "、".join(g.get("human_objects", "") for g in missed_gts if g.get("human_objects"))

        max_confidence = max(float(g.get("human_confidence", 0) or 0) for g in gt_records)

        # Immediate Fix wins if any single decision is immediate_fix
        if "immediate_fix" in single_decisions:
            idx = single_decisions.index("immediate_fix")
            gt_if = gt_records[idx]
            return (
                "Immediate Fix", "High", True,
                "副次対象物の記述欠落が確認済み。"
                f"人間目視確認済み（信頼度 {max_confidence:.0%}）。"
                "note_draft修正後、note.comで記事を更新・再公開。",
                "Missed Secondary Objects / 記述欠落確定。",
                "pending",
                "視覚情報セクション 該当フレーム",
                agg_human_objects,
                agg_comparison,
            )

        # All no_change
        if all(d == "no_change" for d in single_decisions):
            return (
                "No Change", "Low", False,
                "評価セット・人間GT・記事本文を突合した結果、修正不要。",
                "label_error(評価セット誤り)またはFalse Positive確定。記事は正確。",
                "no_change", "", "", agg_comparison,
            )

        # Mix or all detailed
        return (
            "Detailed Edition", "Medium", False,
            "評価セットラベル誤りまたはカバレッジ補完候補。詳細解析版で反映推奨。",
            "Partial Match / Match等。記事は概ね正確だが補完候補あり。",
            "pending", "注意点セクション（時刻・カバレッジ補完）", "", agg_comparison,
        )

    # No GT: fall back to risk_level
    risk_levels = [c["risk_level"] for c in candidates]
    agg_risk = (
        "HIGH" if "HIGH" in risk_levels else
        "MEDIUM" if "MEDIUM" in risk_levels else
        "LOW" if "LOW" in risk_levels else "SKIP"
    )

    if agg_risk == "SKIP":
        return (
            "No Change", "Low", False,
            "SKIP候補（人間GT未確認）。修正不要。",
            "SKIP。GT未確認。", "no_change", "", "", "",
        )
    if agg_risk == "MEDIUM":
        return (
            "Detailed Edition", "Low", False,
            "MEDIUM候補（人間GT未確認）。詳細解析版で確認推奨。",
            "MEDIUM。GT未確認。", "pending", "", "", "",
        )
    # HIGH without GT
    return (
        "Detailed Edition", "Medium", True,
        "HIGH候補（人間GT未確認）。元映像の人間確認推奨。詳細解析版で反映。",
        "HIGH。GT未確認。", "pending", "", "", "",
    )


# ─────────────────────────────────────────────────────────────────
# Record builder
# ─────────────────────────────────────────────────────────────────

def build_records(
    candidates_by_article: dict[str, list[dict]],
    gt_map: dict[str, dict],
    registry: dict[str, dict],
) -> list[EvolutionRecord]:
    records: list[EvolutionRecord] = []

    for article_id, cands in sorted(candidates_by_article.items()):
        reg = registry.get(article_id)
        if not reg:
            continue  # 未公開記事はスキップ

        published_path = reg.get("published_path", "")
        article_text = load_article_text(published_path)
        published_date = reg.get("published_date", "")
        published_url = reg.get("note_url", "")
        h2_number = cands[0]["h2_number"]
        sample_ids_str = ",".join(c["sample_id"] for c in cands)

        # Aggregate risk_level
        risk_levels = [c["risk_level"] for c in cands]
        agg_risk = (
            "HIGH" if "HIGH" in risk_levels else
            "MEDIUM" if "MEDIUM" in risk_levels else
            "LOW" if "LOW" in risk_levels else "SKIP"
        )

        # has_uap_object_neg aggregate
        has_neg = any(c.get("has_uap_object_neg", "False").lower() == "true" for c in cands)

        # GT aggregate for display
        gt_records = [gt_map[c["sample_id"]] for c in cands if c["sample_id"] in gt_map]
        max_confidence = (
            max(float(g.get("human_confidence", 0) or 0) for g in gt_records)
            if gt_records else 0.0
        )
        human_visible_vals = [g.get("human_visible_candidate", "").lower() for g in gt_records]
        vlm_visible_vals = [g.get("vlm_visible_candidate", "").lower() for g in gt_records]
        agg_human_visible = (
            "true" if any(v == "true" for v in human_visible_vals) else
            "false" if human_visible_vals else ""
        )
        agg_vlm_visible = (
            "true" if any(v == "true" for v in vlm_visible_vals) else
            cands[0].get("vlm_visible", "")
        )

        (decision, priority, human_review_required,
         next_action, notes, evolution_status,
         mod_section, mod_draft, agg_comparison) = decide_evolution(cands, gt_map, article_text)

        records.append(EvolutionRecord(
            article_id=article_id,
            h2_number=h2_number,
            sample_ids=sample_ids_str,
            published_date=published_date,
            published_url=published_url,
            evolution_status=evolution_status,
            decision=decision,
            priority=priority,
            human_review_required="true" if human_review_required else "false",
            human_review_done="false",
            human_review_date="",
            vlm_visible=agg_vlm_visible,
            human_visible=agg_human_visible,
            human_confidence=f"{max_confidence:.2f}" if max_confidence else "",
            comparison_label=agg_comparison,
            has_uap_object_neg="true" if has_neg else "false",
            risk_level=agg_risk,
            modification_target_section=mod_section,
            modification_draft=mod_draft,
            next_action=next_action,
            notes=notes,
        ))

    return records


# ─────────────────────────────────────────────────────────────────
# Writers
# ─────────────────────────────────────────────────────────────────

def write_csv(records: list[EvolutionRecord], path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fields = list(EvolutionRecord.__dataclass_fields__.keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in records:
            w.writerow(asdict(r))


def write_report(records: list[EvolutionRecord], model: str, run_id: str, path: str) -> None:
    today = date.today().isoformat()
    immediate = [r for r in records if r.decision == "Immediate Fix"]
    detailed = [r for r in records if r.decision == "Detailed Edition"]
    no_change = [r for r in records if r.decision == "No Change"]

    lines: list[str] = [
        "# Published Article Evolution Report",
        "",
        f"- 実施日: {today}",
        f"- モデル: `{model}`",
        f"- run_id: `{run_id}`",
        f"- 対象公開記事数: {len(records)} 件",
        "",
        "---",
        "",
        "## サマリー",
        "",
        "| decision | 件数 | 優先度 |",
        "|----------|------|--------|",
        f"| **Immediate Fix（即時修正）** | **{len(immediate)}** | High |",
        f"| Detailed Edition（詳細解析版） | {len(detailed)} | Medium/Low |",
        f"| No Change（修正不要） | {len(no_change)} | — |",
        f"| **合計** | **{len(records)}** | |",
        "",
        "---",
        "",
        "## A. Immediate Fix（即時修正）",
        "",
    ]

    if immediate:
        for r in immediate:
            lines += [
                f"### {r.article_id} / {r.h2_number}",
                "",
                f"- **sample_id**: `{r.sample_ids}`",
                f"- **公開日**: {r.published_date}",
                f"- **note URL**: {r.published_url}",
                f"- **risk_level**: {r.risk_level}",
                f"- **comparison_label**: {r.comparison_label}",
                f"- **human_confidence**: {r.human_confidence}",
                f"- **has_uap_object_neg**: {r.has_uap_object_neg}",
                f"- **evolution_status**: {r.evolution_status}",
                f"- **human_review_required**: {r.human_review_required}",
                "",
                f"**修正対象箇所**: {r.modification_target_section}",
                "",
                f"**修正草稿**: {r.modification_draft}",
                "",
                f"**next_action**: {r.next_action}",
                "",
                f"> **notes**: {r.notes}",
                "",
                "---",
                "",
            ]
    else:
        lines += ["*Immediate Fix 対象なし*", "", "---", ""]

    lines += [
        "## B. Detailed Edition（詳細解析版へ反映）",
        "",
        "| article_id | h2_number | sample_ids | priority | comparison_label | next_action |",
        "|------------|-----------|-----------|----------|-----------------|-------------|",
    ]
    for r in detailed:
        na = (r.next_action[:45] + "…") if len(r.next_action) > 45 else r.next_action
        lbl = (r.comparison_label[:35] + "…") if len(r.comparison_label) > 35 else r.comparison_label
        lines.append(f"| {r.article_id} | {r.h2_number} | `{r.sample_ids}` | {r.priority} | {lbl} | {na} |")

    lines += [
        "",
        "---",
        "",
        "## C. No Change（修正不要）",
        "",
        "| article_id | h2_number | sample_ids | notes |",
        "|------------|-----------|-----------|-------|",
    ]
    for r in no_change:
        note = (r.notes[:55] + "…") if len(r.notes) > 55 else r.notes
        lines.append(f"| {r.article_id} | {r.h2_number} | `{r.sample_ids}` | {note} |")

    lines += [
        "",
        "---",
        "",
        "## 判定ルール",
        "",
        "| ルール | 条件 | 判定 |",
        "|--------|------|------|",
        "| R1 | human_verdict=false_positive | No Change |",
        "| R2 | Missed Secondary Objects + confidence≥0.8 + 記事未記載 | Immediate Fix |",
        "| R3 | label_error + Description Gap + confidence<0.8 | No Change |",
        "| R4 | label_error + Match | Detailed Edition |",
        "| R5 | label_error + Partial Match + confidence<0.8 | Detailed Edition |",
        "| R6 | label_error + confidence≥0.8 + 記事記述あり | No Change |",
        "| R7 | GT未確認 + risk_level=MEDIUM | Detailed Edition |",
        "| R8 | GT未確認 + risk_level=SKIP | No Change |",
        "",
        "---",
        "",
        f"*Generated by `scripts/published_article_evolution.py` — {today}*",
    ]

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    Path(path).write_text("\n".join(lines), encoding="utf-8")


# ─────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Published Article Evolution Agent v1")
    parser.add_argument("--published-dir", default="published_articles/")
    parser.add_argument("--ground-truth",
                        default="data/vlm_eval_set/20260625/ground_truth.csv")
    parser.add_argument("--candidates",
                        default="data/vlm_runs/phase3_full50_20260626/article_revision_candidates.csv")
    parser.add_argument("--source-registry",
                        default="review_logs/source_registry.csv")
    parser.add_argument("--model", default="qwen2.5-vl-7b-instruct")
    parser.add_argument("--run-id", default="phase3_full50_20260626")
    parser.add_argument("--output",
                        default="review_reports/published_article_evolution_report_20260626.md")
    parser.add_argument("--csv",
                        default="data/vlm_runs/phase3_full50_20260626/published_article_evolution.csv")
    args = parser.parse_args()

    print(f"[1/4] Loading candidates      : {args.candidates}")
    candidates_by_article = load_candidates(args.candidates)

    print(f"[2/4] Loading ground truth    : {args.ground_truth}")
    gt_map = load_ground_truth(args.ground_truth)

    print(f"[3/4] Loading source registry : {args.source_registry}")
    registry = load_source_registry(args.source_registry)

    print("[4/4] Building evolution records...")
    records = build_records(candidates_by_article, gt_map, registry)

    write_csv(records, args.csv)
    print(f"      CSV  → {args.csv}")

    write_report(records, args.model, args.run_id, args.output)
    print(f"      MD   → {args.output}")

    immediate = [r for r in records if r.decision == "Immediate Fix"]
    detailed  = [r for r in records if r.decision == "Detailed Edition"]
    no_change = [r for r in records if r.decision == "No Change"]

    print("\n=== Evolution Decision Summary ===")
    print(f"  Immediate Fix    : {len(immediate)}")
    print(f"  Detailed Edition : {len(detailed)}")
    print(f"  No Change        : {len(no_change)}")
    print(f"  Total            : {len(records)}")
    print()
    for r in records:
        print(f"  {r.article_id} ({r.h2_number}) [{r.sample_ids}] → {r.decision} ({r.priority})")


if __name__ == "__main__":
    main()
