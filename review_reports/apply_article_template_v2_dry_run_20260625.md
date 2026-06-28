# apply_article_template.py — DRY-RUNレポート

**実行日：** 2026-06-24  
**モード：** DRY-RUN  
**対象ディレクトリ：** `note_drafts/`  

## サマリー

| 項目 | 件数 |
|---|---|
| 対象ファイル総数 | 78 |
| 修正予定ファイル数 | 78 |
| 修正不要ファイル数（既準拠） | 0 |
| エラー | 0 |
| AUTO変換延べ件数 | 331 |
| AUTO_SKELETON延べ件数 | 0 |
| 手動確認必要延べ件数 | 0 |

> ⚠️ **DRY-RUNモード**：ファイルは変更されていません。
> `--execute` で実行すると上記件数のファイルが修正されます（.bakバックアップ付き）。

## 変換内容別集計

| 変換ID | 変換名 | AUTO/SKELETON | SKIPPED | MANUAL_NOTE |
|---|---|---|---|---|
| T01 | タイトルID #R02→#2 | 0 | 78 | 0 |
| T02 | Release Date ・Release 02追加 | 0 | 78 | 0 |
| T03 | 画像プレースホルダー ▼【画像】 | 0 | 78 | 0 |
| T04 | 目視確認注釈 | 0 | 78 | 0 |
| T05 | ファイル名由来注釈 | 0 | 78 | 0 |
| T06+T07 | ffprobe形式変換+intro追加 | 0 | 78 | 0 |
| T12 | ffprobe残留パイプ修正 [v2] | 37 | 41 | 0 |
| T08 | ## 注意点 スケルトン | 0 | 78 | 0 |
| T09 | 掲載画像出典統一 | 0 | 78 | 0 |
| T10 | ディスクレイマー3段落展開 | 0 | 78 | 0 |
| T11 | 語尾統一（です・ます調） | 0 | 78 | 0 |
| T13 | ▲キャプション丁寧体変換 [v2] | 76 | 2 | 0 |
| T14 | DVIDS IDメタデータ統一 [v2] | 77 | 1 | 0 |
| T15 | DVIDS IDファイル名由来統一 [v2] | 75 | 3 | 0 |
| T16 | AI解析メモタイムコード変換 [v2] | 17 | 61 | 0 |
| T17 | セパレータ追加（注意点→出典） [v2] | 49 | 29 | 0 |

## 手動確認が必要な項目

なし

## 全ファイル変換サマリー

| スラグ | AUTO | SKEL | MANUAL | SKIP | 修正予定 |
|---|---|---|---|---|---|
| `DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022` | 6 | 0 | 0 | 10 | ✅ 修正 |
| `DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022` | 6 | 0 | 0 | 10 | ✅ 修正 |
| `DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024` | 6 | 0 | 0 | 10 | ✅ 修正 |
| `DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024` | 6 | 0 | 0 | 10 | ✅ 修正 |
| `DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020` | 6 | 0 | 0 | 10 | ✅ 修正 |
| `DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020` | 6 | 0 | 0 | 10 | ✅ 修正 |
| `DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR050_4_UAP_Formation_Iran` | 1 | 0 | 0 | 15 | ✅ 修正 |
| `DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22` | 2 | 0 | 0 | 14 | ✅ 修正 |
| `DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR059_NAG_UAP_1_Jun_20` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024` | 2 | 0 | 0 | 14 | ✅ 修正 |
| `DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_of_water` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_Phenomenon_UAP_captured_by_fif` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR069_F_A-18_FLIR_UAP` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP` | 3 | 0 | 0 | 13 | ✅ 修正 |
| `DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron` | 2 | 0 | 0 | 14 | ✅ 修正 |
| `DOW-UAP-PR072_ADMINISTRATIVE_REVISION_IIR_1777_J0032_22_Kazakhstan_UAP` | 6 | 0 | 0 | 10 | ✅ 修正 |
| `DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS` | 6 | 0 | 0 | 10 | ✅ 修正 |
| `DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAPs` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR080_20_October_2020_CALLSIGN_CALLSIGN_Observes_UAP` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP_AFRICOM` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP_AFRICOM` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR084_17_Sept_2020_CALLSIGN_observes_UAP` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR085_16_Sept_2020_CALLSIGN_observes_UAP` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR088_31_AUG_CALLSIGN_Observes_UAP` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR089_31_AUG_CALLSIGN_Observes_UAP_part2` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR092_08_AUG_2020_CALLSIGN_UAP_observation` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_Dual_UAP_short` | 6 | 0 | 0 | 10 | ✅ 修正 |
| `DOW-UAP-PR094_CALLSIGN_Mission_HD_2020-02-13` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_Dual_UAP_long` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR096_HH11_03_July_2018_UAPs` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_2135Z` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_1715Z` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `FBI-UAP-PR003_Orbs_Over_the_Pond_2024` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `FBI-UAP-PR004_Northeastern_Orb_Sighting_2025` | 5 | 0 | 0 | 11 | ✅ 修正 |
| `FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023` | 4 | 0 | 0 | 12 | ✅ 修正 |
| `FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_United_States_Event_2023` | 3 | 0 | 0 | 13 | ✅ 修正 |

## ファイル別変換詳細

### `DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006059`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006059`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（3フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05・00:10）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006060`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006060`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（3フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05・00:10）`

### `DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006062`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006062`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（3フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05・00:10）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006063`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006063`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006067`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006067`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006073`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006073`

