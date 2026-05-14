#!/usr/bin/env python3
"""
generate_provenance.py
======================
AI概要版の根拠追跡（プロベナンス）チェックツール

目的:
    AI概要版ドラフトと元PDFのテキストを照合し、
    数値・英語キーワード等の「危険フィールド」がソースに存在するかを確認する。
    contrail/100,000ft のようなハルシネーションを自動検出する。

設計方針:
    「完全精査型」ではなく「重大誤認を止める」ことが目的。
    false positive（過検出）は許容するが、false negative（見逃し）を最小化する。

使用方法:
    # 単一ドラフト
    python3 scripts/generate_provenance.py note_drafts/ai_summary_029_*.md

    # 複数ドラフト（glob可）
    python3 scripts/generate_provenance.py note_drafts/ai_summary_03*.md

    # published_articles/ のファイルも可
    python3 scripts/generate_provenance.py published_articles/ai_summary_016*.md

出力:
    provenance/<pdf_stem>_provenance.json  ... 機械可読な根拠データ
    provenance/<pdf_stem>_check.md         ... 人間向けチェックレポート

必要ライブラリ:
    pip3 install pymupdf
"""

import json
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path

# -------------------------------------------------------
# バッチレポート出力先
# -------------------------------------------------------
REVIEW_LOGS_DIR = None  # main() で初期化

try:
    import fitz  # PyMuPDF
except ImportError:
    print("[エラー] PyMuPDF が必要です: pip3 install pymupdf")
    sys.exit(1)

# -------------------------------------------------------
# パス設定
# -------------------------------------------------------
PROJECT_ROOT    = Path(__file__).resolve().parent.parent
RAW_PDF_DIR     = PROJECT_ROOT / "raw_pdf"
PROVENANCE_DIR  = PROJECT_ROOT / "provenance"
REVIEW_LOGS_DIR = PROJECT_ROOT / "review_logs"

# -------------------------------------------------------
# 「危険フィールド」の定義
# -------------------------------------------------------

# 数値＋単位パターン（記事本文から抽出）
# グループ1: 数値部分, グループ2: 単位部分（省略可）
NUMBER_WITH_UNIT_PATTERNS = [
    # 距離: 86海里, 55NM, 26nm
    # NOTE: (?<![0-9,]) でカンマ直後の部分マッチを防ぐ（例: 9,450 の "450" を個別にマッチしない）
    (re.compile(r"(?<![0-9a-zA-Z_,])(\d[\d,]*(?:\.\d+)?)\s*(NM|nm|海里|ノーティカルマイル|nautical miles?)", re.I),
     "distance"),
    # 速度: 500ノット, 500KTS, 300kts
    (re.compile(r"(?<![0-9a-zA-Z_,])(\d[\d,]*(?:\.\d+)?)\s*(KTS|kts|ノット|knots?|mph|kt)(?![0-9a-zA-Z_])", re.I),
     "speed"),
    # 高度・高さ: 100,000フィート, 35,000ft, 9,450メートル
    (re.compile(r"(?<![0-9a-zA-Z_,])(\d[\d,]*(?:\.\d+)?)\s*(フィート|ft|FT|feet|meters?|メートル)(?![0-9a-zA-Z_])", re.I),
     "altitude"),
    # 時間: 2分間, 12秒
    (re.compile(r"(?<![0-9a-zA-Z_,])(\d[\d,]*(?:\.\d+)?)\s*(分間|秒間|分|秒|hours?|minutes?|seconds?)(?![0-9a-zA-Z_])", re.I),
     "duration"),
]

# 英語・ASCII技術用語パターン（記事の（）内から抽出）
# 例: 飛行雲（contrail）→ "contrail" を抽出
PAREN_ENGLISH_PATTERN = re.compile(
    r"[（(]([A-Za-z][A-Za-z0-9\-/ ]{2,60})[）)]"
)

# 英語の機関名・固有名詞（記事本文中の英字列）
# 最大4単語まで（長い ALL CAPS 文を誤検出しないよう制限）
ENGLISH_NOUN_PATTERN = re.compile(
    r"\b([A-Z][A-Z0-9\-]{2,}(?:\s+[A-Z][A-Z0-9\-]{1,}){0,3})\b"
)

# 引用符で囲まれた日本語または英語の評価・コメント
QUOTE_PATTERN = re.compile(
    r'\u300c(.{10,100})\u300d'
)

# -------------------------------------------------------
# メタデータ解析
# -------------------------------------------------------

def parse_metadata(article_text: str) -> dict:
    """## 文書メタデータ セクションを辞書で返す"""
    meta = {}
    in_meta = False
    for line in article_text.splitlines():
        if line.strip() == "## 文書メタデータ":
            in_meta = True
            continue
        if in_meta and re.match(r"^##\s", line):
            break
        if in_meta:
            m = re.match(r"[-*]\s+\*?\*?(.+?)[：:]\*?\*?\s*(.*)", line)
            if m:
                meta[m.group(1).strip()] = m.group(2).strip()
    return meta


