# Release 02 VID 公開キュー dry-run レポート

**作成日：** 2026-06-21  
**ステータス：** DRY-RUN（workflow.db / source_registry.csv / note公開 / git操作 すべて未実行）  
**目的：** Release 02 VID DONE_CANDIDATE 78件の公開キュー投入前確認  
**参照：** release02_numbering_plan.md（v2+補完）/ release02_gap_closure_plan.md

---

## 0. 件数・重複・欠落サマリー

| チェック項目 | 結果 | 詳細 |
|---|---|---|
| **対象件数** | **78件** | 前バッチA 27 + 前バッチB 6 + 中間バッチ有効 15 + 今回バッチ 28 + 管理漏れ補完 2 |
| **article_id 重複** | **なし** | R02-010〜036 / R02-037〜042 / R02-043〜046 / R02-051〜061 / R02-062〜091（欠番: R02-047〜050 = HOLD） |
| **#2_XXX 重複** | **なし** | #2_010〜036 / #2_037〜042 / #2_043〜046 / #2_051〜061 / #2_062〜091 |
| **publish_order 重複** | **なし** | 2010〜2036 / 2037〜2042 / 2043〜2046 / 2051〜2061 / 2062〜2091 |
| **note_draft 欠落** | **0件** | PR071 正規版（ドラフトA）確定済み。ドラフトBは archive 済み（2026-06-21） |
| **Codex 最終 PASS 欠落** | **✅ 0件** | PR066 iter3・PR071 iter3・PR060 iter2 PASS 確認済み（2026-06-21） |
| **thumbnail 欠落** | **0件** | PR065・PR071 に重複ディレクトリあり（整理推奨・投入ブロックなし） |
| **人間確認必要** | **0件** | PR066・PR071・PR060 すべて解消済み（2026-06-21） |

---

## 1. 対象外確認（公開キューから除外済み）

| 状態 | 件数 | PR番号・article_id |
|---|---|---|
| **公開済み** | 2件 | PR050（R02-008）/ PR051（R02-009）|
| **HOLD** | 3件（4 article_id） | PR057（R02-047）/ PR057a（R02-048）/ PR057b（R02-049）/ PR058（R02-050）|
| **SKIP** | 1件 | PR098（R02-092）超長尺 1056秒 |

---

## 2. 人間確認が必要な記事

### ✅ [解消済み] PR066（R02-058）— Codex iter3 PASS（2026-06-21）

| 項目 | 内容 |
|---|---|
| **ステータス** | **✅ DONE_CANDIDATE（Codex iter3 PASS 2026-06-21）** |
| **旧Codex最終** | `codex_audit_20260619_DOW-UAP-PR066_..._iter2.md` VERDICT: BLOCK（P1-5 / P2-DRAFTNOTE） |
| **実施した修正** | タイトル `#TBD` → `#R02-058`、作業メモ行削除、フッター article_id 採番済み形式に更新 |
| **新Codex最終** | `codex_audit_20260621_DOW-UAP-PR066_..._iter3.md` VERDICT: PASS（BLOCK: 0 / WARN: 1）|
| **WARN（残存・任意）** | W-01: 「IR hot」表現が物理的熱源確認のように読まれる可能性（公開前修正は任意） |
| **article_id** | R02-058 / #2_058 / publish_order: 2058 |

### ✅ [解消済み] PR071（R02-062）— Codex iter3 PASS（2026-06-21）

| 項目 | 内容 |
|---|---|
| **ステータス** | **✅ DONE_CANDIDATE（Codex iter3 PASS 2026-06-21）** |
| **正規ドラフト** | `ai_summary_DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron_note_version.md`（ドラフトA・詳細版）|
| **archive** | `note_drafts/archive/ai_summary_DOW-UAP-PR071_..._Weapon_System_note_version.md`（ドラフトB・簡略版）|
| **差分概要** | ドラフトA：詳細ffprobe / タイムライン分析 / 注意点4項目 / 外部背景情報あり。ドラフトB：簡略ffprobe（「確認済み」表記）/ 注意点なし / 外部背景情報なし |
| **実施した修正** | タイトル `#2_TBD` → `#R02-062`、作業メモ行削除、DVIDS URL 追加、thumbnail 参照を長名dir に更新、フッター article_id 採番済み形式に更新 |
| **新Codex最終** | `codex_audit_20260621_...PR071_...Lake_Huron_iter3.md` VERDICT: PASS（BLOCK: 0 / WARN: 1）|
| **WARN（残存・任意）** | W-01: 「追尾クロスヘア」「ロックオンボックス」が確定調の箇所あり（注意点で留保明示済み・公開ブロックなし） |

