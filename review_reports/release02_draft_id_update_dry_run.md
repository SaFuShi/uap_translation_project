# Release 02 ドラフト title/footer 一括更新 dry-run レポート

**実行日：** 2026-06-23
**モード：** DRY-RUN（変更なし）
**スクリプト：** scripts/update_release02_draft_ids.py v1.0.0

---

## 1. サマリー

| 状態 | 件数 | 内容 |
|---|---|---|
| ⛔ NEED_UPDATE（要更新） | **73件** | #TBD 残存・更新対象 |
| ✅ SKIP（更新済み） | **5件** | #R02-XXX 反映済み |
| ⚠️ MISSING（ファイル未発見） | **0件** | note_drafts/ に該当なし |
| ❌ ERROR（処理不能） | **0件** | パターン不一致 / 読み込み失敗 |
| **合計（マッピング件数）** | **78件** | |

---

## 2. 更新対象ファイル（NEED_UPDATE: 73件）

| No. | article_id | publish_order | ファイル名 | タイトル変更 | footer変更 |
|---|---|---|---|---|---|
| 1 | R02-010 | 2010 | `ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR019：中...` → `# 【概要版#R02-010】DoW DOW-UAP-PR0...` | ✓ |
| 2 | R02-011 | 2011 | `ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR021：イ...` → `# 【概要版#R02-011】DoW DOW-UAP-PR0...` | ✓ |
| 3 | R02-012 | 2012 | `ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR022：シ...` → `# 【概要版#R02-012】DoW DOW-UAP-PR0...` | ✓ |
| 4 | R02-013 | 2013 | `ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR023：イ...` → `# 【概要版#R02-013】DoW DOW-UAP-PR0...` | ✓ |
| 5 | R02-014 | 2014 | `ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR026：ア...` → `# 【概要版#R02-014】DoW DOW-UAP-PR0...` | ✓ |
| 6 | R02-015 | 2015 | `ai_summary_DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR027：ア...` → `# 【概要版#R02-015】DoW DOW-UAP-PR0...` | ✓ |
| 7 | R02-016 | 2016 | `ai_summary_DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR028：ギ...` → `# 【概要版#R02-016】DoW DOW-UAP-PR0...` | ✓ |
| 8 | R02-017 | 2017 | `ai_summary_DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR029：ア...` → `# 【概要版#R02-017】DoW DOW-UAP-PR0...` | ✓ |
| 9 | R02-018 | 2018 | `ai_summary_DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR031：シ...` → `# 【概要版#R02-018】DoW DOW-UAP-PR0...` | ✓ |
| 10 | R02-019 | 2019 | `ai_summary_DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR032：シ...` → `# 【概要版#R02-019】DoW DOW-UAP-PR0...` | ✓ |
| 11 | R02-020 | 2020 | `ai_summary_DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR033：シ...` → `# 【概要版#R02-020】DoW DOW-UAP-PR0...` | ✓ |
| 12 | R02-021 | 2021 | `ai_summary_DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR034：ギ...` → `# 【概要版#R02-021】DoW DOW-UAP-PR0...` | ✓ |
| 13 | R02-022 | 2022 | `ai_summary_DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR035：ギ...` → `# 【概要版#R02-022】DoW DOW-UAP-PR0...` | ✓ |
| 14 | R02-023 | 2023 | `ai_summary_DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR036：中...` → `# 【概要版#R02-023】DoW DOW-UAP-PR0...` | ✓ |
| 15 | R02-024 | 2024 | `ai_summary_DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR037：中...` → `# 【概要版#R02-024】DoW DOW-UAP-PR0...` | ✓ |
| 16 | R02-025 | 2025 | `ai_summary_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR038：中...` → `# 【概要版#R02-025】DoW DOW-UAP-PR0...` | ✓ |
| 17 | R02-026 | 2026 | `ai_summary_DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR039：中...` → `# 【概要版#R02-026】DoW DOW-UAP-PR0...` | ✓ |
| 18 | R02-027 | 2027 | `ai_summary_DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR040：中...` → `# 【概要版#R02-027】DoW DOW-UAP-PR0...` | ✓ |
| 19 | R02-028 | 2028 | `ai_summary_DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR041：中...` → `# 【概要版#R02-028】DoW DOW-UAP-PR0...` | ✓ |
| 20 | R02-029 | 2029 | `ai_summary_DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR042：中...` → `# 【概要版#R02-029】DoW DOW-UAP-PR0...` | ✓ |
| 21 | R02-030 | 2030 | `ai_summary_DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR043：ア...` → `# 【概要版#R02-030】DoW DOW-UAP-PR0...` | ✓ |
| 22 | R02-031 | 2031 | `ai_summary_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR044：中...` → `# 【概要版#R02-031】DoW DOW-UAP-PR0...` | ✓ |
| 23 | R02-032 | 2032 | `ai_summary_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR045：南...` → `# 【概要版#R02-032】DoW DOW-UAP-PR0...` | ✓ |
| 24 | R02-033 | 2033 | `ai_summary_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR046：I...` → `# 【概要版#R02-033】DoW DOW-UAP-PR0...` | ✓ |
| 25 | R02-034 | 2034 | `ai_summary_DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR047：I...` → `# 【概要版#R02-034】DoW DOW-UAP-PR0...` | ✓ |
| 26 | R02-035 | 2035 | `ai_summary_DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR048：I...` → `# 【概要版#R02-035】DoW DOW-UAP-PR0...` | ✓ |
| 27 | R02-036 | 2036 | `ai_summary_DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR049：陸...` → `# 【概要版#R02-036】DoW DOW-UAP-PR0...` | ✓ |
| 28 | R02-037 | 2037 | `ai_summary_FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021_note_version.md` | `# 【概要版#TBD】FBI FBI-UAP-PR001：北...` → `# 【概要版#R02-037】FBI FBI-UAP-PR0...` | ✓ |
| 29 | R02-038 | 2038 | `ai_summary_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_note_version.md` | `# 【概要版#TBD】FBI FBI-UAP-PR002：北...` → `# 【概要版#R02-038】FBI FBI-UAP-PR0...` | ✓ |
| 30 | R02-039 | 2039 | `ai_summary_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_note_version.md` | `# 【概要版#TBD】FBI FBI-UAP-PR003：「...` → `# 【概要版#R02-039】FBI FBI-UAP-PR0...` | ✓ |
| 31 | R02-040 | 2040 | `ai_summary_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_note_version.md` | `# 【概要版#TBD】FBI FBI-UAP-PR004：北...` → `# 【概要版#R02-040】FBI FBI-UAP-PR0...` | ✓ |
| 32 | R02-041 | 2041 | `ai_summary_FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023_note_version.md` | `# 【概要版#TBD】FBI FBI-UAP-PR005：西...` → `# 【概要版#R02-041】FBI FBI-UAP-PR0...` | ✓ |
| 33 | R02-042 | 2042 | `ai_summary_FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_United_States_Event_2023_note_version.md` | `# 【概要版#TBD】FBI FBI-UAP-PR006：西...` → `# 【概要版#R02-042】FBI FBI-UAP-PR0...` | ✓ |
| 34 | R02-043 | 2043 | `ai_summary_DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22_note_version.md` | `# 【概要版#2_TBD】DoW DOW-UAP-PR053...` → `# 【概要版#R02-043】DoW DOW-UAP-PR0...` | ✓ |
| 35 | R02-044 | 2044 | `ai_summary_DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR054：球...` → `# 【概要版#R02-044】DoW DOW-UAP-PR0...` | ✓ |
| 36 | R02-045 | 2045 | `ai_summary_DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR055：球...` → `# 【概要版#R02-045】DoW DOW-UAP-PR0...` | ✓ |
| 37 | R02-046 | 2046 | `ai_summary_DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR056：球...` → `# 【概要版#R02-046】DoW DOW-UAP-PR0...` | ✓ |
| 38 | R02-051 | 2051 | `ai_summary_DOW-UAP-PR059_NAG_UAP_1_Jun_20_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR059：「...` → `# 【概要版#R02-051】DoW DOW-UAP-PR0...` | ✓ |
| 39 | R02-053 | 2053 | `ai_summary_DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR061：球...` → `# 【概要版#R02-053】DoW DOW-UAP-PR0...` | ✓ |
| 40 | R02-054 | 2054 | `ai_summary_DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR062：球...` → `# 【概要版#R02-054】DoW DOW-UAP-PR0...` | ✓ |
| 41 | R02-055 | 2055 | `ai_summary_DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR063：球...` → `# 【概要版#R02-055】DoW DOW-UAP-PR0...` | ✓ |
| 42 | R02-056 | 2056 | `ai_summary_DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR064：A...` → `# 【概要版#R02-056】DoW DOW-UAP-PR0...` | ✓ |
| 43 | R02-057 | 2057 | `ai_summary_DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR065：U...` → `# 【概要版#R02-057】DoW DOW-UAP-PR0...` | ✓ |
| 44 | R02-059 | 2059 | `ai_summary_DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_of_water_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR067：艦...` → `# 【概要版#R02-059】DoW DOW-UAP-PR0...` | ✓ |
| 45 | R02-060 | 2060 | `ai_summary_DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_Phenomenon_UAP_captured_by_fif_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR068：I...` → `# 【概要版#R02-060】DoW DOW-UAP-PR0...` | ✓ |
| 46 | R02-061 | 2061 | `ai_summary_DOW-UAP-PR069_F_A-18_FLIR_UAP_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR069：F...` → `# 【概要版#R02-061】DoW DOW-UAP-PR0...` | ✓ |
| 47 | R02-063 | 2063 | `ai_summary_DOW-UAP-PR072_ADMINISTRATIVE_REVISION_IIR_1777_J0032_22_Kazakhstan_UAP_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR072：カ...` → `# 【概要版#R02-063】DoW DOW-UAP-PR0...` | ✓ |
| 48 | R02-064 | 2064 | `ai_summary_DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR073：米...` → `# 【概要版#R02-064】DoW DOW-UAP-PR0...` | ✓ |
| 49 | R02-065 | 2065 | `ai_summary_DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR074：C...` → `# 【概要版#R02-065】DoW DOW-UAP-PR0...` | ✓ |
| 50 | R02-066 | 2066 | `ai_summary_DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR075：東...` → `# 【概要版#R02-066】DoW DOW-UAP-PR0...` | ✓ |
| 51 | R02-067 | 2067 | `ai_summary_DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR076：C...` → `# 【概要版#R02-067】DoW DOW-UAP-PR0...` | ✓ |
| 52 | R02-068 | 2068 | `ai_summary_DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR077：C...` → `# 【概要版#R02-068】DoW DOW-UAP-PR0...` | ✓ |
| 53 | R02-069 | 2069 | `ai_summary_DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR078：C...` → `# 【概要版#R02-069】DoW DOW-UAP-PR0...` | ✓ |
| 54 | R02-070 | 2070 | `ai_summary_DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAPs_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR079：C...` → `# 【概要版#R02-070】DoW DOW-UAP-PR0...` | ✓ |
| 55 | R02-071 | 2071 | `ai_summary_DOW-UAP-PR080_20_October_2020_CALLSIGN_CALLSIGN_Observes_UAP_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR080：C...` → `# 【概要版#R02-071】DoW DOW-UAP-PR0...` | ✓ |
| 56 | R02-072 | 2072 | `ai_summary_DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP_AFRICOM_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR081：A...` → `# 【概要版#R02-072】DoW DOW-UAP-PR0...` | ✓ |
| 57 | R02-073 | 2073 | `ai_summary_DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP_AFRICOM_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR082：A...` → `# 【概要版#R02-073】DoW DOW-UAP-PR0...` | ✓ |
| 58 | R02-074 | 2074 | `ai_summary_DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR083：C...` → `# 【概要版#R02-074】DoW DOW-UAP-PR0...` | ✓ |
| 59 | R02-075 | 2075 | `ai_summary_DOW-UAP-PR084_17_Sept_2020_CALLSIGN_observes_UAP_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR084：C...` → `# 【概要版#R02-075】DoW DOW-UAP-PR0...` | ✓ |
| 60 | R02-076 | 2076 | `ai_summary_DOW-UAP-PR085_16_Sept_2020_CALLSIGN_observes_UAP_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR085：C...` → `# 【概要版#R02-076】DoW DOW-UAP-PR0...` | ✓ |
| 61 | R02-077 | 2077 | `ai_summary_DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR086：N...` → `# 【概要版#R02-077】DoW DOW-UAP-PR0...` | ✓ |
| 62 | R02-078 | 2078 | `ai_summary_DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR087：C...` → `# 【概要版#R02-078】DoW DOW-UAP-PR0...` | ✓ |
| 63 | R02-079 | 2079 | `ai_summary_DOW-UAP-PR088_31_AUG_CALLSIGN_Observes_UAP_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR088：C...` → `# 【概要版#R02-079】DoW DOW-UAP-PR0...` | ✓ |
| 64 | R02-080 | 2080 | `ai_summary_DOW-UAP-PR089_31_AUG_CALLSIGN_Observes_UAP_part2_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR089：C...` → `# 【概要版#R02-080】DoW DOW-UAP-PR0...` | ✓ |
| 65 | R02-081 | 2081 | `ai_summary_DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR090：C...` → `# 【概要版#R02-081】DoW DOW-UAP-PR0...` | ✓ |
| 66 | R02-082 | 2082 | `ai_summary_DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR091：C...` → `# 【概要版#R02-082】DoW DOW-UAP-PR0...` | ✓ |
| 67 | R02-083 | 2083 | `ai_summary_DOW-UAP-PR092_08_AUG_2020_CALLSIGN_UAP_observation_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR092：C...` → `# 【概要版#R02-083】DoW DOW-UAP-PR0...` | ✓ |
| 68 | R02-084 | 2084 | `ai_summary_DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_Dual_UAP_short_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR093：C...` → `# 【概要版#R02-084】DoW DOW-UAP-PR0...` | ✓ |
| 69 | R02-085 | 2085 | `ai_summary_DOW-UAP-PR094_CALLSIGN_Mission_HD_2020-02-13_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR094：C...` → `# 【概要版#R02-085】DoW DOW-UAP-PR0...` | ✓ |
| 70 | R02-086 | 2086 | `ai_summary_DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_Dual_UAP_long_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR095：C...` → `# 【概要版#R02-086】DoW DOW-UAP-PR0...` | ✓ |
| 71 | R02-087 | 2087 | `ai_summary_DOW-UAP-PR096_HH11_03_July_2018_UAPs_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR096：C...` → `# 【概要版#R02-087】DoW DOW-UAP-PR0...` | ✓ |
| 72 | R02-088 | 2088 | `ai_summary_DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_2135Z_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR097：C...` → `# 【概要版#R02-088】DoW DOW-UAP-PR0...` | ✓ |
| 73 | R02-089 | 2089 | `ai_summary_DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_1715Z_note_version.md` | `# 【概要版#TBD】DoW DOW-UAP-PR099：C...` → `# 【概要版#R02-089】DoW DOW-UAP-PR0...` | ✓ |

