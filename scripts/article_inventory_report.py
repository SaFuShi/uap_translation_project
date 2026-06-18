#!/usr/bin/env python3
"""
article_inventory_report.py — Article Factory 在庫可視化レポート

v0.1.0 — 読み取り専用 / workflow.db 参照なし / 標準ライブラリのみ
"""

import argparse
import csv
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

VERSION = "0.1.0"
JST = timezone(timedelta(hours=9))

BASE          = Path(".")
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
    article_id: str,
    file_id:    str,
    release:    str,
    reg_row:    dict,
    ndr_rows:   list,
    is_priority: bool = False,
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

    note_status    = ndr.get("note_status", "")
    note_draft_url = ndr.get("note_draft_url", "")
    # review_package の値を優先し、なければ note_draft_registry を参照
    ready_to_pub = pkg_state.get("ready_to_publish") or ndr.get("ready_to_publish", "false")
    pub_blocked  = pkg_state.get("publish_blocked")  or ndr.get("publish_blocked",  "false")
    block_reason = pkg_state.get("publish_block_reason") or ndr.get("publish_block_reason", "")

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
    }
    rec["status"] = determine_status(rec)
    return rec


# ---------------------------------------------------------------------------
# データ収集
# ---------------------------------------------------------------------------

def collect_records() -> tuple:
    """(registered_r02, priority_r02, r03) のタプルを返す。"""
    reg_data = load_source_registry()
    ndr_rows = load_note_draft_registry()

    registered_r02 = []
    priority_r02   = []
    r03            = []

    # R02 登録済み
    for aid in sorted(r for r in reg_data if r.startswith("#R02")):
        row = reg_data[aid]
        draft_path = row.get("draft_path", "")
        pdf_name   = row.get("pdf_file_name", "")
        file_id    = extract_file_id(draft_path) or extract_file_id(pdf_name)
        if not file_id:
            continue
        rec = build_record(aid, file_id, "R02", row, ndr_rows)
        registered_r02.append(rec)

    # R02 優先未登録（#R02-004〜007 相当）
    for slug_key in R02_PRIORITY_SLUGS:
        rec = build_record("#R02-???", slug_key, "R02", {}, ndr_rows, is_priority=True)
        priority_r02.append(rec)

    # R03（note_draft_registry から検出）
    for row in ndr_rows:
        aid = row.get("article_id", "")
        if not aid.startswith("#R03"):
            continue
        slug    = row.get("slug", "")
        file_id = extract_file_id(slug) or slug
        reg_row = reg_data.get(aid, {})
        rec = build_record(aid, file_id, "R03", reg_row, ndr_rows)
        r03.append(rec)

    return registered_r02, priority_r02, r03


# ---------------------------------------------------------------------------
# 表示ヘルパー
# ---------------------------------------------------------------------------

def fmt_codex(rec: dict) -> str:
    if not rec["codex_verdict"]:
        return "Codex: 未実施"
    old_note = "" if rec.get("codex_new_fmt") else " ※旧フォーマット"
    return f"Codex iter{rec['codex_iter']}: {rec['codex_verdict']}{old_note}"


# ---------------------------------------------------------------------------
# ターミナル表示
# ---------------------------------------------------------------------------

def render_terminal(registered: list, priority: list, r03: list) -> None:
    now_str = datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")
    W    = 80
    line = "─" * W
    dline = "=" * W

    print(dline)
    print(f" Article Factory 在庫レポート  {now_str}")
    print(f" v{VERSION} — 読み取り専用 / workflow.db 参照なし")
    print(dline)

    # ── Priority: R02 未登録 ──
    print()
    print(f"[PRIORITY] ⚠  Release 02 未公開 PDF 記事（source_registry 未登録）  {len(priority)} 件")
    print(line)
    for rec in priority:
        label  = STATUS_LABEL.get(rec["status"], rec["status"])
        action = NEXT_ACTION.get(rec["status"], "")
        print(f"  {rec['file_id']:<22}  {label}")
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
        print(f"  {rec['file_id']:<22}  {rec['article_id']}  {label}")
        print(f"    {fmt_codex(rec)}")
        if rec["publish_block_reason"]:
            print(f"    block: {rec['publish_block_reason']}")
        if rec["note_url"]:
            print(f"    note:  {rec['note_url']}")
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

    # ── サマリー ──
    print()
    print(line)
    print(f"  Release 02 登録済み: {pub}/{total} 件公開  /  優先未登録: {len(priority)} 件")
    print(f"  Release 03: {r03_pub}/{len(r03)} 件公開")
    if priority:
        print(f"  次の優先アクション:")
        for rec in priority:
            action = NEXT_ACTION.get(rec["status"], "")
            print(f"    {rec['file_id']}: {action}")
    print(dline)


