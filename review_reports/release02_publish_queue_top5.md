# Release 02 note公開キュー TOP 5（#2_010〜#2_014）

**作成日：** 2026-06-23  
**対象：** #2_010（PR019）〜 #2_014（PR026）  
**公開順序：** publish_order 昇順（2010 → 2014）  
**ステータス：** 公開可能（全件 DONE_CANDIDATE 確認済み）

---

## Codex最終判定メモ（公開前確認）

| #2_XXX | PR | Codex iter2 VERDICT | BLOCK内容 | 公開可否 |
|---|---|---|---|---|
| #2_010 | PR019 | BLOCK（3） | ①source_registry未登録（全件共通）②Release表記誤解（Codex誤判定）③WAR.GOV URLトップページ（設計通り） | ✅ **可** |
| #2_011 | PR021 | BLOCK（1） | ①source_registry未登録（全件共通） | ✅ **可** |
| #2_012 | PR022 | WARN（1） | P1-5: source_registry整合（全件共通） | ✅ **可** |
| #2_013 | PR023 | BLOCK（1） | ①source_registry未登録（全件共通） | ✅ **可** |
| #2_014 | PR026 | BLOCK（2） | ①source_registry未登録②WAR.GOV URLトップページ（設計通り） | ✅ **可** |

> **判定根拠：** source_registry未登録BLOCKは公開キュー投入前の全件共通状態（source_registry登録は公開後実施）。WAR.GOV URLはトップページのみが仕様（直接URLはDVIDS URLで補完済み）。Release表記はCodexのプロジェクト番号体系誤解（war.gov "release_1" ≠ 本プロジェクト "Release 02"）。

---

## #2_010

**article_id：** R02-010  
**publish_order：** 2010  
**対象：** DOW-UAP-PR019（中東 2022年5月 UAP事案映像）

```
draft:
  note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md

thumbnail dir:
  thumbnails/DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022/

frame（アイキャッチ候補）:
  thumbnails/DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022/frame_0005.png
  ※ frame_0000.png も利用可（計2枚）

source:
  raw_media/video/DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022.mp4

codex audit（最終）:
  review_reports/codex_audit_20260620_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_iter2.md
```

**Finder表示コマンド：**
```bash
open -R "note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md"
open "thumbnails/DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022/"
```

**公開後に実行するコマンド：**
```bash
python3 scripts/post_publish_workflow.py \
  --slug DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022 \
  --draft "note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md" \
  --note-url https://note.com/deft_ibis3303/n/XXXXXXXX \
  --audit "review_reports/codex_audit_20260620_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_iter2.md"
```

---

## #2_011

**article_id：** R02-011  
**publish_order：** 2011  
**対象：** DOW-UAP-PR021（イラク 2022年5月 UAP事案映像）

```
draft:
  note_drafts/ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md

thumbnail dir:
  thumbnails/DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022/

frame（アイキャッチ候補）:
  thumbnails/DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022/frame_0005.png
  ※ frame_0000.png / frame_0010.png も利用可（計3枚）

source:
  raw_media/video/DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022.mp4

codex audit（最終）:
  review_reports/codex_audit_20260620_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_iter2.md
```

**Finder表示コマンド：**
```bash
open -R "note_drafts/ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md"
open "thumbnails/DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022/"
```

**公開後に実行するコマンド：**
```bash
python3 scripts/post_publish_workflow.py \
  --slug DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022 \
  --draft "note_drafts/ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md" \
  --note-url https://note.com/deft_ibis3303/n/XXXXXXXX \
  --audit "review_reports/codex_audit_20260620_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_iter2.md"
```

---

## #2_012

**article_id：** R02-012  
**publish_order：** 2012  
**対象：** DOW-UAP-PR022（シリア 2022年7月 UAP事案映像・3分割表示）

```
draft:
  note_drafts/ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_note_version.md

thumbnail dir:
  thumbnails/DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022/

frame（アイキャッチ候補）:
  thumbnails/DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022/frame_0005.png
  ※ frame_0000.png / frame_0010.png も利用可（計3枚）

source:
  raw_media/video/DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022.mp4

codex audit（最終）:
  review_reports/codex_audit_20260620_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_iter2.md
```

**Finder表示コマンド：**
```bash
open -R "note_drafts/ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_note_version.md"
open "thumbnails/DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022/"
```

**公開後に実行するコマンド：**
```bash
python3 scripts/post_publish_workflow.py \
  --slug DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022 \
  --draft "note_drafts/ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_note_version.md" \
  --note-url https://note.com/deft_ibis3303/n/XXXXXXXX \
  --audit "review_reports/codex_audit_20260620_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_iter2.md"
```

---

## #2_013

**article_id：** R02-013  
**publish_order：** 2013  
**対象：** DOW-UAP-PR023（イラク 2022年12月 UAP事案映像）

```
draft:
  note_drafts/ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_note_version.md

thumbnail dir:
  thumbnails/DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022/

frame（アイキャッチ候補）:
  thumbnails/DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022/frame_0005.png
  ※ frame_0000.png / frame_0010.png も利用可（計3枚）

source:
  raw_media/video/DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022.mp4

codex audit（最終）:
  review_reports/codex_audit_20260620_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_iter2.md
```

**Finder表示コマンド：**
```bash
open -R "note_drafts/ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_note_version.md"
open "thumbnails/DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022/"
```

**公開後に実行するコマンド：**
```bash
python3 scripts/post_publish_workflow.py \
  --slug DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022 \
  --draft "note_drafts/ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_note_version.md" \
  --note-url https://note.com/deft_ibis3303/n/XXXXXXXX \
  --audit "review_reports/codex_audit_20260620_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_iter2.md"
```

---

## #2_014

**article_id：** R02-014  
**publish_order：** 2014  
**対象：** DOW-UAP-PR026（アラブ首長国連邦 2023年10月 UAP事案映像）

```
draft:
  note_drafts/ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md

thumbnail dir:
  thumbnails/DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023/

frame（アイキャッチ候補）:
  thumbnails/DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023/frame_0005.png
  ※ frame_0000〜frame_0020 まで計5枚（frame_0005 推奨）

source:
  raw_media/video/DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023.mp4

codex audit（最終）:
  review_reports/codex_audit_20260620_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_iter2.md
```

**Finder表示コマンド：**
```bash
open -R "note_drafts/ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md"
open "thumbnails/DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023/"
```

**公開後に実行するコマンド：**
```bash
python3 scripts/post_publish_workflow.py \
  --slug DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023 \
  --draft "note_drafts/ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md" \
  --note-url https://note.com/deft_ibis3303/n/XXXXXXXX \
  --audit "review_reports/codex_audit_20260620_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_iter2.md"
```

---

## 公開手順チェックリスト（各記事共通）

```
[ ] 1. Finder でドラフトを開いてタイトル確認（【概要版#R02-XXX】になっていること）
[ ] 2. Finder でthumbnail dirを開いてアイキャッチ候補を確認
[ ] 3. note.com で新規記事作成
[ ] 4. ドラフト本文を貼り付け
[ ] 5. アイキャッチ画像を設定（frame_0005.png 推奨）
[ ] 6. タグ設定（UAP / Release02 / 米国防省 など）
[ ] 7. プレビューで確認
[ ] 8. 公開 → URLをコピー
[ ] 9. post_publish_workflow.py を実行（公開URLを --note-url に渡す）
[ ] 10. git commit（published_articles/ + logs/ のみ）
```