## 3. 変更前/変更後 詳細（NEED_UPDATE）

### R02-010 / #2_010 / publish_order: 2010

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR019：中東2022年5月UAPとされる事案映像（ファイル名より）──Middle East・米国防省公開・Release 02
変更後: # 【概要版#R02-010】DoW DOW-UAP-PR019：中東2022年5月UAPとされる事案映像（ファイル名より）──Middle East・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-010 / #2_010 / publish_order: 2010**（2026-06-23 正式採番）  
sourc...
```

### R02-011 / #2_011 / publish_order: 2011

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR021：イラク2022年5月UAPとされる事案映像（ファイル名より）──Iraq・米国防省公開・Release 02
変更後: # 【概要版#R02-011】DoW DOW-UAP-PR021：イラク2022年5月UAPとされる事案映像（ファイル名より）──Iraq・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-011 / #2_011 / publish_order: 2011**（2026-06-23 正式採番）  
sourc...
```

### R02-012 / #2_012 / publish_order: 2012

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR022：シリア2022年7月UAPとされる事案映像・3分割表示（ファイル名より）──Syria・米国防省公開・Release 02
変更後: # 【概要版#R02-012】DoW DOW-UAP-PR022：シリア2022年7月UAPとされる事案映像・3分割表示（ファイル名より）──Syria・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-012 / #2_012 / publish_order: 2012**（2026-06-23 正式採番）  
sourc...
```

### R02-013 / #2_013 / publish_order: 2013

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR023：イラク2022年12月UAPとされる事案映像（ファイル名より）──Iraq・米国防省公開・Release 02
変更後: # 【概要版#R02-013】DoW DOW-UAP-PR023：イラク2022年12月UAPとされる事案映像（ファイル名より）──Iraq・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-013 / #2_013 / publish_order: 2013**（2026-06-23 正式採番）  
sourc...
```

