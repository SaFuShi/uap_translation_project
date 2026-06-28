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
| AUTO変換延べ件数 | 642 |
| AUTO_SKELETON延べ件数 | 49 |
| 手動確認必要延べ件数 | 0 |

> ⚠️ **DRY-RUNモード**：ファイルは変更されていません。
> `--execute` で実行すると上記件数のファイルが修正されます（.bakバックアップ付き）。

## 変換内容別集計

| 変換ID | 変換名 | AUTO/SKELETON | SKIPPED | MANUAL_NOTE |
|---|---|---|---|---|
| T01 | タイトルID #R02→#2 | 77 | 1 | 0 |
| T02 | Release Date ・Release 02追加 | 59 | 19 | 0 |
| T03 | 画像プレースホルダー ▼【画像】 | 77 | 1 | 0 |
| T04 | 目視確認注釈 | 77 | 1 | 0 |
| T05 | ファイル名由来注釈 | 69 | 9 | 0 |
| T06+T07 | ffprobe形式変換+intro追加 | 68 | 10 | 0 |
| T08 | ## 注意点 スケルトン | 49 | 29 | 0 |
| T09 | 掲載画像出典統一 | 78 | 0 | 0 |
| T10 | ディスクレイマー3段落展開 | 59 | 19 | 0 |
| T11 | 語尾統一（です・ます調） | 78 | 0 | 0 |

## 手動確認が必要な項目

なし

## 全ファイル変換サマリー