### `DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006074`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006074`

### `DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006076`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006076`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（2フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006078`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006078`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（2フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006079`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006079`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（2フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05）`

### `DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006080`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006080`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006082`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006082`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（5フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05・00:10・00:15・00:20）`

### `DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006083`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006083`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006087`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006087`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（2フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006088`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006088`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006089`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006089`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（2フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006093`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006093`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006094`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006094`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006097`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006097`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006159`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006159`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（3フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05・00:10）`

### `DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006104`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006104`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006105`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006105`

### `DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006106`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006106`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（2フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05）`

### `DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006107`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006107`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006110`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006110`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1006111`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1006111`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR050_4_UAP_Formation_Iran`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**

### `DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007708`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007708`

### `DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`

### `DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007711`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007711`

### `DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007713`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007713`

### `DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007718`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007718`

### `DOW-UAP-PR059_NAG_UAP_1_Jun_20`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007727`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007727`

### `DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007734`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007734`

### `DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007735`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007735`

### `DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007739`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007739`

### `DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007740`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007740`

### `DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007741`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007741`

### `DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024`
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007777`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007777`

### `DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007778`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007778`

### `DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_of_water`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007779`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007779`

### `DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_Phenomenon_UAP_captured_by_fif`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007780`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007780`

### `DOW-UAP-PR069_F_A-18_FLIR_UAP`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007781`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007781`

### `DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007783`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007783`

### `DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`

### `DOW-UAP-PR072_ADMINISTRATIVE_REVISION_IIR_1777_J0032_22_Kazakhstan_UAP`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007788`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007788`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（4フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05・00:10・00:15）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007790`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007790`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（3フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:30・01:00）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007791`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007791`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007795`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007795`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（5フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05・00:10・00:15・00:20）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007804`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007804`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007809`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007809`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007812`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007812`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAPs`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007816`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007816`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR080_20_October_2020_CALLSIGN_CALLSIGN_Observes_UAP`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007803`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007803`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP_AFRICOM`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007805`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007805`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP_AFRICOM`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007807`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007807`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007808`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007808`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR084_17_Sept_2020_CALLSIGN_observes_UAP`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007810`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007810`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR085_16_Sept_2020_CALLSIGN_observes_UAP`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007796`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007796`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007797`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007797`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007799`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007799`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR088_31_AUG_CALLSIGN_Observes_UAP`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007800`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007800`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR089_31_AUG_CALLSIGN_Observes_UAP_part2`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007712`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007712`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007719`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007719`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007716`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007716`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR092_08_AUG_2020_CALLSIGN_UAP_observation`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007715`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007715`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_Dual_UAP_short`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007721`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007721`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（4フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05・00:10・00:15・00:20・00:25・00:30）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR094_CALLSIGN_Mission_HD_2020-02-13`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007722`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007722`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_Dual_UAP_long`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007725`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007725`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR096_HH11_03_July_2018_UAPs`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007726`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007726`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（3フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:30・01:00）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_2135Z`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007728`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007728`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_1715Z`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1007738`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1007738`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：24fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：24fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1010263`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1010263`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1010264`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1010264`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `FBI-UAP-PR003_Orbs_Over_the_Pond_2024`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1010267`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1010267`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `FBI-UAP-PR004_Northeastern_Orb_Sighting_2025`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1010269`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1010269`
- 🔧 [T16] **AI解析メモ タイムコード変換**
  - 変更前: `映像フレーム目視確認済み（2フレーム）`
  - 変更後: `映像フレーム目視確認済み（00:00・00:05・00:10・00:15・00:20・00:25・00:30・00:35・00:40・00:45）`
- 🔧 [T17] **セパレータ追加（注意点→出典）**
  - 変更前: `↩↩## 出典↩`
  - 変更後: `↩↩---↩↩## 出典↩`

### `FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T13] **▲キャプション丁寧体変換（1行）**
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1010272`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1010272`

### `FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_United_States_Event_2023`
- 🔧 [T12] **ffprobe残留パイプ修正**
  - 変更前: `- 解像度：1920×1080（FHD）| フレームレート：30fps・アスペクト比 16:9）`
  - 変更後: `- 解像度：1920×1080（FHD・アスペクト比 16:9）↩- フレームレート：30fps`
- 🔧 [T14] **DVIDS ID メタデータ統一**
  - 変更前: `（DVIDS＝国防映像情報配信サービス）`
  - 変更後: `（DoW/DVIDS管理番号）`
- 🔧 [T15] **DVIDS ID ファイル名由来 統一**
  - 変更前: `- DVIDS ID：1010276`
  - 変更後: `- DVIDS ID（DoW/DVIDS管理番号）：1010276`