### R02-014 / #2_014 / publish_order: 2014

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR026：アラブ首長国連邦2023年10月UAPとされる事案映像（ファイル名より）──UAE・米国防省公開・Release 02
変更後: # 【概要版#R02-014】DoW DOW-UAP-PR026：アラブ首長国連邦2023年10月UAPとされる事案映像（ファイル名より）──UAE・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-014 / #2_014 / publish_order: 2014**（2026-06-23 正式採番）  
sourc...
```

### R02-015 / #2_015 / publish_order: 2015

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR027：アラブ首長国連邦2023年10月UAPとされる事案映像・海岸・施設群の俯瞰（ファイル名より）──UAE・米国防省公開・Release 02
変更後: # 【概要版#R02-015】DoW DOW-UAP-PR027：アラブ首長国連邦2023年10月UAPとされる事案映像・海岸・施設群の俯瞰（ファイル名より）──UAE・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-015 / #2_015 / publish_order: 2015**（2026-06-23 正式採番）  
sourc...
```

### R02-016 / #2_016 / publish_order: 2016

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR028：ギリシャ2024年1月UAPとされる事案映像・2分割（カラー＋グレースケール）表示（ファイル名より）──Greece・米国防省公開・Release 02
変更後: # 【概要版#R02-016】DoW DOW-UAP-PR028：ギリシャ2024年1月UAPとされる事案映像・2分割（カラー＋グレースケール）表示（ファイル名より）──Greece・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-016 / #2_016 / publish_order: 2016**（2026-06-23 正式採番）  
sourc...
```

### R02-017 / #2_017 / publish_order: 2017

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR029：アラブ首長国連邦2024年6月UAPとされる事案映像・矩形トラッキングとオレンジ物体（ファイル名より）──Gulf of Oman・米国防省公開・Release 02
変更後: # 【概要版#R02-017】DoW DOW-UAP-PR029：アラブ首長国連邦2024年6月UAPとされる事案映像・矩形トラッキングとオレンジ物体（ファイル名より）──Gulf of Oman・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-017 / #2_017 / publish_order: 2017**（2026-06-23 正式採番）  
sourc...
```

### R02-018 / #2_018 / publish_order: 2018

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR031：シリア2024年10月UAPとされる事案映像（ファイル名より）──Syria・米国防省公開・Release 02
変更後: # 【概要版#R02-018】DoW DOW-UAP-PR031：シリア2024年10月UAPとされる事案映像（ファイル名より）──Syria・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-018 / #2_018 / publish_order: 2018**（2026-06-23 正式採番）  
sourc...
```

### R02-019 / #2_019 / publish_order: 2019

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR032：シリア2024年10月UAPとされる事案映像・クリップ2（ファイル名より）──Syria・米国防省公開・Release 02
変更後: # 【概要版#R02-019】DoW DOW-UAP-PR032：シリア2024年10月UAPとされる事案映像・クリップ2（ファイル名より）──Syria・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-019 / #2_019 / publish_order: 2019**（2026-06-23 正式採番）  
sourc...
```

### R02-020 / #2_020 / publish_order: 2020

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR033：シリア2024年10月UAPとされる事案映像・赤い熱源が確認できるクリップ（ファイル名より）──Syria・米国防省公開・Release 02
変更後: # 【概要版#R02-020】DoW DOW-UAP-PR033：シリア2024年10月UAPとされる事案映像・赤い熱源が確認できるクリップ（ファイル名より）──Syria・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-020 / #2_020 / publish_order: 2020**（2026-06-23 正式採番）  
sourc...
```

### R02-021 / #2_021 / publish_order: 2021

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR034：ギリシャ2023年10月UAPとされる事案映像（ファイル名より）──Greece・米国防省公開・Release 02
変更後: # 【概要版#R02-021】DoW DOW-UAP-PR034：ギリシャ2023年10月UAPとされる事案映像（ファイル名より）──Greece・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-021 / #2_021 / publish_order: 2021**（2026-06-23 正式採番）  
sourc...
```

