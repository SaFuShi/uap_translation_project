"""
classify_pages.py  v2
=====================
UAP公開文書 翻訳・要約プロジェクト — ページ仮分類ツール（v2改善版）

変更履歴:
    v1: 初期実装。特徴量ベースの仮分類。
    v2: OCR failure pattern フィードバックをもとに routing 精度を改善。
        - typed_text 判定条件を厳格化（edge閾値 0.05→0.08）
        - 低エッジ+高白ページを admin_or_cover へ（0字誤分類対策）
        - 高エッジ+低白+高std を image_or_photo へ（図版誤分類対策）
        - aged paper typed_text 条件を追加
        - 中エッジ帯を typed_text ではなく mixed_annotation へ
        - ocr_results.csv が存在する場合は OCR failure を review_required に格上げ

目的:
    page_images/ 配下の PNG を読み取り、
    OCR・翻訳処理へ進めるための仮分類と処理ルート (routing) を
    classification/page_classification.csv へ出力する。

非対象:
    OCR・翻訳・要約・note整形・外部APIへの送信・AI Vision分類

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
PROJECT_ROOT       = Path(__file__).resolve().parent.parent
PAGE_IMG_DIR       = PROJECT_ROOT / "page_images"
CLASSIFICATION_DIR = PROJECT_ROOT / "classification"
OUTPUT_CSV         = CLASSIFICATION_DIR / "page_classification.csv"
OCR_RESULTS_CSV    = PROJECT_ROOT / "extracted_text" / "ocr_results.csv"

# 分類器バージョン（notes に埋め込む）
CLASSIFIER_VERSION = "v2"

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
# OCR フィードバックのロード（v2追加）
# -------------------------------------------------------

def load_ocr_feedback() -> dict:
    """
    ocr_results.csv が存在すれば読み込み、
    (pdf_stem, page_num) → {"chars": int, "conf": float, "failed": bool}
    の辞書を返す。

    failed = True の条件:
      - extracted_char_count == 0
      - または confidence_estimate < 40 かつ extracted_char_count < 50

    存在しない場合は空辞書を返す（初回実行時）。
    """
    if not OCR_RESULTS_CSV.exists():
        return {}

    feedback = {}
    with open(OCR_RESULTS_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pdf_stem = row["pdf_file"]
            page_num = int(row["page_number"])
            chars    = int(row["extracted_char_count"])
            conf_raw = row["confidence_estimate"]
            conf     = float(conf_raw) if conf_raw not in ("n/a", "") else 95.0

            # 失敗判定: 0字、または低信頼+少文字
            failed = (chars == 0) or (conf < 40.0 and chars < 50)

            feedback[(pdf_stem, page_num)] = {
                "chars":  chars,
                "conf":   conf,
                "failed": failed,
            }
    return feedback


# -------------------------------------------------------
# 仮分類ロジック v2
# -------------------------------------------------------

def classify(features: dict, page_num: int) -> tuple[str, float, str]:
    """
    特徴量から分類カテゴリ・信頼度・理由を返す（v2改善版）。

    v2 主要変更点:
      - typed_text の edge 閾値を 0.05 → 0.08 に引き上げ（誤分類削減）
      - 低エッジ+高白ページを admin_or_cover へ（sparse content対策）
      - 高エッジ+低白+高std を image_or_photo へ（図版誤分類対策）
      - aged paper typed_text 条件を追加（白割合 0.62〜0.72 + 高エッジ）
      - 中エッジ帯（0.03〜0.07）を typed_text でなく mixed_annotation に

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

    # --- 2. スパースコンテンツ → 表紙・管理票・区切りページ ---
    # v2: 条件を大幅拡張。低エッジ+高白 = 内容が乏しいページ
    # OCR結果で確認: このパターンが typed_text 0字誤分類の主因
    if e < 0.025 and w > 0.75:
        return "admin_or_cover", 0.65, "very low edge density on white page; sparse content, likely cover or separator"
    if w > 0.96 and e < 0.04:
        return "admin_or_cover", 0.65, "near-blank page, likely cover or separator"

    # --- 3. 写真・図版中心 ---
    # v1: s > 62 and e < 0.07 and w < 0.62
    # v2-追加: 高エッジ + 低白 + 高std → 図版・グラフィック（p.117 対策）
    #   e > 0.12, w < 0.68, s > 65 のページは文字でなく図版の可能性が高い
    if s > 62 and e < 0.07 and w < 0.62:
        return "image_or_photo", 0.65, "high tonal variance with low edge density, likely photo or figure"
    if e > 0.12 and w < 0.68 and s > 65 and d < 0.10:
        return "image_or_photo", 0.55, "high edge with low white ratio and high std; possibly diagram or graphic, not typed text"

    # --- 4. 横長ページ → 新聞・切り抜き候補 ---
    if ar > 1.3 and e > 0.04:
        return ("newspaper_or_print_clipping", 0.55,
                "landscape orientation with text edges, possibly newspaper clipping")

    # --- 5. typed_text（高白 + 高エッジ）★v2: edge閾値を厳格化 0.05→0.08★ ---
    # 根拠: edge >= 0.08 を持つページは OCR成功率が高い（実測）
    if w > 0.72 and e >= 0.08:
        if d > 0.05 and s > 45:
            # スタンプ・注釈混在の可能性
            return ("mixed_annotation", 0.55,
                    "typed text with notable dark regions, possibly stamps or handwritten annotations")
        return "typed_text", 0.75, "high white background with strong edge density; typed_text likely (v2 strict)"

    # --- 6. aged paper typed_text（白割合が低くても高エッジなら typed） ---
    # 古い黄ばんだ紙は white_ratio が低い（0.62〜0.72）が、
    # 文字がタイプされていれば edge_ratio は高くなる
    if 0.62 <= w <= 0.72 and e >= 0.08 and m > 100:
        if d > 0.05:
            return ("mixed_annotation", 0.55,
                    "aged paper with moderate white ratio and text edges; mixed annotation likely")
        return "typed_text", 0.65, "aged paper typed text; moderate white with strong edge density"

    # --- 7. 中エッジ帯（0.03〜0.07）→ v2: typed_text にしない ---
    # v1 ではこの帯域を typed_text にしていたが、OCR失敗の原因になった
    # v2 では mixed_annotation に寄せ、review_required で安全に処理する
    if e >= 0.03:
        if w > 0.72:
            # 高白 + 中エッジ
            if d > 0.05:
                return "mixed_annotation", 0.50, "moderate edges with notable dark pixels on white page; possibly mixed"
            return "mixed_annotation", 0.45, "moderate edge density on white page; uncertain, routing to review"
        if w > 0.55 and m > 110:
            return "mixed_annotation", 0.45, "moderate edges on medium-brightness page; possibly aged typed or mixed"
        if s > 38:
            return "mixed_annotation", 0.40, "moderate edges on non-white background; possibly mixed content"
        return "handwritten", 0.40, "low-to-moderate edges with non-white background; possibly handwritten"

    # --- 8. 低エッジ + 中程度の白 → v2: typed_text にしない（0字誤分類の根本原因）---
    # v1 では rule 7 で typed_text を返していたが、これが 0字誤分類の主因
    # v2 では admin_or_cover か mixed_annotation に寄せる
    if w > 0.60:
        return "admin_or_cover", 0.45, "low edge density; sparse or faint content, review recommended"

    # --- 9. 判断困難 → 混在扱い ---
    return "mixed_annotation", 0.30, "uncertain features, review recommended"