def get_pdf_name(article_text: str) -> str | None:
    """記事メタデータの File Name を取得する"""
    meta = parse_metadata(article_text)
    fn = meta.get("File Name", "").strip()
    if fn and not fn.endswith(".pdf"):
        fn += ".pdf"
    return fn if fn else None


# -------------------------------------------------------
# PDF テキスト抽出
# -------------------------------------------------------

def extract_pdf_text_by_page(pdf_path: Path) -> dict[int, str]:
    """PDFから1ページ単位でテキストを抽出する。{page_num(1-based): text}"""
    pages = {}
    try:
        doc = fitz.open(str(pdf_path))
        for i, page in enumerate(doc, start=1):
            text = page.get_text().strip()
            pages[i] = text
        doc.close()
    except Exception as e:
        print(f"  [警告] PDF読み込みエラー: {e}")
    return pages


def get_full_text(pages: dict[int, str]) -> str:
    return "\n".join(pages.values())


# -------------------------------------------------------
# 本文（メタデータセクション除外）の抽出
# -------------------------------------------------------

def extract_body_text(article_text: str) -> str:
    """
    ## 文書メタデータ セクションと ## 出典 セクションを除いた本文を返す。
    数値・キーワードの誤検出を防ぐため、メタデータ行は除外する。
    """
    lines = article_text.splitlines()
    skip_sections = {"## 文書メタデータ", "## 出典"}
    current_skip = False
    body_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped in skip_sections:
            current_skip = True
            continue
        if current_skip and re.match(r"^##\s", stripped) and stripped not in skip_sections:
            current_skip = False
        if not current_skip:
            body_lines.append(line)
    return "\n".join(body_lines)


# -------------------------------------------------------
# 括弧内検出ヘルパー
# -------------------------------------------------------

def is_inside_japanese_parens(body_text: str, match_start: int, match_end: int) -> bool:
    """
    マッチ位置が日本語括弧 （ ） の内部にあるか確認する。

    用途: 「31,000フィート（約9.4km）」の「9.4km」部分を
          "AI補助換算" と判定するために使用する。
    """
    # マッチの前に最後に出現する「（」を探す
    before = body_text[:match_start]
    last_open = before.rfind("（")
    if last_open < 0:
        return False
    # マッチの後に最初に出現する「）」を探す
    after = body_text[match_end:]
    first_close = after.find("）")
    if first_close < 0:
        return False
    # 「（」とマッチの間に別の「（」がない（ネスト対策）
    between = body_text[last_open + 1:match_start]
    if "（" in between or "）" in between:
        return False
    return True


def has_approx_marker(body_text: str, match_start: int) -> bool:
    """マッチ直前（最大10文字）に「約」があるか確認する。"""
    prefix = body_text[max(0, match_start - 10):match_start]
    return "約" in prefix


# -------------------------------------------------------
# 危険フィールド抽出
# -------------------------------------------------------

