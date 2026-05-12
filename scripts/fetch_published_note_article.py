#!/usr/bin/env python3
"""
fetch_published_note_article.py — note公開記事取得・Git版差分チェッカー v2

目的:
    自分が公開した無料note記事をHTMLから取得し、
    Git版 published_articles/ との差分を記録する補助ツール。
    正本は引き続き Git 側。このスクリプトは同期補助のみ。

v2 改善点:
    - タイトル取得: <title>タグ → h1(全域) → 本文内h2 の順に試みる
    - noteヘッダーUI除去: 著者名・マガジン名・日付ヘッダーを本文から除去
    - noteフッターUI除去: いいね・チップ・ハッシュタグ等を本文から除去
    - Markdown正規化: URL自動リンク・メタデータ空行の差分ノイズを削減
    - 差分レポート改善: UI差分・フォーマット差分・実質差分を分離表示
    - レポート出力先: review_logs/note_diff_report.md

使用方法:
    python3 scripts/fetch_published_note_article.py <note_url> <article_id>

例:
    python3 scripts/fetch_published_note_article.py https://note.com/user/n/nXXXXX 015

制約:
    - アクセスするのは指定した1記事URLのみ
    - /api/ /pdf/ 等の Disallow パスにはアクセスしない
    - 大量巡回・連続アクセスは行わない
    - 取得失敗は FAILED として記録し、人間コピペ運用へ戻す

出力:
    published_articles/from_note/<article_id>.md  — クリーンなMarkdown
    review_logs/note_diff_report.md               — 差分レポート（追記）

依存:
    requests (pip install requests)
    html.parser (stdlib)
"""

import sys
import os
import re
import difflib
import datetime
import traceback
import json
import html as html_module
from html.parser import HTMLParser
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("[ERROR] requests が必要です: pip install requests")
    sys.exit(1)

# ---- パス定義 ----
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "published_articles", "from_note")
REPORT_PATH = os.path.join(BASE_DIR, "review_logs", "note_diff_report.md")
PUBLISHED_DIR = os.path.join(BASE_DIR, "published_articles")

# robots.txt で Disallow されているパスプレフィックス
DISALLOWED_PATHS = ["/api/", "/pdf/", "/search", "/tags/", "/hashtag/", "/members"]

# 通常記事URL: /username/n/<note_id>
NOTE_ARTICLE_PATTERN = re.compile(r"^/[^/]+/n/[a-zA-Z0-9]+$")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
}

# note.com 記事本文のCSSクラスパターン（複数バージョン対応）
BODY_CLASS_PATTERNS = [
    "note-common-styles__textnote-body",
    "textnote-body",
    "p-article__content__body",
    "p-article__content",
    "m-note__body",
    "o-noteContent__body",
    # v2 追加
    "note-body",
    "article-body",
    "ArticleBody",
    "NoteBody",
    "o-noteContentText",
    "m-articleText",
]

# note UI フッターマーカー（このテキストが出たら記事本文終了）
NOTE_FOOTER_MARKERS = [
    "いいなと思ったら応援しよう",
    "チップで応援",
    "この記事が気に入ったら",
    "フォローする",
    "サポートをする",
]

# フッター直前に出るボタンテキスト・空見出し（後退スキャン用）
NOTE_BUTTON_TEXTS = {"**", "copy", "download", "ダウンロード", "##", "###", "#"}

# UIアーティファクト行の正規表現パターン
NOTE_UI_LINE_PATTERNS = [
    # 著者リンク: [username](https://note.com/username)
    re.compile(r'^\s*\[.{1,40}\]\(https?://note\.com/[^)]+\)'),
    # ** [name](url) ** 形式の著者ブロック
    re.compile(r'^\s*\*\*\s*\[.{1,40}\]\(https?://'),
    # ハッシュタグリンク（note.com/hashtag/）
    re.compile(r'https?://note\.com/hashtag/'),
    # copy/download ボタンテキスト（行全体）
    re.compile(r'^\s*(?:copy|download|ダウンロード)\s*$', re.IGNORECASE),
    # ** のみ行
    re.compile(r'^\s*\*\*\s*$'),
    # 日付+著者のヘッダー行（例: 2026年5月12日 11:04）
    re.compile(r'\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{2}'),
    # いいね/チップ等
    re.compile(r'いいなと思ったら|チップで応援|応援しよう'),
]