### ✅ [解消済み] PR060（R02-052）— Codex iter2 PASS（2026-06-21）

| 項目 | 内容 |
|---|---|
| **ステータス** | **✅ DONE_CANDIDATE（Codex iter2 PASS 2026-06-21）** |
| **旧Codex最終** | `codex_audit_20260619_DOW-UAP-PR060_..._obj_2.md` VERDICT: WARN（BLOCK: 0 / WARN: 3）|
| **実施した修正** | タイトル `#TBD` → `#R02-052`、作業メモ行削除、フッター article_id 採番済み形式に更新 |
| **新Codex最終** | `codex_audit_20260621_DOW-UAP-PR060_..._iter2.md` VERDICT: PASS（BLOCK: 0 / WARN: 0）|

### ℹ️ [確認] PR065（R02-057）— thumbnail 重複ディレクトリ（残課題）

| 対象 | 重複状況 | 推奨 |
|---|---|---|
| PR065 | `thumbnails/DOW-UAP-PR065/`（短名）+ `thumbnails/DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024/`（長名）| 長名ディレクトリを使用。短名はアーカイブか削除。 |
| PR071 | `thumbnails/DOW-UAP-PR071/`（短名）+ 長名：解消済み（正規ドラフトAは長名dirを参照）。短名はアーカイブ推奨。 |

---

## 3. 78件一覧（publish_order 昇順）

> `Codex最終` 欄：`PASS` = BLOCKなし確定 / `WARN許容` = BLOCK=0のWARN / `OUT-1` = Codex sandbox制限の出力制限BLOCK（実質PASS） / `要修正` = 公開前修正必須

### 前バッチA（PR019〜049 / 27件）

| pub_order | PR | article_id | #2_XXX | note_draft | Codex最終 | thumbnail |
|---|---|---|---|---|---|---|
| 2010 | PR019 | R02-010 | #2_010 | ✓ | iter2 PASS | ✓ |
| 2011 | PR021 | R02-011 | #2_011 | ✓ | iter2 PASS | ✓ |
| 2012 | PR022 | R02-012 | #2_012 | ✓ | iter2 PASS | ✓ |
| 2013 | PR023 | R02-013 | #2_013 | ✓ | iter2 PASS | ✓ |
| 2014 | PR026 | R02-014 | #2_014 | ✓ | iter2 PASS | ✓ |
| 2015 | PR027 | R02-015 | #2_015 | ✓ | iter2 PASS | ✓ |
| 2016 | PR028 | R02-016 | #2_016 | ✓ | iter2 PASS | ✓ |
| 2017 | PR029 | R02-017 | #2_017 | ✓ | iter2 PASS | ✓ |
| 2018 | PR031 | R02-018 | #2_018 | ✓ | iter2 PASS | ✓ |
| 2019 | PR032 | R02-019 | #2_019 | ✓ | iter2 PASS | ✓ |
| 2020 | PR033 | R02-020 | #2_020 | ✓ | iter2 PASS | ✓ |
| 2021 | PR034 | R02-021 | #2_021 | ✓ | iter2 PASS | ✓ |
| 2022 | PR035 | R02-022 | #2_022 | ✓ | iter3 PASS | ✓ |
| 2023 | PR036 | R02-023 | #2_023 | ✓ | iter2 PASS | ✓ |
| 2024 | PR037 | R02-024 | #2_024 | ✓ | iter2 PASS | ✓ |
| 2025 | PR038 | R02-025 | #2_025 | ✓ | iter3 PASS | ✓ |
| 2026 | PR039 | R02-026 | #2_026 | ✓ | iter2 PASS | ✓ |
| 2027 | PR040 | R02-027 | #2_027 | ✓ | iter2 PASS | ✓ |
| 2028 | PR041 | R02-028 | #2_028 | ✓ | iter2 PASS | ✓ |
| 2029 | PR042 | R02-029 | #2_029 | ✓ | iter2 PASS | ✓ |
| 2030 | PR043 | R02-030 | #2_030 | ✓ | iter2 PASS | ✓ |
| 2031 | PR044 | R02-031 | #2_031 | ✓ | iter2 PASS | ✓ |
| 2032 | PR045 | R02-032 | #2_032 | ✓ | iter2 PASS | ✓ |
| 2033 | PR046 | R02-033 | #2_033 | ✓ | iter2 PASS | ✓ |
| 2034 | PR047 | R02-034 | #2_034 | ✓ | iter2 PASS | ✓ |
| 2035 | PR048 | R02-035 | #2_035 | ✓ | iter2 PASS | ✓ |
| 2036 | PR049 | R02-036 | #2_036 | ✓ | iter2 PASS | ✓ |

