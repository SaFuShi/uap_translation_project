# Media Inspector Architecture v4

- 作成日: 2026-06-28
- 前バージョン: `docs/media_inspector_architecture_v2.md`（v3フロー含む）
- 設計背景: PR062再検証で判明したv3の限界を踏まえ、単一エンジンから専門Agent分解へ移行
- ステータス: 設計完了・実装待ち

---

## 1. v3 の限界（PR062で判明）

| 問題 | 詳細 | 根本原因 |
|------|------|---------|
| 背景誤識別 | 地表面（山脈）を雲面と誤認 | 背景分類Agentが存在しない |
| 方向推定の誤り | LEFT/RIGHT判定がカメラパンと対象物移動を分離できない | カメラ運動補正がない |
| 対象物捕捉精度低 | 陰影変化・地形テクスチャ変化を対象物候補と混同 | 照明・影専用解析なし |
| カメラ事象未検出 | ズーム切替・ブラックアウト・ホワイトアウトを検出できない | Camera Analyzerがない |
| 影と本体の混同 | 対象物の影を対象物本体と混同するリスク | 影・照明専用解析なし |
| ERRATIC誤評価 | カメラパン追尾を「不規則運動」と誤判定 | カメラ運動補正がない |

---

## 2. v4 設計思想

```
「1つのエンジンが全てを判断する」→「専門Agentが分業し、統合して判断する」
```

各Agentは**自分の専門領域のみ**を判定し、結果を次のAgentへ渡す。
Observation Generatorが最終的に全Agent出力を統合してレポートを生成する。

**不確実性の明示**: 各Agentは自身の判定に確信度（confidence）と根拠を付与する。断定が困難な場合は `unknown` を返す。推測は推測として明記する。

---

## 3. Agent 構成

### Agent 1: Scene Analyzer

**役割**: フレームの背景・環境・センサー種別を分類する。

**入力**: フレーム画像（PNG、1枚単位）

**処理**:
- 背景種別を分類（色調・テクスチャ・エッジ特性を使用）
- 昼夜・可視光/IRを判定
- センサーモード（カラー・グレースケール・IR）を判定

**出力フィールド**:

| フィールド | 型 | 値の選択肢 |
|-----------|-----|-----------|
| `scene_type` | str | `ground_surface` / `cloud` / `sky` / `sea` / `night_sky` / `desert` / `mountain` / `urban` / `mixed` / `unknown` |
| `ground_subtype` | str | `arid` / `vegetated` / `snow` / `water` / `rocky` / `urban` / `unknown`（scene_type=ground_surfaceの場合）|
| `lighting_type` | str | `daytime` / `nighttime` / `twilight` / `ir` / `unknown` |
| `sensor_mode` | str | `color` / `grayscale` / `ir_white_hot` / `ir_black_hot` / `unknown` |
| `scene_confidence` | float | 0.0〜1.0 |
| `scene_notes` | str | 判定根拠・不確実性の記述 |

**実装方針**:
- ルールベース（色ヒストグラム・輝度統計・テクスチャ分散）を基本とする
- グレー均一テクスチャ → `cloud` / `ground_surface(arid)` 候補
- 低域空間周波数 → `cloud` 優先
- 高域空間周波数（砂・岩のテクスチャ）→ `ground_surface` 優先
- ローカルVLMオプション（LM Studio）での補強は Phase 2 で検討

**PR062での期待動作**:
- 全フレームで `scene_type: ground_surface / ground_subtype: rocky` を返す
- AIが誤認した「雲面」はこのAgentで排除される

---

### Agent 2: Camera Analyzer

**役割**: フレーム間のカメラ運動・画角変化・センサー事象を検出する。

**入力前提（サンプリング依存）**:

| サンプリング間隔 | 検出可能なイベント | 用途 |
|----------------|------------------|------|
| 3秒（粗パス） | カメラパン方向・FOV変化候補区間の特定・EDGE_SURGE | 候補区間の絞り込み |
| 0.25〜0.5秒（精密パス） | BLACKOUT / WHITEOUT / FOV切替の精密タイムコード | 確定検出 |

