#!/usr/bin/env python3
"""
migrate_workflow_db_v1_2.py — workflow.db v1.1 → v1.2 migration

追加カラム（articles テーブル）:
  release_id / series_number / publish_order /
  ready_to_publish / publish_blocked / publish_block_reason / note_draft_url

安全設計:
  --dry-run  : 変更内容を表示するだけ。DB は一切変更しない（デフォルト）
  --execute  : バックアップ作成後に migration を実行する
  冪等性     : 既存カラム / インデックスが存在する場合はスキップ

使い方:
  python3 scripts/migrate_workflow_db_v1_2.py --dry-run
  python3 scripts/migrate_workflow_db_v1_2.py --execute
"""

import argparse
import shutil
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

VERSION        = "1.0.0"
TARGET_SCHEMA  = "1.2"
EXPECTED_SCHEMA = "1.1"
JST            = timezone(timedelta(hours=9))

DB_PATH  = Path("workflow.db")
BAK_PATH = Path("workflow.db.v1.1.bak")

# ────────────────────────────────────────────────────────────
# articles テーブルに追加するカラム定義
# (name, sql_type, description)
# ────────────────────────────────────────────────────────────
NEW_COLUMNS = [
    (
        "release_id",
        "INTEGER",
        "Release番号 (2=Release02, 3=Release03, …)",
    ),
    (
        "series_number",
        "INTEGER",
        "Release 内の公開順序番号 (1〜N)。同一 Release 内で昇順公開",
    ),
    (
        "publish_order",
        "INTEGER",
        "全記事横断の公開順整数 = release_id * 1000 + series_number",
    ),
    (
        "ready_to_publish",
        "INTEGER NOT NULL DEFAULT 0",
        "内部作業完了フラグ (0=未完了, 1=Codex PASS + Review Package + 人間レビュー済み)",
    ),
    (
        "publish_blocked",
        "INTEGER NOT NULL DEFAULT 0",
        "公開順ブロックフラグ (0=公開可, 1=前番号に未公開あり)",
    ),
    (
        "publish_block_reason",
        "TEXT",
        "公開ブロック理由（自由記述）",
    ),
    (
        "note_draft_url",
        "TEXT",
        "note 下書き URL (editor.note.com/notes/…) — 一般公開前に記録",
    ),
]

# ────────────────────────────────────────────────────────────
# 追加するインデックス定義
# (index_name, table_name, column_name)
# ────────────────────────────────────────────────────────────
NEW_INDEXES = [
    ("idx_articles_publish_order",     "articles", "publish_order"),
    ("idx_articles_release_id",        "articles", "release_id"),
    ("idx_articles_ready_to_publish",  "articles", "ready_to_publish"),
    ("idx_articles_publish_blocked",   "articles", "publish_blocked"),
]

# ────────────────────────────────────────────────────────────
# backfill: 既存 published 行の ready_to_publish を 1 に設定
# ────────────────────────────────────────────────────────────
BACKFILL_SQL = (
    "UPDATE articles SET ready_to_publish = 1 WHERE status = 'published';"
)


# ──────────────────────────────────────────────────────────────
# ユーティリティ
# ──────────────────────────────────────────────────────────────

def now_jst() -> str:
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")


def get_existing_columns(con: sqlite3.Connection) -> set:
    rows = con.execute("PRAGMA table_info(articles)").fetchall()
    return {row[1] for row in rows}


def get_existing_indexes(con: sqlite3.Connection) -> set:
    rows = con.execute(
        "SELECT name FROM sqlite_master WHERE type='index'"
    ).fetchall()
    return {row[0] for row in rows}


def get_schema_version(con: sqlite3.Connection) -> str:
    row = con.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()
    return row[0] if row else "unknown"


# ──────────────────────────────────────────────────────────────
# Dry-run 表示
# ──────────────────────────────────────────────────────────────

