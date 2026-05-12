#!/usr/bin/env python3
"""
scripts/verify_article_against_sources.py

AI概要版記事と元ソースの照合チェック
目的: 記事のメタデータ・引用・主張が元ソース（CSV・PDF）と矛盾していないか警告を出す

これは完全な真偽判定ではなく、人間レビュー前の警告出しを目的とする。

入力:
  note_drafts/*.md
  metadata/files_catalog.csv
  metadata/text_layer_report.csv
  extracted_text/ocr_results.csv
  classification/page_classification.csv

出力:
  review_logs/source_verification_report.md

使い方:
  python3 scripts/verify_article_against_sources.py
  python3 scripts/verify_article_against_sources.py note_drafts/ai_reading_009.md
"""

import re
import sys
import csv
import glob
from datetime import datetime
from pathlib import Path

# ==================== パス設定 ====================

PROJECT_ROOT = Path(__file__).parent.parent
NOTE_DRAFTS_DIR  = PROJECT_ROOT / "note_drafts"
REVIEW_LOGS_DIR  = PROJECT_ROOT / "review_logs"
RAW_PDF_DIR      = PROJECT_ROOT / "raw_pdf"
OUTPUT_FILE      = REVIEW_LOGS_DIR / "source_verification_report.md"

CATALOG_CSV      = PROJECT_ROOT / "metadata" / "files_catalog.csv"
TEXT_LAYER_CSV   = PROJECT_ROOT / "metadata" / "text_layer_report.csv"
OCR_RESULTS_CSV  = PROJECT_ROOT / "extracted_text" / "ocr_results.csv"
PAGE_CLASS_CSV   = PROJECT_ROOT / "classification" / "page_classification.csv"

# ==================== Finding クラス ====================

class Finding:
    def __init__(self, level: str, category: str, detail: str, hint: str = ""):
        self.level    = level    # "ERROR" / "WARNING" / "INFO"
        self.category = category
        self.detail   = detail
        self.hint     = hint     # 修正の手がかり（任意）


# ==================== データ読み込み ====================

def load_catalog() -> dict[str, dict]:
    """files_catalog.csv を file_name → row の辞書で返す"""
    with open(CATALOG_CSV, encoding="utf-8") as f:
        return {r["file_name"]: r for r in csv.DictReader(f)}