### 前バッチB（FBI-PR001〜006 / 6件）

| pub_order | PR | article_id | #2_XXX | note_draft | Codex最終 | thumbnail |
|---|---|---|---|---|---|---|
| 2037 | FBI-PR001 | R02-037 | #2_037 | ✓ | iter3 PASS | ✓ |
| 2038 | FBI-PR002 | R02-038 | #2_038 | ✓ | iter2 PASS | ✓ |
| 2039 | FBI-PR003 | R02-039 | #2_039 | ✓ | iter2 PASS | ✓ |
| 2040 | FBI-PR004 | R02-040 | #2_040 | ✓ | iter2 PASS | ✓ |
| 2041 | FBI-PR005 | R02-041 | #2_041 | ✓ | iter2 PASS | ✓ |
| 2042 | FBI-PR006 | R02-042 | #2_042 | ✓ | iter2 PASS | ✓ |

### 中間バッチ（PR053〜069 / 15件 DONE_CANDIDATE）

| pub_order | PR | article_id | #2_XXX | note_draft | Codex最終 | thumbnail | 備考 |
|---|---|---|---|---|---|---|---|
| 2043 | PR053 | R02-043 | #2_043 | ✓ | iter2 OUT-1 | ✓ | ※OUT-1=Codex sandbox制限・実質PASS |
| 2044 | PR054 | R02-044 | #2_044 | ✓ | iter3 PASS | ✓ | |
| 2045 | PR055 | R02-045 | #2_045 | ✓ | iter2 PASS | ✓ | |
| 2046 | PR056 | R02-046 | #2_046 | ✓ | iter3 PASS | ✓ | |
| ~~2047~~ | ~~PR057~~ | ~~R02-047~~ | ~~#2_047~~ | — | — | — | **HOLD** |
| ~~2048~~ | ~~PR057a~~ | ~~R02-048~~ | ~~#2_048~~ | — | — | — | **HOLD** |
| ~~2049~~ | ~~PR057b~~ | ~~R02-049~~ | ~~#2_049~~ | — | — | — | **HOLD** |
| ~~2050~~ | ~~PR058~~ | ~~R02-050~~ | ~~#2_050~~ | — | — | — | **HOLD** |
| 2051 | PR059 | R02-051 | #2_051 | ✓ | iter6 WARN許容 | ✓ | |
| 2052 | PR060 | R02-052 | #2_052 | ✓ | **iter2 PASS** | ✓ | ✅ 2026-06-21 解消済み |
| 2053 | PR061 | R02-053 | #2_053 | ✓ | iter2 WARN許容 | ✓ | |
| 2054 | PR062 | R02-054 | #2_054 | ✓ | iter5 WARN許容 | ✓ | |
| 2055 | PR063 | R02-055 | #2_055 | ✓ | iter2 WARN許容 | ✓ | |
| 2056 | PR064 | R02-056 | #2_056 | ✓ | iter2 PASS | ✓ | |
| 2057 | PR065 | R02-057 | #2_057 | ✓ | iter2 WARN許容 | ⚠️ | thumbnail 2dir（長名を使用）|
| 2058 | PR066 | R02-058 | #2_058 | ✓ | iter3 PASS | ✓ | ✅ 2026-06-21 解消済み |
| 2059 | PR067 | R02-059 | #2_059 | ✓ | iter1 PASS | ✓ | ※BLOCK=source_registry系のみ・全件共通 |
| 2060 | PR068 | R02-060 | #2_060 | ✓ | iter2 PASS | ✓ | |
| 2061 | PR069 | R02-061 | #2_061 | ✓ | iter2 PASS | ✓ | |