**3秒サンプリングの限界**: ブラックアウト/ホワイトアウトが3秒未満（PR062では一瞬）の場合、サンプルフレームに現れないため直接検出不能。FOV切替も地形テクスチャの自然変化と混同しやすく、3秒間隔では false positive / false negative 双方が多い。

→ 詳細は「3.5 サンプリング戦略」を参照

**処理**:
- 全体フレームの輝度統計を用いたブラックアウト/ホワイトアウト検出
- 位相相関（外縁領域・クロスヘア除外）を用いたカメラパン/チルト推定
- 空間周波数比（hi_freq_ratio）によるFOV変化候補検出
- Sobelエッジ密度急増（ed_ratio）によるシーン急変後検出

**出力フィールド**:

| フィールド | 型 | 値の選択肢 |
|-----------|-----|-----------|
| `camera_event` | str | `STATIC` / `PAN` / `TILT` / `FOV_IN` / `FOV_OUT` / `EDGE_SURGE` / `BLACKOUT` / `WHITEOUT` / `COMBINED` |
| `cam_dx_px` | int | 背景の水平変位（正=右移動→カメラ左パン）|
| `cam_dy_px` | int | 背景の垂直変位（正=下移動→カメラ上チルト）|
| `pan_confidence` | float | 位相相関の信頼度 0.0〜1.0 |
| `hf_ratio` | float | 空間周波数比（curr/prev）。1.0=変化なし |
| `ed_ratio` | float | Sobelエッジ密度比（curr/prev）|
| `blackout_curr` | bool | 現フレームが全黒（mean_brightness < 10）|
| `whiteout_curr` | bool | 現フレームが全白（mean_brightness > 245）|
| `camera_confidence` | float | 0.0〜1.0 |
| `camera_notes` | str | 判定根拠・不確実性 |

**PR062での実測結果（3秒サンプリング・粗パス）**:
- 25s（00:25）FOV_SWITCH: ⚠️ STATIC（未検出。hf_ratio=1.25 が閾値未満）
- 52s（00:52）ZOOM_IN: ✅ FOV_IN（hf_ratio=2.85）
- 124s（02:04）ZOOM_IN: ✅ FOV_IN（hf_ratio=2.03）
- 249s（04:09）ZOOM_OUT: ⚠️ STATIC（未検出。hf_ratio=0.65 が閾値未満）
- 256s（04:16）BLACKOUT: ⚠️ EDGE_SURGE のみ（事象が瞬間的で直接検出不能）
- パン方向: ✅ 平均 dx=+0.8px/3s（カメラ左追跡→UAP左移動と整合）

**精密パス（0.25秒間隔）での期待改善**:
- BLACKOUT/WHITEOUT を直接検出（256s 区間）
- 25s / 249s の FOV変化を精密なタイムコードで確定
- Camera Analyzer 再実行で 5/5 GT 事象の検出を目標とする

---

### Agent 3: Motion Intelligence v4

**役割**: カメラ運動を補正した上で、対象物候補の相対運動を検出する。

**入力**: フレームペア（prev / curr PNG）＋ Camera Analyzer 出力（pan_dx_px, pan_dy_px）＋ Scene Analyzer 出力

**v3 からの変更点**:

| 項目 | v3 | v4 |
|------|----|----|
| カメラ補正 | なし（位相相関のみ） | Camera Analyzer の補正量を適用 |
| Scene連携 | なし | `scene_type` を受け取り、地表面時は検出閾値を厳しくする |
| 出力追加 | — | `camera_compensated` / `cam_dx` / `cam_dy` / `corrected_cx` / `corrected_cy` |
| 方向出力 | LEFT/RIGHT（断定） | LEFT/RIGHT（補正済み参考値。断定はObservation Generatorが制御）|

