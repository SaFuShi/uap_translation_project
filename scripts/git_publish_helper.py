#!/usr/bin/env python3
"""
git_publish_helper.py — git未コミット状態の監査レポート自動生成

使い方:
  python3 scripts/git_publish_helper.py           # 通常モード（レポート生成）
  python3 scripts/git_publish_helper.py --dry-run  # ドライラン（生成せず表示のみ）
  python3 scripts/git_publish_helper.py --slug DOW-UAP-PR051  # スラッグ絞り込み

機能:
  - git status から未コミットファイルを一覧表示
  - ファイル種別ごとに分類（note_drafts / review_reports / published_articles / logs / metadata）
  - スラッグ単位でcommit候補グループを自動生成
  - commit message案を表示（実行はしない）
  - git add / commit コマンド案を表示（実行はしない）
  - --report オプションで review_reports/ に監査レポートを書き出す

安全方針:
  - git add / commit / push は実行しない
  - Mac mini pull は実行しない
  - workflow.db は変更しない
  - source_registry.csv は変更しない
  - metadata/uap-csv-cache.csv / raw_pdf / page_images は触らない
"""

import argparse
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


# ── 定数 ─────────────────────────────────────────────────────────────────────

COMMIT_TARGET_DIRS = [
    "note_drafts",
    "review_reports",
    "published_articles",
    "logs",
    "docs",
    "scripts",
    "prompts",
    "provenance",
    "reports",
]

COMMIT_EXCLUDE_PATTERNS = [
    r"^metadata/uap-csv-cache\.csv$",
    r"^raw_pdf/",
    r"^page_images/",
    r"^thumbnails/",
    r"^extracted_text/",
    r"^translated/",
    r"^worker_outputs/",
    r"^workflow\.db$",
    r"^review_logs/source_registry\.csv$",
    r"^classification/",
    r"^review_reports/git_audit_",   # このスクリプト自身が生成するレポート（循環防止）
]

# safe: インフラ・ツール系（スクリプト・ドキュメント）→ commit候補として表示
# review: コンテンツ系（記事ドラフト・監査レポート・ログ）→ 人間確認推奨として表示
SAFE_DIRS = {"scripts", "docs", "prompts", "provenance", "reports"}
REVIEW_DIRS = {"note_drafts", "review_reports", "published_articles", "logs"}

SLUG_EXTRACT_PATTERNS = [
    r"(?:note_drafts|review_reports|published_articles|logs/notebooklm)/[^/]*?([A-Z]{2,6}-UAP-[A-Z0-9]+(?:-\d+)?(?:_[A-Za-z0-9_]+)?)",
    r"([A-Z]{2,6}-UAP-[A-Z0-9]+(?:-\d+)?(?:_[A-Za-z0-9_]+)?)",
    r"(?:note_drafts|review_reports|published_articles|logs/notebooklm)/[^/]*?(western_us_event_slides_\d{8})",
    r"(western_us_event_slides_\d{8})",
]

SLUG_NORMALIZE_PATTERNS = [
    r"_note_version$",
    r"_iter\d+$",
    r"_published_\d{8}$",
]

RELEASE_KEYWORDS = ["release02_intro", "release03_intro"]

MAC_MINI_PULL = (
    "ssh agentai@safinoMac-mini.local "
    "'cd /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/repo && git pull'"
)


# ── データクラス ──────────────────────────────────────────────────────────────

@dataclass
class FileEntry:
    path: str
    status: str   # "modified" / "untracked" / "staged"
    category: str


@dataclass
class CommitGroup:
    slug: str
    files: list = field(default_factory=list)
    tier: str = "review"   # "safe" | "review"

    def commit_message(self) -> str:
        for kw in RELEASE_KEYWORDS:
            if kw in self.slug:
                return f"docs: add {self.slug} note draft and audit reports"
        if any("published_articles" in f for f in self.files):
            return f"publish: add {self.slug} article archive and audit log"
        if any("review_reports" in f for f in self.files):
            return f"docs: add {self.slug} codex audit report(s)"
        return f"docs: add {self.slug} related files"


# ── git ユーティリティ ────────────────────────────────────────────────────────