# ============================================================
# HTML → Markdown パーサー（stdlib html.parser ベース）
# ============================================================

class NoteArticleHTMLParser(HTMLParser):
    """
    note.com 記事ページから本文 Markdown とタイトルを抽出する。

    v2 戦略:
        1. <title> タグからページタイトルを取得
        2. <h1> タグを全域スキャン（body 内外問わず）
        3. BODY_CLASS_PATTERNS に一致する <div> を本文コンテナとして検出
        4. <article> タグへフォールバック
        5. get_best_title() で最適タイトルを選択
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.page_title: str = ""      # <title> タグ内容
        self.body_markdown: str = ""
        self.parse_method: str = "not_found"

        # <title> タグ
        self._in_title_tag = False
        self._title_tag_buf = ""

        # h1 全域スキャン
        self._in_h1 = False
        self._h1_buf = ""
        self._all_h1: list[str] = []   # 非空 h1 テキスト一覧

        # 本文コンテナ
        self._in_body = False
        self._body_depth = 0           # body コンテナ開始時の div 深さ
        self._global_div_depth = 0     # 全 div の深さ追跡

        self._parts: list[str] = []
        self._link_href: str = ""
        self._skip_tags = {"script", "style", "nav", "footer", "aside"}
        self._skip_depth = 0

    # ---- 内部ヘルパー ----

    def _class_has_body(self, attrs_dict: dict) -> bool:
        cls = attrs_dict.get("class", "")
        return any(p in cls for p in BODY_CLASS_PATTERNS)

    def _attrs_to_dict(self, attrs) -> dict:
        return {k: v or "" for k, v in attrs}

    # ---- HTMLParser フック ----

    def handle_starttag(self, tag: str, attrs):
        attrs_d = self._attrs_to_dict(attrs)

        # <title> タグ（ページタイトル取得）
        if tag == "title" and not self._in_body:
            self._in_title_tag = True
            self._title_tag_buf = ""
            return

        # スキップタグ
        if tag in self._skip_tags:
            self._skip_depth += 1
            return
        if self._skip_depth > 0:
            return

        # グローバル div 深さ追跡
        if tag == "div":
            self._global_div_depth += 1

        # h1 全域スキャン（body 外）
        if tag == "h1" and not self._in_h1 and not self._in_body:
            self._in_h1 = True
            self._h1_buf = ""
            return

        # 本文コンテナ検出
        if not self._in_body:
            if tag == "div" and self._class_has_body(attrs_d):
                self._in_body = True
                self._body_depth = self._global_div_depth
                self.parse_method = "class_match"
                return
            if tag == "article":
                self._in_body = True
                self._body_depth = -1   # -1 = article モード
                self.parse_method = "article_tag"
                return
            return

        # 本文内の変換処理
        self._convert_open_tag(tag, attrs_d)

    def handle_endtag(self, tag: str):
        # <title> 終了
        if tag == "title" and self._in_title_tag:
            self._in_title_tag = False
            self.page_title = self._title_tag_buf.strip()
            return

        # スキップタグ終了
        if tag in self._skip_tags:
            if self._skip_depth > 0:
                self._skip_depth -= 1
            return
        if self._skip_depth > 0:
            return

        # h1 終了（body 外）
        if tag == "h1" and self._in_h1 and not self._in_body:
            self._in_h1 = False
            text = self._h1_buf.strip()
            if text:
                self._all_h1.append(text)
            return

        # グローバル div 深さ管理
        if tag == "div":
            if self._in_body and self._body_depth >= 0:
                if self._global_div_depth <= self._body_depth:
                    self._in_body = False
                    self.body_markdown = self._clean_markdown("".join(self._parts))
            self._global_div_depth -= 1
            return

        # article 終了
        if tag == "article" and self._in_body and self._body_depth == -1:
            self._in_body = False
            self.body_markdown = self._clean_markdown("".join(self._parts))
            return

        if not self._in_body:
            return

        self._convert_close_tag(tag)

    def handle_data(self, data: str):
        if self._in_title_tag:
            self._title_tag_buf += data
            return
        if self._skip_depth > 0:
            return
        if self._in_h1 and not self._in_body:
            self._h1_buf += data
        elif self._in_body:
            self._parts.append(data)

    def get_best_title(self) -> str:
        """利用可能な情報から最適なタイトルを返す。優先順: <title> > h1。"""
        # 1. <title> タグから "記事タイトル｜note" 形式を分解
        if self.page_title:
            for sep in ["｜", "|", " - ", " – "]:
                if sep in self.page_title:
                    candidate = self.page_title.split(sep)[0].strip()
                    if candidate and candidate.lower() not in {"note", ""}:
                        return candidate
            if self.page_title.lower() not in {"note", ""}:
                return self.page_title

        # 2. h1 テキスト（非空かつ十分な長さのもの）
        for h1 in self._all_h1:
            if h1 and len(h1) > 5:
                return h1

        return ""

    # ---- タグ変換ロジック ----

    def _convert_open_tag(self, tag: str, attrs_d: dict):
        if tag == "h1":
            self._parts.append("\n# ")
        elif tag == "h2":
            self._parts.append("\n## ")
        elif tag == "h3":
            self._parts.append("\n### ")
        elif tag == "h4":
            self._parts.append("\n#### ")
        elif tag == "p":
            self._parts.append("\n")
        elif tag == "br":
            self._parts.append("  \n")
        elif tag == "hr":
            self._parts.append("\n---\n")
        elif tag in ("strong", "b"):
            self._parts.append("**")
        elif tag in ("em", "i"):
            self._parts.append("*")
        elif tag == "a":
            self._link_href = attrs_d.get("href", "")
            self._parts.append("[")
        elif tag == "li":
            self._parts.append("\n- ")
        elif tag == "blockquote":
            self._parts.append("\n> ")
        elif tag == "code":
            self._parts.append("`")
        elif tag == "pre":
            self._parts.append("\n```\n")

    def _convert_close_tag(self, tag: str):
        if tag in ("h1", "h2", "h3", "h4"):
            self._parts.append("\n")
        elif tag == "p":
            self._parts.append("\n")
        elif tag in ("strong", "b"):
            self._parts.append("**")
        elif tag in ("em", "i"):
            self._parts.append("*")
        elif tag == "a":
            href = self._link_href
            self._parts.append(f"]({href})" if href else "]")
            self._link_href = ""
        elif tag == "blockquote":
            self._parts.append("\n")
        elif tag == "code":
            self._parts.append("`")
        elif tag == "pre":
            self._parts.append("\n```\n")

    @staticmethod
    def _clean_markdown(text: str) -> str:
        """連続空行・行末空白を整理する。"""
        text = "\n".join(line.rstrip() for line in text.splitlines())
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


# ============================================================
# JSON 抽出フォールバック（Next.js __NEXT_DATA__ 等）
# ============================================================

def extract_from_json_script(html_text: str) -> tuple[str, str]:
    """
    Next.js の __NEXT_DATA__ や application/ld+json から
    タイトルと本文テキストを抽出する（フォールバック）。

    Returns:
        (title, body_text) または ("", "")
    """
    # __NEXT_DATA__ を探す
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_text, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(1))
            props = data.get("props", {}).get("pageProps", {})
            note = props.get("note", {})
            title = note.get("name", "") or note.get("title", "")
            body = note.get("body", "") or note.get("content", "")
            if title or body:
                return title, body
        except (json.JSONDecodeError, KeyError):
            pass

    # application/ld+json を探す
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html_text, re.DOTALL):
        try:
            data = json.loads(m.group(1))
            title = data.get("headline", "") or data.get("name", "")
            body = data.get("articleBody", "") or data.get("description", "")
            if title:
                return title, body
        except json.JSONDecodeError:
            pass

    return "", ""


# ============================================================
# note UI アーティファクト除去
# ============================================================

def post_process_note_body(raw_markdown: str) -> tuple[str, str]:
    """
    note.com の UI アーティファクトを除去し、クリーンな本文を返す。

    article_tag フォールバック時に混入する:
      - 著者名・マガジン名・日付のヘッダーブロック
      - ダウンロード・copy ボタン
      - いいなと思ったら応援・チップ・ハッシュタグのフッター

    Returns:
        (article_title, clean_body)
        - article_title: 本文内の最初の見出しから取得（空文字の場合もあり）
        - clean_body: UI除去後のMarkdown
    """
    lines = raw_markdown.splitlines()

    # === 1. フッターUI除去 ===
    footer_start = len(lines)
    for i, line in enumerate(lines):
        if any(marker in line for marker in NOTE_FOOTER_MARKERS):
            footer_start = i
            break

    # フッター直前のボタンUI（ダウンロード・copy・** のみ行）も除去
    # 後退スキャン: フッターより前の空行・ボタン行を除去
    trim_end = footer_start
    i = trim_end - 1
    while i >= 0:
        stripped = lines[i].strip()
        if not stripped:          # 空行はスキップ
            i -= 1
            continue
        if stripped in NOTE_BUTTON_TEXTS:
            trim_end = i          # このボタン行まで除去範囲を拡大
            i -= 1
            continue
        break                     # 通常テキスト行に当たったら終了

    lines = lines[:trim_end]

    # 末尾の空行を除去
    while lines and not lines[-1].strip():
        lines.pop()

    # === 2. ヘッダーUI除去 ===
    # article_tag フォールバック時、記事本文の前に
    # マガジン名・著者名・日付のUIが含まれる。
    # 最初の見出し行（## または # ）を記事開始点とする。
    content_start = 0
    article_title_from_body = ""

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## "):
            article_title_from_body = stripped[3:].strip()
            content_start = i
            break
        if stripped.startswith("# ") and stripped[2:].strip():
            article_title_from_body = stripped[2:].strip()
            content_start = i
            break

    body_lines = lines[content_start:]

    # 最初の ## 見出しを # (h1) に変換（Gitドラフトと合わせる）
    if body_lines:
        first = body_lines[0].strip()
        if first.startswith("## "):
            body_lines[0] = "# " + first[3:]

    # === 3. 行単位 UIパターン除去 ===
    filtered_lines = []
    for line in body_lines:
        is_ui = any(p.search(line) for p in NOTE_UI_LINE_PATTERNS)
        if not is_ui:
            filtered_lines.append(line)

    clean_body = "\n".join(filtered_lines)
    clean_body = re.sub(r'\n{3,}', '\n\n', clean_body).strip()

    return article_title_from_body, clean_body


# ============================================================
# 差分ノイズ削減のための正規化
# ============================================================

def normalize_for_diff(text: str) -> str:
    """
    内容は変えずにフォーマット差異を吸収する正規化。

    正規化対象:
    1. URLの自動リンク化: [url](url) → url （同一テキスト・URL の場合）
    2. note メタデータリスト空行: "- \\n\\n**key：**" → "- **key：**"
    3. 連続空行の圧縮
    4. 行末スペース除去
    """

    # 1. [text](url) where text ≈ url → text のみ
    def delink(m: re.Match) -> str:
        text_part = m.group(1).strip()
        url_part  = m.group(2).strip()
        t_norm = text_part.lower().rstrip("/")
        u_norm = url_part.lower().rstrip("/")
        # 完全一致、または http/https 違い
        if t_norm == u_norm:
            return text_part
        u_stripped = re.sub(r'^https?://', '', u_norm)
        if t_norm == u_stripped or t_norm.upper() == u_stripped.upper():
            return text_part
        return m.group(0)   # 変換しない

    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', delink, text)

    # 2. メタデータ/出典リスト項目の改行除去
    #    パターン A: "-\ntext" → "- text"   （-のみ行の直後にコンテンツ）
    #    パターン B: "-\n\n**key" → "- **key"  （-のみ行 + 空行 + bold コンテンツ）
    #    note の <li>text</li> や <li><p>text</p></li> パターンによる改行混入を吸収する
    text = re.sub(r'(?m)^-\s*\n(\S)', r'- \1', text)           # パターン A
    text = re.sub(r'(?m)^-\s*\n\s*\n(\S)', r'- \1', text)      # パターン B

    # 3. 連続空行圧縮
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 4. 行末スペース除去
    text = "\n".join(line.rstrip() for line in text.splitlines())

    return text.strip()


# ============================================================
# 差分のカテゴリ分類
# ============================================================

def categorize_diff(diff: str) -> dict[str, list[str]]:
    """
    unified diff 行をカテゴリ分類する。

    Categories:
        "ui":      note.com UIアーティファクト行（著者ヘッダー・ハッシュタグ等）
        "format":  Markdownフォーマット差異（内容同一・空行・URLリンク化等）
        "content": 実質的な内容差異
        "context": コンテキスト行
        "header":  diff ヘッダー行（---/+++/@@）
    """
    categories: dict[str, list[str]] = {
        "ui": [], "format": [], "content": [], "context": [], "header": []
    }

    for line in diff.splitlines():
        # diff ヘッダー
        if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
            categories["header"].append(line)
            continue

        # コンテキスト行（変更なし）
        if not line.startswith("+") and not line.startswith("-"):
            categories["context"].append(line)
            continue

        text = line[1:]   # +/- を除いたテキスト

        # UIアーティファクト判定
        is_ui = (
            any(p.search(text) for p in NOTE_UI_LINE_PATTERNS)
            or any(marker in text for marker in NOTE_FOOTER_MARKERS)
        )
        if is_ui:
            categories["ui"].append(line)
            continue

        # フォーマット差異判定
        text_stripped = text.strip()
        is_format = (
            not text_stripped                                           # 空行
            or text_stripped in {"**", "-", "---"}                     # 記号のみ
            or bool(re.match(r'\[https?://', text_stripped))           # URL自動リンク行
            or bool(re.match(r'https?://', text_stripped))             # 裸URL行
            or text_stripped == "copy"                                  # copy ボタン残滓
        )
        if is_format:
            categories["format"].append(line)
            continue

        categories["content"].append(line)

    return categories


# ============================================================
# コア処理
# ============================================================

def check_url_allowed(url: str) -> None:
    """URL が対象範囲内かチェックする。問題があれば ValueError を raise。"""
    parsed = urlparse(url)
    if "note.com" not in parsed.netloc:
        raise ValueError(f"note.com 以外のURLは対象外です: {url}")
    for path in DISALLOWED_PATHS:
        if parsed.path.startswith(path):
            raise ValueError(f"アクセス禁止パスです ({path}): {parsed.path}")
    if not NOTE_ARTICLE_PATTERN.match(parsed.path):
        raise ValueError(
            f"通常記事URL パターン (/username/n/nXXXXX) に一致しません: {parsed.path}"
        )


def fetch_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
    resp.raise_for_status()
    return resp.text


def parse_article(html_text: str) -> dict:
    """HTML からタイトル・本文 Markdown を抽出する。複数戦略を試みる。"""
    parser = NoteArticleHTMLParser()
    parser.feed(html_text)

    title = parser.get_best_title()
    raw_body = parser.body_markdown
    method = parser.parse_method

    # HTMLパーサーで本文が取れなかった場合、JSON フォールバック
    if not raw_body:
        j_title, j_body = extract_from_json_script(html_text)
        if j_body:
            title = j_title or title
            raw_body = j_body
            method = "json_fallback"

    if not raw_body:
        raise ValueError(
            "記事本文を抽出できませんでした。\n"
            "note.com のHTML構造が変更されたか、ログインが必要なページの可能性があります。\n"
            "手動でコピーして published_articles/from_note/<id>.md に保存してください。"
        )

    # note UI アーティファクト除去
    body_title, clean_body = post_process_note_body(raw_body)

    # タイトル優先順: <title>タグ / h1 > 本文内 h2
    if not title and body_title:
        title = body_title

    return {
        "title": title,
        "body": clean_body,
        "method": method,
        "char_count": len(clean_body),
        "line_count": clean_body.count("\n") + 1,
        "raw_body": raw_body,   # デバッグ用
        "body_title": body_title,
    }


def find_git_draft(article_id: str) -> str | None:
    """published_articles/ から記事IDに対応するファイルを探す。"""
    pattern = re.compile(rf"ai_(?:summary|reading)_{article_id}[_.]")
    for fname in sorted(os.listdir(PUBLISHED_DIR)):
        if pattern.search(fname) and fname.endswith(".md"):
            return os.path.join(PUBLISHED_DIR, fname)
    return None


def make_diff(text_a: str, text_b: str, label_a: str, label_b: str) -> str:
    """unified diff を生成する。"""
    lines_a = text_a.splitlines(keepends=True)
    lines_b = text_b.splitlines(keepends=True)
    diff = difflib.unified_diff(lines_a, lines_b, fromfile=label_a, tofile=label_b, n=3)
    return "".join(diff)


def diff_stats(diff: str) -> tuple[int, int]:
    """unified diff から (+行数, -行数) を返す。"""
    added   = sum(1 for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff.splitlines() if l.startswith("-") and not l.startswith("---"))
    return added, removed


# ============================================================
# レポート出力
# ============================================================

def init_report() -> None:
    """レポートファイルが存在しない場合はヘッダーを作成する。"""
    if not os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("# note公開版 差分レポート\n\n")
            f.write("このファイルは `scripts/fetch_published_note_article.py` によって自動更新されます。\n\n")
            f.write("## 差分カテゴリの説明\n\n")
            f.write("| カテゴリ | 説明 |\n|---|---|\n")
            f.write("| UIアーティファクト | note.com の著者ヘッダー・ハッシュタグ・いいね/チップUI等 |\n")
            f.write("| Markdownフォーマット差異 | 空行・URLリンク化・リスト整形等（内容は同一） |\n")
            f.write("| **実質的な内容差異** | **実際の本文変更（Git版に反映が必要な可能性あり）** |\n\n")


def write_diff_report(
    article_id: str,
    url: str,
    result: dict,
    git_file: str | None,
    diff_raw: str,
    diff_normalized: str,
    categories: dict,
    status: str,
    error: str = "",
) -> None:
    """note_diff_report.md に差分分析レポートを追記する。"""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    note_rel = os.path.relpath(os.path.join(OUT_DIR, f"{article_id}.md"), BASE_DIR)
    git_rel = os.path.relpath(git_file, BASE_DIR) if git_file else None

    with open(REPORT_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n---\n\n")
        f.write(f"## {ts} — 記事 #{article_id}\n\n")

        # 基本情報テーブル
        f.write(f"| 項目 | 内容 |\n|---|---|\n")
        f.write(f"| URL | {url} |\n")
        f.write(f"| ステータス | **{status}** |\n")
        if error:
            f.write(f"| エラー | {error} |\n")
        if result:
            title_display = result.get("title") or f"（本文内: {result.get('body_title', '不明')}）"
            f.write(f"| 取得タイトル | {title_display} |\n")
            f.write(f"| 抽出方式 | {result.get('method', '?')} |\n")
            f.write(f"| 文字数（クリーン後） | {result.get('char_count', 0)} 文字 |\n")
            f.write(f"| 行数（クリーン後） | {result.get('line_count', 0)} 行 |\n")
            f.write(f"| 保存先 | `{note_rel}` |\n")
        if git_rel:
            f.write(f"| Git版 | `{git_rel}` |\n")

        # 差分分析
        if status.startswith("SUCCESS") and git_file:
            if not diff_raw:
                f.write(f"\n**差分なし — Git版と完全一致**\n")
                return

            n_ui      = len(categories.get("ui",      []))
            n_fmt     = len(categories.get("format",  []))
            n_content = len(categories.get("content", []))
            added_raw,  removed_raw  = diff_stats(diff_raw)
            added_norm, removed_norm = diff_stats(diff_normalized) if diff_normalized else (0, 0)

            f.write(f"\n### 差分サマリー\n\n")
            f.write(f"| カテゴリ | +行 / -行 | 備考 |\n|---|---|---|\n")
            f.write(f"| 全体差分（生） | +{added_raw} / -{removed_raw} | note取得(クリーン後) vs Git版 |\n")
            f.write(f"| 全体差分（正規化後） | +{added_norm} / -{removed_norm} | フォーマット差異除去後 |\n")
            f.write(f"| UIアーティファクト | {n_ui} 行 | 著者ヘッダー・ハッシュタグ等 |\n")
            f.write(f"| Markdownフォーマット差異 | {n_fmt} 行 | 空行・URLリンク化等 |\n")
            f.write(f"| **実質的な内容差異** | **{n_content} 行** | Git版との本文差分 |\n")

            if n_content == 0:
                f.write(f"\n**判定: Git版 ≈ note公開版（実質内容は同一）**\n")
            else:
                f.write(f"\n> ⚠️ **判定: 実質的な内容差異あり（要確認: {n_content}行）**\n")

            # 実質差分（内容がある場合のみ表示）
            if n_content > 0:
                f.write(f"\n#### 実質的な内容差異\n\n```diff\n")
                for line in categories["content"]:
                    f.write(line + "\n")
                f.write("```\n")

            # UIアーティファクト差分（折りたたみ）
            if n_ui > 0:
                f.write(f"\n<details><summary>UIアーティファクト差分（{n_ui}行・除去済み）</summary>\n\n```diff\n")
                for line in categories["ui"]:
                    f.write(line + "\n")
                f.write("```\n</details>\n")

            # フォーマット差異（折りたたみ）
            if n_fmt > 0:
                f.write(f"\n<details><summary>Markdownフォーマット差異（{n_fmt}行）</summary>\n\n```diff\n")
                for line in categories["format"]:
                    f.write(line + "\n")
                f.write("```\n</details>\n")

            # 全差分（デバッグ用・折りたたみ）
            f.write(f"\n<details><summary>全差分 unified diff（デバッグ用）</summary>\n\n```diff\n")
            diff_lines = diff_raw.splitlines()
            if len(diff_lines) > 150:
                f.write("\n".join(diff_lines[:150]))
                f.write(f"\n... (残り {len(diff_lines) - 150} 行を省略)\n")
            else:
                f.write(diff_raw)
            f.write("\n```\n</details>\n")

        elif not git_file and status.startswith("SUCCESS"):
            f.write(f"\n⚠️ Git版ファイルが見つかりませんでした。比較不可。\n")


# ============================================================
# メイン
# ============================================================

def main():
    if len(sys.argv) < 3:
        print("使用方法: python3 scripts/fetch_published_note_article.py <note_url> <article_id>")
        print("例:       python3 scripts/fetch_published_note_article.py https://note.com/user/n/nXXXXX 015")
        sys.exit(1)

    url = sys.argv[1].strip().rstrip("/")
    # クエリパラメータを除去（?app_launch=false 等）
    url = url.split("?")[0]
    article_id = sys.argv[2].strip().zfill(3)   # "15" → "015"

    os.makedirs(OUT_DIR, exist_ok=True)
    init_report()

    print(f"[INFO] 記事 #{article_id} の取得を開始します")
    print(f"[INFO] URL: {url}")

    # ---- URL 検証 ----
    try:
        check_url_allowed(url)
        print("[INFO] URLチェック: OK")
    except ValueError as e:
        print(f"[ERROR] URLチェック失敗: {e}")
        write_diff_report(article_id, url, {}, None, "", "", {}, "BLOCKED", str(e))
        sys.exit(1)

    result: dict = {}
    git_file: str | None = None
    diff_raw = ""
    diff_normalized = ""
    categories: dict = {}
    status = "FAILED"
    error_msg = ""

    try:
        # ---- HTML 取得 ----
        print("[INFO] HTMLを取得中...")
        html_text = fetch_html(url)
        print(f"[INFO] HTML取得完了 ({len(html_text):,} bytes)")

        # ---- 本文抽出 + UI除去 ----
        print("[INFO] 記事本文を抽出中...")
        result = parse_article(html_text)
        print(f"[INFO] 抽出完了 | 方式: {result['method']} | "
              f"タイトル: 「{result['title'][:50] or result['body_title'][:50]}」 | "
              f"{result['char_count']}文字 / {result['line_count']}行")

        # ---- note版 保存（クリーン版） ----
        # body はすでに post_process_note_body で "# タイトル" を先頭に含む。
        # title を重複して付けない。
        out_path = os.path.join(OUT_DIR, f"{article_id}.md")
        note_content = result['body'] + "\n"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(note_content)
        print(f"[INFO] 保存: published_articles/from_note/{article_id}.md")

        # ---- Git版との差分 ----
        git_file = find_git_draft(article_id)
        if git_file:
            with open(git_file, encoding="utf-8") as f:
                git_content = f.read()

            # 生差分
            diff_raw = make_diff(
                git_content,
                note_content,
                f"git:{os.path.basename(git_file)}",
                f"note:{article_id}.md",
            )

            # 正規化後差分
            git_norm  = normalize_for_diff(git_content)
            note_norm = normalize_for_diff(note_content)
            diff_normalized = make_diff(
                git_norm,
                note_norm,
                f"git(norm):{os.path.basename(git_file)}",
                f"note(norm):{article_id}.md",
            )

            # カテゴリ分類（正規化後差分から実施: フォーマット差異を除外した実質差分を得る）
            categories = categorize_diff(diff_normalized)

            if diff_raw:
                added_raw, removed_raw = diff_stats(diff_raw)
                added_norm, removed_norm = diff_stats(diff_normalized)
                n_content = len(categories.get("content", []))
                print(f"[INFO] 生差分: +{added_raw} / -{removed_raw}")
                print(f"[INFO] 正規化後差分: +{added_norm} / -{removed_norm}")
                print(f"[INFO] UIアーティファクト: {len(categories.get('ui', []))}行")
                print(f"[INFO] フォーマット差異: {len(categories.get('format', []))}行")
                print(f"[INFO] 実質内容差異: {n_content}行")
                if n_content == 0:
                    print("[INFO] 判定: Git版 ≈ note公開版（実質内容は同一）")
                else:
                    print(f"[WARN] 判定: 実質的な内容差異あり（{n_content}行）— 要確認")
            else:
                print("[INFO] Git版と完全一致（差分なし）")
        else:
            print(f"[WARN] published_articles/ に #{article_id} のファイルが見つかりません")

        status = "SUCCESS"

    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTPエラー: {e.response.status_code} {e.response.reason}"
        print(f"[ERROR] {error_msg}")
    except requests.exceptions.ConnectionError:
        error_msg = "接続エラー（ネットワーク不可またはnote.com障害）"
        print(f"[ERROR] {error_msg}")
    except requests.exceptions.Timeout:
        error_msg = "タイムアウト（15秒）"
        print(f"[ERROR] {error_msg}")
    except ValueError as e:
        error_msg = str(e)
        print(f"[ERROR] {error_msg}")
    except Exception as e:
        error_msg = f"{type(e).__name__}: {e}"
        print(f"[ERROR] 予期しないエラー: {error_msg}")
        traceback.print_exc()

    write_diff_report(
        article_id, url, result, git_file,
        diff_raw, diff_normalized, categories,
        status, error_msg,
    )
    print(f"[INFO] レポート追記: review_logs/note_diff_report.md")
    print(f"[INFO] 終了ステータス: {status}")
    sys.exit(0 if status == "SUCCESS" else 1)


if __name__ == "__main__":
    main()
