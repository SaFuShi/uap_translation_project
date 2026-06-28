# Release 02 VID note公開ワークフロー

**作成日：** 2026-06-23  
**対象：** DOW-UAP / FBI-UAP VID 78件（#2_010〜#2_091、欠番 #2_047〜050）  
**公開ツール：** note.com（手動投稿）+ post_publish_workflow.py（公開後処理）  
**ステータス：** 公開前準備中（まだ公開しない）

---

## 0. 公開開始前の必須チェック

### 0-A. ⛔ 公開ブロッカー：ドラフト title/footer 未更新（73件）

**現状：** 78件のうち **73件** のドラフトに `#TBD` タイトルと `⚠️ source_registry 未登録` フッターが残存。  
note に貼り付けるとタイトルが `【概要版#TBD】` のまま公開されてしまう。

| 状態 | 件数 | 内容 |
|---|---|---|
| ✅ 更新済み | 5件 | PR052, PR060, PR066, PR070, PR071（直近セッションで更新） |
| ⛔ 未更新 | 73件 | PR019〜049（27件）/ FBI-PR001〜006（6件）/ PR053〜069（15件）/ PR071〜099（28件）の大半 |

**対応方針：** 公開前に一括バッチ更新が必要。  
→ `scripts/local_ops/draft_title_footer_batch_update.py` の実装を推奨（後述 §0-B）  
→ または手動で1件ずつ更新してから公開する

### ドラフト更新の内容（1件あたり）

**更新1：タイトル行**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR019：...
変更後: # 【概要版#R02-010】DoW DOW-UAP-PR019：...
```

**更新2：フッター**
```
変更前:
⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。公開前に source_registry への登録が必要です。

