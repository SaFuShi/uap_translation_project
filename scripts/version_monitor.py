#!/usr/bin/env python3
"""
version_monitor.py — agmsg / Python / SQLite / bash / DBスキーマのバージョン監視

使い方:
  python3 scripts/version_monitor.py
  python3 scripts/version_monitor.py --db-path workflow.db --warn-log logs/version_warnings.log

動作環境: Mac Studio（メイン） / Mac mini（SSH経由でも可）
前提条件: init_db.py で DB 初期化済みであること

役割:
  セッション開始時に以下を確認し、前回値と差異があれば警告ログを生成する
    - agmsg バージョン
    - Python バージョン
    - SQLite バージョン
    - bash バージョン
    - DB スキーマバージョン（schema_meta テーブル）

  変更検知時は人間に通知し、継続するかどうかを人間が判断する（§4 参照）

推奨タイミング:
  - 各記事制作セッションの開始時
  - agmsg をアップデートした後
  - OS アップデート後
"""

import sqlite3
import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime

EXPECTED_SCHEMA_VERSION = "1.1"


def get_cmd_version(cmd: list[str]) -> str:
    """外部コマンドのバージョン文字列を取得（インストールされていなければ NOT_INSTALLED）"""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        output = (r.stdout + r.stderr).strip()
        return output.splitlines()[0] if output else "（出力なし）"
    except FileNotFoundError:
        return "NOT_INSTALLED"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"


def open_db(db_path: str) -> sqlite3.Connection:
    if not Path(db_path).exists():
        sys.exit(
            f"[ERROR] DB が見つかりません: {db_path}\n"
            "先に python3 scripts/init_db.py を実行してください。"
        )
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con


def check_versions(db_path: str) -> list[dict]:
    """各サービスの現在バージョンを取得して前回値と比較し、変更一覧を返す"""
    targets = [
        {"service": "agmsg",   "version_str": get_cmd_version(["agmsg", "--version"])},
        {"service": "python",  "version_str": f"Python {sys.version.split()[0]}"},
        {"service": "sqlite",  "version_str": get_cmd_version(["sqlite3", "--version"])},
        {"service": "bash",    "version_str": get_cmd_version(["bash", "--version"])},
    ]

    con = open_db(db_path)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    changes = []

    for t in targets:
        prev = con.execute(
            "SELECT version_str FROM model_versions WHERE service = ? ORDER BY id DESC LIMIT 1",
            (t["service"],),
        ).fetchone()
        changed = 1 if (prev and prev["version_str"] != t["version_str"]) else 0

        con.execute(
            """INSERT INTO model_versions (checked_at, service, model_id, version_str, changed)
               VALUES (?, ?, ?, ?, ?)""",
            (now, t["service"], t["service"], t["version_str"], changed),
        )

        if changed:
            changes.append({
                "service": t["service"],
                "from":    prev["version_str"],
                "to":      t["version_str"],
            })
        else:
            print(f"  [{t['service']:10s}] {t['version_str']}")

    # DB スキーマバージョンチェック
    schema_row = con.execute(
        "SELECT value FROM schema_meta WHERE key = 'schema_version'"
    ).fetchone()
    actual_schema = schema_row["value"] if schema_row else "UNKNOWN"
    if actual_schema != EXPECTED_SCHEMA_VERSION:
        changes.append({
            "service": "db_schema",
            "from":    actual_schema,
            "to":      EXPECTED_SCHEMA_VERSION,
        })

    con.commit()
    con.close()
    return changes


def write_warn_log(changes: list[dict], log_path: str) -> None:
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# バージョン変更警告ログ",
        f"生成日時: {now}",
        f"変更件数: {len(changes)}",
        "",
    ]
    for c in changes:
        lines.append(f"- [{c['service']}]")
        lines.append(f"    変更前: {c['from']}")
        lines.append(f"    変更後: {c['to']}")
    lines += [
        "",
        "継続するかどうかは人間が判断してください（§4 バージョン変更検知方法 参照）。",
        "今回の監査結果への影響有無を確認してください。",
    ]
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="バージョン監視・変更検知")
    parser.add_argument("--db-path",  default="workflow.db")
    parser.add_argument("--warn-log", default="logs/version_warnings.log",
                        help="警告ログ出力先（デフォルト: logs/version_warnings.log）")
    args = parser.parse_args()

    print("バージョン確認中...")
    changes = check_versions(args.db_path)

    if not changes:
        print("[OK] バージョン変更なし。フローを継続できます。")
    else:
        print(f"\n[WARN] {len(changes)}件のバージョン変更を検知しました：")
        for c in changes:
            print(f"  [{c['service']}]  {c['from']}  →  {c['to']}")
        write_warn_log(changes, args.warn_log)
        print(f"\n警告ログ: {args.warn_log}")
        print("継続するかどうかを確認してからフローを再開してください。")


if __name__ == "__main__":
    main()
