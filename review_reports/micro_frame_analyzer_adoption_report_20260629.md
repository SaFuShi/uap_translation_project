# Micro Frame Analyzer 採用レポート

- 作成日: 2026-06-29
- 検証対象: DOW-UAP-PR062（Spherical UAP CALLSIGN 2021-04-12 vid_1）
- 検証区間: 255.0〜257.0s（60フレーム @ 30fps）
- 実装スクリプト: `scripts/micro_frame_analyzer.py`
- 設計書: `docs/media_inspector_v4_architecture.md`（v4.2 §3.5）

> **証跡ファイル**: 日常運用では参照不要。正式仕様は `docs/media_inspector_v4_architecture.md` を参照。

---

## 1. エグゼクティブサマリー

Micro Frame Analyzer は、PR062 の 255.433s において **BLACKOUT を直接検出した**（輝度=1.88、信頼度=0.95）。

0.25秒精密パス（Precision Sampler + Camera Analyzer）ではブラックアウトを `blackout_curr=False` で見逃していた。ブラックアウトの持続時間が **100ms（3フレーム）** であり、0.25秒サンプリング間隔（250ms）より短かったために起きた構造的な見逃しである。

同時に、ブラックアウト中の **彩度スパイク（SENSOR_SWITCH）** および直後の **輝度ピーク（BLOOM）** も検出。これらは 0.25秒パスでは取得不可能なフレーム間遷移情報であり、カメラセンサーの再起動または IR フラッシュの可能性を示唆する。

**判定: Micro Frame Analyzer を Media Inspector v4.2 の第3層（超精密パス）として採用する。**

---

## 2. 実装ファイル

### 2.1 スクリプト

| ファイル | 役割 | 行数 |
|---------|------|------|
| `scripts/micro_frame_analyzer.py` | Micro Frame Analyzer 本体 | 880行 |

**依存ライブラリ**: `numpy`, `Pillow`（既存環境で動作確認済み）、`ffmpeg`（フレーム抽出）

### 2.2 主な関数構成

| 関数 | 役割 |
|------|------|
| `get_video_fps` / `get_video_duration` | ffprobe で映像メタデータ取得 |
| `extract_micro_frames` | ffmpeg で候補区間を全フレーム抽出 |
| `analyze_single_frame` | 1フレームの全メトリクス計算（輝度・エッジ密度・空間周波数・彩度） |
| `analyze_all_frames` | 全フレームを順次解析、前フレームとの差分も計算 |
| `detect_events` | メトリクス列からイベント候補を検出（9種） |
| `attach_events_to_frames` | CSV 出力用にフレームデータへイベントを付与 |
| `load_manual_windows` | `--manual-windows "255:257"` 形式を解析 |
| `load_camera_event_windows` | `camera_events.csv` からトリガー区間を生成 |
| `write_outputs` | 3ファイル（CSV / MD / JSONL）を出力 |

### 2.3 検出対象イベントと閾値（デフォルト・全て CLI 変更可能）

| イベント | 検出条件 | デフォルト閾値 |
|---------|---------|--------------|
| `BLACKOUT` | `brightness_mean < blackout_thresh` | 15.0 |
| `WHITEOUT` | `brightness_mean > whiteout_thresh` | 240.0 |
| `FLASH` | 単フレーム輝度スパイク（前後フレームより `+flash_delta` 以上） | 60.0 |
| `BLOOM` | `bloom_window` フレーム内の局所輝度最大（周辺平均の `bloom_ratio` 倍） | 10フレーム / 1.30倍 |
| `HARD_CUT` | `frame_diff_mean > hard_cut_diff` かつ `hf_ratio` 急変 | 50.0 |
| `FRAME_DROP` | `frame_diff_mean < frame_drop_diff`（完全一致フレーム） | 1.0 |
| `SENSOR_SWITCH` | 彩度変化 `> sensor_sat_delta` | 30.0 |
| `FOV_SWITCH` | `hf_ratio_vs_prev > fov_switch_hf_high` または `< fov_switch_hf_low` | 3.0 / 0.33 |
| `ZOOM_IN` | `hf_self / rolling_avg > zoom_in_hf` | 2.0（rolling 5フレーム） |
| `ZOOM_OUT` | `hf_self / rolling_avg < zoom_out_hf` | 0.50（rolling 5フレーム） |