変更後:
📋 **article_id：R02-010 / #2_010 / publish_order: 2010**（2026-06-23 正式採番）  
source_registry.csv への登録は公開キュー投入時に実施予定です。
```

### 0-B. バッチ更新スクリプト（提案・未実装）

`scripts/local_ops/draft_title_footer_batch_update.py`

```python
"""
目的: 78件のドラフトを一括でタイトル・フッター更新する
入力: --numbering-plan review_reports/release02_numbering_plan.md
      --dry-run （確認のみ・実際には変更しない）
出力: 変更ファイル一覧を stdout に表示

処理:
  1. numbering_plan から PR番号 → article_id / #2_XXX / publish_order マップを生成
  2. note_drafts/ から対応ドラフトを glob で取得
  3. `#TBD` / `#2_TBD` を `#R02-XXX` に置換（タイトル行のみ）
  4. `⚠️ **source_registry 未登録：**` ブロックを 📋 article_id フッターに置換
  5. --dry-run 時は変更なし（差分表示のみ）

安全方針:
  - workflow.db / source_registry.csv / files_catalog.csv は変更しない
  - git 操作なし
  - note_drafts/archive/ は対象外
"""
```

実装が完了するまでの間は、1件ずつ手動更新してから公開する。

---

### 0-C. 任意残課題（非ブロッカー）

| 項目 | 内容 | 対応時期 |
|---|---|---|
| PR065 thumbnail 短名dir | `thumbnails/DOW-UAP-PR065/`（短名）が存在 | 公開後でも可 |
| PR071 thumbnail 短名dir | `thumbnails/DOW-UAP-PR071/`（短名）が存在 | 公開後でも可 |
| source_registry.csv 登録 | 78件分未登録 | post_publish_workflow 後に実施 |
| workflow.db 更新 | 78件分未登録 | post_publish_workflow 後に実施 |

---

## 1. 公開対象一覧（78件）

| pub_order | PR | article_id | #2_XXX | ドラフトファイル（note_drafts/ 以下） |
|---|---|---|---|---|
| 2010 | PR019 | R02-010 | #2_010 | ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md |
| 2011 | PR021 | R02-011 | #2_011 | ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md |
| 2012 | PR022 | R02-012 | #2_012 | ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_note_version.md |
| 2013 | PR023 | R02-013 | #2_013 | ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_note_version.md |
| 2014 | PR026 | R02-014 | #2_014 | ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md |
| 2015 | PR027 | R02-015 | #2_015 | ai_summary_DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md |
| 2016 | PR028 | R02-016 | #2_016 | ai_summary_DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024_note_version.md |
| 2017 | PR029 | R02-017 | #2_017 | ai_summary_DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024_note_version.md |
| 2018 | PR031 | R02-018 | #2_018 | ai_summary_DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024_note_version.md |
| 2019 | PR032 | R02-019 | #2_019 | ai_summary_DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024_note_version.md |
| 2020 | PR033 | R02-020 | #2_020 | ai_summary_DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024_note_version.md |
| 2021 | PR034 | R02-021 | #2_021 | ai_summary_DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023_note_version.md |
| 2022 | PR035 | R02-022 | #2_022 | ai_summary_DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023_note_version.md |
| 2023 | PR036 | R02-023 | #2_023 | ai_summary_DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020_note_version.md |
| 2024 | PR037 | R02-024 | #2_024 | ai_summary_DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020_note_version.md |
| 2025 | PR038 | R02-025 | #2_025 | ai_summary_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_note_version.md |
| 2026 | PR039 | R02-026 | #2_026 | ai_summary_DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020_note_version.md |
| 2027 | PR040 | R02-027 | #2_027 | ai_summary_DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020_note_version.md |
| 2028 | PR041 | R02-028 | #2_028 | ai_summary_DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020_note_version.md |
| 2029 | PR042 | R02-029 | #2_029 | ai_summary_DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020_note_version.md |
| 2030 | PR043 | R02-030 | #2_030 | ai_summary_DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025_note_version.md |
| 2031 | PR044 | R02-031 | #2_031 | ai_summary_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_note_version.md |
| 2032 | PR045 | R02-032 | #2_032 | ai_summary_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_note_version.md |
| 2033 | PR046 | R02-033 | #2_033 | ai_summary_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md |
| 2034 | PR047 | R02-034 | #2_034 | ai_summary_DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023_note_version.md |
| 2035 | PR048 | R02-035 | #2_035 | ai_summary_DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md |
| 2036 | PR049 | R02-036 | #2_036 | ai_summary_DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026_note_version.md |
| 2037 | FBI-PR001 | R02-037 | #2_037 | ai_summary_FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021_note_version.md |
| 2038 | FBI-PR002 | R02-038 | #2_038 | ai_summary_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_note_version.md |
| 2039 | FBI-PR003 | R02-039 | #2_039 | ai_summary_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_note_version.md |
| 2040 | FBI-PR004 | R02-040 | #2_040 | ai_summary_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_note_version.md |
| 2041 | FBI-PR005 | R02-041 | #2_041 | ai_summary_FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023_note_version.md |
| 2042 | FBI-PR006 | R02-042 | #2_042 | ai_summary_FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_United_States_Event_2023_note_version.md |
| 2043 | PR053 | R02-043 | #2_043 | ai_summary_DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22_note_version.md |
| 2044 | PR054 | R02-044 | #2_044 | ai_summary_DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022_note_version.md |
| 2045 | PR055 | R02-045 | #2_045 | ai_summary_DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020_note_version.md |
| 2046 | PR056 | R02-046 | #2_046 | ai_summary_DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN_note_version.md |
| 2051 | PR059 | R02-051 | #2_051 | ai_summary_DOW-UAP-PR059_NAG_UAP_1_Jun_20_note_version.md |
| 2052 | PR060 | R02-052 | #2_052 | ai_summary_DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_note_version.md |
| 2053 | PR061 | R02-053 | #2_053 | ai_summary_DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_note_version.md |
| 2054 | PR062 | R02-054 | #2_054 | ai_summary_DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_note_version.md |
| 2055 | PR063 | R02-055 | #2_055 | ai_summary_DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2_note_version.md |
| 2056 | PR064 | R02-056 | #2_056 | ai_summary_DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017_note_version.md |
| 2057 | PR065 | R02-057 | #2_057 | ai_summary_DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024_note_version.md |
| 2058 | PR066 | R02-058 | #2_058 | ai_summary_DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024_note_version.md |
| 2059 | PR067 | R02-059 | #2_059 | ai_summary_DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_of_water_note_version.md |
| 2060 | PR068 | R02-060 | #2_060 | ai_summary_DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_Phenomenon_UAP_captured_by_fif_note_version.md |
| 2061 | PR069 | R02-061 | #2_061 | ai_summary_DOW-UAP-PR069_F_A-18_FLIR_UAP_note_version.md |
| 2062 | PR071 | R02-062 | #2_062 | ai_summary_DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron_note_version.md |
| 2063 | PR072 | R02-063 | #2_063 | ai_summary_DOW-UAP-PR072_ADMINISTRATIVE_REVISION_IIR_1777_J0032_22_Kazakhstan_UAP_note_version.md |
| 2064 | PR073 | R02-064 | #2_064 | ai_summary_DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States_note_version.md |
| 2065 | PR074 | R02-065 | #2_065 | ai_summary_DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613_note_version.md |
| 2066 | PR075 | R02-066 | #2_066 | ai_summary_DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS_note_version.md |
| 2067 | PR076 | R02-067 | #2_067 | ai_summary_DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP_note_version.md |
| 2068 | PR077 | R02-068 | #2_068 | ai_summary_DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2_note_version.md |
| 2069 | PR078 | R02-069 | #2_069 | ai_summary_DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2_note_version.md |
| 2070 | PR079 | R02-070 | #2_070 | ai_summary_DOW-UAP-PR079_03_November_2020_CALLSIGN_Observes_and_tracks_Orb_UAP_note_version.md |
| 2071 | PR080 | R02-071 | #2_071 | ai_summary_DOW-UAP-PR080_17_SEP_2020_CALLSIGN_observes_UAP_note_version.md |
| 2072 | PR081 | R02-072 | #2_072 | ai_summary_DOW-UAP-PR081_29_AUG_2020_CALLSIGN_observes_UAP_note_version.md |
| 2073 | PR082 | R02-073 | #2_073 | ai_summary_DOW-UAP-PR082_21_September_2020_CALLSIGN_observes_UAP_note_version.md |
| 2074 | PR083 | R02-074 | #2_074 | ai_summary_DOW-UAP-PR083_13_June_2020_CALLSIGN_Mission_UAP_note_version.md |
| 2075 | PR084 | R02-075 | #2_075 | ai_summary_DOW-UAP-PR084_13_JUN_2020_CALLSIGN_Mission_UAP_part_2_note_version.md |
| 2076 | PR085 | R02-076 | #2_076 | ai_summary_DOW-UAP-PR085_16_Sept_2020_CALLSIGN_observes_UAP_note_version.md |
| 2077 | PR086 | R02-077 | #2_077 | ai_summary_DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast_note_version.md |
| 2078 | PR087 | R02-078 | #2_078 | ai_summary_DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP_note_version.md |
| 2079 | PR088 | R02-079 | #2_079 | ai_summary_DOW-UAP-PR088_31_AUG_CALLSIGN_Observes_UAP_note_version.md |
| 2080 | PR089 | R02-080 | #2_080 | ai_summary_DOW-UAP-PR089_31_AUG_CALLSIGN_Observes_UAP_part2_note_version.md |
| 2081 | PR090 | R02-081 | #2_081 | ai_summary_DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP_note_version.md |
| 2082 | PR091 | R02-082 | #2_082 | ai_summary_DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf_note_version.md |
| 2083 | PR092 | R02-083 | #2_083 | ai_summary_DOW-UAP-PR092_08_AUG_2020_CALLSIGN_UAP_observation_note_version.md |
| 2084 | PR093 | R02-084 | #2_084 | ai_summary_DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_Dual_UAP_short_note_version.md |
| 2085 | PR094 | R02-085 | #2_085 | ai_summary_DOW-UAP-PR094_CALLSIGN_Mission_HD_2020-02-13_note_version.md |
| 2086 | PR095 | R02-086 | #2_086 | ai_summary_DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_Dual_UAP_long_note_version.md |
| 2087 | PR096 | R02-087 | #2_087 | ai_summary_DOW-UAP-PR096_HH11_03_July_2018_UAPs_note_version.md |
| 2088 | PR097 | R02-088 | #2_088 | ai_summary_DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_2135Z_note_version.md |
| 2089 | PR099 | R02-089 | #2_089 | ai_summary_DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_1715Z_note_version.md |
| 2090 | PR052 | R02-090 | #2_090 | ai_summary_DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission_note_version.md |
| 2091 | PR070 | R02-091 | #2_091 | ai_summary_DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP_note_version.md |

---

## 2. 1件あたりの公開手順（#2_010 = PR019 を例に）

### STEP 1: タイトル・フッター確認（公開前チェック）

Finder または エディタで以下を確認する：

```
note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md
```

確認項目：
- [ ] タイトル行が `# 【概要版#R02-010】` で始まっている（`#TBD` でないこと）
- [ ] フッターに `📋 **article_id：R02-010 / #2_010 / publish_order: 2010**` がある
- [ ] 「→ 使用ファイル：」という作業メモ行がないこと

