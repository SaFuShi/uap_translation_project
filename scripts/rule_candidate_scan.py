#!/usr/bin/env python3
"""
rule_candidate_scan.py — ドラフト内ルール候補検出スクリプト

Codex監査の前処理として、記事ドラフト内の
新規用語・禁止表現・表記揺れ候補を検出し、
人間が確認できる rule candidate レポートを生成する。

使い方:
  python3 scripts/rule_candidate_scan.py \\
      --draft note_drafts/ai_summary_ODNI-UAP-D001_usper_narrative_senior_usic_note_version.md
  python3 scripts/rule_candidate_scan.py --draft ... --dry-run
  python3 scripts/rule_candidate_scan.py --draft ... --slug DOW-UAP-PR051

安全方針:
  - ドラフト本文は変更しない
  - docs/draft_rules_v2.md は変更しない
  - workflow.db は変更しない
  - 外部APIは使わない
  - S_CLASS疑い文字列はレポートに警告のみ（外部送信しない）
  - すべての検出は CANDIDATE として出力（断定しない）
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


VERSION = "1.1.0"

# ── CAT-01: 既知組織名・略称と推奨補足 ───────────────────────────────────────

KNOWN_ORGS: dict[str, str] = {
    "AARO":      "全領域異常解決局／米国防総省のUAP調査組織",
    "ODNI":      "国家情報長官室",
    "CENTCOM":   "米国中央軍（中東・中央アジア周辺担当）",
    "INDOPACOM": "インド太平洋軍",
    "SOCOM":     "米特殊作戦軍",
    "JSOC":      "統合特殊作戦軍",
    "FLIR":      "前方監視赤外線カメラ",
    "NVG":       "暗視ゴーグル",
    "JOC":       "合同作戦センター",
    "AGL":       "地上高度（above ground level）",
    "OSI":       "空軍特別調査局",
    "AFSWP":     "軍特殊兵器計画",
    "AEC":       "米国原子力委員会",
    "UNM":       "ニューメキシコ大学",
    "NARA":      "米国国立公文書記録管理局",
    "AFB":       "空軍基地",
    "DVIDS":     "国防映像情報配信サービス",
    "DIA":       "国防情報局",
    "NSA":       "国家安全保障局",
    "USAF":      "米空軍",
    "USN":       "米海軍",
    "USMC":      "米海兵隊",
    "DoW":       "米国防省",
    "DoD":       "米国防総省",
}

# 「〜より」「ファイル名」等の出典参照キーワード（補足ではなく出典）
SOURCE_REF_RE = re.compile(
    r'(?:より|ファイル名|files_catalog|メタデータ|[Cc][Ss][Vv]|records|registry)',
    re.IGNORECASE,
)

# 補足判定: 組織名直後に探す（）の最大文字数
SUPPLEMENT_DIRECT_WINDOW = 10

# ── CAT-02: 禁止表現リスト (text, rule_ref, suggestion) ──────────────────────
#
# 対象: 誤解・事実誤認・公開品質に直結する表現のみ。
#   - Rule 8-6: 元映像系（通常表示映像との混同を招く）
#   - Rule 4:   画像・VID記事における断定表現（観察事実の超過）
#   - Rule 3:   AARO評価の断定化（推定を事実として記述する）
#
# 【将来の拡張】
#
# CAT-06（未実装）: 文体・丁寧体チェック
#   文体統一（常体→丁寧体）は事実誤認には直結しないが公開品質に関わる。
#   例: 「〜確認されない」→「〜確認されていません」
#       「〜ではない」→「〜ではありません」
#   Rule 8-1 相当。単純な文字列マッチでは文末以外の「ない」を誤検知するため
#   文末判定ロジック（行末パターン）を持つ専用検出関数として実装すること。
#
# CAT-08（未実装）: アップロード者タイトルの断定化候補
#   uploader-defined title（例: "instant acceleration"）を AARO の分析結論として
#   断定する表現は文脈依存のため単純な regex では誤検知が多い。
#   例: 「瞬時加速が確認された」「instant acceleration はAAROが認定した」
#   検出には「アップロード者が付与した」「uploader-defined」等の
#   免責フレーズの有無をセクション単位で確認するロジックが必要。

FORBIDDEN_EXPRESSIONS: list[tuple[str, str, str]] = [
    # Rule 8-6: 元映像禁止
    ("元映像",         "Rule 8-6", "→「通常表示映像」"),
    ("原本映像",       "Rule 8-6", "→「通常表示映像」"),
    ("オリジナル映像", "Rule 8-6", "→「通常表示映像」"),
    ("処理前映像",     "Rule 8-6", "→「通常表示映像」"),
    ("処理前の映像",   "Rule 8-6", "→「通常表示映像」"),
    # Rule 4: 画像・VID記事の断定表現（観察事実の超過）
    ("軍用赤外線（IR）カメラ映像",       "Rule 4", "→「IR映像とみられる映像（画像特性より）」"),
    ("赤外線映像である",                 "Rule 4", "→「赤外線映像とみられる（画像特性より）」"),
    ("追跡対象物",                       "Rule 4", "→「暗点」または「追跡対象とみられる暗点」"),
    ("IRカメラが捕捉した",               "Rule 4", "→「画像中央付近に確認できる」"),
    ("ローターブレードが確認できる",     "Rule 4", "→「ローターブレード状の突起が見えるような形状」"),
    ("移動していることが確認できます",   "Rule 4", "→「前フレームと比較して別位置に確認できます」"),
    ("継続的な捕捉は維持されています",   "Rule 4", "→「暗点が継続して確認されています」"),
    ("追跡が継続されていることを示します","Rule 4", "→「暗点が継続して確認されています」"),
    # Rule 3: AARO評価の断定化（推定・評価を事実として記述する）
    ("AAROが確認した", "Rule 3", "→「AAROは（評価・推定）している」"),
    ("AAROが断定した", "Rule 3", "→「AAROは（評価・推定）している」"),
]

# ── CAT-04: 日付ゼロ埋め ──────────────────────────────────────────────────────

DATE_PATTERN = re.compile(r'(\d{4})年(\d{1,2})月(\d{1,2})日')

# ── CAT-05: note禁止フォーマット ──────────────────────────────────────────────

NOTE_FORBIDDEN: list[tuple[re.Pattern, str, str, str]] = [
    (re.compile(r'^\s*\|.+\|'),   "Markdown table",       "Rule 5", "→ 箇条書き or 【】ブロック形式"),
    (re.compile(r'^>'),           "引用ブロック（>）",     "Rule 5", "→ 【原文抜粋】＋【要訳】形式"),
    (re.compile(r'^```'),         "コードブロック（```）", "Rule 5", "→ 【抽出テキスト全文】プレーンテキスト形式"),
]

# ── S_CLASSガード ──────────────────────────────────────────────────────────────

S_CLASS_PATTERN = re.compile(r'S_CLASS|S-CLASS|SCLASS', re.IGNORECASE)


# ── データクラス ──────────────────────────────────────────────────────────────

@dataclass
class Candidate:
    seq: int
    cat_id: str
    cat_name: str
    line_no: int
    matched: str
    context: str
    rule_ref: str
    suggestion: str
    note: str = ""


# ── CAT-01 補足判定ヘルパー ───────────────────────────────────────────────────

def _has_org_supplement(line: str, idx: int, org: str) -> bool:
    """
    True = 組織名に日本語補足あり（出典参照のみは False）

    Case 1: 組織名が（）の中に入っている場合
      例: Intelligence（ODNI / 国家情報長官室）
          → idx直前3文字に（ or / が含まれる

    Case 2: 組織名直後に（）補足がある場合
      例: FLIR（前方監視赤外線カメラ）
          → org直後SUPPLEMENT_DIRECT_WINDOW文字以内に（
          → （と組織名の間に日本語（CJK）・引用符がない
          → （）の内容が出典参照でない
    """
    # Case 1: 組織名が括弧内にある（略称として紹介されている）
    prefix = line[max(0, idx - 3): idx]
    if re.search(r'[（/]\s*$', prefix):
        return True

    # Case 2: 組織名直後に（）がある
    after = line[idx + len(org): idx + len(org) + SUPPLEMENT_DIRECT_WINDOW]
    paren_pos = after.find('（')
    if paren_pos == -1:
        return False

    # （）の間の文字列（日本語・引用符があれば「別の語への括弧」と判断）
    between = after[:paren_pos]
    if re.search(r'[　-鿿"\'」」]', between):
        return False

    # （）の内容を取り出して出典参照チェック
    close_pos = line.find('）', idx + len(org) + paren_pos)
    if close_pos == -1:
        return False
    content = line[idx + len(org) + paren_pos + 1: close_pos]
    if SOURCE_REF_RE.search(content):
        return False

    return True


# ── 検出関数 ──────────────────────────────────────────────────────────────────

def detect_cat01(lines: list[str]) -> list[Candidate]:
    """CAT-01: 組織名・略称の初出補足候補"""
    results: list[Candidate] = []
    seen_supplemented: set[str] = set()
    seen_flagged: set[str] = set()

    for line_no, line in enumerate(lines, start=1):
        for org, suggested in KNOWN_ORGS.items():
            # 単語境界チェック（前後に英数字がない）
            if not re.search(
                r'(?<![A-Za-z\d])' + re.escape(org) + r'(?![A-Za-z\d])', line
            ):
                continue

            if org in seen_supplemented:
                continue  # 既に補足済みの初出あり → スキップ

            idx = line.find(org)

            # 文書ID・ファイル名内の略称はスキップ（例: ODNI-UAP-D001, DOW-UAP-PR051）
            char_after = line[idx + len(org): idx + len(org) + 1]
            if char_after in ('-', '_'):
                continue
            if _has_org_supplement(line, idx, org):
                seen_supplemented.add(org)
                seen_flagged.discard(org)
            elif org not in seen_flagged:
                seen_flagged.add(org)
                results.append(Candidate(
                    seq=0,
                    cat_id="CAT-01",
                    cat_name="組織名・略称の初出補足候補",
                    line_no=line_no,
                    matched=org,
                    context=line.strip()[:120],
                    rule_ref="Rule 7（略語・組織名の注釈）",
                    suggestion=f"→「{org}（{suggested}）」",
                    note="初出または近傍に日本語補足（）が確認できません。",
                ))
    return results


def detect_cat02(lines: list[str]) -> list[Candidate]:
    """CAT-02: 禁止表現候補"""
    results: list[Candidate] = []

    for line_no, line in enumerate(lines, start=1):
        # 「→ 使用ファイル：」行はスキップ（内部パス行）
        if line.strip().startswith("→ 使用ファイル"):
            continue
        for expr, rule_ref, suggestion in FORBIDDEN_EXPRESSIONS:
            if expr in line:
                results.append(Candidate(
                    seq=0,
                    cat_id="CAT-02",
                    cat_name="禁止表現候補",
                    line_no=line_no,
                    matched=expr,
                    context=line.strip()[:120],
                    rule_ref=rule_ref,
                    suggestion=suggestion,
                ))
    return results


def detect_cat04(lines: list[str]) -> list[Candidate]:
    """CAT-04: 日付ゼロ埋め候補"""
    results: list[Candidate] = []

    for line_no, line in enumerate(lines, start=1):
        for m in DATE_PATTERN.finditer(line):
            year_str  = m.group(1)
            month_str = m.group(2)
            day_str   = m.group(3)
            fixes: list[str] = []
            if len(month_str) == 1:
                fixes.append(f"月 {month_str} → {month_str.zfill(2)}")
            if len(day_str) == 1:
                fixes.append(f"日 {day_str} → {day_str.zfill(2)}")
            if fixes:
                fixed = f"{year_str}年{month_str.zfill(2)}月{day_str.zfill(2)}日"
                results.append(Candidate(
                    seq=0,
                    cat_id="CAT-04",
                    cat_name="日付ゼロ埋め候補",
                    line_no=line_no,
                    matched=m.group(0),
                    context=line.strip()[:120],
                    rule_ref="Rule（未定義・新規候補）",
                    suggestion=f"→「{fixed}」（{' / '.join(fixes)}）",
                    note="DOE-UAP-D001 B-01相当。YYYY年MM月DD日形式が推奨。",
                ))
    return results


def detect_cat05(lines: list[str]) -> list[Candidate]:
    """CAT-05: note禁止フォーマット候補"""
    results: list[Candidate] = []

    for line_no, line in enumerate(lines, start=1):
        for pattern, fmt_name, rule_ref, suggestion in NOTE_FORBIDDEN:
            if pattern.search(line):
                results.append(Candidate(
                    seq=0,
                    cat_id="CAT-05",
                    cat_name="note禁止フォーマット候補",
                    line_no=line_no,
                    matched=fmt_name,
                    context=line.strip()[:120],
                    rule_ref=rule_ref,
                    suggestion=suggestion,
                ))
    return results


def detect_sclass(lines: list[str]) -> list[tuple[int, str]]:
    """S_CLASS疑い文字列を検出（警告のみ・外部送信禁止）"""
    results: list[tuple[int, str]] = []
    for line_no, line in enumerate(lines, start=1):
        if S_CLASS_PATTERN.search(line):
            results.append((line_no, line.strip()[:80]))
    return results


# ── レポート生成 ──────────────────────────────────────────────────────────────

def _section_header(cat_id: str, cat_name: str, cat_desc: str) -> list[str]:
    return ["", f"## {cat_id} {cat_name}", "", f"> {cat_desc}", ""]


def _candidate_block(c: Candidate) -> list[str]:
    lines = [
        f"### [CANDIDATE #{c.seq}] L{c.line_no}: `{c.matched}`",
        "",
        f"- **カテゴリ:** {c.cat_id} {c.cat_name}",
        f"- **該当箇所:** `{c.context}`",
        f"- **既存ルール:** {c.rule_ref}",
        f"- **推奨対応:** {c.suggestion}",
    ]
    if c.note:
        lines.append(f"- **補足:** {c.note}")
    lines += [
        "",
        "```",
        "承認: [ ] ACCEPT  [ ] REJECT  [ ] RULE_UPDATE  [ ] NEW_RULE",
        "理由: ",
        "```",
        "",
    ]
    return lines


def build_report(
    slug: str,
    draft_path: str,
    rules_path: str,
    candidates: list[Candidate],
    sclass_warnings: list[tuple[int, str]],
    now: str,
) -> str:
    by_cat: dict[str, list[Candidate]] = {}
    for c in candidates:
        by_cat.setdefault(c.cat_id, []).append(c)

    counts = {k: len(by_cat.get(k, [])) for k in ("CAT-01", "CAT-02", "CAT-04", "CAT-05")}
    total = sum(counts.values())

    out: list[str] = [
        f"# ルール候補レポート: {slug}",
        "",
        f"**生成日時:** {now}",
        f"**スクリプト:** scripts/rule_candidate_scan.py v{VERSION}",
        f"**対象ドラフト:** {draft_path}",
        f"**参照ルールファイル:** {rules_path}",
        (
            f"**検出合計:** {total}件"
            f"（CAT-01: {counts['CAT-01']} / CAT-02: {counts['CAT-02']}"
            f" / CAT-04: {counts['CAT-04']} / CAT-05: {counts['CAT-05']}）"
        ),
        "",
        "> ⚠️ すべての検出は **CANDIDATE（候補）** です。断定ではありません。",
        "> 各項目を人間が確認し、承認欄に記入してください。",
        "",
        "---",
    ]

    # S_CLASS警告
    if sclass_warnings:
        out += [
            "",
            "## ⚠️ S_CLASS疑い文字列（外部送信前に確認必須）",
            "",
            "> **この文書を外部AI・APIへ送信する前に内容確認が必要です。**",
            "",
        ]
        for lno, text in sclass_warnings:
            out.append(f"- L{lno}: `{text}`")
        out += ["", "---"]

    # サマリーテーブル
    out += [
        "",
        "## 検出サマリー",
        "",
        "| カテゴリ | 件数 | 既存ルール |",
        "|---------|-----|----------|",
        f"| CAT-01 組織名・略称補足 | {counts['CAT-01']} | Rule 7 |",
        f"| CAT-02 禁止表現 | {counts['CAT-02']} | Rule 4 / Rule 8 |",
        f"| CAT-04 日付ゼロ埋め | {counts['CAT-04']} | 未定義（新規候補） |",
        f"| CAT-05 note禁止フォーマット | {counts['CAT-05']} | Rule 5 |",
        "",
        "---",
    ]

    # カテゴリ別詳細
    cat_meta = [
        (
            "CAT-01",
            "組織名・略称の初出補足候補",
            "初出または近傍に日本語補足（）が確認できない組織名・略称を検出します。"
            "出典参照（ファイル名より等）のみの場合も候補として出力します。",
        ),
        (
            "CAT-02",
            "禁止表現候補",
            "Rule 8-6（元映像禁止）・Rule 4（画像・VID記事の断定表現）・"
            "Rule 3（AARO評価の断定化）の対象表現を検出します。"
            "文体チェック（丁寧体）は将来 CAT-06 で管理予定。",
        ),
        (
            "CAT-04",
            "日付ゼロ埋め候補",
            "YYYY年M月D日形式（月または日がゼロ埋めなし）を検出します。"
            "Rule未定義・新規追加候補。",
        ),
        (
            "CAT-05",
            "note禁止フォーマット候補",
            "Markdown table・引用ブロック・コードブロックを検出します（Rule 5）。",
        ),
    ]

    for cat_id, cat_name, cat_desc in cat_meta:
        cat_candidates = by_cat.get(cat_id, [])
        out += _section_header(cat_id, cat_name, cat_desc)
        if not cat_candidates:
            out += ["（検出なし）", "", "---"]
            continue
        for c in cat_candidates:
            out += _candidate_block(c)
        out.append("---")

    # 新規ルール追加候補
    out += ["", "## 新規ルール追加候補（docs/draft_rules_v2.md 未定義）", ""]
    if counts["CAT-04"] > 0:
        out.append(
            f"- **日付ゼロ埋め強制**（{counts['CAT-04']}件検出）: "
            "YYYY年MM月DD日形式を Rule 7 または新 Rule 9 として追加を検討"
        )
    else:
        out.append("（今回のドラフトでは新規候補なし）")

    out += [
        "",
        "---",
        "",
        "## 承認後の作業フロー",
        "",
        "1. **ACCEPT** → ドラフトを直接修正（このスクリプトは修正しない）",
        "2. **RULE_UPDATE** → `docs/draft_rules_v2.md` の該当箇所へ人間が追記",
        "3. **NEW_RULE** → `docs/draft_rules_v2.md` に新セクションとして人間が追加",
        "4. **REJECT** → 誤検知理由を「理由:」欄に記録（次回パターン改善に使用）",
        "5. 修正完了後 → Codex監査を実行",
        "",
    ]

    return "\n".join(out)


# ── ユーティリティ ────────────────────────────────────────────────────────────

def extract_slug(draft_path: str) -> str:
    name = Path(draft_path).stem
    m = re.match(r'ai_(?:summary|reading)_(.+?)(?:_note_version)?$', name)
    if m:
        return m.group(1)
    return name


# ── メイン ────────────────────────────────────────────────────────────────────

def run(args: argparse.Namespace) -> None:
    draft_path = Path(args.draft)
    if not draft_path.is_file():
        sys.exit(f"[ERROR] ドラフトファイルが見つかりません: {draft_path}")

    rules_path = args.rules
    slug = args.slug or extract_slug(str(draft_path))
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    today_compact = datetime.now().strftime("%Y%m%d")

    lines = draft_path.read_text(encoding="utf-8").splitlines()

    cat01 = detect_cat01(lines)
    cat02 = detect_cat02(lines)
    cat04 = detect_cat04(lines)
    cat05 = detect_cat05(lines)
    sclass = detect_sclass(lines)

    all_candidates = cat01 + cat02 + cat04 + cat05
    for i, c in enumerate(all_candidates, start=1):
        c.seq = i

    total = len(all_candidates)
    print(f"[rule_candidate_scan] {slug}")
    print(f"  対象: {draft_path}")
    print(
        f"  検出: {total}件"
        f"  (CAT-01:{len(cat01)} / CAT-02:{len(cat02)}"
        f" / CAT-04:{len(cat04)} / CAT-05:{len(cat05)})"
    )
    if sclass:
        print(f"  ⚠️  S_CLASS疑い: {len(sclass)}件 → 外部送信前に確認必須")

    if args.dry_run:
        print()
        print("[DRY-RUN] 検出結果プレビュー（レポートファイル未生成）:")
        print()
        for c in all_candidates:
            print(f"  [{c.cat_id}] L{c.line_no}: {c.matched}")
            print(f"    ルール: {c.rule_ref}")
            print(f"    推奨:   {c.suggestion}")
            print()
        print("[DRY-RUN] 完了。ファイル変更なし。")
        return

    report_content = build_report(
        slug=slug,
        draft_path=str(draft_path),
        rules_path=rules_path,
        candidates=all_candidates,
        sclass_warnings=sclass,
        now=now,
    )

    if args.output:
        out_path = Path(args.output)
    else:
        report_dir = Path("review_reports")
        report_dir.mkdir(exist_ok=True)
        out_path = report_dir / f"rule_candidates_{today_compact}_{slug}.md"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_content, encoding="utf-8")
    print(f"[OK] レポート生成: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ドラフト内ルール候補検出スクリプト（Codex監査前処理）",
    )
    parser.add_argument("--draft",   required=True, help="スキャン対象ドラフトファイル（必須）")
    parser.add_argument("--slug",    default="",    help="スラッグ（省略時はファイル名から推定）")
    parser.add_argument("--rules",   default="docs/draft_rules_v2.md",
                        help="ルールファイルパス")
    parser.add_argument("--output",  default="",
                        help="出力先（省略時: review_reports/rule_candidates_YYYYMMDD_<slug>.md）")
    parser.add_argument("--dry-run", action="store_true",
                        help="レポート未生成・標準出力のみ")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
