#!/usr/bin/env python3
"""
codex_request_gen.py — Codex 監査依頼パッケージ生成スクリプト

使い方:
  python3 scripts/codex_request_gen.py --slug <記事スラッグ>
  python3 scripts/codex_request_gen.py --slug western_us_event_slides_20260508 \\
      --draft-path note_drafts/ai_summary_western_us_event_slides_20260508_note_version.md

動作環境: Mac Studio（メイン）
前提条件: init_db.py でDBを初期化済みであること

役割:
  1. S_CLASS ガード・Current Owner・イテレーション上限を事前チェック
  2. note_drafts/ のドラフトを読み込み、監査プロンプトを組み立てる
  3. review_requests/codex_request_YYYYMMDD_<slug>.md を生成する
  4. workflow_events に draft_created または codex_requested を記録する

次のステップ:
  生成ファイルを確認後 → codex_flow.py で agmsg 送信 or 手動フォールバック
"""

import sqlite3
import argparse
import re
import shlex
import sys
from pathlib import Path
from datetime import datetime

CHECKLIST_VER = "v1.11"
MAX_CODEX_ITERATIONS = 2


# ── PASS後 Finder 表示ユーティリティ ───────────────────────────────────────

def _quote_path(path: str) -> str:
    """Finder表示コマンド用にパスをshell quoteする。"""
    return shlex.quote(path)

def _get_image_info(draft_path: str) -> dict:
    """ドラフトファイルから page_images/ 参照を抽出する。
    フォルダが存在する場合は実ファイルを列挙する（テキスト参照漏れを防ぐ）。"""
    try:
        content = Path(draft_path).read_text(encoding="utf-8")
    except (OSError, IOError):
        return {}
    matches = re.findall(r'page_images/([^/\s、。）(（]+)/page_(\d+)\.png', content)
    if not matches:
        return {}
    folder = matches[0][0]
    folder_path = "page_images/" + folder
    fp = Path(folder_path)
    if fp.is_dir():
        pages = sorted(str(p) for p in fp.glob("page_*.png"))
    else:
        nums = sorted(set(num for _, num in matches))
        pages = [folder_path + "/page_" + n + ".png" for n in nums]
    return {
        "folder_path": folder_path,
        "pages": pages,
        "exists": fp.is_dir(),
    }


def _print_image_steps(draft_path: str) -> None:
    """PASS後のnote投稿準備コマンドを表示する。"""
    info = _get_image_info(draft_path)
    print()
    print("【手順 5（PASS後）】note投稿前のFinder確認コマンド：")
    print("  1. ドラフトFinder表示コマンド：")
    print(f"    open -R {_quote_path(draft_path)}")
    if not info:
        print("  （このドラフトに page_images 参照が見つかりませんでした）")
        return
    if info["exists"]:
        print("  2. 使用画像Finder表示コマンド：")
        for p in info["pages"]:
            print(f"    open -R {_quote_path(p)}")
        print("  3. 画像フォルダFinder表示コマンド：")
        print(f"    open {_quote_path(info['folder_path'])}/")
    else:
        print("  2. 使用画像Finder表示コマンド：")
        for p in info["pages"]:
            print(f"    （Mac Studio側に画像なし）open -R {_quote_path(p)}")
        print("  3. 画像フォルダFinder表示コマンド：")
        print(f"    （Mac Studio側に画像なし）open {_quote_path(info['folder_path'])}/")
        print("  4. 注意：Mac Studio側に画像がありません。")
        print("     Mac Studio側Finderでは直接表示できないため、Mac mini側の画像配置を確認してください。")
        print(f"  （対象フォルダ: {info['folder_path']}）")


