# PR055 Adaptive Frame Pipeline 再分析レポート

- 作成日: 2026-06-26
- 対象: R02-045 / #2_045 / DOW-UAP-PR055
- 元動画: `raw_media/video/DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020.mp4`
- 実施パイプライン: Adaptive Frame Extraction → Frame Delta Analysis → Targeted Frame Extraction → フレーム目視確認

---

## 1. 動画技術仕様

| 項目 | 値 |
|------|-----|
| 尺 | 47.27秒 |
| 解像度 | 1920×1080（フルHD）|
| コーデック | H.264 |
| フレームレート | 30fps |
| ビットレート | 2,985 kbps |
| ファイルサイズ | 16.82 MB |
| 音声 | AAC（本分析対象外）|

---

## 2. Pipeline 実行結果

### Step 1: Adaptive Frame Extraction（2秒間隔）

| 項目 | 値 |
|------|-----|
| 間隔 | 2秒（手動指定・47秒映像のため全区間カバー重視）|
| 出力フレーム数 | **24枚** |
| 出力先 | `data/adaptive_frames/20260626/DOW-UAP-PR055_Spherical_UAP_over/` |
| タイムスタンプ範囲 | 0s 〜 46s（偶数秒） |

### Step 2: Frame Delta Analysis

| 項目 | 値 |
|------|-----|
| 比較ペア数 | 23 |
| ts_mode | seconds（ファイル名=タイムスタンプ秒） |
| 出力先 | `data/frame_delta_runs/20260626/DOW-UAP-PR055_Spherical_UAP_over/DOW-UAP-PR055/` |

| イベント | 件数 |
|---------|------|
| CUT | 8 |
| OBJECT_MOVE | 15 |
| APPEAR | 0 |
| DISAPPEAR | 0 |
| CAMERA_MOTION | 0 |
| STATIC | 0 |

### Step 3: Targeted Frame Extraction（1秒間隔）

| 項目 | 値 |
|------|-----|
| トリガー | CUT + OBJECT_MOVE（pos_delta ≥ 20px）|
| マージ後ゾーン | 1区間（0s〜47s 全体）|
| 新規抽出フレーム数 | **36枚** |
| スキップ（重複） | 12枚 |
| 出力先 | `data/adaptive_frames/20260626/DOW-UAP-PR055_Spherical_UAP_over_targeted/` |

**フレーム合計**: Adaptive 24枚 + Targeted 36枚 = **0〜47秒の1秒間隔完全カバー**

---

## 3. 映像構造の確定（最重要発見）

### 3部構成テロップ映像（既存 note_draft が未認識）

フレーム目視確認により、本映像が**2枚のテキストカードによって区切られた3部構成**であることが判明した。

```
[黒画面] 0-1s
    ↓
[Section 1] 2-11s  ─────────────── 第一映像区間
    ↓
[テキストカード #1] 12-13s  ←★ 既存draftで未認識
    ↓
[Section 2] 14-28s ─────────────── 拡大・加工版映像
    ↓
[テキストカード #2] 29-31s  ←★ 既存draftで未認識
    ↓
[Section 3] 32-47s ─────────────── オリジナルセンサー映像
```

### テキストカード内容（実際の映像フレームから目視確認）

**テキストカード #1（12s〜13s）**:
```
sharpened, zoomed
motion tracked
contrast enhanced
slow to 60% speed
```
（黒背景に白テキスト、1920×1080）

**テキストカード #2（30s〜31s）**:
```
Original Video
```
（黒背景に白テキスト、1920×1080）

### 各 Section の特性

| Section | 時間帯 | 内容 | 視覚的特徴 |
|---------|--------|------|-----------|
| Section 1 | 2-11s | 第一映像区間（原版または初見映像）| 全画面IR映像・黒マスキングなし・球形物体小さめ |
| テキスト #1 | 12-13s | 加工パラメータ告知 | 黒背景白テキスト |
| Section 2 | 14-28s | 拡大・加工版 | 球形物体が大きく鮮明・一部黒マスキング（上部） |
| テキスト #2 | 29-31s | 「Original Video」移行 | 黒背景白テキスト |
| Section 3 | 32-47s | オリジナルセンサー映像 | 緑クロスヘア表示・四辺に黒マスキング |

### Delta 分析との対応

| 発見 | Delta での対応 | 説明 |
|------|--------------|------|
| テキストカード #1（12s）| pair_6: CUT, mean_diff=123.1, bright_count 48,435→133,554 | 白テキストが高輝度ピクセルを急増させた |
| テキストカード #2（30s）| pair_15: CUT, mean_diff=113.6, pair_16: CUT, mean_diff=85.3 | 「Original Video」テキスト |
| Section 3 の物体移動 | pair_17-23: OBJECT_MOVE, pos_delta 20-46px, bright_cx (877,640)→(730,494) | センサー追跡による明輝点の移動 |