def run_dry(con: sqlite3.Connection) -> None:
    W = 72
    line = "─" * W
    dline = "=" * W

    print(dline)
    print(f" migration dry-run — workflow.db v{EXPECTED_SCHEMA} → v{TARGET_SCHEMA}")
    print(f" スクリプト v{VERSION} / {now_jst()}")
    print(dline)

    # 前提確認
    current_ver = get_schema_version(con)
    print()
    print("【前提確認】")
    ok = True
    if DB_PATH.exists():
        print(f"  ✅  DB ファイル存在: {DB_PATH}")
    else:
        print(f"  ❌  DB ファイルが見つかりません: {DB_PATH}")
        ok = False

    ver_ok = current_ver == EXPECTED_SCHEMA
    mark = "✅" if ver_ok else "⚠️"
    print(f"  {mark}  現在の schema_version: {current_ver}  (期待値: {EXPECTED_SCHEMA})")
    if not ver_ok:
        print(f"      → schema_version が {EXPECTED_SCHEMA} でない場合、migration は --execute 時に続行を確認します")

    bak_exists = BAK_PATH.exists()
    bak_mark = "⚠️  既存のバックアップあり（上書きされます）" if bak_exists else "（未作成）"
    print(f"  📦  バックアップ先: {BAK_PATH}  {bak_mark}")

    # カラム確認
    existing_cols = get_existing_columns(con)
    print()
    print("【articles テーブル — カラム追加計画】")
    print(line)
    add_count = 0
    for name, sql_type, desc in NEW_COLUMNS:
        if name in existing_cols:
            print(f"  ⏭   SKIP   {name:<28} （既存）")
        else:
            print(f"  ➕  ADD    {name:<28} {sql_type}")
            print(f"             └ {desc}")
            add_count += 1
    print(line)
    print(f"  追加予定: {add_count} カラム  /  スキップ: {len(NEW_COLUMNS) - add_count} カラム")

    # インデックス確認
    existing_idx = get_existing_indexes(con)
    print()
    print("【インデックス追加計画】")
    print(line)
    idx_add = 0
    for idx_name, tbl, col in NEW_INDEXES:
        if idx_name in existing_idx:
            print(f"  ⏭   SKIP   {idx_name}  （既存）")
        else:
            print(f"  ➕  ADD    CREATE INDEX {idx_name} ON {tbl}({col})")
            idx_add += 1
    print(line)
    print(f"  追加予定: {idx_add} インデックス  /  スキップ: {len(NEW_INDEXES) - idx_add} インデックス")

    # Backfill
    count_pub = con.execute(
        "SELECT COUNT(*) FROM articles WHERE status = 'published'"
    ).fetchone()[0]
    print()
    print("【backfill 計画】")
    print(f"  status='published' の既存行 {count_pub} 件 → ready_to_publish = 1 に更新")

    # schema_meta 更新
    print()
    print("【schema_meta 更新計画】")
    print(f"  schema_version: {current_ver} → {TARGET_SCHEMA}")
    print(f"  migrated_to_1.2_at: {now_jst()}")

    # 最終確認
    print()
    print(dline)
    if add_count == 0 and idx_add == 0:
        print(" ℹ️   migration は不要です（全カラム・インデックスが既に存在します）")
    else:
        print(f" ✅  migration 実行で {add_count} カラム + {idx_add} インデックスが追加されます")
        print()
        print(" ⚠️   実際に実行するには --execute オプションを指定してください")
        print("       python3 scripts/migrate_workflow_db_v1_2.py --execute")
    print(dline)


# ──────────────────────────────────────────────────────────────
# 実際の migration 実行
# ──────────────────────────────────────────────────────────────

