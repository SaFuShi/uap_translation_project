# Commit Plan: Media Inspector v4 Agents

- 作成日: 2026-06-29
- 対象: Scene Analyzer / Camera Analyzer / Precision Sampler 関連の未 commit 変更
- 前提: Micro Frame Analyzer は 314be92 で commit 済み
- git add . 禁止 / ファイル個別指定で実施

---

## 1. 現状サマリー

```
git status --short の分類:

 M  docs/media_inspector_architecture_v2.md    ← 変更済み（tracked）
 M  scripts/extract_frames_targeted.py          ← 変更済み（tracked）
??  scripts/scene_analyzer.py                   ← 新規（未追跡）
??  scripts/camera_analyzer.py                  ← 新規（未追跡）
??  review_reports/media_inspector_v4_design_20260628.md
??  review_reports/media_inspector_v3_validation_DOW-UAP-PR062_...md
??  review_reports/DOW-UAP-PR062_..._ai_observation_report_v3_20260628.md
??  data/adaptive_frames/         ← PNG 画像含む（353MB）
??  data/frame_delta_runs/        ← 旧ツール出力
??  data/ground_truth/            ← 16KB の軽量 CSV/MD
??  data/media_inspector_runs/    ← 116KB の軽量 CSV/MD/JSON
??  data/micro_frame_runs/        ← PNG 31MB + CSV/MD/JSONL 軽量
??  data/motion_intelligence_runs/ ← 旧ツール出力（119MB）
??  data/vlm_runs/                ← 旧ツール出力
```

---

## 2. ファイル分類

### ✅ Commit 対象候補

#### Commit A — スクリプト・設計書（3 + 2 = 5 ファイル）

| ファイル | 種別 | 状態 | 理由 |
|---------|------|------|------|
| `scripts/scene_analyzer.py` | 新規 | `??` | Scene Analyzer v1（980行）実装完了・py_compile OK |
| `scripts/camera_analyzer.py` | 新規 | `??` | Camera Analyzer v1（721行）実装完了・py_compile OK |
| `scripts/extract_frames_targeted.py` | 変更 | ` M` | Precision Sampler v1（689行）として全面再設計。後方互換あり |
| `docs/media_inspector_architecture_v2.md` | 変更 | ` M` | v3 フロー（§11）と MI v3 事例を追記。v2 doc の恒久拡張として妥当 |
| `review_reports/media_inspector_v4_design_20260628.md` | 新規 | `??` | v4 設計経緯の記録。恒久参照文書 |

推奨 commit message:
```
Add Scene Analyzer, Camera Analyzer, and Precision Sampler scripts
```

#### Commit B — PR062 解析結果・レポート（3 + 2 + 9 = 14 ファイル）

**review_reports（3件）:**

| ファイル | 理由 |
|---------|------|
| `review_reports/media_inspector_v3_validation_DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_20260628.md` | v3 検証レポート。コード変更の文脈証跡 |
| `review_reports/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_ai_observation_report_v3_20260628.md` | AI 観察レポート。Ground Truth 作成の根拠 |

**data/ground_truth/（2件 / 16KB）:**

| ファイル | 理由 |
|---------|------|
| `data/ground_truth/segments/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_segments_gt.csv` | 手動確認済み Ground Truth。再現不可の人的判断を記録 |
| `data/ground_truth/segments/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_segments_gt.md` | 同上（MD 版） |

**data/media_inspector_runs/（9件 / 116KB）:**

| ディレクトリ | ファイル | 理由 |
|------------|---------|------|
| `scene_analysis/` | `scene_frames.csv`, `scene_meta.json`, `scene_summary.md` | Scene Analyzer v1 の PR062 実行結果。スクリプト改修時の回帰検証に使用 |
| `camera_analysis/` | `camera_events.csv`, `camera_meta.json`, `camera_summary.md` | Camera Analyzer v1 粗パス（3s）結果 |
| `camera_analysis_targeted/` | `camera_events.csv`, `camera_meta.json`, `camera_summary.md` | Camera Analyzer v1 精密パス（0.25s）結果 |

**data/micro_frame_runs/（3件 / 軽量部分のみ）:**

| ファイル | 理由 |
|---------|------|
| `data/micro_frame_runs/20260629/DOW-UAP-PR062_.../255.0s_257.0s/micro_frame_events.csv` | Micro Frame Analyzer 実行結果（60行） |
| `data/micro_frame_runs/20260629/DOW-UAP-PR062_.../255.0s_257.0s/micro_frame_summary.md` | サマリー |
| `data/micro_frame_runs/20260629/DOW-UAP-PR062_.../255.0s_257.0s/event_candidates.jsonl` | イベント候補（9行）。MI v4 前段入力として再利用可能 |