### 今回バッチ（PR071〜099 / 28件）

| pub_order | PR | article_id | #2_XXX | note_draft | Codex最終 | thumbnail | 備考 |
|---|---|---|---|---|---|---|---|
| 2062 | PR071 | R02-062 | #2_062 | ✓ | **iter3 PASS** | ⚠️ | ✅ ドラフトA正規・ドラフトBはarchive。thumbnail短名dir整理推奨 |
| 2063 | PR072 | R02-063 | #2_063 | ✓ | iter2 WARN許容 | ✓ | |
| 2064 | PR073 | R02-064 | #2_064 | ✓ | iter2 PASS | ✓ | |
| 2065 | PR074 | R02-065 | #2_065 | ✓ | iter2 PASS | ✓ | |
| 2066 | PR075 | R02-066 | #2_066 | ✓ | iter2 PASS | ✓ | |
| 2067 | PR076 | R02-067 | #2_067 | ✓ | iter2 PASS | ✓ | |
| 2068 | PR077 | R02-068 | #2_068 | ✓ | iter2 WARN許容 | ✓ | |
| 2069 | PR078 | R02-069 | #2_069 | ✓ | iter2 WARN許容 | ✓ | |
| 2070 | PR079 | R02-070 | #2_070 | ✓ | iter2 PASS | ✓ | |
| 2071 | PR080 | R02-071 | #2_071 | ✓ | iter2 WARN許容 | ✓ | |
| 2072 | PR081 | R02-072 | #2_072 | ✓ | iter2 PASS | ✓ | |
| 2073 | PR082 | R02-073 | #2_073 | ✓ | iter2 WARN許容 | ✓ | |
| 2074 | PR083 | R02-074 | #2_074 | ✓ | iter2 PASS | ✓ | |
| 2075 | PR084 | R02-075 | #2_075 | ✓ | iter2 PASS | ✓ | |
| 2076 | PR085 | R02-076 | #2_076 | ✓ | iter2 PASS | ✓ | |
| 2077 | PR086 | R02-077 | #2_077 | ✓ | iter2 WARN許容 | ✓ | |
| 2078 | PR087 | R02-078 | #2_078 | ✓ | iter2 WARN許容 | ✓ | |
| 2079 | PR088 | R02-079 | #2_079 | ✓ | iter2 WARN許容 | ✓ | |
| 2080 | PR089 | R02-080 | #2_080 | ✓ | iter2 WARN許容 | ✓ | |
| 2081 | PR090 | R02-081 | #2_081 | ✓ | iter2 WARN許容 | ✓ | |
| 2082 | PR091 | R02-082 | #2_082 | ✓ | iter2 WARN許容 | ✓ | |
| 2083 | PR092 | R02-083 | #2_083 | ✓ | iter2 WARN許容 | ✓ | |
| 2084 | PR093 | R02-084 | #2_084 | ✓ | iter2 WARN許容 | ✓ | |
| 2085 | PR094 | R02-085 | #2_085 | ✓ | iter2 PASS | ✓ | |
| 2086 | PR095 | R02-086 | #2_086 | ✓ | iter2 WARN許容 | ✓ | |
| 2087 | PR096 | R02-087 | #2_087 | ✓ | iter2 WARN許容 | ✓ | |
| 2088 | PR097 | R02-088 | #2_088 | ✓ | iter2 WARN許容 | ✓ | |
| 2089 | PR099 | R02-089 | #2_089 | ✓ | iter2 PASS | ✓ | |

### 管理漏れ補完（PR052 / PR070 / 2件）

| pub_order | PR | article_id | #2_XXX | note_draft | Codex最終 | thumbnail |
|---|---|---|---|---|---|---|
| 2090 | PR052 | R02-090 | #2_090 | ✓ | iter2 PASS（2026-06-21）| ✓ |
| 2091 | PR070 | R02-091 | #2_091 | ✓ | iter3 PASS（2026-06-21）| ✓ |