**実装方針**: `scripts/motion_intelligence_v4.py` として新規実装（v3 を継承・拡張）

---

### Agent 4: Object Tracker

**役割**: Motion Intelligence v4 の出力から対象物候補を追跡し、フレームイン/アウト・再出現・trail・モーションブラーを管理する。

**入力**: Motion Intelligence v4 出力 ＋ Camera Analyzer 出力

**v3 からの変更点**:
- v3 の track_registry を独立Agentとして分離
- フレームアウト方向の記録（`frameout_edge`: LEFT/RIGHT/TOP/BOTTOM）
- マスキング領域（黒塗り矩形）からの出現/退出を識別（`MASKED_ENTRY` / `MASKED_EXIT`）
- 再出現検出（消失後に近傍で再出現した場合 `REAPPEARED` を付与）
- モーションブラースコアの算出

**出力フィールド**:

| フィールド | 型 | 値の選択肢 |
|-----------|-----|-----------|
| `track_id` | int | — |
| `frame_status` | str | `TRACKED` / `FRAMEOUT` / `REAPPEARED` / `MASKED_ENTRY` / `MASKED_EXIT` / `TRAIL` / `MOTIONBLUR` / `LOST` |
| `position_cx` | float | カメラ補正済みX座標 |
| `position_cy` | float | カメラ補正済みY座標 |
| `velocity_cx` | float | カメラ補正済みX速度（px/s）|
| `velocity_cy` | float | カメラ補正済みY速度（px/s）|
| `frameout_edge` | str | `LEFT` / `RIGHT` / `TOP` / `BOTTOM` / `NONE` |
| `masked_region` | bool | マスキング領域内への移動 |
| `trail_detected` | bool | Trail Cluster 検出 |
| `motionblur_score` | float | 0.0〜1.0 |
| `track_confidence` | float | 0.0〜1.0 |

**PR062での期待動作**:
- 225-235s の「対象物出現」を `MASKED_ENTRY`（マスキング外への移動）として記録
- 複数回のフレームアウトを `FRAMEOUT` として記録

---

### Agent 5: Shadow / Illumination Analyzer

**役割**: 陰影変化・対象物の影・照明状態の変化を解析する。

**入力**: フレーム画像（PNG）＋ Scene Analyzer 出力 ＋ Object Tracker 出力（位置）

**出力フィールド**:

| フィールド | 型 | 説明 |
|-----------|-----|-----|
| `illumination_zone` | str | `SUNLIT` / `SHADOW` / `MIXED` / `UNKNOWN` |
| `terrain_shadow_transition` | bool | 地表の陰→日向（またはその逆）への境界移動 |
| `object_shadow_candidate` | bool | 追跡対象物候補の近傍に影候補が存在 |
| `shadow_object_ambiguous` | bool | 本体と影が区別困難 |
| `illumination_change_type` | str | `NONE` / `SUNLIT_TO_SHADOW` / `SHADOW_TO_SUNLIT` / `EXPOSURE_CHANGE` / `GRADUAL` |
| `illumination_confidence` | float | 0.0〜1.0 |
| `illumination_notes` | str | 判定根拠・不確実性 |

**PR062での期待動作**:
- 69-72s（01:09-01:12）: `terrain_shadow_transition: true`（地表陰影変化→CUTと誤認しない）
- Motion Intelligence がこの区間の輝度変化を「イベント」と誤検出するリスクを低減

---

### Agent 6: Observation Generator

**役割**: 全Agentの出力を統合し、AI Observation Report v4 を生成する。

**入力**: Scene / Camera / Motion / Object / Shadow の全Agent出力

**表現ルール**:

| 項目 | 禁止表現 | 推奨表現 |
|------|---------|---------|
| 背景 | AIの推測による「雲面」 | Scene Analyzerの判定結果をそのまま記述 |
| 対象物の存在 | 「〜が確認できる」（断定）| 「〜の可能性がある」「〜とみられる変化が確認できる」 |
| 移動方向 | 「右へ移動した」| 「画面上で右方向への位置変化が確認できる」＋Camera補正有無を明記 |
| 物体の種類 | 「球形UAP」（断定）| 「球形状とみられる暗色の点状変化」 |
| カメラ事象 | 記述なし | Camera Analyzerの出力を根拠として明記 |
| 陰影変化 | 「背景が急変した」| Shadow Analyzerの判定を根拠として記述 |

---

## 3.5 サンプリング戦略

### 設計原則

フレームサンプリングの最適間隔は Agent の目的によって異なる。v4 では「粗パス→精密パス→超精密パス」の3層構造を採用する。

| Agent | 推奨間隔 | 理由 |
|-------|---------|------|
| Scene Analyzer | 3秒 | シーン種別の変化は数十秒単位。3秒で十分 |
| Camera Analyzer 粗パス | 3秒 | FOV変化候補区間の特定用。既存 adaptive_frames をそのまま利用 |
| Camera Analyzer 精密パス | **0.25〜0.5秒** | BLACKOUT / WHITEOUT / FOV切替の精密検出に必要 |
| **Micro Frame Analyzer** | **全フレーム (30fps)** | **0.1秒以下の瞬間イベント（ブラックアウト 3フレーム≒0.1s）を直接検出** |
| Motion Intelligence v4 | 3秒（等間隔） | 物体運動の連続性追跡には均一間隔が重要。FOV変化フレームはスキップ |

### 3層サンプリングフロー

```
Layer 1: Coarse Pass（粗パス、3秒間隔）
  ├── 入力  : 3秒間隔 adaptive_frames（既存）
  ├── 実行  : Scene Analyzer + Camera Analyzer（全フレームペア）
  └── 出力  : camera_events.csv → 「候補区間」を特定

                    ↓ トリガー条件
        camera_event ∈ {FOV_IN, FOV_OUT, EDGE_SURGE, COMBINED}
        OR  brightness_delta > 30  （輝度急変）
        OR  hf_ratio < 0.40 or > 2.00  （強いFOV変化の疑い）
        OR  手動指定タイムコード（Ground Truth 等）

Layer 2: Targeted Pass（精密パス、0.25秒間隔）
  ├── 入力  : 候補区間 ±5s を 0.25秒間隔で抽出したフレーム群
  ├── 抽出  : extract_frames_targeted.py (Precision Sampler)
  ├── 実行  : Camera Analyzer（精密フレームのみ）
  └── 出力  : camera_events_targeted.csv → FOV 区間の絞り込み

                    ↓ トリガー条件
        camera_event ∈ {EDGE_SURGE, COMBINED}
        OR  brightness_curr が急変（0.25s 間隔でも連続2点以上で変化）
        OR  手動指定タイムコード（精密パス結果から人間が判断）

Layer 3: Micro Pass（超精密パス、全フレーム 30fps）
  ├── 入力  : 候補区間 ±1〜2s のみ（30fps で 30〜60 フレーム）
  ├── 実行  : micro_frame_analyzer.py
  └── 出力  : micro_frame_events.csv / event_candidates.jsonl
              → BLACKOUT / WHITEOUT の正確なタイムコード（1/30秒精度）
```

### 候補区間のマージ仕様

- 各トリガーの前後 ±5s を候補区間とする
- 隣接区間は 2s 以内なら自動マージ（`extract_frames_targeted.py` の `merge_gap` と同仕様）
- マージ後の各区間に 0.25s 間隔でフレームを追加抽出

### PR062 精密抽出が必要な区間