PROMPT_TEMPLATE = """\
# Codex 監査依頼

## 依頼メタデータ
- 記事スラッグ：{slug}
- ドラフトファイル：{draft_path}
- チェックリスト：docs/audit_checklist_v1.md（{checklist_ver}）
- 依頼日時：{timestamp}

## 出力指示（必須）
- 監査結果は **{response_path}** に保存してください
- **note_drafts/ 内のファイルは一切編集しないでください**
- 作成・変更してよいファイルは review_reports/ のみです
- 出力は必ず `---CODEX_AUDIT_START---` から `---CODEX_AUDIT_END---` で囲んでください
- 上記マーカー以外の前置き・後書き・補足説明は出力しないでください

## 監査指示
以下の UAP 翻訳記事ドラフトを、docs/audit_checklist_v1.md に従って監査してください。

【重要な制約】
- 応答は監査レポートのみとしてください
- Claude Code への指示・再監査要求は行わないでください
- 修正を自動的に適用しないでください
- 判定は PASS / WARN / BLOCK のいずれかのみ使用してください
- 出力フォーマットは以下の構造に厳密に従ってください

## 出力フォーマット（必須）

⚠ 以下のヘッダー5行は機械判読用です。`---CODEX_AUDIT_START---` の直後に、この順序・この表記で必ず出力してください。
VERDICT / BLOCK / WARN / UNVERIFIABLE / PASS の行は省略・並べ替え・日本語化・絵文字付加を禁止します。

---CODEX_AUDIT_START---
VERDICT: PASS
BLOCK: 0
WARN: 0
UNVERIFIABLE: 0
PASS: 14
MODEL: [使用モデルID]
---ITEMS_START---
[チェック項目コード] [PASS|WARN|BLOCK|UNVERIFIABLE] [説明]
---ITEMS_END---
---WARN_DETAILS_START---
W-01: [セクション名] | [該当文] | [修正案]
---WARN_DETAILS_END---
---CODEX_AUDIT_END---

- VERDICT は `PASS` / `WARN` / `BLOCK` のいずれか1語のみ（絵文字・日本語・補足語句を含まないこと）
- BLOCK / WARN / UNVERIFIABLE / PASS は各カテゴリの件数を半角数値で記述すること

## ドラフト本文
{draft_content}
"""


def open_db(db_path: str) -> sqlite3.Connection:
    if not Path(db_path).exists():
        sys.exit(
            f"[ERROR] DB が見つかりません: {db_path}\n"
            "先に python3 scripts/init_db.py を実行してください。"
        )
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con


def check_preconditions(slug: str, db_path: str) -> None:
    """S_CLASS ガード / Current Owner / イテレーション上限チェック"""
    con = open_db(db_path)

    # S_CLASS ガード（§3-B）
    row = con.execute(
        "SELECT classification FROM articles WHERE slug = ?", (slug,)
    ).fetchone()
    if row:
        cls = row["classification"]
        if cls == "S_CLASS":
            con.close()
            sys.exit(f"[HARD STOP] '{slug}' は S_CLASS 資料です。agmsg 送信禁止。ワークフロー停止。")
        if cls == "CONFIDENTIAL":
            resp = input(f"[WARN] '{slug}' は CONFIDENTIAL です。Codex へ送信してよいですか？ (y/N): ")
            if resp.strip().lower() != "y":
                con.close()
                sys.exit("[停止] ユーザーが CONFIDENTIAL 送信をキャンセルしました。")

    # Current Owner チェック（§3-A）
    owner_row = con.execute(
        "SELECT current_owner FROM workflow_owner WHERE article_slug = ? ORDER BY id DESC LIMIT 1",
        (slug,),
    ).fetchone()
    if owner_row and owner_row["current_owner"] != "CLAUDE":
        owner = owner_row["current_owner"]
        con.close()
        sys.exit(
            f"[停止] オーナー不一致。現在のオーナー: {owner}（送信には CLAUDE である必要があります）"
        )

    # イテレーション上限チェック（§3 MAX_CODEX_ITERATIONS）
    art = con.execute("SELECT id FROM articles WHERE slug = ?", (slug,)).fetchone()
    if art:
        count = con.execute(
            "SELECT COUNT(*) AS cnt FROM codex_sessions WHERE article_id = ?",
            (art["id"],),
        ).fetchone()["cnt"]
        if count >= MAX_CODEX_ITERATIONS:
            con.close()
            sys.exit(
                f"[停止] Codex 呼び出し上限（{MAX_CODEX_ITERATIONS}回）に達しています。\n"
                "3回目以降の実行には人間の明示的な承認が必要です。"
            )
    con.close()