def extract_claims_from_body(body_text: str) -> list[dict]:
    """
    本文から「危険フィールド」（検証すべき主張）を抽出する。

    返り値:
        [{"type": ..., "raw_text": ..., "search_term": ..., "context": ...}, ...]
    """
    claims = []
    seen_terms = set()

    def add_claim(claim_type, raw_text, search_term, context, is_conversion=False):
        key = (claim_type, search_term.strip().lower())
        if key not in seen_terms:
            seen_terms.add(key)
            claims.append({
                "type":          claim_type,
                "raw_text":      raw_text,
                "search_term":   search_term.strip(),
                "context":       context[:120],
                "is_conversion": is_conversion,
            })

    # 1. 数値＋単位パターン
    for pattern, claim_type in NUMBER_WITH_UNIT_PATTERNS:
        for m in pattern.finditer(body_text):
            number_str = m.group(1).replace(",", "")
            start = max(0, m.start() - 30)
            end   = min(len(body_text), m.end() + 30)
            ctx   = body_text[start:end].replace("\n", " ")
            # 括弧内＋「約」付きなら補助換算と判定
            conv = (is_inside_japanese_parens(body_text, m.start(), m.end())
                    and has_approx_marker(body_text, m.start()))
            add_claim(claim_type, m.group(0), number_str, ctx, is_conversion=conv)

    # 2. カンマ区切り大数（単独）: 100,000 など単位なし
    for m in re.finditer(r"(?<![0-9a-zA-Z_,])(\d{1,3}(?:,\d{3})+)(?![0-9a-zA-Z_,])", body_text):
        number_str = m.group(1).replace(",", "")
        start = max(0, m.start() - 30)
        end   = min(len(body_text), m.end() + 30)
        ctx   = body_text[start:end].replace("\n", " ")
        if "文字" in ctx:
            continue
        # 括弧内＋「約」付きなら補助換算
        conv = (is_inside_japanese_parens(body_text, m.start(), m.end())
                and has_approx_marker(body_text, m.start()))
        add_claim("large_number", m.group(0), number_str, ctx, is_conversion=conv)

    # 3. 括弧内英語技術用語: （contrail）→ "contrail"
    for m in PAREN_ENGLISH_PATTERN.finditer(body_text):
        term = m.group(1).strip()
        # 2語以上 or 6文字以上の技術的な単語のみ対象
        words = term.split()
        if len(words) >= 2 or len(term) >= 6:
            start = max(0, m.start() - 40)
            end   = min(len(body_text), m.end() + 40)
            ctx   = body_text[start:end].replace("\n", " ")
            add_claim("paren_english", m.group(0), term, ctx)

    # 4. 記事本文中の英語大文字略語・固有名詞
    # （メタデータ外の本文中に出現する P-8A, INGUL, CTG 67.1 等）
    # 一般英語ストップワード（照合価値なし）
    STOP_WORDS = {
        "THE", "AND", "FOR", "FROM", "WITH", "NOT", "BUT", "ARE", "WAS",
        "WERE", "HAS", "HAD", "THAT", "THIS", "HAVE", "BEEN", "WILL",
        "CAN", "ALL", "ONE", "TWO", "ITS", "THEIR", "THEY", "WHICH",
        "WHEN", "INTO", "OVER", "THAN", "THEN", "ALSO", "BOTH",
        "MORE", "SOME", "SUCH", "EACH", "ONLY", "BEING", "AFTER",
        "OF", "IN", "TO", "BY", "AS", "AT", "AN", "OR", "IF",
        # プロジェクト固有のスキップ語（AI生成メタコメント等）
        "AI", "OCR", "PDF", "UAP", "UFO", "URL", "NOTE",
    }
    for m in ENGLISH_NOUN_PATTERN.finditer(body_text):
        term = m.group(1).strip()
        # 短すぎるものをスキップ
        if len(term) <= 2:
            continue
        # 全単語がストップワードならスキップ（"THE FORMATION" 等）
        words = term.split()
        if all(w in STOP_WORDS for w in words):
            continue
        # 最初の単語だけがストップワードならスキップ（"THE CONTINUOUS..." 等）
        if words and words[0] in STOP_WORDS:
            continue
        start = max(0, m.start() - 30)
        end   = min(len(body_text), m.end() + 30)
        ctx   = body_text[start:end].replace("\n", " ")
        add_claim("proper_noun", m.group(0), term, ctx)

    return claims


# -------------------------------------------------------
# ソース照合
# -------------------------------------------------------

def find_in_source(search_term: str, full_text: str, pages: dict[int, str]) -> dict:
    """
    検索語がPDFテキスト中に存在するか確認する。

    返り値:
        {
            "found": bool,
            "page": int or None,
            "excerpt": str (前後30文字),
        }
    """
    # 正規化: 余分な空白・大文字小文字を無視
    # 改行を空白に正規化することで PDF の行またぎフレーズもマッチ可能にする
    needle = re.sub(r"\s+", " ", search_term.strip().lower())
    if not needle:
        return {"found": False, "page": None, "excerpt": ""}

    # 全文照合（改行正規化済みの haystack で検索）
    haystack_full_normalized = re.sub(r"\s+", " ", full_text.lower())
    haystack_full = full_text.lower()  # excerpt 取得用（元テキスト）

    # 数値の場合: カンマあり/なし両方で試す
    # 例: "100000" → "100,000" も試す
    candidates = [needle]
    if re.match(r"^\d+$", needle) and len(needle) >= 4:
        # 3桁ごとにカンマを挿入した形も試す
        try:
            n = int(needle)
            candidates.append(f"{n:,}")
        except ValueError:
            pass

    for candidate in candidates:
        if candidate in haystack_full_normalized:
            # どのページか確認（ページ内も改行正規化して検索）
            for page_num, page_text in sorted(pages.items()):
                page_normalized = re.sub(r"\s+", " ", page_text.lower())
                if candidate in page_normalized:
                    # コンテキスト取得は正規化済みテキストから
                    idx = page_normalized.index(candidate)
                    start = max(0, idx - 30)
                    end   = min(len(page_normalized), idx + len(candidate) + 30)
                    excerpt = page_normalized[start:end].strip()
                    return {"found": True, "page": page_num, "excerpt": excerpt}
            # ページ特定できないが全文に存在
            idx = haystack_full_normalized.index(candidate)
            start = max(0, idx - 30)
            end   = min(len(haystack_full_normalized), idx + len(candidate) + 30)
            excerpt = haystack_full_normalized[start:end].strip()
            return {"found": True, "page": None, "excerpt": excerpt}

    return {"found": False, "page": None, "excerpt": ""}


# -------------------------------------------------------
# リスクスコアリング
# -------------------------------------------------------

# 翻訳者が追加する地名・言語名（ソースに存在しなくてもLOW）
GEO_CONTEXT_TERMS = {
    "japan", "syria", "greece", "iraq", "iran", "israel", "turkey",
    "china", "russia", "pakistan", "india", "korea", "taiwan",
    "gulf", "sea", "ocean", "mediterranean", "pacific", "atlantic",
    "arabian", "persian", "hormuz", "aden", "djibouti", "red sea",
    "kazakhstan", "papua", "guinea",
}

