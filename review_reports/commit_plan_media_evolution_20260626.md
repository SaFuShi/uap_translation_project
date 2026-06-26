# Commit Plan — Media Inspector Phase 3 / Published Article Evolution

- 作成日: 2026-06-26
- 対象ブランチ: main
- 目的: Media Inspector Phase 3 パイプライン完成 + R02-041 Observation Update 完了までをcommit
- git add / commit はまだ未実施

---

## サマリー

| 区分 | ファイル数 | 状態 |
|------|-----------|------|
| commit対象（必須） | 17 | ?? (untracked) |
| commit対象（推奨追加） | 5 | ?? (untracked) |
| 除外（別タスク） | 多数 | ?? / M |
| 除外（ユーザー指定） | 多数 | ?? / M |

---

## A. commit対象（必須）

### A-1. スクリプト

| ファイル | 説明 |
|---------|------|
| `scripts/score_vlm_vs_ground_truth.py` | VLM評価結果とGround TruthのF1スコア計算 |
| `scripts/article_revision_candidate.py` | 公開記事修正候補の自動生成（risk_level分類） |
| `scripts/published_article_evolution.py` | Published Article Evolution Agent v1（4分類判定） |

### A-2. 設計書

| ファイル | 説明 |
|---------|------|
| `docs/media_inspector_ground_truth_v1.md` | Ground Truth 仕様書 v1 |
| `docs/published_article_evolution_agent_v1.md` | Evolution Agent 設計書 v1.1（4分類） |

### A-3. データ

| ファイル | 説明 |
|---------|------|
| `data/vlm_eval_set/20260625/ground_truth.csv` | 人間目視確認 Ground Truth（7件） |
| `data/vlm_runs/phase3_full50_20260626/` | Phase 3 全50件VLM実行結果ディレクトリ（全体） |

　　↳ 内包ファイル:
　　　- `results.csv` — VLM推論結果
　　　- `results.jsonl` — 詳細応答ログ
　　　- `raw_responses/` — 生応答JSON
　　　- `score_summary.csv` — F1スコアサマリー
　　　- `article_revision_candidates.csv` — 修正候補CSV
　　　- `published_article_evolution.csv` — Evolution判定CSV（R02-041: done）

### A-4. レビューレポート（ユーザー指定）

| ファイル | 説明 |
|---------|------|
| `review_reports/vlm_score_qwen2_5_vl_7b_20260626.md` | VLMスコアリングレポート |
| `review_reports/article_revision_candidates_20260626.md` | 全記事修正候補レポート |
| `review_reports/article_revision_high6_confirmed_20260626.md` | HIGH 6件確定分析レポート |
| `review_reports/published_article_evolution_plan_20260626.md` | Evolution方針・R02-041確定文案 |
| `review_reports/published_article_evolution_report_20260626.md` | Evolution Agent出力レポート（v1.1） |

---

## B. commit対象（推奨追加）

R02-041 Evolution の記録として一体性が高い。今回まとめてcommitを推奨。

| ファイル | 説明 | 理由 |
|---------|------|------|
| `review_reports/r02_041_note_update_diff_20260626.md` | R02-041 note修正差分レポート | Evolution完了の作業記録 |
| `review_reports/vlm_connection_test.md` | VLM接続テスト結果 | Media Inspector環境セットアップ記録 |
| `review_reports/vlm_phase2_5sample_report.md` | Phase 2（5件サンプル）レポート | Phase 3前の検証記録 |
| `review_reports/vlm_phase3_full50_report.md` | Phase 3（全50件）完全レポート | Phase 3実施記録 |
| `review_reports/vlm_phase3_human_review_targets.md` | 人間確認ターゲット一覧 | Ground Truth作成の根拠 |

---

## C. 除外（ユーザー指定）

以下はcommitしない。変更が存在する場合も除外。

| ファイル/ディレクトリ | 除外理由 |
|---------------------|---------|
| `note_drafts/*` | ユーザー指定除外 |
| `published_articles/*` | ユーザー指定除外 |
| `review_logs/source_registry.csv` (M) | ユーザー指定除外 |
| `workflow.db` / `workflow.db.v1.1.bak` | ユーザー指定除外 / .bak |
| `metadata/files_catalog.csv` (M) | ユーザー指定除外 |
| `metadata/uap-csv-cache.csv` (M) | ユーザー指定除外 |

