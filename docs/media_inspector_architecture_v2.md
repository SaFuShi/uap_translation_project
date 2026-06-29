# Media Inspector Architecture v2

- 作成日: 2026-06-27
- バージョン: v2
- 前バージョン: docs/media_inspector_ground_truth_v1.md（VLM評価中心）
- 変更理由: Human Q&A型レビューから AI Observation Report型レビューへ移行

---

## 1. 設計思想の変更

### v1 の問題点

| 問題 | 詳細 |
|------|------|
| 人間の負荷が高い | PR059で14問以上の確認質問が発生。運用継続困難 |
| 人間を「回答者」として扱う | AIがわからないことを人間に聞く構造 → 逆転すべき |
| 質問設計のコストが高い | AIが質問を生成するより、観察レポートを生成する方が効率的 |
| 静止画フレームが主対象 | UAP映像の特性（不規則移動・加速・フレームアウト）は動画で見ないとわからない |

### v2 の設計思想

```
AIが先に「映像で何が起きているか」を整理する。
人間はソース映像を見ながら、AIの観察が合っているかだけ確認する。
人間は「編集長・査読者」として機能する。差分だけ返せばよい。
```

---

## 2. フロー比較

### v1 フロー（Human Q&A型・廃止）

```
Adaptive Frame Extraction
↓
Frame Delta Analysis
↓
Targeted Frame Extraction
↓
Source Video Review Guide（多数の確認質問）
↓
人間が各質問に個別回答（14問以上）
↓
Ground Truth 記録
↓
note_draft 修正
```

### v2 フロー（AI Observation Report型・現行）

```
Adaptive Frame Extraction          ← 映像の「索引」を作る
↓
Frame Delta Analysis               ← 変化の大きい区間・イベントを機械検出
↓
Targeted Frame Extraction          ← イベント前後の詳細フレームを補完
↓
VLM / ルールベース解析（オプション）← フレームの自動記述（参考値）
↓
AI Observation Report 生成         ← AIが映像観察をセグメント別に整理・仮説化
↓
人間がソース映像を確認              ← QuickTime等でタイムコードを参照しながら通し確認
↓
人間が「OK / PARTIAL / WRONG / UNKNOWN」を返す
↓
Ground Truth 記録                  ← 確認済みセグメントを蓄積
↓
note_draft 修正                    ← 人間確認済みの内容を反映
```

---

## 3. 各コンポーネントの役割（v2）

| コンポーネント | 役割 | 人間の関与 |
|--------------|------|-----------|
| Adaptive Frame | 映像の「索引」。変化の有無を3秒間隔で把握 | なし |
| Frame Delta Analysis | CUT/APPEAR/DISAPPEAR/OBJECT_MOVE/STATIC/REVIEW_REQUIRED を機械検出 | なし |
| Targeted Frame | Delta で検出した重要区間を1秒間隔で補完。**タイムコードガイドとして使用** | なし |
| VLM解析 | フレームの自動記述（オプション）。過検出の傾向あり→参考値として扱う | なし（レビューのみ） |
| **AI Observation Report** | **AIがセグメント別に観察・仮説・リスクを整理した主要レポート** | **査読・修正のみ** |
| ソース映像 | **人間が最終確認する本体**。タイムコードに従って再生確認 | **主要アクション** |
| Ground Truth | 人間確認済みセグメントの蓄積。VLM改善・記事精度向上に活用 | 結果の承認のみ |
| note_draft | 人間確認済みの観察内容を反映した公開用ドラフト | 最終承認 |

---

## 4. AI Observation Report の位置づけ

### 役割

AI Observation Report は、Adaptive/Delta/Targeted の機械分析結果と
VLMおよびルールベース解析を統合して、AIが「映像で何が起きているか」を先に整理したレポート。

人間は映像を見る前にこのレポートを読み、
映像確認後に「合っている / 一部違う / 違う / 不明」とだけ返す。

### 生成タイミング

Targeted Frame Extraction 完了直後。ソース映像の人間確認前。

### 出力先

```
review_reports/<slug>_ai_observation_report_<date>.md
```

### 前バージョンとの関係

v1 の `Source Video Review Guide`（`_source_video_review_guide_*.md`）は廃止。
PR059のガイドファイルは確認済み記録として保持するが、新規生成はしない。

---

## 5. タイムコード表記ルール（全ドキュメント共通）

すべての映像確認用タイムコードは **秒数（mm:ss）** の形式で表記する。