| 区間 | Ground Truth イベント | 粗パス結果 | 精密パス必要性 | 推定追加フレーム数 |
|------|---------------------|----------|--------------|----------------|
| 22.0〜30.0s | FOV_SWITCH@25s（ワイド切替） | ⚠️ STATIC（未検出） | **必須** | 33 |
| 49.0〜57.0s | ZOOM_IN@52s（ズーム切替） | ✅ FOV_IN 検出済み | 推奨（精密タイムコード取得） | 33 |
| 121.0〜129.0s | ZOOM_IN@124s（ズーム切替） | ✅ FOV_IN 検出済み | 推奨（精密タイムコード取得） | 33 |
| 246.0〜255.0s | ZOOM_OUT@249s（望遠→ワイド） | ⚠️ STATIC（未検出） | **必須** | 37 |
| 253.0〜263.0s | BLACKOUT+WHITEOUT@256s | ⚠️ EDGE_SURGE のみ（間接検出） | **必須**（直接検出のため） | 41 |

**合計**: 約 177 フレーム追加（元の 97 フレームの約 1.8 倍）

### extract_frames_targeted.py への Camera Analyzer トリガー対応追加

現在の `extract_frames_targeted.py` は `frame_delta.csv` をトリガーソースとして動作する。
Camera Analyzer 出力をトリガーとして使うには、以下の引数・モードを追加実装する：

```
extract_frames_targeted.py \
  --video <source_video> \
  --trigger-source camera \                    ← 新モード
  --camera-events-csv <camera_events.csv> \    ← 新引数
  --camera-trigger-events FOV_IN,FOV_OUT,EDGE_SURGE,COMBINED \  ← 新引数
  --existing-frames-dir <adaptive_frames_dir> \
  --interval 0.25 \
  --window 5 \
  --execute
```

OR、手動区間指定モードでの即時対応：

```
extract_frames_targeted.py \
  --video <source_video> \
  --manual-windows "22:30,49:57,121:129,246:255,253:263" \  ← 新引数
  --existing-frames-dir <adaptive_frames_dir> \
  --interval 0.25 \
  --execute
```

どちらの実装も `extract_frames_targeted.py` へのトリガーソース拡張として行う。
Motion Intelligence v4 の実装前に完成させる。

### Camera Analyzer 入力モードの仕様

```
scripts/camera_analyzer.py の --input-mode（将来追加予定）:
  --input-mode coarse    : 3秒間隔フレーム（デフォルト）。候補区間の特定用。
  --input-mode targeted  : 0.25〜0.5秒間隔フレーム。精密検出用。
  --input-mode auto      : フレーム間隔を自動判定（metadata.json を参照）。
```

現時点では `--input-mode` フラグは未実装。
Camera Analyzer は任意の間隔フレームで動作するが、
出力の `camera_notes` に入力サンプリング間隔を記録することで
後段 Agent がデータの信頼性を評価できるようにする（次バージョンで実装）。

---

## 4. データフロー

```
Raw Video（MP4）
          │
          ├─── [抽出A] extract_frames_adaptive.py
          │      間隔: 3秒（固定）
          │      出力: data/adaptive_frames/<date>/<slug>/
          │
          │            ↓
          │    [1] Scene Analyzer
          │        scene_frames.csv
          │
          │    [2a] Camera Analyzer（粗パス）
          │         camera_events.csv  ← FOV候補区間を特定
          │
          ├─── [抽出B] extract_frames_targeted.py (Precision Sampler)
          │      間隔: 0.25s（候補区間のみ）
          │      トリガー: camera_events.csv の FOV_IN/FOV_OUT/EDGE_SURGE
          │              または --manual-windows 直接指定
          │      出力: data/adaptive_frames/<date>/<slug>_targeted/
          │
          │            ↓
          │    [2b] Camera Analyzer（精密パス）
          │         camera_events_targeted.csv
          │
          ├─── [抽出C] ※フレーム抽出なし（動画から直接読込）
          │
          │    [2c] Micro Frame Analyzer（超精密パス）
          │         micro_frame_events.csv / event_candidates.jsonl
          │         ↑ BLACKOUT@255.433s タイムコード確定（1/30秒精度）
          │         ↑ 彩度スパイク(SENSOR_SWITCH)・BLOOM も同時検出
          │
 [2a]+[2b]+[2c] ─── Camera 統合出力 ──────────────────────────┐
     camera_events_merged.csv                                  │
          │                                                    │
          ▼                                                    │
 [3] Shadow/Illumination Analyzer                             │
     shadow_frames.csv ◄──── scene_frames.csv                 │
          │                                                    │
          ▼                                                    ▼
 [4] Motion Intelligence v4 ◄───────────────────────────────────
     motion_events.csv（カメラ補正済み）
          │
          ▼
 [5] Object Tracker
     track_events.csv
          │
          ▼
 [6] Observation Generator
     ai_observation_report_v4_<date>.md
```

