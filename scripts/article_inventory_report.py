#!/usr/bin/env python3
"""
article_inventory_report.py — Article Factory 在庫可視化レポート

v0.2.0 — workflow.db v1.2 対応
  - release_id / series_number / publish_order / ready_to_publish /
    publish_blocked / publish_block_reason / note_draft_url を DB から読み取り
  - note_draft_registry.csv との整合性チェック（CONFLICT 警告）
  - publish_order 昇順ソート対応
  - data_source バッジ（🗄️ DB / 📄 CSV）
"""

import argparse
import csv
import re
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

VERSION = "0.2.0"
JST = timezone(timedelta(hours=9))

BASE          = Path(".")
DB_PATH       = BASE / "workflow.db"
REPORTS_DIR   = BASE / "review_reports"
PACKAGES_DIR  = BASE / "review_packages"
DRAFTS_DIR    = BASE / "note_drafts"
REG_CSV       = BASE / "review_logs" / "source_registry.csv"
DRAFT_REG_CSV = BASE / "review_logs" / "note_draft_registry.csv"

# Release 02 未登録の優先記事（source_registry に #R02-004〜007 相当が未登録）
R02_PRIORITY_SLUGS = [
    "CIA-UAP-D001",
    "DOW-UAP-D017",
    "ODNI-UAP-D001",
]

STATUS_LABEL = {
    "published":                "✅ 公開済み",
    "draft_saved_unpublished":  "⏸  下書き保存（公開ブロック中）",
    "ready_to_publish_blocked": "⛔ 公開待機中（ブロック）",
    "ready_to_publish":         "🟢 公開可能",
    "codex_pass":               "🔵 Codex PASS（Review Package 未生成）",
    "codex_warn":               "🟡 Codex WARN（要確認）",
    "codex_block":              "🔴 Codex BLOCK（再監査必要）",
    "draft_ready":              "📝 ドラフトあり（Codex 未監査）",
    "no_draft":                 "⬜ ドラフトなし",
    "unknown":                  "❓ 不明",
}

NEXT_ACTION = {
    "published":                "—",
    "draft_saved_unpublished":  "Release 02 完了後に note 編集画面から公開",
    "ready_to_publish_blocked": "前 Release 完了後に note 公開",
    "ready_to_publish":         "note 公開 → post_publish_workflow",
    "codex_pass":               "Review Package 生成 → 人間レビュー",
    "codex_warn":               "WARN 対応 → Codex iter2 実行",
    "codex_block":              "BLOCK 修正 → Codex 再監査",
    "draft_ready":              "Codex 監査依頼生成 → 実行",
    "no_draft":                 "ドラフト作成",
    "unknown":                  "状態確認",
}


# ---------------------------------------------------------------------------
# ユーティリティ
# ---------------------------------------------------------------------------

def extract_file_id(text: str) -> str:
    """テキストから UAP ファイル ID（例: DOE-UAP-D001、DOW-UAP-PR050）を抽出する。"""
    m = re.search(r"([A-Z]+-UAP-(?:PR\d+|D\d+))", text)
    return m.group(1) if m else ""


def _read_csv(path: Path) -> list:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]


# ---------------------------------------------------------------------------
# データ読み込み
# ---------------------------------------------------------------------------

def load_source_registry() -> dict:
    """source_registry.csv から #R-prefix 記事のみ返す。キー = article_id"""
    data = {}
    for row in _read_csv(REG_CSV):
        aid = row.get("article_id", "")
        if re.match(r"#R\d+", aid):
            data[aid] = row
    return data


def load_note_draft_registry() -> list:
    """note_draft_registry.csv の全行を返す。"""
    return _read_csv(DRAFT_REG_CSV)


def load_workflow_db() -> list:
    """
    workflow.db v1.2 から release_id が設定されている記事を返す。
    DB が存在しない / release_id カラムがない場合は空リストを返す。
    """
    if not DB_PATH.exists():
        return []
    try:
        con = sqlite3.connect(str(DB_PATH))
        con.row_factory = sqlite3.Row
        # release_id カラム存在確認
        col_names = {r[1] for r in con.execute("PRAGMA table_info(articles)").fetchall()}
        if "release_id" not in col_names:
            con.close()
            return []
        rows = con.execute("""
            SELECT slug, status, note_url, draft_path,
                   release_id, series_number, publish_order,
                   ready_to_publish, publish_blocked,
                   publish_block_reason, note_draft_url
            FROM articles
            WHERE release_id IS NOT NULL
            ORDER BY publish_order ASC NULLS LAST
        """).fetchall()
        con.close()
        return [dict(r) for r in rows]
    except sqlite3.Error:
        return []