### R02-022 / #2_022 / publish_order: 2022

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR035：ギリシャ2023年10月UAPとされる事案映像（ファイル名より）──Greece・米国防省公開・Release 02
変更後: # 【概要版#R02-022】DoW DOW-UAP-PR035：ギリシャ2023年10月UAPとされる事案映像（ファイル名より）──Greece・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-022 / #2_022 / publish_order: 2022**（2026-06-23 正式採番）  
sourc...
```

### R02-023 / #2_023 / publish_order: 2023

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR036：中東2020年5月UAPとされる事案映像・船状物体を囲むグリーンラインと多色UIマーカー（ファイル名より）──Middle East・米国防省公開・Release 02
変更後: # 【概要版#R02-023】DoW DOW-UAP-PR036：中東2020年5月UAPとされる事案映像・船状物体を囲むグリーンラインと多色UIマーカー（ファイル名より）──Middle East・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-023 / #2_023 / publish_order: 2023**（2026-06-23 正式採番）  
sourc...
```

### R02-024 / #2_024 / publish_order: 2024

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR037：中東2020年UAPとされる事案映像・船が確認できる海面俯瞰（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
変更後: # 【概要版#R02-024】DoW DOW-UAP-PR037：中東2020年UAPとされる事案映像・船が確認できる海面俯瞰（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-024 / #2_024 / publish_order: 2024**（2026-06-23 正式採番）  
sourc...
```

### R02-025 / #2_025 / publish_order: 2025

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR038：中東2013年UAPとされる事案映像・古い世代のUIスタイル（ファイル名より）──Middle East・米国防省公開・Release 02
変更後: # 【概要版#R02-025】DoW DOW-UAP-PR038：中東2013年UAPとされる事案映像・古い世代のUIスタイル（ファイル名より）──Middle East・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-025 / #2_025 / publish_order: 2025**（2026-06-23 正式採番）  
sourc...
```

### R02-026 / #2_026 / publish_order: 2026

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR039：中東2020年UAPとされる事案映像・海岸施設とオレンジ/赤マーカー（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
変更後: # 【概要版#R02-026】DoW DOW-UAP-PR039：中東2020年UAPとされる事案映像・海岸施設とオレンジ/赤マーカー（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-026 / #2_026 / publish_order: 2026**（2026-06-23 正式採番）  
sourc...
```

### R02-027 / #2_027 / publish_order: 2027

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR040：中東（アラビア湾）2020年UAPとされる事案映像・雲の映像と大きな黒塗り矩形（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
変更後: # 【概要版#R02-027】DoW DOW-UAP-PR040：中東（アラビア湾）2020年UAPとされる事案映像・雲の映像と大きな黒塗り矩形（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-027 / #2_027 / publish_order: 2027**（2026-06-23 正式採番）  
sourc...
```

### R02-028 / #2_028 / publish_order: 2028

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR041：中東（アラビア湾）2020年UAPとされる事案映像・地平線と複数のシアンマーカー（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
変更後: # 【概要版#R02-028】DoW DOW-UAP-PR041：中東（アラビア湾）2020年UAPとされる事案映像・地平線と複数のシアンマーカー（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-028 / #2_028 / publish_order: 2028**（2026-06-23 正式採番）  
sourc...
```

### R02-029 / #2_029 / publish_order: 2029

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR042：中東（アラビア湾）2020年UAPとされる事案映像・ノイズが多い映像と青い点マーカー複数（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
変更後: # 【概要版#R02-029】DoW DOW-UAP-PR042：中東（アラビア湾）2020年UAPとされる事案映像・ノイズが多い映像と青い点マーカー複数（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-029 / #2_029 / publish_order: 2029**（2026-06-23 正式採番）  
sourc...
```

### R02-030 / #2_030 / publish_order: 2030

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR043：アフリカ（ジブチ）2025年UAPとされる事案映像・航空機窓からの撮影とみられる（ファイル名より）──Djibouti・米国防省公開・Release 02
変更後: # 【概要版#R02-030】DoW DOW-UAP-PR043：アフリカ（ジブチ）2025年UAPとされる事案映像・航空機窓からの撮影とみられる（ファイル名より）──Djibouti・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-030 / #2_030 / publish_order: 2030**（2026-06-23 正式採番）  
sourc...
```

### R02-031 / #2_031 / publish_order: 2031

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR044：中東（アラビア湾）2020年UAPとされる事案映像・霧中の黒い物体と赤矢印マーカー（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
変更後: # 【概要版#R02-031】DoW DOW-UAP-PR044：中東（アラビア湾）2020年UAPとされる事案映像・霧中の黒い物体と赤矢印マーカー（ファイル名より）──Arabian Gulf・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-031 / #2_031 / publish_order: 2031**（2026-06-23 正式採番）  
sourc...
```

### R02-032 / #2_032 / publish_order: 2032

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR045：南部米国2020年UAPとされる事案映像・大楕円マゼンタUI・グリーンフレーム（ファイル名はMiddle East・AOR=Southern United States）──米国防省公開・Release 02
変更後: # 【概要版#R02-032】DoW DOW-UAP-PR045：南部米国2020年UAPとされる事案映像・大楕円マゼンタUI・グリーンフレーム（ファイル名はMiddle East・AOR=Southern United States）──米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-032 / #2_032 / publish_order: 2032**（2026-06-23 正式採番）  
sourc...
```

### R02-033 / #2_033 / publish_order: 2033

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR046：INDOPACOM2024年UAPとされる事案映像・白い翼状物体が確認できる（ファイル名より）──East China Sea・米国防省公開・Release 02
変更後: # 【概要版#R02-033】DoW DOW-UAP-PR046：INDOPACOM2024年UAPとされる事案映像・白い翼状物体が確認できる（ファイル名より）──East China Sea・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-033 / #2_033 / publish_order: 2033**（2026-06-23 正式採番）  
sourc...
```

### R02-034 / #2_034 / publish_order: 2034

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR047：INDOPACOM（日本）2023年UAPとされる事案映像・赤い円形クロスヘアとグリーンフレーム（ファイル名より）──Japan・米国防省公開・Release 02
変更後: # 【概要版#R02-034】DoW DOW-UAP-PR047：INDOPACOM（日本）2023年UAPとされる事案映像・赤い円形クロスヘアとグリーンフレーム（ファイル名より）──Japan・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-034 / #2_034 / publish_order: 2034**（2026-06-23 正式採番）  
sourc...
```

### R02-035 / #2_035 / publish_order: 2035

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR048：INDOPACOM2024年UAPとされる事案映像・下部に風力発電機（風車）が確認できる（ファイル名より）──Indo-PACOM・米国防省公開・Release 02
変更後: # 【概要版#R02-035】DoW DOW-UAP-PR048：INDOPACOM2024年UAPとされる事案映像・下部に風力発電機（風車）が確認できる（ファイル名より）──Indo-PACOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-035 / #2_035 / publish_order: 2035**（2026-06-23 正式採番）  
sourc...
```