```
【正しい形式】
7s（00:07）
95s（01:35）
219s（03:39）
273〜276s（04:33〜04:36）

【禁止形式】
7s だけ・00:07 だけ・「約7秒」
```

| 対象ドキュメント | 適用 |
|----------------|------|
| AI Observation Report | ✅ 必須 |
| Source Video Review Guide（廃止済み） | 過去ファイルは修正不要 |
| note_draft 内の重要タイムコード | ✅ 必須 |
| 人間確認結果 | ✅ 必須 |
| Ground Truth 記録 | ✅ 必須 |
| Frame Delta summary（機械生成） | ⬜ 将来対応（現状は秒数のみ） |

---

## 6. 確信度（confidence）定義

| 値 | 意味 | 典型的な根拠 |
|----|------|------------|
| `high` | 複数根拠が一致・人間確認済み | Delta + Targeted + VLM が一致、かつ人間が確認 |
| `medium` | 単一根拠または根拠に曖昧さあり | Delta のみ・または Adaptive frame のみ |
| `low` | 推測・間接的根拠のみ | ファイル名メタデータ・類似事例からの類推 |
| `unknown` | 判断不能 | フレームが不鮮明・VLMが過検出・Delta が REVIEW_REQUIRED |

---

## 7. リスクフラグ定義

| フラグ | 意味 | 典型的な発生状況 |
|--------|------|----------------|
| `ui_misidentification` | センサーUIをUAP対象物と誤認するリスク | N方位マーカー・クロスヘア・コーナーマーク |
| `trimming_effect` | 画角トリミングによる対象物の見かけの変化 | 望遠→広角への切り替え・ズームトリミング |
| `blowup_effect` | ブローアップ（拡大）による解像度低下・見かけサイズ変化 | PR056・PR055で確認済み |
| `speed_change` | 再生速度変更による動きの見かけ変化 | PR053の3段階速度、PR055のslow to 60% |
| `frameout_misidentification` | フレームアウトと輝度消失の区別不能 | DISAPPEAR イベントで頻発 |
| `compression_artifact` | 映像圧縮による偽アーティファクト | H.264の高速移動シーンでのブロックノイズ |
| `exposure_change` | 露出変化（ホワイトアウト）をAPPEAR/DISAPPEARと誤検出 | PR059で7s・95s付近で確認 |

---

## 8. 人間確認の選択肢

各セグメントの AI 観察に対して、人間は以下から選択する：

| 選択肢 | 意味 | 後続アクション |
|--------|------|--------------|
| `OK` | AIの観察は正しい | Ground Truth に確認済みとして記録 |
| `PARTIAL` | 一部正しいが修正が必要 | human_note に差分を記述 → AI が note_draft に反映 |
| `WRONG` | AIの観察は誤っている | human_note に正しい観察を記述 → AI が修正 |
| `UNKNOWN` | 映像からは判断できない | Ground Truth に UNKNOWN として記録。note_draft では「確認できない」表現を維持 |

---

## 9. スクリプト一覧（v2時点）

### 実装済み

| スクリプト | 役割 | 状態 |
|-----------|------|------|
| `scripts/extract_frames_adaptive.py` | Adaptive Frame Extraction | ✅ 動作確認済み |
| `scripts/frame_delta_analyzer.py` | Frame Delta Analysis（`--ts-mode seconds` 必須）| ✅ 動作確認済み |
| `scripts/extract_frames_targeted.py` | Targeted Frame Extraction | ✅ 動作確認済み |
| `scripts/run_vlm_on_adaptive.py` | VLM解析（Qwen2.5-VL-7B）| ✅ 実装済み・オプション |

### 計画中

| スクリプト | 役割 | 優先度 |
|-----------|------|--------|
| `scripts/generate_ai_observation_report.py` | AI Observation Report 自動生成 | **高** |
| `scripts/run_vid_pipeline.py` | Step1〜3を1コマンドで実行 | 中 |

---

## 10. Ground Truth との連携（v1からの継続）

v1 で定義した Ground Truth 構造（`data/ground_truth/`）はv2でも継続使用する。
ただし記録単位が「フレーム単位」から「セグメント単位」に変わる。

