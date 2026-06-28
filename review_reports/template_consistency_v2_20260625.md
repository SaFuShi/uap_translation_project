# Release 02 テンプレート準拠チェックレポート

**実行日時：** 2026-06-25 10:21  
**対象ファイル数：** 81  
**FAIL：** 3件  **WARN：** 74件  **PASS：** 4件  
**strict_verbs：** False

---

## サマリーテーブル

| ファイル | FAIL | WARN | PASS | 判定 |
|---|---|---|---|---|
| ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md | 0 | 0 | 29 | PASS |
| ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR050_4_UAP_Formation_Iran_note_version.md | 1 | 2 | 26 | **FAIL** |
| ai_summary_DOW-UAP-PR051_Syrian_UAP_instant_acceleration_note_version.md | 5 | 2 | 22 | **FAIL** |
| ai_summary_DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022_note_version.md | 0 | 0 | 29 | PASS |
| ai_summary_DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020_note_version.md | 0 | 0 | 29 | PASS |
| ai_summary_DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR057_Spherical_UAP_in_clouds_note_version.md | 8 | 7 | 14 | **FAIL** |
| ai_summary_DOW-UAP-PR059_NAG_UAP_1_Jun_20_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017_note_version.md | 0 | 0 | 29 | PASS |
| ai_summary_DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_of_water_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_Phenomenon_UAP_captured_by_fif_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR069_F_A-18_FLIR_UAP_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR072_ADMINISTRATIVE_REVISION_IIR_1777_J0032_22_Kazakhstan_UAP_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAPs_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR080_20_October_2020_CALLSIGN_CALLSIGN_Observes_UAP_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP_AFRICOM_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP_AFRICOM_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR084_17_Sept_2020_CALLSIGN_observes_UAP_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR085_16_Sept_2020_CALLSIGN_observes_UAP_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR088_31_AUG_CALLSIGN_Observes_UAP_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR089_31_AUG_CALLSIGN_Observes_UAP_part2_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR092_08_AUG_2020_CALLSIGN_UAP_observation_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_Dual_UAP_short_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR094_CALLSIGN_Mission_HD_2020-02-13_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_Dual_UAP_long_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_DOW-UAP-PR096_HH11_03_July_2018_UAPs_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_2135Z_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_1715Z_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_note_version.md | 0 | 2 | 27 | WARN |
| ai_summary_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023_note_version.md | 0 | 1 | 28 | WARN |
| ai_summary_FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_United_States_Event_2023_note_version.md | 0 | 2 | 27 | WARN |

---

## 詳細

### ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md

判定: **PASS** | PASS:29 WARN:0 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR050_4_UAP_Formation_Iran_note_version.md

判定: **FAIL** | PASS:26 WARN:2 FAIL:1

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ⚠️ 掲載画像：thumbnails/ 行
  - 「掲載画像：thumbnails/」行が存在しない（note転記済みの場合は正常）
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ❌ **フッターに article_id 行**
  - 「📋 **article_id：R02-XXX」フッターが存在しない
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR051_Syrian_UAP_instant_acceleration_note_version.md

判定: **FAIL** | PASS:22 WARN:2 FAIL:5

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ❌ **画像プレースホルダー ▼【画像】**
  - 「▼ 【画像】」が存在しない
- ⚠️ 掲載画像：thumbnails/ 行
  - 「掲載画像：thumbnails/」行が存在しない（note転記済みの場合は正常）
- ❌ **目視確認注釈フレーズ**
  - 「以下は映像フレームの目視確認によるものです。」が存在しない
- ❌ **ファイル名由来注釈フレーズ**
  - 「以下の情報はファイル名および...映像フレームから直接確認したものではありません。」が存在しない
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ❌ **出典に「掲載画像出典：」**
  - 「掲載画像出典：」が存在しない（「代表フレーム：」旧形式の可能性）
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ❌ **フッターに article_id 行**
  - 「📋 **article_id：R02-XXX」フッターが存在しない
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ⚠️ 語尾: 確認されていない → 確認されていません
  - 残存: ['確認されていない', '確認されていない'] → 確認されていません に統一
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022_note_version.md

判定: **PASS** | PASS:29 WARN:0 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020_note_version.md

判定: **PASS** | PASS:29 WARN:0 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR057_Spherical_UAP_in_clouds_note_version.md

判定: **FAIL** | PASS:14 WARN:7 FAIL:8

- ❌ **タイトルID: #2_XXX 形式**
  - タイトルが #2_XXX 形式でない（#R02-XXX など旧形式の可能性）
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ❌ **画像プレースホルダー ▼【画像】**
  - 「▼ 【画像】」が存在しない
- ⚠️ 掲載画像：thumbnails/ 行
  - 「掲載画像：thumbnails/」行が存在しない（note転記済みの場合は正常）
