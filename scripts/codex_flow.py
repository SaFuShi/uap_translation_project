#!/usr/bin/env python3
"""
codex_flow.py — Codex 監査フロー実行スクリプト（メイン）

使い方:
  [通常モード] agmsg 経由で Codex へ送信し、レスポンスを自動解析
    python3 scripts/codex_flow.py --slug <スラッグ> --request-path <依頼ファイル>

  [フォールバックモード] 手動でペースト保存したレスポンスを解析（§9 Fallback Plan）
    python3 scripts/codex_flow.py --slug <スラッグ> --fallback --response-path <レスポンスファイル>

動作環境: Mac Studio（メイン）
前提条件:
  - init_db.py で DB 初期化済み
  - codex_request_gen.py で依頼パッケージ生成済み（通常モード）
  - agmsg インストール済み（通常モード）

フォールバック手順（agmsg 不使用時）:
  1. review_requests/<slug>.md を開いて Codex（ChatGPT）にペースト
  2. Codex の出力を review_reports/codex_audit_YYYYMMDD_<slug>_manual.md に保存
  3. --fallback --response-path <そのファイル> で実行

Current Owner 制御（§3-A）:
  - 送信前: CLAUDE → CODEX に更新
  - 受信後: CODEX → CLAUDE に更新
  - WARN/BLOCK 時: CLAUDE → HUMAN に更新（人間確認待ち）
"""

import sqlite3
import subprocess
import argparse
import re
import sys
from pathlib import Path
from datetime import datetime

MAX_CODEX_ITERATIONS = 2
AGMSG_TIMEOUT = 120


# ── SQLite ユーティリティ ───────────────────────────────────────────────────

def open_db(db_path: str) -> sqlite3.Connection:
    if not Path(db_path).exists():
        sys.exit(
            f"[ERROR] DB が見つかりません: {db_path}\n"
            "先に python3 scripts/init_db.py を実行してください。"
        )
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con


def get_article_id(con: sqlite3.Connection, slug: str) -> int | None:
    row = con.execute("SELECT id FROM articles WHERE slug = ?", (slug,)).fetchone()
    return row["id"] if row else None


def update_owner(db_path: str, slug: str, owner: str) -> None:
    con = open_db(db_path)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    existing = con.execute(
        "SELECT id FROM workflow_owner WHERE article_slug = ?", (slug,)
    ).fetchone()
    if existing:
        con.execute(
            "UPDATE workflow_owner SET current_owner = ?, updated_at = ? WHERE article_slug = ?",
            (owner, now, slug),
        )
    else:
        con.execute(
            "INSERT INTO workflow_owner (article_slug, current_owner, updated_at) VALUES (?, ?, ?)",
            (slug, owner, now),
        )
    con.commit()
    con.close()
    print(f"[Owner] current_owner → {owner}")


def record_event(
    db_path: str, slug: str, event_type: str, detail: str,
    human_required: int = 0,
    start_time: str = None, end_time: str = None, elapsed_minutes: float = None,
) -> None:
    con = open_db(db_path)
    article_id = get_article_id(con, slug)
    con.execute(
        """INSERT INTO workflow_events
           (article_id, event_type, detail, human_required, start_time, end_time, elapsed_minutes)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (article_id, event_type, detail, human_required, start_time, end_time, elapsed_minutes),
    )
    con.commit()
    con.close()


def record_session(
    db_path: str, slug: str,
    request_path: str, response_path: str, result: dict,
    started_at: str, completed_at: str, auto_triggered: int,
) -> int:
    con = open_db(db_path)
    article_id = get_article_id(con, slug)
    iteration = 1
    if article_id:
        row = con.execute(
            "SELECT COUNT(*) AS cnt FROM codex_sessions WHERE article_id = ?",
            (article_id,),
        ).fetchone()
        iteration = row["cnt"] + 1

    cur = con.execute(
        """INSERT INTO codex_sessions
           (article_id, iteration, request_path, response_path, model_id,
            verdict, block_count, warn_count, pass_count,
            started_at, completed_at, auto_triggered)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            article_id, iteration, request_path, response_path,
            result.get("model_id", "unknown"),
            result["verdict"], result["block_count"], result["warn_count"], result["pass_count"],
            started_at, completed_at, auto_triggered,
        ),
    )
    session_id = cur.lastrowid

    for code, section, text, fix in result.get("warn_details", []):
        con.execute(
            """INSERT INTO warn_items (session_id, warn_code, phase, description, fix_status)
               VALUES (?, ?, ?, ?, 'pending')""",
            (session_id, code, section, f"{text} | 修正案: {fix}"),
        )

    con.commit()
    con.close()
    return session_id