# ユニット説明フレーズ（翻訳者追加の定義）
UNIT_EXPLANATION_TERMS = {
    "nautical miles per hour", "nautical mile", "nautical miles",
    "knots", "kilometers per hour", "miles per hour",
}


def assign_risk(claim_type: str, search_term: str, context: str,
                is_conversion: bool = False) -> str:
    """
    ソースに存在しない(WARNING)クレームにリスクレベルを割り当てる。

    HIGH   : ソースにない技術数値・技術用語。AI ハルシネーションの可能性が高い。
             例: contrail（括弧内英語技術用語）、100,000（大数）、86海里（単位付き数値）
    MEDIUM : OCR 誤読・表記ゆれの可能性があり断定できない。
             例: USCENTCOM MDR（OCRが MOR と誤読）、固有名詞の略語
    LOW    : 翻訳者追加コンテキスト（地名・単位説明）、または補助換算値（数値・単位ルール v1）。
             ソース不在が意図的である可能性が高い。
    """
    # ── 補助換算値（数値・単位表記ルール v1）──
    # 「31,000フィート（約9.4km）」の「9.4km」のように
    # 括弧内＋「約」付きの換算値はソースに存在しなくて当然 → LOW
    if is_conversion:
        return "LOW"

    term_lower = search_term.strip().lower()

    # ── 括弧内英語用語 ──
    if claim_type == "paren_english":
        # 地名・言語名 → LOW（翻訳者が追加した地理的文脈）
        if term_lower in GEO_CONTEXT_TERMS:
            return "LOW"
        # ユニット説明 → LOW（翻訳者が追加した定義）
        if term_lower in UNIT_EXPLANATION_TERMS:
            return "LOW"
        for u in UNIT_EXPLANATION_TERMS:
            if u in term_lower:
                return "LOW"
        # スラッシュ付きフォーマット語（GENTEXT/OBSERVATION 等）→ MEDIUM
        if "/" in search_term:
            return "MEDIUM"
        # 全大文字の略語・文書タイプ表記（MISREP, GENTEXT, SITREP 等）→ MEDIUM
        # 例: ミッションレポート（MISREP）は文書型ラベルであり内容主張ではない
        if search_term == search_term.upper() and search_term.replace(" ", "").isalpha():
            return "MEDIUM"
        # 文書型・報告書名キーワードを含む → MEDIUM
        # 例: Range Fouler Debrief Form, Intelligence Information Report 等
        doc_type_words = {
            "report", "form", "debrief", "record", "document", "memorandum",
            "cable", "message", "correspondence", "brief", "summary",
            "assessment", "analysis", "intelligence", "information",
        }
        term_words = set(term_lower.split())
        if term_words & doc_type_words:
            return "MEDIUM"
        # 翻訳補助語・修飾語 → LOW
        # 例: 「可能性のある（Possible）」「推定（Estimated）」のような補足注釈
        qualifier_words = {
            "possible", "estimated", "approximate", "approximately", "likely",
            "potential", "probable", "roughly", "about",
        }
        if term_lower in qualifier_words:
            return "LOW"
        # 6文字以上の混在ケース技術用語 → HIGH
        # 例: contrail（物理現象）, missile（兵器種別）等の内容主張
        if len(search_term) >= 6:
            return "HIGH"
        return "MEDIUM"

    # ── 数値系（単位付き・大数） ──
    if claim_type in ("large_number", "distance", "speed", "altitude", "duration"):
        return "HIGH"

    # ── 固有名詞 ──
    if claim_type == "proper_noun":
        # OCR 誤読によくある略語（MDR/MOR 等）→ MEDIUM
        if re.match(r"^[A-Z]{2,10}(\s[A-Z]{2,10})?$", search_term):
            return "MEDIUM"
        # 識別番号・ID パターン → MEDIUM
        if re.search(r"\d", search_term):
            return "MEDIUM"
        return "MEDIUM"

    return "MEDIUM"


def article_risk_level(results: list[dict]) -> str:
    """
    記事全体のリスクレベルを WARNING クレームの最大リスクから決定する。
    HIGH > MEDIUM > LOW > (なし→LOW)
    """
    warnings_with_risk = [r for r in results if r["status"] == "WARNING"]
    if not warnings_with_risk:
        return "LOW"
    levels = [r.get("risk", "MEDIUM") for r in warnings_with_risk]
    if "HIGH" in levels:
        return "HIGH"
    if "MEDIUM" in levels:
        return "MEDIUM"
    return "LOW"


RISK_ICON = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}


# -------------------------------------------------------
# プロベナンスデータ生成
# -------------------------------------------------------

