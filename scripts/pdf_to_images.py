"""
pdf_to_images.py
================
UAP公開文書 翻訳・要約プロジェクト — PDFページ画像化ツール

目的:
    raw_pdf/ フォルダにある PDF を、1ページずつ PNG 画像に変換し、
    page_images/ 配下へ保存する。

OCR・翻訳・要約は行わない。まずPNG化の安定稼働を優先する。

実行方法:
    python3 scripts/pdf_to_images.py

必要ライブラリ:
    pip3 install pymupdf

作成者: UAP_TRANSLATION_PROJECT
"""

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
# パス設定（このファイルの2階層上 = プロジェクトルート）
# -------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PDF_DIR  = PROJECT_ROOT / "raw_pdf"
PAGE_IMG_DIR = PROJECT_ROOT / "page_images"

# PNG 出力解像度（DPI）
# 150 = 速度重視・軽量
# 200 = 標準（OCR前提ならこれで十分）
# 300 = 高精細（ファイルサイズ大）
DPI = 200

# fitz の matrix: 72dpi基準なので scale = DPI / 72
SCALE = DPI / 72.0
MATRIX = fitz.Matrix(SCALE, SCALE)


def pdf_to_images(pdf_path: Path) -> dict:
    """
    1つの PDF をページごとの PNG へ変換する。

    Returns:
        {"success": bool, "pages": int, "output_dir": Path, "error": str}
    """
    # PDF のファイル名（拡張子なし）をサブフォルダ名に使う
    folder_name = pdf_path.stem
    output_dir  = PAGE_IMG_DIR / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as e:
        return {
            "success": False,
            "pages": 0,
            "output_dir": output_dir,
            "error": f"PDF を開けませんでした: {e}",
        }

    total_pages = len(doc)
    saved = 0

    for page_num in range(total_pages):
        # ページ番号は1始まり・4桁ゼロ埋め（例: page_0001.png）
        page_label = f"page_{page_num + 1:04d}.png"
        out_path   = output_dir / page_label

        # すでに変換済みのページはスキップ（再実行時の差分処理）
        if out_path.exists():
            saved += 1
            continue

        try:
            page   = doc.load_page(page_num)
            pixmap = page.get_pixmap(matrix=MATRIX, alpha=False)
            pixmap.save(str(out_path))
            saved += 1
        except Exception as e:
            # 1ページ失敗しても次のページへ進む
            print(f"  [警告] {pdf_path.name} p.{page_num + 1} の変換に失敗: {e}")

    doc.close()

    return {
        "success": True,
        "pages": saved,
        "output_dir": output_dir,
        "error": "",
    }


def main():
    print("=" * 60)
    print("PDF → PNG 変換ツール（UAP_TRANSLATION_PROJECT）")
    print("=" * 60)
    print(f"  読み込み元 : {RAW_PDF_DIR}")
    print(f"  出力先     : {PAGE_IMG_DIR}")
    print(f"  解像度     : {DPI} DPI")
    print()

    # raw_pdf/ が存在するか確認
    if not RAW_PDF_DIR.exists():
        print(f"[エラー] フォルダが見つかりません: {RAW_PDF_DIR}")
        sys.exit(1)

    # PDF ファイル一覧を取得（大文字小文字両方）
    pdf_files = sorted(
        list(RAW_PDF_DIR.glob("*.pdf")) + list(RAW_PDF_DIR.glob("*.PDF"))
    )

    if not pdf_files:
        print("[情報] raw_pdf/ に PDF ファイルが見つかりませんでした。")
        sys.exit(0)

    print(f"対象 PDF: {len(pdf_files)} 件")
    print()

    success_count = 0
    error_count   = 0

    for idx, pdf_path in enumerate(pdf_files, start=1):
        print(f"[{idx}/{len(pdf_files)}] {pdf_path.name} を処理中...")

        result = pdf_to_images(pdf_path)

        if result["success"]:
            print(f"  -> 完了: {result['pages']} ページ保存 ({result['output_dir']})")
            success_count += 1
        else:
            print(f"  -> 失敗: {result['error']}")
            error_count += 1

    print()
    print("=" * 60)
    print(f"処理完了 — 成功: {success_count} 件 / 失敗: {error_count} 件")
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
