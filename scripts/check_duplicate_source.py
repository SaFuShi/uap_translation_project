#!/usr/bin/env python3
"""
check_duplicate_source.py
同一PDFの二重記事化を防ぐための重複チェックスクリプト。

使用方法:
  python3 scripts/check_duplicate_source.py <pdf_file_name> [--sha256 <hash>] [--next-id <#037>]

例:
  python3 scripts/check_duplicate_source.py dow-uap-d12-mission-report-iraq-may-2022.pdf
  python3 scripts/check_duplicate_source.py --sha256 9127fb5a81efacf030df4dc6290d02bcdf4c8512cf1809b6eccfe6cf16a77f31
  python3 scripts/check_duplicate_source.py dow-uap-d12-mission-report-iraq-may-2022.pdf --next-id "#037"

終了コード:
  0 = PASS (重複なし)
  1 = BLOCK (重複あり)
  2 = エラー
"""

import sys
import csv
import hashlib
import argparse
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent.parent / "review_logs" / "source_registry.csv"
RAW_PDF_DIR = Path(__file__).parent.parent / "raw_pdf"

BLOCK_STATUSES = {"draft", "reviewing", "published", "hold", "archived"}


def load_registry():
    """source_registry.csv を読み込む。"""
    if not REGISTRY_PATH.exists():
        print(f"[ERROR] Registry not found: {REGISTRY_PATH}", file=sys.stderr)
        sys.exit(2)

    registry = []
    with open(REGISTRY_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            registry.append(row)
    return registry


def compute_sha256(pdf_path: Path) -> str:
    """PDFファイルのSHA256を計算する。"""
    h = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_duplicate(pdf_file_name: str = None, sha256: str = None, next_id: str = None):
    """重複チェックを実行する。"""
    registry = load_registry()
    matches = []

    for row in registry:
        matched = False
        match_reason = []

        # ファイル名チェック
        if pdf_file_name and row["pdf_file_name"].strip() == pdf_file_name.strip():
            matched = True
            match_reason.append("pdf_file_name")

        # SHA256チェック
        if sha256 and row["pdf_sha256"].strip() == sha256.strip():
            matched = True
            match_reason.append("pdf_sha256")

        if matched:
            matches.append((row, match_reason))

    if not matches:
        print("=" * 60)
        print("RESULT: PASS")
        print("=" * 60)
        if pdf_file_name:
            print(f"  pdf_file_name : {pdf_file_name}")
        if sha256:
            print(f"  sha256        : {sha256[:16]}...")
        if next_id:
            print(f"  next_id       : {next_id}")
        print()
        print("  duplicate_check : PASS")
        print("  registry_status : new")
        print()
        print("→ 新規ドラフト生成可。")
        return 0

    else:
        print("=" * 60)
        print("RESULT: BLOCK — 重複ソース検出")
        print("=" * 60)
        if next_id:
            print(f"  requested_article_id : {next_id}")
        if pdf_file_name:
            print(f"  pdf_file_name        : {pdf_file_name}")
        if sha256:
            print(f"  sha256               : {sha256[:16]}...")
        print()
        for row, reasons in matches:
            print(f"  既存エントリ:")
            print(f"    article_id    : {row['article_id']}")
            print(f"    status        : {row['status']}")
            print(f"    note_url      : {row['note_url'] or '(なし)'}")
            print(f"    draft_path    : {row['draft_path']}")
            print(f"    match_reason  : {', '.join(reasons)}")
            if row.get('remarks'):
                print(f"    remarks       : {row['remarks'][:80]}")
            print()
        print("  duplicate_check : BLOCK")
        print("  registry_status : existing")
        print()
        print("→ 人間の明示確認なしに新規ドラフトを生成しないでください。")
        return 1


def check_from_raw_pdf(pdf_file_name: str, next_id: str = None):
    """raw_pdf/ のファイルからSHA256を計算して重複チェックする。"""
    pdf_path = RAW_PDF_DIR / pdf_file_name
    sha256 = None

    if pdf_path.exists():
        sha256 = compute_sha256(pdf_path)
        print(f"[INFO] SHA256 computed: {sha256[:16]}...")
    else:
        print(f"[WARN] PDF not found in raw_pdf/: {pdf_file_name}")

    return check_duplicate(pdf_file_name=pdf_file_name, sha256=sha256, next_id=next_id)


def batch_check(pdf_list: list, start_id_num: int = 37):
    """複数PDFを一括チェックして候補一覧を表示する。"""
    registry = load_registry()
    registered_files = {row["pdf_file_name"].strip() for row in registry}
    registered_sha256 = {row["pdf_sha256"].strip() for row in registry if row["pdf_sha256"]}

    print("=" * 80)
    print("BATCH DUPLICATE CHECK — 候補一覧")
    print("=" * 80)
    print(f"{'候補ID':<10} {'duplicate_check':<18} {'registry_status':<18} {'pdf_file_name'}")
    print("-" * 80)

    current_id = start_id_num
    for pdf_file_name in pdf_list:
        article_id = f"#{current_id}"
        pdf_path = RAW_PDF_DIR / pdf_file_name
        sha256 = None
        if pdf_path.exists():
            sha256 = compute_sha256(pdf_path)

        is_dup_name = pdf_file_name in registered_files
        is_dup_sha = sha256 and sha256 in registered_sha256

        if is_dup_name or is_dup_sha:
            print(f"{article_id:<10} {'BLOCK':<18} {'existing':<18} {pdf_file_name}")
        else:
            print(f"{article_id:<10} {'PASS':<18} {'new':<18} {pdf_file_name}")
            current_id += 1  # BLOCKはIDを消費しない


def main():
    parser = argparse.ArgumentParser(
        description="UAP Translation Project — 重複ソースチェッカー"
    )
    parser.add_argument("pdf_file_name", nargs="?", help="チェック対象のPDFファイル名")
    parser.add_argument("--sha256", help="PDFのSHA256ハッシュ（直接指定）")
    parser.add_argument("--next-id", help="割り当て予定のarticle_id（例: #037）")
    parser.add_argument("--batch", nargs="+", metavar="PDF", help="複数PDFを一括チェック")
    parser.add_argument("--start-id", type=int, default=37, help="バッチ開始ID番号（デフォルト: 37）")

    args = parser.parse_args()

    if args.batch:
        batch_check(args.batch, args.start_id)
        return

    if not args.pdf_file_name and not args.sha256:
        parser.print_help()
        sys.exit(2)

    if args.pdf_file_name and not args.sha256:
        sys.exit(check_from_raw_pdf(args.pdf_file_name, args.next_id))
    else:
        sys.exit(check_duplicate(
            pdf_file_name=args.pdf_file_name,
            sha256=args.sha256,
            next_id=args.next_id
        ))


if __name__ == "__main__":
    main()