def check_db_ndr_conflicts(db_row: dict, ndr_row: dict) -> list:
    """
    workflow.db の行と note_draft_registry.csv の行を比較し、
    値が食い違うフィールドの警告文字列リストを返す。
    """
    conflicts = []
    # ready_to_publish: DB=int(1/0) vs NDR=str("true"/"false")
    db_rtp  = "true" if db_row.get("ready_to_publish") == 1 else "false"
    ndr_rtp = ndr_row.get("ready_to_publish", "")
    if ndr_rtp and db_rtp != ndr_rtp:
        conflicts.append(f"ready_to_publish: DB={db_rtp} vs NDR={ndr_rtp}")
    # publish_blocked
    db_blk  = "true" if db_row.get("publish_blocked") == 1 else "false"
    ndr_blk = ndr_row.get("publish_blocked", "")
    if ndr_blk and db_blk != ndr_blk:
        conflicts.append(f"publish_blocked: DB={db_blk} vs NDR={ndr_blk}")
    # note_draft_url
    db_url  = (db_row.get("note_draft_url") or "").strip()
    ndr_url = (ndr_row.get("note_draft_url") or "").strip()
    if db_url and ndr_url and db_url != ndr_url:
        conflicts.append(f"note_draft_url: DB={db_url[:50]} / NDR={ndr_url[:50]}")
    return conflicts


# ---------------------------------------------------------------------------
# 個別ファイル確認
# ---------------------------------------------------------------------------

def get_codex_info(file_id: str) -> tuple:
    """
    file_id（例: DOE-UAP-D001）でレポートを検索し、
    最も高い iter の (verdict, iter_num, is_new_fmt) を返す。
    見つからなければ (None, None, None)。
    """
    key = file_id.lower()
    candidates = []
    if not REPORTS_DIR.exists():
        return None, None, None
    for f in REPORTS_DIR.glob("codex_audit_*.md"):
        if key not in f.name.lower():
            continue
        m = re.search(r"_iter(\d+)", f.name)
        iter_num = int(m.group(1)) if m else 1
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        is_new = "---CODEX_AUDIT_START---" in content
        verdict = None
        if is_new:
            for line in content.splitlines():
                if line.startswith("VERDICT:"):
                    verdict = line.split(":", 1)[1].strip()
                    break
        else:
            # 旧フォーマット: 「総合判定」セクション直下の **X**
            m2 = re.search(
                r"総合判定.{0,200}?\*\*(PASS|WARN|BLOCK)\*\*",
                content,
                re.DOTALL,
            )
            if m2:
                verdict = m2.group(1)
        if verdict:
            candidates.append((iter_num, verdict, is_new))
    if not candidates:
        return None, None, None
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1], candidates[0][0], candidates[0][2]


def find_note_draft(file_id: str) -> tuple:
    """file_id を含む note_draft ファイルを探し (exists: bool, title: str) を返す。"""
    key = file_id.lower()
    if not DRAFTS_DIR.exists():
        return False, ""
    for f in DRAFTS_DIR.glob("ai_summary_*_note_version.md"):
        if key in f.name.lower():
            try:
                first_line = f.read_text(encoding="utf-8", errors="ignore").splitlines()[0]
                title = first_line.lstrip("#").strip()
            except Exception:
                title = f.stem
            return True, title
    return False, ""


def get_review_package_state(article_id: str) -> dict:
    """
    review_package から publish 状態を抽出する。
    存在しなければ {"exists": False}。
    """
    if not PACKAGES_DIR.exists():
        return {"exists": False}
    aid_clean = article_id.lstrip("#")  # "#R03-001" → "R03-001"
    for f in PACKAGES_DIR.glob(f"#{aid_clean}_*.md"):
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        ready   = bool(re.search(r"\*\*ready_to_publish\*\*[^\n]*?true", content))
        blocked = bool(re.search(r"\*\*publish_blocked\*\*[^\n]*?true", content))
        m = re.search(r"\*\*publish_block_reason\*\*[：:]\s*(.+)", content)
        reason = m.group(1).strip() if m else ""
        return {
            "exists":                True,
            "ready_to_publish":      "true" if ready else "false",
            "publish_blocked":       "true" if blocked else "false",
            "publish_block_reason":  reason,
        }
    return {"exists": False}


