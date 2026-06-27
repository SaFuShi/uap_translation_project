# Frame Delta Analysis Summary (v2)

- 実行日時: 2026-06-27 18:05:55
- article_id: R02-051
- source_id: DOW-UAP-PR059_NAG_UAP_1_Jun_20
- frames_dir: data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20
- 分類器バージョン: frame_delta_v2.py

---

## 基本統計

| 項目 | 値 |
|------|-----|
| 総フレーム数 | 98 |
| 比較ペア数 | 97 |

## イベント別件数

| イベント | 件数 | 説明 |
|---------|------|------|
| CUT | 2 | シーン構造崩壊（brightness急変+tracking失敗+広域変化の3条件） |
| APPEAR | 9 | 輝点出現（bc_prev≈0 → bc_curr 大または相対20倍増） |
| DISAPPEAR | 13 | 輝点消失（bc_curr → 0 またはbc_prev比で75%減） |
| ZOOM_BLOOM | 0 | 輝度急拡大/縮小（bc比5倍以上、centroid安定） |
| CAMERA_TRACK | 0 | カメラ追従（centroid安定 + 背景移動） |
| OBJECT_MOVE | 73 | 対象物移動（centroid移動5px以上または輝度変化） |
| REVIEW_REQUIRED | 0 | 自動判定困難（要人間確認） |
| STATIC | 0 | 変化なし（mean_diff < 2.0） |

---

## 人間確認推奨フレーム

### CUT（scene_structure崩壊）2 件
*(v2: brightness急変 AND tracking失敗 AND 広域変化の3条件すべて必須)*
| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | mean_diff | conc |
|---------|-----------|-----------|---------|---------|-----------|------|
| 93 | frame_0276.png | frame_0279.png | 276.0s | 279.0s | 48.22 | 3.13 |
| 94 | frame_0279.png | frame_0282.png | 279.0s | 282.0s | 32.302 | 4.18 |

### APPEAR（輝点出現）9 件
| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | bc_prev | bc_curr |
|---------|-----------|-----------|---------|---------|---------|---------|
| 1 | frame_0000.png | frame_0003.png | 0.0s | 3.0s | 0 | 4887 |
| 4 | frame_0009.png | frame_0012.png | 9.0s | 12.0s | 0 | 354 |
| 11 | frame_0030.png | frame_0033.png | 30.0s | 33.0s | 74 | 2442 |
| 15 | frame_0042.png | frame_0045.png | 42.0s | 45.0s | 64 | 3181 |
| 74 | frame_0219.png | frame_0222.png | 219.0s | 222.0s | 0 | 726638 |
| 76 | frame_0225.png | frame_0228.png | 225.0s | 228.0s | 0 | 2996 |
| 78 | frame_0231.png | frame_0234.png | 231.0s | 234.0s | 0 | 9937 |
| 95 | frame_0282.png | frame_0285.png | 282.0s | 285.0s | 28 | 2573 |
| 97 | frame_0288.png | frame_0291.png | 288.0s | 291.0s | 0 | 7643 |

### DISAPPEAR（輝点消失）13 件
| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | bc_prev | bc_curr |
|---------|-----------|-----------|---------|---------|---------|---------|
| 2 | frame_0003.png | frame_0006.png | 3.0s | 6.0s | 4887 | 95 |
| 3 | frame_0006.png | frame_0009.png | 6.0s | 9.0s | 95 | 0 |
| 7 | frame_0018.png | frame_0021.png | 18.0s | 21.0s | 598 | 136 |
| 12 | frame_0033.png | frame_0036.png | 33.0s | 36.0s | 2442 | 63 |
| 16 | frame_0045.png | frame_0048.png | 45.0s | 48.0s | 3181 | 72 |
| 24 | frame_0069.png | frame_0072.png | 69.0s | 72.0s | 742 | 60 |
| 30 | frame_0087.png | frame_0090.png | 87.0s | 90.0s | 987 | 67 |
| 73 | frame_0216.png | frame_0219.png | 216.0s | 219.0s | 4930 | 0 |
| 75 | frame_0222.png | frame_0225.png | 222.0s | 225.0s | 726638 | 0 |
| 77 | frame_0228.png | frame_0231.png | 228.0s | 231.0s | 2996 | 0 |
| 79 | frame_0234.png | frame_0237.png | 234.0s | 237.0s | 9937 | 936 |
| 92 | frame_0273.png | frame_0276.png | 273.0s | 276.0s | 5307 | 0 |
| 96 | frame_0285.png | frame_0288.png | 285.0s | 288.0s | 2573 | 0 |