---

## 4. フレーム別目視確認結果

### Section 1（2-11s）: 第一映像区間

| フレーム | タイムスタンプ | 内容 |
|---------|-------------|------|
| frame_0000.png | 0s | 黒画面（ファイルサイズ 29KB）|
| frame_0002.png | 2s | グレースケールのIR映像・雲が画面を覆う・球形物体確認できず |
| **frame_0004.png** | **4s** | **グレースケールIR映像・白い雲の背景に対して左上部に暗い球形物体が明確に確認できる** ★既存draft未捕捉 |
| frame_0006.png | 6s〜11s | 雲の映像（球形物体の視認性は確認対象。4sより視認困難な可能性）|

**★重要: 既存 note_draft の「00:05〜00:15 物体確認できず」は誤り。少なくとも4sに球形物体が明確に確認できる。**

### Section 2（14-28s）: 拡大・加工版

| フレーム | タイムスタンプ | 内容 |
|---------|-------------|------|
| frame_0014.png | 14s | 雲の映像・左上に黒マスキング・左寄りに微小な白い点（物体候補）|
| frame_0020.png | 20s | **雲の背景に対して中央に暗い球形物体が確認できる**（加工後）|
| **frame_0022.png** | **22s** | **白い雲に対して中央に大きく鮮明な暗い球形物体が確認できる。左上に黒マスキング** ★最も明確な区間の一つ |
| **frame_0025.png** | **25s** | **白い雲に対して上中央部に暗い球形物体が非常に鮮明に確認できる。輪郭明瞭。既存draftの frame_0025 相当（5秒間隔で偶然一致）** |
| frame_0026-0028.png | 26-28s | 雲が球形物体を覆いつつある（確認対象）|

### テキストカード #2 周辺（29-31s）

| フレーム | タイムスタンプ | 内容 |
|---------|-------------|------|
| frame_00029.png | 29s | **黒画面**（ファイルサイズ 9.4KB = 最小）← 黒画面開始は既存draftの「30s」ではなく **29s**|
| frame_0030.png | 30s | 「**Original Video**」白テキスト（黒背景）|
| frame_0031.png | 31s | 黒画面（テキストカード終了）|

### Section 3（32-47s）: オリジナルセンサー映像（"Original Video"）

| フレーム | タイムスタンプ | 内容 |
|---------|-------------|------|
| frame_0032.png | 32s | 雲のIR映像・緑クロスヘア・四辺に黒マスキング |
| frame_0036.png | 36s | 雲のIR映像・緑クロスヘア（+マーク）が画面中央に確認できる・四辺に黒マスキング |
| **frame_0040.png** | **40s** | **雲のIR映像・緑クロスヘア・黒マスキング・画面左上部に小さな暗い点（球形物体とみられる）が確認できる** |
| frame_0046.png | 46s | 雲のIR映像・緑クロスヘア・黒マスキング・球形物体の視認困難（雲に覆われた可能性）|

**備考**: Section 3 の緑クロスヘアはオリジナルセンサー映像由来（テキスト #1 の "motion tracked" 処理で除去/置換された）とみられる。

---

## 5. Delta 分析：詳細解釈

### bright_count 推移と映像構造の対応

| 区間 | bright_count 範囲 | 解釈 |
|------|-----------------|------|
| 0-11s（Section 1）| 48,434〜60,530 | 通常のIR映像（輝点は雲の明るい部分）|
| 12-13s（テキスト #1）| 133,554 | **白いテキスト文字が高輝度ピクセルを急増**（約2.8倍）|
| 14-28s（Section 2）| 48,468〜48,714 | 加工済み映像（輝点分布は Section 1 と類似）|
| 29-31s（テキスト #2）| 48,566〜66,354 | 「Original Video」テキスト（輝点やや増）|
| 32-47s（Section 3）| 156,667〜204,763 | **緑クロスヘアが高輝度ピクセルを大量生成**（約3倍）|

### 明輝点中心座標の推移

Section 1（2-22s）: 明輝点が (1419, 267) 付近に固定
→ 画面右上の同一の雲の明るい部位を継続して追跡

Section 2 CUT 区間（22-28s）: 若干の変化（背景の明るさ変動）
→ 球形物体が雲に近づくにつれて映像内のコントラスト変化

Section 3（32-47s）: 明輝点が (877,640) → (730,494) へ一貫して移動
→ 緑クロスヘアが左上方向に移動（約147px / 14秒）
→ センサーが対象を追跡してカメラが左上に振れているか、または対象が右下から移動しているとみられる

---

## 6. 既存 note_draft との差異（修正候補）

