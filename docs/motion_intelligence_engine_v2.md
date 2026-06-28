# Motion Intelligence Engine v2 設計書

- 作成日: 2026-06-27
- 前バージョン: `docs/motion_intelligence_engine_v1.md`
- 対象スクリプト: `scripts/motion_intelligence_v2.py`（未実装）
- ステータス: 設計承認待ち

---

## 1. 背景・目的

### 1.1 v1 の成果と限界

**v1 成果（PR061 検証）:**
- Frame Delta v2 の OBJECT_MOVE=93 件が地形・照明・視差変化だったことを定量的に確認
- FFT Phase Correlation により探索窓制限なしでグローバルシフト推定を実現
- バウンディングボックス面積比（bbox_ratio）による LSC 判別が機能

**v1 の限界（PR061 での UAP 未検出）:**
1. **固定閾値の失敗**: `residual_thresh=12.0` が低すぎ、全セルが候補化→全 LSC
2. **適応性なし**: 地形の複雑さ（テクスチャ密度・パラックス量）に無関係な固定値
3. **時間軸なし**: 単一フレームペアのみ解析、連続フレームでの追跡なし
4. **3秒間隔の限界**: カメラ追跡補正で bg=(0,0)、UAP の変位が背景ノイズに埋没

### 1.2 PR061 における物理的考察

PR061 は **カメラが UAP をアクティブ追跡する昼間カラー俯瞰映像**。

```
カメラの動き:
  航空機の移動 → カメラがパン補正 → 地形の見かけ変位 ≈ 0 (位相相関 bg=(0,0))

フレーム間変化の構造:
  3秒間隔: 山岳地形のパラックス変化 → 全域で残差 MAD 20〜35
  1秒間隔: パラックス変化が 1/3 → 残差 MAD 8〜15 程度（推定）

UAP の動き:
  183s〜189s: 右上から下方へ約 17px/s の見かけ速度（推定）
  3秒間隔での変位: 約 51px ≈ 1.6 グリッドセル（32px）
  → UAP が完全にセルを離れるため「残差が非常に高い」
  1秒間隔での変位: 約 17px ≈ 0.5 グリッドセル
  → UAP セルが部分重複、残差は中程度だが一方向ドリフトが顕在
```

### 1.3 v2 の目標

1. **適応的閾値**: フレームペアごとの残差分布に基づく動的閾値（固定値廃止）
2. **時間的一貫性**: 連続フレームで「移動する候補スポット」を追跡
3. **Targeted Frames 対応**: 1秒間隔フレームでの高精度解析モード
4. **PR061 検証**: 183s 付近の PTA/ROM 検出、189s PTD の確認

---

## 2. v1 との差分

| 項目 | v1 | v2 |
|------|----|----|
| 閾値方式 | 固定値（12.0） | 各ペアの残差 p90 (適応的) |
| 時間軸解析 | なし（単一ペア） | スライディングウィンドウ（W ペア） |
| 対応フレーム種別 | adaptive only | adaptive + targeted |
| 背景推定 | FFT Phase Correlation | 同左（継続） |
| LSC vs ROM 判別 | bbox_ratio のみ | bbox_ratio + 時間的ドリフト |
| 出力 CSV | motion_events.csv | motion_events_v2.csv + track_events.csv |
| 候補追跡 | なし | track_id 付与・線形モデルフィッティング |

---

## 3. アルゴリズム設計

### 3.1 処理フロー概要

