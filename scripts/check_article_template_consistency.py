#!/usr/bin/env python3
"""
check_article_template_consistency.py — Release 02 VID記事テンプレート準拠チェック v2

目的:
  note_drafts/ 内の Release 02 VID記事ドラフトが
  docs/release02_article_template_v2.md の定義に準拠しているかをチェックする。
  #2_012 以降の公開前チェックとして必ず実行する。

使い方:
  # 単一ファイルチェック
  python3 scripts/check_article_template_consistency.py --file note_drafts/ai_summary_DOW-UAP-PR019_..._note_version.md

  # 全VIDドラフト一括チェック
  python3 scripts/check_article_template_consistency.py --all

  # VIDドラフト一括 + Markdownレポート出力
  python3 scripts/check_article_template_consistency.py --all --report review_reports/template_consistency_check_YYYYMMDD.md

  # 特定 article_id 範囲
  python3 scripts/check_article_template_consistency.py --all --from-order 2010 --to-order 2014

オプション:
  --file         単一ファイルのパス
  --all          note_drafts/ 内の全 DOW-UAP-PR* / FBI-UAP-PR* ファイルを対象
  --report       Markdownレポートの出力先（省略時は stdout のみ）
  --from-order   publish_order の下限フィルタ（--all と併用）
  --to-order     publish_order の上限フィルタ（--all と併用）
  --strict       語尾チェックをエラー扱い（デフォルトはWARN）
  --no-color     ANSIカラーを無効化

安全方針:
  - 読み取り専用。ファイルを変更しない
  - workflow.db / source_registry.csv は変更しない
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# ── チェック定義 ────────────────────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    ok: bool
    level: str  # "PASS" | "WARN" | "FAIL"
    detail: str = ""


DRAFTS_DIR = Path("note_drafts")
ARCHIVE_DIR = DRAFTS_DIR / "archive"

# (pattern, check_name, level, detail_on_fail)
STRUCTURAL_CHECKS: list[tuple[str, str, str, str]] = [
    # タイトル
    (r"# 【概要版#2_\d{3}】",
     "タイトルID: #2_XXX 形式",
     "FAIL",
     "タイトルが #2_XXX 形式でない（#R02-XXX など旧形式の可能性）"),

    # Release 02 表記
    (r"Release Date.*Release 02",
     "Release Date に「Release 02」",
     "FAIL",
     "Release Date に「・Release 02」が含まれていない"),

    # AOR情報
    (r"担当AOR：",
     "Related Location に AOR 情報",
     "WARN",
     "Related Location に「担当AOR：」が含まれていない"),

    # 画像プレースホルダー ▼
    (r"▼ 【画像】",
     "画像プレースホルダー ▼【画像】",
     "FAIL",
     "「▼ 【画像】」が存在しない"),

    # 掲載画像行（アイキャッチパス）
    (r"掲載画像：thumbnails/",
     "掲載画像：thumbnails/ 行",
     "WARN",
     "「掲載画像：thumbnails/」行が存在しない（note転記済みの場合は正常）"),

    # 目視確認注釈
    (r"以下は映像フレームの目視確認によるものです。",
     "目視確認注釈フレーズ",
     "FAIL",
     "「以下は映像フレームの目視確認によるものです。」が存在しない"),

    # ファイル名由来注釈
    (r"以下の情報はファイル名および.{0,60}映像フレームから直接確認したものではありません。",
     "ファイル名由来注釈フレーズ",
     "FAIL",
     "「以下の情報はファイル名および...映像フレームから直接確認したものではありません。」が存在しない"),

    # ffprobe 拡張形式
    (r"ffprobeによる技術情報を以下に示します。",
     "ffprobe 拡張箇条書きフォーマット",
     "FAIL",
     "「ffprobeによる技術情報を以下に示します。」が存在しない（パイプ区切り旧形式の可能性）"),

    # パイプ区切り旧形式の禁止（negated check）
    (r"コンテナ：.+\|.+解像度：",
     "映像メタデータ旧形式（パイプ区切り）の不在",
     "FAIL",
     "パイプ区切りの旧形式メタデータが残存している"),

    # 注意点セクション
    (r"^## 注意点",
     "## 注意点 セクション",
     "FAIL",
     "「## 注意点」セクションが存在しない"),

    # DVIDS ID（DoW/DVIDS管理番号）統一（v2）
    (r"DoW/DVIDS管理番号",
     "DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]",
     "WARN",
     "「（DoW/DVIDS管理番号）」が存在しない（旧形式「DVIDS＝国防映像情報配信サービス」の可能性）"),

    # ffprobe残留パイプ不在（v2）
    (r"解像度：[^（\n]+）\s*\|",
     "ffprobe解像度行のパイプ残留不在 [v2]",
     "FAIL",
     "ffprobe解像度行にパイプ（|）が残存している（T12未適用の可能性）"),

    # ▲キャプション丁寧体（v2）
    (r"^▲ [^\n]*確認できる。",
     "▲キャプション「確認できる。」の不在 [v2]",
     "WARN",
     "▲キャプション行に「確認できる。」（普通体）が残存している（T13未適用の可能性）"),

    # AI解析メモのタイムコード（v2）
    (r"\*\*AI解析メモ：\*\*[^\n]*\d{2}:\d{2}",
     "AI解析メモにタイムコード記載 [v2]",
     "WARN",
     "AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）"),

    # AI解析メモの DVIDS ID 記載
    (r"\*\*AI解析メモ：\*\*.*DVIDS ID \d+",
     "AI解析メモに DVIDS ID 記載",
     "WARN",
     "AI解析メモに「DVIDS ID XXXXXXX」が含まれていない"),

    # ## 注意点 と ## 出典 の間のセパレータ（v2）
    (r"---\n\n## 出典",
     "## 注意点と## 出典間のセパレータ [v2]",
     "WARN",
     "## 注意点と## 出典の間に「---」セパレータが存在しない（T17未適用の可能性）"),

    # ディスクレイマー 3段落確認
    (r"映像内容の判断には不確実性が含まれます。",
     "ディスクレイマー第2段落",
     "FAIL",
     "「映像内容の判断には不確実性が含まれます。」が存在しない"),

    (r"今後、追加情報.{0,40}詳細解析版",
     "ディスクレイマー第3段落",
     "FAIL",
     "「今後、追加情報...詳細解析版」が存在しない"),

    (r"原文リンクを重視し",
     "ディスクレイマー第4段落",
     "FAIL",
     "「原文リンクを重視し」が存在しない"),

    # 出典の画像表記
    (r"掲載画像出典：",
     "出典に「掲載画像出典：」",
     "FAIL",
     "「掲載画像出典：」が存在しない（「代表フレーム：」旧形式の可能性）"),

    # 旧表記の禁止（negated check）
    (r"代表フレーム：thumbnails/",
     "旧形式「代表フレーム：thumbnails/」の不在",
     "WARN",
     "旧形式「代表フレーム：thumbnails/」が残存している"),

    # フッター article_id
    (r"📋 \*\*article_id：R02-\d{3}",
     "フッターに article_id 行",
     "FAIL",
     "「📋 **article_id：R02-XXX」フッターが存在しない"),
]

# 語尾チェック: (禁止パターン, 代替表現, check_name)
VERB_ENDING_CHECKS: list[tuple[str, str, str]] = [
    (r"(?<![せまのいさ])扱わない",          "扱いません",              "語尾: 扱わない → 扱いません"),
    (r"確認できない(?![こと場合])",          "確認できません",          "語尾: 確認できない → 確認できません"),
    (r"特定できない(?![こと場合])",          "特定できません",          "語尾: 特定できない → 特定できません"),
    (r"断定できない(?![こと場合])",          "断定できません",          "語尾: 断定できない → 断定できません"),
    (r"示すものではない(?!こと)",            "示すものではありません",  "語尾: 示すものではない → 示すものではありません"),
    (r"確認されていない(?![こと場合])",      "確認されていません",      "語尾: 確認されていない → 確認されていません"),
    (r"できない(?![こと場合])[。）」\n]",   "できません",              "語尾: できない[。] → できません"),
]

# negated check のパターン（存在したら FAIL / WARN）
NEGATED_CHECKS = {
    "映像メタデータ旧形式（パイプ区切り）の不在",
    "旧形式「代表フレーム：thumbnails/」の不在",
    "ffprobe解像度行のパイプ残留不在 [v2]",
    "▲キャプション「確認できる。」の不在 [v2]",
}


# ── カラー出力 ───────────────────────────────────────────────────────────────

def _color(text: str, code: str, use_color: bool) -> str:
    return f"\033[{code}m{text}\033[0m" if use_color else text

def ok(t: str, c: bool) -> str:   return _color(t, "32", c)
def warn(t: str, c: bool) -> str: return _color(t, "33", c)
def fail(t: str, c: bool) -> str: return _color(t, "31", c)
def bold(t: str, c: bool) -> str: return _color(t, "1",  c)


# ── チェック実行 ─────────────────────────────────────────────────────────────

def check_file(path: Path, strict_verbs: bool = False) -> list[CheckResult]:
    text = path.read_text(encoding="utf-8")
    results: list[CheckResult] = []

    for pattern, name, level, detail_fail in STRUCTURAL_CHECKS:
        found = bool(re.search(pattern, text, re.MULTILINE))
        if name in NEGATED_CHECKS:
            # 見つかった → 旧形式残存 → NG
            if found:
                results.append(CheckResult(name, False, level, detail_fail))
            else:
                results.append(CheckResult(name, True, "PASS", ""))
        else:
            if found:
                results.append(CheckResult(name, True, "PASS", ""))
            else:
                results.append(CheckResult(name, False, level, detail_fail))

    # 語尾チェック
    verb_level = "FAIL" if strict_verbs else "WARN"
    for pattern, suggestion, name in VERB_ENDING_CHECKS:
        matches = re.findall(pattern, text)
        if matches:
            detail = f"残存: {matches[:3]}{'...' if len(matches) > 3 else ''} → {suggestion} に統一"
            results.append(CheckResult(name, False, verb_level, detail))
        else:
            results.append(CheckResult(name, True, "PASS", ""))

    return results


def summarize(results: list[CheckResult]) -> tuple[int, int, int]:
    fails  = sum(1 for r in results if not r.ok and r.level == "FAIL")
    warns  = sum(1 for r in results if not r.ok and r.level == "WARN")
    passes = sum(1 for r in results if r.ok)
    return fails, warns, passes


def print_results(path: Path, results: list[CheckResult], use_color: bool) -> None:
    fails, warns, passes = summarize(results)
    verdict = "FAIL" if fails > 0 else ("WARN" if warns > 0 else "PASS")
    color_fn = fail if verdict == "FAIL" else (warn if verdict == "WARN" else ok)

    print(f"\n{bold(str(path.name), use_color)}")
    print(f"  verdict: {color_fn(verdict, use_color)}  PASS:{passes} WARN:{warns} FAIL:{fails}")

    for r in results:
        if r.ok:
            print(f"  {ok('✓', use_color)} {r.name}")
        elif r.level == "FAIL":
            print(f"  {fail('✗', use_color)} {r.name}")
            if r.detail:
                print(f"      → {r.detail}")
        else:
            print(f"  {warn('△', use_color)} {r.name}")
            if r.detail:
                print(f"      → {r.detail}")


def build_markdown_report(
    file_results: list[tuple[Path, list[CheckResult]]],
    strict_verbs: bool,
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_files = len(file_results)
    total_fail  = sum(1 for _, rs in file_results if any(not r.ok and r.level == "FAIL" for r in rs))
    total_warn  = sum(1 for _, rs in file_results if any(not r.ok and r.level == "WARN" for r in rs) and
                      not any(not r.ok and r.level == "FAIL" for r in rs))
    total_pass  = total_files - total_fail - total_warn

    lines = [
        f"# Release 02 テンプレート準拠チェックレポート",
        f"",
        f"**実行日時：** {now}  ",
        f"**対象ファイル数：** {total_files}  ",
        f"**FAIL：** {total_fail}件  **WARN：** {total_warn}件  **PASS：** {total_pass}件  ",
        f"**strict_verbs：** {strict_verbs}",
        f"",
        f"---",
        f"",
        f"## サマリーテーブル",
        f"",
        f"| ファイル | FAIL | WARN | PASS | 判定 |",
        f"|---|---|---|---|---|",
    ]

    for path, results in file_results:
        fails, warns, passes = summarize(results)
        verdict = "**FAIL**" if fails > 0 else ("WARN" if warns > 0 else "PASS")
        lines.append(f"| {path.name} | {fails} | {warns} | {passes} | {verdict} |")

    lines += ["", "---", "", "## 詳細"]

    for path, results in file_results:
        fails, warns, passes = summarize(results)
        verdict = "FAIL" if fails > 0 else ("WARN" if warns > 0 else "PASS")
        lines += [
            f"",
            f"### {path.name}",
            f"",
            f"判定: **{verdict}** | PASS:{passes} WARN:{warns} FAIL:{fails}",
            f"",
        ]
        for r in results:
            if r.ok:
                lines.append(f"- ✅ {r.name}")
            elif r.level == "FAIL":
                lines.append(f"- ❌ **{r.name}**")
                if r.detail:
                    lines.append(f"  - {r.detail}")
            else:
                lines.append(f"- ⚠️ {r.name}")
                if r.detail:
                    lines.append(f"  - {r.detail}")

    return "\n".join(lines) + "\n"


def find_vid_drafts(from_order: int | None, to_order: int | None) -> list[Path]:
    patterns = [
        "ai_summary_DOW-UAP-PR*_note_version.md",
        "ai_summary_FBI-UAP-PR*_note_version.md",
    ]
    drafts: list[Path] = []
    for pat in patterns:
        for p in sorted(DRAFTS_DIR.glob(pat)):
            if ARCHIVE_DIR in p.parents or p.parent != DRAFTS_DIR:
                continue
            if p.suffix != ".md" or p.name.endswith(".bak"):
                continue
            drafts.append(p)
    return drafts


def main() -> None:
    parser = argparse.ArgumentParser(description="Release 02 VID記事テンプレート準拠チェック")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="単一ファイルのパス")
    group.add_argument("--all", action="store_true", help="note_drafts/ 内の全VIDドラフトを対象")
    parser.add_argument("--report", help="Markdownレポート出力先ファイルパス")
    parser.add_argument("--from-order", type=int, help="publish_order 下限フィルタ（未実装・将来用）")
    parser.add_argument("--to-order", type=int, help="publish_order 上限フィルタ（未実装・将来用）")
    parser.add_argument("--strict", action="store_true", help="語尾チェックをFAIL扱い")
    parser.add_argument("--no-color", action="store_true", help="ANSIカラーを無効化")
    args = parser.parse_args()

    use_color = not args.no_color and sys.stdout.isatty()

    if not DRAFTS_DIR.is_dir():
        sys.exit("[ERROR] note_drafts/ が見つかりません。プロジェクトルートから実行してください。")

    if args.file:
        targets = [Path(args.file)]
    else:
        targets = find_vid_drafts(args.from_order, args.to_order)
        if not targets:
            sys.exit("[ERROR] 対象ファイルが見つかりません。")

    file_results: list[tuple[Path, list[CheckResult]]] = []
    for path in targets:
        if not path.is_file():
            print(f"[SKIP] ファイルが存在しません: {path}")
            continue
        results = check_file(path, strict_verbs=args.strict)
        file_results.append((path, results))
        print_results(path, results, use_color)

    # サマリー
    total = len(file_results)
    total_fail = sum(1 for _, rs in file_results if any(not r.ok and r.level == "FAIL" for r in rs))
    total_warn = sum(1 for _, rs in file_results if any(not r.ok and r.level == "WARN" for r in rs)
                    and not any(not r.ok and r.level == "FAIL" for r in rs))
    print(f"\n{'='*60}")
    print(f"  総計: {total}件  FAIL:{total_fail}  WARN:{total_warn}  PASS:{total - total_fail - total_warn}")
    print(f"{'='*60}\n")

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            build_markdown_report(file_results, strict_verbs=args.strict),
            encoding="utf-8",
        )
        print(f"[レポート出力] {report_path}")

    # exit code: 1 if any FAIL
    sys.exit(1 if total_fail > 0 else 0)


if __name__ == "__main__":
    main()