| スラグ | AUTO | SKEL | MANUAL | SKIP | 修正予定 |
|---|---|---|---|---|---|
| `DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022` | 9 | 0 | 0 | 1 | ✅ 修正 |
| `DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024` | 9 | 0 | 0 | 1 | ✅ 修正 |
| `DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024` | 9 | 0 | 0 | 1 | ✅ 修正 |
| `DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024` | 9 | 0 | 0 | 1 | ✅ 修正 |
| `DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023` | 9 | 0 | 0 | 1 | ✅ 修正 |
| `DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025` | 9 | 0 | 0 | 1 | ✅ 修正 |
| `DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020` | 9 | 0 | 0 | 1 | ✅ 修正 |
| `DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024` | 9 | 0 | 0 | 1 | ✅ 修正 |
| `DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR050_4_UAP_Formation_Iran` | 2 | 0 | 0 | 8 | ✅ 修正 |
| `DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission` | 7 | 0 | 0 | 3 | ✅ 修正 |
| `DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22` | 5 | 0 | 0 | 5 | ✅ 修正 |
| `DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022` | 5 | 0 | 0 | 5 | ✅ 修正 |
| `DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020` | 5 | 0 | 0 | 5 | ✅ 修正 |
| `DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN` | 5 | 0 | 0 | 5 | ✅ 修正 |
| `DOW-UAP-PR059_NAG_UAP_1_Jun_20` | 5 | 0 | 0 | 5 | ✅ 修正 |
| `DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2` | 5 | 0 | 0 | 5 | ✅ 修正 |
| `DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0` | 6 | 0 | 0 | 4 | ✅ 修正 |
| `DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1` | 7 | 0 | 0 | 3 | ✅ 修正 |
| `DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2` | 7 | 0 | 0 | 3 | ✅ 修正 |
| `DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017` | 5 | 0 | 0 | 5 | ✅ 修正 |
| `DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024` | 7 | 0 | 0 | 3 | ✅ 修正 |
| `DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024` | 7 | 0 | 0 | 3 | ✅ 修正 |
| `DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_of_water` | 7 | 0 | 0 | 3 | ✅ 修正 |
| `DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_Phenomenon_UAP_captured_by_fif` | 7 | 0 | 0 | 3 | ✅ 修正 |
| `DOW-UAP-PR069_F_A-18_FLIR_UAP` | 7 | 0 | 0 | 3 | ✅ 修正 |
| `DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP` | 7 | 0 | 0 | 3 | ✅ 修正 |
| `DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron` | 5 | 0 | 0 | 5 | ✅ 修正 |
| `DOW-UAP-PR072_ADMINISTRATIVE_REVISION_IIR_1777_J0032_22_Kazakhstan_UAP` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAPs` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR080_20_October_2020_CALLSIGN_CALLSIGN_Observes_UAP` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP_AFRICOM` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP_AFRICOM` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR084_17_Sept_2020_CALLSIGN_observes_UAP` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR085_16_Sept_2020_CALLSIGN_observes_UAP` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR088_31_AUG_CALLSIGN_Observes_UAP` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR089_31_AUG_CALLSIGN_Observes_UAP_part2` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR092_08_AUG_2020_CALLSIGN_UAP_observation` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_Dual_UAP_short` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR094_CALLSIGN_Mission_HD_2020-02-13` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_Dual_UAP_long` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR096_HH11_03_July_2018_UAPs` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_2135Z` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_1715Z` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `FBI-UAP-PR003_Orbs_Over_the_Pond_2024` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `FBI-UAP-PR004_Northeastern_Orb_Sighting_2025` | 9 | 1 | 0 | 0 | ✅ 修正 |
| `FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023` | 9 | 0 | 0 | 1 | ✅ 修正 |
| `FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_United_States_Event_2023` | 9 | 0 | 0 | 1 | ✅ 修正 |

## ファイル別変換詳細

### `DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-011】`
  - 変更後: `# 【概要版#2_011】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR021 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR02...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Iraq」「May 20...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-012】`
  - 変更後: `# 【概要版#2_012】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR022 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR02...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022/frame_0005.png（00:`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022.mp4 より抽出（00:05時点・3分割表示が確認できるフ`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Syria」「July ...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-013】`
  - 変更後: `# 【概要版#2_013】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR023 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR02...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Iraq」「Decemb...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-014】`
  - 変更後: `# 【概要版#2_014】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR026 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR02...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023/`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023.mp4 より抽出（約0`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「United Arab ...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-015】`
  - 変更後: `# 【概要版#2_015】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR027 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR02...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023/`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023.mp4 より抽出（約0`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-016】`
  - 変更後: `# 【概要版#2_016】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR028 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR02...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024.mp4 より抽出（00:00時点・2分割表示とオレ`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Greece」「Janu...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-017】`
  - 変更後: `# 【概要版#2_017】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR029 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR02...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024/fra`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024.mp4 より抽出（00:00`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「United Arab ...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-018】`
  - 変更後: `# 【概要版#2_018】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR031 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR03...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Syria」「Octob...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-019】`
  - 変更後: `# 【概要版#2_019】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR032 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR03...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Syria」「Octob...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-020】`
  - 変更後: `# 【概要版#2_020】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR033 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR03...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024/frame_0000.png（`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024.mp4 より抽出（00:00時点・赤い領域が確認でき`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Syria」「Octob...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-021】`
  - 変更後: `# 【概要版#2_021】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR034 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR03...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-022】`
  - 変更後: `# 【概要版#2_022】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR035 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR03...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023.mp4 より抽出（00:00時点・黒い点2つが確認`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Greece」「Octo...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-023】`
  - 変更後: `# 【概要版#2_023】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR036 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR03...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020/frame_0000.pn`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020.mp4 より抽出（00:00時点・グリーンライン`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-024】`
  - 変更後: `# 【概要版#2_024】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR037 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR03...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Middle East」...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-025】`
  - 変更後: `# 【概要版#2_025】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR038 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR03...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013/frame_0000.png（00`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013.mp4 より抽出（00:00時点・グレーUI・ビネット・`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-026】`
  - 変更後: `# 【概要版#2_026】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR039 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR03...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png（00`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020.mp4 より抽出（00:00時点・シアンクロスヘアとオレ`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Middle East」...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-027】`
  - 変更後: `# 【概要版#2_027】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR040 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR04...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-028】`
  - 変更後: `# 【概要版#2_028】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR041 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR04...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-029】`
  - 変更後: `# 【概要版#2_029】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR042 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR04...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png（00`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020.mp4 より抽出（00:00時点・ノイズと青い点マーカー`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-030】`
  - 変更後: `# 【概要版#2_030】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR043 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR04...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025/frame_0000.png（00:00時点`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025.mp4 より抽出（00:00時点・航空機窓枠状の弧と川地形が確認で`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「Africa」「Djib...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-031】`
  - 変更後: `# 【概要版#2_031】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR044 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR04...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png（00`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020.mp4 より抽出（00:00時点・黒い物体と赤矢印マーカ`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-032】`
  - 変更後: `# 【概要版#2_032】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR045 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR04...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png（00`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020.mp4 より抽出（00:00時点・グリーンフレームと大楕`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-033】`
  - 変更後: `# 【概要版#2_033】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR046 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR04...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024/frame_0000.png（00:0`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024.mp4 より抽出（00:00時点・白い翼状物体が確認できる代`
- 🔧 [T10] **ディスクレイマー 3段落展開**
  - 変更前: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。「INDOPACOM」「E...`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-034】`
  - 変更後: `# 【概要版#2_034】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR047 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR04...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023/frame_0000.png（00:0`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023.mp4 より抽出（00:00時点・赤い円形クロスヘアとグリー`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-035】`
  - 変更後: `# 【概要版#2_035】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR048 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR04...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024/frame_0000.png（00:0`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024.mp4 より抽出（00:00時点・風力発電機（風車）が確認で`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-036】`
  - 変更後: `# 【概要版#2_036】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR049 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR04...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026/frame_`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026.mp4 より抽出（00:00時点・`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR050_4_UAP_Formation_Iran`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR050/frame_0000.png（約0秒時点）`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR050_4_UAP_Formation_Iran.mp4 より抽出（約0秒時点）`
