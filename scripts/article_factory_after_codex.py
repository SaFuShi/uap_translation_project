#!/usr/bin/env python3
"""
article_factory_after_codex.py — Codex PASS後 Article Factory 後処理

v1.0.0

デフォルトは dry-run。--execute で実際に実行する。

使い方:
  # dry-run（推定・判定確認のみ、DB変更なし）
  python3 scripts/article_factory_after_codex.py \\
      --codex-report review_reports/codex_audit_..._iter2.md

  # 実行（DB更新・Review Package生成・在庫レポート生成）
  python3 scripts/article_factory_after_codex.py \\
      --codex-report review_reports/codex_audit_..._iter2.md \\
      --execute

安全方針:
  - --execute なしでは workflow.db を変更しない
  - S_CLASS 文字列を含むスラッグは停止
  - 公開済み記事には何もしない（SKIP）
  - VERDICT=PASS 以外は停止
  - publish_order が NULL の記事は停止（公開順判定不能）
"""

import argparse
import re
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VERSION       = "1.0.0"
BASE          = Path(".")
DB_PATH       = BASE / "workflow.db"
DRAFTS_DIR    = BASE / "note_drafts"
PUBLISHED_DIR = BASE / "published_articles"

GENERATE_SCRIPT  = BASE / "scripts" / "generate_review_package_from_codex.py"
INVENTORY_SCRIPT = BASE / "scripts" / "article_inventory_report.py"

_S_CLASS_RE = re.compile(r"S[_-]?CLASS", re.IGNORECASE)
_FILE_ID_RE = re.compile(r"([A-Z]+-UAP-(?:PR\d+|D\d+))")


# ---------------------------------------------------------------------------
# Codex 解析
# ---------------------------------------------------------------------------

def read_codex_verdict(path: Path) -> tuple:
    """(verdict: str|None, is_new_fmt: bool) を返す。"""
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None, False
    is_new_fmt = "---CODEX_AUDIT_START---" in content
    verdict = None
    for line in content.splitlines():
        if line.startswith("VERDICT:"):
            verdict = line.split(":", 1)[1].strip()
            break
    return verdict, is_new_fmt


# ---------------------------------------------------------------------------
# 推定ユーティリティ
# ---------------------------------------------------------------------------

def infer_file_id(codex_path: Path) -> str:
    """Codex audit ファイル名から file_id（例: DOW-UAP-D077）を抽出する。"""
    stem = re.sub(r"^codex_audit_\d{8}_", "", codex_path.stem)
    stem = re.sub(r"_iter\d+$", "", stem)
    m = _FILE_ID_RE.search(stem)
    return m.group(1) if m else ""