def record_event(db_path: str, slug: str, event_type: str, detail: str) -> None:
    con = open_db(db_path)
    art = con.execute("SELECT id FROM articles WHERE slug = ?", (slug,)).fetchone()
    article_id = art["id"] if art else None
    con.execute(
        "INSERT INTO workflow_events (article_id, event_type, detail, start_time) VALUES (?, ?, ?, ?)",
        (article_id, event_type, detail, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    con.commit()
    con.close()


def generate_request(slug: str, draft_path: str, db_path: str) -> str:
    check_preconditions(slug, db_path)

    draft = Path(draft_path)
    if not draft.exists():
        sys.exit(f"[ERROR] ドラフトファイルが見つかりません: {draft_path}")

    draft_content = draft.read_text(encoding="utf-8")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_str = datetime.now().strftime("%Y%m%d")

    Path("review_requests").mkdir(exist_ok=True)
    Path("review_reports").mkdir(exist_ok=True)
    out_path = f"review_requests/codex_request_{date_str}_{slug}.md"
    response_path = f"review_reports/codex_audit_{date_str}_{slug}.md"

    content = PROMPT_TEMPLATE.format(
        slug=slug,
        draft_path=draft_path,
        checklist_ver=CHECKLIST_VER,
        timestamp=timestamp,
        response_path=response_path,
        draft_content=draft_content,
    )
    Path(out_path).write_text(content, encoding="utf-8")

    record_event(db_path, slug, "codex_requested", f"request_path={out_path}")

    _print_next_steps(out_path, response_path, slug, draft_path)
    return out_path


def _print_next_steps(out_path: str, response_path: str, slug: str, draft_path: str) -> None:
    """依頼生成後の人間向け手順を表示する"""
    sep = "─" * 60
    print()
    print(sep)
    print(f"[OK] 依頼パッケージ生成: {out_path}")
    print(f"     出力先（監査結果）: {response_path}")
    print(sep)
    print()
    print("【手順 1】Finder でファイルを確認：")
    print(f"  open -R {out_path}")
    print()
    print("【手順 2】依頼文をクリップボードへコピー：")
    print(f"  pbcopy < {out_path}")
    print()
    print("【手順 3-A】Codex Terminal に貼り付け（手動 Fallback）")
    print("  ペースト後、Codex が出力した監査結果を以下のファイルへ保存：")
    print(f"  {response_path}")
    print()
    print("【手順 3-B】Codex CLI 非対話実行（自動）：")
    print(f"  codex exec - \\")
    print(f"    -s read-only \\")
    print(f"    -m o4-mini \\")
    print(f"    -o {response_path} \\")
    print(f"    < {out_path}")
    print()
    print("【手順 4】監査結果の解析（Codex 完了後）：")
    print(f"  python3 scripts/codex_flow.py \\")
    print(f"    --slug {slug} \\")
    print(f"    --fallback \\")
    print(f"    --response-path {response_path}")
    _print_image_steps(draft_path)
    print(sep)


def main() -> None:
    parser = argparse.ArgumentParser(description="Codex 監査依頼パッケージ生成")
    parser.add_argument("--slug", required=True,
                        help="記事スラッグ（例: western_us_event_slides_20260508）")
    parser.add_argument("--draft-path",
                        help="ドラフトファイルパス（省略時: note_drafts/ai_summary_<slug>_note_version.md）")
    parser.add_argument("--db-path", default="workflow.db")
    args = parser.parse_args()

    draft_path = args.draft_path or f"note_drafts/ai_summary_{args.slug}_note_version.md"
    generate_request(args.slug, draft_path, args.db_path)



if __name__ == "__main__":
    main()
