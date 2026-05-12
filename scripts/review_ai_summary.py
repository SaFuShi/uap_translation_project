#!/usr/bin/env python3
"""
scripts/review_ai_summary.py

AI概要版記事の品質チェックスクリプト
目的: note公開前に「煽りすぎ」「断定しすぎ」「長すぎ」「出典不足」などを検出する

入力: note_drafts/ai_*.md
出力: review_logs/article_review_report.md

使い方:
    python3 scripts/review_ai_summary.py
    python3 scripts/review_ai_summary.py note_drafts/ai_reading_009.md  # 1ファイル指定
"""

import re
import sys
import glob
from datetime import datetime
from pathlib import Path

# ==================== パス設定 ====================

PROJECT_ROOT = Path(__file__).parent.parent
NOTE_DRAFTS_DIR = PROJECT_ROOT / "note_drafts"
REVIEW_LOGS_DIR = PROJECT_ROOT / "review_logs"
OUTPUT_FILE = REVIEW_LOGS_DIR / "article_review_report.md"

# ==================== チェック設定 ====================

# 行数チェック
LINE_WARNING_THRESHOLD = 100  # これ以上は WARNING
LINE_TARGET_MAX = 90          # 目標上限（INFO）
LINE_TARGET_MIN = 60          # これ以下は INFO（短すぎる可能性）

# --- 強い表現（ERROR：即座に問題となる断定・誇張） ---
STRONG_EXPRESSIONS_ERROR = [
    (r"UFO[であだとはが]|これはUFO|それはUFO|ＵＦＯである", "「UFO」と断定する表現"),
    (r"宇宙人", "「宇宙人」という表現"),
    (r"エイリアン", "「エイリアン」という表現"),
    (r"地球外生命[体物]", "「地球外生命」という表現"),
    (r"間違いない[。」\s]", "「間違いない」という断定表現"),
    (r"証明され[たてる]|証明した", "「証明」という断定表現"),
    # 「確認」は一般的すぎるため除外。UFO断定・宇宙人などに限定する
]

# --- 強い表現（WARNING：過剰になりやすい表現） ---
STRONG_EXPRESSIONS_WARNING = [
    (r"原因不明[だであ][。」\s]|原因不明です[。」]", "「原因不明」の断定（留保なし）"),
    # 「増殖した」「分裂した」は注意点での否定文脈（「〜したとは」）は誤検出になるため文末に限定
    (r"増殖した[。」\s]|分裂した[。」\s]", "「増殖」「分裂」という断定表現"),
    (r"謎の物体[がをはで]", "「謎の物体」という断定表現"),
    (r"直接的な証拠", "「直接的な証拠」という強い表現"),
    # 「確定した発言ではありません」などの否定文脈はスキップ
    (r"(?:確定|断定)し[たてる](?!.*ではあり|.*ではない|.*わけでは)", "「確定」「断定」という表現"),
    (r"説明がつかない[。」\s]", "「説明がつかない」という断定"),
    (r"未解明の現象|未解明だ[。」]", "「未解明」という断定表現"),
    (r"ありえない|あり得ない", "「ありえない」という断定"),
    (r"飛び抜けた能力|超常現象", "超常現象を示唆する表現"),
]

# --- 文書種別キーワード（いずれか1つあればOK） ---
DOCUMENT_TYPE_KEYWORDS = [
    "観測記録", "会話記録", "目撃証言", "報告書",
    "フォーム", "ブリーフィング", "トランスクリプト",
    "デブリーフィング", "供述", "報告会",
    "記録です", "記録されています", "文書です",
    "記録した", "記録しています",
]

# --- 自然説明キーワード（いずれか1つあればOK） ---
NATURAL_EXPLANATION_KEYWORDS = [
    "水ボイラー", "S-IVB", "プラズマ", "宇宙線",
    "反射光", "排気", "破片", "氷の塊", "ALFMED",
    "電磁干渉", "EMI", "光学的な", "通常の現象",
    "湖の反射", "第3段ロケット", "SLAパネル",
    "かもしれない", "ではないかと", "可能性がある",
    "と考えられ", "と読み取れ", "と述べて",
]

# --- OCR技術説明キーワード（AI解析メモ行以外にあると WARNING） ---
OCR_TECH_PATTERNS = [
    r"Tesseract",
    r"PSM[0-9]",
    r"Adobe Acrobat Paper Capture",
    r"typed_text分類",
    r"テキスト抽出成功",
    r"OCR成功率",
]

