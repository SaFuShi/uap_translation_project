# Commit 計画書 — Release03 Work Cache 移行前 整理 commit

- 作成日: 2026-06-28
- 目的: Phase 1（git clone）の前に未コミット成果物を安全にコミットする
- ステータス: 計画確定 / git add 未実行
- 制約: `git add .` 禁止 / source_registry.csv 除外 / uap-csv-cache.csv 除外 / workflow.db 除外

---

## 1. commit 対象一覧

### GROUP A: 本日作成の設計書（指示明示・確定）

```
git add docs/release03_work_cache_layer.md
git add docs/motion_intelligence_engine_v3.md
git add review_reports/release03_work_cache_migration_plan_20260628.md
git add review_reports/release03_work_cache_phase0_check_20260628.md
git add review_reports/motion_intelligence_v3_design_20260627.md
```

| ファイル | 種別 | 理由 |
|---------|------|------|
| `docs/release03_work_cache_layer.md` | 設計書（本日）| 移行設計 |
| `docs/motion_intelligence_engine_v3.md` | 設計書（本日再作成）| v3 設計 |
| `review_reports/release03_work_cache_migration_plan_20260628.md` | レポート（本日）| 移行計画 |
| `review_reports/release03_work_cache_phase0_check_20260628.md` | レポート（本日）| Phase 0 確認 |
| `review_reports/motion_intelligence_v3_design_20260627.md` | レポート（本日再作成）| v3 設計レビュー |

---

### GROUP B: 設計書・スクリプト（未追跡・確定）

```
git add docs/motion_intelligence_engine_v1.md
git add docs/motion_intelligence_engine_v2.md
git add docs/release02_article_template_v1.md
git add scripts/extract_frames_targeted.py
git add scripts/frame_delta_analyzer.py
git add scripts/motion_intelligence_v1.py
git add scripts/motion_intelligence_v2.py
git add scripts/update_release02_draft_ids.py
git add scripts/publish_done.py
```

| ファイル | 種別 | 理由 |
|---------|------|------|
| `docs/motion_intelligence_engine_v1.md` | 設計書（過去作成）| git 管理すべき |
| `docs/motion_intelligence_engine_v2.md` | 設計書（過去作成）| git 管理すべき |
| `docs/release02_article_template_v1.md` | テンプレート（過去作成）| git 管理すべき |
| `scripts/extract_frames_targeted.py` | 新スクリプト | adaptive frame 抽出 |
| `scripts/frame_delta_analyzer.py` | 新スクリプト | frame delta 解析 |
| `scripts/motion_intelligence_v1.py` | 新スクリプト | motion intel v1 |
| `scripts/motion_intelligence_v2.py` | 新スクリプト | motion intel v2 |
| `scripts/update_release02_draft_ids.py` | 新スクリプト | draft ID 更新 |
| `scripts/publish_done.py` | M: スクリプト更新 | 公開後処理 |

---

### GROUP C: metadata（修正トラックファイル・部分）

```
git add metadata/files_catalog.csv
```

| ファイル | 種別 | 理由 |
|---------|------|------|
| `metadata/files_catalog.csv` | M: カタログ更新 | Release02 追記分 |

> ⚠️ `metadata/uap-csv-cache.csv` は**除外**（.gitignore 対象・war.gov 生キャッシュ）

---

### GROUP D: published_articles/（公開済みアーカイブ・30件・確定）

```
git add published_articles/
```

30件すべて確定（すべて公開済み記事の保存版、2026-06-25日付）:

| 範囲 | 件数 |
|------|------|
| DOW-UAP-PR026〜PR049（Unresolved UAP Reports）| 24件 |
| FBI-UAP-PR001〜PR006（FBI 映像シリーズ）| 6件 |

---

### GROUP E: logs/notebooklm/（公開ログ・30件・確定）

```
git add logs/notebooklm/
```

30件すべて確定（すべて公開後の NotebookLM ログ、2026-06-25〜26日付）:

| ファイル日付 | 対象 | 件数 |
|------------|------|------|
| 2026-06-25 | DOW-UAP-PR026〜049、FBI-PR001〜006 | 29件 |
| 2026-06-26 | DOW-UAP-PR053 | 1件 |

---

### GROUP F: review_reports/（設計レポート・Codex 監査・確定）