# -------------------------------------------------------
# 1ページ分の処理
# -------------------------------------------------------

def process_page(pdf_name: str, page_num: int, img_path: Path,
                 ocr_feedback: dict) -> dict:
    """
    1ページ分の特徴量抽出・分類・ルーティングを実行して dict を返す。
    エラーが起きても unreadable として記録する。

    ocr_feedback: load_ocr_feedback() で得た辞書。前回OCR失敗ページを
                  review_required に格上げするために使用する。
    """
    try:
        features = extract_features(img_path)
        cls, conf, reason = classify(features, page_num)
    except Exception as e:
        print(f"  [警告] {img_path.name} の処理に失敗: {e}")
        cls, conf, reason = "unreadable", 0.0, f"processing error: {e}"
        features = {"width": 0, "height": 0}

    ocr_rec, proc_action, review_req = ROUTING_TABLE[cls]

    # --- confidence が低い場合は review_required を強制 true ---
    if conf < 0.45 and review_req == "false":
        review_req = "true"

    # --- v2: OCR failure フィードバック ---
    # 前回 OCR で 0字 / 低信頼だったページは review_required に格上げ
    fb_note = ""
    fb = ocr_feedback.get((pdf_name, page_num))
    if fb and fb["failed"]:
        review_req = "true"
        fb_note = f" | ocr_feedback:failed(chars={fb['chars']},conf={fb['conf']:.1f})"

    notes = (
        f"cls={CLASSIFIER_VERSION} "
        f"w={features.get('width',0)} h={features.get('height',0)} "
        f"edge={features.get('edge_ratio', 0):.4f} "
        f"white={features.get('white_ratio', 0):.4f} "
        f"dark={features.get('dark_ratio', 0):.4f} "
        f"std={features.get('std_bright', 0):.2f}"
        f"{fb_note}"
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
    print(f"ページ仮分類ツール {CLASSIFIER_VERSION}（UAP_TRANSLATION_PROJECT）")
    print("=" * 60)
    print(f"  入力元 : {PAGE_IMG_DIR}")
    print(f"  出力先 : {OUTPUT_CSV}")
    print()

    if not PAGE_IMG_DIR.exists():
        print(f"[エラー] フォルダが見つかりません: {PAGE_IMG_DIR}")
        sys.exit(1)

    # OCR フィードバックをロード（存在しない場合は空辞書）
    ocr_feedback = load_ocr_feedback()
    if ocr_feedback:
        failed_count = sum(1 for v in ocr_feedback.values() if v["failed"])
        print(f"  OCR feedback: {len(ocr_feedback)} ページ読み込み済み "
              f"（うち失敗: {failed_count} ページ → review_required に格上げ）")
    else:
        print("  OCR feedback: なし（初回実行）")
    print()

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
        pdf_name  = folder.name
        png_files = sorted(folder.glob("*.png"))

        if not png_files:
            print(f"  [{pdf_name}] PNG が見つかりません。スキップ。")
            continue

        print(f"[{pdf_name}] {len(png_files)} ページを分類中...")

        for png_path in png_files:
            try:
                page_num = int(png_path.stem.split("_")[-1])
            except ValueError:
                page_num = 0

            row = process_page(pdf_name, page_num, png_path, ocr_feedback)
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

    # review_required 集計
    review_true  = sum(1 for r in all_rows if r["review_required"] == "true")
    review_false = sum(1 for r in all_rows if r["review_required"] == "false")

    print("=" * 60)
    print(f"完了 — 合計 {total_pages} ページ分類済み（エラー: {error_pages} ページ）")
    print(f"  review_required=true  : {review_true}")
    print(f"  review_required=false : {review_false}")
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