### R02-036 / #2_036 / publish_order: 2036

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR049：陸軍2026年UAPとされる事案映像・夜間撮影で飛行体状の白い物体が確認できる（ファイル名より）──North America・米国防省公開・Release 02
変更後: # 【概要版#R02-036】DoW DOW-UAP-PR049：陸軍2026年UAPとされる事案映像・夜間撮影で飛行体状の白い物体が確認できる（ファイル名より）──North America・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-036 / #2_036 / publish_order: 2036**（2026-06-23 正式採番）  
sourc...
```

### R02-037 / #2_037 / publish_order: 2037

**ファイル：** `note_drafts/ai_summary_FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】FBI FBI-UAP-PR001：北東部米国2021年「三角形オーブ」とされる事案映像──Northeastern United States・FBI公開・Release 02
変更後: # 【概要版#R02-037】FBI FBI-UAP-PR001：北東部米国2021年「三角形オーブ」とされる事案映像──Northeastern United States・FBI公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-037 / #2_037 / publish_order: 2037**（2026-06-23 正式採番）  
sourc...
```

### R02-038 / #2_038 / publish_order: 2038

**ファイル：** `note_drafts/ai_summary_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】FBI FBI-UAP-PR002：北東部米国2022年「赤いオーブの回転」とされる事案映像・明確な赤い光球が確認できる──Northeastern United States・FBI公開・Release 02
変更後: # 【概要版#R02-038】FBI FBI-UAP-PR002：北東部米国2022年「赤いオーブの回転」とされる事案映像・明確な赤い光球が確認できる──Northeastern United States・FBI公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-038 / #2_038 / publish_order: 2038**（2026-06-23 正式採番）  
sourc...
```

### R02-039 / #2_039 / publish_order: 2039

**ファイル：** `note_drafts/ai_summary_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】FBI FBI-UAP-PR003：「池（Pond）の上のオーブ」とされる事案映像・2024年・白い光球が確認できる縦位置映像──Northeastern United States・FBI公開・Release 02
変更後: # 【概要版#R02-039】FBI FBI-UAP-PR003：「池（Pond）の上のオーブ」とされる事案映像・2024年・白い光球が確認できる縦位置映像──Northeastern United States・FBI公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-039 / #2_039 / publish_order: 2039**（2026-06-23 正式採番）  
sourc...
```

### R02-040 / #2_040 / publish_order: 2040

**ファイル：** `note_drafts/ai_summary_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】FBI FBI-UAP-PR004：北東部米国2025年「オーブ目撃」とされる事案映像・赤い光の帯が確認できる縦位置映像──Northeastern United States・FBI公開・Release 02
変更後: # 【概要版#R02-040】FBI FBI-UAP-PR004：北東部米国2025年「オーブ目撃」とされる事案映像・赤い光の帯が確認できる縦位置映像──Northeastern United States・FBI公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-040 / #2_040 / publish_order: 2040**（2026-06-23 正式採番）  
sourc...
```

### R02-041 / #2_041 / publish_order: 2041

**ファイル：** `note_drafts/ai_summary_FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】FBI FBI-UAP-PR005：西部米国2023年事案のデジタル再現映像（ナレーティブステートメント3-1）・砂漠景色とオレンジ色の球体のカラーCG映像──Western United States・FBI公開・Release 02
変更後: # 【概要版#R02-041】FBI FBI-UAP-PR005：西部米国2023年事案のデジタル再現映像（ナレーティブステートメント3-1）・砂漠景色とオレンジ色の球体のカラーCG映像──Western United States・FBI公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-041 / #2_041 / publish_order: 2041**（2026-06-23 正式採番）  
sourc...
```

### R02-042 / #2_042 / publish_order: 2042

**ファイル：** `note_drafts/ai_summary_FBI-UAP-PR006_Digital_Recreation_Narrative_Statement_3-2_Western_United_States_Event_2023_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】FBI FBI-UAP-PR006：西部米国2023年事案のデジタル再現映像（ナレーティブステートメント3-2）──Western United States・FBI公開・Release 02
変更後: # 【概要版#R02-042】FBI FBI-UAP-PR006：西部米国2023年事案のデジタル再現映像（ナレーティブステートメント3-2）──Western United States・FBI公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-042 / #2_042 / publish_order: 2042**（2026-06-23 正式採番）  
sourc...
```

### R02-043 / #2_043 / publish_order: 2043

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#2_TBD】DoW DOW-UAP-PR053：センサー追尾映像内で葉巻型または高速球形と評価されたUAP（赤外線映像と推定）──ファイル名より：CENTCOM担当区域・2022年10月15日・米国防省公開・Release 02
変更後: # 【概要版#R02-043】DoW DOW-UAP-PR053：センサー追尾映像内で葉巻型または高速球形と評価されたUAP（赤外線映像と推定）──ファイル名より：CENTCOM担当区域・2022年10月15日・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-043 / #2_043 / publish_order: 2043**（2026-06-23 正式採番）  
sourc...
```

### R02-044 / #2_044 / publish_order: 2044

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR054：球形UAPとされる物体が不規則な動きを示すとされる映像（ファイル名より）──EUCOM担当区域・2022年・米国防省公開・Release 02
変更後: # 【概要版#R02-044】DoW DOW-UAP-PR054：球形UAPとされる物体が不規則な動きを示すとされる映像（ファイル名より）──EUCOM担当区域・2022年・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-044 / #2_044 / publish_order: 2044**（2026-06-23 正式採番）  
sourc...
```

### R02-045 / #2_045 / publish_order: 2045

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR055：球形UAPとされる物体の雲間映像と追尾表示らしきクロスヘアが確認できる映像（ファイル名より）──CENTCOM担当区域・2020年11月23日・米国防省公開・Release 02
変更後: # 【概要版#R02-045】DoW DOW-UAP-PR055：球形UAPとされる物体の雲間映像と追尾表示らしきクロスヘアが確認できる映像（ファイル名より）──CENTCOM担当区域・2020年11月23日・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-045 / #2_045 / publish_order: 2045**（2026-06-23 正式採番）  
sourc...
```

### R02-046 / #2_046 / publish_order: 2046

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR056：球形UAPとされる物体が水面上でpulsing（点滅・脈動）しているとされる映像（ファイル名より）──担当AOR不明・米国防省公開・Release 02
変更後: # 【概要版#R02-046】DoW DOW-UAP-PR056：球形UAPとされる物体が水面上でpulsing（点滅・脈動）しているとされる映像（ファイル名より）──担当AOR不明・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-046 / #2_046 / publish_order: 2046**（2026-06-23 正式採番）  
sourc...
```

### R02-051 / #2_051 / publish_order: 2051

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR059_NAG_UAP_1_Jun_20_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR059：「NAG」と称されるUAPが映るとされる俯瞰映像（ファイル名より）──CENTCOM担当区域・2020年6月1日・米国防省公開・Release 02
変更後: # 【概要版#R02-051】DoW DOW-UAP-PR059：「NAG」と称されるUAPが映るとされる俯瞰映像（ファイル名より）──CENTCOM担当区域・2020年6月1日・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-051 / #2_051 / publish_order: 2051**（2026-06-23 正式採番）  
sourc...
```

