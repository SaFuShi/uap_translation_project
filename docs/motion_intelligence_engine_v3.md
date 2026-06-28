# Motion Intelligence Engine v3 設計書

- 作成日: 2026-06-27（再作成: 2026-06-28）
- 前バージョン: `docs/motion_intelligence_engine_v2.md`
- 対象スクリプト: `scripts/motion_intelligence_v3.py`（未実装）
- ステータス: 設計承認待ち

---

## 1. 背景・目的

### 1.1 v2 の成果と限界

**v2 成果（PR061 targeted frames 検証）:**
- 適応的閾値（p85）により LSC: 95件（v1）→ 0件（v2）へ大幅改善
- Zone Gap Detection バグ修正（frame_ts 事前計算方式）
- 全 104 ペアで処理成功（6.7秒）

**v2 の限界（PR061 Zone 3 UAP 未検出）:**
1. **select_primary の失敗**: 最高残差クラスタを毎ペア選択 → ノイズ cluster が先に選ばれ誤 track 開始
2. **track 安定性なし**: track が毎ペア別位置へ飛ぶ → 63 tracks / 104 pairs（目標: ≤25）
3. **seed 品質フィルタなし**: pair 30 で noise cluster（5cells, mr≈25）が PTA としてシード → 誤 track が Z3 全体を汚染
4. **trail 未検出**: pair 35 の 102cells が SINGLE_APPEARANCE（track なしのため）

### 1.2 v2 の失敗分析（Zone 3 詳細）

```
pair 30 (181→182s): noise cluster（5cells, mr≈25）が最高残差 → PTA（誤）
pair 31 (182→183s): noise track が継続 → ROM（誤）
pair 32 (183→184s): UAP 出現だが noise track と競合 → 誤選択
pair 34 (185→187s, 2s gap): 1cell ノイズが選択 → track 断絶
pair 35 (187→188s): 102cells SINGLE_APPEARANCE（UAP trail だが track なし）
pair 36 (188→189s): track 消失 → RR（PTD を見逃し）
```

### 1.3 v3 の目標

1. **seed フィルタ**: track 開始時の最小残差閾値（SEED_RES_THRESH=35.0）でノイズ排除
2. **sticky tracking**: アクティブ track がある場合、最近傍コンパクトクラスタを継続選択
3. **trail 検出**: 大型クラスタ（≥20cells, bbox_ratio≤0.20）をトレイル信号として記録
4. **PR061 Zone 3 LINEAR_MOTION 検出**: drift_y≈17px/s、R²≈0.99 の track を確立

---

## 2. v2 との差分

| 項目 | v2 | v3 |
|------|----|----|
| select_primary | 最高 mean_residual のコンパクトクラスタ | sticky: 最近傍 / seed: 高残差（mr≥35） |
| track 開始条件 | なし（最高残差で即開始） | SEED_RES_THRESH=35.0 + MIN_CELLS_SEED=2 |
| track 継続条件 | MAX_TRACK_DIST_CELLS=4.0 | MAX_STICKY_DIST=5（sticky 追跡） |
| trail 検出 | なし | TRAIL_MIN_CELLS=20 + TRAIL_BRATIO_MAX=0.20 |
| 期待 track 数 | 63（PR061） | ≤25（PR061 目標） |

---

## 3. アルゴリズム設計

### 3.1 処理フロー概要