- ❌ **目視確認注釈フレーズ**
  - 「以下は映像フレームの目視確認によるものです。」が存在しない
- ❌ **ファイル名由来注釈フレーズ**
  - 「以下の情報はファイル名および...映像フレームから直接確認したものではありません。」が存在しない
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ⚠️ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
  - 「（DoW/DVIDS管理番号）」が存在しない（旧形式「DVIDS＝国防映像情報配信サービス」の可能性）
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ⚠️ ▲キャプション「確認できる。」の不在 [v2]
  - ▲キャプション行に「確認できる。」（普通体）が残存している（T13未適用の可能性）
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ❌ **ディスクレイマー第3段落**
  - 「今後、追加情報...詳細解析版」が存在しない
- ❌ **ディスクレイマー第4段落**
  - 「原文リンクを重視し」が存在しない
- ❌ **出典に「掲載画像出典：」**
  - 「掲載画像出典：」が存在しない（「代表フレーム：」旧形式の可能性）
- ⚠️ 旧形式「代表フレーム：thumbnails/」の不在
  - 旧形式「代表フレーム：thumbnails/」が残存している
- ❌ **フッターに article_id 行**
  - 「📋 **article_id：R02-XXX」フッターが存在しない
- ⚠️ 語尾: 扱わない → 扱いません
  - 残存: ['扱わない', '扱わない'] → 扱いません に統一
- ⚠️ 語尾: 確認できない → 確認できません
  - 残存: ['確認できない', '確認できない', '確認できない']... → 確認できません に統一
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ⚠️ 語尾: できない[。] → できません
  - 残存: ['できない）', 'できない。', 'できない\n']... → できません に統一

### ai_summary_DOW-UAP-PR059_NAG_UAP_1_Jun_20_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017_note_version.md

判定: **PASS** | PASS:29 WARN:0 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_of_water_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_Phenomenon_UAP_captured_by_fif_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR069_F_A-18_FLIR_UAP_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ✅ Related Location に AOR 情報
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR072_ADMINISTRATIVE_REVISION_IIR_1777_J0032_22_Kazakhstan_UAP_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAPs_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR080_20_October_2020_CALLSIGN_CALLSIGN_Observes_UAP_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP_AFRICOM_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP_AFRICOM_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR084_17_Sept_2020_CALLSIGN_observes_UAP_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR085_16_Sept_2020_CALLSIGN_observes_UAP_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR088_31_AUG_CALLSIGN_Observes_UAP_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR089_31_AUG_CALLSIGN_Observes_UAP_part2_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR092_08_AUG_2020_CALLSIGN_UAP_observation_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_Dual_UAP_short_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR094_CALLSIGN_Mission_HD_2020-02-13_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_Dual_UAP_long_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR096_HH11_03_July_2018_UAPs_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_2135Z_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_1715Z_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023_note_version.md

判定: **WARN** | PASS:28 WARN:1 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ✅ AI解析メモにタイムコード記載 [v2]
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません

### ai_summary_FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_United_States_Event_2023_note_version.md

判定: **WARN** | PASS:27 WARN:2 FAIL:0

- ✅ タイトルID: #2_XXX 形式
- ✅ Release Date に「Release 02」
- ⚠️ Related Location に AOR 情報
  - Related Location に「担当AOR：」が含まれていない
- ✅ 画像プレースホルダー ▼【画像】
- ✅ 掲載画像：thumbnails/ 行
- ✅ 目視確認注釈フレーズ
- ✅ ファイル名由来注釈フレーズ
- ✅ ffprobe 拡張箇条書きフォーマット
- ✅ 映像メタデータ旧形式（パイプ区切り）の不在
- ✅ ## 注意点 セクション
- ✅ DVIDS ID「（DoW/DVIDS管理番号）」表記 [v2]
- ✅ ffprobe解像度行のパイプ残留不在 [v2]
- ✅ ▲キャプション「確認できる。」の不在 [v2]
- ⚠️ AI解析メモにタイムコード記載 [v2]
  - AI解析メモにタイムコード（MM:SS形式）が含まれていない（T16未適用の可能性）
- ✅ AI解析メモに DVIDS ID 記載
- ✅ ## 注意点と## 出典間のセパレータ [v2]
- ✅ ディスクレイマー第2段落
- ✅ ディスクレイマー第3段落
- ✅ ディスクレイマー第4段落
- ✅ 出典に「掲載画像出典：」
- ✅ 旧形式「代表フレーム：thumbnails/」の不在
- ✅ フッターに article_id 行
- ✅ 語尾: 扱わない → 扱いません
- ✅ 語尾: 確認できない → 確認できません
- ✅ 語尾: 特定できない → 特定できません
- ✅ 語尾: 断定できない → 断定できません
- ✅ 語尾: 示すものではない → 示すものではありません
- ✅ 語尾: 確認されていない → 確認されていません
- ✅ 語尾: できない[。] → できません
