#!/usr/bin/env python3
"""
build_page_classification.py

text_layer_report.csv を元に page_classification.csv の自動分類エントリを生成する。
既存の page_classification.csv に含まれるページは保持し、未分類ページのみ追記する。
出力は page_classification_generated.csv に書き出す（本番 CSV は上書きしない）。
"""

import csv
import sys
from pathlib import Path

# ── パス設定 ──────────────────────────────────────────────────────────────────
REPO_ROOT       = Path(__file__).resolve().parent.parent
TEXT_LAYER_CSV  = REPO_ROOT / "metadata"       / "text_layer_report.csv"
EXISTING_CSV    = REPO_ROOT / "classification" / "page_classification.csv"
OUTPUT_CSV      = REPO_ROOT / "classification" / "page_classification_generated.csv"

COLUMNS = [
    "pdf_file", "page_number", "image_file",
    "classification", "confidence", "ocr_recommended",
    "processing_action", "review_required", "reason", "notes",
]


def classify(has_text_layer: str, char_count: int) -> dict:
    """text_layer_report の1行から分類結果を返す。"""
    base_notes = "auto-classified from text_layer_report"

    if has_text_layer == "true":
        if char_count >= 50:
            return dict(
                classification="typed_text",
                processing_action="skip",
                ocr_recommended="false",
                review_required="false",
                reason="has_text_layer=true; embedded text sufficient ({} chars)".format(char_count),
                notes=base_notes,
            )
        else:
            # true かつ chars < 50: 念のため try_ocr でフラグ
            return dict(
                classification="mixed_annotation",
                processing_action="try_ocr",
                ocr_recommended="true",
                review_required="true",
                reason="has_text_layer=true but only {} chars; needs review".format(char_count),
                notes=base_notes,
            )

    if has_text_layer == "false":
        return dict(
            classification="typed_text",
            processing_action="run_ocr",
            ocr_recommended="true",
            review_required="false",
            reason="has_text_layer=false; no embedded text ({} chars)".format(char_count),
            notes=base_notes,
        )

    if has_text_layer == "partial":
        if char_count < 30:
            return dict(
                classification="mixed_annotation",
                processing_action="try_ocr",
                ocr_recommended="true",
                review_required="true",
                reason="has_text_layer=partial; only {} chars (stamp/page-num fragment)".format(char_count),
                notes=base_notes,
            )
        else:
            return dict(
                classification="mixed_annotation",
                processing_action="try_ocr",
                ocr_recommended="true",
                review_required="false",
                reason="has_text_layer=partial; {} chars extracted".format(char_count),
                notes=base_notes,
            )

    # 未知の has_text_layer 値
    return dict(
        classification="unreadable",
        processing_action="skip",
        ocr_recommended="false",
        review_required="true",
        reason="unknown has_text_layer value: {}".format(has_text_layer),
        notes=base_notes,
    )


def main():
    for path, label in [(TEXT_LAYER_CSV, "text_layer_report.csv"), (EXISTING_CSV, "page_classification.csv")]:
        if not path.exists():
            print("ERROR: {} not found: {}".format(label, path))
            sys.exit(1)

    # ── 既存 CSV を読み込む ────────────────────────────────────────────────────
    existing_rows = []
    existing_keys = set()
    with open(EXISTING_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_rows.append(row)
            existing_keys.add((row["pdf_file"], row["page_number"]))

    # ── text_layer_report を読み込み、未収録ページを自動分類 ──────────────────
    new_rows = []
    with open(TEXT_LAYER_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # text_layer_report は .pdf 付き、page_classification は .pdf なし — 統一
            pdf_file = row["pdf_file"]
            if pdf_file.lower().endswith(".pdf"):
                pdf_file = pdf_file[:-4]

            key = (pdf_file, row["page_number"])
            if key in existing_keys:
                continue  # 既存行はスキップ

            char_count  = int(row["extracted_char_count"]) if row["extracted_char_count"].isdigit() else 0
            has_tl      = row["has_text_layer"].strip().lower()
            cls         = classify(has_tl, char_count)

            page_num    = int(row["page_number"])
            image_file  = "page_{:04d}.png".format(page_num)

            new_rows.append({
                "pdf_file":         pdf_file,
                "page_number":      row["page_number"],
                "image_file":       image_file,
                "classification":   cls["classification"],
                "confidence":       "0.0",
                "ocr_recommended":  cls["ocr_recommended"],
                "processing_action": cls["processing_action"],
                "review_required":  cls["review_required"],
                "reason":           cls["reason"],
                "notes":            cls["notes"],
            })

    # ── 出力 CSV に書き出す ────────────────────────────────────────────────────
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for row in existing_rows:
            writer.writerow({col: row.get(col, "") for col in COLUMNS})
        for row in new_rows:
            writer.writerow(row)

    # ── 統計レポート ──────────────────────────────────────────────────────────
    all_rows = existing_rows + new_rows
    from collections import Counter

    cls_cnt  = Counter(r["classification"]   for r in all_rows)
    act_cnt  = Counter(r["processing_action"] for r in all_rows)
    ocr_yes  = sum(1 for r in all_rows if r["ocr_recommended"]  in ("true", "True", "1"))
    rev_yes  = sum(1 for r in all_rows if r["review_required"]  in ("true", "True", "1"))

    print("=== build_page_classification 完了 ===")
    print("既存保持行数   : {:>5}".format(len(existing_rows)))
    print("自動追加行数   : {:>5}".format(len(new_rows)))
    print("合計行数       : {:>5}".format(len(all_rows)))
    print()
    print("classification 別件数:")
    for k, v in sorted(cls_cnt.items(), key=lambda x: -x[1]):
        print("  {:<30} {:>5}".format(k, v))
    print()
    print("processing_action 別件数:")
    for k, v in sorted(act_cnt.items(), key=lambda x: -x[1]):
        print("  {:<30} {:>5}".format(k, v))
    print()
    print("ocr_recommended=true  : {:>5}".format(ocr_yes))
    print("review_required=true  : {:>5}".format(rev_yes))
    print()
    print("出力先: {}".format(OUTPUT_CSV))


if __name__ == "__main__":
    main()
