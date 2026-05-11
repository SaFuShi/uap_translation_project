"""
classify_pages.py
=================
UAP公開文書 翻訳・要約プロジェクト — ページ仮分類ツール

目的:
    page_images/ 配下の PNG を読み取り、
    OCR・翻訳処理へ進めるための仮分類と処理ルート (routing) を
    classification/page_classification.csv へ出力する。

分類方針:
    外部API・AI を使わず、画像の統計的特徴量（明暗・エッジ密度など）を
    もとにした軽量な仮分類を行う。
    分類精度 100% ではなく、次工程へ進めるための routing 情報を優先する。

非対象:
    OCR・翻訳・要約・note整形・外部APIへの送信

実行方法:
    python3 scripts/classify_pages.py

必要ライブラリ:
    pip3 install pillow numpy
"""

import csv
import sys
import traceback
from pathlib import Path

# --- 依存ライブラリ確認 ---
try:
    import numpy as np
    from PIL import Image, ImageFilter
except ImportError as e:
    print("=" * 60)
    print(f"[エラー] 必要なライブラリがインストールされていません: {e}")
    print("  以下のコマンドを実行してからやり直してください:")
    print("  pip3 install pillow numpy")
    print("=" * 60)
    sys.exit(1)

# -------------------------------------------------------
# パス設定
# -------------------------------------------------------
PROJECT_ROOT    = Path(__file__).resolve().parent.parent
PAGE_IMG_DIR    = PROJECT_ROOT / "page_images"
CLASSIFICATION_DIR = PROJECT_ROOT / "classification"
OUTPUT_CSV      = CLASSIFICATION_DIR / "page_classification.csv"

# -------------------------------------------------------
# 分類スキーマ（classification_schema.md 準拠）
# -------------------------------------------------------

# classification → (ocr_recommended, processing_action, review_required)
ROUTING_TABLE = {
    "typed_text":                ("true",             "run_ocr",              "false"),
    "mixed_annotation":          ("conditional",      "try_ocr",              "true"),
    "newspaper_or_print_clipping": ("conditional",    "try_layout_ocr",       "true"),
    "handwritten":               ("false",            "try_vision_or_review", "true"),
    "image_or_photo":            ("false",            "skip_ocr",             "false"),
    "admin_or_cover":            ("metadata_only",    "extract_metadata",     "false"),
    "unreadable":                ("false",            "skip_and_record",      "true"),
}


# -------------------------------------------------------
# 画像特徴量の抽出
# -------------------------------------------------------

def extract_features(img_path: Path) -> dict:
    """
    グレースケール画像から分類に使う統計的特徴量を抽出する。

    Returns:
        dict with keys: mean_bright, std_bright, white_ratio, dark_ratio,
                        edge_ratio, width, height, aspect_ratio
    """
    img = Image.open(str(img_path)).convert("L")  # グレースケール変換

    arr = np.array(img, dtype=np.float32)

    mean_bright = float(arr.mean())
    std_bright  = float(arr.std())
    white_ratio = float((arr > 240).sum() / arr.size)   # ほぼ白の画素割合
    dark_ratio  = float((arr < 30).sum()  / arr.size)   # ほぼ黒の画素割合

    # エッジ検出（FIND_EDGES フィルタ → 閾値で二値化してエッジ割合を算出）
    edge_img = img.filter(ImageFilter.FIND_EDGES)
    edge_arr = np.array(edge_img, dtype=np.float32)
    edge_ratio = float((edge_arr > 20).sum() / edge_arr.size)

    w, h = img.size
    aspect_ratio = round(w / h, 3) if h > 0 else 1.0

    return {
        "mean_bright": round(mean_bright, 2),
        "std_bright":  round(std_bright,  2),
        "white_ratio": round(white_ratio, 4),
        "dark_ratio":  round(dark_ratio,  4),
        "edge_ratio":  round(edge_ratio,  4),
        "width":       w,
        "height":      h,
        "aspect_ratio": aspect_ratio,
    }


# -------------------------------------------------------
# 仮分類ロジック
# -------------------------------------------------------

def classify(features: dict, page_num: int) -> tuple[str, float, str]:
    """
    特徴量から分類カテゴリ・信頼度・理由を返す。

    Returns:
        (classification, confidence, reason)
    """
    w  = features["white_ratio"]
    d  = features["dark_ratio"]
    m  = features["mean_bright"]
    s  = features["std_bright"]
    e  = features["edge_ratio"]
    ar = features["aspect_ratio"]

    # --- 1. 判読不能（暗い・潰れ） ---
    if d > 0.45 or m < 65:
        return "unreadable", 0.75, "very dark or heavily degraded scan"

    # --- 2. ほぼ空白 → 表紙・管理票候補 ---
    if w > 0.96 and e < 0.015:
        return "admin_or_cover", 0.60, "near-blank page, likely cover or separator"

    # --- 3. 写真・図版中心（高分散・低エッジ・低白割合） ---
    # 写真はグラデーションが多く std が高いが、テキストのような鋭いエッジは少ない
    if s > 62 and e < 0.07 and w < 0.62:
        return "image_or_photo", 0.65, "high tonal variance with low edge density, likely photo or figure"

    # --- 4. 横長ページ → 新聞・切り抜き候補 ---
    if ar > 1.3 and e > 0.04:
        return ("newspaper_or_print_clipping", 0.50,
                "landscape orientation with text edges, possibly newspaper clipping")

    # --- 5. タイプ文書（高白割合 + 適度なエッジ） ---
    if w > 0.72 and e >= 0.05:
        # 暗い画素がある程度あればスタンプ・注釈混在と判断
        if d > 0.04 and s > 42:
            return ("mixed_annotation", 0.55,
                    "typed text with notable dark regions, possibly stamps or handwritten annotations")
        return "typed_text", 0.75, "high white background with text-level edge density"

    # --- 6. 中程度のエッジ → タイプ文書（薄い・かすれ）または手書き ---
    if e >= 0.02:
        if w > 0.65:
            return "typed_text", 0.60, "moderate edge density on white background, likely typed"
        # 白割合が低く中程度エッジ → 手書き or 混在
        if s > 38:
            return "mixed_annotation", 0.45, "moderate edges on non-white background, possibly mixed content"
        return "handwritten", 0.40, "low-to-moderate edges with non-white background, possibly handwritten"

    # --- 7. エッジが極めて少ない → 手書き（薄い筆跡）または 表紙 ---
    if w > 0.60:
        if page_num == 1:
            return "admin_or_cover", 0.55, "low edge density on first page, likely cover sheet"
        return "typed_text", 0.45, "very low edge density but white page, possibly light typed content"

    # --- 8. 判断困難 → 混在扱い ---
    return "mixed_annotation", 0.30, "uncertain features, review recommended"


