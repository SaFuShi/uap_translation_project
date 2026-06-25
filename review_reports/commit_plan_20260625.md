# Commit Plan 2026-06-25

Generated: 2026-06-25

目的:

- `git status --short --untracked-files=all` の大量出力を、今回commit推奨・保留・除外に分類する。
- このレポート作成時点では `git add` は実行していない。

## Status概要

トップレベル別の概数:

| path | count |
|---|---:|
| `review_reports/` | 221 |
| `note_drafts/` | 167 |
| `data/` | 53 |
| `published_articles/` | 15 |
| `logs/` | 15 |
| `scripts/` | 7 |
| `metadata/` | 2 |
| `docs/` | 2 |
| `review_logs/` | 1 |
| `workflow.db.v1.1.bak` | 1 |

Tracked modified:

- `metadata/files_catalog.csv`
- `metadata/uap-csv-cache.csv`
- `note_drafts/release02_intro_note_version.md`
- `review_logs/source_registry.csv`

Untracked notable:

- `data/vlm_eval_set/20260625/` 一式
- Media Inspector / VLM関連 scripts
- Template v2 / 公開運用関連 scripts/docs
- 公開済み記事 `published_articles/` 15件
- NotebookLM logs 15件
- `note_drafts/` 大量の新規ドラフトと `.bak`
- `workflow.db.v1.1.bak`

`workflow.db` 本体は今回の status には出ていない。commit対象に含める変更は現時点ではない。

## 推奨commit構成

### Commit 1: Media Inspector / VLM評価基盤

目的:

- Claudeの全件フレーム確認を減らすための候補抽出・評価セット・VLM評価設計をまとめる。

commit推奨:

```text
scripts/media_inspector.py
scripts/build_vlm_eval_set.py
review_reports/media_inspector_candidates_20260625.md
review_reports/vlm_eval_execution_plan.md
review_reports/commit_plan_20260625.md
data/vlm_eval_set/20260625/README.md
data/vlm_eval_set/20260625/manifest.csv
data/vlm_eval_set/20260625/manifest.json
data/vlm_eval_set/20260625/images/
```

補足:

- `data/vlm_eval_set/20260625/` は評価固定セットなので、再現性を重視するなら画像50枚もcommit対象に含める。
- リポジトリ容量を抑える運用なら、`images/` は保留し、`manifest.*` とREADMEだけcommitする案もある。ただしVLM比較の再現性は落ちる。

推奨commit message:

```text
Add media inspector and local VLM evaluation set
```

### Commit 2: Release 02 Template v2 / 公開運用ツール

目的:

- 公開パッケージ確認、公開後処理、記事テンプレート適用、テンプレート整合性チェックをまとめる。

commit推奨:

```text
scripts/open_publish_package.py
scripts/publish_done.py
scripts/apply_article_template.py
scripts/check_article_template_consistency.py
docs/release02_article_template_v2.md
review_reports/apply_article_template_v2_dry_run_20260625.md
review_reports/template_consistency_v2_20260625.md
```

確認してから含める候補:

```text
scripts/update_release02_draft_ids.py
docs/release02_article_template_v1.md
```

判断:

- `scripts/update_release02_draft_ids.py` は今回のユーザー指定リストにはないが、Release 02正式採番フローに関係する。既に運用済みで残すべきならCommit 2に含める。
- `docs/release02_article_template_v1.md` はv2前の参照資料として必要なら含める。v2のみが正なら保留。

推奨commit message:

```text
Add Release 02 template v2 and publish workflow helpers
```

### Commit 3: Release 02 published article post-processing

目的:

- 公開済み記事PR019-PR037の公開後成果物、NotebookLMログ、source_registry更新をまとめる。

commit推奨:

```text
review_logs/source_registry.csv
published_articles/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_published_20260624.md
published_articles/ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020_published_20260625.md
published_articles/ai_summary_DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020_published_20260625.md
logs/notebooklm/2026-06-24_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020_published_log.md
logs/notebooklm/2026-06-25_DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020_published_log.md
```

note draft候補:

```text
note_drafts/release02_intro_note_version.md
note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md
note_drafts/ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md
note_drafts/ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_note_version.md
note_drafts/ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_note_version.md
note_drafts/ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md
note_drafts/ai_summary_DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md
note_drafts/ai_summary_DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024_note_version.md
note_drafts/ai_summary_DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024_note_version.md
note_drafts/ai_summary_DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024_note_version.md
note_drafts/ai_summary_DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024_note_version.md
note_drafts/ai_summary_DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024_note_version.md
note_drafts/ai_summary_DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023_note_version.md
note_drafts/ai_summary_DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023_note_version.md
note_drafts/ai_summary_DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020_note_version.md
note_drafts/ai_summary_DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020_note_version.md
```

判断:

