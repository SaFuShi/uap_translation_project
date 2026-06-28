# Motion Intelligence Engine v1 設計書

- 作成日: 2026-06-27
- バージョン: v1
- ステータス: 設計完了・実装待ち
- 実装ターゲット: `scripts/motion_intelligence_v1.py`

---

## 1. 目的と背景

### 1.1 解決する問題

Frame Delta v2（`frame_delta_v2.py`）は輝点（bc値）と画素差分に基づいてイベントを分類する。
PR061 では OBJECT_MOVE=93件を出力したが、人間確認の結果、93件の大部分が以下の誤認であった:

- 山岳地形の日照部分と影の境界変化（地形テクスチャのbc誤検出）
- カメラ/機体移動による背景地形の流動（フレーム全体がほぼ均一に移動）
- 雲や光源変化による局所的な輝度変化

一方で、183s（03:03）頃に出現した対象物候補は、背景地形とは**異なる相対速度・方向**で移動していた。

Frame Delta v2 の問題: 「全画面の変化量」を見るため、背景流動と対象物移動を区別できない。

### 1.2 新しいアプローチ

```
Frame Delta v2:
  画素差分 → 変化量 → イベント分類
  ※ 背景運動と対象物運動を区別しない

Motion Intelligence v1:
  フレーム間差分 → 背景主運動を推定 → 局所偏差を検出 → 相対運動候補を分類
  ※ 背景運動を除外した上で対象候補を検出する
```

### 1.3 設計方針

| 項目 | 方針 |
|------|------|
| 背景運動の推定 | グリッド分割 + ブロックマッチング（簡易版）で支配的な動きベクトルを推定 |
| 対象候補の検出 | 背景主運動ベクトルから大きく逸脱した局所領域を候補化 |
| 除外ルール | 影・日照・地形テクスチャを候補から除外するためのヒューリスティック |
| 実装環境 | Pillow + numpy のみ（OpenCV なし）|
| 人間確認の保持 | 完全自動判定はしない。人間確認対象を 5〜8 区間以内に絞り込む |

---

## 2. 非目標

- UAP の正体判定
- 物理速度・加速度の定量推定
- カメラパラメータ（焦点距離・姿勢角）の厳密推定
- 完全自動判定（人間確認の廃止）
- 背景地形の3次元復元

---

## 3. 入力仕様

```
必須:
  --frames-dir          adaptive frames ディレクトリ
                        （例: data/adaptive_frames/20260627/<source_id>/）
  --delta-csv           frame_delta_v2.csv のパス
  --article-id          記事ID（例: R02-053）
  --source-id           ソースID（例: DOW-UAP-PR061_...）

オプション:
  --targeted-dir        targeted frames ディレクトリ（補完用）
  --video               ソース映像パス（メタデータ取得用）
  --output-dir          出力先（省略時: data/motion_intelligence_runs/<今日>/<source_id>/）
  --grid-size           グリッドセルサイズ px（デフォルト: 32）
  --search-window       ブロックマッチング探索幅 px（デフォルト: 16）
  --rel-motion-thresh   相対運動閾値 px（デフォルト: 8.0）
  --min-candidate-cells 候補セル最小数（デフォルト: 2）
  --execute             実行モード（省略時: dry-run）
  --verbose             詳細ログ出力
```

---

## 4. 出力仕様

```
data/motion_intelligence_runs/<run_date>/<source_id>/
├── motion_events.csv       # 主出力（generate_ai_observation_report.py 互換）
├── motion_events.jsonl     # JSON-Lines 形式（再生成可能）
└── summary.md              # サマリー・人間確認推奨区間
```

### 4.1 motion_events.csv カラム定義

| カラム | 型 | 説明 |
|--------|-----|------|
| `pair_id` | int | フレームペアの通し番号（frame_delta_v2.csv と同一） |
| `frame_prev` | str | 前フレームファイル名 |
| `frame_curr` | str | 現フレームファイル名 |
| `timestamp_prev_s` | float | 前フレームの秒数 |
| `timestamp_curr_s` | float | 現フレームの秒数 |
| `bg_motion_x` | float | 背景主運動ベクトル X 成分（px/frame）|
| `bg_motion_y` | float | 背景主運動ベクトル Y 成分（px/frame）|
| `bg_motion_magnitude` | float | 背景主運動の大きさ（px/frame）|
| `candidate_cells` | int | 相対運動候補セル数 |
| `candidate_bbox_x` | float | 候補領域の重心 X（px）|
| `candidate_bbox_y` | float | 候補領域の重心 Y（px）|
| `candidate_rel_motion` | float | 候補領域の相対運動量（px/frame）|
| `candidate_direction` | str | 候補相対運動方向（UP/DOWN/LEFT/RIGHT/DIAGONAL/NONE）|
| `frame_delta_event` | str | frame_delta_v2.csv の event_type（JOIN 用）|
| `event_type` | str | Motion Intelligence イベント分類 |