# ---------------------------------------------------------------------------
# ステータス判定
# ---------------------------------------------------------------------------

def determine_status(rec: dict) -> str:
    published   = rec["published"]
    note_status = rec["note_status"]
    rtp         = rec["ready_to_publish"]
    blk         = rec["publish_blocked"]
    cv          = rec["codex_verdict"]
    draft_ok    = rec["draft_exists"]

    if published:
        return "published"
    if note_status == "draft_saved_unpublished" and blk == "true":
        return "draft_saved_unpublished"
    if rtp == "true" and blk == "true":
        return "ready_to_publish_blocked"
    if rtp == "true" and blk != "true":
        return "ready_to_publish"
    if cv == "PASS":
        return "codex_pass"
    if cv == "WARN":
        return "codex_warn"
    if cv == "BLOCK":
        return "codex_block"
    if draft_ok:
        return "draft_ready"
    return "no_draft"


# ---------------------------------------------------------------------------
# レコード構築
# ---------------------------------------------------------------------------

def build_record(
    article_id:  str,
    file_id:     str,
    release:     str,
    reg_row:     dict,
    ndr_rows:    list,
    is_priority: bool = False,
    db_row:      dict = None,
) -> dict:
    # Published state from source_registry
    published = (reg_row.get("status", "") == "published") if reg_row else False
    pub_url   = reg_row.get("note_url", "") if reg_row else ""

    # Note draft existence + title
    draft_exists, title = find_note_draft(file_id)

    # Codex 監査情報
    codex_verdict, codex_iter, codex_new_fmt = get_codex_info(file_id)

    # Review package
    pkg_state = get_review_package_state(article_id)
    has_pkg   = pkg_state.get("exists", False)

    # note_draft_registry: article_id または slug のキーで検索
    ndr = {}
    for row in ndr_rows:
        if row.get("article_id") == article_id or file_id in row.get("slug", ""):
            ndr = row
            break

    note_status = ndr.get("note_status", "")

    if db_row:
        # ── workflow.db v1.2 由来（優先） ──
        ready_to_pub   = "true" if db_row.get("ready_to_publish") == 1 else "false"
        pub_blocked    = "true" if db_row.get("publish_blocked")  == 1 else "false"
        block_reason   = (db_row.get("publish_block_reason") or "").strip()
        note_draft_url = (db_row.get("note_draft_url") or "").strip()
        publish_order  = db_row.get("publish_order")
        series_number  = db_row.get("series_number")
        release_id_val = db_row.get("release_id")
        data_source    = "DB"
        conflicts      = check_db_ndr_conflicts(db_row, ndr) if ndr else []
    else:
        # ── review_package + NDR 由来（フォールバック） ──
        ready_to_pub   = pkg_state.get("ready_to_publish") or ndr.get("ready_to_publish", "false")
        pub_blocked    = pkg_state.get("publish_blocked")  or ndr.get("publish_blocked",  "false")
        block_reason   = pkg_state.get("publish_block_reason") or ndr.get("publish_block_reason", "")
        note_draft_url = ndr.get("note_draft_url", "")
        publish_order  = None
        series_number  = None
        release_id_val = None
        data_source    = "CSV"
        conflicts      = []

    rec = {
        "article_id":           article_id,
        "file_id":              file_id,
        "release":              release,
        "title":                title,
        "published":            published,
        "note_url":             pub_url or note_draft_url,
        "draft_exists":         draft_exists,
        "codex_verdict":        codex_verdict or "",
        "codex_iter":           codex_iter,
        "codex_new_fmt":        codex_new_fmt,
        "has_review_package":   has_pkg,
        "ready_to_publish":     ready_to_pub,
        "publish_blocked":      pub_blocked,
        "publish_block_reason": block_reason,
        "note_status":          note_status,
        "is_priority":          is_priority,
        "publish_order":        publish_order,
        "series_number":        series_number,
        "release_id":           release_id_val,
        "data_source":          data_source,
        "conflicts":            conflicts,
    }
    rec["status"] = determine_status(rec)
    return rec


