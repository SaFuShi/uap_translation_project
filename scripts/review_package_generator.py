#!/usr/bin/env python3
"""
review_package_generator.py — Codex PASS 後 note 公開前レビューパッケージ生成

Codex監査 PASS 後、人間が迷わず note 公開前レビューに入れるように
対象ドラフト・使用画像候補・キャプション・公開前チェック項目をまとめた
Review Package を生成する。

使い方:
  python3 scripts/review_package_generator.py \\
      --article-id R03-001 \\
      --slug DOW-UAP-D077_Unresolved-Case-Analysis-Update_Western-United-States-Event \\
      --draft note_drafts/ai_summary_DOW-UAP-D077_..._note_version.md \\
      --codex-report review_reports/codex_audit_20260618_DOW-UAP-D077_..._iter2.md \\
      --rule-report review_reports/rule_candidates_20260618_DOW-UAP-D077_....md \\
      --image raw_media/page_images/DOW-UAP-D078_notional_map_p1.jpeg \\
        "キャプション案テキスト" \\
      --open-finder

  --dry-run: ファイル書き込みせず stdout にプレビュー表示
  --image: 複数回指定可能。各 --image はパスのみ、またはパスとキャプションの2値
  --open-finder: macOS Finder でドラフト・画像・Review Package を表示

安全方針:
  - note_drafts/ を変更しない
  - workflow.db を変更しない
  - git add / commit / push を実行しない
  - 外部APIを使わない
  - S_CLASS疑い文字列は外部送信しない
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VERSION = "1.1.0"
OUTPUT_DIR = Path("review_packages")


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

class ImageAction(argparse.Action):
    """--image path [caption] を受け取り (path, caption) のリストに積む。"""
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None) or []
        if len(values) == 1:
            items.append((values[0], ""))
        elif len(values) == 2:
            items.append((values[0], values[1]))
        else:
            parser.error(f"--image は 1〜2 引数（パス、キャプション）を取ります: {values}")
        setattr(namespace, self.dest, items)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Codex PASS後 note公開前レビューパッケージ生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--article-id",   required=True,  help="例: R03-001")
    p.add_argument("--slug",         required=True,  help="記事スラッグ")
    p.add_argument("--draft",        required=True,  help="note_drafts/ のドラフトファイルパス")
    p.add_argument("--codex-report", required=True,  help="Codex監査レポートパス（iter2推奨）")
    p.add_argument("--rule-report",  default="",     help="Rule Candidateレポートパス（任意）")
    p.add_argument(
        "--image",
        dest="images",
        nargs="+",
        action=ImageAction,
        metavar=("PATH", "CAPTION"),
        help="使用画像候補。--image path [caption] の形で複数回指定可",
    )
    p.add_argument("--open-finder",          action="store_true", help="macOS Finder で関連ファイルを表示")
    p.add_argument("--dry-run",              action="store_true", help="ファイル書き込みせず stdout にプレビュー")
    # 公開順制御
    p.add_argument("--ready-to-publish",     action="store_true", help="内部作業完了（draft+codex+review_package）")
    p.add_argument("--publish-blocked",      action="store_true", help="公開順ルールにより一般公開ブロック中")
    p.add_argument("--publish-block-reason", default="",          help="公開ブロックの理由（任意）")
    return p


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def check_file(path: str, label: str) -> tuple[bool, str]:
    """ファイルが存在するか確認。(ok, message) を返す。"""
    if not path:
        return False, f"{label}: 未指定"
    p = Path(path)
    if p.exists():
        size_kb = p.stat().st_size // 1024
        return True, f"{label}: {path} ({size_kb}KB)"
    return False, f"{label}: ファイルが存在しない → {path}"


def get_codex_verdict(codex_report_path: str) -> str:
    """Codex監査レポートから VERDICT を抽出する。"""
    if not codex_report_path or not Path(codex_report_path).exists():
        return "UNKNOWN"
    try:
        content = Path(codex_report_path).read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.startswith("VERDICT:"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return "UNKNOWN"


def get_rule_candidate_summary(rule_report_path: str) -> str:
    """Rule Candidateレポートから未処理HIGH件数を推定する。"""
    if not rule_report_path or not Path(rule_report_path).exists():
        return "レポートなし"
    try:
        content = Path(rule_report_path).read_text(encoding="utf-8")
        # 未処理 = [ ] ACCEPT のまま残っているもの
        pending = content.count("[ ] ACCEPT  [ ] REJECT")
        rejected = content.count("[x] REJECT")
        accepted = content.count("[x] ACCEPT")
        total = pending + rejected + accepted
        if total == 0:
            return "検出なし"
        return f"全{total}件 / 未処理{pending}件 / ACCEPT{accepted}件 / REJECT{rejected}件"
    except Exception:
        return "読み取りエラー"


def check_draft_rules(draft_path: str) -> dict:
    """ドラフトの簡易ルールチェック。"""
    results = {
        "rule9_dates": True,
        "rule10_disclaimer": False,
        "source_url": False,
        "download_url": False,
        "internal_path_in_caption": False,
    }
    if not Path(draft_path).exists():
        return results
    try:
        import re
        content = Path(draft_path).read_text(encoding="utf-8")

        # Rule 9: M月D日 形式（ゼロ埋めなし）が残っていないか
        bad_dates = re.findall(r'\d{4}年(?:1[0-2]|[1-9])月(?:[12]\d|3[01]|[1-9])日', content)
        results["rule9_dates"] = len(bad_dates) == 0

        # Rule 10: 免責文キーワード
        results["rule10_disclaimer"] = (
            "投稿者は米政府" in content and "UAP（未確認異常現象）の正体・起源" in content
        )

        # Source URL / Download URL
        results["source_url"] = "Source URL" in content or "source_url" in content.lower()
        results["download_url"] = "Download URL" in content or "download_url" in content.lower()

        # 内部パスがキャプション候補行に残っていないか
        caption_lines = [l for l in content.splitlines() if "キャプション" in l]
        internal_patterns = ["/Users/", "/Volumes/", "raw_pdf/", "/tmp/"]
        results["internal_path_in_caption"] = any(
            pat in line for line in caption_lines for pat in internal_patterns
        )
    except Exception:
        pass
    return results


# ---------------------------------------------------------------------------
# Package content builder
# ---------------------------------------------------------------------------

def build_package(args, verdict: str, rule_summary: str, draft_checks: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    article_id_fmt = f"#{args.article_id}"
    blocked = getattr(args, "publish_blocked", False)
    ready   = getattr(args, "ready_to_publish", False)
    block_reason = getattr(args, "publish_block_reason", "") or ""

    images = args.images or []

    # 画像候補セクション
    image_lines = []
    if images:
        for i, (img_path, caption) in enumerate(images, 1):
            exists = Path(img_path).exists()
            size_str = ""
            if exists:
                size_kb = Path(img_path).stat().st_size // 1024
                size_str = f"（{size_kb}KB）"
            status = "✅ 存在" if exists else "❌ 存在しない"
            image_lines.append(f"### 画像候補 {i}")
            image_lines.append(f"- パス：`{img_path}` {size_str} {status}")
            if caption:
                image_lines.append(f"- キャプション案：{caption}")
            image_lines.append("")
    else:
        image_lines.append("（画像候補なし）")
        image_lines.append("")

    # ルールチェック結果
    def chk(ok: bool) -> str:
        return "✅" if ok else "❌"

    rule_check_lines = [
        f"- {chk(not draft_checks['internal_path_in_caption'])} 画像キャプションに内部パスが残っていない",
        f"- {chk(draft_checks['rule9_dates'])} Rule 9：日付ゼロ埋め（YYYY年MM月DD日）",
        f"- {chk(draft_checks['rule10_disclaimer'])} Rule 10：免責文が入っている",
        f"- {chk(draft_checks['source_url'])} Source URL が記載されている",
        f"- {chk(draft_checks['download_url'])} Download URL が記載されている",
        f"- {chk(verdict == 'PASS')} Codex監査が PASS になっている（現在：{verdict}）",
        f"- [ ] タイトルが本文より強い断定をしていないか（人間確認）",
        f"- [ ] 事実と推論が分離されているか（人間確認）",
        f"- [ ] Rule Candidate 未処理HIGH が残っていないか：{rule_summary}",
        f"- [ ] note転記後に画像が正しく表示されるか（転記後確認）",
        "",
        "**── 公開順チェック（人間確認）──**",
        f"- [ ] 前の Release がすべて公開済みか確認した",
        f"- [ ] 同一 Release 内の前番号記事がすべて公開済みか確認した",
        f"- [ ] source_registry に {article_id_fmt} が登録済みか確認した",
        f"- {chk(not blocked)} publish_blocked = {'true → note公開せず下書き保存に留める' if blocked else 'false（公開可）'}",
    ]

    # note転記手順（ブロック時は下書き保存止まり）
    if blocked:
        note_steps = """\
