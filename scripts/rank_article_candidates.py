"""
rank_article_candidates.py
==========================
UAP公開文書 翻訳・要約プロジェクト — 記事化候補ランキングツール

目的:
    取得済みWAR.GOV/UFO公開文書の中から、
    速報版・詳細版の記事化候補を抽出し優先順位を付ける。

    このツールは翻訳・要約ではなく、
    「どの文書から記事化すべきか」を判断するための入口処理。

recommended_lane:
    breaking  — 速報版向き。日本関連・時事性・話題性を優先。
    detailed  — 詳細版向き。公開順・資料整理・原文対訳向き。
    hold      — OCR困難・判読困難・記事化優先度が低いもの。

実行方法:
    python3 scripts/rank_article_candidates.py

必要ライブラリ:
    pip3 install pymupdf
"""

import csv
import re
import sys
import traceback
from pathlib import Path

try:
    import fitz  # PyMuPDF（ページ数取得用）
except ImportError:
    print("[エラー] PyMuPDF が必要です: pip3 install pymupdf")
    sys.exit(1)

# -------------------------------------------------------
# パス設定
# -------------------------------------------------------
PROJECT_ROOT     = Path(__file__).resolve().parent.parent
RAW_PDF_DIR      = PROJECT_ROOT / "raw_pdf"
METADATA_DIR     = PROJECT_ROOT / "metadata"
CATALOG_CSV      = METADATA_DIR / "files_catalog.csv"
CLASSIFICATION_CSV = PROJECT_ROOT / "classification" / "page_classification.csv"
OCR_CSV          = PROJECT_ROOT / "extracted_text" / "ocr_results.csv"
OUTPUT_CSV       = METADATA_DIR / "article_candidates.csv"

# -------------------------------------------------------
# スコアリング定数
# -------------------------------------------------------

# 日本関連キーワード（小文字で比較）
JAPAN_BASE_KW = ["japan", "japanese", "nippon", "nihon"]
JAPAN_BASE_SCORE = 30

JAPAN_BASE_SCORE = 30  # japan/japanese 一致
JAPAN_BASE_KW = ["japan", "japanese", "nippon", "nihon"]

JAPAN_MILIT_KW = ["okinawa", "kadena", "yokota", "misawa", "ryukyu"]
JAPAN_MILIT_SCORE = 40  # 在日米軍基地直接言及

PACIFIC_KW = ["pacific", "east asia", "asia", "far east", "sea of japan", "japan sea", "indo-pacific"]
PACIFIC_SCORE = 20  # 広域太平洋・東アジア関連

# 地名（incident_location）での日本関連
JAPAN_LOCATION_KW = ["japan", "okinawa", "pacific", "east asia"]
JAPAN_LOCATION_SCORE = 30

# Agency ボーナス
AGENCY_SCORE = {
    "FBI":                 10,
    "NASA":                10,
    "Department of War":    5,
    "Department of State":  5,
}

# ファイル名シグナルによるボーナス
FILENAME_SIGNALS = [
    # (正規表現パターン, スコア, 理由)
    (r"composite.sketch",          +45, "eyewitness sketch — high visual public interest"),
    (r"slides?[_\-]",              +35, "visual presentation slides"),
    (r"[_\-]slides?\.",            +35, "visual presentation slides"),
    (r"usper.statement",           +30, "eyewitness personal statement"),
    (r"press.release|[_\-]pr\d",   +20, "official press release"),
    (r"apollo",                    +25, "NASA Apollo mission — high public interest"),
    (r"crew.debriefing|debriefing",+15, "crew debrief transcript"),
    (r"transcript",                +12, "verbatim transcript"),
    (r"email.correspondence|email",+8,  "email correspondence chain"),
    (r"cable",                     +10, "State Dept diplomatic cable"),
    (r"mission.report",            +10, "specific mission report"),
    (r"range.fouler",              +15, "aerial near-miss debrief"),
    (r"launch.summary",            +10, "launch incident summary"),
    (r"news|clipping",             -10, "newspaper/clipping — layout OCR risk"),
    (r"serial_",                   -5,  "serial (part of large multi-section file)"),
    (r"section_",                  -5,  "section (part of large multi-section file)"),
    (r"sub_a",                     -5,  "sub-file of large case"),
]