# ---------------------------------------------------------------------------
# データ収集
# ---------------------------------------------------------------------------

def collect_records() -> tuple:
    """(registered_r02, priority_r02, r03, all_conflicts) のタプルを返す。"""
    reg_data = load_source_registry()
    ndr_rows = load_note_draft_registry()
    db_rows  = load_workflow_db()

    # DB 行を file_id でインデックス化
    db_by_file_id = {}
    for row in db_rows:
        fid = (
            extract_file_id(row.get("slug", ""))
            or extract_file_id(row.get("draft_path", ""))
        )
        if fid:
            db_by_file_id[fid] = row

    registered_r02 = []
    priority_r02   = []
    r03            = []
    all_conflicts  = []

    # ── R02 登録済み ──
    for aid in sorted(r for r in reg_data if r.startswith("#R02")):
        row = reg_data[aid]
        draft_path = row.get("draft_path", "")
        pdf_name   = row.get("pdf_file_name", "")
        file_id    = extract_file_id(draft_path) or extract_file_id(pdf_name)
        if not file_id:
            continue
        db_r = db_by_file_id.get(file_id)
        rec  = build_record(aid, file_id, "R02", row, ndr_rows, db_row=db_r)
        if rec["conflicts"]:
            all_conflicts.extend([f"[{file_id}] {c}" for c in rec["conflicts"]])
        registered_r02.append(rec)

    # ── R02 優先未登録（#R02-004〜007 相当） ──
    for slug_key in R02_PRIORITY_SLUGS:
        db_r = db_by_file_id.get(slug_key)
        rec  = build_record("#R02-???", slug_key, "R02", {}, ndr_rows,
                            is_priority=True, db_row=db_r)
        if rec["conflicts"]:
            all_conflicts.extend([f"[{slug_key}] {c}" for c in rec["conflicts"]])
        priority_r02.append(rec)

    # ── R03: workflow.db 由来を優先 ──
    r03_file_ids_added = set()
    for db_r in db_rows:
        if (db_r.get("release_id") or 0) != 3:
            continue
        fid = (
            extract_file_id(db_r.get("slug", ""))
            or extract_file_id(db_r.get("draft_path", ""))
        )
        if not fid:
            continue
        # article_id は NDR から取得（なければ "#R03-???"）
        ndr_match = next(
            (r for r in ndr_rows if fid in r.get("slug", "")), {}
        )
        aid = ndr_match.get("article_id", "#R03-???")
        rec = build_record(aid, fid, "R03", reg_data.get(aid, {}),
                           ndr_rows, db_row=db_r)
        if rec["conflicts"]:
            all_conflicts.extend([f"[{fid}] {c}" for c in rec["conflicts"]])
        r03.append(rec)
        r03_file_ids_added.add(fid)

    # R03: NDR のみに存在する記事（DB 未登録）
    for row in ndr_rows:
        aid = row.get("article_id", "")
        if not aid.startswith("#R03"):
            continue
        slug    = row.get("slug", "")
        file_id = extract_file_id(slug) or slug
        if file_id in r03_file_ids_added:
            continue
        rec = build_record(aid, file_id, "R03", reg_data.get(aid, {}), ndr_rows)
        r03.append(rec)
        r03_file_ids_added.add(file_id)

    # publish_order 昇順ソート（None は末尾）
    r03.sort(key=lambda r: (r["publish_order"] is None, r["publish_order"] or 0))
    registered_r02.sort(
        key=lambda r: (r["publish_order"] is None, r["publish_order"] or 0)
    )

    return registered_r02, priority_r02, r03, all_conflicts


# ---------------------------------------------------------------------------
# 表示ヘルパー
# ---------------------------------------------------------------------------

def fmt_codex(rec: dict) -> str:
    if not rec["codex_verdict"]:
        return "Codex: 未実施"
    old_note = "" if rec.get("codex_new_fmt") else " ※旧フォーマット"
    return f"Codex iter{rec['codex_iter']}: {rec['codex_verdict']}{old_note}"


def fmt_source(rec: dict) -> str:
    return "🗄️ DB" if rec.get("data_source") == "DB" else "📄 CSV"


def fmt_publish_order(rec: dict) -> str:
    po = rec.get("publish_order")
    sn = rec.get("series_number")
    if po is not None:
        return f"publish_order={po}  series={sn}"
    return ""