### 4.2 generate_ai_observation_report.py との互換性

`event_type` カラムに新しい分類名を入れるため、`generate_ai_observation_report.py` は
既存のフォールバック（REVIEW_REQUIRED 相当として処理）で動作する。
将来的に `generate_ai_observation_report.py` を拡張して Motion Intelligence イベントを
専用表示できるよう、カラム名は frame_delta_v2.csv と揃える。

---

## 5. アルゴリズム設計（Pillow + numpy 実装）

### 5.1 全体フロー

```
for each (frame_prev, frame_curr) pair:
  1. 画像読込・グレースケール変換（Pillow → numpy array）
  2. グリッド分割
  3. 各グリッドセルのブロックマッチング（簡易版）
  4. 背景主運動ベクトル推定（中央値集計）
  5. 局所偏差計算（各セル – 背景ベクトル）
  6. 候補セル抽出（偏差閾値以上）
  7. 候補セルのクラスタリング（連続セルを1つの候補領域に統合）
  8. 照明・影・地形フィルタ（候補から除外）
  9. イベント分類
  10. 出力行を記録
```

### 5.2 グリッド分割

```python
GRID_SIZE = 32  # px（デフォルト）

# 1280×720 フレームの場合: 40×22 = 880 グリッドセル
grid_cols = width // GRID_SIZE
grid_rows = height // GRID_SIZE
```

マスキング領域（黒塗り矩形）は bc=0 かつ uniform → グリッドスコアが低くなるため自然に除外。

### 5.3 ブロックマッチング（簡易版）

各グリッドセル `(i, j)` について:
- 前フレームのセル内ピクセル配列を `block_prev` として取得
- 現フレームの探索窓（`±SEARCH_WINDOW` px）内で MAD（Mean Absolute Difference）最小位置を探索
- 最小 MAD を与えるオフセット `(dx, dy)` = そのセルの運動ベクトル

```python
SEARCH_WINDOW = 16  # px

def block_match(prev_arr, curr_arr, gi, gj, grid_size, search_window):
    x0 = gj * grid_size
    y0 = gi * grid_size
    block = prev_arr[y0:y0+grid_size, x0:x0+grid_size]
    best_mad = np.inf
    best_dx, best_dy = 0, 0
    for dy in range(-search_window, search_window+1, 2):  # stride=2 で高速化
        for dx in range(-search_window, search_window+1, 2):
            x1 = x0 + dx
            y1 = y0 + dy
            if x1 < 0 or y1 < 0 or x1+grid_size > w or y1+grid_size > h:
                continue
            cand = curr_arr[y1:y1+grid_size, x1:x1+grid_size]
            mad = np.mean(np.abs(block.astype(int) - cand.astype(int)))
            if mad < best_mad:
                best_mad = mad
                best_dx, best_dy = dx, dy
    return best_dx, best_dy, best_mad
```

**計算コスト見積もり（32px グリッド、search_window=16、stride=2）:**
- 探索点数: (16/1+1)^2 = 289 → stride=2 で約 81点
- 880 セル × 81 点 × 32×32 画素演算 = 約 7千万回
- numpy vectorized で 1〜2秒/ペア（許容範囲）

### 5.4 背景主運動ベクトル推定

全グリッドセルの運動ベクトルの**中央値**を背景主運動とする:

```python
all_dx = [v[0] for v in grid_vectors]
all_dy = [v[1] for v in grid_vectors]
bg_dx = np.median(all_dx)
bg_dy = np.median(all_dy)
bg_magnitude = np.sqrt(bg_dx**2 + bg_dy**2)
```

中央値を使う理由: 対象物候補は少数（全体の5〜10%以下）のため、外れ値に頑健な中央値で
背景の支配的な動きを推定できる。

### 5.5 相対運動偏差と候補セル抽出