### ZOOM_BLOOM（輝度急変化）0 件
（なし）

### OBJECT_MOVE（対象物移動）73 件
| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | pos_delta_px | mean_diff |
|---------|-----------|-----------|---------|---------|-------------|-----------|
| 5 | frame_0012.png | frame_0015.png | 12.0s | 15.0s | 247.6 | 7.156 |
| 6 | frame_0015.png | frame_0018.png | 15.0s | 18.0s | 78.0 | 8.434 |
| 8 | frame_0021.png | frame_0024.png | 21.0s | 24.0s | 528.0 | 4.851 |
| 9 | frame_0024.png | frame_0027.png | 24.0s | 27.0s | 82.7 | 5.162 |
| 10 | frame_0027.png | frame_0030.png | 27.0s | 30.0s | 366.4 | 5.246 |
| 13 | frame_0036.png | frame_0039.png | 36.0s | 39.0s | 154.8 | 5.403 |
| 14 | frame_0039.png | frame_0042.png | 39.0s | 42.0s | 49.2 | 4.479 |
| 17 | frame_0048.png | frame_0051.png | 48.0s | 51.0s | 352.5 | 3.474 |
| 18 | frame_0051.png | frame_0054.png | 51.0s | 54.0s | 264.1 | 3.13 |
| 19 | frame_0054.png | frame_0057.png | 54.0s | 57.0s | 350.1 | 3.336 |
| 20 | frame_0057.png | frame_0060.png | 57.0s | 60.0s | 56.6 | 2.964 |
| 21 | frame_0060.png | frame_0063.png | 60.0s | 63.0s | 100.8 | 4.149 |
| 22 | frame_0063.png | frame_0066.png | 63.0s | 66.0s | 70.0 | 4.518 |
| 23 | frame_0066.png | frame_0069.png | 66.0s | 69.0s | 642.4 | 3.583 |
| 25 | frame_0072.png | frame_0075.png | 72.0s | 75.0s | 352.4 | 5.863 |
| 26 | frame_0075.png | frame_0078.png | 75.0s | 78.0s | 337.7 | 4.373 |
| 27 | frame_0078.png | frame_0081.png | 78.0s | 81.0s | 18.4 | 5.147 |
| 28 | frame_0081.png | frame_0084.png | 81.0s | 84.0s | 93.2 | 6.278 |
| 29 | frame_0084.png | frame_0087.png | 84.0s | 87.0s | 646.7 | 4.483 |
| 31 | frame_0090.png | frame_0093.png | 90.0s | 93.0s | 54.8 | 3.731 |
| 32 | frame_0093.png | frame_0096.png | 93.0s | 96.0s | 257.4 | 26.219 |
| 33 | frame_0096.png | frame_0099.png | 96.0s | 99.0s | 1.0 | 10.37 |
| 34 | frame_0099.png | frame_0102.png | 99.0s | 102.0s | 1.4 | 4.805 |
| 35 | frame_0102.png | frame_0105.png | 102.0s | 105.0s | 25.0 | 4.146 |
| 36 | frame_0105.png | frame_0108.png | 105.0s | 108.0s | 33.1 | 3.328 |
| 37 | frame_0108.png | frame_0111.png | 108.0s | 111.0s | 6.1 | 3.729 |
| 38 | frame_0111.png | frame_0114.png | 111.0s | 114.0s | 27.8 | 4.892 |
| 39 | frame_0114.png | frame_0117.png | 114.0s | 117.0s | 2.2 | 3.751 |
| 40 | frame_0117.png | frame_0120.png | 117.0s | 120.0s | 0.0 | 3.43 |
| 41 | frame_0120.png | frame_0123.png | 120.0s | 123.0s | 0.0 | 4.162 |
| 42 | frame_0123.png | frame_0126.png | 123.0s | 126.0s | 1.0 | 4.735 |
| 43 | frame_0126.png | frame_0129.png | 126.0s | 129.0s | 1.0 | 4.954 |
| 44 | frame_0129.png | frame_0132.png | 129.0s | 132.0s | 1.0 | 4.459 |
| 45 | frame_0132.png | frame_0135.png | 132.0s | 135.0s | 2.2 | 4.677 |
| 46 | frame_0135.png | frame_0138.png | 135.0s | 138.0s | 3.2 | 3.79 |
| 47 | frame_0138.png | frame_0141.png | 138.0s | 141.0s | 107.2 | 26.841 |
| 48 | frame_0141.png | frame_0144.png | 141.0s | 144.0s | 3.2 | 3.72 |
| 49 | frame_0144.png | frame_0147.png | 144.0s | 147.0s | 3.0 | 5.551 |
| 50 | frame_0147.png | frame_0150.png | 147.0s | 150.0s | 3.6 | 5.637 |
| 51 | frame_0150.png | frame_0153.png | 150.0s | 153.0s | 6.1 | 4.041 |
| 52 | frame_0153.png | frame_0156.png | 153.0s | 156.0s | 1.4 | 3.958 |
| 53 | frame_0156.png | frame_0159.png | 156.0s | 159.0s | 1.4 | 3.854 |
| 54 | frame_0159.png | frame_0162.png | 159.0s | 162.0s | 0.0 | 4.361 |
| 55 | frame_0162.png | frame_0165.png | 162.0s | 165.0s | 2.0 | 3.826 |
| 56 | frame_0165.png | frame_0168.png | 165.0s | 168.0s | 43.0 | 3.901 |
| 57 | frame_0168.png | frame_0171.png | 168.0s | 171.0s | 101.2 | 4.561 |
| 58 | frame_0171.png | frame_0174.png | 171.0s | 174.0s | 9.5 | 4.152 |
| 59 | frame_0174.png | frame_0177.png | 174.0s | 177.0s | 0.0 | 4.076 |
| 60 | frame_0177.png | frame_0180.png | 177.0s | 180.0s | 2.0 | 4.267 |
| 61 | frame_0180.png | frame_0183.png | 180.0s | 183.0s | 3.2 | 4.291 |
| 62 | frame_0183.png | frame_0186.png | 183.0s | 186.0s | 2.2 | 3.837 |
| 63 | frame_0186.png | frame_0189.png | 186.0s | 189.0s | 88.8 | 18.757 |
| 64 | frame_0189.png | frame_0192.png | 189.0s | 192.0s | 10.8 | 4.746 |
| 65 | frame_0192.png | frame_0195.png | 192.0s | 195.0s | 10.8 | 5.143 |
| 66 | frame_0195.png | frame_0198.png | 195.0s | 198.0s | 8.2 | 7.241 |
| 67 | frame_0198.png | frame_0201.png | 198.0s | 201.0s | 10.6 | 4.749 |
| 68 | frame_0201.png | frame_0204.png | 201.0s | 204.0s | 4.5 | 5.668 |
| 69 | frame_0204.png | frame_0207.png | 204.0s | 207.0s | 4.2 | 5.447 |
| 70 | frame_0207.png | frame_0210.png | 207.0s | 210.0s | 2.0 | 5.001 |
| 71 | frame_0210.png | frame_0213.png | 210.0s | 213.0s | 6.3 | 4.676 |
| 72 | frame_0213.png | frame_0216.png | 213.0s | 216.0s | 1.4 | 5.322 |
| 80 | frame_0237.png | frame_0240.png | 237.0s | 240.0s | 2.8 | 4.4 |
| 81 | frame_0240.png | frame_0243.png | 240.0s | 243.0s | 99.3 | 18.229 |
| 82 | frame_0243.png | frame_0246.png | 243.0s | 246.0s | 6.0 | 4.746 |
| 83 | frame_0246.png | frame_0249.png | 246.0s | 249.0s | 5.0 | 4.934 |
| 84 | frame_0249.png | frame_0252.png | 249.0s | 252.0s | 10.4 | 5.27 |
| 85 | frame_0252.png | frame_0255.png | 252.0s | 255.0s | 6.0 | 4.654 |
| 86 | frame_0255.png | frame_0258.png | 255.0s | 258.0s | 5.0 | 5.723 |
| 87 | frame_0258.png | frame_0261.png | 258.0s | 261.0s | 5.1 | 5.92 |
| 88 | frame_0261.png | frame_0264.png | 261.0s | 264.0s | 9.5 | 5.425 |
| 89 | frame_0264.png | frame_0267.png | 264.0s | 267.0s | 5.0 | 4.792 |
| 90 | frame_0267.png | frame_0270.png | 267.0s | 270.0s | 5.0 | 4.861 |
| 91 | frame_0270.png | frame_0273.png | 270.0s | 273.0s | 2.2 | 4.573 |

