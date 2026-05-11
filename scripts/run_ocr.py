"""
run_ocr.py
==========
UAP公開文書 翻訳・要約プロジェクト — OCR実行ツール

目的:
    page_classification.csv と text_layer_report.csv を参照し、
    OCR対象ページについて Tesseract で本文抽出を行い、
    extracted_text/ocr_results.csv を生成する。

OCR対象:
    - ocr_needed = true（テキストレイヤーなし）
    - classification が typed_text / mixed_annotation / newspaper_or_print_clipping

OCR非対象:
    - handwritten（通常OCRでは精度が低いため）
    - image_or_photo（文字抽出ではなく画像説明が必要）
    - unreadable（判読不能）

このフェーズでは OCR精度100%より
「どのページでOCRが破綻するか」を把握することを優先する。

実行方法:
    python3 scripts/run_ocr.py

必要ライブラリ:
    brew install tesseract      # Tesseract OCRエンジン
    pip3 install pytesseract pillow
"""

import csv
import re
import sys
import time
import traceback
from pathlib import Path

# --- 依存ライブラリ確認 ---
try:
    import pytesseract
    from pytesseract import Output
    from PIL import Image
except ImportError as e:
    print("=" * 60)
    print(f"[エラー] 必要なライブラリが不足しています: {e}")
    print("  pip3 install pytesseract pillow")
    print("=" * 60)
    sys.exit(1)

# --- Tesseract バイナリ確認 ---
try:
    pytesseract.get_tesseract_version()
except pytesseract.TesseractNotFoundError:
    print("=" * 60)
    print("[エラー] Tesseract が見つかりません。")
    print("  brew install tesseract")
    print("=" * 60)
    sys.exit(1)

# -------------------------------------------------------
# パス設定
# -------------------------------------------------------
PROJECT_ROOT      = Path(__file__).resolve().parent.parent
PAGE_IMG_DIR      = PROJECT_ROOT / "page_images"
CLASSIFICATION_CSV = PROJECT_ROOT / "classification" / "page_classification.csv"
TEXT_LAYER_CSV    = PROJECT_ROOT / "metadata" / "text_layer_report.csv"
EXTRACTED_DIR     = PROJECT_ROOT / "extracted_text"
OUTPUT_CSV        = EXTRACTED_DIR / "ocr_results.csv"

# -------------------------------------------------------
# OCR設定
# -------------------------------------------------------

# Tesseract 言語（英語）
LANG = "eng"

# ページ分類ごとの Tesseract PSM（ページ分割モード）
# PSM 3 = 完全自動（デフォルト）
# PSM 4 = 1列の可変サイズテキストと仮定
PSM_MAP = {
    "typed_text":                  3,   # タイプ文書: 自動
    "mixed_annotation":            3,   # タイプ+注釈混在: 自動
    "newspaper_or_print_clipping": 4,   # 段組: 1列モード
}

# 低信頼度と見なす閾値（0〜100）
CONFIDENCE_LOW_THRESHOLD   = 40.0
CONFIDENCE_MID_THRESHOLD   = 60.0

# 抽出文字数が少ない場合に review 推奨する閾値
CHAR_COUNT_MIN = 30

# CSVに保存するテキストの最大文字数（長大テキストをCSVに収める）
TEXT_SAMPLE_MAX = 2000

# -------------------------------------------------------
# OCR除外カテゴリ（明確にスキップ）
# -------------------------------------------------------
OCR_SKIP_CLASSIFICATIONS = {"handwritten", "image_or_photo", "unreadable"}

# OCR実行対象アクション
OCR_TARGET_ACTIONS = {"run_ocr", "try_ocr", "try_layout_ocr"}

# -------------------------------------------------------
# テキスト前処理
# -------------------------------------------------------

