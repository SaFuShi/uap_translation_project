# Camera Analyzer Summary

- 実行日時   : 2026-06-29 09:30:39
- article_id : R02-054
- source_id  : DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1
- frames_dir : data/adaptive_frames/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_targeted
- 分類器     : camera_analyzer_v1
- 解析ペア数 : 152

---

## カメライベント 集計

| camera_event | 件数 | 割合 |
|-------------|------|------|
| STATIC | 108 | 71.1% |
| PAN | 24 | 15.8% |
| FOV_IN | 10 | 6.6% |
| FOV_OUT | 7 | 4.6% |
| TILT | 1 | 0.7% |
| EDGE_SURGE | 1 | 0.7% |
| COMBINED | 1 | 0.7% |

## 検出イベント詳細

**BLACKOUT 検出**: 検出なし

**WHITEOUT 検出**: 検出なし

**FOV_IN 検出（ズームイン方向）** (10 件)

| 時刻 (s) | フレーム | camera_event | 指標 | notes |
|---------|---------|-------------|------|-------|
| 22.50 | frame_000225d.png | FOV_IN | hf_ratio=3.22 ed_ratio=0.9 | 高周波比↑ (0.054→0.172 ×3.22): ズームイン方向 FOV 変化候補（地形テクスチャ変化との混同注意・… |
| 24.50 | frame_000245d.png | FOV_IN | hf_ratio=3.16 ed_ratio=1.0 | 高周波比↑ (0.063→0.200 ×3.16): ズームイン方向 FOV 変化候補（地形テクスチャ変化との混同注意・… |
| 52.50 | frame_000525d.png | FOV_IN | hf_ratio=3.34 ed_ratio=1.0 | 高周波比↑ (0.057→0.188 ×3.34): ズームイン方向 FOV 変化候補（地形テクスチャ変化との混同注意・… |
| 53.80 | frame_000538d.png | FOV_IN | hf_ratio=2.91 ed_ratio=1.1 | 高周波比↑ (0.061→0.176 ×2.91): ズームイン方向 FOV 変化候補（地形テクスチャ変化との混同注意・… |
| 55.50 | frame_000555d.png | FOV_IN | hf_ratio=2.54 ed_ratio=1.1 | 高周波比↑ (0.034→0.086 ×2.54): ズームイン方向 FOV 変化候補（地形テクスチャ変化との混同注意・… |
| 126.20 | frame_001262d.png | FOV_IN | hf_ratio=3.34 ed_ratio=0.6 | 高周波比↑ (0.077→0.256 ×3.34): ズームイン方向 FOV 変化候補（地形テクスチャ変化との混同注意・… |
| 127.50 | frame_001275d.png | FOV_IN | hf_ratio=3.37 ed_ratio=1.0 | 高周波比↑ (0.038→0.127 ×3.37): ズームイン方向 FOV 変化候補（地形テクスチャ変化との混同注意・… |
| 247.00 | frame_002470d.png | FOV_IN | hf_ratio=2.56 ed_ratio=1.0 | 高周波比↑ (0.032→0.083 ×2.56): ズームイン方向 FOV 変化候補（地形テクスチャ変化との混同注意・… |
| 250.80 | frame_002508d.png | FOV_IN | hf_ratio=2.19 ed_ratio=1.0 | 高周波比↑ (0.178→0.390 ×2.19): ズームイン方向 FOV 変化候補（地形テクスチャ変化との混同注意・… |
| 253.80 | frame_002538d.png | FOV_IN | hf_ratio=2.17 ed_ratio=1.0 | 高周波比↑ (0.052→0.112 ×2.17): ズームイン方向 FOV 変化候補（地形テクスチャ変化との混同注意・… |

**FOV_OUT 検出（ズームアウト方向）** (7 件)