# ── Codex レスポンスパーサ ──────────────────────────────────────────────────

def parse_codex_response(file_path: str) -> dict:
    """---CODEX_AUDIT_START--- ... ---CODEX_AUDIT_END--- 形式を解析"""
    content = Path(file_path).read_text(encoding="utf-8")

    if "---CODEX_AUDIT_START---" not in content:
        return {"error": "CODEX_AUDIT_START マーカーが見つかりません。Codex の出力フォーマットを確認してください。"}

    def find(pattern: str, default):
        m = re.search(pattern, content)
        return m.group(1) if m else default

    verdict    = find(r'VERDICT:\s*(PASS|WARN|BLOCK)', "UNKNOWN")
    warn_count = int(find(r'WARN_COUNT:\s*(\d+)', "0"))
    block_count= int(find(r'BLOCK_COUNT:\s*(\d+)', "0"))
    pass_count = int(find(r'PASS_COUNT:\s*(\d+)', "0"))
    model_id   = find(r'MODEL:\s*(.+)', "unknown").strip()

    warn_section = ""
    ws = content.find("---WARN_DETAILS_START---")
    we = content.find("---WARN_DETAILS_END---")
    if ws != -1 and we != -1:
        warn_section = content[ws:we]
    warn_details = re.findall(r'(W-\d+):\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+)', warn_section)

    return {
        "verdict":      verdict,
        "warn_count":   warn_count,
        "block_count":  block_count,
        "pass_count":   pass_count,
        "model_id":     model_id,
        "warn_details": warn_details,
    }


# ── agmsg 送信 ──────────────────────────────────────────────────────────────

def run_agmsg(request_path: str, response_path: str) -> int:
    """agmsg 経由で Codex へ送信（agmsg 未インストール時は FileNotFoundError で失敗する）"""
    cmd = [
        "agmsg", "send",
        "--to", "codex",
        "--input", request_path,
        "--output", response_path,
        "--timeout", str(AGMSG_TIMEOUT),
    ]
    print(f"[agmsg] {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] agmsg stderr: {result.stderr.strip()}")
        return result.returncode
    except FileNotFoundError:
        print("[ERROR] agmsg がインストールされていません。--fallback モードを使用してください。")
        return 127


