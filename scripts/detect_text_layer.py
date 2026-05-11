"""
detect_text_layer.py
====================
UAP公開文書 翻訳・要約プロジェクト — PDFテキストレイヤー検出ツール

目的:
    raw_pdf/ 配下のPDFについて、ページごとにテキストレイヤーの有無を確認し、
    OCRが必要かどうかを判定する。

このツールはOCRを行わない。
「OCRが必要なページ」と「OCR不要なページ」を分けることが唯一の目的。

テキストレイヤーとは:
    PDFにはスキャン画像のみのファイルと、テキストデータが埋め込まれた
    ファイルの2種類がある。後者はOCR不要でテキストを直接取得できる。
    UAP公開文書の多くはスキャン画像のみのため、このツールで先に判別する。

出力:
    metadata/text_layer_report.csv

実行方法:
    python3 scripts/detect_text_layer.py

必要ライブラリ:
    pip3 install pymupdf
"""

import csv
import re
import sys
import traceback
from pathlib import Path

# --- PyMuPDF のインポート確認 ---
try:
    import fitz  # PyMuPDF
except ImportError:
    print("=" * 60)
    print("[エラー] PyMuPDF がインストールされていません。")
    print("  以下のコマンドを実行してからやり直してください:")
    print("  pip3 install pymupdf")
    print("=" * 60)
    sys.exit(1)

# -------------------------------------------------------
# パス設定
# -------------------------------------------------------
PROJECT_ROOT  = Path(__file__).resolve().parent.parent
RAW_PDF_DIR   = PROJECT_ROOT / "raw_pdf"
METADATA_DIR  = PROJECT_ROOT / "metadata"
OUTPUT_CSV    = METADATA_DIR / "text_layer_report.csv"

# -------------------------------------------------------
# 判定しきい値
# -------------------------------------------------------

# 「テキストレイヤーあり」と見なす最低文字数
# 政府文書のタイプページは通常数百文字あるため、50字を最低ラインとする
TEXT_LAYER_MIN_CHARS = 50

# 「部分的なテキストレイヤー」と見なす最低文字数（1〜49字）
# ページ番号・ヘッダー・OCR残滓などが該当する
PARTIAL_MIN_CHARS = 1

# CSVに保存するサンプルテキストの最大文字数
SAMPLE_MAX_CHARS = 120

# -------------------------------------------------------
# テキスト前処理
# -------------------------------------------------------

def clean_text(raw: str) -> str:
    """
    PDFから抽出した生テキストを整形する。
    - 連続する空白・改行を1スペースに置換
    - 制御文字を除去
    """
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", raw)  # 制御文字除去
    text = re.sub(r"\s+", " ", text).strip()
    return text


def sample_text(text: str) -> str:
    """先頭 SAMPLE_MAX_CHARS 文字をサンプルとして返す。"""
    s = text[:SAMPLE_MAX_CHARS]
    return s if len(text) <= SAMPLE_MAX_CHARS else s + "…"


# -------------------------------------------------------
# 1ページの判定
# -------------------------------------------------------

def judge_page(raw_text: str) -> tuple[str, bool, str, str]:
    """
    ページのテキストから has_text_layer / ocr_needed / reason / notes を返す。

    Returns:
        (has_text_layer, ocr_needed, reason, notes)
        has_text_layer: "true" | "partial" | "false"
        ocr_needed:     True / False
    """
    text = clean_text(raw_text)
    char_count = len(text)

    if char_count >= TEXT_LAYER_MIN_CHARS:
        return (
            "true",
            False,
            f"embedded text sufficient ({char_count} chars)",
            "text layer present, OCR not needed",
        )
    elif char_count >= PARTIAL_MIN_CHARS:
        return (
            "partial",
            True,
            f"only {char_count} chars extracted — possibly page number or header only",
            "partial text layer detected; may be page numbers, stamps, or OCR artifacts",
        )
    else:
        return (
            "false",
            True,
            "no extractable text found on this page",
            "no text layer; OCR required",
        )


# -------------------------------------------------------
# 1ページの処理
# -------------------------------------------------------