- 上記note draftsは、公開済みPR019-PR037の元ドラフトとして追跡するならCommit 3に含める。
- `workflow.db` 本体は変更表示がないため含めない。
- `workflow.db.v1.1.bak` は含めない。

推奨commit message:

```text
Add Release 02 published article outputs through PR037
```

## 保留すべきファイル

metadata:

```text
metadata/files_catalog.csv
metadata/uap-csv-cache.csv
```

理由:

- 変更理由が今回のMedia/VLM、Template v2、公開後処理のどれに属するか未確認。
- catalog/cache系は差分確認後に別commit推奨。

未公開・大量note drafts:

```text
note_drafts/ai_summary_CIA-UAP-D001_intelligence_information_report_ussr_1973_note_version.md
note_drafts/ai_summary_DOW-UAP-D077_Unresolved-Case-Analysis-Update_Western-United-States-Event_note_version.md
note_drafts/ai_summary_DOW-UAP-D079_Narrative-1_Western-US-Event_note_version.md
note_drafts/ai_summary_DOW-UAP-PR038_*_note_version.md
note_drafts/ai_summary_DOW-UAP-PR039_*_note_version.md
...
note_drafts/ai_summary_DOW-UAP-PR099_*_note_version.md
note_drafts/ai_summary_FBI-UAP-PR001_*_note_version.md
...
note_drafts/ai_summary_FBI-UAP-PR006_*_note_version.md
note_drafts/ai_summary_ODNI-UAP-D001_usper_narrative_senior_usic_note_version.md
note_drafts/ai_summary_western_us_event_slides_20260508_note_version.md
note_drafts/archive/ai_summary_DOW-UAP-PR071_USAF_ANG_F-16C_callsign_CALLSIGN_Shoots_Down_UAP_over_Lake_Huron_with_Weapon_System_note_version.md
```

理由:

- 大量で範囲が広く、公開済み・未公開・Release 03候補が混在している。
- 公開済みPR019-PR037以外は別commitまたは別レビューが安全。

大量review reports:

```text
review_reports/codex_audit_*.md
review_reports/rule_candidates_*.md
review_reports/release02_*.md
review_reports/template_check_20260624*.md
review_reports/project_asset_audit.md
review_reports/local_llm_cost_reduction_plan.md
...
```

理由:

- `review_reports/` は221件あり、今回のVLM/Template/公開後処理に直接必要なものだけを選ぶべき。
- 過去監査ログをまとめて入れるなら別commit推奨。

## commit対象から除外すべきファイル

バックアップ/一時ファイル:

```text
workflow.db.v1.1.bak
note_drafts/*.bak
```

現状 `.bak` は80件。原則commitしない。

除外案:

```gitignore
*.bak
workflow.db.*.bak
```

注意:

- `.gitignore` の追加自体は別判断。既存運用でバックアップを追跡しているなら追加前に確認する。

その他:

- `data/` 配下は `data/vlm_eval_set/20260625/` 以外をcommitしない。
- `workflow.db` 本体はstatusに出ていないためcommit不要。

## 推奨git add案

まだ実行しない。実行する場合の候補のみ。

Commit 1:

```bash
git add scripts/media_inspector.py scripts/build_vlm_eval_set.py \
  review_reports/media_inspector_candidates_20260625.md \
  review_reports/vlm_eval_execution_plan.md \
  review_reports/commit_plan_20260625.md \
  data/vlm_eval_set/20260625
```

Commit 2:

```bash
git add scripts/open_publish_package.py scripts/publish_done.py \
  scripts/apply_article_template.py scripts/check_article_template_consistency.py \
  docs/release02_article_template_v2.md \
  review_reports/apply_article_template_v2_dry_run_20260625.md \
  review_reports/template_consistency_v2_20260625.md
```

Commit 3:

```bash
git add review_logs/source_registry.csv published_articles logs/notebooklm \
  note_drafts/release02_intro_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_May_2022_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_2022_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Emirates_October_2023_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January_2024_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October_2024_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October_2024_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October_2023_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_May_2020_note_version.md \
  note_drafts/ai_summary_DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020_note_version.md
```

重要:

- `git add note_drafts/` は使わない。`.bak` と未公開ドラフトを巻き込む。
- `git add review_reports/` は使わない。過去監査ログを大量に巻き込む。
- `git add data/` は使わない。今回対象は `data/vlm_eval_set/20260625/` のみ。

## 最終判断

最も安全な順序:

1. Commit 1だけ先に作る。これは今回のMedia Inspector / VLM評価作業として閉じている。
2. Commit 2はTemplate v2運用ツールの差分確認後に作る。
3. Commit 3は公開済み記事範囲、source_registry差分、note_drafts公開済み範囲を確認してから作る。
4. metadataと未公開note_draftsは別レビューまで保留する。