```
git add review_reports/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_ai_observation_report_20260627.md
git add review_reports/apply_article_template_dry_run_20260624.md
git add review_reports/apply_article_template_v2_dry_run_20260625.md
git add review_reports/batch_final_report_20260620_PR071-PR099.md
git add review_reports/batch_status_20260620_release02_vid_batch.md
git add review_reports/commit_plan_vs_staged_diff_20260626.md
git add review_reports/frame_interval_validation_plan.md
git add review_reports/git_audit_20260618_pending_commits.md
git add review_reports/local_llm_cost_reduction_plan.md
git add review_reports/motion_intelligence_v1_design_20260627.md
git add review_reports/motion_intelligence_v2_design_20260627.md
git add review_reports/pr054_adaptive_delta_reanalysis_plan_20260626.md
git add review_reports/pr055_adaptive_reanalysis_report_20260626.md
git add review_reports/project_asset_audit.md
git add review_reports/ready_to_publish_plan_20260620_PR071-PR099.md
git add review_reports/release02_article_unit_policy_v3.md
git add review_reports/release02_coverage_audit_20260620.md
git add review_reports/release02_draft_id_update_dry_run.md
git add review_reports/release02_gap_closure_plan.md
git add review_reports/release02_hold_material_reassessment.md
git add review_reports/release02_note_publish_workflow.md
git add review_reports/release02_numbering_plan.md
git add review_reports/release02_prebatch_fix_report.md
git add review_reports/release02_publish_queue_top5.md
git add review_reports/release02_ready_to_publish_master_plan.md
git add review_reports/release02_vid_publish_queue_dry_run.md
git add review_reports/release02_video_quality_pause_plan.md
git add review_reports/rule_candidates_20260618_CIA-UAP-D001_intelligence_information_report_ussr_1973.md
git add review_reports/rule_candidates_20260618_DOW-UAP-D077_Unresolved-Case-Analysis-Update.md
git add review_reports/rule_candidates_20260618_ODNI-UAP-D001_usper_narrative_senior_usic.md
git add review_reports/rule_candidates_20260619_DOW-UAP-D079.md
git add review_reports/rule_candidates_20260619_DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22.md
git add review_reports/rule_candidates_20260619_DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron.md
git add review_reports/rule_candidates_20260621_DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission.md
git add review_reports/template_check_20260624.md
git add review_reports/template_check_20260624_final.md
git add review_reports/template_check_20260624_post_apply.md
git add review_reports/template_check_20260624_post_apply2.md
git add review_reports/template_check_after_apply_20260624.md
git add review_reports/template_consistency_v2_20260625.md
git add "review_reports/codex_audit_20260530_release02_intro.md"
git add "review_reports/codex_audit_20260531_ODNI-UAP-D001.md"
git add "review_reports/codex_audit_20260531_ai_summary_DOW-UAP-D017_general_correspondence_sandia_note_version.md"
git add "review_reports/codex_audit_20260602_ai_summary_western_us_event_slides_20260508_note_version.md"
git add "review_reports/codex_audit_20260613_DOW-UAP-PR050_4_UAP_Formation_Iran.md"
git add "review_reports/codex_audit_20260613_DOW-UAP-PR050_4_UAP_Formation_Iran_iter2.md"
git add "review_reports/codex_audit_20260614_DOW-UAP-PR051_Syrian_UAP_instant_acceleration.md"
git add "review_reports/codex_audit_20260614_DOW-UAP-PR051_Syrian_UAP_instant_acceleration_iter2.md"
git add "review_reports/codex_audit_20260618_DOW-UAP-D077_Unresolved-Case-Analysis-Update.md"
git add "review_reports/codex_audit_20260618_DOW-UAP-D077_Unresolved-Case-Analysis-Update_iter2.md"
git add "review_reports/codex_audit_20260619_DOW-UAP-D079_Narrative-1_Western-US-Event.md"
git add "review_reports/codex_audit_20260619_DOW-UAP-D079_Narrative-1_Western-US-Event_iter2.md"
# ... および codex_audit_20260619〜20260621 シリーズ全件（PR052〜PR099, FBI-PR001〜006）
git add review_reports/codex_audit_20260619_*.md
git add review_reports/codex_audit_20260620_*.md
git add review_reports/codex_audit_20260621_*.md
git add review_reports/commit_plan_release03_work_cache_20260628.md
```

---

### GROUP G（M: note_drafts — 要確認 2件）

| ファイル | 判定 | 理由 |
|---------|------|------|
| M `note_drafts/ai_summary_DOW-UAP-PR059_NAG_UAP_1_Jun_20_note_version.md` | **commit 候補** | PR059 修正分（意図的変更）|
| M `note_drafts/release02_intro_note_version.md` | **要確認** | どの変更か不明。承認後に追加 |

---

### GROUP H（?? note_drafts — 要確認）