def clean_ocr_text(raw: str) -> str:
    """OCR結果の生テキストを整形する。"""
    # 制御文字除去（改行・タブは保持）
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", raw)
    # 3行以上の連続空行を2行に圧縮
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def truncate(text: str, max_chars: int = TEXT_SAMPLE_MAX) -> str:
    """テキストを max_chars に丸める。"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "…[truncated]"


# -------------------------------------------------------
# 信頼度スコア計算
# -------------------------------------------------------

def get_confidence(img: Image.Image, psm: int) -> float:
    """
    Tesseract の word-level confidence を平均して返す（0.0〜100.0）。
    信頼度を取得できない場合は -1.0 を返す。
    """
    try:
        config = f"--psm {psm} -l {LANG}"
        data = pytesseract.image_to_data(img, config=config, output_type=Output.DICT)
        confs = [int(c) for c in data["conf"] if str(c).lstrip("-").isdigit() and int(c) >= 0]
        if not confs:
            return -1.0
        return round(sum(confs) / len(confs), 1)
    except Exception:
        return -1.0


# -------------------------------------------------------
# 1ページの OCR 実行
# -------------------------------------------------------

def run_ocr_page(img_path: Path, classification: str, cls_review: str) -> dict:
    """
    1ページに OCR を実行して結果 dict を返す。
    エラーが起きても記録して継続。
    """
    psm = PSM_MAP.get(classification, 3)

    try:
        img  = Image.open(str(img_path))
        config = f"--psm {psm} -l {LANG}"

        raw_text = pytesseract.image_to_string(img, config=config)
        text     = clean_ocr_text(raw_text)
        char_count = len(text)

        confidence = get_confidence(img, psm)

        # review_required 判定
        # ① 分類段階で review 推奨されていたなら引き継ぐ
        # ② 信頼度が低い
        # ③ 抽出文字数が極端に少ない
        # ④ newspaper は常に review
        review = cls_review == "true"
        if confidence >= 0 and confidence < CONFIDENCE_LOW_THRESHOLD:
            review = True
        if char_count < CHAR_COUNT_MIN:
            review = True
        if classification == "newspaper_or_print_clipping":
            review = True

        # reason 決定
        if confidence < 0:
            reason = f"OCR completed, confidence unavailable, {char_count} chars"
        elif confidence < CONFIDENCE_LOW_THRESHOLD:
            reason = f"low confidence ({confidence:.1f}/100), may contain noise or degraded scan"
        elif confidence < CONFIDENCE_MID_THRESHOLD:
            reason = f"medium confidence ({confidence:.1f}/100), review recommended for mixed pages"
        else:
            reason = f"confidence {confidence:.1f}/100, extraction likely reliable"

        notes = f"psm={psm} lang={LANG}"
        if classification == "newspaper_or_print_clipping":
            notes += "; layout OCR may have column ordering issues"
        if char_count < CHAR_COUNT_MIN:
            notes += f"; very short extraction ({char_count} chars), possible blank or image-only page"

        return {
            "ocr_engine":          f"tesseract-{pytesseract.get_tesseract_version()}",
            "extracted_text":      truncate(text),
            "extracted_char_count": char_count,
            "confidence_estimate": confidence if confidence >= 0 else "n/a",
            "review_required":     "true" if review else "false",
            "reason":              reason,
            "notes":               notes,
            "error":               "",
        }

    except Exception as e:
        return {
            "ocr_engine":          "tesseract",
            "extracted_text":      "",
            "extracted_char_count": 0,
            "confidence_estimate": "n/a",
            "review_required":     "true",
            "reason":              f"OCR failed: {e}",
            "notes":               f"psm={psm} lang={LANG}; error during processing",
            "error":               str(e),
        }


# -------------------------------------------------------
# CSV ロード
# -------------------------------------------------------

def load_classification_csv() -> dict[tuple[str, int], dict]:
    """page_classification.csv を (pdf_stem, page_num) キーの dict に変換。"""
    rows = {}
    with open(CLASSIFICATION_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = (r["pdf_file"], int(r["page_number"]))
            rows[key] = r
    return rows


def load_text_layer_csv() -> dict[tuple[str, int], dict]:
    """
    text_layer_report.csv を (pdf_stem, page_num) キーの dict に変換。
    pdf_file 列には .pdf 拡張子が含まれているため除去してキーに使う。
    """
    rows = {}
    with open(TEXT_LAYER_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            stem = Path(r["pdf_file"]).stem
            key  = (stem, int(r["page_number"]))
            rows[key] = r
    return rows


# -------------------------------------------------------
# OCR対象ページの選定
# -------------------------------------------------------

def select_ocr_targets(cls_rows: dict, tl_rows: dict) -> list[dict]:
    """
    2つのCSVを結合し、OCR対象ページのリストを返す。
    """
    targets = []

    for key, cls in cls_rows.items():
        classification    = cls["classification"]
        processing_action = cls["processing_action"]

        # 明確スキップ
        if classification in OCR_SKIP_CLASSIFICATIONS:
            continue

        # processing_action が OCR対象でない
        if processing_action not in OCR_TARGET_ACTIONS:
            continue

        # text_layer_report と結合（ocr_needed 確認）
        tl = tl_rows.get(key, {})
        ocr_needed = tl.get("ocr_needed", "true")  # 不明なら要OCRとして扱う
        if ocr_needed == "false":
            continue

        targets.append({
            "pdf_stem":          key[0],
            "page_number":       key[1],
            "image_file":        cls["image_file"],
            "classification":    classification,
            "processing_action": processing_action,
            "cls_review":        cls["review_required"],
        })

    # ページ番号順にソート
    targets.sort(key=lambda x: (x["pdf_stem"], x["page_number"]))
    return targets


# -------------------------------------------------------
# メイン処理
# -------------------------------------------------------

CSV_FIELDS = [
    "pdf_file", "page_number", "image_file",
    "classification", "ocr_engine",
    "extracted_text", "extracted_char_count",
    "confidence_estimate", "review_required",
    "reason", "notes",
]


def main():
    print("=" * 60)
    print("OCR実行ツール（UAP_TRANSLATION_PROJECT）")
    print("=" * 60)
    print(f"  分類CSV   : {CLASSIFICATION_CSV}")
    print(f"  テキスト検出: {TEXT_LAYER_CSV}")
    print(f"  出力先    : {OUTPUT_CSV}")
    print()

    for path, label in [(CLASSIFICATION_CSV, "page_classification.csv"),
                         (TEXT_LAYER_CSV, "text_layer_report.csv")]:
        if not path.exists():
            print(f"[エラー] {label} が見つかりません: {path}")
            sys.exit(1)

    cls_rows = load_classification_csv()
    tl_rows  = load_text_layer_csv()

    targets = select_ocr_targets(cls_rows, tl_rows)

    if not targets:
        print("[情報] OCR対象ページが0件でした。処理を終了します。")
        sys.exit(0)

    # スキップ数の表示（非対象分類）
    total_pages = len(cls_rows)
    skipped = total_pages - len(targets)
    print(f"全ページ        : {total_pages}")
    print(f"OCR対象         : {len(targets)}")
    print(f"スキップ(非対象): {skipped}  "
          f"(handwritten / image_or_photo / unreadable / text layer あり)")
    print()

    # 対象内訳
    from collections import Counter
    cls_cnt = Counter(t["classification"] for t in targets)
    print("対象内訳:")
    for cls, cnt in sorted(cls_cnt.items()):
        print(f"  {cls:<35} {cnt:>4} ページ")
    print()

    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    # 既存CSVがあれば読み込んで差分スキップ
    done_keys: set[tuple[str, int]] = set()
    existing_rows: list[dict] = []
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                done_keys.add((r["pdf_file"], int(r["page_number"])))
                existing_rows.append(r)
        print(f"[再実行] 既処理 {len(done_keys)} ページをスキップします。")
        print()

    new_rows:     list[dict] = []
    success_count = 0
    review_count  = 0
    error_count   = 0

    start_all = time.time()

    for idx, target in enumerate(targets, start=1):
        pdf_stem   = target["pdf_stem"]
        page_num   = target["page_number"]
        image_file = target["image_file"]
        cls        = target["classification"]

        # 差分スキップ
        if (pdf_stem, page_num) in done_keys:
            continue

        img_path = PAGE_IMG_DIR / pdf_stem / image_file
        if not img_path.exists():
            print(f"  [警告] 画像が見つかりません: {img_path}")
            error_count += 1
            continue

        # 進捗表示
        elapsed = time.time() - start_all
        remain  = len(targets) - idx
        eta_str = ""
        if idx > 1 and remain > 0:
            avg_sec = elapsed / (idx - 1)
            eta = int(avg_sec * remain)
            eta_str = f"  ETA ~{eta}s"
        print(f"[{idx:>4}/{len(targets)}] p.{page_num:>4}  {cls:<30}{eta_str}")

        ocr_result = run_ocr_page(img_path, cls, target["cls_review"])

        if ocr_result["error"]:
            print(f"          -> OCR失敗: {ocr_result['error']}")
            error_count += 1
        else:
            conf = ocr_result["confidence_estimate"]
            print(f"          -> {ocr_result['extracted_char_count']:>5}字  "
                  f"conf={conf}  review={ocr_result['review_required']}")
            success_count += 1

        if ocr_result["review_required"] == "true":
            review_count += 1

        row = {
            "pdf_file":             pdf_stem,
            "page_number":          page_num,
            "image_file":           image_file,
            "classification":       cls,
            "ocr_engine":           ocr_result["ocr_engine"],
            "extracted_text":       ocr_result["extracted_text"],
            "extracted_char_count": ocr_result["extracted_char_count"],
            "confidence_estimate":  ocr_result["confidence_estimate"],
            "review_required":      ocr_result["review_required"],
            "reason":               ocr_result["reason"],
            "notes":                ocr_result["notes"],
        }
        new_rows.append(row)

    # 既存 + 新規をマージして書き出し
    all_rows = existing_rows + new_rows
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)

    elapsed_total = int(time.time() - start_all)
    print()
    print("=" * 60)
    print(f"処理完了 — {elapsed_total}秒")
    print(f"  成功        : {success_count} ページ")
    print(f"  エラー      : {error_count} ページ")
    print(f"  要レビュー  : {review_count} ページ")
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