### 2.4 出力ファイル

```
data/micro_frame_runs/<date>/<source_id>/<start>s_<end>s/
├── micro_frame_events.csv   : per-frame メトリクス + 検出イベント（60行）
├── micro_frame_summary.md   : 人間可読サマリー
├── event_candidates.jsonl   : 1行1イベント候補（機械可読、後段 Agent 入力）
└── [frames/]                : --keep-frames 指定時のみ
```

### 2.5 実行コマンド（PR062 検証時）

```bash
python3 scripts/micro_frame_analyzer.py \
  --video raw_media/video/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1.mp4 \
  --manual-windows "255:257" \
  --source-id DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1 \
  --article-id R02-054 \
  --keep-frames \
  --verbose \
  --execute
```

---

## 3. PR062 255.0〜257.0s 検証結果

### 3.1 検証条件

| 項目 | 値 |
|------|----|
| 映像 | DOW-UAP-PR062 Spherical UAP CALLSIGN 2021-04-12 vid_1 |
| 解析区間 | 255.0〜257.0s（手動指定） |
| fps | 30fps |
| 解析フレーム数 | 60フレーム（2秒 × 30fps） |
| 前パス情報 | 精密パス (0.25s) で EDGE_SURGE@255.5s + COMBINED@256.0s を検出済み |

### 3.2 輝度推移

```
255.0s  →  255.4s  : 輝度 65〜72（通常映像）
255.43s →  255.5s  : 輝度 1.9, 1.7, 1.5  ← BLACKOUT（3フレーム / 100ms）
255.53s             : 輝度 28.9            ← 回復開始、彩度急落（SENSOR_SWITCH）
255.57s             : 輝度 195.0           ← BLOOM（輝度ピーク）
255.6s  →  257.0s  : 輝度 45〜194（不安定、その後 90前後に収束）
```

### 3.3 全検出イベント

| タイムスタンプ | フレーム# | イベント | 信頼度 | 備考 |
|-------------|---------|---------|--------|------|
| 255.300s | f10 | `FRAME_DROP` | 0.90 | diff=0.108（ブラックアウト直前のコマ落ちまたはエンコードアーティファクト） |
| **255.433s** | **f14** | **`BLACKOUT`** | **0.95** | **輝度=1.9（閾値15以下）** |
| **255.433s** | **f14** | **`SENSOR_SWITCH`** | **0.75** | **彩度: 13.9→77.7（+63.8）** |
| 255.467s | f15 | `BLACKOUT` | 0.95 | 輝度=1.7 |
| 255.467s | f15 | `FRAME_DROP` | 0.90 | diff=0.543（ブラックアウト中の静止フレーム） |
| 255.500s | f16 | `BLACKOUT` | 0.95 | 輝度=1.5（3フレーム中最暗） |
| 255.500s | f16 | `FRAME_DROP` | 0.90 | diff=0.564 |
| 255.533s | f17 | `SENSOR_SWITCH` | 0.75 | 彩度: 65.2→19.7（−45.5、回復時の急落） |
| 255.567s | f18 | `BLOOM` | 0.70 | 輝度ピーク=195.0（周辺平均89.4の2.18倍） |

### 3.4 BLACKOUT の詳細

| 指標 | 値 |
|------|----|
| 開始タイムスタンプ | 255.433s |
| 終了タイムスタンプ | 255.500s |
| 持続時間 | **100ms（3フレーム @ 30fps）** |
| 最低輝度 | 1.53（f16） |
| BLACKOUT 中の彩度 | 77.7 → 68.1 → 65.2（いずれも高彩度） |

> **注目**: ブラックアウトフレームの彩度が 65〜78 と高い。完全暗黒（grayscale blackout）ではなく、特定波長成分が残存している。IR センサーの初期化フレームまたは映像エンコードの圧縮アーティファクトの可能性がある。Human review 推奨。

---

## 4. 0.25秒パスで検出できなかった理由

### 4.1 サンプリング間隔と事象持続時間の関係

