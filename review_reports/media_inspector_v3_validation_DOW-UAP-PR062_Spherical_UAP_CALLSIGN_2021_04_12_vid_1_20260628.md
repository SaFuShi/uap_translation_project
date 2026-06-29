# Media Inspector v3 Validation Report

- 対象: DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1
- article_id: R02-054 / #2_054
- 実行日: 2026-06-28
- フロー: Media Inspector v3（Motion Intelligence v3 主軸）
- 担当: AI（Claude Sonnet 4.6）

---

## 1. 選定理由

未投稿VIDキュー（unpublished_vid_reanalysis_plan_20260626.md）より以下の基準で選定：

- PR062以降を優先（指定）
- PR059・PR060・PR061はframe_delta_runs/20260627_v2に既存データあり（処理済み）
- PR062は全処理未着手・note_draftが30秒間隔ベース（30s前提: **Yes**）
- 尺289.6秒（4分49秒）のHIGH優先度映像
- 同日同一イベント4本連続（PR060〜PR063）の中でvid_1（PR062）は前後関係把握のため重要

---

## 2. 実行ログ

### Step 1: Adaptive Frame Extraction

```
スクリプト : scripts/extract_frames_adaptive.py
間隔       : 3秒（手動指定）
入力       : raw_media/video/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1.mp4
出力       : data/adaptive_frames/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/
抽出枚数   : 97枚
失敗       : 0
```

### Step 2: Motion Intelligence v3 実行

```
スクリプト : scripts/motion_intelligence_v3.py
mode       : adaptive
出力       : data/motion_intelligence_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/v3/
総ペア数   : 96
実行日時   : 2026-06-28 17:19:55
```

**イベント集計**

| イベント | 件数 |
|---------|------|
| STATIC | 1 |
| LIGHTING_SHADOW_CHANGE | 34 |
| POSSIBLE_TARGET_APPEAR | 8 |
| RELATIVE_OBJECT_MOTION | 53 |
| CAMERA_TRACK | 0 |
| BACKGROUND_FLOW | 0 |
| POSSIBLE_TARGET_DISAPPEAR | 0 |
| REVIEW_REQUIRED | 0 |

**select_mode 内訳**

| mode | 件数 |
|------|------|
| sticky | 53 |
| seed | 8 |
| lost | 30 |
| no_seed | 5 |

trail_detected ペア数: 1（pair_36: 105s→108s、trail_cells=21、DOWN_LEFT方向）

**検出トラック**

| track_id | 区間 | 尺 | drift(px/s) | R² | 分類 | 方向 | conf |
|----------|------|----|------------|-----|------|------|------|
| 1 | 9-12s（00:09-00:12） | 3s | 0.0 | 1.0 | SHORT_TRACK | CENTER | 0.614 |
| 2 | 24-54s（00:24-00:54） | 30s | 12.32 | 0.675 | **LINEAR_MOTION** | RIGHT | **0.876** |
| 3 | 72-135s（01:12-02:15） | 63s | 0.74 | 0.034 | **ERRATIC_MOTION** | LEFT | 0.52 |
| 4 | 147-171s（02:27-02:51） | 24s | 0.86 | 0.085 | **ERRATIC_MOTION** | CENTER | 0.538 |
| 5 | 183s（03:03） | 1s | 0.0 | 0.0 | SINGLE_APPEARANCE | UP_RIGHT | 0.254 |
| 6 | 198-213s（03:18-03:33） | 15s | 10.54 | 0.53 | **LINEAR_MOTION** | RIGHT | **0.841** |
| 7 | 225-276s（03:45-04:36） | 51s | 10.22 | 0.461 | **LINEAR_MOTION** | LEFT | **0.835** |
| 8 | 288s（04:48） | 1s | 0.0 | 0.0 | SINGLE_APPEARANCE | RIGHT | 0.249 |

### Step 3: Targeted Frame Extraction

Motion Intelligence v3 track区間を1秒間隔で補強抽出。

| セグメント | 区間 | 対象 track | 抽出理由 |
|-----------|------|-----------|---------|
| Seg-A | 18-60s（00:18-01:00） | track_2 | LINEAR_MOTION conf=0.876（最高信頼度）|
| Seg-B | 69-141s（01:09-02:21） | track_3 | ERRATIC_MOTION + trail@105-108s |
| Seg-C | 141-177s（02:21-02:57） | track_4 | ERRATIC_MOTION CENTER |
| Seg-D | 192-219s（03:12-03:39） | track_6 | LINEAR_MOTION conf=0.841 |
| Seg-E | 219-282s（03:39-04:42） | track_7 | LINEAR_MOTION conf=0.835（51秒・最長）|

抽出総計: 240枚
出力先: data/motion_intelligence_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/targeted_frames/

---

## 3. 映像構造の観察（フレーム目視確認）

| タイムコード | 観察内容 |
|------------|---------|
| 0s（00:00） | 雲背景・モーションブラーあり・Nマーカー下方・クロスヘア CENTER・黒塗り矩形 |
| 24s（00:24） | 雲背景・コーナーマーカー（L字シアン）出現・Nマーカー下方 |
| 36s（00:36） | 雲背景・コーナーマーカー継続 |
| 54s（00:54） | 雲背景・RIGHT方向に**小さな暗色ドット状物体**（約x=940, y=342）可視 |
| 72s（01:12） | **背景が雲→砂漠地形に急変**・小暗色ドット LEFT上（約x=450, y=290）可視 |
| 108s（01:48）| 地形テクスチャ・trail_detected（21セル・DOWN_LEFT） |
| 135s（02:15）| 雲背景に戻る・小暗色ドット（約x=430, y=420）可視 |
| 198s（03:18）| 雲背景・Nマーカー位置変化（左上寄り）・コーナーマーカーなし |
| 252s（04:12）| 雲背景・コーナーマーカー再出現・小暗色ドット LEFT付近 |