### R02-053 / #2_053 / publish_order: 2053

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR061：球形UAPとされる物体を記録したとされる昼間カラー俯瞰映像・クリップ0（ファイル名より）──CENTCOM担当区域・2021年4月12日・米国防省公開・Release 02
変更後: # 【概要版#R02-053】DoW DOW-UAP-PR061：球形UAPとされる物体を記録したとされる昼間カラー俯瞰映像・クリップ0（ファイル名より）──CENTCOM担当区域・2021年4月12日・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-053 / #2_053 / publish_order: 2053**（2026-06-23 正式採番）  
sourc...
```

### R02-054 / #2_054 / publish_order: 2054

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR062：球形UAPとされる物体を記録したとされる昼間カラー俯瞰映像・映像クリップ番号1（vid_1）（ファイル名より）──CENTCOM担当区域・2021年4月12日・米国防省公開・Release 02
変更後: # 【概要版#R02-054】DoW DOW-UAP-PR062：球形UAPとされる物体を記録したとされる昼間カラー俯瞰映像・映像クリップ番号1（vid_1）（ファイル名より）──CENTCOM担当区域・2021年4月12日・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-054 / #2_054 / publish_order: 2054**（2026-06-23 正式採番）  
sourc...
```

### R02-055 / #2_055 / publish_order: 2055

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR063：球形UAPとされる物体を記録したとされる昼間カラー俯瞰映像・クリップ2（ファイル名より）──CENTCOM担当区域・2021年4月12日・米国防省公開・Release 02
変更後: # 【概要版#R02-055】DoW DOW-UAP-PR063：球形UAPとされる物体を記録したとされる昼間カラー俯瞰映像・クリップ2（ファイル名より）──CENTCOM担当区域・2021年4月12日・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-055 / #2_055 / publish_order: 2055**（2026-06-23 正式採番）  
sourc...
```

### R02-056 / #2_056 / publish_order: 2056

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR064：AFSOC（米空軍特殊作戦コマンド）によるカブール上空UAP追尾映像（ファイル名より）──CENTCOM担当区域・2017年7月・米国防省公開・Release 02
変更後: # 【概要版#R02-056】DoW DOW-UAP-PR064：AFSOC（米空軍特殊作戦コマンド）によるカブール上空UAP追尾映像（ファイル名より）──CENTCOM担当区域・2017年7月・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-056 / #2_056 / publish_order: 2056**（2026-06-23 正式採番）  
sourc...
```

### R02-057 / #2_057 / publish_order: 2057

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR065：USCG C-144からの「TIC TAC IR hot」とされる映像・クリップ2（ファイル名より）──南東部米国・2024年4月24日・米国防省公開・Release 02
変更後: # 【概要版#R02-057】DoW DOW-UAP-PR065：USCG C-144からの「TIC TAC IR hot」とされる映像・クリップ2（ファイル名より）──南東部米国・2024年4月24日・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-057 / #2_057 / publish_order: 2057**（2026-06-23 正式採番）  
sourc...
```

### R02-059 / #2_059 / publish_order: 2059

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_of_water_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR067：艦船とみられる物体の近傍に複数の点状マーカーが確認されるグレースケール俯瞰映像（ファイル名より「球形UAP・USO・潜水艦近傍・水出入り」）──米国防省公開・Release 02
変更後: # 【概要版#R02-059】DoW DOW-UAP-PR067：艦船とみられる物体の近傍に複数の点状マーカーが確認されるグレースケール俯瞰映像（ファイル名より「球形UAP・USO・潜水艦近傍・水出入り」）──米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-059 / #2_059 / publish_order: 2059**（2026-06-23 正式採番）  
sourc...
```

### R02-060 / #2_060 / publish_order: 2060

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_Unidentified_Aerial_Phenomenon_UAP_captured_by_fif_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR068：IIRセンサーによるUAP映像とされるクリップ（IIR_1_666・S0151_23・ファイル名より）──NORTHCOM・2023年・米国防省公開・Release 02
変更後: # 【概要版#R02-060】DoW DOW-UAP-PR068：IIRセンサーによるUAP映像とされるクリップ（IIR_1_666・S0151_23・ファイル名より）──NORTHCOM・2023年・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-060 / #2_060 / publish_order: 2060**（2026-06-23 正式採番）  
sourc...
```

### R02-061 / #2_061 / publish_order: 2061

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR069_F_A-18_FLIR_UAP_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR069：F/A-18のFLIRによるUAP映像とされるクリップ（ファイル名より）──NORTHCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-061】DoW DOW-UAP-PR069：F/A-18のFLIRによるUAP映像とされるクリップ（ファイル名より）──NORTHCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-061 / #2_061 / publish_order: 2061**（2026-06-23 正式採番）  
sourc...
```

### R02-063 / #2_063 / publish_order: 2063

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR072_ADMINISTRATIVE_REVISION_IIR_1777_J0032_22_Kazakhstan_UAP_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR072：カザフスタン2022年UAP事案の管理改訂版（ADMINISTRATIVE REVISION）映像──Kazakhstan・米国防省公開・Release 02
変更後: # 【概要版#R02-063】DoW DOW-UAP-PR072：カザフスタン2022年UAP事案の管理改訂版（ADMINISTRATIVE REVISION）映像──Kazakhstan・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-063 / #2_063 / publish_order: 2063**（2026-06-23 正式採番）  
sourc...
```

### R02-064 / #2_064 / publish_order: 2064

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR073：米国中西部2022年・複数UAPとされる事案映像（縦位置・変則解像度608×1080）──Midwestern United States・米国防省公開・Release 02
変更後: # 【概要版#R02-064】DoW DOW-UAP-PR073：米国中西部2022年・複数UAPとされる事案映像（縦位置・変則解像度608×1080）──Midwestern United States・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-064 / #2_064 / publish_order: 2064**（2026-06-23 正式採番）  
sourc...
```

### R02-065 / #2_065 / publish_order: 2065

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR074：CENTCOM管轄2022年6月13日のミッション映像（HD）・雲中のシアンUIと複数のUAP候補点が確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-065】DoW DOW-UAP-PR074：CENTCOM管轄2022年6月13日のミッション映像（HD）・雲中のシアンUIと複数のUAP候補点が確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-065 / #2_065 / publish_order: 2065**（2026-06-23 正式採番）  
sourc...
```

### R02-066 / #2_066 / publish_order: 2066

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR075_09JUN2021_Platform_observed_UAP_in_the_ECS_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR075：東シナ海2021年6月9日・白い線状物体が確認できるUAP事案映像──East China Sea・米国防省公開・Release 02
変更後: # 【概要版#R02-066】DoW DOW-UAP-PR075：東シナ海2021年6月9日・白い線状物体が確認できるUAP事案映像──East China Sea・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-066 / #2_066 / publish_order: 2066**（2026-06-23 正式採番）  
sourc...
```