def run_execute(con: sqlite3.Connection) -> None:
    W = 72
    dline = "=" * W
    line  = "─" * W

    print(dline)
    print(f" migration EXECUTE — workflow.db v{EXPECTED_SCHEMA} → v{TARGET_SCHEMA}")
    print(f" スクリプト v{VERSION} / {now_jst()}")
    print(dline)

    # schema_version 確認
    current_ver = get_schema_version(con)
    if current_ver != EXPECTED_SCHEMA:
        print(f"\n⚠️   schema_version が {EXPECTED_SCHEMA} ではありません（現在: {current_ver}）")
        ans = input("   続行しますか？ [y/N]: ").strip().lower()
        if ans != "y":
            print("   migration を中止しました。")
            sys.exit(0)

    # バックアップ
    print(f"\n【1/5】バックアップ作成中: {BAK_PATH} …")
    shutil.copy2(DB_PATH, BAK_PATH)
    print(f"      完了: {BAK_PATH}  ({BAK_PATH.stat().st_size:,} bytes)")

    existing_cols = get_existing_columns(con)
    existing_idx  = get_existing_indexes(con)

    # BEGIN TRANSACTION
    print(f"\n【2/5】articles テーブル — カラム追加")
    print(line)
    with con:
        for name, sql_type, desc in NEW_COLUMNS:
            if name in existing_cols:
                print(f"  ⏭   SKIP   {name}")
            else:
                sql = f"ALTER TABLE articles ADD COLUMN {name} {sql_type};"
                con.execute(sql)
                print(f"  ✅  ADD    {name:<28} {sql_type}")

    # インデックス
    print(f"\n【3/5】インデックス追加")
    print(line)
    with con:
        for idx_name, tbl, col in NEW_INDEXES:
            if idx_name in existing_idx:
                print(f"  ⏭   SKIP   {idx_name}")
            else:
                sql = f"CREATE INDEX IF NOT EXISTS {idx_name} ON {tbl}({col});"
                con.execute(sql)
                print(f"  ✅  ADD    {idx_name}")

    # Backfill
    print(f"\n【4/5】backfill — published 記事の ready_to_publish 更新")
    with con:
        cur = con.execute(BACKFILL_SQL)
        print(f"  ✅  {cur.rowcount} 件更新 (status='published' → ready_to_publish=1)")

    # schema_meta 更新
    print(f"\n【5/5】schema_meta 更新")
    ts = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    with con:
        con.execute(
            "UPDATE schema_meta SET value = ? WHERE key = 'schema_version'",
            (TARGET_SCHEMA,),
        )
        con.execute(
            "INSERT OR REPLACE INTO schema_meta (key, value) VALUES (?, ?)",
            ("migrated_to_1.2_at", ts),
        )
    ver_now = get_schema_version(con)
    print(f"  ✅  schema_version: {ver_now}")
    print(f"  ✅  migrated_to_1.2_at: {ts}")

    # 最終確認
    print()
    print(dline)
    print(" ✅  migration 完了")
    print(f"     バックアップ: {BAK_PATH}")
    print(f"     schema_version: {ver_now}")
    print()
    print(" 次のステップ:")
    print("   python3 scripts/migrate_workflow_db_v1_2.py --dry-run  （検証）")
    print("   D077 を workflow.db に INSERT する")
    print(dline)


# ──────────────────────────────────────────────────────────────
# エントリポイント
# ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"workflow.db v{EXPECTED_SCHEMA} → v{TARGET_SCHEMA} migration  (スクリプト v{VERSION})",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "例:\n"
            "  python3 scripts/migrate_workflow_db_v1_2.py --dry-run   # 確認のみ\n"
            "  python3 scripts/migrate_workflow_db_v1_2.py --execute   # 実際に実行\n"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="追加予定カラム・インデックスを表示するだけ。DB は変更しない",
    )
    group.add_argument(
        "--execute",
        action="store_true",
        help="バックアップ作成後に migration を実行する",
    )
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"❌  workflow.db が見つかりません: {DB_PATH}")
        print("   スクリプトはプロジェクトルートから実行してください。")
        sys.exit(1)

    con = sqlite3.connect(str(DB_PATH))
    con.row_factory = sqlite3.Row
    try:
        if args.dry_run:
            run_dry(con)
        else:
            run_execute(con)
    finally:
        con.close()


if __name__ == "__main__":
    main()