def run_git(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def get_git_status() -> list[tuple[str, str]]:
    lines = run_git("status", "--porcelain")
    entries = []
    for line in lines:
        if len(line) < 3:
            continue
        xy = line[:2]
        path = line[3:].strip()
        if xy[0] != " " and xy[0] != "?":
            entries.append(("staged", path))
        elif xy[1] == "M":
            entries.append(("modified", path))
        elif xy == "??":
            entries.append(("untracked", path))
        else:
            entries.append(("modified", path))
    return entries


def get_recent_commits(n: int = 5) -> list[str]:
    return run_git("log", "--oneline", f"-{n}")


# ── 分類 ─────────────────────────────────────────────────────────────────────

def is_excluded(path: str) -> bool:
    for pattern in COMMIT_EXCLUDE_PATTERNS:
        if re.match(pattern, path):
            return True
    return False


def categorize(path: str) -> str:
    parts = path.split("/")
    if not parts:
        return "other"
    top = parts[0]
    category_map = {
        "note_drafts": "note_drafts",
        "review_reports": "review_reports",
        "published_articles": "published_articles",
        "logs": "logs",
        "docs": "docs",
        "scripts": "scripts",
        "prompts": "prompts",
        "provenance": "provenance",
        "reports": "reports",
        "metadata": "metadata（commit対象外）",
        "raw_pdf": "raw（commit対象外）",
        "page_images": "raw（commit対象外）",
        "thumbnails": "raw（commit対象外）",
        "extracted_text": "raw（commit対象外）",
        "translated": "raw（commit対象外）",
        "worker_outputs": "raw（commit対象外）",
        "review_logs": "review_logs（要確認）",
    }
    return category_map.get(top, "other")


def normalize_slug(slug: str) -> str:
    for pattern in SLUG_NORMALIZE_PATTERNS:
        slug = re.sub(pattern, "", slug)
    return slug


def extract_slug(path: str) -> str:
    for kw in RELEASE_KEYWORDS:
        if kw in path:
            return kw
    for pattern in SLUG_EXTRACT_PATTERNS:
        m = re.search(pattern, path)
        if m:
            return normalize_slug(m.group(1))
    return "_misc"


# ── グループ化 ────────────────────────────────────────────────────────────────

def file_tier(path: str) -> str:
    top = path.split("/")[0] if "/" in path else ""
    if top in SAFE_DIRS:
        return "safe"
    if top in REVIEW_DIRS:
        return "review"
    return "review"


def group_by_slug(entries: list[FileEntry], slug_filter: str = "") -> dict:
    groups: dict[str, CommitGroup] = {}
    for entry in entries:
        if is_excluded(entry.path):
            continue
        slug = extract_slug(entry.path)
        if slug_filter and slug_filter.lower() not in slug.lower():
            continue
        tier = file_tier(entry.path)
        if slug not in groups:
            groups[slug] = CommitGroup(slug=slug, tier=tier)
        else:
            # いずれかが review なら review に格上げ
            if tier == "review":
                groups[slug].tier = "review"
        groups[slug].files.append(entry.path)
    return groups


# ── 表示 ─────────────────────────────────────────────────────────────────────

def section(title: str) -> None:
    print()
    print(f"{'─' * 56}")
    print(f"  {title}")
    print(f"{'─' * 56}")


def print_file_list(title: str, files: list) -> None:
    print()
    print(f"【{title}】")
    if files:
        for f in files:
            print(f"  {f}")
    else:
        print("  （なし）")


def _print_group(group: CommitGroup, dry_run: bool) -> None:
    msg = group.commit_message()
    quoted = " ".join(shlex.quote(f) for f in group.files)
    tier_label = "[safe]" if group.tier == "safe" else "[要確認]"
    print()
    print(f"  スラッグ: {group.slug}  {tier_label}")
    print(f"  ファイル:")
    for f in group.files:
        print(f"    {f}")
    print(f"  commit message案:")
    print(f"    {msg}")
    prefix = "  [DRY-RUN] " if dry_run else "  "
    print(f"{prefix}gitコマンド案（表示のみ・未実行）:")
    print(f"    git add {quoted}")
    print(f"    git commit -m {shlex.quote(msg)}")


def print_commit_plan(groups: dict, dry_run: bool) -> None:
    if not groups:
        section("commit候補グループ")
        print("  commit対象ファイルが見つかりませんでした。")
        return

    safe_groups   = {s: g for s, g in groups.items() if g.tier == "safe"}
    review_groups = {s: g for s, g in groups.items() if g.tier == "review"}

    section("commit候補グループ [safe] ─ インフラ・ツール系")
    if safe_groups:
        for slug, group in sorted(safe_groups.items()):
            _print_group(group, dry_run)
    else:
        print("  （なし）")

    section("commit候補グループ [要確認] ─ コンテンツ系（人間確認推奨）")
    if review_groups:
        for slug, group in sorted(review_groups.items()):
            _print_group(group, dry_run)
    else:
        print("  （なし）")


# ── レポート生成 ──────────────────────────────────────────────────────────────

def build_report(
    all_entries: list[FileEntry],
    groups: dict,
    excluded: list[str],
    recent_commits: list[str],
    today: str,
) -> str:
    lines = [
        f"# git未コミット状態 監査レポート",
        "",
        f"**生成日時：** {today}",
        f"**スクリプト：** scripts/git_publish_helper.py",
        "",
        "---",
        "",
        "## 1. 未コミットファイル一覧",
        "",
    ]

    by_category: dict[str, list[str]] = {}
    for e in all_entries:
        by_category.setdefault(e.category, []).append(f"[{e.status}] {e.path}")
    for cat, files in sorted(by_category.items()):
        lines.append(f"### {cat}")
        lines.append("")
        for f in files:
            lines.append(f"- {f}")
        lines.append("")

    lines += [
        "---",
        "",
        "## 2. commit対象外ファイル",
        "",
    ]
    if excluded:
        for f in excluded:
            lines.append(f"- {f}")
    else:
        lines.append("（なし）")
    lines.append("")

    safe_groups   = {s: g for s, g in groups.items() if g.tier == "safe"}
    review_groups = {s: g for s, g in groups.items() if g.tier == "review"}

    lines += [
        "---",
        "",
        "## 3a. commit候補 [safe] ─ インフラ・ツール系",
        "",
        "> scripts / docs / prompts / provenance など。内容確認後にcommit可。",
        "",
    ]
    if safe_groups:
        for slug, group in sorted(safe_groups.items()):
            msg = group.commit_message()
            quoted = " ".join(shlex.quote(f) for f in group.files)
            lines.append(f"### {slug}  [safe]")
            lines.append("")
            for f in group.files:
                lines.append(f"- {f}")
            lines.append("")
            lines.append(f"**commit message案:** `{msg}`")
            lines.append("")
            lines.append("```bash")
            lines.append(f"git add {quoted}")
            lines.append(f"git commit -m {shlex.quote(msg)}")
            lines.append("```")
            lines.append("")
    else:
        lines.append("（なし）")
        lines.append("")

    lines += [
        "---",
        "",
        "## 3b. commit候補 [要確認] ─ コンテンツ系（人間確認推奨）",
        "",
        "> note_drafts / review_reports / published_articles / logs など。",
        "> 内容を人間が確認してからcommitしてください。",
        "",
    ]
    if review_groups:
        for slug, group in sorted(review_groups.items()):
            msg = group.commit_message()
            quoted = " ".join(shlex.quote(f) for f in group.files)
            lines.append(f"### {slug}  [要確認]")
            lines.append("")
            for f in group.files:
                lines.append(f"- {f}")
            lines.append("")
            lines.append(f"**commit message案:** `{msg}`")
            lines.append("")
            lines.append("```bash")
            lines.append(f"git add {quoted}")
            lines.append(f"git commit -m {shlex.quote(msg)}")
            lines.append("```")
            lines.append("")
    else:
        lines.append("（なし）")
        lines.append("")

    lines += [
        "---",
        "",
        "## 4. 直近commitログ（参考）",
        "",
    ]
    for c in recent_commits:
        lines.append(f"- {c}")
    lines.append("")

    lines += [
        "---",
        "",
        "## 5. 安全確認",
        "",
        "- [ ] git add / commit / push は自動実行されていない",
        "- [ ] Mac mini pull は自動実行されていない",
        "- [ ] workflow.db は変更されていない",
        "- [ ] source_registry.csv は変更されていない",
        "- [ ] metadata/uap-csv-cache.csv は変更されていない",
        "",
    ]
    return "\n".join(lines)


# ── メイン ────────────────────────────────────────────────────────────────────

def run(args: argparse.Namespace) -> None:
    dry_run = args.dry_run
    slug_filter = args.slug or ""
    today = datetime.now().strftime("%Y-%m-%d")
    today_compact = datetime.now().strftime("%Y%m%d")

    raw_status = get_git_status()
    if not raw_status:
        print("git status: 未コミットファイルはありません。")
        return

    all_entries: list[FileEntry] = []
    excluded_paths: list[str] = []

    for status, path in raw_status:
        cat = categorize(path)
        all_entries.append(FileEntry(path=path, status=status, category=cat))
        if is_excluded(path):
            excluded_paths.append(path)

    groups = group_by_slug(all_entries, slug_filter)

    section("git未コミット状態サマリー")
    by_category: dict[str, list[str]] = {}
    for e in all_entries:
        by_category.setdefault(e.category, []).append(f"[{e.status}] {e.path}")
    for cat, files in sorted(by_category.items()):
        print_file_list(cat, files)

    if excluded_paths:
        print()
        print("【commit対象外（自動除外）】")
        for f in excluded_paths:
            print(f"  {f}")

    print_commit_plan(groups, dry_run)

    section("直近commitログ（参考）")
    for c in get_recent_commits():
        print(f"  {c}")

    section("Mac mini pullコマンド案（表示のみ・未実行）")
    print(f"  {MAC_MINI_PULL}")

    if args.report and not dry_run:
        report_dir = Path("review_reports")
        report_dir.mkdir(exist_ok=True)
        report_path = report_dir / f"git_audit_{today_compact}_pending_commits.md"
        content = build_report(all_entries, groups, excluded_paths, get_recent_commits(10), today)
        report_path.write_text(content, encoding="utf-8")
        print()
        print(f"[OK] 監査レポート生成: {report_path}")
    elif args.report and dry_run:
        print()
        print("[DRY-RUN] --report 指定あり。ドライランのためレポートファイルは生成しません。")

    if dry_run:
        print()
        print("[DRY-RUN] 完了。ファイル生成・git操作はすべて未実行です。")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="git未コミット状態の監査レポート自動生成（git操作は表示のみ）"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="ドライラン（レポートファイル生成なし・git操作なし・表示のみ）",
    )
    parser.add_argument(
        "--slug",
        default="",
        help="スラッグ絞り込み（例: DOW-UAP-PR051）",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="review_reports/ に監査レポートを生成する（--dry-run と併用時は生成しない）",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