- 🔧 [T11] **語尾統一（4箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません、示すものではない→示すものではありません…`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-090】`
  - 変更後: `# 【概要版#2_090】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR052 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR05...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（00:00・01:00・02:00・03:00・04:00・05:00・06:00・07:00・08:00・60秒間隔・計9フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission/frame_0060.png（01:00時`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission.mp4 より抽出（01:00時点・編隊と黒塗り矩形が確認できるフ`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-043】`
  - 変更後: `# 【概要版#2_043】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR053 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR05...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0秒・5秒・10秒・15秒・20秒）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR053/frame_0005.png（5秒時点）`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22.mp4 より抽出（5秒時点）`
- 🔧 [T11] **語尾統一（4箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません、示すものではない→示すものではありません…`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-044】`
  - 変更後: `# 【概要版#2_044】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR054 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR05...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜210秒・30秒間隔の8フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022/fra`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022.mp4 より抽出（01:00`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-045】`
  - 変更後: `# 【概要版#2_045】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR055 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR05...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0秒・5秒・10秒・15秒・20秒・25秒・30秒・35秒・40秒・45秒）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020/`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020.mp4 より抽出（25`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-046】`
  - 変更後: `# 【概要版#2_046】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR056 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR05...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜210秒・30秒間隔の8フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN.mp4 より抽出（00:00時点・暗い球形物体と青`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR059_NAG_UAP_1_Jun_20`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-051】`
  - 変更後: `# 【概要版#2_051】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR059 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR05...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜270秒・30秒間隔の10フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR059_NAG_UAP_1_Jun_20/frame_0240.png（04:00時点・物体とシアンクロスヘアが最も明確`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR059_NAG_UAP_1_Jun_20.mp4 より抽出（04:00時点・物体とシアンクロスヘアが最も明確に確認できる代表フレーム）`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-052】`
  - 変更後: `# 【概要版#2_052】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR060 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR06...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜270秒・30秒間隔の10フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/frame_0030.png（0`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2.mp4 より抽出（00:30時点・クロスヘア状表示と地`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、区別できない→区別できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-053】`
  - 変更後: `# 【概要版#2_053】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR061 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR06...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜270秒・30秒間隔の10フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 注釈フレーズ追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0/frame_0060.png（0`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0.mp4 より抽出（01:00時点・クロスヘア状表示とシ`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、区別できない→区別できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-054】`
  - 変更後: `# 【概要版#2_054】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR062 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR06...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜270秒・30秒間隔の10フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/frame_0060.png（0`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1.mp4 より抽出（01:00時点・シアンマーカーと地形`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、区別できない→区別できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-055】`
  - 変更後: `# 【概要版#2_055】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR063 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR06...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜270秒・30秒間隔の10フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2/frame_0030.png（0`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2.mp4 より抽出（00:30時点・シアンクロスヘア状表`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、区別できない→区別できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-056】`
  - 変更後: `# 【概要版#2_056】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR064 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR06...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0秒・5秒・10秒・15秒）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017/frame_0005.png（5秒時点・追尾マーカーが確認でき`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017.mp4 より抽出（5秒時点・追尾マーカーが確認できる代表フレーム）`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-057】`
  - 変更後: `# 【概要版#2_057】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR065 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR06...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜35秒・5秒間隔の8フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024/fr`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024.mp4 より抽出（00:0`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-058】`
  - 変更後: `# 【概要版#2_058】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR066 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR06...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜45秒・5秒間隔の10フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024/fr`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024.mp4 より抽出（00:0`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_of_water`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-059】`
  - 変更後: `# 【概要版#2_059】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR067 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR06...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜270秒・30秒間隔の10フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_Phenomenon_UAP_captured_by_fif`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-060】`
  - 変更後: `# 【概要版#2_060】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR068 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR06...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜60秒・5秒間隔の10フレーム程度）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_Phenomenon_`