```
[入力] frames_dir (adaptive または targeted)
          ↓
[Phase 1] フレームペア解析（適応的残差閾値）
  ├─ FFT Phase Correlation → (bg_dx, bg_dy, bg_mag)
  ├─ 全グリッドセルの残差 MAD 計算
  ├─ 適応的閾値 = max(percentile(residuals, P90), MIN_RESIDUAL)
  ├─ 候補セル = residual > 適応的閾値
  ├─ クラスタリング（4連結 Union-Find）
  └─ ペアごとの最大クラスタ情報（bbox, centroid, mean_residual）
          ↓
[Phase 2] 時間的一貫性分析（W ペアのスライディングウィンドウ）
  ├─ セル単位出現カウント（N_PREV ペア遡って集計）
  ├─ 出現回数 ≥ T_MIN → 持続候補（persistent candidate）
  ├─ 持続候補のクラスタリング（時空間）
  └─ クラスタ centroid の時系列記録
          ↓
[Phase 3] 空間追跡・分類
  ├─ centroid の線形回帰（R², ドリフト量）
  ├─ 線形運動 → ROM / PTA / PTD
  ├─ 定常異常 → REVIEW_REQUIRED
  └─ ランダム散在 → LSC (降格)
          ↓
[出力]
  ├─ motion_events_v2.csv (per-pair)
  ├─ track_events.csv (per-track)
  └─ summary.md
```

### 3.2 Phase 1: フレームペア解析（適応的閾値）

#### 3.2.1 残差分布の計算

各有効グリッドセルで残差 MAD を計算（v1 と同一）:

```python
residual_all = []
for gi, gj, y0, x0 in iter_valid_cells(h, w, gs, mask_top, mask_bot):
    if std(prev[y0:y0+gs]) < TEXTURE_STD_MIN: continue
    rmad = residual_mad(prev, curr, y0, x0, gs, bg_dx, bg_dy)
    if not isnan(rmad):
        residual_all.append((gi, gj, rmad))
```

#### 3.2.2 適応的閾値

```python
all_residual_values = [r for _, _, r in residual_all]
p_thresh = np.percentile(all_residual_values, PERCENTILE_CANDIDATE)  # default: 90
adaptive_thresh = max(p_thresh, MIN_RESIDUAL)  # フロア値でゼロ分散ペアを防ぐ

# 候補セル: 残差が適応的閾値を超える上位 (100-PERCENTILE)% のセル
candidates = {(gi, gj) for gi, gj, r in residual_all if r >= adaptive_thresh}
```

**パラメータ:**
- `PERCENTILE_CANDIDATE = 90`（上位 10% が候補）
- `MIN_RESIDUAL = 8.0`（フロア値。静止フレームで全セルが候補化するのを防ぐ）

**効果:**
- 全フレームペアで常に有効セルの約 10% が候補化
- 地形パラックスが激しいペアでも「その中での外れ値」を抽出
- UAP セル（完全にセルを離れた高残差）が地形ノイズより高い残差を持てば検出可能

#### 3.2.3 クラスタリングと bbox 計算（v1 継続）

4連結 Union-Find によるクラスタリング。最大クラスタの bbox_ratio で LSC vs 候補を一次分類。

### 3.3 Phase 2: 時間的一貫性分析

#### 3.3.1 スライディングウィンドウ

```python
TEMPORAL_WINDOW = W   # default: 3 (adaptive), 5 (targeted)
TEMPORAL_MIN    = T   # default: 2 (W の 60% 以上に出現)

# ウィンドウ: 現在のペア含む直近 W ペアのセル出現履歴
cell_history = deque(maxlen=W)  # 各要素: set of (gi, gj) candidates

# 現在ペアの候補追加
cell_history.append(current_pair_candidates)

# W ペア分の累積カウント
cell_count = Counter()
for candidate_set in cell_history:
    cell_count.update(candidate_set)

# 持続候補 = W ペア中 T_MIN 回以上出現
persistent = {cell for cell, cnt in cell_count.items() if cnt >= TEMPORAL_MIN}
```

#### 3.3.2 時空間クラスタリング

持続候補セルを4連結でクラスタリング → 「持続クラスタ」を生成。

各持続クラスタに **track_id** を付与。

#### 3.3.3 Centroid 時系列の記録

track_id ごとに、各ペアでの centroid 座標 (cx, cy) を記録:

```python
tracks[track_id]["centroids"].append({
    "pair_id": pair_id,
    "timestamp_s": timestamp_curr_s,
    "cx": cx, "cy": cy,
    "n_cells": n_cells_in_cluster,
})
```

### 3.4 Phase 3: 空間追跡・イベント分類

#### 3.4.1 線形回帰フィッティング