---

## 5. 出力ディレクトリ構造

```
data/adaptive_frames/<date>/<slug>/          ← 3秒間隔（粗パス用）
data/adaptive_frames/<date>/<slug>_targeted/ ← 0.25s間隔（精密パス用・候補区間のみ）
                                               ※超精密パスはフレーム書き出しなし（動画直読）

data/micro_frame_runs/<date>/<slug>/<start>s_<end>s/  ← Micro Pass 出力（区間ごと）
├── micro_frame_events.csv        ← per-frame メトリクス + 検出イベント
├── micro_frame_summary.md        ← 人間可読サマリー
├── event_candidates.jsonl        ← 1行1候補（MI v4 / OT 前段入力）
└── [frames/]                     ← --keep-frames 指定時のみ

data/media_inspector_runs/<date>/<slug>/
├── scene_analysis/
│   ├── scene_frames.csv          ← 3秒フレーム対象
│   ├── scene_summary.md
│   └── scene_meta.json
├── camera_analysis/
│   ├── camera_events.csv         ← 粗パス (3秒フレーム)
│   ├── camera_events_targeted.csv ← 精密パス (0.25sフレーム)
│   ├── camera_summary.md
│   └── camera_meta.json
├── shadow_analysis/
│   ├── shadow_frames.csv
│   └── shadow_summary.md
├── motion_events/
│   ├── motion_events.csv         ← カメラ補正済み
│   ├── track_events.csv
│   └── motion_summary.md
├── track_events/
│   ├── track_events.csv
│   └── track_summary.md
└── observation_report/
    └── ai_observation_report_v4_<date>.md
```

v3 との出力先変更:
- v3: `data/motion_intelligence_runs/<date>/<slug>/v3/`
- v4: `data/media_inspector_runs/<date>/<slug>/`（全Agent統合）

---

## 6. v3 との比較

| 項目 | v3 | v4 |
|------|----|----|
| エンジン構成 | 単一スクリプト | 6専門Agent |
| 背景分類 | なし（目視に依存）| Scene Analyzer（ルールベース）|
| カメラ運動補正 | 位相相関のみ（内部）| Camera Analyzer → MI v4 補正量入力 |
| カメラ事象検出 | なし | Camera Analyzer（zoom/blackout/whiteout/fov）|
| 陰影解析 | なし | Shadow/Illumination Analyzer |
| 対象物追跡 | MI v3内のtrack_registry | Object Tracker（独立Agent）|
| レポート生成 | build_summary()（統計のみ）| Observation Generator（ルール付き統合）|
| 方向表現制御 | なし | Observation Generatorが「位置変化」表現に変換 |
| 不確実性表現 | なし | 全Agentが confidence + notes を付与 |

---

## 7. 実装優先順位

| 優先度 | Agent | 理由 |
|--------|-------|------|
| 1 | **Scene Analyzer** | PR062最大の誤認（背景）を解決。他の全Agentの前提 |
| 2 | **Camera Analyzer** | 方向誤推定・zoom/blackout未検出を解決 |
| 3 | **Motion Intelligence v4** | Camera Analyzer補正を適用した改良版。v3の上位互換 |
| 4 | **Observation Generator（ルール更新）** | Scene/Camera出力を受け取れるよう拡張 |
| 5 | **Object Tracker** | v3 track_registryの独立Agent化 |
| 6 | **Shadow/Illumination Analyzer** | 最も専門的。Phase 2 での実装を推奨 |