推奨 commit message:
```
Add PR062 Media Inspector v4 analysis results and review reports
```

---

### ❌ Commit 除外（PNG 画像・巨大バイナリ）

| パス | サイズ | 理由 |
|-----|--------|------|
| `data/adaptive_frames/20260628/DOW-UAP-PR062_.../ (PNG 97枚)` | 46MB | ffmpeg で再生成可能。git に不向き |
| `data/adaptive_frames/20260628/DOW-UAP-PR062_..._targeted/ (PNG 153枚)` | 84MB | Precision Sampler で再生成可能 |
| `data/micro_frame_runs/.../frames/ (PNG 60枚)` | 31MB | Micro Frame Analyzer で再生成可能 |

**推奨**: `.gitignore` に以下を追加することを検討する（今 commit では対応しない）:
```
data/adaptive_frames/**/*.png
data/micro_frame_runs/**/frames/
```

---

### ⚠️ 要確認（今回の commit スコープ外・別バッチ推奨）

| パス | サイズ | 判断理由 |
|-----|--------|---------|
| `data/frame_delta_runs/` | 軽量 CSV/MD | 旧 Frame Delta ツール出力。Media Inspector v4 の直接前身ではなく別バッチで整理すべき |
| `data/motion_intelligence_runs/` | 119MB（CSV/MD のみなら軽量） | MI v1/v2/v3 の全 run 結果。motion_intelligence_vX 採用レポートと合わせて別 commit |
| `data/vlm_runs/phase2_5sample_20260626/` | 軽量 | VLM 評価結果。VLM 関連 commit として別バッチ |
| `data/adaptive_frames/.../metadata.json` | 軽量 | 再生成可能。commit してもよいが今回の scope 外 |
| `data/adaptive_frames/.../_targeted/precision_sampling_log.json` | 軽量 | Precision Sampler 実行ログ。commit してもよいが今回の scope 外 |

---

## 3. 推奨 git add コマンド（実行前に確認すること）

### Commit A

```bash
git add \
  scripts/scene_analyzer.py \
  scripts/camera_analyzer.py \
  scripts/extract_frames_targeted.py \
  docs/media_inspector_architecture_v2.md \
  review_reports/media_inspector_v4_design_20260628.md
```

### Commit B

```bash
git add \
  "review_reports/media_inspector_v3_validation_DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_20260628.md" \
  "review_reports/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_ai_observation_report_v3_20260628.md" \
  "data/ground_truth/segments/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_segments_gt.csv" \
  "data/ground_truth/segments/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1_segments_gt.md" \
  "data/media_inspector_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/scene_analysis/scene_frames.csv" \
  "data/media_inspector_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/scene_analysis/scene_meta.json" \
  "data/media_inspector_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/scene_analysis/scene_summary.md" \
  "data/media_inspector_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/camera_analysis/camera_events.csv" \
  "data/media_inspector_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/camera_analysis/camera_meta.json" \
  "data/media_inspector_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/camera_analysis/camera_summary.md" \
  "data/media_inspector_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/camera_analysis_targeted/camera_events.csv" \
  "data/media_inspector_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/camera_analysis_targeted/camera_meta.json" \
  "data/media_inspector_runs/20260628/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/camera_analysis_targeted/camera_summary.md" \
  "data/micro_frame_runs/20260629/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/255.0s_257.0s/micro_frame_events.csv" \
  "data/micro_frame_runs/20260629/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/255.0s_257.0s/micro_frame_summary.md" \
  "data/micro_frame_runs/20260629/DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1/255.0s_257.0s/event_candidates.jsonl"
```

---

## 4. Commit 後の期待状態

```
git log --oneline -4:

  XXXXXXX Add PR062 Media Inspector v4 analysis results and review reports
  XXXXXXX Add Scene Analyzer, Camera Analyzer, and Precision Sampler scripts
  314be92 Add Micro Frame Analyzer for Media Inspector v4
  0ce0633 Add Motion Intelligence v3 sticky tracking
```

残る `??` は `data/frame_delta_runs/`, `data/motion_intelligence_runs/`, `data/vlm_runs/`, PNG 画像群のみとなり、
Media Inspector v4 関連の整理が完了する。