未追跡の note_drafts が多数存在する（PR026〜PR099 シリーズ、CIA-UAP-D001、D077、D079 等）。
これらは Release02 バッチ公開後の残存ドラフトと思われるが、今回の commit 対象として一括指定するには確認が必要。

**対応方針（ユーザー判断）:**

| 選択肢 | 説明 |
|--------|------|
| A: 今回は除外 | Phase 1 移行後に別途 commit する |
| B: 今回全件追加 | `.md` ファイルのみ追加（`.bak` は除外）|

`.bak` ファイルは確定除外（nano バックアップ）。

---

## 2. 除外対象一覧（確定）

| ファイル / ディレクトリ | 除外理由 |
|----------------------|---------|
| `metadata/uap-csv-cache.csv` | .gitignore 対象（war.gov 生キャッシュ）|
| `review_logs/source_registry.csv` | 変更禁止（source_registry.csv 変更禁止指示）|
| `workflow.db` | .gitignore 対象（バイナリ・実行状態依存）|
| `workflow.db.v1.1.bak` | バックアップファイル・不要 |
| `data/adaptive_frames/` | git 管理外（大容量・移行時に rsync でコピー）|
| `data/frame_delta_runs/` | git 管理外（解析中間生成物）|
| `data/motion_intelligence_runs/` | git 管理外（解析中間生成物）|
| `data/vlm_runs/` | git 管理外（VLM 評価データ）|
| `note_drafts/*.bak` | nano バックアップ。git 管理不要 |
| `note_drafts/release02_intro_note_version.md`（M）| 要確認のため保留 |

---

## 3. 要確認対象

| ファイル | 確認事項 | 推奨アクション |
|---------|---------|-------------|
| M `note_drafts/release02_intro_note_version.md` | どんな変更が入っているか（今回意図した変更か？）| `git diff note_drafts/release02_intro_note_version.md` で確認後に判断 |
| `note_drafts/*.md`（untracked, 70件超）| Release02 バッチ公開後の残存ドラフト。今回 commit するか？ | ユーザー判断（選択肢 A or B）|
| `review_reports/codex_audit_20260531_ai_summary_CIA-UAP-D001_intelligence_information_report_ussr_1973_note_version.md` | 既存の commit 済みファイルと重複しないか | `git log --oneline -- review_reports/codex_audit_20260531_*` で確認 |

---

## 4. 推奨 commit message

```
feat: add Release03 Work Cache Layer design, Motion Intelligence v3, and Release02 batch outputs

- Add docs/release03_work_cache_layer.md (三層アーキテクチャ設計)
- Add review_reports/release03_work_cache_migration_plan_20260628.md
- Add review_reports/release03_work_cache_phase0_check_20260628.md
- Add docs/motion_intelligence_engine_v1/v2/v3.md (設計書シリーズ)
- Add review_reports/motion_intelligence_v2/v3_design_20260627.md
- Add scripts: extract_frames_targeted.py, frame_delta_analyzer.py,
  motion_intelligence_v1/v2.py, update_release02_draft_ids.py
- Update scripts/publish_done.py
- Update metadata/files_catalog.csv
- Add published_articles/ (PR026-PR049, FBI-PR001-006, 30件)
- Add logs/notebooklm/ (PR026-PR053 公開ログ, 30件)
- Add review_reports/codex_audit_* (PR050-PR099, FBI series, 120件超)
- Add review_reports/release02_* planning and analysis reports
- Add docs/release02_article_template_v1.md
```

---

## 5. 実行手順（承認後に実行）

### Step 1: 確認コマンド（オプション）

```bash
# note_drafts/release02_intro_note_version.md の変更内容確認
git diff note_drafts/release02_intro_note_version.md | head -40
```

### Step 2: GROUP A〜F を git add（確定分）