```
[入力] frames_dir (targeted モード)
          ↓
[Phase 1] フレームペア解析（v2 継続）
  ├─ FFT Phase Correlation → (bg_dx, bg_dy, bg_mag)
  ├─ 適応的閾値（p85 in targeted）
  ├─ 候補セル抽出
  └─ Union-Find クラスタリング
          ↓
[Phase 2] クラスタ分類（v3 新規）
  ├─ TRAIL_CLUSTER: n_cells≥20 AND bbox_ratio≤0.20
  ├─ COMPACT: n_cells<20 OR bbox_ratio>0.20
  └─ NOISE_REJECTED: mean_residual<SEED_RES_THRESH（アクティブ track なし時のみ）
          ↓
[Phase 3] select_primary（v3 核心）
  ├─ アクティブ track あり → sticky: 最近傍 COMPACT クラスタ（距離≤MAX_STICKY_DIST）
  └─ アクティブ track なし → seed: mean_res≥SEED_RES_THRESH の COMPACT クラスタ（高残差優先）
          ↓
[Phase 4] 時間的一貫性（v2 継続）
  ├─ deque(W=5) + T_MIN=2
  └─ 持続候補 → track_id 付与
          ↓
[Phase 5] 線形回帰・イベント分類（v2 継続）
  └─ LINEAR_MOTION / STATIONARY_ANOMALY / ERRATIC / SINGLE
          ↓
[出力] motion_events_v3.csv + track_events.csv + summary.md
```

### 3.2 クラスタ分類（v3 新規）

#### 3.2.1 TRAIL_CLUSTER 判定

```python
TRAIL_MIN_CELLS  = 20   # UAP トレイル（尾引き）の最小セル数
TRAIL_BRATIO_MAX = 0.20  # トレイルは細長い → bbox_ratio 小

def classify_cluster(cluster):
    n = len(cluster["cells"])
    bratio = cluster["bbox_ratio"]
    mr = cluster["mean_residual"]
    
    if n >= TRAIL_MIN_CELLS and bratio <= TRAIL_BRATIO_MAX:
        return "TRAIL_CLUSTER"   # 追跡対象ではなく証拠として記録
    elif n < MIN_CELLS_CONT:
        return "TINY"            # 単独セル等（継続時のみ許容）
    else:
        return "COMPACT"         # 追跡対象候補
```

TRAIL_CLUSTER は track の primary 候補にはしない。ただし `trail_detected=True` フラグを当該ペアに立て、UAP 存在の証拠として出力に記録する。

#### 3.2.2 NOISE_REJECTED 判定

```python
SEED_RES_THRESH = 35.0  # track 開始に必要な最小 mean_residual

def is_valid_seed(cluster, has_active_track):
    if has_active_track:
        return True   # sticky 継続時は残差フィルタなし
    return cluster["mean_residual"] >= SEED_RES_THRESH  # seed 時のみフィルタ
```

**根拠**: pair 30 の noise cluster は mr≈25 < 35.0 → NOISE_REJECTED → track 開始せず → pair 31 以降が BF に分類 → pair 32 で UAP が mr≥35 で正しく seed される。

### 3.3 select_primary（v3 核心変更）

#### 3.3.1 v2 との比較

```python
# v2: 最高残差優先（毎ペア飛ぶ）
def select_primary_v2(clusters):
    compact = [c for c in clusters if c["bbox_ratio"] < COMPACT_BRATIO]
    return max(compact, key=lambda c: c["mean_residual"])

# v3: sticky / seed 二段階
def select_primary_v3(clusters, active_track_centroid):
    compact = [c for c in clusters if classify_cluster(c) == "COMPACT"]
    
    if active_track_centroid is not None:
        # sticky: アクティブ track に最も近い COMPACT クラスタ
        nearest = min(compact, key=lambda c: dist(c["centroid"], active_track_centroid))
        if dist(nearest["centroid"], active_track_centroid) <= MAX_STICKY_DIST:
            return nearest, "sticky"
        else:
            return None, "lost"   # 距離超過 → track 中断
    else:
        # seed: 高残差 COMPACT クラスタのみ（SEED_RES_THRESH でフィルタ済み）
        seeds = [c for c in compact if c["mean_residual"] >= SEED_RES_THRESH
                 and len(c["cells"]) >= MIN_CELLS_SEED]
        if seeds:
            return max(seeds, key=lambda c: c["mean_residual"]), "seed"
        return None, "no_seed"
```

#### 3.3.2 アクティブ track の定義

