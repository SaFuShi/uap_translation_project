# PR054 / PR053 Adaptive Frame + Delta 再分析計画

- 作成日: 2026-06-26
- 対象: R02-044（DOW-UAP-PR054）/ R02-043（DOW-UAP-PR053・公開済み追加再監査）
- 公開停止: #2_044 以降 — 本再分析完了まで公開再停止
- 出力予定: `review_reports/pr054_pr053_delta_analysis_results_20260626.md`

---

## 1. 公開停止の判断根拠

### PR054（#2_044 / R02-044）
- 映像尺：237秒（3:57）に対し、既存 note_draft は 30 秒間隔 8 フレームのみを前提
- ファイル名「Erratic movement（不規則な動き）」が示す動きを分析できていない
- 短時間に現れる UAP 候補を見逃している可能性がある
- フレーム間差分による速度・方向・出現消失の把握がない

### PR053（#2_043 / R02-043 — 公開済み）
- 映像は同一シーンを 3 段階速度で繰り返す構造とみられる（人間確認済み）
- 高速横切りイベント（約 3 秒）は公開記事に反映済みだが、フレーム差分による定量分析がない
- 再生速度違いの区間境界（0〜8s / 9〜14s / 15〜21s）が推定のみで確定していない
- 公開済み記事: Published Article Evolution の「Observation Update」対象とする

---

## 2. 既存フレームデータ

| 記事 | source file | 既存フレーム | 間隔 | 収録場所 |
|------|-------------|------------|------|---------|
| R02-043 | PR053 | 22枚（今回抽出済み） | 1秒 | `data/adaptive_frames/20260626/DOW-UAP-PR053_.../` |
| R02-044 | PR054 | 79枚（今回抽出完了）| 3秒 | `data/adaptive_frames/20260626/DOW-UAP-PR054_.../` |

### PR054 フレームタイムライン
- frame_0001 = 3s / frame_0079 = 237s
- 既存サムネイル（30秒間隔・8枚）→ 新規 Adaptive（3秒間隔・79枚）で約10倍のカバレッジ
- 既存サムネイルでカバーできていた区間: 0・30・60・90・120・150・180・210 秒の8点のみ

---

## 3. Frame Delta Analysis 設計

### 目的
連続フレーム間の差分を定量化し、以下を自動検出する。

| 検出対象 | 指標 |
|---------|------|
| カット変化 | フレーム全体の平均差分が閾値超え（突然の場面転換） |
| カメラ動き | 差分が画面全体に分散（パン・ズーム・チルト） |
| 対象物移動 | 差分が局所的に集中（対象物だけが動いた） |
| 対象物出現/消失またはフレームイン/アウト | 前フレームに存在した明輝点が次フレームで消失（消失とフレームアウトは映像のみでは区別不可） |
| 静止 | 差分がほぼゼロ（映像停止・同一フレーム反復） |

### 出力フィールド（per-frame CSV）

```
frame_id, timestamp_s, mean_diff, max_diff, std_diff,
hotspot_x, hotspot_y, hotspot_size,
event_type,          # CUT / CAMERA_MOTION / OBJECT_MOVE / DISAPPEAR / STATIC
prev_bright_x, prev_bright_y,  # 前フレームの最輝点
curr_bright_x, curr_bright_y,  # 現フレームの最輝点
position_delta_px,   # 輝点の移動量（pixel）
notes
```

---

## 4. scripts/frame_delta_analyzer.py 設計案

```python
#!/usr/bin/env python3
"""
frame_delta_analyzer.py
連続フレーム間の差分を分析し、UAP候補の動き・カット変化・カメラ動きを検出する。

使用方法:
  python3 scripts/frame_delta_analyzer.py \
    --frames-dir data/adaptive_frames/20260626/<slug>/ \
    --output data/vlm_runs/delta_analysis_20260626/<slug>_delta.csv \
    [--execute]  # なければ dry-run

依存: Python 標準ライブラリ + Pillow (pip install pillow)
"""

# --- 主要パラメータ ---
CUT_THRESHOLD     = 40   # mean_diff がこれ以上 → CUT と判定
MOTION_THRESHOLD  = 15   # mean_diff がこれ以上・局所集中なし → CAMERA_MOTION
OBJECT_THRESHOLD  = 10   # 局所ピーク差分 / mean_diff > 3 → OBJECT_MOVE
STATIC_THRESHOLD  =  3   # mean_diff がこれ以下 → STATIC

# --- 処理フロー ---
# 1. フレームディレクトリを時系列順にソートして読み込む
# 2. 各フレームペア (N, N+1) について:
#    a. グレースケール変換
#    b. 絶対差分画像を生成
#    c. mean_diff / max_diff / std_diff を計算
#    d. 差分のピーク座標 (hotspot_x, hotspot_y) を特定
#    e. 差分集中度 = max_diff / (mean_diff + 1e-6) を計算
#    f. event_type を分類
# 3. 各フレームの最輝点座標を記録し、フレーム間移動量を計算
# 4. CSV に出力
# 5. --verbose 時は event_type ごとのサマリーを表示
```