# ---------------------------------------------------------------------------
# ターミナル表示
# ---------------------------------------------------------------------------

def render_terminal(
    registered: list,
    priority:   list,
    r03:        list,
    conflicts:  list,
) -> None:
    now_str = datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")
    db_ok   = DB_PATH.exists()
    W    = 80
    line = "─" * W
    dline = "=" * W

    print(dline)
    print(f" Article Factory 在庫レポート  {now_str}")
    db_status = f"🗄️ workflow.db v1.2 参照中" if db_ok else "📄 CSV のみ（DB なし）"
    print(f" v{VERSION} — 読み取り専用 / {db_status}")
    print(dline)

    # ── Priority: R02 未登録 ──
    print()
    print(f"[PRIORITY] ⚠  Release 02 未公開 PDF 記事（source_registry 未登録）  {len(priority)} 件")
    print(line)
    for rec in priority:
        label  = STATUS_LABEL.get(rec["status"], rec["status"])
        action = NEXT_ACTION.get(rec["status"], "")
        print(f"  {rec['file_id']:<22}  {label}  {fmt_source(rec)}")
        print(f"    {fmt_codex(rec)}")
        print(f"    → next: {action}")
    if not priority:
        print("  （なし）")

    # ── Release 03 ──
    print()
    r03_pub = sum(1 for r in r03 if r["published"])
    print(f"[Release 03]  {r03_pub}/{len(r03)} 件公開済み")
    print(line)
    for rec in r03:
        label  = STATUS_LABEL.get(rec["status"], rec["status"])
        action = NEXT_ACTION.get(rec["status"], "")
        po_str = fmt_publish_order(rec)
        print(f"  {rec['file_id']:<22}  {rec['article_id']}  {label}  {fmt_source(rec)}")
        if po_str:
            print(f"    {po_str}")
        print(f"    {fmt_codex(rec)}")
        if rec["publish_block_reason"]:
            print(f"    block: {rec['publish_block_reason']}")
        if rec["note_url"]:
            print(f"    note:  {rec['note_url']}")
        if rec["conflicts"]:
            for c in rec["conflicts"]:
                print(f"    ⚠️  CONFLICT: {c}")
        print(f"    → next: {action}")
    if not r03:
        print("  （なし）")

    # ── Release 02 登録済み ──
    pub   = sum(1 for r in registered if r["published"])
    total = len(registered)
    print()
    print(f"[Release 02 登録済み]  {pub}/{total} 件公開済み")
    print(line)
    for rec in registered:
        label = STATUS_LABEL.get(rec["status"], rec["status"])
        print(f"  {rec['file_id']:<22}  {rec['article_id']}  {label}")
        if not rec["published"]:
            print(f"    → next: {NEXT_ACTION.get(rec['status'], '')}")

    # ── CONFLICT 一覧 ──
    if conflicts:
        print()
        print(f"[CONFLICT] ⚠️  DB と CSV で値が食い違う項目  {len(conflicts)} 件")
        print(line)
        for c in conflicts:
            print(f"  {c}")

    # ── サマリー ──
    print()
    print(line)
    print(f"  Release 02 登録済み: {pub}/{total} 件公開  /  優先未登録: {len(priority)} 件")
    print(f"  Release 03: {r03_pub}/{len(r03)} 件公開")
    if conflicts:
        print(f"  ⚠️  CONFLICT: {len(conflicts)} 件（要確認）")
    if priority:
        print(f"  次の優先アクション:")
        for rec in priority:
            action = NEXT_ACTION.get(rec["status"], "")
            print(f"    {rec['file_id']}: {action}")
    print(dline)


# ---------------------------------------------------------------------------
# Markdown 出力
# ---------------------------------------------------------------------------