# --- 免責事項キーワード（全部あればOK） ---
DISCLAIMER_KEYWORDS = ["AI概要版", "OCR誤認識", "詳細解析版"]

# --- セクション名 ---
NOTES_SECTION_HEADER  = "## 注意点"
SOURCE_SECTION_HEADER = "## 出典"
ANALYSIS_MEMO_LABEL   = "AI解析メモ"

# --- 英文引用の長さ ---
ENGLISH_BLOCKQUOTE_WARN_LINES = 4   # blockquote内の英語行がこれ以上で WARNING
ENGLISH_BLOCKQUOTE_MAX_CHARS  = 400  # 英語引用の文字数合計がこれ以上で WARNING


# ==================== ユーティリティ ====================

def load_file(path: Path) -> tuple[list[str], str]:
    """ファイルを読み込み、行リストと全文を返す"""
    text = path.read_text(encoding="utf-8")
    return text.splitlines(), text


def extract_section(lines: list[str], header: str) -> list[str]:
    """指定ヘッダーから次の ## ヘッダーまでの行を返す"""
    in_section = False
    result = []
    for line in lines:
        if line.strip().startswith(header):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            result.append(line)
    return result


def find_analysis_memo_line(lines: list[str]) -> str:
    """AI解析メモの行を返す（1行）"""
    for line in lines:
        if ANALYSIS_MEMO_LABEL in line:
            return line
    return ""


def is_in_memo_line(line: str) -> bool:
    return ANALYSIS_MEMO_LABEL in line


def find_pdf_url_in_sources(lines: list[str]) -> str:
    """出典セクション内のPDF URLを返す"""
    source_lines = extract_section(lines, SOURCE_SECTION_HEADER)
    for line in source_lines:
        match = re.search(r"https://[^\s)]+\.pdf", line)
        if match:
            return match.group(0)
    return ""


def extract_english_blockquotes(lines: list[str]) -> list[tuple[int, list[str]]]:
    """
    blockquote (> で始まる行) の連続ブロックを返す。
    各ブロック: (開始行番号, 行リスト)
    """
    blocks = []
    current_block = []
    start_line = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(">"):
            content = stripped[1:].strip()
            if re.search(r"[a-zA-Z]{3,}", content):  # 英語が含まれる行
                if not current_block:
                    start_line = i
                current_block.append(content)
            elif current_block:
                blocks.append((start_line, current_block))
                current_block = []
                start_line = -1
        else:
            if current_block:
                blocks.append((start_line, current_block))
                current_block = []
                start_line = -1
    if current_block:
        blocks.append((start_line, current_block))
    return blocks


def find_ocr_tech_in_body(lines: list[str]) -> list[tuple[int, str]]:
    """
    AI解析メモ行以外でOCR技術キーワードが出てくる行を返す
    """
    findings = []
    for i, line in enumerate(lines):
        if is_in_memo_line(line):
            continue
        for pattern in OCR_TECH_PATTERNS:
            if re.search(pattern, line):
                findings.append((i + 1, line.strip()[:80]))
                break
    return findings


# ==================== チェック関数群 ====================

class Finding:
    """チェック結果の1件"""
    def __init__(self, level: str, category: str, detail: str, line_no: int = 0):
        self.level = level      # "ERROR" / "WARNING" / "INFO"
        self.category = category
        self.detail = detail
        self.line_no = line_no

    def __repr__(self):
        loc = f" (行{self.line_no})" if self.line_no else ""
        return f"[{self.level}] {self.category}: {self.detail}{loc}"


def check_line_count(lines: list[str]) -> list[Finding]:
    findings = []
    n = len(lines)
    if n > LINE_WARNING_THRESHOLD:
        findings.append(Finding("WARNING", "行数", f"{n}行（目標上限: {LINE_TARGET_MAX}行）"))
    elif n > LINE_TARGET_MAX:
        findings.append(Finding("INFO", "行数", f"{n}行（目標上限: {LINE_TARGET_MAX}行）"))
    elif n < LINE_TARGET_MIN:
        findings.append(Finding("INFO", "行数", f"{n}行（目標下限: {LINE_TARGET_MIN}行・短い可能性あり）"))
    return findings