---

## 8. PR062 再検証手順（v4実装後）

```
Step 1: Scene Analyzer を PR062 adaptive_frames に適用（完了済み）
  python3 scripts/scene_analyzer.py \
    --frames-dir data/adaptive_frames/20260628/DOW-UAP-PR062_.../ \
    --output-dir data/media_inspector_runs/20260628/DOW-UAP-PR062_.../scene_analysis/ \
    --execute
  ✅ 完了: ground_surface 62.9%, sensor_mode=color 確認済み

Step 2a: Camera Analyzer 粗パス（完了済み）
  python3 scripts/camera_analyzer.py \
    --frames-dir data/adaptive_frames/20260628/DOW-UAP-PR062_.../ \
    --output-dir .../camera_analysis/ \
    --execute
  ✅ 完了: FOV_IN@52s・FOV_IN@124s・EDGE_SURGE@258s 検出。25s/249s は未検出。

Step 2b: 精密フレーム抽出（要実施）
  python3 scripts/extract_frames_targeted.py \
    --video raw_media/video/DOW-UAP-PR062_...mp4 \
    --manual-windows "22:30,49:57,121:129,246:255,253:263" \
    --existing-frames-dir data/adaptive_frames/20260628/DOW-UAP-PR062_.../ \
    --interval 0.25 \
    --execute
  出力先: data/adaptive_frames/20260628/DOW-UAP-PR062_..._targeted/
  期待結果: 候補5区間に合計約177フレームを0.25s間隔で追加

Step 2c: Camera Analyzer 精密パス（Step 2b 完了後）
  python3 scripts/camera_analyzer.py \
    --frames-dir data/adaptive_frames/20260628/DOW-UAP-PR062_..._targeted/ \
    --output-dir .../camera_analysis/ \
    --execute
  出力: camera_events_targeted.csv
  期待結果: 25s=FOV切替 / 249s=ZOOM_OUT / 256s=BLACKOUT+WHITEOUT を精密検出

Step 3: Motion Intelligence v4 を適用（Camera補正あり・未実装）
  python3 scripts/motion_intelligence_v4.py \
    --frames-dir data/adaptive_frames/20260628/DOW-UAP-PR062_.../ \
    --camera-csv .../camera_analysis/camera_events.csv \
    --scene-csv .../scene_analysis/scene_frames.csv \
    --output-dir .../motion_events/ \
    --execute
  期待結果: track_2 の方向がカメラ補正後に再判定される

Step 4: Object Tracker を適用（未実装）
  期待結果: FRAMEOUT・MASKED_ENTRY 事象が適切に記録される

Step 5: Shadow Analyzer を適用（未実装・Phase 2）
  期待結果: 69-72s の terrain_shadow_transition=true を返す

Step 6: Observation Generator を実行（未実装）
  期待結果: 背景「地表面」・方向「画面上の位置変化」・不確実性明記のレポート
```

---

## 9. バージョン履歴

| バージョン | 日付 | 主な変更 |
|-----------|------|---------|
| v1 | 2026-06-26 | 初版。VLM評価・Ground Truth設計 |
| v2 | 2026-06-27 | AI Observation Report型へ移行。source-video-first確立 |
| v3 | 2026-06-28 | Motion Intelligence v3 を主役に昇格 |
| v4.0 | 2026-06-28 | 6専門Agentへ分解。背景/カメラ/陰影の独立解析を追加 |
| v4.1 | 2026-06-29 | サンプリング戦略追加。Camera Analyzer入力前提・2層サンプリングフロー・PR062精密抽出区間を設計 |
| **v4.2** | **2026-06-29** | **Micro Frame Analyzer 追加。3層サンプリング構造へ拡張。PR062@255.433s でブラックアウト直接検出（1/30秒精度）** |