**映像構造推定**

```
0-21s    雲背景・初期フレーム
21-57s   雲背景・track_2：小暗色ドットが右方向へ線形移動（最高信頼度区間）
57-69s   LSC多発・遷移
69-75s   背景急変：雲→砂漠地形（track_3 開始）
72-135s  地形+雲混在・track_3 ERRATIC・trail@105-108s（DOWN_LEFT）
135-147s 雲背景に戻る・遷移
147-174s 雲背景・track_4 ERRATIC CENTER
174-198s 遷移
198-216s 雲背景・track_6 LINEAR RIGHT
216-225s 遷移
225-279s 雲背景+コーナーマーカー・track_7 LINEAR LEFT（最長51秒）
279-289s 終端
```

---

## 4. 既存 note_draft との比較評価

### 既存 note_draft の前提

- 使用フレーム: 0, 30, 60, 90, 120, 150, 180, 210, 240, 270s（10枚・30秒間隔）
- 記述: 「球形物体は抽出フレームでは背景地形と明確に区別できる形では確認できませんでした」
- 背景記述: 「背景は岩山・渓谷・砂漠地形が中心」

### 旧フロー（30秒間隔）の見落とし

| 見落とし項目 | 詳細 | 影響度 |
|------------|------|--------|
| track_2（24-54s）完全未把握 | 30sと60sのみ。最重要の暗色ドット移動を「地形と区別できない」と誤評価 | **高** |
| 69-72sの背景急変 | 60sと90sの間に急変。変化点が完全に欠落 | **高** |
| trail@105-108s 未検出 | 90sと120sのみ。細長いcluster（21セル）が完全欠落 | **高** |
| track_3 ERRATIC（72-135s）の誤記述 | 63秒間の不規則運動が「確認できない」で片付けられている | 中 |
| track_6・track_7 未把握 | 198-213s・225-276sの2本のLINEAR_MOTIONが現ドラフトでは検出されていない | 中 |
| 「背景が岩山・渓谷地形が中心」の誤表現 | 映像の大半は**雲背景**。地形は69-135s付近の一部に過ぎない | **高** |

### note_draft の主要誤記述

1. **「背景は岩山・渓谷・砂漠地形が中心」** → 実際の大半は**雲背景**
2. **「球形物体は確認できず」** → 54s・135s・252sに**小暗色ドット状物体**が可視
3. **「モーションブラー」の記述はあるが方向・速度は未記載** → track_2で12.3px/s・RIGHT方向を特定

---

## 5. note_draft 修正候補の整理

本ドキュメント時点では note_draft 本文は変更しない。人間査読完了後に修正する。

| 箇所 | 現状の記述 | 修正候補 |
|------|-----------|---------|
| 「共通の観察事項」背景説明 | 「背景は岩山・渓谷・砂漠地形が中心」 | 「背景の大半は雲面（上空から俯瞰した雲層）。69-135s（01:09-02:15）付近では砂漠・荒地地形が一時的に確認できる」 |
| 「球形UAP物体は確認できず」 | 「抽出フレームでは確認できませんでした」 | 「24-54s（00:24-00:54）・135s（02:15）・225-276s（03:45-04:36）付近に小さな暗色ドット状物体が確認できる。同物体が球形UAPとされる物体である可能性があるが、形状詳細は低解像度のため確認困難」 |
| AI解析メモ | 「0〜270秒・30秒間隔の10フレーム」 | 「Motion Intelligence v3解析（2026-06-28）。3秒間隔97枚+1秒間隔240枚（重要区間補強）。8トラック検出。最重要区間: 24-54s（LINEAR_MOTION conf=0.876）・225-276s（LINEAR_MOTION conf=0.835）」 |
| アイキャッチ | frame_0000.png（0秒）またはframe_0060.png（1:00） | frame_0054.png（54s・00:54）推奨（暗色ドット状物体が最も明確） |

---

## 6. 進行状況

| ステップ | 状態 |
|---------|------|
| Adaptive Frame Extraction | ✅ 完了 |
| Motion Intelligence v3 | ✅ 完了 |
| Targeted Frame Extraction | ✅ 完了 |
| AI Observation Report 生成 | ✅ 完了（別ファイル参照）|
| 人間によるソース映像確認 | ⏳ 未実施（人間査読待ち）|
| Ground Truth 記録 | ⏳ 人間確認後 |
| note_draft 本文修正 | ⏳ 人間査読完了後 |

---

## 7. 出力ファイル一覧

| ファイル | パス |
|---------|------|
| adaptive_frames（97枚） | `data/adaptive_frames/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/` |
| motion_events.csv | `data/motion_intelligence_runs/20260628/DOW-UAP-PR062_.../v3/motion_events.csv` |
| track_events.csv | `data/motion_intelligence_runs/20260628/DOW-UAP-PR062_.../v3/track_events.csv` |
| summary.md | `data/motion_intelligence_runs/20260628/DOW-UAP-PR062_.../v3/summary.md` |
| targeted_frames（240枚） | `data/motion_intelligence_runs/20260628/DOW-UAP-PR062_.../targeted_frames/` |
| AI Observation Report | `review_reports/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_ai_observation_report_v3_20260628.md` |
| docs v3追記 | `docs/media_inspector_architecture_v2.md`（Section 11追記）|