Finder 表示コマンド（ターミナル）：
```bash
open -R "note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md"
```

### STEP 2: アイキャッチ画像の確認

```
thumbnails/DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022/frame_0005.png
```

Finder 表示コマンド：
```bash
open "thumbnails/DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022/"
```

使用する frame は `frame_0005.png`（各ドラフトの出典セクション参照）。

### STEP 3: note.com への投稿（手動）

1. note.com にログイン
2. 新規記事作成
3. ドラフト本文（`note_drafts/ai_summary_...md`）の内容をコピー＆ペースト
4. アイキャッチ画像を `thumbnails/.../frame_0005.png` などから設定
5. タグを設定（UAP / Release02 / 米国防省 など）
6. **公開前にプレビューで確認**
7. 公開ボタンを押す
8. 公開後の URL をコピー（例：`https://note.com/deft_ibis3303/n/XXXXXXXX`）

### STEP 4: post_publish_workflow.py の実行（公開後）

公開URLが確定したら以下を実行する：

```bash
python3 scripts/post_publish_workflow.py \
  --slug DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022 \
  --draft note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md \
  --note-url https://note.com/deft_ibis3303/n/XXXXXXXX \
  --audit review_reports/codex_audit_20260620_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_iter2.md
```

このスクリプトが生成するもの（実行後）：
- `published_articles/ai_summary_DOW-UAP-PR019_..._published_YYYYMMDD.md`（保存版）
- `logs/notebooklm/YYYY-MM-DD_DOW-UAP-PR019_..._published_log.md`（ログ）
- git add / commit / push コマンド案（表示のみ・未実行）
- source_registry 更新候補（表示のみ・自動変更なし）

