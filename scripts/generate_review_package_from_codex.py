#!/usr/bin/env python3
"""
generate_review_package_from_codex.py — Codex PASS 後 Review Package 自動生成

v0.2.0

使い方:
  # 単体モード: 指定した Codex audit ファイルから生成
  python3 scripts/generate_review_package_from_codex.py --codex-report <path>

  # スキャンモード: review_reports/ を全スキャンして PASS を一括処理
  python3 scripts/generate_review_package_from_codex.py --scan

共通オプション:
  --dry-run        推定結果と実行予定コマンドを表示するだけ（ファイル変更なし）
  --force          既存 Review Package を上書き
  --open-finder    生成後に macOS Finder で表示
  --update-db      生成後に workflow.db の ready_to_publish = 1 に更新（要確認）
"""

import argparse
import csv
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

VERSION       = "0.2.0"
BASE          = Path(".")
REPORTS_DIR   = BASE / "review_reports"
PACKAGES_DIR  = BASE / "review_packages"
DRAFTS_DIR    = BASE / "note_drafts"
PUBLISHED_DIR = BASE / "published_articles"
REG_CSV       = BASE / "review_logs" / "source_registry.csv"
DB_PATH       = BASE / "workflow.db"
GENERATOR     = BASE / "scripts" / "review_package_generator.py"

# S_CLASS ガード: スラッグ文字列に含まれている場合は外部送信しない
_S_CLASS_RE = re.compile(r"S[_-]?CLASS", re.IGNORECASE)


# ─────────────────────────────────────────────────────────────
# Codex ファイル検索
# ─────────────────────────────────────────────────────────────

def find_pass_files(reports_dir: Path) -> tuple:
    """
    review_reports/ から Codex PASS ファイルを抽出する。

    Returns:
      pass_files  : 新フォーマット + VERDICT: PASS + 最大 iter のリスト
      old_fmt     : 旧フォーマット（判定不可）の iter 付きファイルリスト
      non_pass    : 新フォーマットだが PASS でないファイルのリスト
    """
    # slug_key → (iter_num, Path)
    pass_by_slug: dict = {}
    old_fmt: list = []
    non_pass: list = []

    for f in sorted(reports_dir.glob("codex_audit_*.md")):
        iter_m = re.search(r"_iter(\d+)", f.name)
        if not iter_m:
            continue
        iter_num = int(iter_m.group(1))

        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        if "---CODEX_AUDIT_START---" not in content:
            old_fmt.append(f)
            continue

        verdict = None
        for line in content.splitlines():
            if line.startswith("VERDICT:"):
                verdict = line.split(":", 1)[1].strip()
                break

        if verdict != "PASS":
            non_pass.append(f)
            continue

        slug_key = re.sub(r"^codex_audit_\d{8}_", "", f.stem)
        slug_key = re.sub(r"_iter\d+$", "", slug_key)

        if slug_key not in pass_by_slug or iter_num > pass_by_slug[slug_key][0]:
            pass_by_slug[slug_key] = (iter_num, f)

    return [v[1] for v in pass_by_slug.values()], old_fmt, non_pass


# ─────────────────────────────────────────────────────────────
# 引数推定
# ─────────────────────────────────────────────────────────────