---

## D. 除外（別タスク・無関係）

以下は今回のcommitスコープ外。別途commitを検討。

| ファイル/ディレクトリ | 除外理由 |
|---------------------|---------|
| `scripts/publish_done.py` (M) | 公開ワークフロー変更（別タスク） |
| `scripts/update_release02_draft_ids.py` | 別タスク |
| `docs/release02_article_template_v1.md` | 別タスク |
| `logs/notebooklm/` (多数) | 公開ログ（別タスク） |
| `review_reports/codex_audit_*` (多数) | Codex監査レポート（別タスク） |
| `review_reports/release02_*` (多数) | Release 02ワークフロー（別タスク） |
| `review_reports/template_*` | テンプレート（別タスク） |
| `review_reports/rule_candidates_*` | ルール候補（別タスク） |
| `review_reports/apply_article_template_*` | テンプレート適用（別タスク） |
| `review_reports/batch_*` | バッチ処理（別タスク） |
| `review_reports/git_audit_*` | git監査（別タスク） |
| `review_reports/ready_to_publish_*` | 公開キュー（別タスク） |
| `review_reports/local_llm_cost_reduction_plan.md` | 別タスク |
| `review_reports/project_asset_audit.md` | 別タスク |
| `review_reports/frame_interval_validation_plan.md` | 別タスク |
| `review_reports/vlm_eval_execution_plan.md` | 既にtracked（変更なし） |

---

## E. git add コマンド（確認後に実行）

```bash
git add \
  scripts/score_vlm_vs_ground_truth.py \
  scripts/article_revision_candidate.py \
  scripts/published_article_evolution.py \
  docs/media_inspector_ground_truth_v1.md \
  docs/published_article_evolution_agent_v1.md \
  data/vlm_eval_set/20260625/ground_truth.csv \
  data/vlm_runs/phase3_full50_20260626/ \
  review_reports/vlm_score_qwen2_5_vl_7b_20260626.md \
  review_reports/article_revision_candidates_20260626.md \
  review_reports/article_revision_high6_confirmed_20260626.md \
  review_reports/published_article_evolution_plan_20260626.md \
  review_reports/published_article_evolution_report_20260626.md \
  review_reports/r02_041_note_update_diff_20260626.md \
  review_reports/vlm_connection_test.md \
  review_reports/vlm_phase2_5sample_report.md \
  review_reports/vlm_phase3_full50_report.md \
  review_reports/vlm_phase3_human_review_targets.md
```

> 必須のみ（Bを除外する場合）は末尾5行を省く。

---

## F. 推奨 commit message

```
Add Media Inspector Phase 3 pipeline and R02-041 Observation Update

- Add VLM scoring, article revision candidate, and evolution agent scripts (v1)
- Add Ground Truth CSV (7 records, human-verified 2026-06-26)
- Add Phase 3 full-50 VLM run results (qwen2.5-vl-7b-instruct)
- Add design docs: ground_truth_v1, evolution_agent_v1.1 (4-category decision)
- Record R02-041 evolution: Observation Update → done (note updated 2026-06-26)
- Add HIGH-6 analysis, evolution plan, and evolution report
```

---

## G. 注意事項

| 項目 | 内容 |
|------|------|
| `data/vlm_runs/` が `??` | ディレクトリ丸ごと未追跡。`phase3_full50_20260626/` 配下の全ファイルが含まれる |
| `raw_responses/` 配下 | 生JSONファイル多数。容量確認推奨（git add前に `du -sh data/vlm_runs/` で確認） |
| published_articles は除外 | `??` で多数存在するが今回はcommitしない（別タスクで整理） |
| source_registry.csv は除外 | `M` だが今回のスコープ外 |

---

## H. 容量確認コマンド（git add前に実行推奨）

```bash
du -sh data/vlm_runs/phase3_full50_20260626/
du -sh data/vlm_runs/phase3_full50_20260626/raw_responses/
```
