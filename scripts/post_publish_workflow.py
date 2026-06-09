#!/usr/bin/env python3
"""
post_publish_workflow.py — note公開後の保存版・ログ作成とcommit準備表示

使い方:
  python3 scripts/post_publish_workflow.py \\
    --slug DOE-UAP-D001_pantex_unidentified_object_incident_report \\
    --draft note_drafts/ai_summary_DOE-UAP-D001_pantex_unidentified_object_incident_report_note_version.md \\
    --note-url https://note.com/deft_ibis3303/n/xxxx \\
    --audit review_reports/codex_audit_20260609_DOE-UAP-D001_pantex_unidentified_object_incident_report_iter2.md

安全方針:
  - git add / commit / push は実行しない
  - Mac mini pull は実行しない
  - source_registry.csv は変更しない
  - metadata/uap-csv-cache.csv / raw_pdf / page_images / workflow.db は触らない
"""

import argparse
import re
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path


MAC_MINI_PULL_COMMAND = (
    "ssh agentai@safinoMac-mini.local "
    "'cd /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/repo && git pull'"
)


def shell_quote(path: str) -> str:
    return shlex.quote(path)


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        sys.exit(f"[ERROR] {label} が見つかりません: {path}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_new_file(path: Path, content: str, overwrite: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def ensure_outputs_writable(paths: list[Path], overwrite: bool) -> None:
    existing = [str(path) for path in paths if path.exists()]
    if existing and not overwrite:
        joined = "\n".join(f"  {path}" for path in existing)
        sys.exit(
            "[ERROR] 出力先が既に存在します:\n"
            f"{joined}\n"
            "上書きする場合は --overwrite を指定してください。"
        )


def parse_audit_summary(audit_text: str) -> dict:
    def find(pattern: str, default: str) -> str:
        match = re.search(pattern, audit_text)
        return match.group(1).strip() if match else default

    return {
        "verdict": find(r"VERDICT:\s*(PASS|WARN|BLOCK)", "UNKNOWN"),
        "block_count": find(r"BLOCK_COUNT:\s*(\d+)", "0"),
        "warn_count": find(r"WARN_COUNT:\s*(\d+)", "0"),
        "pass_count": find(r"PASS_COUNT:\s*(\d+)", "0"),
        "model": find(r"MODEL:\s*(.+)", "unknown"),
    }


def build_published_content(draft_text: str, note_url: str, slug: str, today_compact: str) -> str:
    return "\n".join(
        [
            draft_text.rstrip(),
            "",
            "---",
            "",
            "## 公開情報",
            "",
            f"- note公開URL：{note_url}",
            f"- 公開日：{datetime.now().strftime('%Y-%m-%d')}",
            f"- 記事スラッグ：{slug}",
            f"- 保存版作成日：{today_compact}",
            "",
        ]
    )


def build_log_content(
    slug: str,
    note_url: str,
    draft_path: Path,
    audit_path: Path,
    published_path: Path,
    audit_summary: dict,
) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    commit_message = f"publish: add {slug} article archive and log"

    return "\n".join(
        [
            f"# 作業ログ：{slug} 記事 公開完了",
            "",
            f"**日付：** {today}",
            "**フェーズ：** Release 02",
            "",
            "---",
            "",
            "## 1. 公開記事",
            "",
            f"- note公開URL：{note_url}",
            f"- 記事スラッグ：{slug}",
            f"- ドラフト：{draft_path}",
            f"- Codex監査レポート：{audit_path}",
            f"- 公開記事保存版：{published_path}",
            "",
            "---",
            "",
            "## 2. Codex監査サマリー",
            "",
            f"- 判定：{audit_summary['verdict']}",
            f"- BLOCK：{audit_summary['block_count']}",
            f"- WARN：{audit_summary['warn_count']}",
            f"- PASS：{audit_summary['pass_count']}",
            f"- モデル：{audit_summary['model']}",
            "",
            "---",
            "",
            "## 3. source_registry 更新候補（自動変更なし）",
            "",
            "- note_url に上記 note公開URL を記録する候補",
            f"- published_path に {published_path} を記録する候補",
            f"- published_date に {today} を記録する候補",
            "",
            "---",
            "",
            "## 4. commit候補",
            "",
            f"- {published_path}",
            f"- {Path('logs/notebooklm') / (today + '_' + slug + '_published_log.md')}",
            "",
            "## 5. commit message案",
            "",
            f"`{commit_message}`",
            "",
            "## 6. Mac mini pullコマンド案",
            "",
            "```bash",
            MAC_MINI_PULL_COMMAND,
            "```",
            "",
        ]
    )


def git_lines(args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return [f"[git {' '.join(args)} failed] {result.stderr.strip()}"]
    return [line for line in result.stdout.splitlines() if line.strip()]


def print_section(title: str, lines: list[str]) -> None:
    print()
    print(title)
    if lines:
        for line in lines:
            print(f"  {line}")
    else:
        print("  （なし）")


def build_commit_candidates(published_path: Path, log_path: Path) -> list[str]:
    return [
        str(published_path),
        str(log_path),
    ]


def print_git_guidance(slug: str, commit_candidates: list[str]) -> None:
    commit_message = f"publish: add {slug} article archive and log"
    quoted = " ".join(shell_quote(path) for path in commit_candidates)

    print()
    print("実行すべきgitコマンド案（表示のみ・未実行）")
    print(f"  git add {quoted}")
    print(f"  git commit -m {shell_quote(commit_message)}")
    print("  git push origin main")

    print()
    print("Mac mini pullコマンド案（表示のみ・未実行）")
    print(f"  {MAC_MINI_PULL_COMMAND}")


def run(args: argparse.Namespace) -> None:
    slug = args.slug
    draft_path = Path(args.draft)
    audit_path = Path(args.audit)
    today = datetime.now().strftime("%Y-%m-%d")
    today_compact = datetime.now().strftime("%Y%m%d")

    require_file(draft_path, "記事ドラフト")
    require_file(audit_path, "監査レポート")

    published_path = Path("published_articles") / f"ai_summary_{slug}_published_{today_compact}.md"
    log_path = Path("logs/notebooklm") / f"{today}_{slug}_published_log.md"
    ensure_outputs_writable([published_path, log_path], args.overwrite)

    draft_text = read_text(draft_path)
    audit_text = read_text(audit_path)
    audit_summary = parse_audit_summary(audit_text)

    published_content = build_published_content(draft_text, args.note_url, slug, today_compact)
    log_content = build_log_content(
        slug=slug,
        note_url=args.note_url,
        draft_path=draft_path,
        audit_path=audit_path,
        published_path=published_path,
        audit_summary=audit_summary,
    )

    write_new_file(published_path, published_content, args.overwrite)
    write_new_file(log_path, log_content, args.overwrite)

    created_files = [str(published_path), str(log_path)]
    commit_candidates = build_commit_candidates(published_path, log_path)
    excluded_candidates = [
        "metadata/uap-csv-cache.csv",
        "note_drafts/",
        "review_reports/",
        "review_logs/source_registry.csv（自動変更なし・変更候補表示のみ）",
        "raw_pdf/",
        "page_images/",
        "workflow.db",
        "review_requests/",
    ]

    print_section("作成ファイル一覧", created_files)
    print_section("git diff 対象ファイル一覧", git_lines(["diff", "--name-only"]))
    print_section("未追跡ファイル一覧", git_lines(["ls-files", "--others", "--exclude-standard"]))
    print_section("commit対象候補", commit_candidates)
    print_section("commit対象外候補", excluded_candidates)
    print()
    print("source_registry変更候補（表示のみ・未変更）")
    print(f"  note_url={args.note_url}")
    print(f"  published_path={published_path}")
    print(f"  published_date={today}")
    print_git_guidance(slug, commit_candidates)


def main() -> None:
    parser = argparse.ArgumentParser(description="note公開後の保存版・ログ作成とcommit準備表示")
    parser.add_argument("--slug", required=True, help="記事スラッグ")
    parser.add_argument("--draft", required=True, help="note_drafts/ の記事ドラフト")
    parser.add_argument("--note-url", required=True, help="公開済みnote URL")
    parser.add_argument("--audit", required=True, help="Codex監査レポート")
    parser.add_argument("--overwrite", action="store_true", help="既存の保存版・ログを上書きする")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