def load_ocr_results() -> dict[str, list[dict]]:
    """ocr_results.csv を pdf_file → [rows] の辞書で返す"""
    result = {}
    with open(OCR_RESULTS_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            result.setdefault(row["pdf_file"], []).append(row)
    return result


def load_text_layer_report() -> dict[str, list[dict]]:
    """text_layer_report.csv を pdf_file → [rows] の辞書で返す"""
    result = {}
    with open(TEXT_LAYER_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            result.setdefault(row["pdf_file"], []).append(row)
    return result


def extract_pdf_text(file_name: str) -> tuple[str, str]:
    """
    raw_pdf/ から PyMuPDF でテキストを抽出する。
    返り値: (全ページ結合テキスト, 方法の説明文)
    """
    try:
        import fitz
    except ImportError:
        return "", "PyMuPDF未インストール"

    pdf_path = RAW_PDF_DIR / file_name
    if not pdf_path.exists():
        return "", "PDFファイルが見当たりません"

    try:
        doc = fitz.open(str(pdf_path))
        pages_text = []
        for page in doc:
            t = page.get_text().strip()
            if t:
                pages_text.append(t)
        doc.close()
        full_text = "\n".join(pages_text)
        if full_text.strip():
            return full_text, f"テキスト層から抽出（{len(full_text)}文字）"
        else:
            return "", "テキスト層なし（スキャン専用PDF）"
    except Exception as e:
        return "", f"PDF読み込みエラー: {e}"


# ==================== メタデータ解析 ====================

def parse_article_metadata(text: str) -> dict[str, str]:
    """## 文書メタデータ セクションを辞書で返す"""
    meta = {}
    in_meta = False
    for line in text.splitlines():
        if line.strip() == "## 文書メタデータ":
            in_meta = True
            continue
        if in_meta and re.match(r"^##\s", line):
            break
        if in_meta:
            m = re.match(r"-\s+\*\*(.+?)[：:]\*\*\s*(.*)", line)
            if m:
                meta[m.group(1).strip()] = m.group(2).strip()
    return meta


def extract_english_blockquotes(text: str) -> list[str]:
    """英語を含む blockquote ブロックをリストで返す"""
    quotes = []
    current = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(">"):
            content = s[1:].strip()
            if re.search(r"[a-zA-Z]{3,}", content):
                current.append(content)
            elif current:
                quotes.append(" ".join(current))
                current = []
        else:
            if current:
                quotes.append(" ".join(current))
                current = []
    if current:
        quotes.append(" ".join(current))
    return quotes


# ==================== 日付正規化 ====================

def normalize_date(raw: str) -> dict:
    """
    各種日付フォーマットを {year, month, day, partial} に正規化する。
    partial=True は年のみ・あいまいな場合を示す。
    """
    raw = raw.strip()
    if not raw or raw in ("N/A", "Unknown", "不明"):
        return {}

    # "5/8/26" → 2026-05-08
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{2,4})$", raw)
    if m:
        y = int(m.group(3))
        year = 2000 + y if y < 100 else y
        return {"year": year, "month": int(m.group(1)), "day": int(m.group(2))}

    # "2026年5月8日" / "2020年5月14日 20:40 UTC（夜間）"
    m = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", raw)
    if m:
        return {"year": int(m.group(1)), "month": int(m.group(2)), "day": int(m.group(3))}

    # "8/24/20" 形式 → 上で捕捉済み
    # "1969年" / "1972年（...）"
    m = re.match(r"(\d{4})年", raw)
    if m:
        return {"year": int(m.group(1)), "partial": True}

    # 純粋な年 "1969" / "2023"
    m = re.match(r"^(\d{4})$", raw)
    if m:
        return {"year": int(m.group(1)), "partial": True}

    # "Late 2025" / "2025年（後半）"
    m = re.search(r"(\d{4})", raw)
    if m:
        return {"year": int(m.group(1)), "partial": True}

    return {"raw": raw}


def dates_conflict(a: dict, b: dict) -> tuple[bool, str]:
    """
    2つの正規化日付が矛盾するか判定。
    返り値: (conflict: bool, reason: str)
    """
    if not a or not b:
        return False, ""

    if "year" not in a or "year" not in b:
        return False, ""

    # どちらかが partial (年のみ) の場合は年だけ比較
    if a.get("partial") or b.get("partial"):
        if a["year"] != b["year"]:
            return True, f"年が一致しません（記事: {a['year']} / カタログ: {b['year']}）"
        return False, ""

    # 両方 full date の場合
    a_tuple = (a.get("year"), a.get("month"), a.get("day"))
    b_tuple = (b.get("year"), b.get("month"), b.get("day"))
    if a_tuple != b_tuple:
        return True, f"日付が一致しません（記事: {a_tuple} / カタログ: {b_tuple}）"
    return False, ""


def normalize_agency(raw: str) -> str:
    """括弧内の補足を除いたエージェンシー名を返す"""
    return re.split(r"[（(]", raw)[0].strip()


# ==================== チェック関数群 ====================

def check_file_name_in_catalog(
    meta: dict, catalog: dict
) -> list[Finding]:
    fn = meta.get("File Name", "")
    if not fn:
        return [Finding("WARNING", "File Name", "記事にFile Nameが記載されていません")]
    if fn not in catalog:
        return [Finding(
            "WARNING", "File Name",
            f"「{fn}」が files_catalog.csv に見当たりません",
            "ファイル名の表記ゆれ・タイポを確認してください"
        )]
    return []


def check_agency(meta: dict, catalog_entry: dict) -> list[Finding]:
    article_agency  = normalize_agency(meta.get("Agency", ""))
    catalog_agency  = catalog_entry.get("agency", "").strip()
    if not article_agency or not catalog_agency:
        return []
    if article_agency != catalog_agency:
        return [Finding(
            "WARNING", "Agency",
            f"記事「{article_agency}」/ カタログ「{catalog_agency}」",
            "表記を統一するか、カタログとの差異に注意書きを入れてください"
        )]
    return []


def check_release_date(meta: dict, catalog_entry: dict) -> list[Finding]:
    art_date = normalize_date(meta.get("Release Date", ""))
    cat_date = normalize_date(catalog_entry.get("release_date", ""))
    conflict, reason = dates_conflict(art_date, cat_date)
    if conflict:
        return [Finding(
            "WARNING", "Release Date",
            reason,
            "2026年5月8日（5/8/26）が正しいリリース日です"
        )]
    return []


def check_incident_date(meta: dict, catalog_entry: dict) -> list[Finding]:
    art_raw  = meta.get("Incident Date", "")
    cat_raw  = catalog_entry.get("incident_date", "")
    if not art_raw or not cat_raw or cat_raw in ("N/A", ""):
        return []

    art_date = normalize_date(art_raw)
    cat_date = normalize_date(cat_raw)
    conflict, reason = dates_conflict(art_date, cat_date)
    if conflict:
        return [Finding(
            "INFO", "Incident Date",
            f"{reason}（記事原文: 「{art_raw}」 / カタログ原文: 「{cat_raw}」）",
            "インシデント日と文書作成日が異なる場合があります。意図的なら注記を"
        )]
    return []


def check_incident_location(meta: dict, catalog_entry: dict) -> list[Finding]:
    """
    記事ロケーションがカタログロケーションを含んでいるか（拡張は許可、矛盾は警告）
    """
    art_loc = meta.get("Incident Location", "").lower()
    cat_loc = catalog_entry.get("incident_location", "").strip().lower()
    if not art_loc or not cat_loc or cat_loc in ("n/a", ""):
        return []

    # カタログのロケーションが記事に含まれていれば OK（翻訳・拡張を許容）
    # カタログ: "Moon" → 記事: "Moon（月）" → OK
    # カタログ: "Arabian Sea" → 記事: "アラビア海北部" → 要チェック（翻訳のみ）
    # 完全不一致は WARNING
    cat_words = re.sub(r"[（(）)\-,]", " ", cat_loc).split()
    # カタログのキーワードが記事に1つも含まれていなければ不一致の可能性
    hits = [w for w in cat_words if len(w) >= 3 and w in art_loc]
    if not hits:
        # 翻訳されている場合を考慮して INFO どまり
        return [Finding(
            "INFO", "Incident Location",
            f"カタログ「{catalog_entry['incident_location']}」と記事「{meta.get('Incident Location','')}」に共通語なし",
            "翻訳・詳細化は問題ありませんが、矛盾がないか確認してください"
        )]
    return []


def check_url_consistency(meta: dict, article_text: str) -> list[Finding]:
    """元PDF URL がメタデータの File Name と一致するか"""
    findings = []
    fn = meta.get("File Name", "")

    # Source URL
    source_url = meta.get("Source URL", "")
    if source_url and "war.gov/UFO" not in source_url:
        findings.append(Finding(
            "WARNING", "Source URL",
            f"Source URL が war.gov/UFO ではありません: 「{source_url}」"
        ))

    # 出典セクションの PDF URL
    pdf_url_match = re.search(r"https://[^\s)]+\.pdf", article_text)
    if not pdf_url_match:
        findings.append(Finding("WARNING", "元PDF URL", "出典セクションに PDF URL が見当たりません"))
    elif fn and fn not in pdf_url_match.group(0):
        findings.append(Finding(
            "WARNING", "元PDF URL",
            f"PDF URL（{pdf_url_match.group(0)[-60:]}）に File Name「{fn}」が含まれていません",
            "URL と File Name が一致しているか確認してください"
        ))
    return findings


def check_english_quotes_against_pdf(
    article_text: str, pdf_text: str, file_name: str
) -> list[Finding]:
    """
    記事内の英文引用が PDF 抽出テキストに存在するか確認する。
    PDF にテキスト層がない場合はスキップ。
    """
    if not pdf_text:
        return [Finding(
            "INFO", "英文引用照合",
            f"「{file_name}」のテキスト層が取得できないため引用照合をスキップしました",
            "スキャン専用PDFの場合は目視確認が必要です"
        )]

    quotes = extract_english_blockquotes(article_text)
    if not quotes:
        return []

    findings = []
    pdf_normalized = re.sub(r"\s+", " ", pdf_text).lower()

    for quote in quotes:
        # 引用の冒頭20文字をキーとして照合（OCRノイズを考慮して短め）
        key = re.sub(r"\s+", " ", quote[:60]).lower().strip()
        if len(key) < 10:
            continue
        # 10文字以上の連続マッチを探す（OCR誤字を考慮して分割チェック）
        words = key.split()
        if len(words) >= 4:
            # 4単語の連続ブロックをいくつか確認
            found = False
            for i in range(0, min(len(words), 8) - 3):
                snippet = " ".join(words[i:i+4])
                if snippet in pdf_normalized:
                    found = True
                    break
            if not found:
                findings.append(Finding(
                    "WARNING", "英文引用照合",
                    f"引用冒頭「{quote[:70]}…」がPDFテキストに見当たりません",
                    "OCRノイズ・スキャン由来の誤字、または引用の改変がないか確認してください"
                ))
    return findings


def check_redaction_speculation(
    article_text: str, pdf_text: str
) -> list[Finding]:
    """
    黒塗り（1.4(a)、(b)(6) 等）が多い文書で、
    記事が黒塗り内容を推測・断定していないか確認する。
    """
    findings = []
    if not pdf_text:
        return findings

    # 黒塗りマーカーの密度を確認
    redaction_patterns = [r"\(b\)\([0-9]+\)", r"1\.4\(a\)", r"3\.5c", r"\[REDACTED\]"]
    redaction_count = sum(
        len(re.findall(p, pdf_text)) for p in redaction_patterns
    )
    redaction_density = redaction_count / max(len(pdf_text.split()), 1)

    if redaction_density < 0.02:
        return findings  # 黒塗りが少ない文書はスキップ

    # 記事に黒塗りへの言及があるか
    redaction_disclosure_kw = [
        "黒塗り", "墨消し", "伏字", "[REDACTED]", "REDACTED",
        "不明", "開示されていません", "確認できません",
    ]
    has_disclosure = any(kw in article_text for kw in redaction_disclosure_kw)

    if not has_disclosure:
        findings.append(Finding(
            "WARNING", "黒塗り開示",
            f"元PDFに黒塗りが多数（密度: {redaction_density:.3f}）ありますが、記事に黒塗りへの言及が見当たりません",
            "「〜は黒塗りのため不明」などの注記を追加することを検討してください"
        ))

    # 黒塗り内容を推測・断定しているように見えるパターン
    spec_patterns = [
        (r"おそらく.{0,15}(部隊|組織|地名|座標|場所)", "黒塗り箇所の推測表現の可能性"),
        (r"(と思われる|と推測され).{0,20}(組織|部隊|地名|人物|場所)",
         "黒塗り箇所の推測表現の可能性"),
    ]
    for pattern, label in spec_patterns:
        matches = re.findall(pattern, article_text)
        if matches:
            findings.append(Finding(
                "INFO", "黒塗り推測",
                f"{label}（パターン検出）",
                "推測であることが明示されているか確認してください"
            ))
    return findings


def check_speculation_hedging(article_text: str) -> list[Finding]:
    """
    AIが追加した可能性がある推測的主張（ソースにない内容の断定）を検出する。
    対象: 「〜だろう」「〜に違いない」「〜と分かる」など、引用外での断定。
    """
    findings = []
    non_quote_lines = [
        l for l in article_text.splitlines()
        if not l.strip().startswith(">") and not l.strip().startswith("*")
    ]
    body = "\n".join(non_quote_lines)

    patterns = [
        (r"〜に違いない|に違いない[。」\s]", "「〜に違いない」という推測断定"),
        (r"明らかに.{0,20}[だです][。」]", "「明らかに」という断定的表現"),
        (r"間違いなく", "「間違いなく」という断定表現"),
        (r"確実に.{0,20}[だです][。」]", "「確実に」という断定表現"),
        (r"実際に.{0,15}(存在|飛行|移動|出現)し", "「実際に〜した」という断定表現"),
    ]
    for pattern, label in patterns:
        if re.search(pattern, body):
            findings.append(Finding(
                "WARNING", "推測断定",
                label,
                "引用外での断定は「〜と記録されています」「〜と読み取れます」に置き換えを検討"
            ))
    return findings


def check_ocr_pipeline_coverage(
    file_name: str, ocr_results: dict, text_layer_report: dict
) -> list[Finding]:
    """OCRパイプラインのデータがあるか・品質はどうかを確認する"""
    findings = []
    stem = file_name.replace(".pdf", "")

    # ocr_results.csv にエントリがあるか
    has_ocr_csv = stem in ocr_results or file_name in ocr_results
    if not has_ocr_csv:
        findings.append(Finding(
            "INFO", "OCRパイプライン",
            f"「{file_name}」の OCR パイプライン実行記録が ocr_results.csv にありません",
            "個別処理（手動OCR）で対応した場合はこの警告を無視してください"
        ))

    # text_layer_report.csv にエントリがあるか
    has_tl = stem in text_layer_report or file_name in text_layer_report
    if not has_tl:
        findings.append(Finding(
            "INFO", "テキスト層レポート",
            f"「{file_name}」の text_layer_report.csv エントリがありません",
            "個別処理の場合はこの警告を無視してください"
        ))
    return findings


# ==================== メインレビュー関数 ====================

def verify_file(
    path: Path,
    catalog: dict,
    ocr_results: dict,
    text_layer_report: dict,
) -> tuple[str, dict, list[Finding]]:
    """
    1ファイルを検証し (ファイル名, メタデータ, findings) を返す
    """
    text = path.read_text(encoding="utf-8")
    meta = parse_article_metadata(text)
    findings: list[Finding] = []

    fn = meta.get("File Name", "")

    # (1) File Name → カタログ照合
    fn_findings = check_file_name_in_catalog(meta, catalog)
    findings += fn_findings

    # カタログエントリが見つかった場合のみメタデータ比較を実施
    catalog_entry = catalog.get(fn)
    if catalog_entry:
        findings += check_agency(meta, catalog_entry)
        findings += check_release_date(meta, catalog_entry)
        findings += check_incident_date(meta, catalog_entry)
        findings += check_incident_location(meta, catalog_entry)

    # (2) URL 整合性チェック
    findings += check_url_consistency(meta, text)

    # (3) PDF テキスト抽出 → 引用照合・黒塗りチェック
    if fn:
        pdf_text, pdf_method = extract_pdf_text(fn)
        findings += check_english_quotes_against_pdf(text, pdf_text, fn)
        findings += check_redaction_speculation(text, pdf_text)
    else:
        pdf_text, pdf_method = "", "File Name なし"

    # (4) 推測断定チェック（引用外の本文）
    findings += check_speculation_hedging(text)

    # (5) OCR パイプライン記録チェック
    if fn:
        findings += check_ocr_pipeline_coverage(fn, ocr_results, text_layer_report)

    # メタデータに pdf_method を付加（レポート用）
    meta["_pdf_text_method"] = pdf_method
    meta["_pdf_text_len"]    = len(pdf_text)

    return path.name, meta, findings


# ==================== レポート生成 ====================

def verdict(findings: list[Finding]) -> str:
    levels = {f.level for f in findings}
    if "ERROR"   in levels: return "❌ 要修正"
    if "WARNING" in levels: return "⚠️ 要確認"
    if "INFO"    in levels: return "💬 確認推奨"
    return "✅ 問題なし"


def count_by_level(findings: list[Finding]) -> dict:
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    for f in findings:
        counts[f.level] += 1
    return counts


def build_report(results: list[tuple[str, dict, list[Finding]]]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []

    lines += [
        "# AI概要版 原文照合チェックレポート",
        f"生成日時: {now}",
        "",
        "---",
        "",
        "## 目的と限界",
        "",
        "このレポートはルールベースの自動チェックです。完全な真偽判定ではなく、",
        "**人間レビュー前の警告出し**を目的としています。",
        "",
        "- ✅ 問題なし：自動チェックでは問題を検出しませんでした",
        "- 💬 確認推奨：軽微な確認点があります（公開前に目を通してください）",
        "- ⚠️ 要確認：メタデータ不一致・引用照合失敗など確認が必要です",
        "- ❌ 要修正：重大な問題が検出されました",
        "",
        "---",
        "",
    ]

    # サマリーテーブル
    lines += ["## サマリー", ""]
    lines.append("| ファイル | PDF照合 | ERROR | WARNING | INFO | 判定 |")
    lines.append("|---|---|---|---|---|---|")

    for fname, meta, findings in results:
        counts = count_by_level(findings)
        v = verdict(findings)
        pdf_len = meta.get("_pdf_text_len", 0)
        pdf_icon = "📄" if pdf_len > 100 else "🔍"
        lines.append(
            f"| {fname} | {pdf_icon}{pdf_len}文字 "
            f"| {counts['ERROR']} | {counts['WARNING']} | {counts['INFO']} | {v} |"
        )

    total_e = sum(count_by_level(f)["ERROR"]   for _, _, f in results)
    total_w = sum(count_by_level(f)["WARNING"] for _, _, f in results)
    total_i = sum(count_by_level(f)["INFO"]    for _, _, f in results)
    lines.append(
        f"| **合計 ({len(results)}件)** | | **{total_e}** | **{total_w}** | **{total_i}** | |"
    )
    lines += ["", "---", "", "## 詳細レポート", ""]

    for fname, meta, findings in results:
        v = verdict(findings)
        fn = meta.get("File Name", "(不明)")
        pdf_method = meta.get("_pdf_text_method", "")

        lines.append(f"### {fname}")
        lines.append("")
        lines.append(f"**判定: {v}**")
        lines.append("")
        lines.append(f"- File Name: `{fn}`")
        lines.append(f"- PDF照合方法: {pdf_method}")
        lines.append("")

        if not findings:
            lines.append("自動チェックで問題は検出されませんでした。")
            lines += ["", "---", ""]
            continue

        for level in ("ERROR", "WARNING", "INFO"):
            lf = [f for f in findings if f.level == level]
            if not lf:
                continue
            icon = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "💬"}[level]
            for f in lf:
                lines.append(f"- {icon} **[{level}] {f.category}**  ")
                lines.append(f"  {f.detail}")
                if f.hint:
                    lines.append(f"  → *{f.hint}*")

        lines += ["", "---", ""]

    # チェック項目説明
    lines += [
        "## チェック項目の説明",
        "",
        "| チェック | 内容 | 判定レベル |",
        "|---|---|---|",
        "| File Name照合 | files_catalog.csv にファイル名が存在するか | WARNING |",
        "| Agency | 記事とカタログのエージェンシーが一致するか | WARNING |",
        "| Release Date | リリース日が一致するか（正規化比較） | WARNING |",
        "| Incident Date | インシデント日が一致するか（年レベル比較） | INFO |",
        "| Incident Location | カタログの場所が記事に含まれるか | INFO |",
        "| URL整合性 | Source URL が war.gov/UFO か・元PDF URL にファイル名が含まれるか | WARNING |",
        "| 英文引用照合 | 引用の冒頭部分がPDFテキストに存在するか（テキスト層のみ） | WARNING/INFO |",
        "| 黒塗り開示 | 黒塗りの多いPDFで記事が黒塗りに言及しているか | WARNING |",
        "| 黒塗り推測 | 黒塗り箇所の内容を推測していないか | INFO |",
        "| 推測断定 | 引用外の本文で「〜に違いない」等の断定表現がないか | WARNING |",
        "| OCRパイプライン | ocr_results.csv / text_layer_report.csv に記録があるか | INFO |",
        "",
        "---",
        "",
        "*このレポートは `scripts/verify_article_against_sources.py` によって自動生成されました。*",
        "*完全な真偽判定ではなく、人間レビュー前の参考情報です。*",
    ]

    return "\n".join(lines)


# ==================== エントリーポイント ====================

def get_target_files(args: list[str]) -> list[Path]:
    if args:
        return [Path(p) for p in args if Path(p).exists()]
    return sorted(NOTE_DRAFTS_DIR.glob("ai_*.md"))


def main():
    args = sys.argv[1:]
    target_files = get_target_files(args)

    if not target_files:
        print("対象ファイルが見つかりません。")
        sys.exit(1)

    print("データ読み込み中...")
    catalog         = load_catalog()
    ocr_results     = load_ocr_results()
    text_layer_rep  = load_text_layer_report()
    print(f"  catalog: {len(catalog)}件 / ocr_results: {sum(len(v) for v in ocr_results.values())}件")

    print(f"\n対象ファイル: {len(target_files)} 件")
    results = []
    for path in target_files:
        fname, meta, findings = verify_file(path, catalog, ocr_results, text_layer_rep)
        counts = count_by_level(findings)
        v = verdict(findings)
        print(f"  {v} {fname}  (E:{counts['ERROR']} W:{counts['WARNING']} I:{counts['INFO']})")
        results.append((fname, meta, findings))

    report = build_report(results)
    REVIEW_LOGS_DIR.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"\nレポート出力: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