### 実装上の注意点
- Pillow のみで完結（numpy 不要だが、numpy があれば高速化可）
- 差分集中度（`max_diff / mean_diff`）が高い = 局所的な動き（対象物移動）
- 差分が全体に均等分散 = カメラ動き
- `mean_diff` が突然大きくなる = カット
- 輝点追跡は単純な最大輝度ピクセル座標（精緻な物体追跡ではない）

---

## 5. PR054 分析計画

### 5-1. VLM バッチ評価
- 対象: `data/adaptive_frames/20260626/DOW-UAP-PR054_.../` 79枚
- スクリプト: `scripts/run_vlm_on_adaptive.py --execute --articles R02-044 --run-date 20260626`
- 出力: `data/vlm_runs/adaptive_poc_20260626/R02-044_results.csv`

### 5-2. Frame Delta Analysis
- 対象: 79枚（frame_0001〜0079）→ 78 ペアの差分
- スクリプト: `scripts/frame_delta_analyzer.py`（実装後）
- 検出重点: 球形白輝点の出現・消失・位置変化 / カット変化の有無

### 5-3. 人間確認対象候補（優先区間）

| 区間 | 理由 |
|------|------|
| 0〜30s（frame_0001〜0010）| 映像開始・初出確認 |
| VLM が `visible_candidate=true` を返した全フレーム | UAP候補の優先確認 |
| Delta分析で `event_type=CUT` と判定された前後フレーム | 場面転換確認 |
| Delta分析で `OBJECT_MOVE` かつ `position_delta_px` 大のフレーム | 急激な位置変化 |
| `DISAPPEAR` 判定フレーム | 対象物の消失確認 |

### 5-4. note_draft 修正方針（分析後）
- 要点1〜3 の再構成（Adaptive結果・Delta結果を反映）
- 視覚情報セクションに時系列での出現・消失・位置変化を追記
- 代表フレームをアイキャッチとして適切なものに差し替え
- 断定しない表現を維持しつつ、具体的な観察事実を充実させる

---

## 6. PR053 追加再監査計画（公開済み記事 / Published Article Evolution）

### 6-1. 既存データ
- 1秒間隔 22フレーム: `data/adaptive_frames/20260626/DOW-UAP-PR053_.../`（抽出済み）
- 公開済み記事 URL: https://note.com/deft_ibis3303/n/n91198ae60ede

### 6-2. 追加分析項目

| 分析項目 | 内容 |
|---------|------|
| 高速横切り対象の定量確認 | frame_0001〜0008（通常速区間）での輝点座標変化 |
| 再生速度違いの区間境界確定 | Delta分析で区間境界（カット/スロー転換点）を特定 |
| 3区間の輝点移動速度比較 | 通常速 vs スロー1 vs スロー2 での位置変化量比較 |
| 対象物の出現・消失 | 各区間での最初/最後の検出フレームを記録 |
| 繰り返し再生構成の確認 | 同一または類似フレームの検出（区間間の類似度比較） |

### 6-3. Frame Delta Analysis（PR053）
- 対象: 22フレーム → 21ペア
- 重点: 区間境界（0〜8s / 9〜14s / 15〜21s）でのカット/速度変化検出
- 各区間内の輝点移動量の比較（スロー区間ほど移動量が小さいはず）

### 6-4. Published Article Evolution の扱い
| 項目 | 内容 |
|------|------|
| カテゴリ | Observation Update（観察情報の補強） |
| 優先度 | Medium（公開済みで概要は正確・定量分析の追加） |
| 対応タイミング | PR054 再分析と合わせて実施 |
| 変更内容候補 | 3区間の境界秒数を確定値に更新・速度比較結果を追記 |

---

## 7. 実行フロー

```
Step 1: scripts/frame_delta_analyzer.py を実装
Step 2: PR053（22枚）に対して delta analysis を実行 → 区間境界を確定
Step 3: PR054（79枚）に対して VLM バッチ評価を実行
Step 4: PR054（79枚）に対して delta analysis を実行
Step 5: 人間目視確認（VLM + Delta が示す重要フレームを優先）
Step 6: PR054 note_draft を更新
Step 7: PR053 公開済み記事 Evolution 内容を確定（必要なら note 更新）
Step 8: PR054 公開
```

---

## 8. 除外・制約

| 制約 | 内容 |
|------|------|
| thumbnails/ 変更なし | Adaptive フレームのみ使用 |
| workflow.db / source_registry.csv 変更なし | 公開後に publish_done.py で処理 |
| note_draft 変更なし | 本再分析完了まで保留 |
| git 操作なし | 分析完了後にまとめて commit |
| 外部 API 禁止 | LM Studio ローカル VLM のみ使用 |
