#!/usr/bin/env python3
"""
notebooklm_log_gen.py — NotebookLM 公開ログ自動生成スクリプト

使い方:
  python3 scripts/notebooklm_log_gen.py --slug <スラッグ> --note-url <URL>
  python3 scripts/notebooklm_log_gen.py \\
      --slug western_us_event_slides_20260508 \\
      --note-url https://note.com/deft_ibis3303/n/nXXXXX

動作環境: Mac Studio（メイン）
前提条件:
  - init_db.py で DB 初期化済み
  - codex_flow.py でセッション記録済み
  - articles テーブルに当該スラッグが登録済み

役割:
  SQLite から記事・監査サマリー・タイムラインを取得し、
  logs/notebooklm/YYYY-MM-DD_<slug>_published_log.md のテンプレートを生成する

注意:
  - SSH 鍵・パスワード・IP アドレス・API キーは自動生成ログに含めない
  - [TODO: ...] 箇所は人間が内容を確認・補完してからコミットすること
  - 目標達成判定（45分以内）を elapsed_minutes から自動算出する
"""

import sqlite3
import argparse
import sys
from pathlib import Path
from datetime import datetime

TARGET_ELAPSED_MIN = 45.0   # §7-4 PoC 時短目標


def open_db(db_path: str) -> sqlite3.Connection:
    if not Path(db_path).exists():
        sys.exit(
            f"[ERROR] DB が見つかりません: {db_path}\n"
            "先に python3 scripts/init_db.py を実行してください。"
        )
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con


def fetch_article(con: sqlite3.Connection, slug: str):
    return con.execute("SELECT * FROM articles WHERE slug = ?", (slug,)).fetchone()


def fetch_sessions(con: sqlite3.Connection, article_id: int):
    return con.execute(
        "SELECT * FROM codex_sessions WHERE article_id = ? ORDER BY iteration",
        (article_id,),
    ).fetchall()


def fetch_warn_items(con: sqlite3.Connection, session_id: int):
    return con.execute(
        "SELECT warn_code, description, fix_status FROM warn_items WHERE session_id = ?",
        (session_id,),
    ).fetchall()


def fetch_events(con: sqlite3.Connection, article_id: int):
    return con.execute(
        """SELECT event_type, detail, elapsed_minutes, start_time, end_time
           FROM workflow_events WHERE article_id = ? ORDER BY id""",
        (article_id,),
    ).fetchall()


def calc_total_elapsed(events) -> float:
    return round(sum(e["elapsed_minutes"] for e in events if e["elapsed_minutes"]), 1)


def generate_log(slug: str, note_url: str, db_path: str) -> str:
    con = open_db(db_path)
    art = fetch_article(con, slug)
    if not art:
        con.close()
        sys.exit(
            f"[ERROR] articles テーブルに '{slug}' が見つかりません。\n"
            "先に articles テーブルへ記事情報を登録してください。"
        )

    article_id = art["id"]
    sessions   = fetch_sessions(con, article_id)
    events     = fetch_events(con, article_id)
    total_min  = calc_total_elapsed(events)
    today      = datetime.now().strftime("%Y-%m-%d")
    target_ok  = "✓ 達成" if total_min <= TARGET_ELAPSED_MIN else f"✗ 未達（目標: {TARGET_ELAPSED_MIN}分）"

    out_dir  = Path("logs/notebooklm")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{today}_{slug}_published_log.md"

    lines = [
        f"# 作業ログ：{slug} 記事 公開完了",
        "",
        f"**日付：** {today}  ",
        f"**フェーズ：** Release 02  ",
        "",
        "---",
        "",
        "## 1. 本日の目的",
        "",
        "[TODO: この記事の目的・対象資料の概要を記載]",
        "",
        "---",
        "",
        "## 2. 公開記事の概要",
        "",
        f"- 公開先：note（{note_url}）",
        f"- 公開日：{today}",
        f"- 対象資料：{art['source_pdf'] or '（未登録）'}",
        f"- Agency：{art['agency'] or '（未登録）'}",
        f"- ドラフトファイル：{art['draft_path'] or '（未登録）'}",
        f"- 保存版：{art['pub_path'] or '（未登録）'}",
        f"- 分類：{art['classification']}",
        "",
        "---",
        "",
        "## 3. Codex 監査サマリー",
        "",
    ]

    if not sessions:
        lines.append("（監査セッション記録なし）")
    else:
        for s in sessions:
            warn_items = fetch_warn_items(con, s["id"])
            auto_label = "agmsg 自動" if s["auto_triggered"] else "手動（フォールバック）"
            lines += [
                f"### 監査 {s['iteration']} 回目（{auto_label}）",
                "",
                f"- 判定：**{s['verdict']}**",
                f"- BLOCK: {s['block_count']}  WARN: {s['warn_count']}  PASS: {s['pass_count']}",
                f"- モデル：{s['model_id'] or '不明'}",
                f"- 実行：{s['started_at']} → {s['completed_at']}",
                "",
            ]
            if warn_items:
                lines.append("WARN 対応状況：")
                for w in warn_items:
                    lines.append(f"- {w['warn_code']}: {w['fix_status']}  （{str(w['description'])[:60]}）")
                lines.append("")

    lines += [
        "---",
        "",
        "## 4. タイムライン（elapsed_minutes）",
        "",
        "| フェーズ | 開始 | 終了 | 所要 (分) |",
        "|---------|------|------|---------|",
    ]

    for ev in events:
        elapsed_str = f"{ev['elapsed_minutes']:.1f}" if ev["elapsed_minutes"] else "—"
        start = ev["start_time"] or "—"
        end   = ev["end_time"]   or "—"
        lines.append(f"| {ev['event_type']} | {start} | {end} | {elapsed_str} |")

    lines += [
        "",
        f"**合計所要時間：{total_min} 分**　目標 {TARGET_ELAPSED_MIN} 分以内 → {target_ok}",
        "",
        "---",
        "",
        "## 5. テキスト処理の特記事項",
        "",
        "[TODO: OCR品質・単位混在・note手修正内容等を記載]",
        "",
        "---",
        "",
        "## 6. 次のアクション",
        "",
        "1. [TODO: 次の記事候補・残タスク]",
        "",
        "---",
        "",
        "*このログは NotebookLM へのアップロード用です。"
        "SSH 鍵・パスワード・IP アドレス・API キーは含まれていません。*",
    ]

    con.close()
    content = "\n".join(lines)
    out_path.write_text(content, encoding="utf-8")
    print(f"[OK] NotebookLM ログ生成: {out_path}")
    print(f"     合計所要時間: {total_min} 分  {target_ok}")
    print("     [TODO] 箇所を確認・補完してからコミットしてください。")
    return str(out_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="NotebookLM 公開ログ自動生成")
    parser.add_argument("--slug",     required=True, help="記事スラッグ")
    parser.add_argument("--note-url", required=True, help="note 公開 URL")
    parser.add_argument("--db-path",  default="workflow.db")
    args = parser.parse_args()
    generate_log(args.slug, args.note_url, args.db_path)


if __name__ == "__main__":
    main()