# ページ数ボーナス（短い = 処理しやすい）
def page_score(n: int) -> tuple[int, str]:
    if n <= 0:   return 0,    "page count unknown"
    if n <= 5:   return +10,  f"{n}p: very short, quick to process"
    if n <= 20:  return +5,   f"{n}p: short document"
    if n <= 50:  return 0,    f"{n}p: medium length"
    if n <= 200: return -5,   f"{n}p: long document"
    return -10,  f"{n}p: very long document"

# OCR有効データがある場合のボーナス
OCR_DATA_SCORE    = +5   # OCRデータが存在
OCR_SUCCESS_SCORE = +10  # OCR成功率 70%以上
OCR_REVIEW_SCORE  = +5   # review_required が50%未満

# 高 unreadable ページペナルティ
UNREADABLE_PENALTY  = -20   # unreadable ページが20%超え
NEWSPAPER_PENALTY   = -10   # newspaper ページが30%超え

# 時事性ボーナス（インシデント年が近い）
RECENT_YEAR_SCORE   = +10   # 2015年以降
MODERN_YEAR_SCORE   = +15   # 2020年以降

# スコアによるレーン割り当て
LANE_BREAKING  = 50   # ≥ LANE_BREAKING → breaking
LANE_DETAILED  = 20   # ≥ LANE_DETAILED  → detailed
# < LANE_DETAILED → hold

# -------------------------------------------------------
# CSVロード
# -------------------------------------------------------

def load_catalog() -> list[dict]:
    return [r for r in csv.DictReader(open(CATALOG_CSV, encoding="utf-8"))
            if r["file_type"] == "PDF" and r["downloaded"] == "true"]


def load_classification() -> dict[str, list[dict]]:
    """pdf_file → ページ行リスト"""
    data: dict[str, list[dict]] = {}
    if not CLASSIFICATION_CSV.exists():
        return data
    for r in csv.DictReader(open(CLASSIFICATION_CSV, encoding="utf-8")):
        data.setdefault(r["pdf_file"], []).append(r)
    return data


def load_ocr() -> dict[str, list[dict]]:
    """pdf_file → OCR行リスト"""
    data: dict[str, list[dict]] = {}
    if not OCR_CSV.exists():
        return data
    for r in csv.DictReader(open(OCR_CSV, encoding="utf-8")):
        data.setdefault(r["pdf_file"], []).append(r)
    return data


# -------------------------------------------------------
# ページ数取得（PyMuPDF）
# -------------------------------------------------------

def get_page_count(pdf_path: Path) -> int:
    try:
        doc = fitz.open(str(pdf_path))
        n = len(doc)
        doc.close()
        return n
    except Exception:
        return -1


# -------------------------------------------------------
# キーワード検出
# -------------------------------------------------------

def detect_japan_keywords(text: str) -> list[str]:
    """テキストから日本関連キーワードを検出して返す。"""
    t = text.lower()
    found = []
    for kw in JAPAN_MILIT_KW:
        if kw in t:
            found.append(kw)
    for kw in JAPAN_BASE_KW:
        if kw in t and kw not in found:
            found.append(kw)
    for kw in PACIFIC_KW:
        if kw in t and kw not in found:
            found.append(kw)
    return found


# -------------------------------------------------------
# 時事性スコア（incident_date / ファイル名から年を推定）
# -------------------------------------------------------

def recency_score(catalog_row: dict, filename: str) -> tuple[int, str]:
    # incident_dateから年を取得
    raw = catalog_row.get("incident_date", "") or ""
    year_match = re.search(r"(19|20)(\d{2})", raw)
    if not year_match:
        # ファイル名から年を推定
        year_match = re.search(r"(19|20)(\d{2})", filename)

    if not year_match:
        return 0, ""

    year = int(year_match.group(0))
    if year >= 2020:
        return MODERN_YEAR_SCORE,  f"recent incident ({year})"
    if year >= 2015:
        return RECENT_YEAR_SCORE,  f"modern incident ({year})"
    return 0, ""


# -------------------------------------------------------
# 1ファイルのスコアリング
# -------------------------------------------------------