各 track_id のクラスタ centroid 時系列に線形回帰を適用:

```python
import numpy as np

ts = np.array([c["timestamp_s"] for c in track["centroids"]])
xs = np.array([c["cx"] for c in track["centroids"]])
ys = np.array([c["cy"] for c in track["centroids"]])

# 線形フィット: cx = a*t + b, cy = c*t + d
if len(ts) >= 3:
    px = np.polyfit(ts, xs, 1)
    py = np.polyfit(ts, ys, 1)
    
    # R² 計算
    r2_x = r_squared(ts, xs, px)
    r2_y = r_squared(ts, ys, py)
    r2_mean = (r2_x + r2_y) / 2
    
    # ドリフト速度 (px/s)
    drift_x_per_s = px[0]
    drift_y_per_s = py[0]
    drift_mag_per_s = sqrt(drift_x_per_s**2 + drift_y_per_s**2)
else:
    r2_mean = 0.0
    drift_mag_per_s = 0.0
```

#### 3.4.2 Track イベント分類

| 条件 | track_event_type |
|------|-----------------|
| n_pairs=1 | SINGLE_APPEARANCE（低信頼度、要確認） |
| n_pairs≥2 AND drift_mag<1.0 px/s | STATIONARY_ANOMALY（定常異常）|
| n_pairs≥2 AND drift_mag≥1.0 AND R²≥0.60 | LINEAR_MOTION（線形運動候補） |
| n_pairs≥2 AND drift_mag≥1.0 AND R²<0.60 | ERRATIC_MOTION（不規則、ノイズ可能性）|
| 持続クラスタの前ペアが空 | TRACK_APPEAR（出現） |
| 持続クラスタの後ペアが空 | TRACK_DISAPPEAR（消失） |

#### 3.4.3 Per-pair イベント分類（v2 版）

Track 情報を使ったフォールバック判定:

```
イベント優先順位:
  1. STATIC: bg_mag < 2.0 AND 候補なし
  2. LIGHTING_SHADOW_CHANGE: bbox_ratio ≥ 0.08（v1 継続）
  3. POSSIBLE_TARGET_APPEAR: 前ペアに track_id なし → 現ペアに LINEAR_MOTION/STATIONARY_ANOMALY の track
  4. POSSIBLE_TARGET_DISAPPEAR: 前ペアに track → 現ペアに track なし
  5. CAMERA_TRACK: bg_mag ≥ 20 AND uniformity ≥ 0.6
  6. RELATIVE_OBJECT_MOTION: LINEAR_MOTION track あり
  7. BACKGROUND_FLOW: bg_mag ≥ 2.0 AND 候補なし
  8. REVIEW_REQUIRED: STATIONARY_ANOMALY または条件未満
```

---

## 4. Targeted Frames モード

### 4.1 格納ディレクトリ

PR061 の targeted frames:
```
data/adaptive_frames/20260627/
└── DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted/
    ├── frame_00180.png  (180s)
    ├── frame_00181.png  (181s)
    ├── frame_00182.png  (182s)
    ├── frame_00183.png  (183s)   ← UAP 出現推定点
    ├── frame_00184.png  (184s)
    ├── ...
    └── frame_00198.png  (198s)   ← 再出現後
```

カバー区間（6ゾーン）:
| ゾーン | 時刻 | トリガー理由 | UAP 関連性 |
|--------|------|-------------|-----------|
| Zone 1 | 7-21s | DISAPPEAR (pair 5) | なし（地形パラックス） |
| Zone 2 | 39-54s | OBJECT_MOVE (pair 16, pos_delta=224px) | なし |
| **Zone 3** | **180-198s** | **OBJECT_MOVE (pair 63, 64)** | **UAP 出現・フレームアウト** |
| Zone 4 | 204-234s | OBJECT_MOVE (pair 71, 74, 76) | UAP 継続移動 |
| Zone 5 | 243-258s | OBJECT_MOVE (pair 84) | 影・HUD 変化 |
| Zone 6 | 264-285s | OBJECT_MOVE + DISAPPEAR (91, 93) | ホワイトアウト・探索 |