def generate_provenance(draft_path: Path) -> tuple[dict, list[dict]]:
    """
    ドラフトファイルとPDFを照合してプロベナンスデータを返す。

    返り値:
        (meta_info, results_list)
        results_list: [{"type", "raw_text", "search_term", "context", "found", "page", "excerpt", "status"}, ...]
    """
    article_text = draft_path.read_text(encoding="utf-8")
    pdf_name = get_pdf_name(article_text)

    if not pdf_name:
        return {"error": "File Name not found in article"}, []

    pdf_path = RAW_PDF_DIR / pdf_name
    if not pdf_path.exists():
        return {"error": f"PDF not found: {pdf_path}"}, []

    pages    = extract_pdf_text_by_page(pdf_path)
    full_text = get_full_text(pages)
    body_text = extract_body_text(article_text)

    claims  = extract_claims_from_body(body_text)
    results = []
    warning_count = 0
    ok_count = 0

    high_count = medium_count = low_count = 0

    for claim in claims:
        match = find_in_source(claim["search_term"], full_text, pages)
        status = "OK" if match["found"] else "WARNING"
        risk   = "OK"
        if status == "WARNING":
            warning_count += 1
            risk = assign_risk(
                claim["type"], claim["search_term"], claim["context"],
                is_conversion=claim.get("is_conversion", False)
            )
            if risk == "HIGH":
                high_count += 1
            elif risk == "MEDIUM":
                medium_count += 1
            else:
                low_count += 1
        else:
            ok_count += 1

        results.append({
            **claim,
            "found":   match["found"],
            "page":    match["page"],
            "excerpt": match["excerpt"],
            "status":  status,
            "risk":    risk,
        })

    art_risk = article_risk_level(results)

    meta_info = {
        "generated_at":    datetime.now().isoformat(),
        "draft_file":      str(draft_path.resolve().relative_to(PROJECT_ROOT)),
        "pdf_file":        pdf_name,
        "pdf_stem":        pdf_path.stem,
        "pdf_page_count":  len(pages),
        "pdf_char_count":  len(full_text),
        "claims_total":    len(results),
        "warning_count":   warning_count,
        "ok_count":        ok_count,
        "high_count":      high_count,
        "medium_count":    medium_count,
        "low_count":       low_count,
        "article_risk":    art_risk,
        "pdf_text":        full_text,
    }

    return meta_info, results


# -------------------------------------------------------
# レポート生成
# -------------------------------------------------------