| 時刻 (s) | フレーム | camera_event | 指標 | notes |
|---------|---------|-------------|------|-------|
| 22.80 | frame_000228d.png | FOV_OUT | hf_ratio=0.37 ed_ratio=1.0 | 高周波比↓ (0.172→0.064 ×0.37): ズームアウト方向 FOV 変化候補（地形テクスチャ変化との混同注意… |
| 53.20 | frame_000532d.png | FOV_OUT | hf_ratio=0.27 ed_ratio=1.0 | 高周波比↓ (0.252→0.068 ×0.27): ズームアウト方向 FOV 変化候補（地形テクスチャ変化との混同注意… |
| 54.20 | frame_000542d.png | FOV_OUT | hf_ratio=0.40 ed_ratio=1.1 | 高周波比↓ (0.176→0.070 ×0.40): ズームアウト方向 FOV 変化候補（地形テクスチャ変化との混同注意… |
| 55.20 | frame_000552d.png | FOV_OUT | hf_ratio=0.37 ed_ratio=1.1 | 高周波比↓ (0.092→0.034 ×0.37): ズームアウト方向 FOV 変化候補（地形テクスチャ変化との混同注意… |
| 121.00 | frame_001210d.png | FOV_OUT | hf_ratio=0.38 ed_ratio=2.2 | 高周波比↓ (0.151→0.057 ×0.38): ズームアウト方向 FOV 変化候補（地形テクスチャ変化との混同注意… |
| 251.50 | frame_002515d.png | FOV_OUT | hf_ratio=0.33 ed_ratio=1.0 | 高周波比↓ (0.316→0.105 ×0.33): ズームアウト方向 FOV 変化候補（地形テクスチャ変化との混同注意… |
| 252.80 | frame_002528d.png | FOV_OUT | hf_ratio=0.20 ed_ratio=1.0 | 高周波比↓ (0.222→0.045 ×0.20): ズームアウト方向 FOV 変化候補（地形テクスチャ変化との混同注意… |

**EDGE_SURGE 検出（エッジ密度急増）** (1 件)

| 時刻 (s) | フレーム | camera_event | 指標 | notes |
|---------|---------|-------------|------|-------|
| 255.50 | frame_002555d.png | EDGE_SURGE | ed_ratio=22.6 | hf 値が低いため FOV 比較スキップ (prev=0.173, curr=0.000); エッジ密度急増 (0.00… |

**COMBINED 検出（複合イベント）** (1 件)

| 時刻 (s) | フレーム | camera_event | 指標 | notes |
|---------|---------|-------------|------|-------|
| 256.00 | frame_002560d.png | COMBINED | hf_ratio=0.27 ed_ratio=3.3 | 高周波比↓ (0.251→0.067 ×0.27): ズームアウト方向 FOV 変化候補（地形テクスチャ変化との混同注意… |

## カメラパン統計

- 解析ペア数 (pan_conf ≥ 0.25): 152 件
- 平均背景変位 dx=-7.9px, dy=-3.7px

> 正の dx = 背景が右へ移動 = カメラが左へパン（UAP が左方向へ移動中に追跡している場合に発生）
> 正の dy = 背景が下へ移動 = カメラが上へチルト

## PR062 期待値との比較（Ground Truth 対応）

| GT イベント | 期待検出 | 本結果 | 判定 |
|-----------|---------|--------|------|
| FOV_SWITCH@25s (ワイド切替) | FOV_IN, FOV_OUT, COMBINED | フレームなし | — |
| ZOOM_IN@52s (ズーム画角) | COMBINED, FOV_IN | フレームなし | — |
| ZOOM_IN@124s (ズーム画角) | COMBINED, FOV_IN | フレームなし | — |
| ZOOM_OUT@249s (望遠→ワイド) | COMBINED, FOV_OUT | フレームなし | — |
| ZOOM_OUT@249s (望遠→ワイド) | COMBINED, FOV_OUT | フレームなし | — |
| BLACKOUT+WHITEOUT@256s | WHITEOUT, BLACKOUT, EDGE_SURGE, COMBINED | フレームなし | — |

## 検出限界 (3秒サンプリング)

> 3秒サンプリング時の検出限界: ブラックアウト/ホワイトアウトが3秒未満の場合、サンプルフレームに現れず直接検出不能。FOV切替は空間周波数比の変化で検出するが、地形テクスチャの自然変化と混同する場合がある。

## Motion Intelligence v4 連携メモ

- `cam_dx_px`, `cam_dy_px`: フレームペアごとの背景変位推定。MI v4 の `camera_compensated` モード入力として利用可能。
- `camera_event = FOV_IN / FOV_OUT / COMBINED`: 当該ペアの Motion 解析を **スキップまたは要注意** とマーク推奨。
- `camera_event = STATIC / PAN / TILT` かつ `pan_confidence ≥ 0.5`: 信頼できるパン補正ベクトルとして利用可能。