def score_pdf(cat: dict, cls_pages: list[dict], ocr_pages: list[dict],
              page_count: int) -> dict:
    """
    1PDF について全シグナルを集計してスコアと理由を返す。
    """
    filename = cat["file_name"].lower()
    agency   = cat.get("agency", "")
    location = cat.get("incident_location", "") or ""

    score    = 0
    reasons  = []
    notes    = []

    # --- Agency ボーナス ---
    ag_bonus = AGENCY_SCORE.get(agency, 0)
    if ag_bonus:
        score += ag_bonus
        reasons.append(f"agency={agency}(+{ag_bonus})")

    # --- ファイル名シグナル ---
    for pattern, pts, label in FILENAME_SIGNALS:
        if re.search(pattern, filename, re.I):
            score += pts
            reasons.append(f"{label}({'+'if pts>=0 else ''}{pts})")

    # --- 日本関連キーワード（ファイル名 + location） ---
    search_text = filename + " " + location.lower()
    kw_hits = detect_japan_keywords(search_text)

    # OCRテキストがある場合も検索
    ocr_kw_hits = []
    if ocr_pages:
        ocr_full = " ".join(r.get("extracted_text","") for r in ocr_pages[:30])
        ocr_kw_hits = detect_japan_keywords(ocr_full)
        for kw in ocr_kw_hits:
            if kw not in kw_hits:
                kw_hits.append(kw)

    japan_related = "true" if kw_hits else "false"

    # キーワード別スコア加算
    milit_hits  = [k for k in kw_hits if k in JAPAN_MILIT_KW]
    base_hits   = [k for k in kw_hits if k in JAPAN_BASE_KW and k not in milit_hits]
    pacific_hits = [k for k in kw_hits if k in PACIFIC_KW and k not in milit_hits and k not in base_hits]
    loc_hits    = [k for k in kw_hits if k in JAPAN_LOCATION_KW and location]

    if milit_hits:
        score += JAPAN_MILIT_SCORE
        reasons.append(f"Japan_military_base({','.join(milit_hits)})+{JAPAN_MILIT_SCORE}")
    if base_hits:
        score += JAPAN_BASE_SCORE
        reasons.append(f"Japan_keyword({','.join(base_hits)})+{JAPAN_BASE_SCORE}")
    if pacific_hits and not base_hits and not milit_hits:
        score += PACIFIC_SCORE
        reasons.append(f"Pacific_keyword({','.join(pacific_hits)})+{PACIFIC_SCORE}")
    if location and any(k in location.lower() for k in JAPAN_LOCATION_KW):
        score += JAPAN_LOCATION_SCORE
        reasons.append(f"Japan_location({location})+{JAPAN_LOCATION_SCORE}")

    # --- ページ数ボーナス ---
    pg_bonus, pg_note = page_score(page_count)
    score += pg_bonus
    if pg_bonus != 0 or page_count > 0:
        reasons.append(f"{pg_note}({'+'if pg_bonus>=0 else ''}{pg_bonus})")

    # --- 時事性 ---
    rec_bonus, rec_note = recency_score(cat, filename)
    score += rec_bonus
    if rec_note:
        reasons.append(f"{rec_note}(+{rec_bonus})")

    # --- 分類データがある場合 ---
    ocr_success_rate     = ""
    review_required_count = 0

    if cls_pages:
        total_cls = len(cls_pages)
        unreadable = sum(1 for p in cls_pages if p["classification"] == "unreadable")
        newspaper  = sum(1 for p in cls_pages if p["classification"] == "newspaper_or_print_clipping")

        unreadable_ratio = unreadable / total_cls
        newspaper_ratio  = newspaper / total_cls

        if unreadable_ratio > 0.20:
            score += UNREADABLE_PENALTY
            reasons.append(f"high_unreadable({unreadable_ratio:.0%}){UNREADABLE_PENALTY}")
        if newspaper_ratio > 0.30:
            score += NEWSPAPER_PENALTY
            reasons.append(f"high_newspaper({newspaper_ratio:.0%}){NEWSPAPER_PENALTY}")

    if ocr_pages:
        score += OCR_DATA_SCORE
        reasons.append(f"ocr_data_available(+{OCR_DATA_SCORE})")

        total_ocr     = len(ocr_pages)
        success_pages = sum(1 for p in ocr_pages if int(p.get("extracted_char_count",0)) >= 100)
        review_pages  = sum(1 for p in ocr_pages if p.get("review_required","") == "true")
        review_required_count = review_pages

        success_rate = success_pages / total_ocr if total_ocr else 0
        ocr_success_rate = f"{success_rate:.0%}"

        if success_rate >= 0.70:
            score += OCR_SUCCESS_SCORE
            reasons.append(f"ocr_success_rate={ocr_success_rate}(+{OCR_SUCCESS_SCORE})")

        review_ratio = review_pages / total_ocr if total_ocr else 1
        if review_ratio < 0.50:
            score += OCR_REVIEW_SCORE
            reasons.append(f"low_review_required({review_ratio:.0%})(+{OCR_REVIEW_SCORE})")
        else:
            notes.append(f"high_review_required={review_ratio:.0%}")

    # --- レーン決定 ---
    if score >= LANE_BREAKING:
        lane = "breaking"
    elif score >= LANE_DETAILED:
        lane = "detailed"
    else:
        lane = "hold"

    return {
        "page_count":           page_count if page_count > 0 else "",
        "ocr_success_rate":     ocr_success_rate,
        "review_required_count": review_required_count,
        "japan_related":        japan_related,
        "japan_keywords":       ",".join(kw_hits),
        "candidate_score":      score,
        "recommended_lane":     lane,
        "reasons":              " | ".join(reasons),
        "notes":                " | ".join(notes),
    }


