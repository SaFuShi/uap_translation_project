# Motion Intelligence Engine v1 設計レビュー

- 作成日: 2026-06-27
- 対象スクリプト: `scripts/motion_intelligence_v1.py`（未実装）
- 設計書: `docs/motion_intelligence_engine_v1.md`
- ステータス: 設計承認待ち

---

## 1. 設計判断サマリー

### 1.1 実装方式の決定

**採用: A案（Pillow + numpy）**

| 選択肢 | 状況 | 判断 |
|--------|------|------|
| OpenCV あり（B案） | `import cv2` → ModuleNotFoundError | **利用不可** |
| scipy | `import scipy` → ModuleNotFoundError | 利用不可 |
| **numpy 2.4.4** | インストール済み | **✅ 利用可** |
| **Pillow** | インストール済み | **✅ 利用可** |

OpenCV は未インストール。v1 は **Pillow + numpy の簡易ブロックマッチング方式**で実装する。

numpy が利用可能なため、B案（OpenCV版）の Optical Flow に近い品質を、
ブロックマッチング（BMA）で代替できる:

```
B案（OpenCV）        A案（Pillow+numpy）
Optical Flow     →  ブロックマッチング
全画素ベクトル    →  グリッド単位ベクトル（32px×32px）
連続的           →  離散的（グリッド解像度依存）
処理: 0.1秒/ペア →  処理: 1〜3秒/ペア（許容範囲）
```

将来 OpenCV が利用可能になった場合は v2 で採用し、motion_events.csv の互換性を維持する。

---

## 2. PR061 での課題分析

### 2.1 Frame Delta v2 の誤検出パターン

PR061 人間確認結果から、Frame Delta v2 の誤検出構造を整理する。

**誤検出の原因（93件中の内訳推定）:**

| 誤検出原因 | 推定件数 | 区間 | v1 での期待分類 |
|-----------|---------|------|----------------|
| カメラ/機体移動による背景流動 | 〜60件 | 0〜286s 全体 | BACKGROUND_FLOW / CAMERA_TRACK |
| 山岳地形テクスチャの輝度変化 | 〜20件 | 0〜183s | LIGHTING_SHADOW_CHANGE |
| 対象物の実際の移動 | 〜10件 | 183〜240s | RELATIVE_OBJECT_MOTION / PTA / PTD |
| 影・モード変更・Zoom切替 | 〜3件 | 240〜286s | LIGHTING_SHADOW_CHANGE / ZOOM_OR_CROP |

**根本原因:** Frame Delta v2 は「フレーム全体の変化量」を見るため、
カメラが動けば地形全体が移動しても OBJECT_MOVE と分類する。

### 2.2 Motion Intelligence v1 が解決すべき問題

```
問題1: 背景が全体的に動く場合に OBJECT_MOVE が大量発生
解決策: グリッド全体の中央値を背景主運動として推定し、局所偏差のみを候補化

問題2: 山岳地形の明暗境界が輝点変化として検出される
解決策: 運動ベクトルが小さいが MAD が高い → LIGHTING_SHADOW_CHANGE に分類

問題3: 対象物が小さく、背景地形に埋もれる
解決策: 相対運動閾値（rel_motion_thresh）を低く設定し、感度を上げる
        その代わり、最小候補セル数（min_candidate_cells）でノイズを除去
```

---

## 3. アルゴリズム選択の根拠

### 3.1 ブロックマッチング vs 差分統計

| 手法 | 背景運動の除去 | 計算コスト | numpy のみで実装可否 |
|------|------------|---------|-------------------|
| 単純差分（v2方式） | ✗ | 低 | ✓ |
| グリッド差分集計 | △（方向不明） | 低 | ✓ |
| **ブロックマッチング（v1方式）** | **✓（ベクトル推定）** | 中 | **✓** |
| Optical Flow（OpenCV） | ✓（高精度） | 低〜中 | ✗（要 OpenCV） |

ブロックマッチングは「各グリッドセルがどの方向に何 px 動いたか」を推定できるため、
中央値による背景主運動の推定・除去が可能。

### 3.2 グリッドサイズの選定

| グリッドサイズ | 解像度 | セル数（1280×720） | 処理時間/ペア | 対象物最小検出サイズ |
|--------------|--------|----------------|------------|------------------|
| 16px | 高 | 3,600 | 5〜15秒 | 16×16px = 0.3% |
| **32px** | 中 | 900 | **1〜3秒** | **32×32px = 0.6%** |
| 64px | 低 | 252 | <1秒 | 64×64px = 2.2% |

