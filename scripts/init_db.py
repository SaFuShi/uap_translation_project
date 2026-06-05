#!/usr/bin/env python3
"""
init_db.py — UAP Translation Project: SQLite DB 初期化スクリプト

使い方:
  python3 scripts/init_db.py
  python3 scripts/init_db.py --db-path /path/to/workflow.db

動作環境: Mac Studio（メイン） / Mac mini（SSH経由も可）
前提条件: なし（初回実行で workflow.db を新規作成）

テーブル構成 (schema v1.1):
  articles       — 記事マスター（classification カラム含む）
  codex_sessions — Codex 監査セッション（1記事あたり最大2回）
  warn_items     — WARN 項目と修正追跡
  workflow_events— フロー全体のタイムライン（elapsed_minutes 含む）
  model_versions — agmsg/Codex/Python バージョン履歴
  workflow_owner — Current Owner 制御（CLAUDE / CODEX / HUMAN）
  schema_meta    — スキーマバージョン管理
"""

import sqlite3
import argparse
from pathlib import Path
from datetime import datetime

SCHEMA_VERSION = "1.1"

DDL = """
CREATE TABLE IF NOT EXISTS articles (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    slug           TEXT UNIQUE NOT NULL,
    source_pdf     TEXT,
    agency         TEXT,
    draft_path     TEXT,
    pub_path       TEXT,
    note_url       TEXT,
    classification TEXT DEFAULT 'PUBLIC',
    -- classification: PUBLIC / INTERNAL / CONFIDENTIAL / S_CLASS
    status         TEXT DEFAULT 'draft',
    -- status: draft / in_review / warn / blocked / pass / published
    created_at     TEXT DEFAULT (datetime('now','localtime')),
    updated_at     TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS codex_sessions (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id     INTEGER REFERENCES articles(id),
    iteration      INTEGER DEFAULT 1,
    request_path   TEXT,
    response_path  TEXT,
    model_id       TEXT,
    checklist_ver  TEXT,
    verdict        TEXT,
    block_count    INTEGER DEFAULT 0,
    warn_count     INTEGER DEFAULT 0,
    pass_count     INTEGER DEFAULT 0,
    started_at     TEXT,
    completed_at   TEXT,
    auto_triggered INTEGER DEFAULT 1   -- 1=agmsg自動, 0=手動フォールバック
);

CREATE TABLE IF NOT EXISTS warn_items (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id     INTEGER REFERENCES codex_sessions(id),
    warn_code      TEXT,
    phase          TEXT,
    description    TEXT,
    fix_status     TEXT DEFAULT 'pending',
    -- fix_status: pending / applied / rejected / deferred
    human_decision TEXT,
    fixed_at       TEXT
);

CREATE TABLE IF NOT EXISTS workflow_events (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id      INTEGER REFERENCES articles(id),
    event_type      TEXT,
    -- event_type: draft_created / codex_requested / codex_received /
    --             warn_presented / warn_fixed / warn_rejected /
    --             published / git_committed / stopped / error
    detail          TEXT,
    human_required  INTEGER DEFAULT 0,
    human_approved  INTEGER,           -- 1=承認, 0=却下, NULL=未確認
    start_time      TEXT,
    end_time        TEXT,
    elapsed_minutes REAL,
    created_at      TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS model_versions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    checked_at  TEXT,
    service     TEXT,                  -- claude / codex / agmsg / python / sqlite / bash
    model_id    TEXT,
    version_str TEXT,
    changed     INTEGER DEFAULT 0     -- 前回から変更があれば 1
);

CREATE TABLE IF NOT EXISTS workflow_owner (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    article_slug  TEXT NOT NULL,
    current_owner TEXT NOT NULL,       -- CLAUDE / CODEX / HUMAN
    updated_at    TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS schema_meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""


def init_db(db_path: str) -> None:
    path = Path(db_path)
    already_exists = path.exists()
    con = sqlite3.connect(db_path)
    con.executescript(DDL)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con.execute(
        "INSERT OR REPLACE INTO schema_meta (key, value) VALUES (?, ?)",
        ("schema_version", SCHEMA_VERSION),
    )
    con.execute(
        "INSERT OR REPLACE INTO schema_meta (key, value) VALUES (?, ?)",
        ("initialized_at", now),
    )
    con.commit()
    con.close()
    verb = "更新" if already_exists else "新規作成"
    print(f"[OK] {db_path} を{verb}しました（スキーマバージョン: {SCHEMA_VERSION}）")
    print("     テーブル: articles / codex_sessions / warn_items /")
    print("              workflow_events / model_versions / workflow_owner / schema_meta")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="UAP Translation Project SQLite DB 初期化 (schema v1.1)"
    )
    parser.add_argument(
        "--db-path", default="workflow.db",
        help="DB ファイルパス（デフォルト: workflow.db）"
    )
    args = parser.parse_args()
    init_db(args.db_path)


if __name__ == "__main__":
    main()
