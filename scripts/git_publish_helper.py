#!/usr/bin/env python3
"""
git_publish_helper.py — git未コミット状態の監査・本実行スクリプト

使い方:
  [ドライラン（デフォルト）]
    python3 scripts/git_publish_helper.py
    python3 scripts/git_publish_helper.py --dry-run
    python3 scripts/git_publish_helper.py --slug DOW-UAP-PR051

  [レポート生成のみ]
    python3 scripts/git_publish_helper.py --report

  [本実行]
    python3 scripts/git_publish_helper.py \\
      --execute \\
      --commit-message "feat: add new script" \\
      [--doc-id <スラッグ>] \\
      [--skip-pull]

安全方針:
  - --execute がない限り git add / commit / push / ssh pull は実行しない
  - --execute 時は [safe] ファイルのみ add（[要確認] / excluded は追加しない）
  - HARD_STOP_PATTERNS に該当するファイルが add対象に含まれた場合は即座に停止
  - Mac mini pull は ssh agentai@safinoMac-mini.local 経由で
    /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/repo のみに限定
  - Mac Studio 側 /Volumes は Mac mini 同期確認に使用しない
  - workflow.db は変更しない
  - source_registry.csv は変更しない
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

COMMIT_EXCLUDE_PATTERNS = [
    r"^metadata/uap-csv-cache\.csv$",
    r"^metadata/uap-data\.csv$",
    r"^raw_pdf/",
    r"^page_images/",
    r"^thumbnails/",
    r"^extracted_text/",
    r"^translated/",
    r"^worker_outputs/",
    r"^workflow\.db$",
    r"^review_logs/source_registry\.csv$",
    r"^classification/",
    r"^review_requests/",
    r"^review_reports/git_audit_",   # このスクリプト自身の出力（循環防止）
]

# --execute 時の安全停止パターン（1件でも該当 → 即座に全停止）
HARD_STOP_PATTERNS = [
    r"^workflow\.db$",
    r"^review_requests/",
    r"^review_reports/",
    r"^metadata/uap-csv-cache\.csv$",
    r"^metadata/uap-data\.csv$",
    r"^note_drafts/release02_intro_note_version\.md$",
    r"(^|/)\.env$",
    r"\.key$",
    r"(^|/)secrets(/|$)",
    r"[Ss]_[Cc][Ll][Aa][Ss][Ss]",
    r"^uap-data\.csv$",
]

# [safe]: インフラ・ツール系 → --execute の add 対象
SAFE_DIRS = {"scripts", "docs", "prompts", "provenance", "reports"}
# [要確認]: コンテンツ系 → 表示のみ・--execute では追加しない
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

# Mac mini 接続設定（Mac Studio 側 /Volumes は使用しない）
MAC_MINI_HOST = "agentai@safinoMac-mini.local"
MAC_MINI_REPO = "/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/repo"
MAC_MINI_PULL_DISPLAY = (
    f"ssh {MAC_MINI_HOST} "
    f"'cd {MAC_MINI_REPO} && git pull && git log --oneline -1 && git status --short'"
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
        if any("scripts" in f for f in self.files):
            return f"feat: add {self.slug} script"
        return f"docs: add {self.slug} related files"


@dataclass
class ExecuteResult:
    step: str
    ok: bool
    stdout: str = ""
    stderr: str = ""

    def label(self) -> str:
        return "✓" if self.ok else "✗"


# ── git / ssh ユーティリティ ──────────────────────────────────────────────────

def run_git(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def run_git_cmd(args: list[str]) -> tuple[int, str, str]:
    """git コマンドを実行して (returncode, stdout, stderr) を返す。"""
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


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


def run_mac_mini_pull() -> ExecuteResult:
    """ssh 経由で Mac mini の git pull / log / status を実行する。
    Mac Studio 側 /Volumes は使用しない。"""
    cmd = (
        f"cd {MAC_MINI_REPO} && "
        "git pull && git log --oneline -1 && git status --short"
    )
    result = subprocess.run(
        ["ssh", MAC_MINI_HOST, cmd],
        capture_output=True, text=True, timeout=60,
    )
    return ExecuteResult(
        step="mac_mini_pull",
        ok=result.returncode == 0,
        stdout=result.stdout.strip(),
        stderr=result.stderr.strip(),
    )


# ── 分類 ─────────────────────────────────────────────────────────────────────

def is_excluded(path: str) -> bool:
    for pattern in COMMIT_EXCLUDE_PATTERNS:
        if re.match(pattern, path):
            return True
    return False


def is_hard_stop(path: str) -> bool:
    """True のとき --execute を即座に停止する。"""
    for pattern in HARD_STOP_PATTERNS:
        if re.search(pattern, path):
            return True
    return False


def categorize(path: str) -> str:
    top = path.split("/")[0] if "/" in path else path
    category_map = {
        "note_drafts":       "note_drafts",
        "review_reports":    "review_reports",
        "published_articles":"published_articles",
        "logs":              "logs",
        "docs":              "docs",
        "scripts":           "scripts",
        "prompts":           "prompts",
        "provenance":        "provenance",
        "reports":           "reports",
        "metadata":          "metadata（commit対象外）",
        "raw_pdf":           "raw（commit対象外）",
        "page_images":       "raw（commit対象外）",
        "thumbnails":        "raw（commit対象外）",
        "extracted_text":    "raw（commit対象外）",
        "translated":        "raw（commit対象外）",
        "worker_outputs":    "raw（commit対象外）",
        "review_logs":       "review_logs（要確認）",
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


def file_tier(path: str) -> str:
    top = path.split("/")[0] if "/" in path else ""
    if top in SAFE_DIRS:
        return "safe"
    return "review"


# ── グループ化 ────────────────────────────────────────────────────────────────

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
            if tier == "review":
                groups[slug].tier = "review"
        groups[slug].files.append(entry.path)
    return groups


def collect_safe_files(groups: dict, doc_id: str = "") -> list[str]:
    """--execute 時に git add する [safe] ファイルの一覧を返す。
    doc_id が指定された場合はそのスラッグのみ対象とする。"""
    files = []
    for slug, group in groups.items():
        if group.tier != "safe":
            continue
        if doc_id and doc_id.lower() not in slug.lower():
            continue
        files.extend(group.files)
    return files


# ── 安全停止チェック ──────────────────────────────────────────────────────────

def check_safe_to_execute(files: list[str]) -> list[str]:
    """HARD_STOP_PATTERNS に該当するファイルを返す（空なら安全）。"""
    return [f for f in files if is_hard_stop(f)]


# ── 表示 ─────────────────────────────────────────────────────────────────────

def section(title: str) -> None:
    print()
    print(f"{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


def print_file_list(title: str, files: list) -> None:
    print()
    print(f"【{title}】")
    if files:
        for f in files:
            print(f"  {f}")
    else:
        print("  （なし）")


def _print_group(group: CommitGroup, label_prefix: str = "") -> None:
    msg = group.commit_message()
    quoted = " ".join(shlex.quote(f) for f in group.files)
    tier_label = "[safe]" if group.tier == "safe" else "[要確認]"
    print()
    print(f"  スラッグ: {group.slug}  {tier_label}")
    print(f"  ファイル:")
    for f in group.files:
        print(f"    {f}")
    print(f"  commit message案:  {msg}")
    print(f"  {label_prefix}gitコマンド案（表示のみ・未実行）:")
    print(f"    git add {quoted}")
    print(f"    git commit -m {shlex.quote(msg)}")


def print_commit_plan(groups: dict, label_prefix: str = "") -> None:
    safe_groups   = {s: g for s, g in groups.items() if g.tier == "safe"}
    review_groups = {s: g for s, g in groups.items() if g.tier == "review"}

    if not safe_groups and not review_groups:
        section("commit候補グループ")
        print("  commit対象ファイルが見つかりませんでした。")
        return

    section("commit候補グループ [safe] ─ インフラ・ツール系")
    if safe_groups:
        for _, group in sorted(safe_groups.items()):
            _print_group(group, label_prefix)
    else:
        print("  （なし）")

    section("commit候補グループ [要確認] ─ コンテンツ系（人間確認推奨）")
    if review_groups:
        for _, group in sorted(review_groups.items()):
            _print_group(group, label_prefix)
    else:
        print("  （なし）")


def print_execute_plan(safe_files: list[str], commit_message: str, skip_pull: bool) -> None:
    section("本実行計画 (--execute)")
    print()
    print(f"  commit message : {commit_message}")
    print(f"  skip-pull      : {skip_pull}")
    print()
    print("  add 対象ファイル:")
    for f in safe_files:
        print(f"    {f}")
    print()
    quoted = " ".join(shlex.quote(f) for f in safe_files)
    print("  実行予定コマンド（順）:")
    print(f"    git add {quoted}")
    print(f"    git commit -m {shlex.quote(commit_message)}")
    print(f"    git push origin main")
    if not skip_pull:
        print(f"    ssh {MAC_MINI_HOST} 'cd {MAC_MINI_REPO} && git pull && git log --oneline -1 && git status --short'")


# ── 本実行 ────────────────────────────────────────────────────────────────────

def execute_commit(
    safe_files: list[str],
    commit_message: str,
    skip_pull: bool,
) -> list[ExecuteResult]:
    """git add → commit → push → Mac mini pull を順に実行する。
    いずれかが失敗した時点で停止する。"""
    results: list[ExecuteResult] = []

    # 1. git add
    rc, out, err = run_git_cmd(["add", "--"] + safe_files)
    results.append(ExecuteResult("git add", rc == 0, out, err))
    if rc != 0:
        return results

    # 2. git commit
    rc, out, err = run_git_cmd(["commit", "-m", commit_message])
    results.append(ExecuteResult("git commit", rc == 0, out, err))
    if rc != 0:
        return results

    # 3. git push
    rc, out, err = run_git_cmd(["push", "origin", "main"])
    results.append(ExecuteResult("git push", rc == 0, out, err))
    if rc != 0:
        return results

    # 4. Mac mini pull（--skip-pull でなければ）
    if not skip_pull:
        results.append(run_mac_mini_pull())

    return results


def print_execute_results(results: list[ExecuteResult]) -> None:
    section("本実行結果")
    for r in results:
        print()
        print(f"  {r.label()} {r.step}")
        if r.stdout:
            for line in r.stdout.splitlines():
                print(f"      {line}")
        if r.stderr:
            for line in r.stderr.splitlines():
                print(f"      [stderr] {line}")


# ── レポート生成 ──────────────────────────────────────────────────────────────

def build_report(
    all_entries: list[FileEntry],
    groups: dict,
    excluded: list[str],
    recent_commits: list[str],
    today: str,
    execute_results: list[ExecuteResult] = None,
    commit_message: str = "",
    safe_files: list[str] = None,
) -> str:
    lines = [
        "# git未コミット状態 監査レポート",
        "",
        f"**生成日時：** {today}",
        f"**スクリプト：** scripts/git_publish_helper.py",
        f"**モード：** {'本実行 (--execute)' if execute_results is not None else 'ドライラン'}",
        "",
        "---",
        "",
        "## 1. 未コミットファイル一覧（実行時点）",
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

    lines += ["---", "", "## 2. commit対象外ファイル（自動除外）", ""]
    if excluded:
        for f in excluded:
            lines.append(f"- {f}")
    else:
        lines.append("（なし）")
    lines.append("")

    safe_groups   = {s: g for s, g in groups.items() if g.tier == "safe"}
    review_groups = {s: g for s, g in groups.items() if g.tier == "review"}

    lines += [
        "---", "",
        "## 3a. commit候補 [safe] ─ インフラ・ツール系", "",
        "> scripts / docs / prompts / provenance など。--execute で add 対象。", "",
    ]
    if safe_groups:
        for slug, group in sorted(safe_groups.items()):
            msg = group.commit_message()
            quoted = " ".join(shlex.quote(f) for f in group.files)
            lines.append(f"### {slug}  [safe]")
            lines.append("")
            for f in group.files:
                lines.append(f"- {f}")
            lines += ["", f"**commit message案:** `{msg}`", "", "```bash",
                      f"git add {quoted}", f"git commit -m {shlex.quote(msg)}", "```", ""]
    else:
        lines += ["（なし）", ""]

    lines += [
        "---", "",
        "## 3b. commit候補 [要確認] ─ コンテンツ系（人間確認推奨）", "",
        "> note_drafts / review_reports など。--execute では add しない。", "",
    ]
    if review_groups:
        for slug, group in sorted(review_groups.items()):
            msg = group.commit_message()
            quoted = " ".join(shlex.quote(f) for f in group.files)
            lines.append(f"### {slug}  [要確認]")
            lines.append("")
            for f in group.files:
                lines.append(f"- {f}")
            lines += ["", f"**commit message案:** `{msg}`", "", "```bash",
                      f"git add {quoted}", f"git commit -m {shlex.quote(msg)}", "```", ""]
    else:
        lines += ["（なし）", ""]

    lines += ["---", "", "## 4. 直近commitログ（参考）", ""]
    for c in recent_commits:
        lines.append(f"- {c}")
    lines.append("")

    if execute_results is not None:
        lines += ["---", "", "## 5. 本実行結果", ""]
        if commit_message:
            lines.append(f"**commit message:** `{commit_message}`")
            lines.append("")
        if safe_files:
            lines.append("**add 対象ファイル:**")
            for f in safe_files:
                lines.append(f"- {f}")
            lines.append("")
        for r in execute_results:
            status = "成功" if r.ok else "失敗"
            lines.append(f"### {r.step} → {status}")
            lines.append("")
            if r.stdout:
                lines.append("```")
                lines.append(r.stdout)
                lines.append("```")
            if r.stderr:
                lines.append("```")
                lines.append(f"[stderr] {r.stderr}")
                lines.append("```")
            lines.append("")

    lines += [
        "---", "",
        "## 6. 安全確認", "",
        "- [ ] workflow.db は変更されていない",
        "- [ ] source_registry.csv は変更されていない",
        "- [ ] metadata/uap-csv-cache.csv は変更されていない",
        "- [ ] review_reports/git_audit_*.md は commit対象外として除外済み",
        "",
    ]
    return "\n".join(lines)


def save_report(
    all_entries, groups, excluded, recent_commits,
    today, today_compact,
    execute_results=None, commit_message="", safe_files=None,
) -> Path:
    report_dir = Path("review_reports")
    report_dir.mkdir(exist_ok=True)
    mode = "execute" if execute_results is not None else "pending"
    report_path = report_dir / f"git_audit_{today_compact}_{mode}_commits.md"
    content = build_report(
        all_entries, groups, excluded, recent_commits, today,
        execute_results, commit_message, safe_files,
    )
    report_path.write_text(content, encoding="utf-8")
    return report_path


# ── メイン ────────────────────────────────────────────────────────────────────

def run(args: argparse.Namespace) -> None:
    dry_run = args.dry_run or not args.execute
    slug_filter = args.slug or args.doc_id or ""
    today = datetime.now().strftime("%Y-%m-%d")
    today_compact = datetime.now().strftime("%Y%m%d")

    # --execute 引数チェック
    if args.execute and not args.commit_message:
        sys.exit("[ERROR] --execute を使う場合は --commit-message が必要です。")

    # git status 取得
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

    # ── 状態サマリー表示 ─────────────────────────────────────────────────────
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

    label_prefix = "[DRY-RUN] " if dry_run else ""
    print_commit_plan(groups, label_prefix)

    section("直近commitログ（参考）")
    for c in get_recent_commits():
        print(f"  {c}")

    # ── ドライランモード ──────────────────────────────────────────────────────
    if dry_run:
        safe_files_preview = collect_safe_files(groups, args.doc_id or "")
        section("本実行プレビュー（--execute 時の動作確認）")
        if not safe_files_preview:
            print("  [safe] ファイルがありません。--execute しても add 対象がありません。")
        else:
            msg = args.commit_message or "<--commit-message で指定>"
            print_execute_plan(safe_files_preview, msg, args.skip_pull)
        print()
        print(f"  Mac mini pull コマンド案（表示のみ・未実行）:")
        print(f"    {MAC_MINI_PULL_DISPLAY}")

        if args.report:
            report_path = save_report(
                all_entries, groups, excluded_paths, get_recent_commits(10),
                today, today_compact,
            )
            print()
            print(f"[OK] 監査レポート生成: {report_path}")
        print()
        print("[DRY-RUN] 完了。git add / commit / push / Mac mini pull はすべて未実行です。")
        return

    # ── 本実行モード（--execute）─────────────────────────────────────────────
    safe_files = collect_safe_files(groups, args.doc_id or "")

    if not safe_files:
        print()
        print("[STOP] add 対象の [safe] ファイルがありません。処理を中止します。")
        return

    # HARD_STOP チェック
    dangerous = check_safe_to_execute(safe_files)
    if dangerous:
        print()
        print("[HARD STOP] 安全停止条件に該当するファイルが検出されました。")
        for f in dangerous:
            print(f"  危険ファイル: {f}")
        print("git add / commit / push を実行せずに終了します。")
        sys.exit(1)

    print_execute_plan(safe_files, args.commit_message, args.skip_pull)
    print()

    results = execute_commit(safe_files, args.commit_message, args.skip_pull)
    print_execute_results(results)

    # 失敗チェック
    failed = [r for r in results if not r.ok]
    if failed:
        print()
        print(f"[ERROR] {failed[0].step} が失敗しました。後続処理を中止します。")

    # 実行レポート保存
    report_path = save_report(
        all_entries, groups, excluded_paths, get_recent_commits(10),
        today, today_compact,
        execute_results=results,
        commit_message=args.commit_message,
        safe_files=safe_files,
    )
    print()
    print(f"[OK] 実行レポート保存: {report_path}")

    if not failed:
        print()
        print("[DONE] 本実行完了。")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="git未コミット状態の監査・本実行スクリプト"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="ドライラン（表示のみ、git操作なし）",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="本実行: [safe]ファイルを git add → commit → push → Mac mini pull",
    )
    parser.add_argument(
        "--commit-message",
        default="",
        help="commit メッセージ（--execute 時は必須）",
    )
    parser.add_argument(
        "--doc-id",
        default="",
        help="対象スラッグ絞り込み（--execute 時は該当slugのsafeファイルのみadd）",
    )
    parser.add_argument(
        "--slug",
        default="",
        help="表示絞り込み用スラッグ（--doc-id と同義、ドライラン用）",
    )
    parser.add_argument(
        "--skip-pull",
        action="store_true",
        help="--execute 時に Mac mini pull をスキップする",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="review_reports/ に監査レポートを生成（ドライラン時のみ有効）",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