def build_check_report(meta_info: dict, results: list[dict]) -> str:
    """人間向けチェックレポート（Markdown）を生成する"""
    lines = []

    draft    = meta_info.get("draft_file", "unknown")
    pdf      = meta_info.get("pdf_file", "unknown")
    total    = meta_info.get("claims_total", 0)
    warns    = meta_info.get("warning_count", 0)
    oks      = meta_info.get("ok_count", 0)
    high     = meta_info.get("high_count", 0)
    medium   = meta_info.get("medium_count", 0)
    low      = meta_info.get("low_count", 0)
    art_risk = meta_info.get("article_risk", "LOW")
    risk_icon = RISK_ICON.get(art_risk, "")

    if warns == 0:
        verdict = "✅ 問題なし"
    else:
        verdict = f"{risk_icon} {art_risk} (H:{high} M:{medium} L:{low})"

    lines += [
        f"# プロベナンスチェック: {Path(draft).name}",
        f"生成日時: {meta_info.get('generated_at', '')[:19]}",
        "",
        "---",
        "",
        "## サマリー",
        "",
        "| 項目 | 値 |",
        "|---|---|",
        f"| ドラフト | `{draft}` |",
        f"| 元PDF | `{pdf}` |",
        f"| PDFページ数 | {meta_info.get('pdf_page_count', 0)} |",
        f"| PDF文字数 | {meta_info.get('pdf_char_count', 0):,} |",
        f"| 抽出クレーム数 | {total} |",
        f"| OK | {oks} |",
        f"| WARNING (HIGH) | {high} |",
        f"| WARNING (MEDIUM) | {medium} |",
        f"| WARNING (LOW) | {low} |",
        f"| **記事リスク** | **{risk_icon} {art_risk}** |",
        f"| **判定** | **{verdict}** |",
        "",
    ]

    if "error" in meta_info:
        lines += [
            "## ❌ エラー",
            "",
            "```",
            meta_info["error"],
            "```",
        ]
        return "\n".join(lines)

    # WARNING を HIGH→MEDIUM→LOW の順に表示
    warnings = sorted(
        [r for r in results if r["status"] == "WARNING"],
        key=lambda r: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}.get(r.get("risk", "MEDIUM"), 1)
    )
    oks_list = [r for r in results if r["status"] == "OK"]

    if warnings:
        lines += [
            "## WARNING 一覧（要確認）",
            "",
            "| リスク | 検索語 | 種別 | 記事での出現 |",
            "|---|---|---|---|",
        ]
        for r in warnings:
            risk_lv  = r.get("risk", "MEDIUM")
            icon     = RISK_ICON.get(risk_lv, "")
            term     = r["search_term"][:40]
            raw      = r["raw_text"][:40].replace("|", "｜")
            lines.append(f"| {icon} {risk_lv} | `{term}` | {r['type']} | `{raw}` |")
        lines.append("")

        # HIGH のみ詳細展開
        high_warnings = [r for r in warnings if r.get("risk") == "HIGH"]
        if high_warnings:
            lines += [
                "### 🔴 HIGH リスク詳細",
                "",
                "以下の用語・数値が元PDFテキストに存在しません。",
                "**AI ハルシネーションの可能性があります。公開前に元 PDF を目視確認してください。**",
                "",
            ]
            for r in high_warnings:
                lines += [
                    f"#### `{r['search_term']}` ({r['type']})",
                    "",
                    f"- **記事での出現:** `{r['raw_text']}`",
                    f"- **コンテキスト:** `...{r['context'][:100]}...`",
                    f"- **PDFで検索:** `{r['search_term']}` → **見つかりません**",
                    "",
                ]

        medium_warnings = [r for r in warnings if r.get("risk") == "MEDIUM"]
        if medium_warnings:
            lines += [
                "<details>",
                "<summary>🟡 MEDIUM リスク詳細（OCR誤読・略語不一致の可能性あり）</summary>",
                "",
            ]
            for r in medium_warnings:
                lines += [
                    f"- **`{r['search_term']}`** ({r['type']}): `{r['context'][:80]}`",
                ]
            lines += ["", "</details>", ""]

        low_warnings = [r for r in warnings if r.get("risk") == "LOW"]
        if low_warnings:
            lines += [
                "<details>",
                "<summary>🟢 LOW リスク詳細（翻訳者追加コンテキスト等）</summary>",
                "",
            ]
            for r in low_warnings:
                lines += [
                    f"- **`{r['search_term']}`** ({r['type']}): `{r['context'][:80]}`",
                ]
            lines += ["", "</details>", ""]

    else:
        lines += [
            "## ✅ 全クレームが元PDFで確認済み",
            "",
        ]

    # OK リスト（折りたたみ）
    if oks_list:
        lines += [
            "<details>",
            "<summary>確認済みクレーム一覧（クリックで展開）</summary>",
            "",
            "| 検索語 | 種別 | ページ | PDFテキスト（前後） |",
            "|---|---|---|---|",
        ]
        for r in oks_list:
            page_str = str(r["page"]) if r["page"] else "?"
            excerpt  = r["excerpt"][:60].replace("|", "｜")
            lines.append(f"| `{r['search_term']}` | {r['type']} | p.{page_str} | `{excerpt}` |")
        lines += [
            "",
            "</details>",
            "",
        ]

    # PDF テキスト全文（デバッグ用・折りたたみ）
    pdf_text = meta_info.get("pdf_text", "")
    if pdf_text:
        lines += [
            "<details>",
            "<summary>元PDFテキスト全文（デバッグ用）</summary>",
            "",
            "```",
            pdf_text[:5000] + ("..." if len(pdf_text) > 5000 else ""),
            "```",
            "",
            "</details>",
            "",
        ]

    lines += [
        "---",
        "",
        "*このレポートは `scripts/generate_provenance.py` によって自動生成されました。*",
        "*WARNING は「PDFに見当たらない」事実のみを示します。*",
        "*記事の誤りを断定するものではありませんが、公開前に元PDFで目視確認してください。*",
    ]

    return "\n".join(lines)


# -------------------------------------------------------
# JSON 出力
# -------------------------------------------------------

def write_provenance_json(meta_info: dict, results: list[dict], out_path: Path) -> None:
    """プロベナンスデータをJSONで保存する"""
    # pdf_text は JSON に含めない（大きすぎる）
    meta_clean = {k: v for k, v in meta_info.items() if k != "pdf_text"}
    data = {
        "meta": meta_clean,
        "claims": results,
    }
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# -------------------------------------------------------
# メイン
# -------------------------------------------------------

def process_file(draft_path: Path) -> tuple[dict, list[dict]]:
    """
    1ファイルを処理して (meta_info, results) を返す。
    エラー時は meta_info に "error" キーが入る。
    """
    print(f"\n処理中: {draft_path.name}")

    meta_info, results = generate_provenance(draft_path)

    if "error" in meta_info:
        print(f"  ❌ エラー: {meta_info['error']}")
        return meta_info, results

    warns    = meta_info["warning_count"]
    oks      = meta_info["ok_count"]
    high     = meta_info["high_count"]
    medium   = meta_info["medium_count"]
    low      = meta_info["low_count"]
    art_risk = meta_info["article_risk"]
    pdf      = meta_info.get("pdf_file", "unknown")
    pdf_stem = meta_info.get("pdf_stem", "unknown")
    icon     = RISK_ICON.get(art_risk, "")

    print(f"  PDF: {pdf}")
    print(f"  PDFテキスト: {meta_info['pdf_char_count']:,}文字 / {meta_info['pdf_page_count']}ページ")
    print(f"  クレーム: {meta_info['claims_total']}件 (OK={oks} / WARNING={warns})")
    print(f"  リスク: {icon} {art_risk}  (HIGH={high} MEDIUM={medium} LOW={low})")

    # 出力ディレクトリ
    PROVENANCE_DIR.mkdir(exist_ok=True)

    # JSON 保存
    json_path = PROVENANCE_DIR / f"{pdf_stem}_provenance.json"
    write_provenance_json(meta_info, results, json_path)
    print(f"  JSON → {json_path.relative_to(PROJECT_ROOT)}")

    # Markdown レポート保存
    report = build_check_report(meta_info, results)
    md_path = PROVENANCE_DIR / f"{pdf_stem}_check.md"
    md_path.write_text(report, encoding="utf-8")
    print(f"  レポート → {md_path.relative_to(PROJECT_ROOT)}")

    # WARNING をコンソールに表示
    high_list = [r for r in results if r["status"] == "WARNING" and r.get("risk") == "HIGH"]
    med_list  = [r for r in results if r["status"] == "WARNING" and r.get("risk") == "MEDIUM"]
    low_list  = [r for r in results if r["status"] == "WARNING" and r.get("risk") == "LOW"]
    if high_list:
        print()
        for r in high_list:
            print(f"  🔴 HIGH [{r['type']}] `{r['search_term']}` ← `{r['raw_text']}`")
    if med_list:
        for r in med_list:
            print(f"  🟡 MED  [{r['type']}] `{r['search_term']}`")
    if low_list:
        for r in low_list:
            print(f"  🟢 LOW  [{r['type']}] `{r['search_term']}`")

    return meta_info, results