```python
REL_MOTION_THRESH = 8.0  # px（デフォルト）

for each cell (i, j):
    rel_dx = cell_dx - bg_dx
    rel_dy = cell_dy - bg_dy
    rel_magnitude = sqrt(rel_dx**2 + rel_dy**2)
    is_candidate = rel_magnitude >= REL_MOTION_THRESH
```

候補セルが連続（隣接する 4-連結または 8-連結）する場合は1つの候補領域（クラスタ）に統合。

### 5.6 照明・影・地形フィルタ

候補領域を以下の条件でフィルタリングして除外:

| 除外条件 | 判定方法 | 理由 |
|---------|---------|------|
| 低コントラスト領域 | セル内の std < TEXTURE_THRESH=5.0 | 空・均一塗りつぶし領域 |
| 広域一様変化 | 候補セル数 > 全セルの 30% | 全体が変化 = 照明変化 |
| 低 MAD セル | best_mad < MAD_MIN=3.0 | ほぼ変化なし（静止）|
| 高 MAD + bc=0 継続 | bc_prev=0 AND bc_curr=0 | マスキング領域 |
| マスキング領域境界 | セルが画面上下15%内 AND bc=0隣接 | 黒塗り境界ノイズ |

### 5.7 frame_delta_v2.csv とのジョイン

同一 `pair_id` で motion_events.csv と frame_delta_v2.csv を JOIN し、
`frame_delta_event` カラムを付与。

目的: AI Observation Report 生成時に両方の視点を統合できるようにする。

---

## 6. イベント分類

### 6.1 分類定義

| イベント | 略称 | 説明 |
|---------|------|------|
| `BACKGROUND_FLOW` | BF | 全セルがほぼ同方向に動く（カメラ/機体移動による背景流動） |
| `RELATIVE_OBJECT_MOTION` | ROM | 背景主運動と異なる相対速度・方向の局所領域が検出された |
| `CAMERA_TRACK` | CT | 背景流動が大きく（bg_magnitude ≥ 30px）、均一 |
| `ZOOM_OR_CROP` | ZC | 全セルが中心方向または外側方向に発散する放射状運動 |
| `LIGHTING_SHADOW_CHANGE` | LSC | 候補セル数が多く、MAD は高いが運動ベクトルが小さい |
| `POSSIBLE_TARGET_APPEAR` | PTA | 直前フレームで候補なし → 現フレームで候補あり |
| `POSSIBLE_TARGET_DISAPPEAR` | PTD | 直前フレームで候補あり → 現フレームで候補なし |
| `STATIC` | S | bg_magnitude < 2.0 かつ候補セルなし |
| `REVIEW_REQUIRED` | RR | 上記に分類できない、または複数条件が競合する |

### 6.2 分類優先順位（v1）

```
1. STATIC         (bg_magnitude < 2.0 AND candidate_cells == 0)
2. ZOOM_OR_CROP   (放射状ベクトルパターン検出)
3. LIGHTING_SHADOW_CHANGE (候補広域 AND 運動小)
4. POSSIBLE_TARGET_APPEAR (前フレーム候補=0 → 現フレーム候補≥2)
5. POSSIBLE_TARGET_DISAPPEAR (前フレーム候補≥2 → 現フレーム候補=0)
6. CAMERA_TRACK   (bg_magnitude ≥ 30 AND セル均一性高)
7. RELATIVE_OBJECT_MOTION (候補セル≥MIN_CANDIDATE_CELLS)
8. BACKGROUND_FLOW (bg_magnitude ≥ 2.0 AND candidate_cells < MIN)
9. REVIEW_REQUIRED (fallback)
```

---

## 7. PR061 検証方針

### 7.1 成功条件

| 検証項目 | 期待結果 |
|---------|---------|
| 0〜183s（全体の64%）| BACKGROUND_FLOW / CAMERA_TRACK が支配的 |
| 183s（03:03）出現区間 | POSSIBLE_TARGET_APPEAR または RELATIVE_OBJECT_MOTION |
| 189s（03:09）フレームアウト | POSSIBLE_TARGET_DISAPPEAR |
| 193s（03:13）再出現 | POSSIBLE_TARGET_APPEAR |
| 240s（04:00）影区間 | LIGHTING_SHADOW_CHANGE（対象物候補としない）|
| REVIEW_REQUIRED 件数 | 5〜8件以内 |