```bash
# GROUP A: 本日作成設計書
git add docs/release03_work_cache_layer.md
git add docs/motion_intelligence_engine_v3.md
git add review_reports/release03_work_cache_migration_plan_20260628.md
git add review_reports/release03_work_cache_phase0_check_20260628.md
git add review_reports/motion_intelligence_v3_design_20260627.md

# GROUP B: 設計書・スクリプト
git add docs/motion_intelligence_engine_v1.md docs/motion_intelligence_engine_v2.md docs/release02_article_template_v1.md
git add scripts/extract_frames_targeted.py scripts/frame_delta_analyzer.py
git add scripts/motion_intelligence_v1.py scripts/motion_intelligence_v2.py
git add scripts/update_release02_draft_ids.py scripts/publish_done.py

# GROUP C: metadata
git add metadata/files_catalog.csv

# GROUP D: published_articles
git add published_articles/

# GROUP E: logs/notebooklm
git add logs/notebooklm/

# GROUP F: review_reports（個別指定）
git add review_reports/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_ai_observation_report_20260627.md
git add review_reports/apply_article_template_dry_run_20260624.md
git add review_reports/apply_article_template_v2_dry_run_20260625.md
git add review_reports/batch_final_report_20260620_PR071-PR099.md
git add review_reports/batch_status_20260620_release02_vid_batch.md
git add review_reports/commit_plan_vs_staged_diff_20260626.md
git add review_reports/frame_interval_validation_plan.md
git add review_reports/git_audit_20260618_pending_commits.md
git add review_reports/local_llm_cost_reduction_plan.md
git add review_reports/motion_intelligence_v1_design_20260627.md
git add review_reports/motion_intelligence_v2_design_20260627.md
git add review_reports/pr054_adaptive_delta_reanalysis_plan_20260626.md
git add review_reports/pr055_adaptive_reanalysis_report_20260626.md
git add review_reports/project_asset_audit.md
git add review_reports/ready_to_publish_plan_20260620_PR071-PR099.md
git add review_reports/release02_article_unit_policy_v3.md
git add review_reports/release02_coverage_audit_20260620.md
git add review_reports/release02_draft_id_update_dry_run.md
git add review_reports/release02_gap_closure_plan.md
git add review_reports/release02_hold_material_reassessment.md
git add review_reports/release02_note_publish_workflow.md
git add review_reports/release02_numbering_plan.md
git add review_reports/release02_prebatch_fix_report.md
git add review_reports/release02_publish_queue_top5.md
git add review_reports/release02_ready_to_publish_master_plan.md
git add review_reports/release02_vid_publish_queue_dry_run.md
git add review_reports/release02_video_quality_pause_plan.md
git add review_reports/rule_candidates_20260618_CIA-UAP-D001_intelligence_information_report_ussr_1973.md
git add review_reports/rule_candidates_20260618_DOW-UAP-D077_Unresolved-Case-Analysis-Update.md
git add review_reports/rule_candidates_20260618_ODNI-UAP-D001_usper_narrative_senior_usic.md
git add review_reports/rule_candidates_20260619_DOW-UAP-D079.md
git add review_reports/rule_candidates_20260619_DOW-UAP-PR053_Cigar_Shaped_or_Fast_Spherical_UAP_clip_15_OCT_22.md
git add review_reports/rule_candidates_20260619_DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron.md
git add review_reports/rule_candidates_20260621_DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission.md
git add review_reports/template_check_20260624.md
git add review_reports/template_check_20260624_final.md
git add review_reports/template_check_20260624_post_apply.md
git add review_reports/template_check_20260624_post_apply2.md
git add review_reports/template_check_after_apply_20260624.md
git add review_reports/template_consistency_v2_20260625.md
git add review_reports/codex_audit_20260530_release02_intro.md
git add review_reports/codex_audit_20260531_ODNI-UAP-D001.md
git add "review_reports/codex_audit_20260531_ai_summary_DOW-UAP-D017_general_correspondence_sandia_note_version.md"
git add "review_reports/codex_audit_20260602_ai_summary_western_us_event_slides_20260508_note_version.md"
git add review_reports/codex_audit_20260613_*.md
git add review_reports/codex_audit_20260614_*.md
git add review_reports/codex_audit_20260618_*.md
git add review_reports/codex_audit_20260619_*.md
git add review_reports/codex_audit_20260620_*.md
git add review_reports/codex_audit_20260621_*.md
git add review_reports/commit_plan_release03_work_cache_20260628.md

# GROUP G: note_drafts (PR059修正分のみ)
git add note_drafts/ai_summary_DOW-UAP-PR059_NAG_UAP_1_Jun_20_note_version.md
# ※ release02_intro は確認後に判断
```

### Step 3: git status で staging 確認

```bash
git status --short
```

### Step 4: commit

```bash
git commit -m "feat: add Release03 Work Cache Layer design, Motion Intelligence v3, and Release02 batch outputs"
```

### Step 5: push

```bash
git push origin main
```

---

## 6. note_drafts 大量追加（別 commit 候補）

note_drafts の未追跡 .md ファイル（70件超、.bak 除く）は、Release02 バッチ公開時の成果物。
今回の commit から分離し、別 commit としてまとめることを推奨する。

```bash
# .bak を除く .md のみ追加（別 commit）
git add note_drafts/*.md
# 次に .bak が staging されていないことを確認
git status --short | grep "note_drafts"
```

commit message（別 commit 用）:
```
feat: add Release02 batch note_drafts (PR026-PR099, CIA-UAP-D001, D077, D079)
```