### 既存 draft が誤っていた点・未記述の点

| # | 項目 | 既存 draft の記述 | 実際 |
|---|------|-----------------|------|
| 1 | 映像構造 | 記述なし（3部構成未認識）| **テキストカード2枚で区切られた3部構成** |
| 2 | テキストカード #1（12s）| 記述なし | "sharpened, zoomed, motion tracked, contrast enhanced, slow to 60% speed" |
| 3 | テキストカード #2（30s）| 「黒画面」と記述 | "Original Video"（テキスト）|
| 4 | 黒画面開始 | 「00:30」| **00:29（29s）** |
| 5 | 4s の球形物体 | 「00:05〜00:15 物体確認できず」| **4sに暗い球形物体が明確に確認できる** |
| 6 | Section 2 のサイズ感 | 「frame_0025（00:25）は輪郭が最も明確」| 正しいが加工済み映像であることが未記述 |
| 7 | 緑クロスヘアの文脈 | 「追尾マーカーと推定されるが確認できません」| Section 3 = "Original Video" のセンサー表示であることが確定 |
| 8 | Section 3 の球形物体 | 「frame_0040（00:40）: フレーム上部に小さな暗い点」とのみ記述 | **Section 3 が "Original Video"（オリジナルセンサー出力）であることが確定** |
| 9 | アイキャッチ | frame_0005（5s）または frame_0025（25s）| **frame_00025.png（targeted/25s）が最適**（加工版での最鮮明フレーム）|
| 10 | 映像加工の明示 | 記述なし | Section 2 は "sharpened, zoomed, contrast enhanced" を明示すべき |

---

## 7. アイキャッチ推奨フレーム

### 最有力: frame_0022.png または frame_00025.png（Section 2・加工版）

| フレーム | パス | 推奨理由 |
|---------|------|---------|
| frame_0025.png | `data/adaptive_frames/20260626/DOW-UAP-PR055_Spherical_UAP_over/frame_0025.png` | 球形物体が最も鮮明（既存 draft の推奨と一致） |
| frame_0022.png | `data/adaptive_frames/20260626/DOW-UAP-PR055_Spherical_UAP_over/frame_0022.png` | 球形物体が鮮明・中央配置 |
| frame_0004.png | `data/adaptive_frames/20260626/DOW-UAP-PR055_Spherical_UAP_over/frame_0004.png` | Section 1 で物体が視認できる（小さめ） |
| frame_0040.png | `data/adaptive_frames/20260626/DOW-UAP-PR055_Spherical_UAP_over/frame_0040.png` | Section 3（オリジナル）+ 緑クロスヘア + 物体の点（上部左）|

**最終推奨**: `frame_0025.png`（加工版で最も鮮明・物体形状が明確）または `frame_0022.png`（同等）

ただし、note_draft に使用する場合は「加工・拡大処理済み映像からの抽出（contrast enhanced, sharpened, zoomed）」であることを明記すること。

---

## 8. 人間確認が必要なフレーム一覧

以下を Finder で確認することを推奨。

### 優先確認（Phase 1）

| ファイルパス | 秒 | 確認目的 |
|------------|-----|---------|
| `...PR055_Spherical_UAP_over/frame_0004.png` | 4s | Section 1 での球形物体の視認確認・大きさ・位置 |
| `...PR055_Spherical_UAP_over/frame_0006.png` | 6s | 4s → 6s での物体変化（雲に入る？）|
| `...PR055_Spherical_UAP_over/frame_0008.png` | 8s | 8s での物体視認性 |
| `...PR055_Spherical_UAP_over/frame_0010.png` | 10s | Section 1 末期の状態（直前フレーム）|
| `...PR055_Spherical_UAP_over/frame_0022.png` | 22s | Section 2 での球形物体（明確区間中盤）|
| `...PR055_Spherical_UAP_over/frame_0025.png` | 25s | **アイキャッチ候補・最鮮明** |
| `...PR055_Spherical_UAP_over/frame_0026.png` | 26s | Section 2 末期・物体が雲に入り始める？|
| `...PR055_Spherical_UAP_over/frame_0040.png` | 40s | Section 3 での小さな球形物体の点の確認 |
| `...PR055_Spherical_UAP_over/frame_0036.png` | 36s | Section 3 の緑クロスヘアの確認 |

### 補足確認（Phase 2）

| ファイルパス | 秒 | 確認目的 |
|------------|-----|---------|
| `...PR055_Spherical_UAP_over_targeted/frame_00005.png` | 5s | Section 1 の5s（既存draftが「物体なし」と誤記）|
| `...PR055_Spherical_UAP_over_targeted/frame_00009.png` | 9s | 物体が雲に入る瞬間候補 |
| `...PR055_Spherical_UAP_over_targeted/frame_00015.png` | 15s | Section 2 開始直後 |
| `...PR055_Spherical_UAP_over_targeted/frame_00027.png` | 27s | Section 2 末期・物体と雲の関係 |
| `...PR055_Spherical_UAP_over_targeted/frame_00043.png` | 43s | Section 3 中盤 |
| `...PR055_Spherical_UAP_over_targeted/frame_00047.png` | 47s | 映像末端 |