# -------------------------------------------------------
# バッチレポート生成
# -------------------------------------------------------

def build_batch_report(
    batch_results: list,
    batch_label: str = "",
) -> str:
    """複数記事の検証結果をまとめたバッチレポート（Markdown）を生成する。"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# プロベナンス一括検証レポート",
        f"生成日時: {now}",
    ]
    if batch_label:
        lines.append(f"対象範囲: {batch_label}")
    lines += [
        "",
        "---",
        "",
        "## リスクスコア定義",
        "",
        "| レベル | 意味 | 対応方針 |",
        "|---|---|---|",
        "| 🔴 HIGH | ソースに存在しない技術用語・数値（AI ハルシネーションの疑い） | **公開停止 / 要修正** |",
        "| 🟡 MEDIUM | OCR 誤読・略語不一致の可能性あり | 元 PDF 目視確認推奨 |",
        "| 🟢 LOW | 翻訳者追加コンテキスト（地名等）または軽微な不一致 | 許容範囲（確認任意） |",
        "",
        "---",
        "",
        "## 全記事サマリー",
        "",
        "| 記事ファイル | 元PDF | リスク | HIGH | MED | LOW | 判定 |",
        "|---|---|---|---|---|---|---|",
    ]

    high_articles   = []
    medium_articles = []

    for draft_path, meta, results in batch_results:
        fname    = draft_path.name
        pdf      = meta.get("pdf_file", "?")[:50]
        art_risk = meta.get("article_risk", "?")
        icon     = RISK_ICON.get(art_risk, "")
        h = meta.get("high_count", 0)
        m = meta.get("medium_count", 0)
        l = meta.get("low_count", 0)

        if "error" in meta:
            lines.append(
                f"| `{fname}` | `{pdf}` | ❌ ERROR | - | - | - | `{meta['error'][:40]}` |"
            )
            continue

        verdict = "✅ OK" if art_risk == "LOW" and h == 0 else f"{icon} {art_risk}"
        lines.append(
            f"| `{fname}` | `{pdf}` | {icon} {art_risk} | {h} | {m} | {l} | {verdict} |"
        )
        if art_risk == "HIGH":
            high_articles.append((draft_path, meta, results))
        elif art_risk == "MEDIUM":
            medium_articles.append((draft_path, meta, results))

    # 統計
    total    = len(batch_results)
    n_high   = sum(1 for _, m, _ in batch_results if m.get("article_risk") == "HIGH")
    n_medium = sum(1 for _, m, _ in batch_results if m.get("article_risk") == "MEDIUM")
    n_low    = sum(1 for _, m, _ in batch_results
                  if m.get("article_risk") == "LOW" and "error" not in m)
    n_error  = sum(1 for _, m, _ in batch_results if "error" in m)
    lines += [
        "",
        f"**合計 {total} 件**: 🔴 HIGH={n_high}  🟡 MEDIUM={n_medium}  🟢 LOW={n_low}"
        + (f"  ❌ ERROR={n_error}" if n_error else ""),
        "",
        "---",
        "",
    ]

    # HIGH 詳細
    if high_articles:
        lines += [
            "## 🔴 HIGH リスク記事 詳細（要修正）",
            "",
        ]
        for draft_path, meta, results in high_articles:
            lines += [
                f"### {draft_path.name}",
                "",
                f"- **元PDF**: `{meta.get('pdf_file', '?')}`",
                f"- **PDF文字数**: {meta.get('pdf_char_count', 0):,}",
                "",
                "| 検索語 | 種別 | 記事での出現 | コンテキスト（前後） |",
                "|---|---|---|---|",
            ]
            for r in results:
                if r["status"] == "WARNING" and r.get("risk") == "HIGH":
                    ctx = r["context"][:60].replace("|", "｜")
                    raw = r["raw_text"][:40].replace("|", "｜")
                    lines.append(
                        f"| `{r['search_term']}` | {r['type']} | `{raw}` | `...{ctx}...` |"
                    )
            lines += [
                "",
                f"→ 個別レポート: `provenance/{meta.get('pdf_stem', '?')}_check.md`",
                "",
            ]
    else:
        lines += [
            "## ✅ HIGH リスク記事なし",
            "",
            "このバッチの全記事で HIGH リスクの候補は検出されませんでした。",
            "",
        ]

    # MEDIUM 要約
    if medium_articles:
        lines += [
            "## 🟡 MEDIUM リスク記事（OCR誤読等・確認推奨）",
            "",
        ]
        for draft_path, meta, results in medium_articles:
            med_warns = [r for r in results if r["status"] == "WARNING" and r.get("risk") == "MEDIUM"]
            terms = ", ".join(f"`{r['search_term']}`" for r in med_warns[:5])
            lines.append(f"- **{draft_path.name}**: {terms}")
        lines.append("")

    lines += [
        "---",
        "",
        "*このレポートは `scripts/generate_provenance.py` によって自動生成されました。*",
        "*HIGH リスクは「PDF に見当たらない」事実を示します。公開前に元 PDF を目視確認してください。*",
    ]

    return "\n".join(lines)


def resolve_article_id(draft_path: Path) -> str:
    """ファイル名から記事ID を抽出する（ai_summary_029_... → #029）"""
    m = re.search(r"ai_summary_(\d+)", draft_path.name)
    return f"#{m.group(1)}" if m else draft_path.stem