デフォルト 32px を採用。対象物が小さい場合は 16px への変更オプション提供。

### 3.3 背景推定に中央値を使う理由

平均値 vs 中央値:
- 対象物候補は全セルの 5〜15% 程度
- 平均値: 外れ値（対象物セル）に引っ張られる可能性
- **中央値**: 外れ値に頑健。対象物セルが 50% 未満なら背景主運動を正確に推定できる

PR061 の場合、対象物は画面の一部のみ（最大でも 10〜20% 程度）のため中央値が有効。

---

## 4. イベント分類の判断フロー

```
入力: (bg_magnitude, candidate_cells, rel_motion, mad_distribution, zoom_pattern)

if bg_magnitude < 2.0 AND candidate_cells == 0:
    → STATIC

elif zoom_pattern_detected:
    → ZOOM_OR_CROP

elif candidate_cells > total_cells * 0.30 AND rel_motion < 5.0:
    → LIGHTING_SHADOW_CHANGE  ← 山岳日照・影はここに入る

elif prev_candidates == 0 AND curr_candidates >= MIN_CELLS:
    → POSSIBLE_TARGET_APPEAR   ← 183s（03:03）の対象物出現を検出したい

elif prev_candidates >= MIN_CELLS AND curr_candidates == 0:
    → POSSIBLE_TARGET_DISAPPEAR ← 189s（03:09）のフレームアウト

elif bg_magnitude >= 30.0 AND uniformity > 0.8:
    → CAMERA_TRACK              ← カメラ追跡モードのフォロー

elif candidate_cells >= MIN_CANDIDATE_CELLS:
    → RELATIVE_OBJECT_MOTION   ← 対象物の継続移動

elif bg_magnitude >= 2.0 AND candidate_cells == 0:
    → BACKGROUND_FLOW

else:
    → REVIEW_REQUIRED
```

---

## 5. PR061 検証の詳細予測

### 5.1 区間別期待分類

| 時刻 | 秒数 | 人間確認内容 | v1 期待分類 | 信頼度 |
|------|------|------------|-----------|--------|
| 00:00〜03:02 | 0〜182s | カメラ移動・地形流動・日照変化 | BACKGROUND_FLOW / LSC / CAMERA_TRACK | 高 |
| 03:03 | 183s | 対象物出現（右上から） | POSSIBLE_TARGET_APPEAR | 中 |
| 03:03〜03:09 | 183〜189s | 対象物が直線移動 | RELATIVE_OBJECT_MOTION | 中 |
| 03:09 | 189s | フレームアウト | POSSIBLE_TARGET_DISAPPEAR | 中 |
| 03:09〜03:13 | 189〜193s | カメラが対象物を追跡 | CAMERA_TRACK | 高 |
| 03:13 | 193s | 上部マスクから再出現 | POSSIBLE_TARGET_APPEAR | 低（マスク境界ノイズ混入可能性）|
| 03:13〜04:00 | 193〜240s | 対象物継続移動 | RELATIVE_OBJECT_MOTION | 中 |
| 04:00〜04:01 | 240〜241s | 影が地表に見える | LIGHTING_SHADOW_CHANGE | 低〜中 |
| 04:01〜04:12 | 241〜252s | カメラが消失点を探索 | BACKGROUND_FLOW / CAMERA_TRACK | 高 |
| 04:12 | 252s | HUD 色変化（センサーモード） | LIGHTING_SHADOW_CHANGE / ZOOM_OR_CROP | 低 |
| 04:17 | 257s | ホワイトアウト + Zoom 切替 | ZOOM_OR_CROP | 高 |
| 04:17〜04:46 | 257〜286s | 探索継続、対象物なし | BACKGROUND_FLOW / STATIC | 高 |

### 5.2 成功判断基準

| 判定 | 条件 |
|------|------|
| **成功** | REVIEW_REQUIRED ≤ 8件 AND 183s区間に PTA/ROM を含む |
| **部分成功** | REVIEW_REQUIRED ≤ 15件 AND BACKGROUND_FLOW が 0〜183s で支配的 |
| **失敗** | REVIEW_REQUIRED > 20件 または 0〜183s で PTA/ROM が大量発生 |