### 7.2 失敗条件（v1 では許容）

- 183s の対象物が RELATIVE_OBJECT_MOTION に分類されず BACKGROUND_FLOW になる
  → threshold チューニングで対応（v1 のパラメータ探索フェーズ）
- 240s の影が POSSIBLE_TARGET_APPEAR と誤検出される
  → LSC フィルタのチューニングで対応

### 7.3 実行コマンド（実装後）

```bash
# dry-run
python3 scripts/motion_intelligence_v1.py \
  --frames-dir data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0 \
  --delta-csv data/frame_delta_runs/20260627_v2/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0/frame_delta.csv \
  --article-id R02-053 \
  --source-id DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0 \
  --grid-size 32 \
  --search-window 16 \
  --rel-motion-thresh 8.0

# 実行
python3 scripts/motion_intelligence_v1.py \
  [上記と同じ] --execute
```

---

## 8. パフォーマンス見積もり

| 項目 | 見積もり |
|------|---------|
| 1ペアあたりの処理時間 | 1〜3秒（stride=2 最適化あり）|
| PR061（95ペア）の総処理時間 | 90〜285秒（1.5〜5分）|
| メモリ消費 | 1280×720×2フレーム×numpy float32 = 約14MB/ペア |

ボトルネック: ブロックマッチングのネストループ。numpy スライスで内部ループを除去し、
外側ループのみ Python ループにする設計で実用範囲に収める。

---

## 9. OpenCV 将来採用方針

現環境では OpenCV は未インストール。v1 は Pillow + numpy で実装する。

OpenCV が利用可能になった場合、以下を v2 で採用:
- `cv2.calcOpticalFlowFarneback`: 密な Optical Flow（全画素ベクトル）
- `cv2.calcOpticalFlowPyrLK`: スパースな特徴点追跡
- `cv2.findHomography`: 背景運動のホモグラフィ推定

v1 との出力互換性（motion_events.csv のカラム定義）は維持する。

---

## 10. Frame Delta v2 との位置づけ

| 特性 | Frame Delta v2 | Motion Intelligence v1 |
|------|---------------|------------------------|
| 主要入力 | 輝点（bc値）・画素差分 | グリッド運動ベクトル |
| 背景/対象分離 | しない | する（主運動推定）|
| 処理速度 | 速い（数分/本） | やや遅い（1〜5分/本）|
| 適した映像 | 暗視IR・黒背景 | カラー昼間・複雑背景 |
| 誤検出傾向 | 地形輝度変化を拾う | 放射状ズームに弱い可能性 |

両者は補完関係:
- bc値が有効（IR映像・明確な輝点）→ Frame Delta v2 が主
- カラー昼間・地形複雑 → Motion Intelligence v1 が主
- 両方実行して AND/OR で判断 → 理想的な v2+ パイプライン

---

## 11. ディレクトリ構成

```
scripts/
└── motion_intelligence_v1.py       ← 実装ターゲット

data/
└── motion_intelligence_runs/
    └── 20260627/
        └── <source_id>/
            ├── motion_events.csv
            ├── motion_events.jsonl
            └── summary.md

docs/
└── motion_intelligence_engine_v1.md  ← このファイル

review_reports/
└── motion_intelligence_v1_design_20260627.md
```

---

## 12. 実装チェックリスト

### Phase 1: コアエンジン
- [ ] グレースケール変換（Pillow → numpy）
- [ ] グリッド分割ロジック
- [ ] ブロックマッチング関数（stride=2 最適化）
- [ ] 背景主運動推定（中央値）
- [ ] 相対偏差計算
- [ ] 候補セル抽出
- [ ] クラスタリング（連結セル統合）

### Phase 2: フィルタリング
- [ ] 低コントラストフィルタ
- [ ] 広域変化フィルタ
- [ ] マスキング領域除外

### Phase 3: イベント分類
- [ ] 全8イベント分類ロジック
- [ ] 優先順位制御

### Phase 4: 出力
- [ ] motion_events.csv 出力（frame_delta_v2.csv JOIN）
- [ ] motion_events.jsonl 出力
- [ ] summary.md 出力

### Phase 5: 検証
- [ ] PR061 dry-run
- [ ] 183s 区間での PTA/ROM 検出確認
- [ ] 0〜183s での BACKGROUND_FLOW 支配確認
- [ ] REVIEW_REQUIRED ≤ 8件 確認