```python
# 直前ペアで primary が選択されていた場合、アクティブ track が存在する
# TRACK_MISS_TOLERANCE=2 を維持（2ペア連続 miss で track 終了）
TRACK_MISS_TOLERANCE = 2

track_miss_count = 0
if selected is None:
    track_miss_count += 1
    if track_miss_count > TRACK_MISS_TOLERANCE:
        active_track_centroid = None  # track リセット
        track_miss_count = 0
else:
    active_track_centroid = selected["centroid"]
    track_miss_count = 0
```

### 3.4 パラメータ一覧（targeted モード）

**絶対に変更しないパラメータ:**

| パラメータ | 値 | 変更禁止理由 |
|----------|----|-----------| 
| `T_MIN` | 2 | 17px/s UAP は 16px グリッドに最大 2 ペア分の残差。T_MIN=3 にすると UAP セルが持続候補にならず検出不能 |
| `W` | 5 | 5秒追跡窓（1秒間隔 × 5） |
| `grid_size` | 16 | UAP が小さいため細かいグリッドが必須 |

**v3 主要パラメータ:**

| パラメータ | 値 | 説明 |
|----------|----|----|
| `SEED_RES_THRESH` | 35.0 | track 開始時の最小 mean_residual |
| `MIN_CELLS_SEED` | 2 | track 開始時の最小セル数 |
| `MIN_CELLS_CONT` | 1 | track 継続時の最小セル数 |
| `MAX_STICKY_DIST` | 5 | sticky 追跡の最大距離（cell 単位、80px） |
| `TRAIL_MIN_CELLS` | 20 | TRAIL_CLUSTER 判定の最小セル数 |
| `TRAIL_BRATIO_MAX` | 0.20 | TRAIL_CLUSTER の最大 bbox_ratio |
| `TRACK_MISS_TOLERANCE` | 2 | track 中断を許容する連続 miss 数 |

---

## 4. PR061 Zone 3 期待動作

### 4.1 ペアごとの期待

| pair | 秒 | v2 結果 | v3 期待 | 理由 |
|------|------|---------|---------|------|
| 30 | 181→182 | 誤 PTA（noise mr≈25）| BF / RR | NOISE_REJECTED（mr<35）→ track 開始せず |
| 31 | 182→183 | ROM（noise track 継続）| RR | アクティブ track なし、UAP seed なし |
| 32 | 183→184 | ROM | **PTA** | UAP mr≥35 → seed 開始 |
| 33 | 184→185 | ROM | **ROM** | sticky 継続（nearest compact） |
| 34 | 185→187 | ROM/RR（2s gap）| ROM | gap=2s < ZONE_GAP_THRESH=3s → sticky 継続 |
| 35 | 187→188 | RR（102cells SINGLE）| ROM + `trail_detected=True` | sticky で UAP track + trail 記録 |
| 36 | 188→189 | RR | **PTD** | sticky 距離超過 / 候補消失 → track 終了 |

### 4.2 期待 track_event（track_events.csv）

```
track_id:          1
start_pair:        pair 32（183→184s）
end_pair:          pair 36（188→189s）
n_pairs_detected:  5
drift_y_per_s:     ≈ 17.0 px/s（下方向）
drift_x_per_s:     ≈ 0〜5 px/s
r_squared:         ≥ 0.90
track_event_type:  LINEAR_MOTION  ← v3 の成功基準
```

### 4.3 成功基準

| 判定 | 条件 |
|------|------|
| **成功** | track_events.csv に LINEAR_MOTION トラックあり AND 183-189s に開始 AND 下方向ドリフト |
| **部分成功** | REVIEW_REQUIRED 件数減少 AND 総 tracks ≤ 25 AND pair 30 が PTA でない |
| **失敗** | pair 32 が PTA にならない / LINEAR_MOTION が生成されない |

---

## 5. 出力スキーマ（v2 からの追加分）