### CAMERA_TRACK（カメラ追従）0 件
（なし）

### REVIEW_REQUIRED（要確認）0 件
（なし）

---

## 高変化量区間（mean_diff 上位10件）

| pair_id | frame_prev | frame_curr | ts_prev | ts_curr | mean_diff | event_type |
|---------|-----------|-----------|---------|---------|-----------|------------|
| 75 | frame_0222.png | frame_0225.png | 222.0s | 225.0s | 105.734 | DISAPPEAR |
| 74 | frame_0219.png | frame_0222.png | 219.0s | 222.0s | 54.532 | APPEAR |
| 93 | frame_0276.png | frame_0279.png | 276.0s | 279.0s | 48.22 | CUT |
| 79 | frame_0234.png | frame_0237.png | 234.0s | 237.0s | 41.546 | DISAPPEAR |
| 95 | frame_0282.png | frame_0285.png | 282.0s | 285.0s | 39.139 | APPEAR |
| 96 | frame_0285.png | frame_0288.png | 285.0s | 288.0s | 39.102 | DISAPPEAR |
| 77 | frame_0228.png | frame_0231.png | 228.0s | 231.0s | 36.842 | DISAPPEAR |
| 76 | frame_0225.png | frame_0228.png | 225.0s | 228.0s | 36.82 | APPEAR |
| 1 | frame_0000.png | frame_0003.png | 0.0s | 3.0s | 34.046 | APPEAR |
| 94 | frame_0279.png | frame_0282.png | 279.0s | 282.0s | 32.302 | CUT |