def find_draft(file_id: str) -> Path:
    """note_drafts/ から file_id に対応するドラフトを探す。複数ヒット時は最長名を採用。"""
    candidates = list(DRAFTS_DIR.glob(f"ai_summary_{file_id}*_note_version.md"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: len(p.name))


def is_published(file_id: str) -> tuple:
    """(published: bool, source: str) を返す。"""
    if PUBLISHED_DIR.exists():
        hits = list(PUBLISHED_DIR.glob(f"*{file_id}*_published_*.md"))
        if hits:
            return True, f"published_articles/{hits[0].name}"
    if DB_PATH.exists():
        try:
            con = sqlite3.connect(str(DB_PATH))
            row = con.execute(
                "SELECT status FROM articles WHERE slug LIKE ?",
                (f"%{file_id}%",),
            ).fetchone()
            con.close()
            if row and row[0] == "published":
                return True, "workflow.db status=published"
        except sqlite3.Error:
            pass
    return False, ""


# ---------------------------------------------------------------------------
# workflow.db アクセス
# ---------------------------------------------------------------------------

def lookup_db_article(file_id: str) -> dict:
    """workflow.db から file_id に対応する記事を dict で返す。なければ None。"""
    if not DB_PATH.exists():
        return None
    try:
        con = sqlite3.connect(str(DB_PATH))
        con.row_factory = sqlite3.Row
        row = con.execute(
            """
            SELECT id, article_id, slug, status,
                   release_id, series_number, publish_order,
                   ready_to_publish, publish_blocked, publish_block_reason,
                   draft_path, note_draft_url
            FROM articles
            WHERE slug LIKE ?
            """,
            (f"%{file_id}%",),
        ).fetchone()
        con.close()
        return dict(row) if row else None
    except sqlite3.Error as e:
        print(f"  ❌ DB 読み取りエラー: {e}")
        return None


def determine_publish_blocked(publish_order: int, release_id: int) -> tuple:
    """
    publish_order / release_id に基づいて publish_blocked を判定する。

    優先順位:
      1. 自分より小さい publish_order で未公開記事がある → ブロック
      2. release_id == 3（Release 03）は公開開始待ち → ブロック
      3. ブロックなし

    Returns: (blocked: bool, block_reason: str)
    """
    if not DB_PATH.exists():
        return True, "workflow.db が存在しない"
    try:
        con = sqlite3.connect(str(DB_PATH))
        rows = con.execute(
            """
            SELECT slug, publish_order FROM articles
            WHERE publish_order < ?
              AND publish_order IS NOT NULL
              AND status != 'published'
            ORDER BY publish_order
            """,
            (publish_order,),
        ).fetchall()
        con.close()
    except sqlite3.Error as e:
        return True, f"DB エラー: {e}"

    if rows:
        slug, order = rows[0]
        return True, f"先行記事が未公開 (publish_order={order}: {slug[:50]})"

    if release_id == 3:
        return True, "Release 03公開開始待ち"

    return False, ""


def update_db(db_id: int, blocked: bool, block_reason: str) -> bool:
    """workflow.db を更新する。成功で True。"""
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        con = sqlite3.connect(str(DB_PATH))
        con.execute(
            """
            UPDATE articles
            SET status               = 'ready_to_publish',
                ready_to_publish     = 1,
                publish_blocked      = ?,
                publish_block_reason = ?,
                updated_at           = ?
            WHERE id = ?
            """,
            (1 if blocked else 0, block_reason or None, now, db_id),
        )
        con.commit()
        con.close()
        return True
    except sqlite3.Error as e:
        print(f"  ❌ DB 更新エラー: {e}")
        return False


# ---------------------------------------------------------------------------
# サブプロセス呼び出し
# ---------------------------------------------------------------------------

def call_generate_review_package(codex_path: Path, open_finder: bool, force: bool) -> bool:
    """generate_review_package_from_codex.py --codex-report を呼び出す。"""
    cmd = [
        sys.executable, str(GENERATE_SCRIPT),
        "--codex-report", str(codex_path),
    ]
    if open_finder:
        cmd.append("--open-finder")
    if force:
        cmd.append("--force")
    result = subprocess.run(cmd)
    return result.returncode == 0


def call_inventory_report() -> bool:
    """article_inventory_report.py を呼び出す（通常出力・Markdown生成あり）。"""
    cmd = [sys.executable, str(INVENTORY_SCRIPT)]
    result = subprocess.run(cmd)
    return result.returncode == 0


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Article Factory — Codex PASS後処理  v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "例:\n"
            "  # dry-run（デフォルト）\n"
            "  python3 scripts/article_factory_after_codex.py \\\n"
            "      --codex-report review_reports/codex_audit_..._iter2.md\n\n"
            "  # 実行\n"
            "  python3 scripts/article_factory_after_codex.py \\\n"
            "      --codex-report review_reports/codex_audit_..._iter2.md \\\n"
            "      --execute\n"
        ),
    )
    parser.add_argument(
        "--codex-report", required=True, metavar="PATH",
        help="Codex audit ファイルパス（新フォーマット・PASS のみ受け付ける）",
    )
    parser.add_argument(
        "--article-id", metavar="ID",
        help="article_id 上書き（例: R03-002）。省略時は workflow.db の article_id カラムから自動取得",
    )
    parser.add_argument(
        "--execute", action="store_true",
        help="DB更新・Review Package生成・在庫レポート生成を実行する（省略時は dry-run）",
    )
    parser.add_argument(
        "--open-finder", action="store_true",
        help="Review Package 生成後に macOS Finder で表示",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="既存 Review Package を上書き",
    )
    args = parser.parse_args()

    dry_run = not args.execute

    W     = 80
    dline = "=" * W
    line  = "─" * W

    print(dline)
    mode_label = "[dry-run]" if dry_run else "[EXECUTE]"
    print(f" article_factory_after_codex.py  v{VERSION}  {mode_label}")
    print(dline)

    codex_path = Path(args.codex_report)

    # ── Step 1: ファイル存在確認 ──────────────────────────────────────────
    print(f"\n[Step 1] Codex audit ファイル確認")
    if not codex_path.exists():
        print(f"  ❌ ファイルが見つかりません: {codex_path}")
        sys.exit(1)
    print(f"  ✅ {codex_path.name}")

    # ── Step 2: フォーマット / VERDICT 確認 ─────────────────────────────
    print(f"\n[Step 2] VERDICT 確認")
    verdict, is_new_fmt = read_codex_verdict(codex_path)

    if not is_new_fmt:
        print(f"  ❌ 旧フォーマットです（---CODEX_AUDIT_START--- が見つかりません）")
        sys.exit(1)
    if verdict is None:
        print(f"  ❌ 監査レポートの機械判読ヘッダーが不足しています")
        print(f"     VERDICT: 行が見つかりません。")
        print(f"     ---CODEX_AUDIT_START--- の直後に以下の形式が必要です:")
        print(f"       VERDICT: PASS|WARN|BLOCK")
        print(f"       BLOCK: <件数>")
        print(f"       WARN: <件数>")
        print(f"       UNVERIFIABLE: <件数>")
        print(f"       PASS: <件数>")
        sys.exit(1)
    if verdict != "PASS":
        print(f"  ❌ VERDICT={verdict} — PASS 以外は処理できません（Codex 再監査または人間レビューが必要です）")
        sys.exit(1)
    print(f"  ✅ VERDICT: PASS（新フォーマット）")

    # ── Step 3: file_id 推定 ─────────────────────────────────────────────
    print(f"\n[Step 3] file_id 推定")
    file_id = infer_file_id(codex_path)
    if not file_id:
        print(f"  ❌ file_id を推定できません（ファイル名: {codex_path.name}）")
        sys.exit(1)
    print(f"  ✅ file_id: {file_id}")

    # ── Step 4: S_CLASS ガード ───────────────────────────────────────────
    print(f"\n[Step 4] S_CLASS ガード")
    if _S_CLASS_RE.search(codex_path.name):
        print(f"  ❌ S_CLASS 検出 — 外部送信禁止: {codex_path.name}")
        sys.exit(1)
    print(f"  ✅ S_CLASS 非検出")

    # ── Step 5: 公開済みチェック ─────────────────────────────────────────
    print(f"\n[Step 5] 公開済みチェック")
    pub, pub_source = is_published(file_id)
    if pub:
        print(f"  ⏭  公開済みのためスキップ: {pub_source}")
        sys.exit(0)
    print(f"  ✅ 未公開（処理対象）")

    # ── Step 6: workflow.db 検索 ─────────────────────────────────────────
    print(f"\n[Step 6] workflow.db 検索")
    if not DB_PATH.exists():
        print(f"  ❌ workflow.db が見つかりません: {DB_PATH}")
        sys.exit(1)

    db_row = lookup_db_article(file_id)
    if not db_row:
        print(f"  ❌ workflow.db に {file_id} の登録がありません")
        print(f"     先に workflow.db へ登録してください（release_id / publish_order 必須）")
        sys.exit(1)

    db_id         = db_row["id"]
    release_id    = db_row.get("release_id")
    publish_order = db_row.get("publish_order")
    cur_status    = db_row.get("status", "")

    # article_id: DB の article_id カラム優先。"#" プレフィックスを除去
    db_aid     = (db_row.get("article_id") or "").lstrip("#")
    article_id = args.article_id or db_aid

    print(f"  ✅ id={db_id}  article_id={article_id or '（未設定）'}  release_id={release_id}")
    print(f"     publish_order={publish_order}  current_status={cur_status}")

    if not article_id:
        print(f"  ❌ article_id が未設定です（--article-id で指定するか DB の article_id カラムを更新してください）")
        sys.exit(1)
    if release_id is None or publish_order is None:
        print(f"  ❌ release_id または publish_order が NULL です（公開順判定不能）")
        sys.exit(1)

    # ── Step 7: draft 確認 ───────────────────────────────────────────────
    print(f"\n[Step 7] draft ファイル確認")
    draft = find_draft(file_id)
    if not draft:
        db_draft = db_row.get("draft_path")
        if db_draft:
            p = Path(db_draft)
            if p.exists():
                draft = p
    if draft:
        print(f"  ✅ {draft}")
    else:
        print(f"  ⚠️  draft 未検出（note_drafts/ai_summary_{file_id}*_note_version.md）")
        print(f"     Review Package 生成はスキップされます")

    # ── Step 8: publish_blocked 判定 ────────────────────────────────────
    print(f"\n[Step 8] publish_blocked 判定")
    blocked, block_reason = determine_publish_blocked(publish_order, release_id)
    if blocked:
        print(f"  → publish_blocked: true")
        print(f"  → block_reason:    {block_reason}")
    else:
        print(f"  → publish_blocked: false（公開可）")

    # ── Step 9: 実行計画表示 ────────────────────────────────────────────
    print(f"\n[Step 9] 実行計画")
    print(line)
    print(f"  対象:             {file_id}  (#{article_id})")
    print(f"  Codex:            VERDICT=PASS  ({codex_path.name})")
    print(f"  draft:            {draft or '（未検出 — Review Package スキップ）'}")
    print(f"  ─ DB 更新 ─")
    print(f"    status           → ready_to_publish")
    print(f"    ready_to_publish → 1")
    print(f"    publish_blocked  → {1 if blocked else 0}")
    print(f"    block_reason     → {block_reason or '（なし）'}")
    rp_action = "生成（generate_review_package_from_codex.py --codex-report）" if draft else "スキップ（draft 未検出）"
    print(f"  ─ Review Package ─")
    print(f"    {rp_action}")
    print(f"  ─ Inventory Report ─")
    print(f"    article_inventory_report.py（Markdown生成あり）")
    print(line)

    if dry_run:
        print(f"\n  ℹ️  dry-run モード — workflow.db は変更されていません")
        print(f"     実行するには --execute を追加してください:\n")
        print(f"     python3 scripts/article_factory_after_codex.py \\")
        print(f"         --codex-report {codex_path} \\")
        print(f"         --execute")
        print(f"\n{dline}")
        sys.exit(0)

    # ── Step 10: DB 更新（--execute のみ） ──────────────────────────────
    print(f"\n[Step 10] workflow.db 更新")
    ok = update_db(db_id, blocked, block_reason)
    if not ok:
        sys.exit(1)
    print(f"  ✅ id={db_id} 更新完了")
    print(f"     status=ready_to_publish / ready_to_publish=1 / publish_blocked={1 if blocked else 0}")

    # ── Step 11: Review Package 生成（--execute のみ） ──────────────────
    print(f"\n[Step 11] Review Package 生成")
    if not draft:
        print(f"  ⏭  draft 未検出のためスキップ")
    else:
        ok = call_generate_review_package(codex_path, args.open_finder, args.force)
        if ok:
            print(f"  ✅ Review Package 生成完了")
        else:
            print(f"  ❌ Review Package 生成に失敗しました")

    # ── Step 12: Inventory Report 更新（--execute のみ） ─────────────────
    print(f"\n[Step 12] Article Inventory Report 更新")
    call_inventory_report()

    # ── 完了サマリー ─────────────────────────────────────────────────────
    print(f"\n{dline}")
    print(f" 完了: {file_id}  (#{article_id})")
    print(f"   status           = ready_to_publish")
    print(f"   ready_to_publish = 1")
    print(f"   publish_blocked  = {1 if blocked else 0}")
    if block_reason:
        print(f"   block_reason     = {block_reason}")
    print(f"   次のステップ: Review Package を確認 → note 下書き保存")
    print(dline)


if __name__ == "__main__":
    main()
