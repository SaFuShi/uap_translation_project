#!/usr/bin/env python3
"""
publish_done.py — note公開後の一括後処理

使い方:
  # URLを直接指定（確認のみ）
  python3 scripts/publish_done.py --note-url https://note.com/deft_ibis3303/n/xxxx --dry-run

  # URLを直接指定（実行）
  python3 scripts/publish_done.py --note-url https://note.com/deft_ibis3303/n/xxxx --execute

  # クリップボードからURL取得（確認のみ）
  python3 scripts/publish_done.py --clipboard --dry-run

  # クリップボードからURL取得（実行）
  python3 scripts/publish_done.py --clipboard --execute

動作:
  1. 次の未公開記事を自動判定（workflow.db の published 済み publish_order を除外した最小番号）
  2. post_publish_workflow を実行（published_articles / notebooklm log 作成）
  3. URL二重化チェック・自動修正
  4. workflow.db に INSERT
  5. source_registry.csv に追記
  6. 次の記事コマンドを表示

安全仕様:
  - --execute 明示時のみ変更を実行
  - --dry-run では何も変更しない
  - normalize_url() でURL二重化を防止
  - 既に published の記事には実行しない
  - HOLD / SKIP 除外（workflow.db publish_blocked=1 は対象外）
  - --note-url と --clipboard の同時指定はエラー
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# scripts/ 内の共有データをインポート
sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_publish_package import (
    MAPPING,
    DRAFTS_DIR,
    SOURCE_DIR,
    DB_PATH,
    find_draft,
    find_source,
    find_codex_audit,
    get_published_orders,
    find_next_unpublished,
    parse_codex_verdict,
)

NOTE_BASE      = "https://note.com/deft_ibis3303/n/"
REGISTRY_PATH  = Path("review_logs/source_registry.csv")
WAR_GOV_URL    = "https://www.war.gov/UFO/"


# ── URL正規化 ──────────────────────────────────────────────────────────────

def normalize_url(raw: str) -> str:
    """フルURL・末尾ID・二重化URLのいずれも正規化してフルURLを返す。

    Examples:
      https://note.com/deft_ibis3303/n/n9fac665888a9  → そのまま
      n9fac665888a9                                    → NOTE_BASE + ID
      https://note.com/.../n/https://note.com/.../n/ID → NOTE_BASE + ID  (二重化修正)
    """
    raw = raw.strip()
    m = re.search(r"/n/([^/\s?#]+)", raw)
    if m:
        return NOTE_BASE + m.group(1)
    # note.com を含まない場合はそのままIDとして扱う
    return NOTE_BASE + raw


# ── ファイル操作ヘルパー ───────────────────────────────────────────────────

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_verdict_and_iter(audit_path: Path) -> tuple[str, str]:
    """(verdict, iter_label) を返す。例: ('BLOCK', 'iter2')"""
    verdict = parse_codex_verdict(audit_path)
    m = re.search(r"_iter(\d+)\.md$", audit_path.name)
    iter_label = f"iter{m.group(1)}" if m else "iter?"
    return verdict, iter_label


def slug_from_draft(draft: Path) -> str:
    return draft.stem.removeprefix("ai_summary_").removesuffix("_note_version")


# ── DB / CSV 操作 ──────────────────────────────────────────────────────────

def is_published_in_db(slug: str) -> bool:
    if not DB_PATH.exists():
        return False
    conn = sqlite3.connect(str(DB_PATH))
    try:
        row = conn.execute(
            "SELECT status FROM articles WHERE slug=?", (slug,)
        ).fetchone()
        return row is not None and row[0] == "published"
    finally:
        conn.close()


def do_workflow_db_insert(
    slug: str,
    source: Path | None,
    draft: Path,
    pub_path: Path,
    note_url: str,
    publish_order: int,
    article_id: str,
    today: str,
    dry_run: bool,
) -> None:
    source_pdf = str(source) if source else ""
    if dry_run:
        print(f"  [DRY] workflow.db INSERT: {article_id} slug={slug} publish_order={publish_order}")
        return
    conn = sqlite3.connect(str(DB_PATH))
    try:
        cur = conn.execute(
            """
            INSERT INTO articles (
                slug, source_pdf, agency, draft_path, pub_path,
                note_url, classification, status,
                created_at, updated_at,
                release_id, series_number, publish_order,
                ready_to_publish, publish_blocked,
                publish_block_reason, note_draft_url, article_id
            ) VALUES (?,?,?,?,?,?,'PUBLIC','published',?,?,NULL,NULL,?,1,0,NULL,NULL,?)
            """,
            (
                slug, source_pdf, "Department of War",
                str(draft), str(pub_path), note_url,
                f"{today} 00:00:00", f"{today} 00:00:00",
                publish_order, article_id,
            ),
        )
        conn.commit()
        print(f"  [OK] workflow.db INSERT id={cur.lastrowid} / {article_id}")
    except sqlite3.IntegrityError as e:
        print(f"  [WARN] workflow.db INSERT スキップ（既存エントリの可能性）: {e}")
    finally:
        conn.close()


def do_source_registry_append(
    article_id: str,
    source: Path | None,
    note_url: str,
    draft: Path,
    pub_path: Path,
    today: str,
    verdict: str,
    iter_label: str,
    dry_run: bool,
) -> None:
    sha256 = sha256_file(source) if source else "unknown"
    filename = source.name if source else "unknown.mp4"
    row = ",".join([
        article_id,
        filename,
        WAR_GOV_URL,
        sha256,
        "published",
        note_url,
        str(draft),
        str(pub_path),
        today,
        today,
        f"Release 02 動画記事・Codex {iter_label} {verdict}・公開済み {today}",
    ])
    if dry_run:
        print(f"  [DRY] source_registry.csv 追記: {row[:90]}...")
        return
    with REGISTRY_PATH.open("a", encoding="utf-8") as f:
        f.write(row + "\n")
    print(f"  [OK] source_registry.csv 追記: {article_id}")


# ── URL二重化チェック / 修正 ───────────────────────────────────────────────

def fix_url_doubling(path: Path) -> bool:
    """URL二重化を検出・修正。修正した場合 True を返す。"""
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    fixed = re.sub(
        r"https://note\.com/deft_ibis3303/n/https://note\.com/deft_ibis3303/n/(\S+)",
        r"https://note.com/deft_ibis3303/n/\1",
        text,
    )
    if fixed != text:
        path.write_text(fixed, encoding="utf-8")
        return True
    return False


# ── メイン処理 ────────────────────────────────────────────────────────────

def run(args: argparse.Namespace) -> None:
    dry_run  = args.dry_run
    note_url = normalize_url(args.note_url)
    today    = datetime.now().strftime("%Y-%m-%d")
    today_c  = today.replace("-", "")

    print(f"\n[publish_done.py] mode={'DRY-RUN' if dry_run else 'EXECUTE'}")
    print(f"  note_url (正規化後): {note_url}")

    # 次の未公開記事を自動判定
    entry = find_next_unpublished()
    if not entry:
        print("[INFO] 次の未公開記事が見つかりません（全件公開済み）。")
        return

    glob_key, r02_num, po = entry
    article_id = f"#R02-{r02_num:03d}"
    h2_xxx     = f"#2_{r02_num:03d}"

    draft  = find_draft(glob_key)
    source = find_source(glob_key)
    codex  = find_codex_audit(glob_key)

    if not draft:
        sys.exit(f"[ERROR] ドラフトが見つかりません: {glob_key}")
    if not codex:
        sys.exit(f"[ERROR] Codex audit が見つかりません: {glob_key}")

    slug     = slug_from_draft(draft)
    pub_path = Path("published_articles") / f"ai_summary_{slug}_published_{today_c}.md"
    log_path = Path("logs/notebooklm") / f"{today}_{slug}_published_log.md"
    verdict, iter_label = parse_verdict_and_iter(codex)

    print(f"\n{'='*60}")
    print(f"  対象: {h2_xxx} / {article_id} / publish_order={po}")
    print(f"  slug: {slug}")
    print(f"  Codex: {iter_label} {verdict}")
    print(f"{'='*60}\n")

    # 公開済みチェック
    if is_published_in_db(slug):
        sys.exit(f"[ERROR] {slug} は既に published です。")

    # Step 1: post_publish_workflow
    print("[Step 1] post_publish_workflow 実行...")
    ppw_cmd = [
        "python3", "scripts/post_publish_workflow.py",
        "--slug", slug,
        "--draft", str(draft),
        "--note-url", note_url,
        "--audit", str(codex),
    ]
    if dry_run:
        print(f"  [DRY] {' '.join(ppw_cmd[:2])} ... --note-url {note_url}")
        print(f"  [DRY] → {pub_path}")
        print(f"  [DRY] → {log_path}")
    else:
        if pub_path.exists():
            print(f"  [INFO] published_articles 既存: {pub_path}（スキップ）")
        else:
            result = subprocess.run(ppw_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"  [ERROR] post_publish_workflow 失敗:\n{result.stderr}")
                sys.exit(1)
            print(f"  [OK] {pub_path}")
            print(f"  [OK] {log_path}")

    # Step 2: URL二重化チェック・修正
    print("\n[Step 2] URL二重化チェック...")
    if dry_run:
        print("  [DRY] スキップ")
    else:
        fixed = fix_url_doubling(pub_path) | fix_url_doubling(log_path)
        print(f"  [OK] {'URL二重化を修正しました' if fixed else 'URL二重化なし'}")

    # Step 3: workflow.db
    print("\n[Step 3] workflow.db 登録...")
    do_workflow_db_insert(
        slug=slug, source=source, draft=draft, pub_path=pub_path,
        note_url=note_url, publish_order=po, article_id=article_id,
        today=today, dry_run=dry_run,
    )

    # Step 4: source_registry.csv
    print("\n[Step 4] source_registry.csv 追記...")
    do_source_registry_append(
        article_id=article_id, source=source, note_url=note_url,
        draft=draft, pub_path=pub_path, today=today,
        verdict=verdict, iter_label=iter_label, dry_run=dry_run,
    )

    # 完了サマリー
    print(f"\n{'='*60}")
    if dry_run:
        print(f"  [DRY-RUN完了] 対象: {h2_xxx} / {article_id}")
        print(f"\n  実行する場合:")
        print(f"    python3 scripts/publish_done.py \\")
        print(f"      --note-url {note_url} \\")
        print(f"      --execute")
    else:
        print(f"  [完了] {h2_xxx} / {article_id} / {note_url}")
    print(f"\n  次の記事を確認:")
    print(f"    python3 scripts/open_publish_package.py --next")
    print(f"{'='*60}\n")


def get_clipboard_url() -> str:
    """macOS クリップボードから note URL を取得して返す（生文字列）。"""
    try:
        result = subprocess.run(
            ["pbpaste"], capture_output=True, text=True, check=True
        )
    except FileNotFoundError:
        sys.exit("[ERROR] pbpaste が見つかりません（macOS 専用です）")
    except subprocess.CalledProcessError as e:
        sys.exit(f"[ERROR] pbpaste 失敗: {e}")

    raw = result.stdout.strip()
    if not raw:
        sys.exit("[ERROR] クリップボードが空です")

    # URL形式なのに note.com でない場合はエラー
    if raw.startswith("http") and "note.com" not in raw:
        sys.exit(
            f"[ERROR] クリップボードのURLがnote.comではありません: {raw!r}\n"
            "       note公開後のURLをコピーしてから再実行してください。"
        )

    print(f"  [CLIPBOARD] 取得値: {raw!r}")
    return raw


def main() -> None:
    parser = argparse.ArgumentParser(description="note公開後の一括後処理")

    url_src = parser.add_mutually_exclusive_group(required=True)
    url_src.add_argument(
        "--note-url",
        help="公開済みnote URL（フルURLも末尾IDのみも可）",
    )
    url_src.add_argument(
        "--clipboard", action="store_true",
        help="macOS クリップボードから note URL を取得（pbpaste）",
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="確認のみ（変更なし）")
    mode.add_argument("--execute", action="store_true", help="実際に実行")

    args = parser.parse_args()

    # クリップボードモード: URL を解決して args.note_url に格納
    if args.clipboard:
        args.note_url = get_clipboard_url()

    run(args)


if __name__ == "__main__":
    main()