### STEP 5: git commit（公開後・任意タイミング）

post_publish_workflow.py が表示した git コマンドを確認・実行する：

```bash
git add published_articles/ai_summary_DOW-UAP-PR019_..._published_YYYYMMDD.md \
        logs/notebooklm/YYYY-MM-DD_DOW-UAP-PR019_..._published_log.md
git commit -m "publish: add DOW-UAP-PR019 article archive and log"
git push origin main
```

### STEP 6: 次の記事へ

`#2_011`（PR021）を同じ手順で実施する。

---

## 3. #2_010（PR019）の公開に必要なファイル一覧

| 種別 | パス |
|---|---|
| **記事ドラフト** | `note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md` |
| **Codex audit** | `review_reports/codex_audit_20260620_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_iter2.md` |
| **thumbnail dir** | `thumbnails/DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022/` |
| **アイキャッチ候補** | `thumbnails/DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022/frame_0005.png` |

**事前に必要な手動更新（現在 #TBD のため）：**

| 更新箇所 | 変更前 | 変更後 |
|---|---|---|
| タイトル | `# 【概要版#TBD】` | `# 【概要版#R02-010】` |
| フッター | `⚠️ **source_registry 未登録：**...` | `📋 **article_id：R02-010 / #2_010 / publish_order: 2010**（2026-06-23 正式採番）` |

---

## 4. post_publish_workflow.py 引数マッピング（全78件）

