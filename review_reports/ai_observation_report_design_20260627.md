# AI Observation Report 設計仕様

- 作成日: 2026-06-27
- 対応アーキテクチャ: docs/media_inspector_architecture_v2.md
- ステータス: 設計確定・実装待ち

---

## 1. 目的

Adaptive Frame / Frame Delta / Targeted Frame の機械分析結果を統合し、
AIが映像セグメントごとに観察・仮説・リスクを事前に整理したレポートを自動生成する。

人間はソース映像を確認し、「OK / PARTIAL / WRONG / UNKNOWN」を返すだけでよい。

---

## 2. ファイル命名規則

```
review_reports/<source_id>_ai_observation_report_<YYYYMMDD>.md
```

例：
```
review_reports/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_ai_observation_report_20260627.md
```

---

## 3. レポート構造（Markdown形式）

```markdown
# AI Observation Report: <source_id>

## メタデータ
- source_id:
- article_id:
- source_video_path:
- duration: Xs（mm:ss）
- run_date:
- pipeline_steps:
  - adaptive_frames: data/adaptive_frames/<date>/<slug>/（N枚・X秒間隔）
  - delta_analysis: data/frame_delta_runs/<date>/<slug>/summary.md
  - targeted_frames: data/adaptive_frames/<date>/<slug>_targeted/（N枚・4区間）
  - vlm_output: （未実施 / data/vlm_runs/<date>/<slug>/）

## 観察サマリー
（1〜3文。映像全体で何が起きているかを端的に記述）

## 重要セグメント

### セグメント <ID>: <start>s（<mm:ss>）〜<end>s（<mm:ss>）
**概要タグ:** APPEAR / DISAPPEAR / CUT / OBJECT_MOVE / STATIC / EXPOSURE_CHANGE など

**AI観察:**
（このセグメントで何が起きているとAIが判断するかを記述。断定しない表現で）

**確信度:** high / medium / low / unknown

**根拠:**
- Adaptive frame: （該当フレーム名・内容）
- Delta result: （イベント種別・bc値・mean_diff値）
- Targeted frame: （補完フレームの観察）
- VLM output: （VLMの記述・または「未実施」）
- Filename metadata: （ファイル名・メタデータ由来の情報）

**リスクフラグ:**
- ui_misidentification: none / low / medium / high（理由）
- trimming_effect: none / low / medium / high（理由）
- blowup_effect: none / low / medium / high（理由）
- speed_change: none / low / medium / high（理由）
- frameout_misidentification: none / low / medium / high（理由）
- exposure_change: none / low / medium / high（理由）
- compression_artifact: none / low / medium / high（理由）

**人間確認:**
- [ ] OK — AIの観察は正しい
- [ ] PARTIAL — 一部修正が必要（以下に記述）
- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

## note_draft 反映候補

（各セグメントの確認済み観察をどの表現で note_draft に反映するかの案）

| セグメント | note_draft 反映案 | 確信度 | 人間確認後に反映 |
|-----------|-----------------|--------|----------------|
| | | | |

## 代表フレーム候補

| フレーム | タイムスタンプ | 選定理由 | 優先度 |
|---------|-------------|---------|--------|
| | | | |

**→ 代表フレーム確定:** （人間確認後に記入）
```

---

## 4. セグメント分割ルール

Delta 分析結果を基に以下の優先度でセグメントを設定する：

| 優先度 | 条件 | セグメント数の目安 |
|--------|------|-----------------|
| 必須 | CUT（mean_diff ≥ 30）・APPEAR（bc ≥ 500）・DISAPPEAR（bc ≥ 500）が集中する区間 | 各クラスタ1セグメント |
| 推奨 | REVIEW_REQUIRED が3件以上連続する区間 | 1セグメント |
| オプション | STATIC が長期間続く区間（≥ 10ペア = ≥ 30秒） | 1セグメント（「静止区間」として括る） |
| 除外 | OBJECT_MOVE のみでbc値が低い区間 | セグメント化不要 |

**セグメント数の上限目安:** 1映像あたり 5〜8セグメント（多すぎると人間確認負荷が増える）

---

## 5. 確信度の判定ロジック

```
if (delta_result == APPEAR または DISAPPEAR) and (bc >= 1000):
    if targeted_frame で目視可能な変化あり:
        confidence = "high"
    else:
        confidence = "medium"

elif delta_result == CUT and mean_diff >= 50:
    confidence = "medium"（CUTは自然な変化でも発生しうる）

elif delta_result == REVIEW_REQUIRED:
    confidence = "low"（mean_diffが低くpos_deltaが大きい→不確実性高）

elif delta_result == STATIC and 連続10ペア以上:
    confidence = "medium"（映像が静止または変化なしは確実・内容が不明なだけ）

else:
    confidence = "unknown"
```

---

## 6. リスクフラグの自動判定ルール