- 🔧 [T11] **語尾統一（3箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません、区別できない→区別できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR069_F_A-18_FLIR_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-061】`
  - 変更後: `# 【概要版#2_061】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR069 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR06...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜25秒・5秒間隔の6フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR069_F_A-18_FLIR_UAP/frame_0000.png（00:00時点・FLIR UIと画面上部の明るい点`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR069_F_A-18_FLIR_UAP.mp4 より抽出（00:00時点・FLIR UIと画面上部の明るい点が確認できる代表フレーム）`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-091】`
  - 変更後: `# 【概要版#2_091】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR070 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR07...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0〜25秒・5秒間隔の7フレーム）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_Unidentifi`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP.mp4 より抽出（00:10時点・`
- 🔧 [T11] **語尾統一（3箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません、区別できない→区別できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-062】`
  - 変更後: `# 【概要版#2_062】`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR071 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR07...`
- 🔧 [T04] **目視確認注釈 タイムコード付き→標準形**
  - 変更前: `以下は映像フレーム（0秒・5秒・10秒・15秒・20秒・25秒・30秒・35秒・40秒・45秒）の目視確認によるものです。`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR071_USAF_ANG_F-16C_callsign_CALLSIGN_Shoots_Down_UAP_over_La`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron.mp4 より抽出（20秒時点・追尾対象が最も明確に`
- 🔧 [T11] **語尾統一（2箇所）**
  - 変更前: `内容は本記事では扱わない→内容は本記事では扱いません、確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR072_ADMINISTRATIVE_REVISION_IIR_1777_J0032_22_Kazakhstan_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-063】`
  - 変更後: `# 【概要版#2_063】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR072 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR07...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR072_.../frame_0005.png（00:05時点・夜間カラー映像が確認できるフレーム）`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR072_ADMINISTRATIVE_REVISION_IIR_1777_J0032_22_Kazakhstan_UAP.mp4 より抽出（0`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-064】`
  - 変更後: `# 【概要版#2_064】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR073 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR07...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR073_.../frame_0030.png（00:30時点）`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States.mp4 より抽出（00`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-065】`
  - 変更後: `# 【概要版#2_065】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR074 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR07...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-066】`
  - 変更後: `# 【概要版#2_066】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR075 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR07...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS/frame_0000.pn`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-067】`
  - 変更後: `# 【概要版#2_067】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR076 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR07...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP/frame_0000`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-068】`
  - 変更後: `# 【概要版#2_068】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR077 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR07...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR077_.../frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2.mp4 より抽出（約0`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-069】`
  - 変更後: `# 【概要版#2_069】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR078 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR07...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR078_.../frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2.mp4 より抽出（約0`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAPs`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-070】`
  - 変更後: `# 【概要版#2_070】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR079 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR07...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR079_.../frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAPs.mp4 より`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR080_20_October_2020_CALLSIGN_CALLSIGN_Observes_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-071】`
  - 変更後: `# 【概要版#2_071】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR080 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR08...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR080_.../frame_0030.png（00:30時点・水面IR映像が確認できるフレーム）`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR080_20_October_2020_CALLSIGN_CALLSIGN_Observes_UAP.mp4 より抽出（00:30時点・水面I`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP_AFRICOM`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-072】`
  - 変更後: `# 【概要版#2_072】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR081 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR08...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP_AFRICOM.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP_AFRICOM`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-073】`
  - 変更後: `# 【概要版#2_073】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR082 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR08...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP_AFRICOM.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-074】`
  - 変更後: `# 【概要版#2_074】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR083 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR08...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR084_17_Sept_2020_CALLSIGN_observes_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-075】`
  - 変更後: `# 【概要版#2_075】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR084 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR08...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR084_17_Sept_2020_CALLSIGN_observes_UAP/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR084_17_Sept_2020_CALLSIGN_observes_UAP.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR085_16_Sept_2020_CALLSIGN_observes_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-076】`
  - 変更後: `# 【概要版#2_076】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR085 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR08...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR085_16_Sept_2020_CALLSIGN_CALLSIGN_observes_UAP/frame_0000.p`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR085_16_Sept_2020_CALLSIGN_observes_UAP.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-077】`
  - 変更後: `# 【概要版#2_077】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR086 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR08...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast/frame_0000.png（白い球体（オーブ）が確認`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast.mp4 より抽出（白い球体（オーブ）が確認できる）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-078】`
  - 変更後: `# 【概要版#2_078】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR087 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR08...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR088_31_AUG_CALLSIGN_Observes_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-079】`
  - 変更後: `# 【概要版#2_079】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR088 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR08...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR088_31_AUG_CALLSIGN_CALLSIGN_Observes_UAP/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR088_31_AUG_CALLSIGN_Observes_UAP.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR089_31_AUG_CALLSIGN_Observes_UAP_part2`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-080】`
  - 変更後: `# 【概要版#2_080】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR089 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR08...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR089_31_AUG_CALLSIGN_CALLSIGN_Observes_UAP_part2/frame_0000.p`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR089_31_AUG_CALLSIGN_Observes_UAP_part2.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-081】`
  - 変更後: `# 【概要版#2_081】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR090 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR09...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-082】`
  - 変更後: `# 【概要版#2_082】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR091 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR09...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf/frame_0000.`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR092_08_AUG_2020_CALLSIGN_UAP_observation`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-083】`
  - 変更後: `# 【概要版#2_083】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR092 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR09...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR092_08_AUG_2020_CALLSIGN_CALLSIGN_UAP_observation/frame_0000`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR092_08_AUG_2020_CALLSIGN_UAP_observation.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_Dual_UAP_short`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-084】`
  - 変更後: `# 【概要版#2_084】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR093 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR09...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_CALLSIGN_Platform_Dual_UAP/fr`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_Dual_UAP_short.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR094_CALLSIGN_Mission_HD_2020-02-13`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-085】`
  - 変更後: `# 【概要版#2_085】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR094 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR09...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR094_CALLSIGN_Mission_-_HD_2020-02-13/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR094_CALLSIGN_Mission_HD_2020-02-13.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_Dual_UAP_long`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-086】`
  - 変更後: `# 【概要版#2_086】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR095 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR09...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_CALLSIGN_Platform_Dual_UAP/fr`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_Dual_UAP_long.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR096_HH11_03_July_2018_UAPs`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-087】`
  - 変更後: `# 【概要版#2_087】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR096 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR09...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR096_HH11_03_July_2018_UAPs/frame_0000.png`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR096_HH11_03_July_2018_UAPs.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_2135Z`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-088】`
  - 変更後: `# 【概要版#2_088】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR097 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR09...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_on_25SEP19_at_2135Z/frame_0`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_2135Z.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_1715Z`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-089】`
  - 変更後: `# 【概要版#2_089】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】DOW-UAP-PR099 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/DOW-UAP-PR09...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_on_25SEP19_at_1715Z/frame_0`
  - 変更後: `- 掲載画像出典：DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_1715Z.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-037】`
  - 変更後: `# 【概要版#2_037】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】FBI-UAP-PR001 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/FBI-UAP-PR00...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021/frame_0000`
  - 変更後: `- 掲載画像出典：FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021.mp4 より抽出（約0秒時点）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-038】`
  - 変更後: `# 【概要版#2_038】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】FBI-UAP-PR002 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/FBI-UAP-PR00...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022/frame_0`
  - 変更後: `- 掲載画像出典：FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022.mp4 より抽出（00:00時点・赤`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `FBI-UAP-PR003_Orbs_Over_the_Pond_2024`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-039】`
  - 変更後: `# 【概要版#2_039】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】FBI-UAP-PR003 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/FBI-UAP-PR00...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/FBI-UAP-PR003_Orbs_Over_the_Pond_2024/frame_0000.png（00:00時点・白い光球が確認でき`
  - 変更後: `- 掲載画像出典：FBI-UAP-PR003_Orbs_Over_the_Pond_2024.mp4 より抽出（00:00時点・白い光球が確認できる代表フレーム）`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `FBI-UAP-PR004_Northeastern_Orb_Sighting_2025`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-040】`
  - 変更後: `# 【概要版#2_040】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】FBI-UAP-PR004 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/FBI-UAP-PR00...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 📋 [T08] **## 注意点 スケルトン追加**
  - 変更前: `[## 出典の前]`
  - 変更後: `## 注意点↩↩**物体の正体・種別について**↩本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。「UAP」「Unresolved...`
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/FBI-UAP-PR004_Northeastern_Orb_Sighting_2025/frame_0000.png（00:00時点・赤い`
  - 変更後: `- 掲載画像出典：FBI-UAP-PR004_Northeastern_Orb_Sighting_2025.mp4 より抽出（00:00時点・赤い光帯と樹木シルエットが確認できる代`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-041】`
  - 変更後: `# 【概要版#2_041】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】FBI-UAP-PR005 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/FBI-UAP-PR00...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_Unite`
  - 変更後: `- 掲載画像出典：FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Ev`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