| pub_order | PR | slug（--slug 引数） | audit ファイル |
|---|---|---|---|
| 2010 | PR019 | `DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022` | `codex_audit_20260620_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_iter2.md` |
| 2011 | PR021 | `DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022` | `codex_audit_20260620_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_iter2.md` |
| 2012 | PR022 | `DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022` | `codex_audit_20260620_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_iter2.md` |
| 2013 | PR023 | `DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022` | `codex_audit_20260620_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_iter2.md` |
| 2014 | PR026 | `DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023` | `codex_audit_20260620_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_iter2.md` |
| 2015 | PR027 | `DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023` | `codex_audit_20260620_DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_iter2.md` |
| 2016 | PR028 | `DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024` | `codex_audit_20260620_DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024_iter2.md` |
| 2017 | PR029 | `DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024` | `codex_audit_20260620_DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024_iter2.md` |
| 2018 | PR031 | `DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024` | `codex_audit_20260620_DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024_iter2.md` |
| 2019 | PR032 | `DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024` | `codex_audit_20260620_DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024_iter2.md` |
| 2020 | PR033 | `DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024` | `codex_audit_20260620_DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024_iter2.md` |
| 2021 | PR034 | `DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023` | `codex_audit_20260620_DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023_iter2.md` |
| 2022 | PR035 | `DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023` | `codex_audit_20260620_DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023_iter3.md` |
| 2023 | PR036 | `DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020` | `codex_audit_20260620_DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020_iter2.md` |
| 2024 | PR037 | `DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020` | `codex_audit_20260620_DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020_iter2.md` |
| 2025 | PR038 | `DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013` | `codex_audit_20260620_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_iter3.md` |
| 2026 | PR039 | `DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020` | `codex_audit_20260620_DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020_iter2.md` |
| 2027 | PR040 | `DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020` | `codex_audit_20260620_DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020_iter2.md` |
| 2028 | PR041 | `DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020` | `codex_audit_20260620_DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020_iter2.md` |
| 2029 | PR042 | `DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020` | `codex_audit_20260620_DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020_iter2.md` |
| 2030 | PR043 | `DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025` | `codex_audit_20260620_DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025_iter2.md` |
| 2031 | PR044 | `DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020` | `codex_audit_20260620_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_iter2.md` |
| 2032 | PR045 | `DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020` | `codex_audit_20260620_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_iter2.md` |
| 2033 | PR046 | `DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024` | `codex_audit_20260620_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_iter2.md` |
| 2034 | PR047 | `DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023` | `codex_audit_20260620_DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023_iter2.md` |
| 2035 | PR048 | `DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024` | `codex_audit_20260620_DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024_iter2.md` |
| 2036 | PR049 | `DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026` | `codex_audit_20260620_DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026_iter2.md` |
| 2037〜2042 | FBI-PR001〜006 | `FBI-UAP-PR001_...` 〜 `FBI-UAP-PR006_...` | 各 iter3.md |
| 2043〜2061 | PR053〜069 | 各スラッグ | 各 iter_最新.md |
| 2062〜2089 | PR071〜099 | 各スラッグ | 各 iter_最新.md |
| 2090 | PR052 | `DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission` | `codex_audit_20260621_DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission_iter2.md` |
| 2091 | PR070 | `DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP` | `codex_audit_20260620_DOW-UAP-PR070_..._iter3.md` |

---

## 5. 未対応素材（Release 02 VID 以外）

公開キュー対象外だが存在する素材。今回は後回し。

| 種別 | 内容 | 状態 |
|---|---|---|
| PDF / IMG | Release 02 PDF/画像素材 | ドラフト作成未着手 |
| HOLD VID | PR057/PR057a/PR057b（Yellow Sea）/ PR058（INDOPACOM） | HOLD中（MD5重複等） |
| SKIP VID | PR098（1056秒超長尺） | SKIP確定 |
| Release 03 | files_catalog.csv に存在する新規素材 | 未着手 |

---

## 6. 公開フロー全体図

```
[公開前準備]
  ① ドラフト title/footer バッチ更新（73件・⛔ 必須）
     → scripts/local_ops/draft_title_footer_batch_update.py（未実装）
     → または手動で1件ずつ更新してから公開

[1件ごとの公開ループ（#2_010 → #2_091）]
  ② STEP 1: ドラフト確認（タイトル・フッター・作業メモ行）
  ③ STEP 2: アイキャッチ画像確認（thumbnails/...）
  ④ STEP 3: note.com 手動投稿
  ⑤ STEP 4: post_publish_workflow.py 実行（公開URL引数に渡す）
  ⑥ STEP 5: git commit（published_articles/ + logs/）

[公開後一括処理]
  ⑦ source_registry.csv 78件分更新
  ⑧ workflow.db 78件分更新
  ⑨ Mac mini pull
```

---

## 7. 公開開始可否の判定

| 判定項目 | 状態 |
|---|---|
| DONE_CANDIDATE 78件確定 | ✅ |
| 必須ブロッカー（Codex BLOCK） | ✅ なし |
| ⛔ **ドラフト title/footer 更新（73件）** | **⛔ 未完了** |
| 任意残課題（thumbnail短名dir整理） | ⚠️ 後回し可 |

**結論：⛔ 公開開始にはドラフト更新（73件）が必要**  
バッチスクリプトまたは手動更新が完了したら公開開始可能。