### 4.2 Targeted モードの処理差分

```python
if mode == "targeted":
    PERCENTILE_CANDIDATE = 85   # より感度高（短間隔で変化量小→閾値下げる）
    MIN_RESIDUAL         = 5.0  # フロア下げ（パラックス少ない）
    TEMPORAL_WINDOW      = 5    # 1秒間隔 × 5 = 5秒追跡
    TEMPORAL_MIN         = 2    # 5ペア中 2回で持続候補
    GRID_SIZE            = 16   # より細かいグリッド（UAP が小さい）
else:  # adaptive
    PERCENTILE_CANDIDATE = 90
    MIN_RESIDUAL         = 8.0
    TEMPORAL_WINDOW      = 3    # 3秒間隔 × 3 = 9秒追跡
    TEMPORAL_MIN         = 2
    GRID_SIZE            = 32
```

### 4.3 Targeted フレームのファイル名規則

targeted フレームは `frame_NNNNN.png`（5桁）形式。
`ts_from_name` は `int("00183") = 183` を返し、秒単位タイムスタンプとして扱う（v1 と互換）。

### 4.4 ゾーン間の非連続性への対応

targeted frames は飛び飛びのゾーンをカバーする。ゾーン境界（例: 21s→39s）でタイムスタンプが不連続になる。

**対応策**: ペア間のタイムスタンプ差が `ZONE_GAP_THRESH`（例: 10s）を超える場合、時間的一貫性のカウンターをリセット。ゾーンをまたいだトラッキングは行わない。

```python
ZONE_GAP_THRESH = 10.0  # 秒

if (timestamp_curr - timestamp_prev) > ZONE_GAP_THRESH:
    cell_history.clear()  # ゾーン境界でリセット
    track_active = {}
```

---

## 5. 出力スキーマ

### 5.1 motion_events_v2.csv（per-pair）

```
pair_id, frame_prev, frame_curr, timestamp_prev_s, timestamp_curr_s,
bg_motion_x, bg_motion_y, bg_motion_magnitude,
adaptive_threshold,                    ← v2 新規
candidate_cells, total_valid_cells,
candidate_bbox_x, candidate_bbox_y,
mean_residual_mad,
candidate_direction,
frame_delta_event,
event_type,
track_id,                              ← v2 新規（-1 = 未割当）
track_consecutive_count,               ← v2 新規
track_drift_px_per_s,                  ← v2 新規
detection_confidence                   ← v2 新規（0.0-1.0）
```

### 5.2 track_events.csv（per-track）

```
track_id, start_pair_id, end_pair_id,
start_ts_s, end_ts_s, duration_s,
n_pairs_detected,
start_bbox_x, start_bbox_y, end_bbox_x, end_bbox_y,
drift_x_per_s, drift_y_per_s, drift_mag_per_s,
r_squared,
track_event_type,                      ← LINEAR_MOTION / STATIONARY_ANOMALY / ERRATIC / SINGLE
track_direction,                       ← 空間方向ラベル
mean_detection_confidence
```

### 5.3 detection_confidence スコア（0.0-1.0）

```python
# 信頼スコア計算
score = 0.0
score += 0.30 * min(1.0, track_consecutive_count / 4)   # 連続出現数（最大 4 で満点）
score += 0.30 * min(1.0, r_squared)                      # 線形性（1.0 が最良）
score += 0.20 * (1.0 if track_drift_px_per_s >= 2.0 else drift/2.0)  # 移動速度
score += 0.20 * (1.0 - bbox_ratio)                       # コンパクト性（bbox 小 = 高スコア）
```

---

## 6. イベント分類 v2 一覧

