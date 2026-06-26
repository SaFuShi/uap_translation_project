#!/usr/bin/env python3
"""
score_vlm_vs_ground_truth.py

Compare VLM evaluation results against human ground truth and compute
detection scores (Precision / Recall / F1) with category and comparison_label breakdowns.

Scoring modes
─────────────
gold   (default): Uses only samples present in ground_truth.csv (human-reviewed).
proxy : Uses all samples from results.csv, deriving expected labels from category:
          A_clear_candidate   → expected visible=true
          B_small_unclear     → expected visible=true  (ambiguous; included but flagged)
          C_no_visible_target → expected visible=false
          D_sensor_ui_background → expected visible=false
          E_known_miss_case   → expected visible=true

The gold mode is authoritative. Proxy mode supplements it for full-50 coverage.

Safety
──────
- Read-only on all project files (ground_truth, results, manifest).
- Writes only to the --output and --score-csv paths.
- Does not touch note_drafts, workflow.db, source_registry, or manifest.csv.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

CATEGORY_PROXY_LABEL: dict[str, bool | None] = {
    "A_clear_candidate":      True,
    "B_small_unclear":        None,   # ambiguous — excluded from proxy F1
    "C_no_visible_target":    False,
    "D_sensor_ui_background": False,
    "E_known_miss_case":      True,
}

COMPARISON_LABELS_ORDER = [
    "Match",
    "Partial Match",
    "Partial Match / Description Gap",
    "Partial Match / Missed Secondary Objects",
    "Description Gap",
    "Missed Secondary Objects",
    "False Positive",
    "False Positive / Acceptable",
    "False Negative",
    "Acceptable",
    "Label Error",
]

CATEGORY_ORDER = [
    "A_clear_candidate",
    "B_small_unclear",
    "C_no_visible_target",
    "D_sensor_ui_background",
    "E_known_miss_case",
]


# ── Loaders ───────────────────────────────────────────────────────────────────

def load_ground_truth(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sid = row["sample_id"].strip()
            rows[sid] = row
    return rows


def load_results(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sid = row["sample_id"].strip()
            rows[sid] = row
    return rows


def parse_bool(value: str | bool | None) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    v = str(value).strip().lower()
    if v in ("true", "1", "yes"):
        return True
    if v in ("false", "0", "no"):
        return False
    return None


# ── Confusion matrix helpers ───────────────────────────────────────────────────

def compute_confusion(pairs: list[tuple[bool, bool]]) -> dict[str, int]:
    tp = fp = tn = fn = 0
    for human, vlm in pairs:
        if human and vlm:
            tp += 1
        elif not human and vlm:
            fp += 1
        elif not human and not vlm:
            tn += 1
        else:
            fn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}


def prf(cm: dict[str, int]) -> tuple[float, float, float]:
    tp, fp, fn = cm["tp"], cm["fp"], cm["fn"]
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1        = (2 * precision * recall / (precision + recall)
                 if (precision + recall) > 0 else 0.0)
    return precision, recall, f1


# ── Score computation ──────────────────────────────────────────────────────────

def score_gold(
    gt: dict[str, dict],
    results: dict[str, dict],
) -> dict:
    """Score using only ground-truth samples (authoritative)."""
    matched: list[dict] = []
    unmatched_gt: list[str] = []

    for sid, gt_row in gt.items():
        if sid not in results:
            unmatched_gt.append(sid)
            continue
        r = results[sid]
        human_vis = parse_bool(gt_row.get("human_visible_candidate"))
        vlm_vis   = parse_bool(r.get("visible_candidate"))
        if human_vis is None or vlm_vis is None:
            continue
        matched.append({
            "sample_id":         sid,
            "category":          gt_row.get("category", r.get("category", "")),
            "human_visible":     human_vis,
            "vlm_visible":       vlm_vis,
            "human_verdict":     gt_row.get("human_verdict", ""),
            "comparison_label":  gt_row.get("comparison_label", ""),
            "review_required":   gt_row.get("review_required", ""),
            "human_confidence":  gt_row.get("human_confidence", ""),
            "vlm_confidence":    r.get("confidence", ""),
            "human_description": gt_row.get("human_description", ""),
            "vlm_description":   r.get("description", ""),
        })

    pairs = [(m["human_visible"], m["vlm_visible"]) for m in matched]
    cm = compute_confusion(pairs)
    precision, recall, f1 = prf(cm)

    # Per-category breakdown
    by_cat: dict[str, list[tuple[bool, bool]]] = defaultdict(list)
    for m in matched:
        by_cat[m["category"]].append((m["human_visible"], m["vlm_visible"]))

    cat_scores: dict[str, dict] = {}
    for cat, cat_pairs in by_cat.items():
        c = compute_confusion(cat_pairs)
        p, r_, f = prf(c)
        cat_scores[cat] = {**c, "precision": p, "recall": r_, "f1": f, "n": len(cat_pairs)}

    # comparison_label distribution
    comp_counts: dict[str, int] = defaultdict(int)
    for m in matched:
        for label in m["comparison_label"].split("/"):
            comp_counts[label.strip()] += 1

    # human_verdict distribution
    verdict_counts: dict[str, int] = defaultdict(int)
    for gt_row in gt.values():
        verdict_counts[gt_row.get("human_verdict", "unknown")] += 1

    return {
        "mode": "gold",
        "n_ground_truth": len(gt),
        "n_matched": len(matched),
        "n_unmatched_gt": len(unmatched_gt),
        "unmatched_gt": unmatched_gt,
        "cm": cm,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "cat_scores": cat_scores,
        "comp_counts": dict(comp_counts),
        "verdict_counts": dict(verdict_counts),
        "matched": matched,
        "description_gap_count": sum(
            1 for m in matched if "Description Gap" in m["comparison_label"]
        ),
        "missed_secondary_count": sum(
            1 for m in matched if "Missed Secondary Objects" in m["comparison_label"]
        ),
        "label_error_count": sum(
            1 for m in matched if m["human_verdict"] == "label_error"
        ),
        "review_required_count": sum(
            1 for m in matched
            if str(m["review_required"]).strip().lower() in ("true", "1")
        ),
    }


def score_proxy(results: dict[str, dict]) -> dict:
    """Score all 50 samples using category-derived expected labels."""
    pairs: list[tuple[bool, bool]] = []
    by_cat: dict[str, list[tuple[bool, bool]]] = defaultdict(list)
    skipped_ambiguous: list[str] = []
    included: list[dict] = []

    for sid, r in results.items():
        cat = r.get("category", "")
        expected = CATEGORY_PROXY_LABEL.get(cat)
        if expected is None:
            skipped_ambiguous.append(sid)
            continue
        vlm_vis = parse_bool(r.get("visible_candidate"))
        if vlm_vis is None:
            continue
        pairs.append((expected, vlm_vis))
        by_cat[cat].append((expected, vlm_vis))
        included.append({"sample_id": sid, "category": cat,
                          "expected": expected, "vlm_visible": vlm_vis})

    cm = compute_confusion(pairs)
    precision, recall, f1 = prf(cm)

    cat_scores: dict[str, dict] = {}
    for cat in CATEGORY_ORDER:
        cat_pairs = by_cat.get(cat, [])
        if not cat_pairs:
            continue
        c = compute_confusion(cat_pairs)
        p, r_, f = prf(c)
        cat_scores[cat] = {**c, "precision": p, "recall": r_, "f1": f, "n": len(cat_pairs)}

    return {
        "mode": "proxy",
        "n_total": len(results),
        "n_included": len(pairs),
        "n_skipped_ambiguous": len(skipped_ambiguous),
        "skipped_ambiguous": skipped_ambiguous,
        "cm": cm,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "cat_scores": cat_scores,
    }


# ── CSV writer ────────────────────────────────────────────────────────────────

def write_score_csv(gold: dict, proxy: dict, model: str, run_id: str, path: Path) -> None:
    rows = []

    def _row(scope: str, category: str, mode: str, cm: dict, p: float, r_: float, f: float, n: int) -> dict:
        return {
            "model": model, "run_id": run_id, "scope": scope, "category": category,
            "mode": mode, "n": n,
            "tp": cm["tp"], "fp": cm["fp"], "tn": cm["tn"], "fn": cm["fn"],
            "precision": f"{p:.4f}", "recall": f"{r_:.4f}", "f1": f"{f:.4f}",
        }

    g_p, g_r, g_f = gold["precision"], gold["recall"], gold["f1"]
    rows.append(_row("overall", "all", "gold", gold["cm"], g_p, g_r, g_f, gold["n_matched"]))
    for cat, s in gold["cat_scores"].items():
        rows.append(_row("category", cat, "gold", s, s["precision"], s["recall"], s["f1"], s["n"]))

    px_p, px_r, px_f = proxy["precision"], proxy["recall"], proxy["f1"]
    rows.append(_row("overall", "all", "proxy", proxy["cm"], px_p, px_r, px_f, proxy["n_included"]))
    for cat, s in proxy["cat_scores"].items():
        rows.append(_row("category", cat, "proxy", s, s["precision"], s["recall"], s["f1"], s["n"]))

    fields = ["model", "run_id", "scope", "category", "mode", "n",
              "tp", "fp", "tn", "fn", "precision", "recall", "f1"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


# ── Markdown report ───────────────────────────────────────────────────────────

def _pct(v: float) -> str:
    return f"{v*100:.1f}%"


def write_md_report(
    gold: dict, proxy: dict,
    model: str, run_id: str,
    gt_path: Path, results_path: Path,
    score_csv: Path,
    output: Path,
) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def cm_row(label: str, cm: dict, p: float, r_: float, f: float, n: int) -> str:
        return (f"| {label} | {n} | {cm['tp']} | {cm['fp']} | {cm['tn']} | {cm['fn']} "
                f"| {_pct(p)} | {_pct(r_)} | {_pct(f)} |")

    lines: list[str] = [
        f"# VLM Score Report — {model}",
        "",
        f"- 実施日時: {now}",
        f"- モデル: `{model}`",
        f"- run_id: `{run_id}`",
        f"- ground_truth: `{gt_path}`",
        f"- results: `{results_path}`",
        f"- score_csv: `{score_csv}`",
        "",
        "---",
        "",
        "## 1. Gold スコア（人間目視 ground truth 7件）",
        "",
        (f"Ground truth に登録された {gold['n_ground_truth']} 件中 "
         f"{gold['n_matched']} 件が results.csv と突合できた。"),
        "",
        "### Overall",
        "",
        "| scope | n | TP | FP | TN | FN | Precision | Recall | F1 |",
        "|-------|---|----|----|----|----|-----------|--------|----|",
        cm_row("overall (gold)", gold["cm"], gold["precision"], gold["recall"], gold["f1"], gold["n_matched"]),
        "",
        "### Category 別（gold）",
        "",
        "| category | n | TP | FP | TN | FN | Precision | Recall | F1 |",
        "|----------|---|----|----|----|----|-----------|--------|----|",
    ]
    for cat in CATEGORY_ORDER:
        s = gold["cat_scores"].get(cat)
        if s:
            lines.append(cm_row(cat, s, s["precision"], s["recall"], s["f1"], s["n"]))

    lines += [
        "",
        "### comparison_label 分布（gold）",
        "",
        "| comparison_label | 件数 |",
        "|-----------------|------|",
    ]
    for label, cnt in sorted(gold["comp_counts"].items(), key=lambda x: -x[1]):
        lines.append(f"| {label} | {cnt} |")

    lines += [
        "",
        "### human_verdict 分布",
        "",
        "| human_verdict | 件数 |",
        "|--------------|------|",
    ]
    for verdict, cnt in sorted(gold["verdict_counts"].items(), key=lambda x: -x[1]):
        lines.append(f"| {verdict} | {cnt} |")

    lines += [
        "",
        "### 詳細指標（gold）",
        "",
        f"- description_gap 件数: {gold['description_gap_count']}",
        f"- missed_secondary_objects 件数: {gold['missed_secondary_count']}",
        f"- label_error 件数: {gold['label_error_count']}",
        f"- review_required 件数: {gold['review_required_count']}",
        "",
        "---",
        "",
        "## 2. Proxy スコア（カテゴリラベルを正解とした全50件）",
        "",
        (f"B_small_unclear ({proxy['n_skipped_ambiguous']} 件) は ambiguous のため除外。"
         f"{proxy['n_included']} 件でスコアを算出。"),
        "",
        "### Overall",
        "",
        "| scope | n | TP | FP | TN | FN | Precision | Recall | F1 |",
        "|-------|---|----|----|----|----|-----------|--------|----|",
        cm_row("overall (proxy)", proxy["cm"], proxy["precision"], proxy["recall"], proxy["f1"], proxy["n_included"]),
        "",
        "### Category 別（proxy）",
        "",
        "| category | n | TP | FP | TN | FN | Precision | Recall | F1 |",
        "|----------|---|----|----|----|----|-----------|--------|----|",
    ]
    for cat in CATEGORY_ORDER:
        s = proxy["cat_scores"].get(cat)
        if s:
            lines.append(cm_row(cat, s, s["precision"], s["recall"], s["f1"], s["n"]))

    lines += [
        "",
        "---",
        "",
        "## 3. サンプル別詳細（gold 7件）",
        "",
        "| sample_id | category | human_visible | vlm_visible | human_conf | vlm_conf | human_verdict | comparison_label |",
        "|-----------|----------|---------------|-------------|------------|----------|---------------|-----------------|",
    ]
    for m in gold["matched"]:
        lines.append(
            f"| {m['sample_id']} | {m['category']} "
            f"| {m['human_visible']} | {m['vlm_visible']} "
            f"| {m['human_confidence']} | {m['vlm_confidence']} "
            f"| {m['human_verdict']} | {m['comparison_label']} |"
        )

    # Interpretation
    g_f = gold["f1"]
    g_p = gold["precision"]
    g_r = gold["recall"]
    if g_f >= 0.8:
        judgment = "良好。次モデル比較へ進める。"
    elif g_f >= 0.6:
        judgment = "許容範囲。プロンプト調整 or 32B モデルで改善を検討。"
    else:
        judgment = "要改善。プロンプト再設計または上位モデルへの切替を推奨。"

    proxy_c_fp = proxy["cat_scores"].get("C_no_visible_target", {}).get("fp", 0)
    proxy_d_fp = proxy["cat_scores"].get("D_sensor_ui_background", {}).get("fp", 0)

    lines += [
        "",
        "---",
        "",
        "## 4. 総合評価",
        "",
        f"- Gold F1: **{_pct(g_f)}** (Precision {_pct(g_p)} / Recall {_pct(g_r)})",
        f"- Proxy F1: **{_pct(proxy['f1'])}**",
        f"- C_no_visible_target 誤検出（proxy）: {proxy_c_fp} 件",
        f"  （うち label_error 確定: {gold['label_error_count']} 件）",
        f"- D_sensor_ui_background 誤検出（proxy）: {proxy_d_fp} 件",
        "",
        f"**→ 判定: {judgment}**",
        "",
        "### 次モデル比較時の基準",
        "",
        "- 同一 ground_truth.csv を使用",
        "- Gold F1 がこのスコアを上回るか確認",
        "- missed_secondary_objects の改善（特に vlm_0049 の赤い光源2個）",
        "- C/D 誤検出率の低減",
        "",
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Score VLM results against ground truth.")
    p.add_argument("--ground-truth", type=Path, required=True)
    p.add_argument("--results",      type=Path, required=True)
    p.add_argument("--model",        type=str,  required=True)
    p.add_argument("--run-id",       type=str,  required=True)
    p.add_argument("--output",       type=Path, required=True)
    p.add_argument("--score-csv",    type=Path, default=None,
                   help="Path for score summary CSV. Defaults to results dir / score_summary.csv")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if not args.ground_truth.exists():
        print(f"ERROR: ground-truth not found: {args.ground_truth}")
        return 1
    if not args.results.exists():
        print(f"ERROR: results not found: {args.results}")
        return 1

    score_csv = args.score_csv or (args.results.parent / "score_summary.csv")

    print(f"Loading ground truth: {args.ground_truth}")
    gt = load_ground_truth(args.ground_truth)
    print(f"  → {len(gt)} samples")

    print(f"Loading results: {args.results}")
    results = load_results(args.results)
    print(f"  → {len(results)} samples")

    print("Computing gold scores ...")
    gold = score_gold(gt, results)

    print("Computing proxy scores ...")
    proxy = score_proxy(results)

    print("Writing score CSV ...")
    write_score_csv(gold, proxy, args.model, args.run_id, score_csv)

    print("Writing Markdown report ...")
    write_md_report(
        gold, proxy,
        model=args.model,
        run_id=args.run_id,
        gt_path=args.ground_truth,
        results_path=args.results,
        score_csv=score_csv,
        output=args.output,
    )

    g_p, g_r, g_f = gold["precision"], gold["recall"], gold["f1"]
    print()
    print(f"=== Gold Score (n={gold['n_matched']}) ===")
    print(f"  TP={gold['cm']['tp']}  FP={gold['cm']['fp']}  "
          f"TN={gold['cm']['tn']}  FN={gold['cm']['fn']}")
    print(f"  Precision={g_p:.3f}  Recall={g_r:.3f}  F1={g_f:.3f}")
    print()
    print(f"=== Proxy Score (n={proxy['n_included']}) ===")
    print(f"  TP={proxy['cm']['tp']}  FP={proxy['cm']['fp']}  "
          f"TN={proxy['cm']['tn']}  FN={proxy['cm']['fn']}")
    print(f"  Precision={proxy['precision']:.3f}  "
          f"Recall={proxy['recall']:.3f}  F1={proxy['f1']:.3f}")
    print()
    print(f"report   : {args.output}")
    print(f"score_csv: {score_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