```
ブラックアウト持続時間: 100ms（255.433s〜255.500s）
0.25秒パスのサンプリング間隔: 250ms

100ms < 250ms
→ 0.25秒間隔では最短でも 1フレームしかサンプリングできず、
  ブラックアウトフレームが「ちょうどサンプリング点に当たらない」可能性が高い。
```

### 4.2 0.25秒パスの実際の検出状況（精密パス結果）

| タイムスタンプ (0.25s点) | Camera Analyzer 判定 | blackout_curr | 輝度 |
|------------------------|---------------------|--------------|------|
| 255.20s | STATIC | False | 75.4 |
| **255.50s** | **EDGE_SURGE** | **False** | **74.5** |
| 255.80s | STATIC | False | 186.2 |

255.50s の点がブラックアウト区間（255.433〜255.500s）の **終端** にほぼ一致しているが、Camera Analyzer の `blackout_curr` フラグが False になっている。これは 0.25s パスのフレームが「回復直前の境界フレーム」を捉えており、輝度が閾値（15）を超えていたためである。

### 4.3 構造的な限界のまとめ

| パス | 間隔 | BLACKOUT 直接検出 | 代替検出 |
|------|------|-----------------|---------|
| 粗パス（3s） | 3000ms | 不可（100ms < 3000ms） | EDGE_SURGE@258s（2.5秒ずれ） |
| 精密パス（0.25s） | 250ms | 不可（100ms < 250ms） | EDGE_SURGE@255.5s + COMBINED@256.0s |
| **超精密パス（Micro）** | **33ms (30fps)** | **✅ 直接検出 @255.433s** | — |

---

## 5. Media Inspector v4.2 としての位置づけ

### 5.1 3層サンプリング構造

```
Layer 1: 粗パス (3s間隔)
  Scene Analyzer + Camera Analyzer
  目的: シーン種別・FOV候補区間の特定
        ↓ camera_event ∈ {EDGE_SURGE, COMBINED} 等をトリガーに
        
Layer 2: 精密パス (0.25s間隔) — Precision Sampler
  Camera Analyzer 再実行
  目的: FOV タイムコードの絞り込み、大型輝度変化の捕捉
        ↓ 0.25s でも blackout_curr=False の区間をトリガーに
        
Layer 3: 超精密パス (全フレーム 30fps) — Micro Frame Analyzer ← 本スクリプト
  目的: 100ms 以下の瞬間的なカメラ/センサーイベントの直接検出
  出力: event_candidates.jsonl（後段 Agent への受け渡し）
```

### 5.2 他の Agent / ツールとの分担

| ツール | 責務 |
|--------|------|
| `extract_frames_targeted.py`（Precision Sampler） | フレーム抽出（3s / 0.25s）。解析は行わない。 |
| `camera_analyzer.py`（Camera Analyzer） | 3s / 0.25s フレームのカメライベント解析 |
| **`micro_frame_analyzer.py`（本スクリプト）** | **候補区間の全フレーム解析（30fps）。フレーム抽出は内部完結。** |

### 5.3 適用条件（いつ Micro Pass を実行するか）

以下のいずれかに該当する区間に対してのみ実行する。全動画への適用は行わない。

1. 精密パスで `EDGE_SURGE` または `COMBINED` が検出された区間
2. 精密パスで `brightness_curr` が 150 以上、または `blackout_curr=False` のまま輝度が急変している区間
3. Ground Truth に BLACKOUT / WHITEOUT / SENSOR_SWITCH が記載されている区間
4. Human review で「映像が一瞬切れた」等の記述がある区間

---

## 6. Camera Analyzer / Observation Report への渡し方

### 6.1 event_candidates.jsonl の形式

各行が 1 イベント候補（機械可読）:

```json
{"timestamp_s": 255.433, "event": "BLACKOUT", "confidence": 0.95,
 "frame_no": 14, "brightness_mean": 1.88, "frame_diff_mean": 70.306,
 "hf_ratio_vs_prev": 0.0, "color_saturation": 77.68,
 "notes": "平均輝度=1.9 (閾値=15.0)"}
```

**必須フィールド**: `timestamp_s`, `event`, `confidence`, `frame_no`, `brightness_mean`, `frame_diff_mean`, `hf_ratio_vs_prev`, `color_saturation`, `notes`

### 6.2 Camera Analyzer 統合への組み込み