| event_type | 説明 | 判定条件 |
|-----------|------|---------|
| STATIC | 変化なし | bg_mag<2 AND 候補なし |
| BACKGROUND_FLOW | 背景流動 | bg_mag≥2 AND 候補なし |
| CAMERA_TRACK | カメラ追跡 | bg_mag≥20 AND uniformity≥0.6 |
| LIGHTING_SHADOW_CHANGE | 照明・影変化 | bbox_ratio≥0.08 AND 非線形トラック |
| POSSIBLE_TARGET_APPEAR | 候補出現 | 前ペアにトラックなし→現ペアにトラックあり |
| POSSIBLE_TARGET_DISAPPEAR | 候補消失 | 前ペアにトラックあり→現ペアになし |
| RELATIVE_OBJECT_MOTION | 候補相対運動 | LINEAR_MOTION トラック継続 |
| REVIEW_REQUIRED | 要確認 | STATIONARY_ANOMALY または R²<0.3 |

---

## 7. PR061 検証計画

### 7.1 Adaptive Frames（3秒間隔）での期待

v2 で adaptive frames を処理した場合の区間別期待分類:

| 時刻 | 秒数 | 期待分類 | 根拠 |
|------|------|---------|------|
| 00:00〜03:02 | 0〜182s | LSC | 地形パラックス、bbox_ratio 高い |
| 03:03 | 183s | **PTA** | 適応的閾値で UAP セルが上位 10% に入る可能性 |
| 03:03〜03:09 | 183〜189s | **ROM** | UAP が下方向に移動、線形トラック |
| 03:09 | 189s | **PTD** | UAP フレームアウト |
| 03:09〜03:13 | 189〜193s | LSC / BF | カメラが UAP を見失い、探索 |
| 03:13 | 193s | **PTA** | 再出現（ただしマスク境界ノイズ混入リスク） |
| 04:00 | 240s | LSC | 影とみられるもの、bbox 広い可能性 |
| 04:17 | 257s | LSC / RR | ホワイトアウト + Zoom 切替 |

### 7.2 Targeted Frames（1秒間隔）での期待

Zone 3（180s〜198s）での期待:

| フレームペア | 秒数 | 期待分類 | 期待 track_id |
|-------------|------|---------|--------------|
| 180→181s | 180-181 | LSC | なし |
| 181→182s | 181-182 | LSC | なし |
| 182→183s | 182-183 | **PTA** | track_001 出現 |
| 183→184s | 183-184 | **ROM** | track_001 継続（下方向 drift） |
| 184→185s | 184-185 | ROM | track_001 継続 |
| 185→186s | 185-186 | ROM | track_001 継続 |
| 186→187s | 186-187 | ROM | track_001 継続 |
| 187→188s | 187-188 | ROM | track_001 継続 |
| 188→189s | 188-189 | **PTD** | track_001 消失 |
| 189→190s | 189-190 | BF / CT | カメラ追跡 |
| 190→191s | 190-191 | BF / CT | |
| 191→192s | 191-192 | BF（停止） | |
| 192→193s | 192-193 | **PTA** | track_002 出現（再出現） |
| 193→194s | 193-194 | ROM | track_002 継続 |
| ...以降 | 194-198s | ROM | track_002 継続 |

### 7.3 成功基準

| 判定 | 条件 |
|------|------|
| **成功** | track_events.csv に LINEAR_MOTION トラックあり AND 182-189s に開始 AND 下方向ドリフト |
| **部分成功** | REVIEW_REQUIRED 件数減少 AND LSC が 0-183s で支配的（v1 比較） |
| **失敗** | 全ペアが LSC のまま（v1 と同結果） |

---

## 8. パラメータ設計

### 8.1 Adaptive Mode デフォルト

| パラメータ | デフォルト値 | 説明 |
|----------|-----------|------|
| `--grid-size` | 32 | グリッドセルサイズ (px) |
| `--percentile` | 90 | 候補化パーセンタイル |
| `--min-residual` | 8.0 | 最低残差フロア |
| `--temporal-window` | 3 | 時間ウィンドウ幅（ペア数） |
| `--temporal-min` | 2 | 持続候補化に必要な最小出現数 |
| `--drift-min-px-s` | 1.0 | LINEAR_MOTION 判定の最小ドリフト速度 |
| `--r2-linear-thresh` | 0.60 | 線形運動判定の R² 閾値 |
| `--zone-gap-thresh` | 10.0 | ゾーン境界と見なすタイムスタンプ差（秒） |

