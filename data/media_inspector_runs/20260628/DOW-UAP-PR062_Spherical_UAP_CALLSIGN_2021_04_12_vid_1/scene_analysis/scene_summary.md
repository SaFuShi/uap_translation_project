# Scene Analyzer Summary

- 実行日時   : 2026-06-28 22:17:46
- article_id : R02-054
- source_id  : DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1
- frames_dir : data/adaptive_frames/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1
- 分類器     : scene_analyzer_v1
- フレーム数 : 97

---

## 背景種別 集計

| scene_type | 件数 | 割合 | 説明 |
|-----------|------|------|------|
| ground_surface | 61 | 62.9% | 地表面 |
| unknown | 28 | 28.9% | 判定不能 |
| cloud | 8 | 8.2% | 雲面 |

## 地表サブタイプ（ground_surface フレームのみ）

| ground_subtype | 件数 |
|---------------|------|
| rocky | 51 |
| unknown | 6 |
| arid | 4 |

## センサーモード / 照明種別

| センサーモード | 件数 | 割合 |
|--------------|------|------|
| color | 97 | 100.0% |

| 照明種別 | 件数 |
|---------|------|
| daytime | 97 |

## センサーモード別 判定前提

**主要センサーモード: `color`**

> 可視光カラー映像。輝度による地表/雲識別が有効（可視光の雲は白い）。現在の分類ロジックを最大信頼度で使用する。

✅ **カラー映像確認済み**: 輝度による地表/雲識別が有効です。
現在の分類結果は最大信頼度で使用できます。


## 平均特徴量

| 特徴量 | 平均値 |
|-------|--------|
| edge_density | 0.01080 |
| spatial_freq_ratio | 0.08899 |
| texture_variance | 3.94 |
| scene_confidence | 0.558 |
| masked_pixel_ratio | 0.186 |

---

## 総合判定（多数決）

- **scene_type : ground_surface**（地表面）
- ground_subtype : rocky
- lighting_type : daytime
- sensor_mode   : color
- ✅ 分類信頼度: カラー映像・輝度識別有効

## PR062 期待値との比較

| 期待値 | 本結果 | 判定 |
|-------|--------|------|
| scene_type = ground_surface | ground_surface | ✅ |
| ground_subtype = rocky/arid | rocky | ✅ |
| sensor_mode = color | color | ✅ |