---

## 9. VLM 解析候補フレーム

Section 2（加工済み）の明確な球形物体フレームが最有力候補。

| フレーム | 秒 | VLM 推奨理由 |
|---------|-----|------------|
| frame_0022.png | 22s | 大きく鮮明な球形物体・最も VLM 検出しやすい |
| frame_0025.png | 25s | 球形物体が中央上部に鮮明・形状評価に最適 |
| frame_0020.png | 20s | Section 2 での物体（中央部）|
| frame_0004.png | 4s | Section 1（オリジナル）での物体（小さめ・検出難度高）|
| frame_0040.png | 40s | Section 3（オリジナル）での物体（点状・検出難度高）|

**注意**: テキストカード（12s・30s）・黒画面（0,1,29s）は VLM 解析対象外。

---

## 10. note_draft 修正候補サマリー

note_drafts は本フェーズでは変更しない。以下は公開前修正が必要な内容の整理。

### 必須修正

1. **映像3部構成の記述を追加**
   - Section 1（2-11s）/ テキストカード #1 / Section 2（14-28s）/ テキストカード #2 / Section 3（32-47s）

2. **テキストカード内容を明記**
   - 12s: "sharpened, zoomed, motion tracked, contrast enhanced, slow to 60% speed"
   - 30s: "Original Video"

3. **4s の球形物体を追記**
   - 「00:05〜00:15 物体確認できず」→ 削除または修正
   - 「4s にも暗い球形物体が確認できる（Section 1 / 拡大処理前の映像）」に修正

4. **Section 2 の球形物体が加工済みであることを明記**
   - 現状: 「球形物体が確認できる」のみ
   - 修正: 「sharpened, zoomed, contrast enhanced, slow to 60% speed で加工された映像において球形物体が明確に確認できる」

5. **テキストカード #2 の記述修正**
   - 「00:30（黒画面）」→ 「00:29 黒画面・00:30-31 'Original Video' テキストカード」

6. **Section 3 の緑クロスヘアの文脈明記**
   - "Original Video" ラベルの映像区間（32-47s）での確認
   - センサー原映像由来のトラッキング表示とみられる

7. **アイキャッチ画像パスの更新**
   - 現状: `thumbnails/.../frame_0005.png`（物体が確認できないフレーム）
   - 推奨: `data/adaptive_frames/20260626/DOW-UAP-PR055_Spherical_UAP_over/frame_0025.png`（最鮮明）

### 推奨修正（断定表現の修正）

8. **「追尾マーカーと推定されるが確認できません」（緑クロスヘア）**
   - → "Original Video" セクションの文脈で記述すれば「原映像に含まれるセンサー表示」としてより明確に記述可能

9. **Section 1 での物体の「in and out of clouds」動作の記述**
   - Section 1 の 4s に明確な球形物体 → 8-11s で雲内に入る（要人間確認）
   - Section 2（加工版）でも同動作が確認できる（14-28s）

---

## 11. 公開前推奨アクション

| アクション | 優先度 | 内容 |
|-----------|--------|------|
| 人間確認（Phase 1） | **必須** | 上記9フレームを Finder で目視確認 |
| note_draft 修正 | **必須** | 上記10項目の修正を実施 |
| 人間確認（Phase 2） | 推奨 | 補足フレーム6枚の確認 |
| VLM 解析 | オプション | LM Studio 起動時に実施 |
| 映像全体の直接確認 | 推奨 | 特に Section 1（2-11s）での物体の「in/out of clouds」動作を時系列で確認 |

---

## 12. 成果物一覧

| ファイル | サイズ |
|---------|-------|
| `data/adaptive_frames/20260626/DOW-UAP-PR055_Spherical_UAP_over/` | 19 MB / 24枚 |
| `data/adaptive_frames/20260626/DOW-UAP-PR055_Spherical_UAP_over_targeted/` | 27 MB / 36枚 |
| `data/frame_delta_runs/20260626/DOW-UAP-PR055_Spherical_UAP_over/DOW-UAP-PR055/frame_delta.csv` | 23行 |
| `data/frame_delta_runs/20260626/DOW-UAP-PR055_Spherical_UAP_over/DOW-UAP-PR055/summary.md` | — |
| 本レポート | — |

**総フレーム数（重複除く）**: 24 + 36 = 60枚（0〜47s の1秒間隔完全カバー）