1. `note_drafts/` の対象ファイルをテキストエディタで開く
2. note.com の新規投稿画面を開く
3. タイトル行（H1）をコピー → noteのタイトル欄に貼り付け
4. H1以降の本文をコピー → noteの本文エリアに貼り付け
5. 画像をアップロードし、対応するキャプションを設定
6. 【画像候補】プレースホルダー行をnote上で削除
7. メタデータブロック（File Name・Agency 等）は本文冒頭のまま残す
8. プレビューで表示確認（Markdownレンダリング崩れがないか）
9. note 上での最終タイトル確認（【AI概要版】タグを含むか）
10. ⚠️ 「下書き保存」で保存する → 公開しない（publish_blocked = true）"""
    else:
        note_steps = """\
1. `note_drafts/` の対象ファイルをテキストエディタで開く
2. note.com の新規投稿画面を開く
3. タイトル行（H1）をコピー → noteのタイトル欄に貼り付け
4. H1以降の本文をコピー → noteの本文エリアに貼り付け
5. 画像をアップロードし、対応するキャプションを設定
6. 【画像候補】プレースホルダー行をnote上で削除
7. メタデータブロック（File Name・Agency 等）は本文冒頭のまま残す
8. プレビューで表示確認（Markdownレンダリング崩れがないか）
9. note 上での最終タイトル確認（【AI概要版】タグを含むか）
10. 公開 → note URL を控える"""

    # 公開状態バナー
    if blocked:
        publish_status_lines = [
            "## 公開状態",
            "",
            "⛔ **この記事は公開ブロック中です。note公開を行わないでください。**",
            "",
            f"- **ready_to_publish**: {'true' if ready else 'false'}　（内部作業は完了）",
            f"- **publish_blocked**: true　（公開順ルールにより待機中）",
        ]
        if block_reason:
            publish_status_lines.append(f"- **publish_block_reason**: {block_reason}")
        publish_status_lines += [
            "",
            "**対応**: note に下書き保存するところまで実施する。一般公開は publish_blocked が解除されてから。",
            "",
            "---",
            "",
        ]
    else:
        publish_status_lines = [
            "## 公開状態",
            "",
            f"- **ready_to_publish**: {'true' if ready else 'false（内部作業が未完了の可能性あり）'}",
            "- **publish_blocked**: false（公開可）",
            "",
            "---",
            "",
        ]

    lines = [
        f"# Review Package — {article_id_fmt} {args.slug}",
        "",
        f"**生成日時**: {now}",
        f"**スクリプト**: scripts/review_package_generator.py v{VERSION}",
        "",
        "---",
        "",
        "## 記事情報",
        "",
        f"- **article_id**: {article_id_fmt}",
        f"- **slug**: {args.slug}",
        "",
        "---",
        "",
    ]
    lines += publish_status_lines

    lines += [
        "## ファイルパス",
        "",
        f"- **noteドラフト**: `{args.draft}`",
        f"- **Codex監査レポート**: `{args.codex_report}`",
    ]

    if args.rule_report:
        lines.append(f"- **Rule Candidateレポート**: `{args.rule_report}`")

    lines += [
        "",
        "---",
        "",
        "## 使用画像候補",
        "",
    ]
    lines += image_lines

    lines += [
        "---",
        "",
        "## 公開前チェックリスト",
        "",
        "✅ = 自動確認済み　[ ] = 人間確認が必要",
        "",
    ]
    lines += rule_check_lines

    lines += [
        "",
        "---",
        "",
        "## note 転記手順",
        "",
        note_steps,
        "",
        "---",
        "",
        "## 公開後の作業",
        "",
    ]

    if blocked:
        lines += [
            "⛔ **publish_blocked = true のため、post_publish_workflow は実行しないでください。**",
            "",
            "publish_blocked が解除（前 Release の公開完了）されたら、以下を実行してください：",
            "",
        ]
    else:
        lines += [
            "note 公開後は **post_publish_workflow** へ進んでください。",
            "",
        ]

    lines += [
        "```",
        "python3 scripts/post_publish_workflow.py \\",
        f"    --slug {args.slug} \\",
        f"    --draft {args.draft} \\",
        "    --note-url https://note.com/deft_ibis3303/n/XXXX \\",
        f"    --audit {args.codex_report}",
        "```",
        "",
        "post_publish_workflow が行うこと:",
        "- published_articles/ への保存版コピー生成",
        f"- source_registry.csv への {article_id_fmt} エントリ追加（手動確認後）",
        "- git commit 準備（コマンド表示のみ・実行は人間が行う）",
        "",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Finder opener
# ---------------------------------------------------------------------------

def open_in_finder(paths: list[str]) -> None:
    """macOS Finder で指定パスを選択状態で表示する。"""
    for p in paths:
        resolved = Path(p).resolve()
        if resolved.exists():
            subprocess.run(["open", "-R", str(resolved)], check=False)
        else:
            print(f"  [FINDER SKIP] 存在しないパス: {p}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    print(f"[review_package_generator] v{VERSION}", file=sys.stderr)
    print(f"  article_id : {args.article_id}", file=sys.stderr)
    print(f"  slug       : {args.slug}", file=sys.stderr)

    # ファイル存在チェック
    ok_draft, msg_draft = check_file(args.draft, "ドラフト")
    ok_codex, msg_codex = check_file(args.codex_report, "Codex監査レポート")
    ok_rule,  msg_rule  = check_file(args.rule_report, "Rule Candidateレポート") if args.rule_report else (True, "Rule Candidateレポート: 未指定（任意）")

    for ok, msg in [(ok_draft, msg_draft), (ok_codex, msg_codex), (ok_rule, msg_rule)]:
        status = "✓" if ok else "✗"
        print(f"  [{status}] {msg}", file=sys.stderr)

    if not ok_draft or not ok_codex:
        print("[ERROR] 必須ファイルが存在しません。", file=sys.stderr)
        sys.exit(1)

    # Codex VERDICT 取得
    verdict = get_codex_verdict(args.codex_report)
    print(f"  Codex VERDICT: {verdict}", file=sys.stderr)

    # Rule Candidate サマリー
    rule_summary = get_rule_candidate_summary(args.rule_report) if args.rule_report else "レポートなし"

    # ドラフト簡易チェック
    draft_checks = check_draft_rules(args.draft)

    # Review Package 本文生成
    content = build_package(args, verdict, rule_summary, draft_checks)

    if args.dry_run:
        print("\n" + "=" * 60, file=sys.stderr)
        print("[DRY-RUN] 以下の内容が生成されます（ファイル書き込みなし）", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(content)
        print(file=sys.stderr)
        print("[DRY-RUN] 完了。--dry-run を外すと実際に生成されます。", file=sys.stderr)
        return

    # 出力ディレクトリ作成
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"#{args.article_id}_{args.slug}_review_package.md"

    output_path.write_text(content, encoding="utf-8")
    print(f"[OK] Review Package 生成: {output_path}", file=sys.stderr)

    # Finder 表示
    if args.open_finder:
        print("[FINDER] ファイルを Finder で表示します...", file=sys.stderr)
        finder_targets = [args.draft]
        finder_targets += [img for img, _ in (args.images or []) if Path(img).exists()]
        finder_targets.append(str(output_path))
        open_in_finder(finder_targets)

    print(f"[review_package_generator] 完了: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