def _infer_article_id_from_registry(file_id: str) -> str | None:
    """source_registry.csv の draft_path / pdf_file_name から article_id を推定する。"""
    if not REG_CSV.exists():
        return None
    try:
        with open(REG_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                aid = (row.get("article_id") or "").strip()
                if not re.match(r"#R\d+", aid):
                    continue
                if file_id in row.get("draft_path", "") or file_id in row.get("pdf_file_name", ""):
                    return aid.lstrip("#")  # "R02-001" 形式
    except OSError:
        pass
    return None


def infer_args(codex_path: Path) -> dict:
    """
    Codex audit ファイルパスから review_package_generator.py の引数を推定する。

    Returns dict with keys:
      file_id, slug, draft, codex_report, rule_report,
      article_id, publish_blocked, block_reason, errors, warnings
    """
    errors: list = []
    warnings: list = []

    # ── slug / file_id 抽出 ──
    slug_part = re.sub(r"^codex_audit_\d{8}_", "", codex_path.stem)
    slug_part = re.sub(r"_iter\d+$", "", slug_part)

    file_id_m = re.search(r"([A-Z]+-UAP-(?:PR\d+|D\d+))", slug_part)
    file_id = file_id_m.group(1) if file_id_m else None
    if not file_id:
        errors.append(f"file_id を推定できません（スラッグ: {slug_part}）")
        return {"errors": errors, "warnings": warnings}

    # S_CLASS ガード
    if _S_CLASS_RE.search(slug_part):
        errors.append(f"S_CLASS 検出 — 外部送信禁止: {slug_part}")
        return {"errors": errors, "warnings": warnings}

    # ── draft path ──
    draft_candidates = list(DRAFTS_DIR.glob(f"ai_summary_{file_id}*_note_version.md"))
    if len(draft_candidates) == 0:
        errors.append(f"draft が見つかりません（{DRAFTS_DIR}/ai_summary_{file_id}*）")
        draft = None
    elif len(draft_candidates) == 1:
        draft = draft_candidates[0]
    else:
        # 複数ヒット: 最長ファイル名（最も具体的）を採用
        draft = max(draft_candidates, key=lambda p: len(p.name))
        warnings.append(f"draft が複数ヒット → {draft.name} を採用")

    # ── rule report ──
    rule_candidates = list(REPORTS_DIR.glob(f"rule_candidates_*{file_id}*.md"))
    rule = rule_candidates[0] if rule_candidates else None
    if not rule:
        warnings.append("rule_report が見つかりません（省略）")

    # ── article_id / publish_blocked から workflow.db ──
    article_id    = None
    publish_blocked = False
    block_reason  = ""

    if DB_PATH.exists():
        try:
            con = sqlite3.connect(str(DB_PATH))
            row = con.execute(
                """
                SELECT slug, release_id, series_number,
                       publish_blocked, publish_block_reason
                FROM articles
                WHERE slug LIKE ?
                """,
                (f"%{file_id}%",),
            ).fetchone()
            con.close()
            if row and row[1] is not None and row[2] is not None:
                article_id = f"R0{row[1]}-{row[2]:03d}"
                publish_blocked = bool(row[3])
                block_reason    = (row[4] or "").strip()
            elif row:
                warnings.append(
                    "workflow.db に記事はあるが release_id / series_number が NULL "
                    "→ source_registry.csv で補完を試みます"
                )
        except sqlite3.Error as e:
            warnings.append(f"workflow.db 読み取りエラー: {e}")

    # fallback: source_registry.csv
    if not article_id:
        article_id = _infer_article_id_from_registry(file_id)
        if article_id:
            warnings.append(f"article_id を source_registry.csv から補完: #{article_id}")
        else:
            errors.append(
                "article_id を推定できません（workflow.db / source_registry.csv に未登録）"
            )

    return {
        "file_id":         file_id,
        "slug":            slug_part,
        "draft":           draft,
        "codex_report":    codex_path,
        "rule_report":     rule,
        "article_id":      article_id,
        "publish_blocked": publish_blocked,
        "block_reason":    block_reason,
        "errors":          errors,
        "warnings":        warnings,
    }


# ─────────────────────────────────────────────────────────────
# 公開済み確認
# ─────────────────────────────────────────────────────────────

def is_published(file_id: str) -> tuple:
    """
    公開済みかどうかを確認する。

    判定順序:
      1. published_articles/ に *{file_id}*_published_*.md が存在
      2. workflow.db の articles.status = 'published'

    Returns: (bool, source_description)
    """
    # 1. published_articles/ ディレクトリ（最優先・最も信頼できる）
    if PUBLISHED_DIR.exists():
        hits = list(PUBLISHED_DIR.glob(f"*{file_id}*_published_*.md"))
        if hits:
            return True, f"published_articles/{hits[0].name}"

    # 2. workflow.db
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


# ─────────────────────────────────────────────────────────────
# Review Package 存在確認
# ─────────────────────────────────────────────────────────────

def find_existing_package(article_id: str, file_id: str) -> Path | None:
    """既存の Review Package ファイルを返す。なければ None。"""
    if not PACKAGES_DIR.exists():
        return None
    for f in PACKAGES_DIR.glob(f"#{article_id}_*.md"):
        return f
    for f in PACKAGES_DIR.glob(f"*{file_id}*.md"):
        return f
    return None


# ─────────────────────────────────────────────────────────────
# Review Package 生成
# ─────────────────────────────────────────────────────────────

def build_generator_cmd(inferred: dict, open_finder: bool, dry_run: bool) -> list:
    """review_package_generator.py へのコマンドリストを構築する。"""
    cmd = [
        sys.executable,
        str(GENERATOR),
        "--article-id",    inferred["article_id"],
        "--slug",          inferred["slug"],
        "--draft",         str(inferred["draft"]),
        "--codex-report",  str(inferred["codex_report"]),
        "--ready-to-publish",
    ]
    if inferred.get("rule_report"):
        cmd += ["--rule-report", str(inferred["rule_report"])]
    if inferred.get("publish_blocked"):
        cmd.append("--publish-blocked")
        if inferred.get("block_reason"):
            cmd += ["--publish-block-reason", inferred["block_reason"]]
    if open_finder:
        cmd.append("--open-finder")
    if dry_run:
        cmd.append("--dry-run")
    return cmd


def run_generator(cmd: list) -> bool:
    """review_package_generator.py を実行する。成功で True を返す。"""
    result = subprocess.run(cmd)
    return result.returncode == 0


# ─────────────────────────────────────────────────────────────
# workflow.db 更新
# ─────────────────────────────────────────────────────────────

def update_db_ready(file_id: str, dry_run: bool) -> str:
    """
    workflow.db の ready_to_publish = 1 に更新する。
    --update-db が指定された場合のみ呼ばれる。
    """
    if not DB_PATH.exists():
        return "SKIP（workflow.db なし）"
    if dry_run:
        return "SKIP（dry-run）"
    try:
        con = sqlite3.connect(str(DB_PATH))
        cur = con.execute(
            """
            UPDATE articles
            SET ready_to_publish = 1,
                updated_at = datetime('now', 'localtime')
            WHERE slug LIKE ?
            """,
            (f"%{file_id}%",),
        )
        con.commit()
        updated = cur.rowcount
        con.close()
        return f"✅ {updated} 件更新"
    except sqlite3.Error as e:
        return f"❌ DB エラー: {e}"


# ─────────────────────────────────────────────────────────────
# 1 ファイルの処理
# ─────────────────────────────────────────────────────────────

def process_one(
    codex_path: Path,
    dry_run:    bool,
    force:      bool,
    open_finder: bool,
    update_db:  bool,
) -> str:
    """
    1 つの Codex audit ファイルを処理する。
    Returns: "GENERATED" / "SKIPPED" / "ERROR"
    """
    W = 72
    line = "─" * W
    print(f"\n{line}")
    print(f"  対象: {codex_path.name}")

    # 引数推定
    inferred = infer_args(codex_path)

    # エラー表示
    for e in inferred.get("errors", []):
        print(f"  ❌  ERROR: {e}")
    for w in inferred.get("warnings", []):
        print(f"  ⚠️   WARN:  {w}")

    if inferred.get("errors"):
        return "ERROR"

    article_id = inferred["article_id"]
    file_id    = inferred["file_id"]

    print(f"  file_id:     {file_id}")
    print(f"  article_id:  #{article_id}")
    print(f"  slug:        {inferred['slug']}")
    print(f"  draft:       {inferred['draft']}")
    print(f"  rule_report: {inferred['rule_report'] or '（なし）'}")
    print(f"  publish_blocked: {inferred['publish_blocked']}")
    if inferred["block_reason"]:
        print(f"  block_reason: {inferred['block_reason'][:60]}")

    # 公開済みチェック（既存 pkg チェックより先に行う）
    pub, pub_source = is_published(file_id)
    if pub:
        print(f"  ⏭   SKIP: already published ({pub_source})")
        return "SKIPPED"

    # 既存 pkg チェック
    existing = find_existing_package(article_id, file_id)
    if existing and not force:
        print(f"  ⏭   SKIP: Review Package 既存 → {existing.name}")
        print(f"       上書きするには --force を指定してください")
        return "SKIPPED"

    if existing and force:
        print(f"  ♻️   FORCE: 既存 pkg を上書きします → {existing.name}")

    # コマンド構築
    cmd = build_generator_cmd(inferred, open_finder, dry_run)

    if dry_run:
        print(f"  [dry-run] 実行予定コマンド:")
        cmd_display = " \\\n      ".join(str(c) for c in cmd)
        print(f"      {cmd_display}")
        return "GENERATED(dry-run)"

    # 実行
    print(f"  🚀  review_package_generator.py を実行中...")
    ok = run_generator(cmd)
    if not ok:
        print(f"  ❌  ERROR: review_package_generator.py が失敗しました")
        return "ERROR"

    print(f"  ✅  Review Package 生成完了")

    # DB 更新（オプション）
    if update_db:
        db_result = update_db_ready(file_id, dry_run)
        print(f"  🗄️   DB 更新: {db_result}")

    return "GENERATED"


# ─────────────────────────────────────────────────────────────
# エントリポイント
# ─────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Codex PASS 後 Review Package 自動生成  v{VERSION}  (公開済み除外対応)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "例:\n"
            "  # D077 単体 dry-run\n"
            "  python3 scripts/generate_review_package_from_codex.py \\\n"
            "      --codex-report review_reports/codex_audit_..._iter2.md --dry-run\n\n"
            "  # 全スキャン dry-run\n"
            "  python3 scripts/generate_review_package_from_codex.py --scan --dry-run\n"
        ),
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--codex-report", metavar="PATH",
        help="処理する Codex audit ファイル（新フォーマット + PASS のみ受け付ける）",
    )
    mode.add_argument(
        "--scan", action="store_true",
        help="review_reports/ を全スキャンして PASS を一括処理",
    )

    parser.add_argument("--dry-run",     action="store_true", help="推定結果と実行コマンドを表示するだけ")
    parser.add_argument("--force",       action="store_true", help="既存 Review Package を上書き")
    parser.add_argument("--open-finder", action="store_true", help="生成後に macOS Finder で表示")
    parser.add_argument(
        "--update-db", action="store_true",
        help="生成後に workflow.db の ready_to_publish = 1 に更新",
    )

    args = parser.parse_args()

    # ── スキャン or 単体 ──
    if args.scan:
        if not REPORTS_DIR.exists():
            print(f"❌  review_reports/ が見つかりません: {REPORTS_DIR}")
            sys.exit(1)
        pass_files, old_fmt, non_pass = find_pass_files(REPORTS_DIR)

        W = 72
        print("=" * W)
        print(f" generate_review_package_from_codex.py  v{VERSION}  --scan")
        mode_str = "[dry-run]" if args.dry_run else "[EXECUTE]"
        print(f" {mode_str}")
        print("=" * W)

        if old_fmt:
            print(f"\n⚠️   旧フォーマット（判定不可）: {len(old_fmt)} 件 — スキップ")
            for f in old_fmt:
                print(f"    {f.name}")

        if not pass_files:
            print("\nℹ️   PASS 済みの Codex audit ファイルが見つかりませんでした。")
            sys.exit(0)

        print(f"\n PASS 対象: {len(pass_files)} 件")

        counts = {"GENERATED": 0, "GENERATED(dry-run)": 0, "SKIPPED": 0, "ERROR": 0}
        for f in pass_files:
            result = process_one(f, args.dry_run, args.force, args.open_finder, args.update_db)
            counts[result] = counts.get(result, 0) + 1

        print(f"\n{'─' * W}")
        dr = "(dry-run) " if args.dry_run else ""
        gen_key = "GENERATED(dry-run)" if args.dry_run else "GENERATED"
        print(
            f"  {dr}生成: {counts.get(gen_key, 0)}  "
            f"スキップ: {counts['SKIPPED']}  "
            f"エラー: {counts['ERROR']}"
        )
        print("=" * W)

    else:
        # 単体モード
        codex_path = Path(args.codex_report)
        if not codex_path.exists():
            print(f"❌  ファイルが見つかりません: {codex_path}")
            sys.exit(1)

        W = 72
        print("=" * W)
        print(f" generate_review_package_from_codex.py  v{VERSION}  --codex-report")
        mode_str = "[dry-run]" if args.dry_run else "[EXECUTE]"
        print(f" {mode_str}  {codex_path.name}")
        print("=" * W)

        # 新フォーマット確認
        try:
            content = codex_path.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            print(f"❌  ファイル読み取りエラー: {e}")
            sys.exit(1)

        if "---CODEX_AUDIT_START---" not in content:
            print("❌  旧フォーマットの Codex audit ファイルです（判定不可）。")
            print("   新フォーマット（---CODEX_AUDIT_START--- を含む）のファイルを指定してください。")
            sys.exit(1)

        verdict = next(
            (l.split(":", 1)[1].strip() for l in content.splitlines() if l.startswith("VERDICT:")),
            None,
        )
        if verdict != "PASS":
            print(f"❌  VERDICT が PASS ではありません（VERDICT: {verdict or '不明'}）。")
            sys.exit(1)

        if not re.search(r"_iter\d+", codex_path.name):
            print("⚠️   ファイル名に iter 番号がありません。処理を続けますが、最大 iter かどうか確認してください。")

        result = process_one(codex_path, args.dry_run, args.force, args.open_finder, args.update_db)
        print(f"\n{'─' * W}")
        print(f"  結果: {result}")
        print("=" * W)

        if result == "ERROR":
            sys.exit(1)


if __name__ == "__main__":
    main()