# ---------------------------------------------------------------------------
# Markdown 出力
# ---------------------------------------------------------------------------

def render_markdown(registered: list, priority: list, r03: list) -> str:
    now_str  = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S JST")
    date_str = datetime.now(JST).strftime("%Y%m%d")
    pub_r02  = sum(1 for r in registered if r["published"])
    pub_r03  = sum(1 for r in r03 if r["published"])

    lines = [
        f"# Article Factory 在庫レポート {date_str}",
        "",
        f"- **生成日時**: {now_str}",
        f"- **バージョン**: v{VERSION}",
        f"- **備考**: 読み取り専用 — workflow.db 参照なし",
        "",
        "---",
        "",
        "## サマリー",
        "",
        f"| Release | 公開済み / 総件数 | 備考 |",
        f"| ------- | ----------------- | ---- |",
        f"| Release 02 登録済み | {pub_r02} / {len(registered)} | 残り {len(registered)-pub_r02} 件 |",
        f"| Release 02 優先未登録 | 0 / {len(priority)} | source_registry 未登録・要対応 |",
        f"| Release 03 | {pub_r03} / {len(r03)} | 下書き保存済み（公開ブロック中）|",
        "",
        "---",
        "",
        "## [PRIORITY] Release 02 未公開 PDF 記事（source_registry 未登録）",
        "",
        "| file_id | status | codex | next_action |",
        "| ------- | ------ | ----- | ----------- |",
    ]

    for rec in priority:
        label  = STATUS_LABEL.get(rec["status"], rec["status"])
        action = NEXT_ACTION.get(rec["status"], "")
        lines.append(f"| {rec['file_id']} | {label} | {fmt_codex(rec)} | {action} |")

    if not priority:
        lines.append("| （なし） | | | |")

    lines += [
        "",
        "## Release 03",
        "",
        "| article_id | file_id | status | codex | publish_blocked | next_action |",
        "| ---------- | ------- | ------ | ----- | --------------- | ----------- |",
    ]

    for rec in r03:
        label      = STATUS_LABEL.get(rec["status"], rec["status"])
        action     = NEXT_ACTION.get(rec["status"], "")
        blk_reason = rec["publish_block_reason"]
        blk_col    = f"true — {blk_reason}" if rec["publish_blocked"] == "true" else "false"
        lines.append(
            f"| {rec['article_id']} | {rec['file_id']} | {label} | {fmt_codex(rec)} | {blk_col} | {action} |"
        )
    if not r03:
        lines.append("| （なし） | | | | | |")

    lines += [
        "",
        f"## Release 02 登録済み（{pub_r02}/{len(registered)} 件公開済み）",
        "",
        "| article_id | file_id | status | codex | note_url |",
        "| ---------- | ------- | ------ | ----- | -------- |",
    ]

    for rec in registered:
        label = STATUS_LABEL.get(rec["status"], rec["status"])
        url   = rec["note_url"] or "—"
        lines.append(
            f"| {rec['article_id']} | {rec['file_id']} | {label} | {fmt_codex(rec)} | {url} |"
        )

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

    registered, priority, r03 = collect_records()

    render_terminal(registered, priority, r03)

    date_str = datetime.now(JST).strftime("%Y%m%d")
    out_path = Path(args.output) if args.output else REPORTS_DIR / f"article_inventory_{date_str}.md"

    if args.dry_run:
        print(f"\n[dry-run] Markdown 出力スキップ: {out_path}")
    else:
        md_content = render_markdown(registered, priority, r03)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md_content, encoding="utf-8")
        print(f"\nMarkdown 出力: {out_path}")


if __name__ == "__main__":
    main()