# ── メインフロー ────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Codex 監査フロー実行")
    parser.add_argument("--slug", required=True, help="記事スラッグ")
    parser.add_argument("--request-path",  help="依頼ファイルパス（通常モード）")
    parser.add_argument("--response-path", help="レスポンスファイルパス（出力先 or フォールバック時の入力）")
    parser.add_argument("--db-path", default="workflow.db")
    parser.add_argument("--fallback", action="store_true",
                        help="フォールバックモード: agmsg 不使用・既存レスポンスファイルを解析（§9）")
    args = parser.parse_args()

    slug       = args.slug
    db_path    = args.db_path
    date_str   = datetime.now().strftime("%Y%m%d")
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_ts   = datetime.now()

    if args.fallback:
        # ── フォールバックモード（§9 Fallback Plan）───────────────────
        if not args.response_path:
            sys.exit("[ERROR] --fallback 使用時は --response-path が必要です。")
        response_path = args.response_path
        request_path  = args.request_path or "(fallback: 手動実行)"
        print(f"[FALLBACK] レスポンスファイルを直接解析: {response_path}")

    else:
        # ── 通常モード（agmsg 経由）──────────────────────────────────
        if not args.request_path:
            sys.exit("[ERROR] 通常モードでは --request-path が必要です。")
        request_path  = args.request_path
        response_path = args.response_path or \
            f"review_reports/codex_audit_{date_str}_{slug}_auto.md"
        Path("review_reports").mkdir(exist_ok=True)

        # Current Owner: CLAUDE → CODEX
        update_owner(db_path, slug, "CODEX")

        ret = run_agmsg(request_path, response_path)
        if ret != 0:
            update_owner(db_path, slug, "HUMAN")
            record_event(db_path, slug, "error",
                         f"agmsg 失敗 returncode={ret}", human_required=1)
            sys.exit(
                "[停止] agmsg エラー。§9 Fallback Plan の手順で手動実行してください:\n"
                f"  1. {request_path} の内容を Codex (ChatGPT) にペースト\n"
                f"  2. 出力を {response_path} に保存\n"
                f"  3. python3 scripts/codex_flow.py --slug {slug} "
                f"--fallback --response-path {response_path}"
            )

        # Current Owner: CODEX → CLAUDE
        update_owner(db_path, slug, "CLAUDE")

    # ── レスポンス解析 ───────────────────────────────────────────────────────
    if not Path(response_path).exists():
        sys.exit(f"[ERROR] レスポンスファイルが見つかりません: {response_path}")

    result = parse_codex_response(response_path)
    if "error" in result:
        sys.exit(f"[ERROR] パース失敗: {result['error']}")

    completed_at  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elapsed_min   = (datetime.now() - start_ts).total_seconds() / 60

    # SQLite 記録
    auto_flag   = 0 if args.fallback else 1
    session_id  = record_session(
        db_path, slug, request_path, response_path, result,
        started_at, completed_at, auto_flag,
    )
    record_event(
        db_path, slug, "codex_received",
        f"verdict={result['verdict']} warn={result['warn_count']} block={result['block_count']}",
        start_time=started_at, end_time=completed_at,
        elapsed_minutes=round(elapsed_min, 2),
    )

    # ── 結果サマリー表示 ─────────────────────────────────────────────────────
    mode_label = "FALLBACK" if args.fallback else "AUTO"
    print(f"\n{'='*56}")
    print(f"[Codex 監査結果] {slug}  ({mode_label})")
    print(f"  判定  : {result['verdict']}")
    print(f"  BLOCK : {result['block_count']}  WARN : {result['warn_count']}  PASS : {result['pass_count']}")
    print(f"  モデル: {result['model_id']}")
    print(f"  所要  : {elapsed_min:.1f} 分  (目標 Codex 往復 5 分以内)")

    if result["verdict"] == "BLOCK":
        update_owner(db_path, slug, "HUMAN")
        record_event(db_path, slug, "stopped", "BLOCK判定による完全停止", human_required=1)
        print("\n[BLOCK] 完全停止。BLOCK 内容を確認し、修正指示を与えてください：")
        for code, sec, text, fix in result["warn_details"]:
            print(f"  {code}: [{sec}] {text[:60]}")

    elif result["verdict"] == "WARN":
        update_owner(db_path, slug, "HUMAN")
        record_event(db_path, slug, "warn_presented",
                     f"WARN {result['warn_count']}件を提示", human_required=1)
        print(f"\n[WARN] {result['warn_count']}件の警告があります：")
        for code, sec, text, fix in result["warn_details"]:
            print(f"  {code}: {sec}")
            print(f"    該当 : {text[:80]}")
            print(f"    修正案: {fix[:80]}")
        print("\n[停止] 各 WARN を確認・対応後、Claude Code に結果を報告してください。")

    else:
        print("\n[PASS] 監査合格。git / 公開は人間が判断してください。")

    print(f"{'='*56}")
    print(f"[SQLite] session_id={session_id}  db={db_path}")


if __name__ == "__main__":
    main()