### R02-067 / #2_067 / publish_order: 2067

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR076：CENTCOM管轄2021年1月3日のUAP観測映像・カラーIR俯瞰で地上景色とマーカーが確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-067】DoW DOW-UAP-PR076：CENTCOM管轄2021年1月3日のUAP観測映像・カラーIR俯瞰で地上景色とマーカーが確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-067 / #2_067 / publish_order: 2067**（2026-06-23 正式採番）  
sourc...
```

### R02-068 / #2_068 / publish_order: 2068

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR077：CENTCOM管轄2020年11月2日のUAP追跡映像（1/2）・水面IRグレースケールでシアン点複数が確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-068】DoW DOW-UAP-PR077：CENTCOM管轄2020年11月2日のUAP追跡映像（1/2）・水面IRグレースケールでシアン点複数が確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-068 / #2_068 / publish_order: 2068**（2026-06-23 正式採番）  
sourc...
```

### R02-069 / #2_069 / publish_order: 2069

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR078：CENTCOM管轄2020年11月2日のUAP追跡映像（2/2）・PR077と一連の事案映像──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-069】DoW DOW-UAP-PR078：CENTCOM管轄2020年11月2日のUAP追跡映像（2/2）・PR077と一連の事案映像──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-069 / #2_069 / publish_order: 2069**（2026-06-23 正式採番）  
sourc...
```

### R02-070 / #2_070 / publish_order: 2070

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAPs_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR079：CENTCOM管轄2020年10月29日・「3つの速く動くUAP」とされる事案映像・シアンUIが確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-070】DoW DOW-UAP-PR079：CENTCOM管轄2020年10月29日・「3つの速く動くUAP」とされる事案映像・シアンUIが確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-070 / #2_070 / publish_order: 2070**（2026-06-23 正式採番）  
sourc...
```

### R02-071 / #2_071 / publish_order: 2071

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR080_20_October_2020_CALLSIGN_CALLSIGN_Observes_UAP_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR080：CENTCOM管轄2020年10月20日のUAP観測映像・水面IR俯瞰映像──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-071】DoW DOW-UAP-PR080：CENTCOM管轄2020年10月20日のUAP観測映像・水面IR俯瞰映像──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-071 / #2_071 / publish_order: 2071**（2026-06-23 正式採番）  
sourc...
```

### R02-072 / #2_072 / publish_order: 2072

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP_AFRICOM_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR081：AFRICOM管轄2020年10月18日のUAP観測映像・地上俯瞰カラーIR映像──AFRICOM・米国防省公開・Release 02
変更後: # 【概要版#R02-072】DoW DOW-UAP-PR081：AFRICOM管轄2020年10月18日のUAP観測映像・地上俯瞰カラーIR映像──AFRICOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-072 / #2_072 / publish_order: 2072**（2026-06-23 正式採番）  
sourc...
```

### R02-073 / #2_073 / publish_order: 2073

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP_AFRICOM_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR082：AFRICOM管轄2020年10月16日のUAP観測映像・グレースケールIR地上俯瞰──AFRICOM・米国防省公開・Release 02
変更後: # 【概要版#R02-073】DoW DOW-UAP-PR082：AFRICOM管轄2020年10月16日のUAP観測映像・グレースケールIR地上俯瞰──AFRICOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-073 / #2_073 / publish_order: 2073**（2026-06-23 正式採番）  
sourc...
```

### R02-074 / #2_074 / publish_order: 2074

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR083：CENTCOM管轄2020年10月7日のUAP観測映像・市街地IRグレースケール俯瞰──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-074】DoW DOW-UAP-PR083：CENTCOM管轄2020年10月7日のUAP観測映像・市街地IRグレースケール俯瞰──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-074 / #2_074 / publish_order: 2074**（2026-06-23 正式採番）  
sourc...
```

### R02-075 / #2_075 / publish_order: 2075

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR084_17_Sept_2020_CALLSIGN_observes_UAP_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR084：CENTCOM管轄2020年9月17日のUAP観測映像・雲中IRグレースケールと小さな内部映像エリア──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-075】DoW DOW-UAP-PR084：CENTCOM管轄2020年9月17日のUAP観測映像・雲中IRグレースケールと小さな内部映像エリア──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-075 / #2_075 / publish_order: 2075**（2026-06-23 正式採番）  
sourc...
```

### R02-076 / #2_076 / publish_order: 2076

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR085_16_Sept_2020_CALLSIGN_observes_UAP_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR085：CENTCOM管轄2020年9月16日のUAP観測映像・均一グレーIRと右付近のUAP候補点が確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-076】DoW DOW-UAP-PR085：CENTCOM管轄2020年9月16日のUAP観測映像・均一グレーIRと右付近のUAP候補点が確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-076 / #2_076 / publish_order: 2076**（2026-06-23 正式採番）  
sourc...
```

### R02-077 / #2_077 / publish_order: 2077

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR086_UAP_from_Dec_2019_East_Coast_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR086：NORTHCOM管轄2019年12月・東海岸で観測された白い球体（オーブ）UAP映像・青い海面上の白い球体が視覚的に明確──NORTHCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-077】DoW DOW-UAP-PR086：NORTHCOM管轄2019年12月・東海岸で観測された白い球体（オーブ）UAP映像・青い海面上の白い球体が視覚的に明確──NORTHCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-077 / #2_077 / publish_order: 2077**（2026-06-23 正式採番）  
sourc...
```

### R02-078 / #2_078 / publish_order: 2078

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR087_05_September_2020_CALLSIGN_UAP_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR087：CENTCOM管轄2020年9月5日のUAP映像・雲中IRグレースケールとシアンUIマーカー──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-078】DoW DOW-UAP-PR087：CENTCOM管轄2020年9月5日のUAP映像・雲中IRグレースケールとシアンUIマーカー──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-078 / #2_078 / publish_order: 2078**（2026-06-23 正式採番）  
sourc...
```

### R02-079 / #2_079 / publish_order: 2079

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR088_31_AUG_CALLSIGN_Observes_UAP_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR088：CENTCOM管轄2020年8月31日のUAP観測映像（本編）・PR089と対になる映像──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-079】DoW DOW-UAP-PR088：CENTCOM管轄2020年8月31日のUAP観測映像（本編）・PR089と対になる映像──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-079 / #2_079 / publish_order: 2079**（2026-06-23 正式採番）  
sourc...
```

### R02-080 / #2_080 / publish_order: 2080

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR089_31_AUG_CALLSIGN_Observes_UAP_part2_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR089：CENTCOM管轄2020年8月31日のUAP観測映像（part2）・中央付近のUAP候補点が確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-080】DoW DOW-UAP-PR089：CENTCOM管轄2020年8月31日のUAP観測映像（part2）・中央付近のUAP候補点が確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-080 / #2_080 / publish_order: 2080**（2026-06-23 正式採番）  
sourc...
```

