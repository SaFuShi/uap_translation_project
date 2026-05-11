"""
rank_article_candidates.py
==========================
UAP公開文書 翻訳・要約プロジェクト — 記事化候補ランキングツール  v2

目的:
    取得済みWAR.GOV/UFO公開文書の中から、
    速報版・詳細版の記事化候補を抽出し優先順位を付ける。

    このツールは翻訳・要約ではなく、
    「どの文書から記事化すべきか」を判断するための入口処理。

recommended_lane:
    breaking  — 速報版向き。日本関連・時事性・話題性を優先。
    detailed  — 詳細版向き。公開順・資料整理・原文対訳向き。
    hold      — OCR困難・判読困難・記事化優先度が低いもの。

japan_signal_source:
    file_name         — ファイル名のみに Japan キーワードあり（弱いシグナル）
    incident_location — incident_location に Japan キーワードあり（強いシグナル）
    ocr_text          — OCR本文に Japan キーワードあり（強いシグナル）
    mixed             — 複数ソースで一致
    conflict          — ファイル名は Japan だが location/OCR は矛盾
    (空文字)          — Japan 関連シグナルなし

v2 変更点:
    - ファイル名のみの "japan" は弱いシグナル(+5)に降格
    - japan_related=true は location または OCR 本文で確認できた場合のみ
    - location が非日本地域かつファイル名に japan → conflict 検出・notes に警告
    - "Pacific Time Zone" 等の時間帯表記を地理的 Pacific と区別
    - japan_signal_source / location_conflict / location_conflict_reason を出力

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
# OCR本文 / incident_location に出現した場合のみ強いシグナルとして扱う
JAPAN_MILIT_KW    = ["okinawa", "kadena", "yokota", "misawa", "ryukyu"]
JAPAN_MILIT_SCORE = 40   # 在日米軍基地を直接言及（最強シグナル）

JAPAN_BASE_KW    = ["japan", "japanese", "nippon", "nihon", "tokyo"]
JAPAN_BASE_SCORE = 30    # Japan 国名・国民の言及

PACIFIC_KW    = ["pacific ocean", "pacific theater", "west pacific", "western pacific",
                 "east asia", "far east", "sea of japan", "japan sea",
                 "indo-pacific", "indopacom"]
PACIFIC_SCORE = 20       # 広域太平洋・東アジア（地理的に確実な表記のみ）

# ファイル名のみに日本キーワードがある場合の弱いシグナル
JAPAN_FILENAME_WEAK_KW    = ["japan", "japanese", "nippon", "nihon", "okinawa",
                              "kadena", "yokota", "misawa", "tokyo"]
JAPAN_FILENAME_WEAK_SCORE = +5  # 弱いシグナル（場所の裏付けなし）

# incident_location での日本関連判定
# ※ "Pacific Time Zone" 等の時間帯名は除外
JAPAN_LOCATION_KW    = ["japan", "okinawa", "kadena", "yokota", "misawa",
                         "pacific ocean", "east asia", "far east", "indo-pacific",
                         "ryukyu", "tokyo"]
JAPAN_LOCATION_SCORE = 30

# location が明示的に非日本地域であることを示すパターン
# ファイル名に Japan キーワードがあっても、これらが location に含まれれば conflict
NON_JAPAN_LOCATION_PATTERNS = [
    "arabian gulf", "persian gulf", "arabian sea", "gulf of aden", "gulf of oman",
    "red sea", "indian ocean",
    "iraq", "syria", "iran", "afghanistan", "kuwait", "bahrain", "qatar",
    "middle east",
    "mediterranean", "atlantic",
    "europe", "africa",
    "south america", "caribbean", "gulf of mexico",
    "united states", "western us", "eastern us", "conus",
]

# "Pacific Time Zone" 等の時間帯表記は地理的 Pacific と区別して除外
PACIFIC_TIMEZONE_PATTERNS = [
    "pacific time", "pacific standard time", "pacific daylight",
    "pacific time zone", "pst", "pdt",
]

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
# キーワード検出（3ソース分離版）
# -------------------------------------------------------

def _kw_hits(text_lower: str, kwlists: list[list[str]]) -> list[str]:
    """text_lower から複数リストのキーワードを検出してデdup返却する。"""
    found = []
    for kwlist in kwlists:
        for kw in kwlist:
            if kw in text_lower and kw not in found:
                found.append(kw)
    return found


def _location_is_pacific(location_lower: str) -> bool:
    """
    incident_location が地理的 Pacific / 東アジアを示すか判定する。
    "Pacific Time Zone" 等の時間帯表記は除外する。
    """
    # 時間帯表記が含まれている場合は地理的 Pacific ではない
    for tz in PACIFIC_TIMEZONE_PATTERNS:
        if tz in location_lower:
            return False
    for kw in JAPAN_LOCATION_KW:
        if kw in location_lower:
            return True
    return False


def detect_japan_signals(filename: str, location: str, ocr_text: str) -> dict:
    """
    ファイル名・incident_location・OCR本文の3ソースでJapan関連シグナルを検出する。

    Returns dict with keys:
        fn_kw          : list[str]  ファイル名で検出されたキーワード
        loc_kw         : list[str]  locationで検出されたキーワード
        ocr_kw         : list[str]  OCR本文で検出されたキーワード
        all_confirmed_kw: list[str] location/OCRで確認されたキーワード（弱シグナル除く）
        japan_related  : bool       location or OCR に根拠あり = True
        signal_source  : str        file_name / incident_location / ocr_text / mixed / conflict / ""
        location_conflict     : bool
        location_conflict_reason : str
    """
    fn_lower  = filename.lower()
    loc_lower = location.lower()
    ocr_lower = ocr_text.lower() if ocr_text else ""

    # ---- ファイル名キーワード ----
    fn_kw = []
    for kw in JAPAN_FILENAME_WEAK_KW:
        if kw in fn_lower and kw not in fn_kw:
            fn_kw.append(kw)

    # ---- location キーワード（タイムゾーン除外あり） ----
    loc_kw = []
    if _location_is_pacific(loc_lower):
        for kw in JAPAN_LOCATION_KW:
            if kw in loc_lower and kw not in loc_kw:
                loc_kw.append(kw)
    # location が "Pacific Ocean" 等の場合でも個別キーワードを収集
    for kw in JAPAN_LOCATION_KW:
        if kw in loc_lower and kw not in loc_kw:
            # タイムゾーン文脈でないことを確認
            is_tz = any(tz in loc_lower for tz in PACIFIC_TIMEZONE_PATTERNS)
            if not is_tz:
                loc_kw.append(kw)

    # ---- OCR本文キーワード ----
    ocr_kw = _kw_hits(ocr_lower, [JAPAN_MILIT_KW, JAPAN_BASE_KW, PACIFIC_KW])

    # ---- conflict 検出 ----
    # ファイル名に Japan キーワードがあるが、location が明示的に非日本地域
    location_conflict = False
    location_conflict_reason = ""

    if fn_kw and not loc_kw and not ocr_kw:
        for pat in NON_JAPAN_LOCATION_PATTERNS:
            if pat in loc_lower:
                location_conflict = True
                location_conflict_reason = (
                    f"filename has Japan keyword ({', '.join(fn_kw)}) "
                    f"but incident_location='{location}' indicates non-Japan area ({pat})"
                )
                break
        # "Pacific Time Zone" 等の偽陽性 Pacific
        if not location_conflict and fn_kw:
            for tz in PACIFIC_TIMEZONE_PATTERNS:
                if tz in loc_lower:
                    location_conflict = True
                    location_conflict_reason = (
                        f"filename has Japan keyword ({', '.join(fn_kw)}) "
                        f"but incident_location='{location}' is a timezone, not a geographic location"
                    )
                    break

    # ---- japan_related (confirmed 判定) ----
    # location または OCR で根拠があるときのみ True
    japan_related = bool(loc_kw) or bool(ocr_kw)

    # ---- signal_source 文字列 ----
    sources = []
    if fn_kw:  sources.append("file_name")
    if loc_kw: sources.append("incident_location")
    if ocr_kw: sources.append("ocr_text")

    if location_conflict:
        signal_source = "conflict"
    elif not sources:
        signal_source = ""
    elif len(sources) == 1:
        signal_source = sources[0]
    else:
        signal_source = "mixed"

    # 確認済みキーワード（location + OCR のみ）
    all_confirmed: list[str] = []
    for kw in loc_kw + ocr_kw:
        if kw not in all_confirmed:
            all_confirmed.append(kw)

    return {
        "fn_kw":                  fn_kw,
        "loc_kw":                 loc_kw,
        "ocr_kw":                 ocr_kw,
        "all_confirmed_kw":       all_confirmed,
        "japan_related":          japan_related,
        "signal_source":          signal_source,
        "location_conflict":      location_conflict,
        "location_conflict_reason": location_conflict_reason,
    }


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

    # --- 日本関連シグナル（3ソース分離） ---
    ocr_full = ""
    if ocr_pages:
        ocr_full = " ".join(r.get("extracted_text", "") for r in ocr_pages[:30])

    js = detect_japan_signals(filename, location, ocr_full)

    japan_related        = "true" if js["japan_related"] else "false"
    japan_signal_source  = js["signal_source"]
    location_conflict    = "true" if js["location_conflict"] else "false"
    location_conflict_reason = js["location_conflict_reason"]

    # conflict 警告を notes に追記
    if js["location_conflict"]:
        notes.append(f"LOCATION_CONFLICT: {js['location_conflict_reason']}")

    # ---- スコア加算ロジック ----
    # OCR本文 or incident_location からの確認済みシグナル
    ocr_milit  = [k for k in js["ocr_kw"] if k in JAPAN_MILIT_KW]
    ocr_base   = [k for k in js["ocr_kw"] if k in JAPAN_BASE_KW and k not in ocr_milit]
    ocr_pac    = [k for k in js["ocr_kw"] if k in PACIFIC_KW
                  and k not in ocr_milit and k not in ocr_base]

    loc_milit  = [k for k in js["loc_kw"] if k in JAPAN_MILIT_KW]
    loc_base   = [k for k in js["loc_kw"] if k in JAPAN_BASE_KW and k not in loc_milit]
    loc_pac    = [k for k in js["loc_kw"] if k not in loc_milit and k not in loc_base]

    # OCR本文での日本キーワード（最強シグナル）
    if ocr_milit:
        score += JAPAN_MILIT_SCORE
        reasons.append(f"OCR_Japan_military_base({','.join(ocr_milit)})+{JAPAN_MILIT_SCORE}")
    if ocr_base:
        score += JAPAN_BASE_SCORE
        reasons.append(f"OCR_Japan_keyword({','.join(ocr_base)})+{JAPAN_BASE_SCORE}")
    if ocr_pac:
        score += PACIFIC_SCORE
        reasons.append(f"OCR_Pacific_keyword({','.join(ocr_pac)})+{PACIFIC_SCORE}")

    # incident_location での日本関連（強いシグナル）
    if loc_milit:
        score += JAPAN_MILIT_SCORE
        reasons.append(f"location_Japan_military_base({','.join(loc_milit)})+{JAPAN_MILIT_SCORE}")
    if loc_base:
        score += JAPAN_BASE_SCORE
        reasons.append(f"location_Japan_keyword({','.join(loc_base)})+{JAPAN_BASE_SCORE}")
    if loc_pac:
        score += PACIFIC_SCORE
        reasons.append(f"location_Pacific({','.join(loc_pac)})+{PACIFIC_SCORE}")

    # ファイル名のみの弱いシグナル（conflict の場合はスキップ）
    if js["fn_kw"] and not js["loc_kw"] and not js["ocr_kw"] and not js["location_conflict"]:
        score += JAPAN_FILENAME_WEAK_SCORE
        reasons.append(f"filename_Japan_weak_signal({','.join(js['fn_kw'])})+{JAPAN_FILENAME_WEAK_SCORE}")

    # japan_keywords 表示：confirmed のみ、なければ fn のみを weak として表示
    if js["all_confirmed_kw"]:
        kw_hits = js["all_confirmed_kw"]
    elif js["fn_kw"]:
        kw_hits = [f"{k}(filename-only)" for k in js["fn_kw"]]
    else:
        kw_hits = []

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
        "page_count":              page_count if page_count > 0 else "",
        "ocr_success_rate":        ocr_success_rate,
        "review_required_count":   review_required_count,
        "japan_related":           japan_related,
        "japan_keywords":          ",".join(kw_hits),
        "japan_signal_source":     japan_signal_source,
        "location_conflict":       location_conflict,
        "location_conflict_reason": location_conflict_reason,
        "candidate_score":         score,
        "recommended_lane":        lane,
        "reasons":                 " | ".join(reasons),
        "notes":                   " | ".join(notes),
    }


# -------------------------------------------------------
# メイン処理
# -------------------------------------------------------

CSV_FIELDS = [
    "file_name", "agency", "release_date", "incident_date", "incident_location",
    "file_type", "page_count", "ocr_success_rate", "review_required_count",
    "japan_related", "japan_keywords", "japan_signal_source",
    "location_conflict", "location_conflict_reason",
    "candidate_score", "recommended_lane",
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
    print("=== 日本関連候補（confirmed: location/OCR根拠あり） ===")
    for r in japan:
        print(f"  [{r['candidate_score']:>3}] [{r['recommended_lane']:<9}] "
              f"{r['file_name'][:48]}  src={r['japan_signal_source']}  kw={r['japan_keywords']}")

    conflicts = [r for r in all_rows if r["location_conflict"] == "true"]
    if conflicts:
        print()
        print("=== 場所矛盾（conflict）検出 ===")
        for r in conflicts:
            print(f"  [{r['candidate_score']:>3}] {r['file_name'][:48]}")
            print(f"       {r['location_conflict_reason']}")

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
