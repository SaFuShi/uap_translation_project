# Motion Intelligence v3 設計レビューレポート

- 作成日: 2026-06-27（再作成: 2026-06-28）
- 設計書: `docs/motion_intelligence_engine_v3.md`
- レビュー対象: v2 → v3 の差分設計
- ステータス: 承認待ち

---

## 1. レビューサマリー

### 1.1 v2 の問題点（確認済み）

PR061 targeted frames（104 ペア）の v2 実行結果:

```
総ペア: 104, 総ゾーン: 5
STATIC: 1, PTA: 1, ROM: 35, RR: 67, LSC: 0
総 tracks: 63（LINEAR_MOTION: 0）← 失敗
Zone 3（180-198s）: 誤 PTA@pair30, track 断絶@pair34, 102cells SINGLE_APPEARANCE@pair35
```

**根本原因**: `select_primary_v2()` が最高残差優先のため、毎ペア最高残差クラスタが変わるたびに新 track が生成される。pair 30 の noise cluster（mr≈25）が先にシードされ、Zone 3 全体を汚染。

### 1.2 v3 の設計変更（承認を求める点）

| 変更 | 内容 | 効果 |
|------|------|------|
| SEED_RES_THRESH=35.0 | track 開始時の最小 mean_residual フィルタ | noise（mr≈25）を排除、UAP（mr≥35）のみシード |
| sticky tracking | アクティブ track → 最近傍クラスタを継続選択 | track が毎ペア飛ぶ問題を解消 |
| TRAIL_CLUSTER 検出 | n_cells≥20 AND bbox_ratio≤0.20 を trail として記録 | pair 35 の 102cells を証拠として取得 |
| T_MIN=2 維持（変更禁止）| 変更しない | UAP 検出に必須（下記参照） |

---

## 2. 設計の妥当性検証

### 2.1 T_MIN=2 変更禁止の根拠

PR061 UAP の物理的制約:

```
UAP 移動速度（推定）: 17 px/s（Zone 3, 下方向）
グリッドセルサイズ (targeted): 16 px

1秒間の移動: 17px ≈ 1.06 グリッドセル

→ UAP が特定セルに留まるのは最大 2 ペア分
→ T_MIN=3 にすると UAP セルの出現回数が 2 で止まり、持続候補にならない
→ T_MIN=2 は検出に必要な最小値（これ以下には下げない）
```

### 2.2 SEED_RES_THRESH=35.0 の根拠

v2 実行データから:

```
pair 30 noise cluster: mr ≈ 25.0（誤シード → 排除対象）
pair 32 UAP cluster（期待）: mr ≥ 35.0（正規シード）
地形パラックス通常値: mr ≈ 20〜30

閾値 35.0 は地形ノイズとUAPの間のギャップに位置する。
ただし、UAP の実際の mr が 30〜35 の場合は閾値を 30.0 に下げる必要あり。
→ v3 dry-run で pair 32 の mr を verbose ログで確認してから調整。
```

### 2.3 MAX_STICKY_DIST=5 の根拠

```
UAP 移動速度: 17 px/s
グリッドセル: 16 px

1秒間のセル移動: 17/16 ≈ 1.06 cells/s

sticky 距離 5 cells = 80 px で追跡可能範囲:
80 / 17 ≈ 4.7 秒分の移動をカバー

→ 1秒間隔フレームで 5 cells は十分な余裕（実際の移動は 1 cell/s 程度）
→ ただし pair 34 の 2s gap 時は 2 cells 移動 → 5 cells 以内でカバー可能
```

### 2.4 TRAIL_CLUSTER=20cells の根拠

```
v2 実行結果 pair 35: 102 cells の SINGLE_APPEARANCE
→ これは UAP trail（光学尾引き・残像）と考えられる

20 cells = 320×320px 相当（16px × 20）
→ 小さすぎるクラスタを trail と誤判定しないための最小値

bbox_ratio ≤ 0.20:
→ trail は細長い形状（幅/高さの比が小さい）
→ 丸い大型クラスタ（地形パラックス）を排除
```

---

## 3. 実装リスク評価

### 3.1 高リスク

**R1: pair 32 の UAP mean_residual が 35 未満の場合**
- 影響: seed 失敗 → LINEAR_MOTION 未検出
- 確認方法: `--verbose` ログで pair 32 の compact clusters の mr を確認
- 対策: mr が 30〜35 の場合は SEED_RES_THRESH を 30.0 に下げる

### 3.2 中リスク

**R2: sticky で track が pair 34（2s gap）を越えられない**
- 影響: pair 34 で track 断絶 → R² 不足 → LINEAR_MOTION 失敗
- 確認方法: verbose ログで pair 34 の centroid 距離を確認
- 対策: MAX_STICKY_DIST を 5→7 に拡大

**R3: TRAIL_CLUSTER 誤分類**
- 影響: 大型地形クラスタを trail と誤検出
- 確認方法: verbose ログで trail 検出ペアの bbox_ratio を確認
- 対策: TRAIL_BRATIO_MAX を 0.20→0.15 に厳格化

### 3.3 低リスク

**R4: 総 tracks 数が目標（≤25）を超える**
- v3 の seed フィルタで対応できるはず
- 対策不要（SEED_RES_THRESH 調整で自然に解決）

---

## 4. 設計承認チェックリスト

- [ ] sticky tracking ロジック（select_primary_v3）の設計を承認
- [ ] SEED_RES_THRESH=35.0 の初期値を承認（dry-run 後調整可）
- [ ] T_MIN=2 維持の合意確認
- [ ] TRAIL_CLUSTER 検出フィーチャーを v3 に含めることを承認
- [ ] 出力フィールド追加（select_mode, trail_detected）を承認
- [ ] 実装開始（`scripts/motion_intelligence_v2.py` → `v3.py` fork）を承認

---

## 5. 承認後の実装ステップ

```
Step 1: cp scripts/motion_intelligence_v2.py scripts/motion_intelligence_v3.py
Step 2: TARGETED_OVERRIDES に v3 パラメータ追加
Step 3: classify_cluster() 関数追加
Step 4: select_primary() → select_primary_v3() 置換
Step 5: アクティブ track 管理（miss_count）追加
Step 6: trail_detected / select_mode 出力追加
Step 7: dry-run 実行 → verbose ログ確認
Step 8: 必要に応じてパラメータ調整（R1〜R3 対応）
Step 9: 本番実行 → track_events.csv に LINEAR_MOTION 確認
```

---

## 6. 参考: v2 実行コマンドと結果

```bash
# v2 実行コマンド（参考）
python3 scripts/motion_intelligence_v2.py \
  --frames-dir "data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted" \
  --article-id "R02-053" \
  --source-id "DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0" \
  --output-dir "data/motion_intelligence_runs/20260627/DOW-UAP-PR061_v2" \
  --mode targeted --verbose --execute

# v2 結果
总ペア: 104, 総 zones: 5
STATIC: 1, PTA: 1, ROM: 35, RR: 67, LSC: 0
総 tracks: 63, LINEAR_MOTION: 0 ← 失敗
```

```bash
# v3 実行コマンド（予定）
python3 scripts/motion_intelligence_v3.py \
  --frames-dir "data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted" \
  --article-id "R02-053" \
  --source-id "DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0" \
  --output-dir "data/motion_intelligence_runs/20260628/DOW-UAP-PR061_v3" \
  --mode targeted --verbose --execute
```