---

## VLM 解析推奨フレーム候補

以下のフレームを優先的に VLM へ渡すことを推奨します（97 件）。

| frame | timestamp_s | event_type |
|-------|------------|------------|
| frame_0000.png | 0.0s | APPEAR |
| frame_0003.png | 3.0s | APPEAR |
| frame_0006.png | 6.0s | DISAPPEAR |
| frame_0009.png | 9.0s | DISAPPEAR |
| frame_0012.png | 12.0s | APPEAR |
| frame_0015.png | 15.0s | OBJECT_MOVE |
| frame_0018.png | 18.0s | OBJECT_MOVE |
| frame_0021.png | 21.0s | DISAPPEAR |
| frame_0024.png | 24.0s | OBJECT_MOVE |
| frame_0027.png | 27.0s | OBJECT_MOVE |
| frame_0030.png | 30.0s | OBJECT_MOVE |
| frame_0033.png | 33.0s | APPEAR |
| frame_0036.png | 36.0s | DISAPPEAR |
| frame_0039.png | 39.0s | OBJECT_MOVE |
| frame_0042.png | 42.0s | OBJECT_MOVE |
| frame_0045.png | 45.0s | APPEAR |
| frame_0048.png | 48.0s | DISAPPEAR |
| frame_0051.png | 51.0s | OBJECT_MOVE |
| frame_0054.png | 54.0s | OBJECT_MOVE |
| frame_0057.png | 57.0s | OBJECT_MOVE |
| frame_0060.png | 60.0s | OBJECT_MOVE |
| frame_0063.png | 63.0s | OBJECT_MOVE |
| frame_0066.png | 66.0s | OBJECT_MOVE |
| frame_0069.png | 69.0s | OBJECT_MOVE |
| frame_0072.png | 72.0s | DISAPPEAR |
| frame_0075.png | 75.0s | OBJECT_MOVE |
| frame_0078.png | 78.0s | OBJECT_MOVE |
| frame_0081.png | 81.0s | OBJECT_MOVE |
| frame_0084.png | 84.0s | OBJECT_MOVE |
| frame_0087.png | 87.0s | OBJECT_MOVE |
| frame_0090.png | 90.0s | DISAPPEAR |
| frame_0093.png | 93.0s | OBJECT_MOVE |
| frame_0096.png | 96.0s | OBJECT_MOVE |
| frame_0099.png | 99.0s | OBJECT_MOVE |
| frame_0102.png | 102.0s | OBJECT_MOVE |
| frame_0105.png | 105.0s | OBJECT_MOVE |
| frame_0108.png | 108.0s | OBJECT_MOVE |
| frame_0111.png | 111.0s | OBJECT_MOVE |
| frame_0114.png | 114.0s | OBJECT_MOVE |
| frame_0117.png | 117.0s | OBJECT_MOVE |
| frame_0120.png | 120.0s | OBJECT_MOVE |
| frame_0123.png | 123.0s | OBJECT_MOVE |
| frame_0126.png | 126.0s | OBJECT_MOVE |
| frame_0129.png | 129.0s | OBJECT_MOVE |
| frame_0132.png | 132.0s | OBJECT_MOVE |
| frame_0135.png | 135.0s | OBJECT_MOVE |
| frame_0138.png | 138.0s | OBJECT_MOVE |
| frame_0141.png | 141.0s | OBJECT_MOVE |
| frame_0144.png | 144.0s | OBJECT_MOVE |
| frame_0147.png | 147.0s | OBJECT_MOVE |
| frame_0150.png | 150.0s | OBJECT_MOVE |
| frame_0153.png | 153.0s | OBJECT_MOVE |
| frame_0156.png | 156.0s | OBJECT_MOVE |
| frame_0159.png | 159.0s | OBJECT_MOVE |
| frame_0162.png | 162.0s | OBJECT_MOVE |
| frame_0165.png | 165.0s | OBJECT_MOVE |
| frame_0168.png | 168.0s | OBJECT_MOVE |
| frame_0171.png | 171.0s | OBJECT_MOVE |
| frame_0174.png | 174.0s | OBJECT_MOVE |
| frame_0177.png | 177.0s | OBJECT_MOVE |
| frame_0180.png | 180.0s | OBJECT_MOVE |
| frame_0183.png | 183.0s | OBJECT_MOVE |
| frame_0186.png | 186.0s | OBJECT_MOVE |
| frame_0189.png | 189.0s | OBJECT_MOVE |
| frame_0192.png | 192.0s | OBJECT_MOVE |
| frame_0195.png | 195.0s | OBJECT_MOVE |
| frame_0198.png | 198.0s | OBJECT_MOVE |
| frame_0201.png | 201.0s | OBJECT_MOVE |
| frame_0204.png | 204.0s | OBJECT_MOVE |
| frame_0207.png | 207.0s | OBJECT_MOVE |
| frame_0210.png | 210.0s | OBJECT_MOVE |
| frame_0213.png | 213.0s | OBJECT_MOVE |
| frame_0216.png | 216.0s | OBJECT_MOVE |
| frame_0219.png | 219.0s | DISAPPEAR |
| frame_0222.png | 222.0s | APPEAR |
| frame_0225.png | 225.0s | DISAPPEAR |
| frame_0228.png | 228.0s | APPEAR |
| frame_0231.png | 231.0s | DISAPPEAR |
| frame_0234.png | 234.0s | APPEAR |
| frame_0237.png | 237.0s | DISAPPEAR |
| frame_0240.png | 240.0s | OBJECT_MOVE |
| frame_0243.png | 243.0s | OBJECT_MOVE |
| frame_0246.png | 246.0s | OBJECT_MOVE |
| frame_0249.png | 249.0s | OBJECT_MOVE |
| frame_0252.png | 252.0s | OBJECT_MOVE |
| frame_0255.png | 255.0s | OBJECT_MOVE |
| frame_0258.png | 258.0s | OBJECT_MOVE |
| frame_0261.png | 261.0s | OBJECT_MOVE |
| frame_0264.png | 264.0s | OBJECT_MOVE |
| frame_0267.png | 267.0s | OBJECT_MOVE |
| frame_0270.png | 270.0s | OBJECT_MOVE |
| frame_0273.png | 273.0s | OBJECT_MOVE |
| frame_0276.png | 276.0s | DISAPPEAR |
| frame_0279.png | 279.0s | CUT |
| frame_0282.png | 282.0s | CUT |
| frame_0285.png | 285.0s | APPEAR |
| frame_0288.png | 288.0s | DISAPPEAR |
| frame_0291.png | 291.0s | APPEAR |

---

## CUT 判定ロジック（v2）

```
CUT = (mean_diff >= 30.0)          # 条件A: brightness急変
    AND (not prev_has OR not curr_has)  # 条件B: object tracking 失敗
    AND (conc < 5.5)               # 条件C: scene_structure破綻（広域変化）

大型オブジェクト（bc >> 20）が両フレームに存在 → track_fail=False → CUT不成立
bc は CUT 判定基準に直接使用しない（OBJECT_TRACKING 補助のみ）
```
