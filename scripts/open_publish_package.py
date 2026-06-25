#!/usr/bin/env python3
"""
open_publish_package.py — 公開パッケージ一括Finder表示

目的:
  article_id（または #2_XXX / publish_order）を渡すと
  対応するドラフト・thumbnail・フレーム・ソースファイルを
  Finder で一括表示する。

使い方:
  python3 scripts/open_publish_package.py --article-id R02-010
  python3 scripts/open_publish_package.py --h2 2010
  python3 scripts/open_publish_package.py --article-id R02-010 --open-source
  python3 scripts/open_publish_package.py --article-id R02-010 --dry-run

オプション:
  --article-id   R02-010 形式で指定
  --h2           2010（publish_order）形式で指定
  --open-source  ソースMP4をQuickTimeで開く（省略時はパス表示のみ）
  --dry-run      コマンドを表示するのみ（Finderを開かない）

安全方針:
  - workflow.db / source_registry.csv は変更しない
  - note公開なし / git操作なし
  - open コマンドは macOS のみ対応
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

# ── マッピング（update_release02_draft_ids.py と同一定義） ─────────────────
# (glob_key, r02_num, publish_order)
MAPPING: list[tuple[str, int, int]] = [
    ("DOW-UAP-PR019", 10, 2010),
    ("DOW-UAP-PR021", 11, 2011),
    ("DOW-UAP-PR022", 12, 2012),
    ("DOW-UAP-PR023", 13, 2013),
    ("DOW-UAP-PR026", 14, 2014),
    ("DOW-UAP-PR027", 15, 2015),
    ("DOW-UAP-PR028", 16, 2016),
    ("DOW-UAP-PR029", 17, 2017),
    ("DOW-UAP-PR031", 18, 2018),
    ("DOW-UAP-PR032", 19, 2019),
    ("DOW-UAP-PR033", 20, 2020),
    ("DOW-UAP-PR034", 21, 2021),
    ("DOW-UAP-PR035", 22, 2022),
    ("DOW-UAP-PR036", 23, 2023),
    ("DOW-UAP-PR037", 24, 2024),
    ("DOW-UAP-PR038", 25, 2025),
    ("DOW-UAP-PR039", 26, 2026),
    ("DOW-UAP-PR040", 27, 2027),
    ("DOW-UAP-PR041", 28, 2028),
    ("DOW-UAP-PR042", 29, 2029),
    ("DOW-UAP-PR043", 30, 2030),
    ("DOW-UAP-PR044", 31, 2031),
    ("DOW-UAP-PR045", 32, 2032),
    ("DOW-UAP-PR046", 33, 2033),
    ("DOW-UAP-PR047", 34, 2034),
    ("DOW-UAP-PR048", 35, 2035),
    ("DOW-UAP-PR049", 36, 2036),
    ("FBI-UAP-PR001", 37, 2037),
    ("FBI-UAP-PR002", 38, 2038),
    ("FBI-UAP-PR003", 39, 2039),
    ("FBI-UAP-PR004", 40, 2040),
    ("FBI-UAP-PR005", 41, 2041),
    ("FBI-UAP-PR006", 42, 2042),
    ("DOW-UAP-PR053", 43, 2043),
    ("DOW-UAP-PR054", 44, 2044),
    ("DOW-UAP-PR055", 45, 2045),
    ("DOW-UAP-PR056", 46, 2046),
    ("DOW-UAP-PR059", 51, 2051),
    ("DOW-UAP-PR060", 52, 2052),
    ("DOW-UAP-PR061", 53, 2053),
    ("DOW-UAP-PR062", 54, 2054),
    ("DOW-UAP-PR063", 55, 2055),
    ("DOW-UAP-PR064", 56, 2056),
    ("DOW-UAP-PR065", 57, 2057),
    ("DOW-UAP-PR066", 58, 2058),
    ("DOW-UAP-PR067", 59, 2059),
    ("DOW-UAP-PR068", 60, 2060),
    ("DOW-UAP-PR069", 61, 2061),
    ("DOW-UAP-PR071", 62, 2062),
    ("DOW-UAP-PR072", 63, 2063),
    ("DOW-UAP-PR073", 64, 2064),
    ("DOW-UAP-PR074", 65, 2065),
    ("DOW-UAP-PR075", 66, 2066),
    ("DOW-UAP-PR076", 67, 2067),
    ("DOW-UAP-PR077", 68, 2068),
    ("DOW-UAP-PR078", 69, 2069),
    ("DOW-UAP-PR079", 70, 2070),
    ("DOW-UAP-PR080", 71, 2071),
    ("DOW-UAP-PR081", 72, 2072),
    ("DOW-UAP-PR082", 73, 2073),
    ("DOW-UAP-PR083", 74, 2074),
    ("DOW-UAP-PR084", 75, 2075),
    ("DOW-UAP-PR085", 76, 2076),
    ("DOW-UAP-PR086", 77, 2077),
    ("DOW-UAP-PR087", 78, 2078),
    ("DOW-UAP-PR088", 79, 2079),
    ("DOW-UAP-PR089", 80, 2080),
    ("DOW-UAP-PR090", 81, 2081),
    ("DOW-UAP-PR091", 82, 2082),
    ("DOW-UAP-PR092", 83, 2083),
    ("DOW-UAP-PR093", 84, 2084),
    ("DOW-UAP-PR094", 85, 2085),
    ("DOW-UAP-PR095", 86, 2086),
    ("DOW-UAP-PR096", 87, 2087),
    ("DOW-UAP-PR097", 88, 2088),
    ("DOW-UAP-PR099", 89, 2089),
    ("DOW-UAP-PR052", 90, 2090),
    ("DOW-UAP-PR070", 91, 2091),
]

DRAFTS_DIR   = Path("note_drafts")
ARCHIVE_DIR  = DRAFTS_DIR / "archive"
THUMBS_DIR   = Path("thumbnails")
SOURCE_DIR   = Path("raw_media/video")
REPORTS_DIR  = Path("review_reports")
DB_PATH      = Path("workflow.db")


def get_published_orders() -> set[int]:
    if not DB_PATH.exists():
        return set()
    conn = sqlite3.connect(str(DB_PATH))
    try:
        rows = conn.execute(
            "SELECT publish_order FROM articles "
            "WHERE status='published' AND publish_order IS NOT NULL"
        ).fetchall()
        return {row[0] for row in rows}
    finally:
        conn.close()


def find_next_unpublished() -> tuple[str, int, int] | None:
    """MAPPING から未公開の最小 publish_order エントリを返す（>= 2010）。"""
    published = get_published_orders()
    for entry in sorted(MAPPING, key=lambda x: x[2]):
        glob_key, r02_num, po = entry
        if po >= 2010 and po not in published:
            return entry
    return None


def parse_codex_verdict(codex: Path | None) -> str:
    if not codex or not codex.exists():
        return "UNKNOWN"
    text = codex.read_text(encoding="utf-8")
    m = re.search(r"VERDICT:\s*(PASS|WARN|BLOCK)", text)
    return m.group(1) if m else "UNKNOWN"


def find_entry(article_id: str | None, publish_order: int | None) -> tuple[str, int, int] | None:
    for glob_key, r02_num, po in MAPPING:
        if article_id and f"R02-{r02_num:03d}" == article_id:
            return (glob_key, r02_num, po)
        if publish_order and po == publish_order:
            return (glob_key, r02_num, po)
    return None


def find_draft(glob_key: str) -> Path | None:
    candidates = [
        p for p in DRAFTS_DIR.glob(f"ai_summary_{glob_key}_*_note_version.md")
        if ARCHIVE_DIR not in p.parents and p.parent == DRAFTS_DIR
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda p: len(p.name))
    return candidates[0]


def find_thumbnail_dir(glob_key: str) -> Path | None:
    candidates = list(THUMBS_DIR.glob(f"{glob_key}*/"))
    if not candidates:
        return None
    # 長名ディレクトリを優先（正規化方針）
    candidates.sort(key=lambda p: len(p.name), reverse=True)
    return candidates[0]


def find_frames(thumb_dir: Path) -> list[Path]:
    frames = sorted(thumb_dir.glob("frame_*.png"))
    return frames


def find_source(glob_key: str) -> Path | None:
    candidates = list(SOURCE_DIR.glob(f"{glob_key}_*.mp4"))
    if not candidates:
        return None
    return candidates[0]


def find_codex_audit(glob_key: str) -> Path | None:
    candidates = list(REPORTS_DIR.glob(f"codex_audit_*_{glob_key}*.md"))
    if not candidates:
        return None
    # iter番号でソートして最新を返す
    def sort_key(p: Path) -> tuple[int, str]:
        name = p.stem
        import re
        m = re.search(r"_iter(\d+)$", name)
        iter_num = int(m.group(1)) if m else 0
        return (iter_num, name)
    candidates.sort(key=sort_key, reverse=True)
    return candidates[0]


def run_open(path: str | Path, reveal: bool = False, dry_run: bool = False) -> None:
    """macOS open コマンドを実行する。reveal=True で Finder に選択表示。"""
    cmd = ["open", "-R", str(path)] if reveal else ["open", str(path)]
    print(f"  $ {' '.join(cmd)}")
    if not dry_run:
        subprocess.run(cmd, check=False)


def print_package(
    glob_key: str,
    r02_num: int,
    po: int,
    draft: Path | None,
    thumb_dir: Path | None,
    frames: list[Path],
    source: Path | None,
    codex: Path | None,
    open_source: bool,
    dry_run: bool,
    show_publish_done: bool = False,
) -> None:
    article_id = f"R02-{r02_num:03d}"
    h2_xxx = f"#2_{r02_num:03d}"
    eyecatch = frames[1] if len(frames) > 1 else frames[0] if frames else None

    print(f"\n{'='*60}")
    print(f"  {h2_xxx} / {article_id} / publish_order: {po}")
    print(f"  glob_key: {glob_key}")
    print(f"{'='*60}")

    print(f"\n[draft]")
    if draft:
        print(f"  {draft}")
        print(f"  Finder 表示:")
        run_open(draft, reveal=True, dry_run=dry_run)
    else:
        print(f"  ⚠️ ドラフトが見つかりません")

    print(f"\n[thumbnail dir]")
    if thumb_dir:
        print(f"  {thumb_dir}")
        print(f"  Finder 表示:")
        run_open(thumb_dir, reveal=False, dry_run=dry_run)
    else:
        print(f"  ⚠️ thumbnail ディレクトリが見つかりません")

    print(f"\n[frames]")
    if frames:
        for f in frames:
            marker = " ← アイキャッチ推奨" if f == eyecatch else ""
            print(f"  {f}{marker}")
    else:
        print(f"  ⚠️ フレームが見つかりません")

    print(f"\n[source]")
    if source:
        print(f"  {source}")
        if open_source:
            print(f"  QuickTime で開く:")
            run_open(source, reveal=False, dry_run=dry_run)
    else:
        print(f"  ⚠️ ソースファイルが見つかりません（raw_media/video/ を確認）")

    print(f"\n[codex audit（最終）]")
    if codex:
        verdict = parse_codex_verdict(codex)
        print(f"  {codex}  [{verdict}]")
    else:
        print(f"  ⚠️ Codex auditが見つかりません")

    if show_publish_done:
        print(f"\n[publish_done.py コマンド（公開後に実行）]")
        print(f"  # 確認のみ:")
        print(f"  python3 scripts/publish_done.py \\")
        print(f"    --note-url https://note.com/deft_ibis3303/n/XXXXXXXX \\")
        print(f"    --dry-run")
        print(f"  # 実行:")
        print(f"  python3 scripts/publish_done.py \\")
        print(f"    --note-url https://note.com/deft_ibis3303/n/XXXXXXXX \\")
        print(f"    --execute")
    else:
        print(f"\n[post_publish_workflow コマンド（公開URL確定後に実行）]")
        slug = draft.stem.removeprefix("ai_summary_").removesuffix("_note_version") if draft else glob_key
        codex_path = str(codex) if codex else "review_reports/codex_audit_YYYYMMDD_<slug>.md"
        print(f"  python3 scripts/post_publish_workflow.py \\")
        print(f"    --slug {slug} \\")
        print(f"    --draft \"{draft}\" \\")
        print(f"    --note-url https://note.com/deft_ibis3303/n/XXXXXXXX \\")
        print(f"    --audit \"{codex_path}\"")


def main() -> None:
    parser = argparse.ArgumentParser(description="公開パッケージ一括Finder表示")
    id_group = parser.add_mutually_exclusive_group(required=True)
    id_group.add_argument("--article-id", help="R02-010 形式")
    id_group.add_argument("--h2", type=int, help="publish_order（例: 2010）")
    id_group.add_argument("--next", action="store_true",
                          help="次の未公開記事を自動判定して表示")
    parser.add_argument("--open-source", action="store_true",
                        help="ソースMP4を QuickTime で開く")
    parser.add_argument("--dry-run", action="store_true",
                        help="コマンドを表示するのみ（Finderを開かない）")
    args = parser.parse_args()

    if not DRAFTS_DIR.is_dir():
        sys.exit("[ERROR] note_drafts/ が見つかりません。プロジェクトルートから実行してください。")

    if args.next:
        entry = find_next_unpublished()
        if not entry:
            print("[INFO] 次の未公開記事が見つかりません（全件公開済み）。")
            return
        show_pd = True
    else:
        entry = find_entry(args.article_id, args.h2)
        if not entry:
            key = args.article_id or str(args.h2)
            sys.exit(f"[ERROR] '{key}' はマッピングに存在しません。")
        show_pd = False

    glob_key, r02_num, po = entry
    draft     = find_draft(glob_key)
    thumb_dir = find_thumbnail_dir(glob_key)
    frames    = find_frames(thumb_dir) if thumb_dir else []
    source    = find_source(glob_key)
    codex     = find_codex_audit(glob_key)

    mode = "DRY-RUN" if args.dry_run else "OPEN"
    print(f"\n[open_publish_package.py] mode={mode}")

    print_package(
        glob_key=glob_key, r02_num=r02_num, po=po,
        draft=draft, thumb_dir=thumb_dir, frames=frames,
        source=source, codex=codex,
        open_source=args.open_source,
        dry_run=args.dry_run,
        show_publish_done=show_pd,
    )

    print(f"\n{'='*60}")
    if args.dry_run:
        print("  dry-run 完了（Finderは開いていません）")
    else:
        print("  Finder表示完了")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