def render_markdown(
    registered: list,
    priority:   list,
    r03:        list,
    conflicts:  list,
) -> str:
    now_str  = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")
    date_str = datetime.now(JST).strftime("%Y%m%d")
    pub_r02  = sum(1 for r in registered if r["published"])
    pub_r03  = sum(1 for r in r03 if r["published"])
    db_ok    = DB_PATH.exists()

    lines = [
        f"# Article Factory 在庫レポート {date_str}",
        "",
        f"- **生成日時**: {now_str}",
        f"- **バージョン**: v{VERSION}",
        f"- **DB**: {'workflow.db v1.2 参照' if db_ok else 'なし（CSV のみ）'}",
        f"- **CONFLICT**: {len(conflicts)} 件",
        "",
        "---",
        "",
        "## サマリー",
        "",
        "| Release | 公開済み / 総件数 | 備考 |",
        "| ------- | ----------------- | ---- |",
        f"| Release 02 登録済み | {pub_r02} / {len(registered)} | 残り {len(registered)-pub_r02} 件 |",
        f"| Release 02 優先未登録 | 0 / {len(priority)} | source_registry 未登録・要対応 |",
        f"| Release 03 | {pub_r03} / {len(r03)} | 下書き保存済み（公開ブロック中）|",
        "",
        "---",
        "",
        "## [PRIORITY] Release 02 未公開 PDF 記事（source_registry 未登録）",
        "",
        "| file_id | status | codex | source | next_action |",
        "| ------- | ------ | ----- | ------ | ----------- |",
    ]

    for rec in priority:
        label  = STATUS_LABEL.get(rec["status"], rec["status"])
        action = NEXT_ACTION.get(rec["status"], "")
        lines.append(
            f"| {rec['file_id']} | {label} | {fmt_codex(rec)} | {fmt_source(rec)} | {action} |"
        )
    if not priority:
        lines.append("| （なし） | | | | |")

    lines += [
        "",
        "## Release 03",
        "",
        "| article_id | file_id | publish_order | status | codex | publish_blocked | source | next_action |",
        "| ---------- | ------- | ------------- | ------ | ----- | --------------- | ------ | ----------- |",
    ]

    for rec in r03:
        label      = STATUS_LABEL.get(rec["status"], rec["status"])
        action     = NEXT_ACTION.get(rec["status"], "")
        blk_col    = "true" if rec["publish_blocked"] == "true" else "false"
        po_col     = str(rec["publish_order"]) if rec["publish_order"] is not None else "—"
        conflict_mark = " ⚠️" if rec["conflicts"] else ""
        lines.append(
            f"| {rec['article_id']} | {rec['file_id']} | {po_col} | {label}{conflict_mark}"
            f" | {fmt_codex(rec)} | {blk_col} | {fmt_source(rec)} | {action} |"
        )
    if not r03:
        lines.append("| （なし） | | | | | | | |")

    lines += [
        "",
        f"## Release 02 登録済み（{pub_r02}/{len(registered)} 件公開済み）",
        "",
        "| article_id | file_id | publish_order | status | codex | note_url |",
        "| ---------- | ------- | ------------- | ------ | ----- | -------- |",
    ]

    for rec in registered:
        label  = STATUS_LABEL.get(rec["status"], rec["status"])
        url    = rec["note_url"] or "—"
        po_col = str(rec["publish_order"]) if rec["publish_order"] is not None else "—"
        lines.append(
            f"| {rec['article_id']} | {rec['file_id']} | {po_col}"
            f" | {label} | {fmt_codex(rec)} | {url} |"
        )

    if conflicts:
        lines += [
            "",
            "## CONFLICT 一覧",
            "",
            "| 記事 | 差異 |",
            "| ---- | ---- |",
        ]
        for c in conflicts:
            parts = c.split("] ", 1)
            key   = parts[0].lstrip("[") if len(parts) == 2 else c
            diff  = parts[1] if len(parts) == 2 else ""
            lines.append(f"| {key} | {diff} |")

    lines += [""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# エントリポイント
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Article Factory 在庫可視化レポート v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="ファイル出力せずターミナルのみ表示",
    )
    parser.add_argument(
        "--output", metavar="PATH",
        help="Markdown 出力先（デフォルト: review_reports/article_inventory_YYYYMMDD.md）",
    )
    args = parser.parse_args()

    registered, priority, r03, conflicts = collect_records()

    render_terminal(registered, priority, r03, conflicts)

    date_str = datetime.now(JST).strftime("%Y%m%d")
    out_path = Path(args.output) if args.output else REPORTS_DIR / f"article_inventory_{date_str}.md"

    if args.dry_run:
        print(f"\n[dry-run] Markdown 出力スキップ: {out_path}")
    else:
        md_content = render_markdown(registered, priority, r03, conflicts)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md_content, encoding="utf-8")
        print(f"\nMarkdown 出力: {out_path}")


if __name__ == "__main__":
    main()
