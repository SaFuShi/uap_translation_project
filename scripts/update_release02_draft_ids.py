#!/usr/bin/env python3
"""
update_release02_draft_ids.py — Release 02 VIDドラフト title/footer 一括更新

目的:
  note公開前ブロッカー（73件 #TBD / #2_TBD 残存）を解消する。
  タイトル行の #TBD / #2_TBD を正式 article_id（#R02-XXX）に置換し、
  フッターを 📋 article_id 表記に更新する。

使い方:
  python3 scripts/update_release02_draft_ids.py --dry-run
  python3 scripts/update_release02_draft_ids.py --dry-run --output review_reports/release02_draft_id_update_dry_run.md
  python3 scripts/update_release02_draft_ids.py --execute    # dry-run確認後のみ

安全方針:
  - --dry-run 時はファイルを変更しない（差分表示のみ）
  - --execute 時は上書き前に .bak バックアップを作成
  - workflow.db / source_registry.csv / files_catalog.csv は変更しない
  - note_drafts/archive/ は対象外
  - git操作なし / note公開なし
  - archive/ 配下のファイルは対象外
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

VERSION = "1.0.0"
TODAY = "2026-06-23"
DRAFTS_DIR = Path("note_drafts")
ARCHIVE_DIR = DRAFTS_DIR / "archive"


# ── article_id マッピング（release02_numbering_plan.md 準拠） ─────────────────
# (glob_key, r02_num, publish_order)
#   glob_key: note_drafts/ 内の ai_summary_{glob_key}_*_note_version.md を検索
#   r02_num: 3桁ゼロ埋め番号 → R02-{r02_num:03d} / #2_{r02_num:03d}
#   publish_order: 公開順序番号

MAPPING: list[tuple[str, int, int]] = [
    # 前バッチA: DOW-UAP-PR019〜049（27件）
    ("DOW-UAP-PR019", 10, 2010),
    ("DOW-UAP-PR021", 11, 2011),
    ("DOW-UAP-PR022", 12, 2012),
    ("DOW-UAP-PR023", 13, 2013),
    ("DOW-UAP-PR026", 14, 2014),
    ("DOW-UAP-PR027", 15, 2015),
    ("DOW-UAP-PR028", 16, 2016),
    ("DOW-UAP-PR029", 17, 2017),
    ("DOW-UAP-PR031", 18, 2018),
    ("DOW-UAP-PR032", 19, 2019),
    ("DOW-UAP-PR033", 20, 2020),
    ("DOW-UAP-PR034", 21, 2021),
    ("DOW-UAP-PR035", 22, 2022),
    ("DOW-UAP-PR036", 23, 2023),
    ("DOW-UAP-PR037", 24, 2024),
    ("DOW-UAP-PR038", 25, 2025),
    ("DOW-UAP-PR039", 26, 2026),
    ("DOW-UAP-PR040", 27, 2027),
    ("DOW-UAP-PR041", 28, 2028),
    ("DOW-UAP-PR042", 29, 2029),
    ("DOW-UAP-PR043", 30, 2030),
    ("DOW-UAP-PR044", 31, 2031),
    ("DOW-UAP-PR045", 32, 2032),
    ("DOW-UAP-PR046", 33, 2033),
    ("DOW-UAP-PR047", 34, 2034),
    ("DOW-UAP-PR048", 35, 2035),
    ("DOW-UAP-PR049", 36, 2036),
    # 前バッチB: FBI-UAP-PR001〜006（6件）
    ("FBI-UAP-PR001", 37, 2037),
    ("FBI-UAP-PR002", 38, 2038),
    ("FBI-UAP-PR003", 39, 2039),
    ("FBI-UAP-PR004", 40, 2040),
    ("FBI-UAP-PR005", 41, 2041),
    ("FBI-UAP-PR006", 42, 2042),
    # 中間バッチ: PR053〜069（15件 DONE_CANDIDATE、HOLD除く）
    ("DOW-UAP-PR053", 43, 2043),
    ("DOW-UAP-PR054", 44, 2044),
    ("DOW-UAP-PR055", 45, 2045),
    ("DOW-UAP-PR056", 46, 2046),
    # PR057/057a/057b(R02-047〜049) / PR058(R02-050): HOLD → マッピング対象外
    ("DOW-UAP-PR059", 51, 2051),
    ("DOW-UAP-PR060", 52, 2052),
    ("DOW-UAP-PR061", 53, 2053),
    ("DOW-UAP-PR062", 54, 2054),
    ("DOW-UAP-PR063", 55, 2055),
    ("DOW-UAP-PR064", 56, 2056),
    ("DOW-UAP-PR065", 57, 2057),
    ("DOW-UAP-PR066", 58, 2058),
    ("DOW-UAP-PR067", 59, 2059),
    ("DOW-UAP-PR068", 60, 2060),
    ("DOW-UAP-PR069", 61, 2061),
    # 今回バッチ: PR071〜099（28件、PR098除く）
    ("DOW-UAP-PR071", 62, 2062),
    ("DOW-UAP-PR072", 63, 2063),
    ("DOW-UAP-PR073", 64, 2064),
    ("DOW-UAP-PR074", 65, 2065),
    ("DOW-UAP-PR075", 66, 2066),
    ("DOW-UAP-PR076", 67, 2067),
    ("DOW-UAP-PR077", 68, 2068),
    ("DOW-UAP-PR078", 69, 2069),
    ("DOW-UAP-PR079", 70, 2070),
    ("DOW-UAP-PR080", 71, 2071),
    ("DOW-UAP-PR081", 72, 2072),
    ("DOW-UAP-PR082", 73, 2073),
    ("DOW-UAP-PR083", 74, 2074),
    ("DOW-UAP-PR084", 75, 2075),
    ("DOW-UAP-PR085", 76, 2076),
    ("DOW-UAP-PR086", 77, 2077),
    ("DOW-UAP-PR087", 78, 2078),
    ("DOW-UAP-PR088", 79, 2079),
    ("DOW-UAP-PR089", 80, 2080),
    ("DOW-UAP-PR090", 81, 2081),
    ("DOW-UAP-PR091", 82, 2082),
    ("DOW-UAP-PR092", 83, 2083),
    ("DOW-UAP-PR093", 84, 2084),
    ("DOW-UAP-PR094", 85, 2085),
    ("DOW-UAP-PR095", 86, 2086),
    ("DOW-UAP-PR096", 87, 2087),
    ("DOW-UAP-PR097", 88, 2088),
    # PR098(R02-092): SKIP → マッピング対象外
    ("DOW-UAP-PR099", 89, 2089),
    # 管理漏れ補完: PR052(R02-090) / PR070(R02-091)
    ("DOW-UAP-PR052", 90, 2090),
    ("DOW-UAP-PR070", 91, 2091),
]

# ── 定数 ─────────────────────────────────────────────────────────────────────

# マッチするタイトル先頭パターン（#TBD または #2_TBD）
TITLE_TBD_PATTERN = re.compile(
    r"^(# 【概要版)#(?:TBD|2_TBD)(】.*)$",
    re.MULTILINE,
)

# 更新済みチェック用（R02-NNN が既に入っているか）
TITLE_DONE_PATTERN = re.compile(
    r"^# 【概要版#R02-\d{3}】",
    re.MULTILINE,
)

# フッター置換対象（一行・固定文字列）
FOOTER_OLD = (
    "⚠️ **source_registry 未登録：** "
    "本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。"
    "公開前に source_registry への登録が必要です。"
)


# ── データクラス ──────────────────────────────────────────────────────────────

@dataclass
class Entry:
    glob_key: str
    r02_num: int
    publish_order: int

    @property
    def article_id(self) -> str:
        return f"R02-{self.r02_num:03d}"

    @property
    def h2_xxx(self) -> str:
        return f"#2_{self.r02_num:03d}"

    @property
    def footer_new(self) -> str:
        return (
            f"📋 **article_id：{self.article_id} / {self.h2_xxx} / publish_order: {self.publish_order}**"
            f"（{TODAY} 正式採番）  \n"
            "source_registry.csv への登録は公開キュー投入時に実施予定です。"
        )

    @property
    def title_replacement(self) -> str:
        return f"\\g<1>#{self.article_id}\\g<2>"


@dataclass
class Result:
    entry: Entry
    path: Path | None
    status: str          # SKIP | NEED_UPDATE | MISSING | ERROR
    reason: str
    title_before: str = ""
    title_after: str = ""
    footer_changed: bool = False


# ── ファイル検索 ──────────────────────────────────────────────────────────────

def find_draft(entry: Entry) -> Path | None:
    """glob_key に対応するドラフトファイルを返す（archive 除外）。"""
    pattern = f"ai_summary_{entry.glob_key}_*_note_version.md"
    candidates = [
        p for p in DRAFTS_DIR.glob(pattern)
        if ARCHIVE_DIR not in p.parents and p.parent == DRAFTS_DIR
    ]
    if not candidates:
        return None
    if len(candidates) > 1:
        # 複数ある場合は最も短い名前（= 標準形）を選択
        candidates.sort(key=lambda p: len(p.name))
    return candidates[0]


# ── 更新ロジック ──────────────────────────────────────────────────────────────

def analyze(entry: Entry) -> Result:
    """ドラフトの更新要否を分析する（ファイルは変更しない）。"""
    path = find_draft(entry)

    if path is None:
        return Result(entry=entry, path=None, status="MISSING",
                      reason="note_drafts/ にドラフトファイルが見つからない")

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return Result(entry=entry, path=path, status="ERROR",
                      reason=f"読み込みエラー: {e}")

    # 更新済みチェック
    if TITLE_DONE_PATTERN.search(text):
        title_line = text.splitlines()[0] if text else ""
        return Result(entry=entry, path=path, status="SKIP",
                      reason="タイトルに #R02-XXX が既に反映済み",
                      title_before=title_line)

    # 更新必要チェック
    title_match = TITLE_TBD_PATTERN.search(text)
    if not title_match:
        title_line = text.splitlines()[0] if text else ""
        return Result(entry=entry, path=path, status="ERROR",
                      reason=f"タイトル行にパターン不一致（#TBD / #R02-XXX いずれもなし）: {title_line[:60]}",
                      title_before=title_line)

    title_before = title_match.group(0)
    title_after = TITLE_TBD_PATTERN.sub(entry.title_replacement, title_before, count=1)
    footer_changed = FOOTER_OLD in text

    return Result(
        entry=entry,
        path=path,
        status="NEED_UPDATE",
        reason="",
        title_before=title_before,
        title_after=title_after,
        footer_changed=footer_changed,
    )


def apply_update(result: Result, backup: bool = True) -> str:
    """ファイルを実際に更新する。backup=True の場合 .bak を作成する。"""
    assert result.path is not None
    text = result.path.read_text(encoding="utf-8")

    # バックアップ
    if backup:
        bak_path = result.path.with_suffix(".md.bak")
        shutil.copy2(result.path, bak_path)

    # タイトル更新（最初の1件のみ）
    new_text = TITLE_TBD_PATTERN.sub(result.entry.title_replacement, text, count=1)

    # フッター更新
    if FOOTER_OLD in new_text:
        new_text = new_text.replace(FOOTER_OLD, result.entry.footer_new)

    result.path.write_text(new_text, encoding="utf-8")
    return str(result.path.with_suffix(".md.bak")) if backup else ""


# ── レポート生成 ──────────────────────────────────────────────────────────────

def build_report(results: list[Result], mode: str) -> str:
    need = [r for r in results if r.status == "NEED_UPDATE"]
    skip = [r for r in results if r.status == "SKIP"]
    missing = [r for r in results if r.status == "MISSING"]
    error = [r for r in results if r.status == "ERROR"]

    lines: list[str] = []
    lines.append(f"# Release 02 ドラフト title/footer 一括更新 dry-run レポート")
    lines.append(f"")
    lines.append(f"**実行日：** {TODAY}")
    lines.append(f"**モード：** {mode}")
    lines.append(f"**スクリプト：** scripts/update_release02_draft_ids.py v{VERSION}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## 1. サマリー")
    lines.append(f"")
    lines.append(f"| 状態 | 件数 | 内容 |")
    lines.append(f"|---|---|---|")
    lines.append(f"| ⛔ NEED_UPDATE（要更新） | **{len(need)}件** | #TBD 残存・更新対象 |")
    lines.append(f"| ✅ SKIP（更新済み） | **{len(skip)}件** | #R02-XXX 反映済み |")
    lines.append(f"| ⚠️ MISSING（ファイル未発見） | **{len(missing)}件** | note_drafts/ に該当なし |")
    lines.append(f"| ❌ ERROR（処理不能） | **{len(error)}件** | パターン不一致 / 読み込み失敗 |")
    lines.append(f"| **合計（マッピング件数）** | **{len(results)}件** | |")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # NEED_UPDATE 詳細
    lines.append(f"## 2. 更新対象ファイル（NEED_UPDATE: {len(need)}件）")
    lines.append(f"")
    lines.append(f"| No. | article_id | publish_order | ファイル名 | タイトル変更 | footer変更 |")
    lines.append(f"|---|---|---|---|---|---|")
    for i, r in enumerate(need, 1):
        fname = r.path.name if r.path else "(none)"
        title_change = f"`{r.title_before[:30]}...` → `{r.title_after[:30]}...`" if r.title_before else ""
        lines.append(
            f"| {i} | {r.entry.article_id} | {r.entry.publish_order} "
            f"| `{fname}` | {title_change} | {'✓' if r.footer_changed else '—'} |"
        )
    lines.append(f"")

    # NEED_UPDATE 差分詳細
    lines.append(f"## 3. 変更前/変更後 詳細（NEED_UPDATE）")
    lines.append(f"")
    for r in need:
        lines.append(f"### {r.entry.article_id} / {r.entry.h2_xxx} / publish_order: {r.entry.publish_order}")
        lines.append(f"")
        lines.append(f"**ファイル：** `{r.path}`")
        lines.append(f"")
        lines.append(f"**タイトル変更：**")
        lines.append(f"```")
        lines.append(f"変更前: {r.title_before}")
        lines.append(f"変更後: {r.title_after}")
        lines.append(f"```")
        lines.append(f"")
        if r.footer_changed:
            lines.append(f"**フッター変更：**")
            lines.append(f"```")
            lines.append(f"変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...")
            lines.append(f"変更後: {r.entry.footer_new[:80]}...")
            lines.append(f"```")
        else:
            lines.append(f"**フッター：** 変更なし（旧形式フッターが見つからない）")
        lines.append(f"")

    # SKIP 詳細
    lines.append(f"## 4. 更新済みファイル（SKIP: {len(skip)}件）")
    lines.append(f"")
    lines.append(f"| article_id | publish_order | ファイル名 | タイトル |")
    lines.append(f"|---|---|---|---|")
    for r in skip:
        fname = r.path.name if r.path else "(none)"
        lines.append(
            f"| {r.entry.article_id} | {r.entry.publish_order} "
            f"| `{fname}` | `{r.title_before[:50]}...` |"
        )
    lines.append(f"")

    # MISSING 詳細
    if missing:
        lines.append(f"## 5. ファイル未発見（MISSING: {len(missing)}件）")
        lines.append(f"")
        lines.append(f"| article_id | glob_key | 理由 |")
        lines.append(f"|---|---|---|")
        for r in missing:
            lines.append(f"| {r.entry.article_id} | `{r.entry.glob_key}` | {r.reason} |")
        lines.append(f"")

    # ERROR 詳細
    if error:
        lines.append(f"## 6. 処理不能（ERROR: {len(error)}件）")
        lines.append(f"")
        for r in error:
            lines.append(f"- **{r.entry.article_id}** `{r.path}` : {r.reason}")
        lines.append(f"")

    # execute 実行方法
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## 7. 実行方法")
    lines.append(f"")
    lines.append(f"dry-run 確認後に以下で実行：")
    lines.append(f"")
    lines.append(f"```bash")
    lines.append(f"python3 scripts/update_release02_draft_ids.py --execute")
    lines.append(f"```")
    lines.append(f"")
    lines.append(f"- 実行時は各ファイルの `.bak` バックアップを自動作成")
    lines.append(f"- `--no-backup` オプションでバックアップをスキップ可")
    lines.append(f"- workflow.db / source_registry.csv は変更しない")
    lines.append(f"")

    return "\n".join(lines)


# ── メイン ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Release 02 VIDドラフト title/footer 一括更新"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true",
                      help="変更内容を表示するのみ（ファイル変更なし）")
    mode.add_argument("--execute", action="store_true",
                      help="実際にファイルを更新する（.bak バックアップ作成）")
    parser.add_argument("--no-backup", action="store_true",
                        help="--execute 時にバックアップをスキップ（非推奨）")
    parser.add_argument("--output", default=None,
                        help="dry-run レポートの出力先（省略時は stdout）")
    args = parser.parse_args()

    # 作業ディレクトリ確認
    if not DRAFTS_DIR.is_dir():
        sys.exit(f"[ERROR] {DRAFTS_DIR} が見つかりません。プロジェクトルートから実行してください。")

    # --execute は dry-run 確認後のみ許可するガード
    if args.execute:
        print("=" * 60)
        print("⚠️  --execute モードです。ファイルが変更されます。")
        print(f"   対象: {DRAFTS_DIR}/")
        print("   バックアップ: 各ファイルに .bak を作成します。")
        if args.no_backup:
            print("   ⚠️ --no-backup 指定：バックアップをスキップします。")
        print("=" * 60)
        confirm = input("続行しますか？ [yes/no]: ").strip().lower()
        if confirm != "yes":
            print("中止しました。")
            sys.exit(0)

    # 全エントリを分析
    entries = [Entry(*m) for m in MAPPING]
    results = [analyze(e) for e in entries]

    need = [r for r in results if r.status == "NEED_UPDATE"]
    skip = [r for r in results if r.status == "SKIP"]
    missing = [r for r in results if r.status == "MISSING"]
    error = [r for r in results if r.status == "ERROR"]

    # dry-run
    if args.dry_run:
        mode_label = "DRY-RUN（変更なし）"
        report = build_report(results, mode_label)

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report, encoding="utf-8")
            print(f"レポートを保存しました: {out_path}")
        else:
            print(report)

        print(f"\n--- dry-run サマリー ---")
        print(f"  NEED_UPDATE: {len(need)}件")
        print(f"  SKIP（更新済み）: {len(skip)}件")
        print(f"  MISSING: {len(missing)}件")
        print(f"  ERROR: {len(error)}件")
        print(f"  合計（マッピング件数）: {len(results)}件")
        return

    # execute
    if args.execute:
        if not need:
            print("更新が必要なファイルはありません。")
            return

        updated: list[str] = []
        failed: list[str] = []
        for r in need:
            try:
                bak = apply_update(r, backup=not args.no_backup)
                updated.append(str(r.path))
                bak_info = f" (bak: {bak})" if bak else ""
                print(f"  ✅ 更新: {r.path}{bak_info}")
            except Exception as exc:
                failed.append(str(r.path))
                print(f"  ❌ 失敗: {r.path}: {exc}")

        print(f"\n--- execute 完了 ---")
        print(f"  更新済み: {len(updated)}件")
        print(f"  失敗: {len(failed)}件")
        print(f"  SKIP（更新済み）: {len(skip)}件")
        if failed:
            print(f"  失敗ファイル: {failed}")


if __name__ == "__main__":
    main()