精密パスの `camera_events_targeted.csv` と Micro Pass の `event_candidates.jsonl` を統合し、`camera_events_merged.csv` を生成する。統合ルールは以下の通り:

| 優先度 | ソース | 対象イベント | 理由 |
|--------|--------|------------|------|
| 最高 | Micro Pass JSONL | BLACKOUT / WHITEOUT | フレーム単位の直接検出。最も精度が高い |
| 高 | Micro Pass JSONL | SENSOR_SWITCH / FRAME_DROP / BLOOM | サブフレーム精度の事象 |
| 中 | 精密パス CSV | EDGE_SURGE / COMBINED | 0.25s精度。Micro Passで確定される前の候補 |
| 低 | 粗パス CSV | FOV_IN / FOV_OUT | 3秒精度。区間の絞り込みに使用 |

> **統合スクリプトは未実装**。次バージョン（v4.3予定）で `camera_events_merge.py` として実装する。

### 6.3 Motion Intelligence v4 への渡し方

Motion Intelligence v4 は `camera_events_merged.csv` を前段入力として受け取る。

Micro Pass の BLACKOUT / WHITEOUT イベントが検出された区間では:
- 当該フレームペアを **`SKIP`（解析対象外）** とする
- 理由: ブラックアウト前後のフレームはカメラ位置が不連続であり、位相相関や変位推定が無効になる

具体的なフィールドマッピング:

```python
# motion_intelligence_v4.py が参照する camera_events_merged.csv の想定フィールド
{
    "timestamp_s":     255.433,
    "camera_event":    "BLACKOUT",       # 最高優先ソース: micro_frame
    "source":          "micro_frame",    # どのパスで検出されたか
    "confidence":      0.95,
    "skip_motion":     True,             # MI v4 が当該ペアをスキップする
    "skip_reason":     "BLACKOUT: motion estimation invalid",
}
```

### 6.4 Observation Report（最終レポート）への渡し方

Observation Generator は `event_candidates.jsonl` を直接参照し、以下のセクションに反映する:

**カメラ・映像状態セクション（例）**:

```markdown
## カメラ・映像状態

| 時刻 | イベント | 信頼度 | 解釈 |
|------|---------|--------|------|
| 255.433s | BLACKOUT (100ms) | 0.95 | 映像信号が瞬断。原因不明（センサーリセットまたはエンコードアーティファクトの可能性）|
| 255.433s | SENSOR_SWITCH | 0.75 | ブラックアウト中に高彩度フレーム（sat=77.7）。IR 初期化の可能性 |
| 255.567s | BLOOM | 0.70 | ブラックアウト直後に輝度ピーク（195/255）。ホワイトバランスの再初期化の可能性 |
```

---

## 7. 未解決事項・次バージョンへの課題

| 課題 | 詳細 | 優先度 |
|------|------|--------|
| SENSOR_SWITCH の彩度スパイク原因特定 | ブラックアウト中に sat=77.7 になる物理的原因が不明。IR フレーム / Bayer パターンの露出か要調査 | 高 |
| camera_events_merge.py の実装 | 粗パス・精密パス・Micro Pass の統合ツール（v4.3 課題） | 高 |
| WHITEOUT 閾値の調整 | PR062 の BLOOM は輝度=195（閾値 240 未満）。別動画では WHITEOUT 閾値を下げる必要がある可能性 | 中 |
| FRAME_DROP の誤検出評価 | 255.467s・255.500s の FRAME_DROP はブラックアウト中の「輝度が低い=差分が小さい」ことによる擬似検出の可能性 | 中 |
| Motion Intelligence v4 実装 | Micro Pass の `event_candidates.jsonl` を前段入力として受け取る実装 | 高 |

---

## 付録: 出力ファイルパス（PR062 検証）

```
data/micro_frame_runs/20260629/
  DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/
    255.0s_257.0s/
      micro_frame_events.csv     (60行: per-frame メトリクス)
      micro_frame_summary.md     (サマリー)
      event_candidates.jsonl     (9件: BLACKOUT×3, SENSOR_SWITCH×2, FRAME_DROP×3, BLOOM×1)
      frames/                    (60フレーム PNG: --keep-frames 指定で保存)
```