### R02-081 / #2_081 / publish_order: 2081

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR090_24_AUG_2020_CALLSIGN_Mission_Observes_UAP_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR090：CENTCOM管轄2020年8月24日のUAP観測映像・農地・水田・川・道路の地上俯瞰が確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-081】DoW DOW-UAP-PR090：CENTCOM管轄2020年8月24日のUAP観測映像・農地・水田・川・道路の地上俯瞰が確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-081 / #2_081 / publish_order: 2081**（2026-06-23 正式採番）  
sourc...
```

### R02-082 / #2_082 / publish_order: 2082

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR091_21_AUG_CALLSIGN_Observes_UAP_in_Persian_Gulf_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR091：CENTCOM管轄2020年8月21日・ペルシャ湾でのUAP観測映像・IRで大型船（タンカーとみられる）が鮮明に確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-082】DoW DOW-UAP-PR091：CENTCOM管轄2020年8月21日・ペルシャ湾でのUAP観測映像・IRで大型船（タンカーとみられる）が鮮明に確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-082 / #2_082 / publish_order: 2082**（2026-06-23 正式採番）  
sourc...
```

### R02-083 / #2_083 / publish_order: 2083

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR092_08_AUG_2020_CALLSIGN_UAP_observation_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR092：CENTCOM管轄2020年8月8日のUAP観測映像・ノイズの多いIRグレースケール映像──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-083】DoW DOW-UAP-PR092：CENTCOM管轄2020年8月8日のUAP観測映像・ノイズの多いIRグレースケール映像──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-083 / #2_083 / publish_order: 2083**（2026-06-23 正式採番）  
sourc...
```

### R02-084 / #2_084 / publish_order: 2084

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR093_May_05_2020_Gulf_of_Arabia_Dual_UAP_short_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR093：CENTCOM管轄2020年5月5日・アラビア湾のDual UAP事案映像（短尺版30秒）──Gulf of Arabia・米国防省公開・Release 02
変更後: # 【概要版#R02-084】DoW DOW-UAP-PR093：CENTCOM管轄2020年5月5日・アラビア湾のDual UAP事案映像（短尺版30秒）──Gulf of Arabia・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-084 / #2_084 / publish_order: 2084**（2026-06-23 正式採番）  
sourc...
```

### R02-085 / #2_085 / publish_order: 2085

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR094_CALLSIGN_Mission_HD_2020-02-13_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR094：CENTCOM管轄2020年2月13日のUAP映像・特殊UIの青い帯とグリーンラインが確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-085】DoW DOW-UAP-PR094：CENTCOM管轄2020年2月13日のUAP映像・特殊UIの青い帯とグリーンラインが確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-085 / #2_085 / publish_order: 2085**（2026-06-23 正式採番）  
sourc...
```

### R02-086 / #2_086 / publish_order: 2086

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR095_May_05_2020_Gulf_of_Arabia_Dual_UAP_long_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR095：CENTCOM管轄2020年5月5日・アラビア湾のDual UAP事案映像（長尺版288秒）・PR093と同日同事案の別ファイル──Gulf of Arabia・米国防省公開・Release 02
変更後: # 【概要版#R02-086】DoW DOW-UAP-PR095：CENTCOM管轄2020年5月5日・アラビア湾のDual UAP事案映像（長尺版288秒）・PR093と同日同事案の別ファイル──Gulf of Arabia・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-086 / #2_086 / publish_order: 2086**（2026-06-23 正式採番）  
sourc...
```

### R02-087 / #2_087 / publish_order: 2087

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR096_HH11_03_July_2018_UAPs_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR096：CENTCOM管轄2018年7月3日のUAP映像・Release 02最古の事案の一つ──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-087】DoW DOW-UAP-PR096：CENTCOM管轄2018年7月3日のUAP映像・Release 02最古の事案の一つ──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-087 / #2_087 / publish_order: 2087**（2026-06-23 正式採番）  
sourc...
```

### R02-088 / #2_088 / publish_order: 2088

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR097_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_2135Z_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR097：CENTCOM管轄2019年9月25日21:35Z・Hi-Res（高解像度）UAP観測映像・シアンUIと複数の点が確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-088】DoW DOW-UAP-PR097：CENTCOM管轄2019年9月25日21:35Z・Hi-Res（高解像度）UAP観測映像・シアンUIと複数の点が確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-088 / #2_088 / publish_order: 2088**（2026-06-23 正式採番）  
sourc...
```

### R02-089 / #2_089 / publish_order: 2089

**ファイル：** `note_drafts/ai_summary_DOW-UAP-PR099_Hi-Res_CALLSIGN_Observes_UAP_25SEP19_1715Z_note_version.md`

**タイトル変更：**
```
変更前: # 【概要版#TBD】DoW DOW-UAP-PR099：CENTCOM管轄2019年9月25日17:15Z・Hi-Res（高解像度）UAP観測映像・港湾施設の俯瞰景色とオレンジマーカーが確認できる──CENTCOM・米国防省公開・Release 02
変更後: # 【概要版#R02-089】DoW DOW-UAP-PR099：CENTCOM管轄2019年9月25日17:15Z・Hi-Res（高解像度）UAP観測映像・港湾施設の俯瞰景色とオレンジマーカーが確認できる──CENTCOM・米国防省公開・Release 02
```

**フッター変更：**
```
変更前: ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への...
変更後: 📋 **article_id：R02-089 / #2_089 / publish_order: 2089**（2026-06-23 正式採番）  
sourc...
```

## 4. 更新済みファイル（SKIP: 5件）

| article_id | publish_order | ファイル名 | タイトル |
|---|---|---|---|
| R02-052 | 2052 | `ai_summary_DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_note_version.md` | `# 【概要版#R02-052】DoW DOW-UAP-PR060：球形UAPとされる物体を記録したと...` |
| R02-058 | 2058 | `ai_summary_DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024_note_version.md` | `# 【概要版#R02-058】DoW DOW-UAP-PR066：USCG C-144からの「TIC...` |
| R02-062 | 2062 | `ai_summary_DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron_note_version.md` | `# 【概要版#R02-062】DoW DOW-UAP-PR071：米空軍F-16CがLake Hur...` |
| R02-090 | 2090 | `ai_summary_DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission_note_version.md` | `# 【概要版#R02-090】DoW DOW-UAP-PR052：水面上を移動するUAP編隊（USO...` |
| R02-091 | 2091 | `ai_summary_DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP_note_version.md` | `# 【概要版#R02-091】DoW DOW-UAP-PR070：エグリンAFB乗員が目視確認したと...` |

---

## 7. 実行方法

dry-run 確認後に以下で実行：

```bash
python3 scripts/update_release02_draft_ids.py --execute
```

- 実行時は各ファイルの `.bak` バックアップを自動作成
- `--no-backup` オプションでバックアップをスキップ可
- workflow.db / source_registry.csv は変更しない