# -------------------------------------------------------
# メイン処理
# -------------------------------------------------------

CSV_FIELDS = [
    "file_name", "agency", "release_date", "incident_date", "incident_location",
    "file_type", "page_count", "ocr_success_rate", "review_required_count",
    "japan_related", "japan_keywords", "candidate_score", "recommended_lane",
    "reasons", "notes",
]


def main():
    print("=" * 60)
    print("記事化候補ランキングツール（UAP_TRANSLATION_PROJECT）")
    print("=" * 60)

    for path, label in [(CATALOG_CSV, "files_catalog.csv")]:
        if not path.exists():
            print(f"[エラー] {label} が見つかりません: {path}")
            sys.exit(1)

    catalog   = load_catalog()
    cls_data  = load_classification()
    ocr_data  = load_ocr()

    print(f"  PDF（取得済み）: {len(catalog)} 件")
    print(f"  分類データあり : {len(cls_data)} PDF")
    print(f"  OCRデータあり  : {len(ocr_data)} PDF")
    print()

    all_rows = []

    for i, cat in enumerate(catalog, 1):
        filename = cat["file_name"]
        stem     = Path(filename).stem  # 拡張子なし

        # page_classification / ocr_results との照合（stemで照合）
        cls_pages = cls_data.get(stem, [])
        ocr_pages = ocr_data.get(stem, [])

        # ページ数取得
        pdf_path   = RAW_PDF_DIR / filename
        page_count = get_page_count(pdf_path) if pdf_path.exists() else -1

        # スコアリング
        scored = score_pdf(cat, cls_pages, ocr_pages, page_count)

        row = {
            "file_name":          filename,
            "agency":             cat.get("agency", ""),
            "release_date":       cat.get("release_date", ""),
            "incident_date":      cat.get("incident_date", ""),
            "incident_location":  cat.get("incident_location", ""),
            "file_type":          cat.get("file_type", "PDF"),
        }
        row.update(scored)
        all_rows.append(row)

    # スコア降順でソート
    all_rows.sort(key=lambda r: (-int(r["candidate_score"]), r["file_name"]))

    # CSV 書き出し
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)

    # サマリ表示
    breaking = [r for r in all_rows if r["recommended_lane"] == "breaking"]
    detailed = [r for r in all_rows if r["recommended_lane"] == "detailed"]
    hold     = [r for r in all_rows if r["recommended_lane"] == "hold"]
    japan    = [r for r in all_rows if r["japan_related"] == "true"]

    print(f"=== ランキング結果 ===")
    print(f"  breaking : {len(breaking)} 件")
    print(f"  detailed : {len(detailed)} 件")
    print(f"  hold     : {len(hold)} 件")
    print(f"  日本関連 : {len(japan)} 件")
    print()

    print("=== breaking 上位10件 ===")
    for r in breaking[:10]:
        print(f"  [{r['candidate_score']:>3}] {r['file_name'][:55]:<55} {r['agency']}")

    print()
    print("=== 日本関連候補 ===")
    for r in japan:
        print(f"  [{r['candidate_score']:>3}] [{r['recommended_lane']:<9}] "
              f"{r['file_name'][:50]}  kw={r['japan_keywords']}")

    print()
    print(f"CSV 出力: {OUTPUT_CSV}  ({len(all_rows)} 件)")
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