def check_strong_expressions(lines: list[str]) -> list[Finding]:
    findings = []
    for i, line in enumerate(lines, 1):
        # 引用行（>）はチェックを緩める（原文引用なので）
        is_quote = line.strip().startswith(">")

        for pattern, label in STRONG_EXPRESSIONS_ERROR:
            if re.search(pattern, line):
                level = "INFO" if is_quote else "ERROR"
                findings.append(Finding(level, "強い表現", f"{label} → 「{line.strip()[:60]}」", i))

        if not is_quote:
            for pattern, label in STRONG_EXPRESSIONS_WARNING:
                if re.search(pattern, line):
                    findings.append(Finding("WARNING", "強い表現", f"{label} → 「{line.strip()[:60]}」", i))

    return findings


def check_document_type_declaration(text: str) -> list[Finding]:
    for kw in DOCUMENT_TYPE_KEYWORDS:
        if kw in text:
            return []
    return [Finding("WARNING", "文書種別", "「観測記録」「会話記録」「目撃証言フォーム」などの文書種別が明示されていない可能性があります")]


def check_natural_explanation(text: str) -> list[Finding]:
    for kw in NATURAL_EXPLANATION_KEYWORDS:
        if kw in text:
            return []
    return [Finding("INFO", "自然説明", "本文中に自然説明・留保表現が見当たりません。目撃者の自己解説がある場合は記載を検討してください")]


def check_source_section(lines: list[str]) -> list[Finding]:
    findings = []
    source_lines = extract_section(lines, SOURCE_SECTION_HEADER)
    full_source = "\n".join(source_lines)

    if not source_lines:
        findings.append(Finding("ERROR", "出典", "「## 出典」セクションが見当たりません"))
        return findings

    # 元PDFのURLチェック
    has_pdf_label = bool(re.search(r"元PDF[：:]", full_source))
    has_pdf_url   = bool(re.search(r"https://[^\s)]+\.pdf", full_source))

    if not has_pdf_label:
        findings.append(Finding("WARNING", "出典", "「元PDF：」の行が出典セクションにありません"))
    if not has_pdf_url:
        findings.append(Finding("WARNING", "出典", "出典セクションにPDFのURLが含まれていません"))

    return findings


def check_disclaimer(text: str) -> list[Finding]:
    missing = [kw for kw in DISCLAIMER_KEYWORDS if kw not in text]
    if missing:
        return [Finding("WARNING", "免責事項", f"免責事項に以下が見当たりません: {', '.join(missing)}")]
    return []


def check_notes_section(lines: list[str]) -> list[Finding]:
    for line in lines:
        if line.strip().startswith(NOTES_SECTION_HEADER):
            return []
    return [Finding("WARNING", "注意点セクション", "「## 注意点」セクションが見当たりません")]


def check_english_blockquotes(lines: list[str]) -> list[Finding]:
    findings = []
    blocks = extract_english_blockquotes(lines)
    for start_line, block_lines in blocks:
        if len(block_lines) >= ENGLISH_BLOCKQUOTE_WARN_LINES:
            total_chars = sum(len(l) for l in block_lines)
            findings.append(Finding(
                "WARNING", "英文引用",
                f"英文blockquoteが{len(block_lines)}行・{total_chars}文字あります（目安: {ENGLISH_BLOCKQUOTE_WARN_LINES}行未満）。要約への切り替えを検討してください",
                start_line + 1
            ))
    return findings


def check_ocr_tech_in_body(lines: list[str]) -> list[Finding]:
    occurrences = find_ocr_tech_in_body(lines)
    if not occurrences:
        return []
    findings = []
    for line_no, snippet in occurrences[:3]:  # 最大3件まで表示
        findings.append(Finding(
            "INFO", "OCR技術説明",
            f"AI解析メモ以外の本文にOCR技術キーワードがあります → 「{snippet}」",
            line_no
        ))
    if len(occurrences) > 3:
        findings.append(Finding("INFO", "OCR技術説明", f"他 {len(occurrences) - 3} 件"))
    return findings


# ==================== メイン処理 ====================

def review_file(path: Path) -> tuple[str, list[Finding]]:
    """1ファイルをレビューし、(ファイル名, findings) を返す"""
    lines, text = load_file(path)
    findings = []

    findings += check_line_count(lines)
    findings += check_strong_expressions(lines)
    findings += check_document_type_declaration(text)
    findings += check_natural_explanation(text)
    findings += check_source_section(lines)
    findings += check_disclaimer(text)
    findings += check_notes_section(lines)
    findings += check_english_blockquotes(lines)
    findings += check_ocr_tech_in_body(lines)

    return path.name, findings


def verdict(findings: list[Finding]) -> str:
    levels = {f.level for f in findings}
    if "ERROR" in levels:
        return "❌ 要修正"
    if "WARNING" in levels:
        return "⚠️ 要確認"
    if "INFO" in levels:
        return "💬 参考情報あり"
    return "✅ 問題なし"