---

## 4. source_registry.csv 登録予定（dry-run）

**登録予定件数：** 78件  
**登録タイミング：** 公開キュー投入実行時（本 dry-run では未実行）  
**既登録：** PR050（R02-008）/ PR051（R02-009）はすでに登録済み

### 登録内容サンプル（先頭3件）

```csv
# 登録予定（dry-run。実際には source_registry.csv に追記）
# publish_order, article_id, #2_XXX, source_file, draft_path, agency, dvids_id
2010, R02-010, #2_010, DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022.mp4, note_drafts/ai_summary_DOW-UAP-PR019_..._note_version.md, Department of War, (DVIDS ID 要確認)
2011, R02-011, #2_011, DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022.mp4, note_drafts/ai_summary_DOW-UAP-PR021_..._note_version.md, Department of War, (DVIDS ID 要確認)
...（以下 78件分）
2091, R02-091, #2_091, DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_Unidentified_Aerial_Phenomena_UAP_on_13_.mp4, note_drafts/ai_summary_DOW-UAP-PR070_..._note_version.md, Department of War, 1007783
```

### 注記

- **76件**は現在 `⚠️ source_registry 未登録` フッターを持つ。source_registry 登録実行時に `📋 article_id：R02-XXX / #2_XXX / publish_order: XXXX` に更新が必要。
- **2件**（PR052 / PR070）はすでに `📋 article_id：...` フッター形式で登録済み。
- source_registry.csv の既存列（dvids_video_id 等）はファイル名から参照可能だが、全件のDVIDS IDは files_catalog.csv と突き合わせが必要。

---

## 5. workflow.db 登録予定（dry-run）

**登録予定件数：** 78件  
**登録タイミング：** 公開キュー投入実行時（本 dry-run では未実行）

### 登録内容サンプル

```sql
-- 登録予定（dry-run。実際には INSERT OR REPLACE INTO articles を実行）
-- PR066 は修正完了後に追加（現時点では除外推奨）

INSERT OR REPLACE INTO articles (slug, status, publish_order, blocked) VALUES
  ('DOW-UAP-PR019', 'ready_to_publish', 2010, 0),
  ('DOW-UAP-PR021', 'ready_to_publish', 2011, 0),
  ('DOW-UAP-PR022', 'ready_to_publish', 2012, 0),
  ...（以下 2013〜2089 / 2090〜2091）
  ('DOW-UAP-PR052', 'ready_to_publish', 2090, 0),
  ('DOW-UAP-PR070', 'ready_to_publish', 2091, 0);

-- PR066 は Codex iter3 PASS 後に追加:
-- INSERT INTO articles (slug, status, publish_order, blocked)
--   VALUES ('DOW-UAP-PR066', 'ready_to_publish', 2058, 0);
```

### 注記

- PR066（2058）は **iter3 PASS 後に別途追加** する。先行投入するか後追い投入するかを判断する。
- 公開実行は workflow.db 登録完了 + `blocked = 0` を確認後。
- `publish_order` 順に Mac mini 側で自動公開または手動公開。

---

## 6. Review Package 生成予定一覧

**生成対象：** 78件（PR066 は Codex iter3 PASS 後）  
**生成タイミング：** workflow.db 登録・source_registry 更新後（本 dry-run では未実行）

### 生成形式

```
review_packages/
  R02-010_DOW-UAP-PR019_Unresolved_UAP_Middle_East_May_2022/
    article.md       (note_draft コピー)
    frame.png        (代表フレーム)
    metadata.json    (article_id / publish_order / Codex audit ref)
  R02-011_DOW-UAP-PR021_.../
  ...
  R02-091_DOW-UAP-PR070_.../
```

### 特記事項

- PR066（R02-058）Codex iter3 PASS 確認済み（2026-06-21）。Review Package 生成対象に含む。
- PR071（R02-062）正規ドラフトA（`ai_summary_DOW-UAP-PR071_..._Lake_Huron_note_version.md`）を使用した Review Package を生成する。ドラフトB は `note_drafts/archive/` に移動済み（2026-06-21）。