### 5.1 motion_events_v3.csv（追加フィールド）

```
...（v2 フィールド継続）...
select_mode,          ← "sticky" / "seed" / "lost" / "no_seed"
trail_detected,       ← True / False（TRAIL_CLUSTER が存在するペア）
trail_cells,          ← trail クラスタのセル数（trail_detected=True 時）
seed_residual,        ← seed 選択時の mean_residual（sticky 時は NaN）
```

### 5.2 track_events.csv（変更なし、v2 と同一スキーマ）

---

## 6. 実装スコープ

### 6.1 v3 で実装する機能（v2 からの差分）

- [ ] `classify_cluster()` 関数（TRAIL_CLUSTER / COMPACT / TINY 分類）
- [ ] `select_primary_v3()` 関数（sticky / seed 二段階選択）
- [ ] `SEED_RES_THRESH` フィルタ（track 開始時のみ適用）
- [ ] `MAX_STICKY_DIST` による sticky 距離制限
- [ ] `trail_detected` フラグの per-pair 出力
- [ ] `select_mode` フィールドの出力
- [ ] 上記パラメータの `TARGETED_OVERRIDES` への追加

### 6.2 v3 で変更しない機能（v2 から継続）

- FFT Phase Correlation（背景推定）
- 適応的閾値（p85 in targeted）
- Union-Find クラスタリング
- Zone Gap Detection（frame_ts 事前計算方式）
- 時間的一貫性（deque W=5, T_MIN=2）
- 線形回帰・track_event_type 分類
- detection_confidence スコア計算
- 出力ディレクトリ規則

---

## 7. 実装計画

### 7.1 ファイル構成

```
scripts/
├── motion_intelligence_v2.py  （既存・変更なし）
└── motion_intelligence_v3.py  （v2 から fork → 差分実装）
```

### 7.2 実装手順

1. `motion_intelligence_v2.py` を `motion_intelligence_v3.py` としてコピー
2. `TARGETED_OVERRIDES` に v3 パラメータ追加
3. `classify_cluster()` 関数追加
4. `select_primary()` を `select_primary_v3()` に置換
5. アクティブ track 管理ロジック（miss count）追加
6. `trail_detected` / `select_mode` の出力追加
7. PR061 targeted dry-run 実行・検証

### 7.3 検証コマンド

```bash
python3 scripts/motion_intelligence_v3.py \
  --frames-dir "data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted" \
  --article-id "R02-053" \
  --source-id "DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0" \
  --output-dir "data/motion_intelligence_runs/20260628/DOW-UAP-PR061_v3" \
  --mode targeted --verbose --execute
```

---

## 8. 技術的リスクと対策

| リスク | 影響 | 対策 |
|--------|------|------|
| SEED_RES_THRESH=35.0 が UAP mr に届かない | pair 32 が seed 失敗 | verbose ログで pair 32 の compact clusters の mr を確認 → 閾値を 30.0 に下げる |
| MAX_STICKY_DIST=5 が小さすぎ | track 途切れ | pair間の実際の centroid 移動距離をログ確認 → 7 or 10 に拡大 |
| T_MIN=2 でも pair 32 が持続候補にならない | PTA 失敗 | T_MIN=2 は変更禁止。W=5 なので 5ペア中 2回で十分なはず |
| pair 35 の 102cells が TRAIL と判定されない | trail_detected=False | TRAIL_MIN_CELLS を 20→15 に下げる（デバッグ後） |

---

## 9. 次のステップ

1. **設計承認**: このドキュメントのレビューと承認
2. **v3 実装**: `scripts/motion_intelligence_v3.py`（v2 fork + 差分）
3. **PR061 targeted dry-run**: Zone 3 で LINEAR_MOTION 確認
4. **成功基準評価**: track_events.csv に LINEAR_MOTION（183-189s, 下方向）が存在するか
5. **v3 成功後**: generate_ai_observation_report.py への track_events 統合（v4 以降）