def count_by_level(findings: list[Finding]) -> dict:
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    for f in findings:
        counts[f.level] = counts.get(f.level, 0) + 1
    return counts


def build_report(results: list[tuple[str, list[Finding]]]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []

    lines.append("# AI概要版 品質チェックレポート")
    lines.append(f"生成日時: {now}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # サマリーテーブル
    lines.append("## サマリー")
    lines.append("")
    lines.append("| ファイル | ERROR | WARNING | INFO | 判定 |")
    lines.append("|---|---|---|---|---|")

    for fname, findings in results:
        counts = count_by_level(findings)
        v = verdict(findings)
        lines.append(f"| {fname} | {counts['ERROR']} | {counts['WARNING']} | {counts['INFO']} | {v} |")

    total_errors   = sum(count_by_level(f)["ERROR"]   for _, f in results)
    total_warnings = sum(count_by_level(f)["WARNING"] for _, f in results)
    total_infos    = sum(count_by_level(f)["INFO"]    for _, f in results)
    lines.append(f"| **合計 ({len(results)}件)** | **{total_errors}** | **{total_warnings}** | **{total_infos}** | |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 詳細レポート
    lines.append("## 詳細レポート")
    lines.append("")

    for fname, findings in results:
        v = verdict(findings)
        lines.append(f"### {fname}")
        lines.append("")
        lines.append(f"**判定: {v}**")
        lines.append("")

        if not findings:
            lines.append("チェック項目に問題は見当たりませんでした。")
            lines.append("")
            lines.append("---")
            lines.append("")
            continue

        # レベル別に分けて表示
        for level in ("ERROR", "WARNING", "INFO"):
            level_findings = [f for f in findings if f.level == level]
            if not level_findings:
                continue
            icon = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "💬"}[level]
            for f in level_findings:
                loc = f" （行{f.line_no}）" if f.line_no else ""
                lines.append(f"- {icon} **[{level}] {f.category}**{loc}  ")
                lines.append(f"  {f.detail}")

        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## チェック項目の説明")
    lines.append("")
    items = [
        ("行数", f"目標: {LINE_TARGET_MIN}〜{LINE_TARGET_MAX}行。{LINE_WARNING_THRESHOLD}行超で WARNING"),
        ("強い表現", "UFO断定・宇宙人・増殖・分裂・証明 などの表現を検出"),
        ("文書種別", "「観測記録」「会話記録」などの文書種別が明示されているか"),
        ("自然説明", "目撃者自身の自然説明・留保表現（「〜かもしれない」等）があるか"),
        ("出典", "「## 出典」セクションに「元PDF：」と .pdf URLがあるか"),
        ("免責事項", "「AI概要版」「OCR誤認識」「詳細解析版」の3語があるか"),
        ("注意点セクション", "「## 注意点」ヘッダーがあるか"),
        ("英文引用", f"英文blockquoteが{ENGLISH_BLOCKQUOTE_WARN_LINES}行以上で WARNING（要約推奨）"),
        ("OCR技術説明", "AI解析メモ以外の本文にOCR技術キーワードがないか"),
    ]
    for name, desc in items:
        lines.append(f"- **{name}**: {desc}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*このレポートは `scripts/review_ai_summary.py` によって自動生成されました。*")
    lines.append("*目的は「検閲」ではなく、AI概要版を「読みやすく・誤解されにくく」することです。*")

    return "\n".join(lines)


# ==================== エントリーポイント ====================

def get_target_files(args: list[str]) -> list[Path]:
    if args:
        return [Path(p) for p in args if Path(p).exists()]
    pattern = str(NOTE_DRAFTS_DIR / "ai_*.md")
    return sorted(Path(p) for p in glob.glob(pattern))


def main():
    args = sys.argv[1:]
    target_files = get_target_files(args)

    if not target_files:
        print("対象ファイルが見つかりません。")
        sys.exit(1)

    print(f"対象ファイル: {len(target_files)} 件")
    results = []
    for path in target_files:
        fname, findings = review_file(path)
        v = verdict(findings)
        counts = count_by_level(findings)
        print(f"  {v} {fname}  (E:{counts['ERROR']} W:{counts['WARNING']} I:{counts['INFO']})")
        results.append((fname, findings))

    report = build_report(results)
    REVIEW_LOGS_DIR.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"\nレポート出力: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