### `FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_United_States_Event_2023`
- 🔧 [T01] **タイトルID #R02→#2**
  - 変更前: `# 【概要版#R02-042】`
  - 変更後: `# 【概要版#2_042】`
- 🔧 [T02] **Release Date ・Release 02追加**
  - 変更前: `（war.gov/UFO/ にて公開）`
  - 変更後: `（war.gov/UFO/ にて公開・Release 02）`
- 🔧 [T03] **画像プレースホルダー ▼【画像】追加**
  - 変更前: `[▲行の直前]`
  - 変更後: `▼ 【画像】FBI-UAP-PR006 代表フレーム（映像開始直後・約0秒時点）↩↩掲載画像：thumbnails/FBI-UAP-PR00...`
- 🔧 [T04] **目視確認注釈追加**
  - 変更前: `[セクション直後]`
  - 変更後: `以下は映像フレームの目視確認によるものです。`
- 🔧 [T05] **ファイル名由来注釈 セクションヘッダー括弧追加・注釈フレーズ追加**
- 🔧 [T06+T07] **ffprobe パイプ区切り→展開箇条書き変換・intro追加**
- 🔧 [T09] **掲載画像出典 代表フレーム→掲載画像出典**
  - 変更前: `- 代表フレーム：thumbnails/FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_Unite`
  - 変更後: `- 掲載画像出典：FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_United_States_Ev`
- 🔧 [T10] **ディスクレイマー 新規追加（欠落）**
  - 変更前: `[article_id行の前]`
  - 変更後: `※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。↩↩映像内容の判断には不確...`
- 🔧 [T11] **語尾統一（1箇所）**
  - 変更前: `確認できない→確認できません`
  - 変更後: `→ です・ます調`