### 8.2 Targeted Mode デフォルト（override）

| パラメータ | Targeted での値 | 変更理由 |
|----------|---------------|---------|
| `--grid-size` | 16 | 小さな UAP を細かく追跡 |
| `--percentile` | 85 | 1秒間隔で変化量小→感度上げ |
| `--min-residual` | 5.0 | パラックスが小さい→フロア下げ |
| `--temporal-window` | 5 | 5秒窓 |
| `--temporal-min` | 2 | 同左 |

### 8.3 チューニング方針

PR061 で失敗した場合の調整順:

1. `--percentile` を 90 → 85 → 80 に下げる（候補率を増やす）
2. `--temporal-min` を 2 → 1 に下げる（1回出現でも持続候補化）
3. `--r2-linear-thresh` を 0.60 → 0.40 に下げる（不規則な線形も許容）
4. `--grid-size` を 32 → 16 に下げる（UAP が小さい場合）

---

## 9. 実装スコープ

### 9.1 v2 で実装する機能

- [ ] 適応的閾値計算（percentile ベース）
- [ ] Phase 2 時間的一貫性分析（スライディングウィンドウ）
- [ ] Phase 3 空間追跡・線形回帰
- [ ] track_id 付与ロジック
- [ ] ゾーン境界リセット（targeted frames 用）
- [ ] track_events.csv 出力
- [ ] detection_confidence スコア計算
- [ ] `--mode targeted` CLI オプション
- [ ] PR061 targeted frames での dry-run 検証

### 9.2 v2 で実装しない機能（v3 以降）

- OpenCV Optical Flow（v2 も Pillow + numpy のみ）
- Kalman Filter による滑らかな追跡
- 複数候補のコンフリクト解決（重複 track_id）
- generate_ai_observation_report.py への track_events 統合表示
- 機械学習による分類精度向上

---

## 10. 技術的リスクと対策

| リスク | 影響 | 対策 |
|--------|------|------|
| 適応的閾値でも UAP 非検出 | v2 も全 LSC | targeted frames モードに期待を移す。1秒間隔ならパラックス減少 |
| Targeted Zone 間の連続性問題 | トラック誤接続 | ZONE_GAP_THRESH でゾーン間リセット |
| 線形回帰に N≥3 必要（N<3 は不安定） | SINGLE_APPEARANCE 大量 | n_pairs=2 の場合は方向のみ推定（R² なし）、REVIEW_REQUIRED に分類 |
| 処理時間（targeted 105 フレーム、16px グリッド） | 2倍以上遅い | 16px グリッドで セル数 4 倍 → 処理 4 倍増。受容範囲（〜20分以内） |
| マスキング境界での偽 PTA | 誤検出増 | 上下 12% フィルタを 15% に拡大（マスク除外範囲拡大） |
| ゾーン境界でのトラック消失 | PTD 誤検出 | ゾーン境界の PTD/PTA はフラグ付き（`near_zone_boundary=True`） |

---

## 11. 出力ディレクトリ規則

```
data/motion_intelligence_runs/<date>/
└── <source_id>/
    ├── v1/
    │   ├── motion_events.csv
    │   ├── motion_events.jsonl
    │   └── summary.md
    └── v2/                              ← v2 出力
        ├── motion_events_v2.csv
        ├── motion_events_v2.jsonl
        ├── track_events.csv
        └── summary.md
```

`--output-dir` 省略時は `data/motion_intelligence_runs/<today>/<source_id>/v2/` に出力。

---

## 12. 次のステップ

1. **設計承認**: このドキュメントのレビューと承認
2. **v2 実装**: `scripts/motion_intelligence_v2.py` の実装
3. **PR061 adaptive dry-run**: 適応的閾値効果の確認
4. **PR061 targeted dry-run**: Zone 3（180-198s）での PTA/ROM 検出確認
5. **成功基準評価**: `track_events.csv` に LINEAR_MOTION トラックが 182-189s に存在するか
6. **generate_ai_observation_report.py 統合計画**: track_events.csv を使ったセグメント分類改善（v3）