# -------------------------------------------------------
# 1ページ分の処理
# -------------------------------------------------------

def process_page(pdf_name: str, page_num: int, img_path: Path) -> dict:
    """
    1ページ分の特徴量抽出・分類・ルーティングを実行して dict を返す。
    エラーが起きても unreadable として記録する。
    """
    try:
        features = extract_features(img_path)
        cls, conf, reason = classify(features, page_num)
    except Exception as e:
        # 画像読み込み失敗などはエラーとして記録し処理継続
        print(f"  [警告] {img_path.name} の処理に失敗: {e}")
        cls, conf, reason = "unreadable", 0.0, f"processing error: {e}"
        features = {"width": 0, "height": 0}

    ocr_rec, proc_action, review_req = ROUTING_TABLE[cls]

    # confidence が低い場合は強制的に review_required = true
    if conf < 0.45 and review_req == "false":
        review_req = "true"

    notes = (
        f"w={features.get('width',0)} h={features.get('height',0)} "
        f"edge={features.get('edge_ratio', 0):.4f} "
        f"white={features.get('white_ratio', 0):.4f} "
        f"dark={features.get('dark_ratio', 0):.4f} "
        f"std={features.get('std_bright', 0):.2f}"
    )

    return {
        "pdf_file":          pdf_name,
        "page_number":       page_num,
        "image_file":        img_path.name,
        "classification":    cls,
        "confidence":        round(conf, 2),
        "ocr_recommended":   ocr_rec,
        "processing_action": proc_action,
        "review_required":   review_req,
        "reason":            reason,
        "notes":             notes,
    }


# -------------------------------------------------------
# メイン処理
# -------------------------------------------------------

CSV_FIELDS = [
    "pdf_file", "page_number", "image_file",
    "classification", "confidence", "ocr_recommended",
    "processing_action", "review_required",
    "reason", "notes",
]


def main():
    print("=" * 60)
    print("ページ仮分類ツール（UAP_TRANSLATION_PROJECT）")
    print("=" * 60)
    print(f"  入力元 : {PAGE_IMG_DIR}")
    print(f"  出力先 : {OUTPUT_CSV}")
    print()

    if not PAGE_IMG_DIR.exists():
        print(f"[エラー] フォルダが見つかりません: {PAGE_IMG_DIR}")
        sys.exit(1)

    # PDFごとのサブフォルダを走査
    pdf_dirs = sorted([d for d in PAGE_IMG_DIR.iterdir() if d.is_dir()])
    if not pdf_dirs:
        print("[情報] page_images/ にサブフォルダが見つかりませんでした。")
        sys.exit(0)

    print(f"対象PDFフォルダ: {len(pdf_dirs)} 件")
    print()

    CLASSIFICATION_DIR.mkdir(parents=True, exist_ok=True)

    all_rows    = []
    total_pages = 0
    error_pages = 0

    for folder in pdf_dirs:
        pdf_name = folder.name
        png_files = sorted(folder.glob("*.png"))

        if not png_files:
            print(f"  [{pdf_name}] PNG が見つかりません。スキップ。")
            continue

        print(f"[{pdf_name}] {len(png_files)} ページを分類中...")

        for png_path in png_files:
            # ページ番号はファイル名 page_XXXX.png から取得
            try:
                page_num = int(png_path.stem.split("_")[-1])
            except ValueError:
                page_num = 0

            row = process_page(pdf_name, page_num, png_path)
            all_rows.append(row)
            total_pages += 1

            if row["classification"] == "unreadable" and row["confidence"] == 0.0:
                error_pages += 1

        # フォルダ単位のサマリ表示
        cls_counts: dict[str, int] = {}
        for r in all_rows:
            if r["pdf_file"] == pdf_name:
                cls_counts[r["classification"]] = cls_counts.get(r["classification"], 0) + 1
        for cls, cnt in sorted(cls_counts.items()):
            print(f"  {cls:<35} {cnt:>4} ページ")
        print()

    # CSV 書き出し
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)

    print("=" * 60)
    print(f"完了 — 合計 {total_pages} ページ分類済み（エラー: {error_pages} ページ）")
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