---

## 7. Finder 表示対象一覧（note.com 公開作業用）

公開作業時に Finder で開くべきファイル（公開順）:

### 最初の5件（publish_order 2010〜2014）

| pub_order | 開くファイル | 用途 |
|---|---|---|
| 2010 | `note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md` | 記事本文 |
| 2010 | `thumbnails/DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022/frame_0005.png` | アイキャッチ画像候補 |
| 2011 | `note_drafts/ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md` | 記事本文 |
| 2011 | `thumbnails/DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022/frame_0005.png` | アイキャッチ画像候補 |
| ... | ... | ... |

### PR066（⛔ 修正完了後に追加）

| pub_order | 開くファイル | 用途 |
|---|---|---|
| 2058（保留） | `note_drafts/ai_summary_DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024_note_version.md` | 修正 + iter3 後 |

### PR071（ドラフトA 正規版・2026-06-21 確定）

| pub_order | 開くファイル | 用途 |
|---|---|---|
| 2062 | `note_drafts/ai_summary_DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron_note_version.md` | 記事本文（ドラフトA・正規版） |
| 2062 | `thumbnails/DOW-UAP-PR071_USAF_ANG_F-16C_callsign_CALLSIGN_Shoots_Down_UAP_over_Lake_Huron_with_Weapon_System_12/frame_0020.png` | アイキャッチ画像候補（長名dir・代表フレーム） |

---

## 8. 投入前作業チェックリスト

### ⛔ 必須（投入前に完了が必要）

- [x] **PR066（R02-058）** 作業メモ行削除 → Codex iter3 PASS 確認（2026-06-21 完了）
- [x] **PR071（R02-062）** 正規ドラフトA確定 + ドラフトB を `note_drafts/archive/` に移動（2026-06-21 完了）

### ⚠️ 推奨（投入前に対応）

- [x] **PR060（R02-052）** Codex iter2 PASS 確認（2026-06-21 完了 / BLOCK: 0 / WARN: 0）
- [ ] **PR065（R02-057）** thumbnail 短名dir（`DOW-UAP-PR065/`）の扱い決定（アーカイブ / 削除）
- [ ] **PR071（R02-062）** thumbnail 短名dir（`DOW-UAP-PR071/`）の扱い決定（アーカイブ / 削除）

### ✅ 実行コマンド（dry-run 完了後・実際の投入時）

```bash
# 1. source_registry.csv 更新（78件分 CSV 追記）
# → scripts/ 内の登録スクリプトを実行予定（未実装）

# 2. workflow.db 更新（78件分 INSERT）
# → scripts/migrate_workflow_db_v1_2.py または INSERT 直接実行

# 3. 76件のドラフトフッター更新（⚠️ → 📋）
# → note_drafts/ の各ファイルの末尾フッターを article_id 採番済み形式に変換

# 4. Review Package 生成
# → scripts/generate_review_package_from_codex.py で一括生成

# 5. Mac mini 側への転送（別途）
```

---

## 9. 最終確認

| 確認項目 | 状態 |
|---|---|
| **対象件数 78件** | **✅ 確認済み** |
| **article_id 重複なし** | **✅ 確認済み** |
| **#2_XXX 重複なし** | **✅ 確認済み** |
| **publish_order 重複なし** | **✅ 確認済み** |
| **note_draft 欠落なし** | **✅ 確認済み（PR071 ドラフトA正規確定・ドラフトBはarchive・2026-06-21）** |
| **Codex 最終 PASS** | **✅ 78件完了（PR066 iter3・PR071 iter3・PR060 iter2 PASS 2026-06-21）** |
| **thumbnail 欠落なし** | **✅ 確認済み（PR065/PR071 短名dir整理推奨・投入ブロックなし）** |
| **公開キュー投入可能** | **✅ 78件すべて投入可能（任意残課題: PR065・PR071 thumbnail短名dir整理のみ）** |

---

**出力ファイル：** `review_reports/release02_vid_publish_queue_dry_run.md`  
**作成：** 2026-06-21（dry-run）  
**次工程：** PR066 作業メモ削除 → Codex iter3 → 全78件 source_registry / workflow.db 更新 → Review Package 生成