### 5.3 パラメータチューニング方針

初期値で失敗した場合の調整順:

1. `--rel-motion-thresh` を 8.0 → 12.0 に上げる（感度を下げてノイズ低減）
2. `--min-candidate-cells` を 2 → 4 に上げる（小さな候補領域を除外）
3. `--grid-size` を 32 → 16 に下げる（小さな対象物の検出感度を上げる）
4. `--search-window` を 16 → 24 に上げる（高速カメラパンに対応）

---

## 6. generate_ai_observation_report.py との統合計画

### 6.1 現在の互換性

`generate_ai_observation_report.py` は `event_type` カラムの文字列を読み込む。
未知の event_type は REVIEW_REQUIRED 相当（priority=3）として処理される。

```python
# 現在の generate_ai_observation_report.py のイベント優先度マップ
EVENT_PRIORITY = {
    "CUT": 10, "APPEAR": 10, "DISAPPEAR": 10,
    "OBJECT_MOVE": 5, "ZOOM_BLOOM": 5, "CAMERA_TRACK": 3,
    "REVIEW_REQUIRED": 3, "STATIC": 0,
}
# → POSSIBLE_TARGET_APPEAR などは priority=3 で処理される（問題なし）
```

### 6.2 将来の拡張（v2 以降）

```python
# 将来 generate_ai_observation_report.py に追加予定
MOTION_INTELLIGENCE_PRIORITY = {
    "POSSIBLE_TARGET_APPEAR": 10,
    "POSSIBLE_TARGET_DISAPPEAR": 10,
    "RELATIVE_OBJECT_MOTION": 8,
    "CAMERA_TRACK": 4,
    "ZOOM_OR_CROP": 4,
    "LIGHTING_SHADOW_CHANGE": 2,
    "BACKGROUND_FLOW": 0,
}
```

---

## 7. 実装スコープ（v1）

### 7.1 実装する機能

- [x] 設計確定（このドキュメント）
- [ ] グリッドベースのブロックマッチングエンジン
- [ ] 背景主運動推定（numpy 中央値）
- [ ] 候補セル抽出・クラスタリング
- [ ] フィルタ（照明・影・マスキング）
- [ ] イベント分類（8種）
- [ ] CSV / JSONL / summary.md 出力
- [ ] PR061 dry-run 検証

### 7.2 v1 で実装しない機能（v2 以降）

- OpenCV Optical Flow への置き換え
- フレーム間の対象物追跡（Kalman Filter 等）
- 複数対象物の分離
- generate_ai_observation_report.py へのイベント専用表示追加
- targeted frames の活用（v1 は adaptive frames のみ）

---

## 8. リスクと対策

| リスク | 影響 | 対策 |
|--------|------|------|
| ブロックマッチングが遅すぎる | PR061 95ペアで 5分超 | stride=2 最適化。それでも遅い場合は grid_size=48 へ |
| マスキング境界（黒塗り矩形端）が候補に入る | 誤検出増加 | 上下15%領域フィルタ + bc=0 隣接チェック |
| 03:13 の上部マスクからの再出現が検出できない | PTA 欠損 | マスク境界を検出対象外にしているため発生しうる。v1 では REVIEW_REQUIRED で対応 |
| 対象物が背景と同じ方向に動く場合 | ROM 欠損 | 相対速度が小さくなるため検出不可能。v1 の限界として許容 |

---

## 9. 次のステップ

1. **実装（次回セッション）**: `scripts/motion_intelligence_v1.py` の実装
2. **PR061 dry-run**: 設計パラメータ（32px / search=16 / thresh=8.0）で実行
3. **結果評価**: 183s区間の PTA 検出・0〜183s の BACKGROUND_FLOW 支配を確認
4. **パラメータ調整**: 成功基準に応じてチューニング
5. **AI Observation Report 統合**: motion_events.csv を generate_ai_observation_report.py に渡す

---

## 10. 設計承認チェックリスト

- [x] OpenCV 利用不可を確認
- [x] Pillow + numpy 方式（A案）を選定
- [x] グリッドサイズ・探索窓・閾値のデフォルト値を決定
- [x] イベント分類（8種）と優先順位を定義
- [x] PR061 での検証方針を確定
- [x] generate_ai_observation_report.py との互換性を確認
- [ ] ユーザー承認
- [ ] 実装開始