def main():
    args = list(sys.argv[1:])
    if not args:
        print("使用方法: python3 scripts/generate_provenance.py <draft_md> [...]")
        print("例（単一）:   python3 scripts/generate_provenance.py note_drafts/ai_summary_029*.md")
        print("例（一括）:   python3 scripts/generate_provenance.py published_articles/ai_summary_02*.md")
        print("例（ラベル）: python3 scripts/generate_provenance.py --batch '#026-#029' published_articles/ai_summary_02[6-9]*.md")
        sys.exit(1)

    # --batch <label> オプション解析
    batch_label = ""
    if args and args[0] == "--batch":
        args.pop(0)
        # 次のトークンがパスでなければラベルとして使用
        if args and not Path(args[0]).exists() and not args[0].startswith("-"):
            batch_label = args.pop(0)

    # glob 展開（シェルが展開しなかった場合も対応）
    target_files = []
    for arg in args:
        p = Path(arg)
        if p.exists():
            target_files.append(p)
        else:
            matches = sorted(PROJECT_ROOT.glob(str(p)))
            if matches:
                target_files.extend(matches)
            else:
                print(f"  [警告] ファイルが見つかりません: {arg}")

    if not target_files:
        print("対象ファイルが0件です。")
        sys.exit(1)

    print("=" * 60)
    print("プロベナンスチェック（generate_provenance.py）")
    print("=" * 60)
    print(f"対象: {len(target_files)}件")
    if batch_label:
        print(f"バッチラベル: {batch_label}")

    batch_results = []
    total_high = 0

    for path in target_files:
        meta_info, results = process_file(path)
        batch_results.append((path, meta_info, results))
        if "error" not in meta_info:
            total_high += meta_info.get("high_count", 0)

    # バッチレポート（2件以上 or --batch 指定時）
    if len(target_files) >= 2 or batch_label:
        report = build_batch_report(batch_results, batch_label)
        REVIEW_LOGS_DIR.mkdir(exist_ok=True)
        # ラベル → ファイル名変換: "#026-#029" → "026-029"
        safe_label = re.sub(r"[#\s]", "", batch_label) if batch_label else "batch"
        safe_label = re.sub(r"[^\w\-]", "_", safe_label)
        report_path = REVIEW_LOGS_DIR / f"provenance_{safe_label}_report.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"\nバッチレポート → {report_path.relative_to(PROJECT_ROOT)}")

    print()
    print("=" * 60)
    n_high   = sum(1 for _, m, _ in batch_results if m.get("article_risk") == "HIGH")
    n_medium = sum(1 for _, m, _ in batch_results if m.get("article_risk") == "MEDIUM")
    n_low    = sum(1 for _, m, _ in batch_results
                  if m.get("article_risk") == "LOW" and "error" not in m)
    print(f"完了: 計{len(batch_results)}件  "
          f"🔴HIGH={n_high}  🟡MEDIUM={n_medium}  🟢LOW={n_low}")
    if total_high > 0:
        print(f"⚠️ HIGH リスク WARNING が {total_high} 件あります。要修正記事を確認してください。")
    elif sum(m.get("warning_count", 0) for _, m, _ in batch_results) > 0:
        print("MEDIUM/LOW のみです。provenance/ フォルダのレポートを参照してください。")
    else:
        print("✅ 全クレームが元PDFで確認できました。")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[中断]")
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