```
data/ground_truth/
├── segments/                     ← v2 追加（セグメント単位の確認済み記録）
│   ├── <slug>_segments_gt.csv   ← セグメントごとのOK/PARTIAL/WRONG/UNKNOWN
│   └── <slug>_segments_gt.md    ← 人間メモ付き詳細記録
├── ui_elements/                  ← v1 継続（UIフレームの誤検出サンプル）
├── uap_candidates/               ← v1 継続（UAP候補フレームの確認済みサンプル）
└── negative/                     ← v1 継続（UAP候補なし確認済みフレーム）
```

---

## 11. v3 フロー（Motion Intelligence v3 主軸）

**制定日: 2026-06-28**

### v2 からの変更点

| 要素 | v2（旧） | v3（新） |
|------|---------|---------|
| 主役 | Adaptive Frame Extraction | Motion Intelligence v3 |
| 重要区間の特定 | Frame Delta Analysis（CUT/APPEAR等） | Motion Intelligence v3（track検出・sticky追跡） |
| Adaptive の役割 | 主役（映像索引） | 補助（前処理フレーム供給） |
| Targeted の役割 | Delta イベントを起点に補完 | MI v3 重要区間（track）を補強 |
| 人間確認の起点 | Frame Delta summary → ガイド作成 | MI v3 summary → AI Observation Report |

### v3 正式フロー

```
動画
↓
[1] Adaptive Frame Extraction（3秒間隔・全体索引）
     scripts/extract_frames_adaptive.py --interval 3 --execute
     出力: data/adaptive_frames/<date>/<slug>/
↓
[2] Motion Intelligence v3（重要区間抽出・主役）
     scripts/motion_intelligence_v3.py --mode adaptive --execute
     出力: data/motion_intelligence_runs/<date>/<slug>/v3/
       motion_events.csv  — ペア単位イベント
       track_events.csv   — トラック単位サマリー
       summary.md         — 重要区間・トラック一覧
↓
[3] Targeted Frame Extraction（MI v3 track 区間を1秒間隔補強）
     ffmpeg または extract_frames_targeted.py
     出力: data/motion_intelligence_runs/<date>/<slug>/targeted_frames/
     優先区間: LINEAR_MOTION（高 drift / 高 R²）+ ERRATIC_MOTION + trail_detected
↓
[4] AI Observation Report 生成（AIが映像観察を整理）
     出力: review_reports/<slug>_ai_observation_report_v3_<date>.md
     形式: 5〜8 セグメント・秒数（mm:ss）併記
↓
[5] 人間査読（ソース映像を確認しながら）
     各セグメントに OK / PARTIAL / WRONG / UNKNOWN を返す
↓
[6] Ground Truth 記録
     data/ground_truth/segments/<slug>_segments_gt.csv
↓
[7] note_draft 修正
```

### v3 での Targeted 抽出対象の優先度

| 優先度 | MI v3 イベント | 理由 |
|--------|--------------|------|
| **最高** | LINEAR_MOTION（drift≥10px/s・R²≥0.45） | 高信頼度の追跡対象 |
| **高** | ERRATIC_MOTION（n_pairs≥7） | 不規則運動 = UAP候補の可能性 |
| **高** | trail_detected=True | 細長いクラスタ（軌跡・引き波の痕跡） |
| 中 | POSSIBLE_TARGET_APPEAR（conf≥0.5） | 出現イベント・追跡開始点 |
| 低 | SINGLE_APPEARANCE（conf<0.3） | 確認用のみ・優先度低 |

### v3 Targeted 抽出パラメータ

- 抽出間隔: 1秒（通常）/ 0.1秒（trail付近・高速移動疑い区間）
- バッファ: track 開始3s前〜終了3s後
- ツール: ffmpeg `-ss <start> -to <end> -vf "fps=1"`
- 出力先: `data/motion_intelligence_runs/<date>/<slug>/targeted_frames/`（内蔵SSD）

### v3 初適用事例

| 事例 | 対象 | 日付 | 結果 |
|------|------|------|------|
| PR062 | DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1 | 2026-06-28 | track×8・LINEAR×3・ERRATIC×2・trail×1 |

---

## 12. バージョン履歴

| バージョン | 日付 | 主な変更 |
|-----------|------|---------|
| v1 | 2026-06-26 | Media Inspector 初版。VLM評価とGround Truth設計 |
| v2 | 2026-06-27 | Human Q&A型 → AI Observation Report型へ移行。source-video-first確立 |
| v3 | 2026-06-28 | Motion Intelligence v3 を主役に昇格。Adaptive/Targeted を補助に再定義 |