def process_page(pdf_name: str, page_num: int, page: fitz.Page) -> dict:
    """
    1ページ分のテキスト抽出・判定を行い dict を返す。
    エラーが起きても記録して継続する。
    """
    try:
        raw_text  = page.get_text("text")  # テキストレイヤーから抽出
        text      = clean_text(raw_text)
        char_count = len(text)
        s_text    = sample_text(text)
        has_layer, ocr_needed, reason, notes = judge_page(raw_text)
    except Exception as e:
        print(f"  [警告] {pdf_name} p.{page_num} のテキスト抽出に失敗: {e}")
        char_count = 0
        s_text     = ""
        has_layer  = "false"
        ocr_needed = True
        reason     = f"extraction error: {e}"
        notes      = "processing error; treat as no text layer"

    return {
        "pdf_file":            pdf_name,
        "page_number":         page_num,
        "has_text_layer":      has_layer,
        "extracted_char_count": char_count,
        "sample_text":         s_text,
        "ocr_needed":          "true" if ocr_needed else "false",
        "reason":              reason,
        "notes":               notes,
    }


# -------------------------------------------------------
# メイン処理
# -------------------------------------------------------

CSV_FIELDS = [
    "pdf_file",
    "page_number",
    "has_text_layer",
    "extracted_char_count",
    "sample_text",
    "ocr_needed",
    "reason",
    "notes",
]


def main():
    print("=" * 60)
    print("PDFテキストレイヤー検出ツール（UAP_TRANSLATION_PROJECT）")
    print("=" * 60)
    print(f"  入力元 : {RAW_PDF_DIR}")
    print(f"  出力先 : {OUTPUT_CSV}")
    print(f"  判定しきい値: {TEXT_LAYER_MIN_CHARS}字以上 → has_text_layer=true")
    print()

    if not RAW_PDF_DIR.exists():
        print(f"[エラー] フォルダが見つかりません: {RAW_PDF_DIR}")
        sys.exit(1)

    pdf_files = sorted(
        list(RAW_PDF_DIR.glob("*.pdf")) + list(RAW_PDF_DIR.glob("*.PDF"))
    )

    if not pdf_files:
        print("[情報] raw_pdf/ に PDF ファイルが見つかりませんでした。")
        sys.exit(0)

    print(f"対象PDF: {len(pdf_files)} 件")
    print()

    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    all_rows    = []
    total_pages = 0
    error_pdfs  = 0

    for idx, pdf_path in enumerate(pdf_files, start=1):
        print(f"[{idx}/{len(pdf_files)}] {pdf_path.name} を処理中...")

        try:
            doc = fitz.open(str(pdf_path))
        except Exception as e:
            print(f"  [エラー] PDF を開けませんでした: {e}")
            error_pdfs += 1
            continue

        pdf_name   = pdf_path.name
        page_count = len(doc)

        ocr_true    = 0
        ocr_false   = 0
        has_partial = 0

        for page_num in range(page_count):
            page = doc.load_page(page_num)
            row  = process_page(pdf_name, page_num + 1, page)
            all_rows.append(row)
            total_pages += 1

            if row["ocr_needed"] == "true":
                ocr_true += 1
            else:
                ocr_false += 1
            if row["has_text_layer"] == "partial":
                has_partial += 1

        doc.close()

        print(f"  合計 {page_count} ページ")
        print(f"  OCR不要(text layer あり): {ocr_false} ページ")
        print(f"  OCR必要                 : {ocr_true} ページ")
        if has_partial:
            print(f"  部分的テキストレイヤー  : {has_partial} ページ")
        print()

    # CSV 書き出し
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)

    # 全体サマリ
    total_ocr_needed  = sum(1 for r in all_rows if r["ocr_needed"] == "true")
    total_ocr_skipped = sum(1 for r in all_rows if r["ocr_needed"] == "false")
    total_partial     = sum(1 for r in all_rows if r["has_text_layer"] == "partial")

    print("=" * 60)
    print(f"処理完了 — 合計 {total_pages} ページ")
    print(f"  OCR不要(text layer あり) : {total_ocr_skipped} ページ")
    print(f"  OCR必要                  : {total_ocr_needed} ページ")
    print(f"  うち部分的テキストレイヤー: {total_partial} ページ")
    print(f"  PDFエラー                : {error_pdfs} 件")
    print(f"CSV 出力: {OUTPUT_CSV}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[中断] ユーザーによって処理が中断されました。")
        sys.exit(0)
    except Exception:
        print("[予期しないエラー]")
        traceback.print_exc()
        sys.exit(1)