| フラグ | 自動判定条件 |
|--------|------------|
| `exposure_change` | CUT の直前または直後に APPEAR/DISAPPEAR（bc変化大）が発生する場合 |
| `frameout_misidentification` | DISAPPEAR（bc→0）かつ CUT が直後に発生する場合 |
| `ui_misidentification` | VLM が「crosshair」「target」「marker」を UAP として記述した場合 |
| `blowup_effect` | STATIC が長期間続いた後に解像度が著しく低下するフレームが検出された場合 |
| `speed_change` | CUT の mean_diff が段階的に変化する連続パターン（PR053型）|

---

## 7. スクリプト仕様：`scripts/generate_ai_observation_report.py`

### 概要

Adaptive / Delta / Targeted の処理結果を読み込み、AI Observation Report の Markdown を生成するスクリプト。

### 入力

```
--video          : ソース映像ファイルパス
--article-id     : 例 R02-052
--source-id      : 例 DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2
--adaptive-dir   : data/adaptive_frames/<date>/<slug>/
--delta-csv      : data/frame_delta_runs/<date>/<slug>/frame_delta.csv
--delta-summary  : data/frame_delta_runs/<date>/<slug>/summary.md
--targeted-dir   : data/adaptive_frames/<date>/<slug>_targeted/（省略可）
--vlm-output     : data/vlm_runs/<date>/<slug>/（省略可）
--run-date       : 出力ファイルの日付キー（デフォルト: 今日）
--output-dir     : 出力先ディレクトリ（デフォルト: review_reports/）
--dry-run        : 生成内容のプレビューのみ（ファイル生成なし）
--execute        : 実際にファイルを生成する
```

### 処理フロー

```python
# 1. メタデータ読み込み
meta = load_adaptive_metadata(adaptive_dir + "/metadata.json")

# 2. Delta CSV 読み込み・セグメント生成
events = load_delta_csv(delta_csv)
segments = cluster_events_to_segments(events, rules=SEGMENT_RULES)

# 3. 各セグメントの観察文生成
for seg in segments:
    seg.ai_observation = generate_observation_text(seg, meta, targeted_dir, vlm_output)
    seg.confidence = determine_confidence(seg)
    seg.risks = detect_risks(seg, events)

# 4. note_draft反映候補生成
draft_candidates = generate_draft_candidates(segments)

# 5. 代表フレーム候補生成
frame_candidates = select_frame_candidates(segments, adaptive_dir, targeted_dir)

# 6. Markdown 出力
output_path = f"review_reports/{source_id}_ai_observation_report_{run_date}.md"
write_markdown(output_path, meta, segments, draft_candidates, frame_candidates)
```

### 出力例（PR060の場合・想定）

```
review_reports/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_ai_observation_report_20260627.md
```

### 依存関係

- Python 3.10+
- pandas（Delta CSV読み込み）
- Pillow（フレームサイズ確認）
- ffprobe（映像メタデータ。subprocess経由）
- 既存: `frame_delta_analyzer.py` の CSV フォーマットに依存

---

## 8. PR059 からの学習（設計反映済み事項）

| PR059 での発見 | 設計への反映 |
|--------------|------------|
| bc=4887（3s）はホワイトアウトによる誤検出 | `exposure_change` リスクフラグを自動判定 |
| STATIC 39件は対象物が緩やかに移動していた | STATIC区間を「内容不明な静止区間」としてセグメント化 |
| CUT検出がレンズ切り替えだった | `trimming_effect` リスクフラグを追加 |
| 219s（03:39）の急加速は瞬時に発生 | 急加速をOBJECT_MOVEのpos_delta急増として自動検出 |
| 「2M」サイズ推定UIの発見 | UI要素をVLMで検出→観察文に「センサーUI表示」として記述 |
| 14問の確認質問は負荷が高い | セグメントを5〜8件に絞り、質問型ではなく観察文型に変更 |

---

## 9. 今後の実装優先度

| 優先度 | タスク | 前提条件 |
|--------|--------|---------|
| **高** | `scripts/generate_ai_observation_report.py` の実装 | Delta CSV フォーマット確定済み |
| **高** | PR060〜PR063 で AI Observation Report 試用 | 上記スクリプト完成後 |
| 中 | `scripts/run_vid_pipeline.py`（Adaptive〜Targeted一括実行） | 単体スクリプト安定後 |
| 中 | Ground Truth のセグメント単位記録 CSV 設計 | AI Observation Report 試用後 |
| 低 | Delta summary への mm:ss 併記対応 | 他が安定してから |

---

## 10. 参照ドキュメント

| ドキュメント | 内容 |
|------------|------|
| `docs/media_inspector_architecture_v2.md` | 全体アーキテクチャ・フロー定義 |
| `docs/media_inspector_ground_truth_v1.md` | v1 Ground Truth 仕様（VLM評価フレーム単位・継続使用） |
| `review_reports/unpublished_vid_reanalysis_plan_20260626.md` | 未公開VID処理計画・Pipeline定義 |
| `review_reports/pr059_source_video_review_guide_20260627.md` | PR059確認記録（旧Human Q&A型の最終例） |
