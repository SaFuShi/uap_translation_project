# git未コミット状態 監査レポート

**生成日時：** 2026-06-18
**スクリプト：** scripts/git_publish_helper.py

---

## 1. 未コミットファイル一覧

### metadata（commit対象外）

- [modified] metadata/uap-csv-cache.csv

### note_drafts

- [modified] note_drafts/release02_intro_note_version.md
- [untracked] note_drafts/ai_summary_CIA-UAP-D001_intelligence_information_report_ussr_1973_note_version.md
- [untracked] note_drafts/ai_summary_DOW-UAP-PR050_4_UAP_Formation_Iran_note_version.md
- [untracked] note_drafts/ai_summary_DOW-UAP-PR051_Syrian_UAP_instant_acceleration_note_version.md
- [untracked] note_drafts/ai_summary_ODNI-UAP-D001_usper_narrative_senior_usic_note_version.md
- [untracked] note_drafts/ai_summary_western_us_event_slides_20260508_note_version.md

### review_reports

- [untracked] review_reports/codex_audit_20260530_release02_intro.md
- [untracked] review_reports/codex_audit_20260531_ODNI-UAP-D001.md
- [untracked] review_reports/codex_audit_20260531_ai_summary_DOW-UAP-D017_general_correspondence_sandia_note_version.md
- [untracked] review_reports/codex_audit_20260602_ai_summary_western_us_event_slides_20260508_note_version.md
- [untracked] review_reports/codex_audit_20260613_DOW-UAP-PR050_4_UAP_Formation_Iran.md
- [untracked] review_reports/codex_audit_20260613_DOW-UAP-PR050_4_UAP_Formation_Iran_iter2.md
- [untracked] review_reports/codex_audit_20260614_DOW-UAP-PR051_Syrian_UAP_instant_acceleration.md
- [untracked] review_reports/codex_audit_20260614_DOW-UAP-PR051_Syrian_UAP_instant_acceleration_iter2.md

### scripts

- [untracked] scripts/git_publish_helper.py

---

## 2. commit対象外ファイル

- metadata/uap-csv-cache.csv

---

## 3a. commit候補 [safe] ─ インフラ・ツール系

> scripts / docs / prompts / provenance など。内容確認後にcommit可。

### _misc  [safe]

- scripts/git_publish_helper.py

**commit message案:** `docs: add _misc related files`

```bash
git add scripts/git_publish_helper.py
git commit -m 'docs: add _misc related files'
```

---

## 3b. commit候補 [要確認] ─ コンテンツ系（人間確認推奨）

> note_drafts / review_reports / published_articles / logs など。
> 内容を人間が確認してからcommitしてください。

### CIA-UAP-D001_intelligence_information_report_ussr_1973  [要確認]

- note_drafts/ai_summary_CIA-UAP-D001_intelligence_information_report_ussr_1973_note_version.md

**commit message案:** `docs: add CIA-UAP-D001_intelligence_information_report_ussr_1973 related files`

```bash
git add note_drafts/ai_summary_CIA-UAP-D001_intelligence_information_report_ussr_1973_note_version.md
git commit -m 'docs: add CIA-UAP-D001_intelligence_information_report_ussr_1973 related files'
```

### DOW-UAP-D017_general_correspondence_sandia  [要確認]

- review_reports/codex_audit_20260531_ai_summary_DOW-UAP-D017_general_correspondence_sandia_note_version.md

**commit message案:** `docs: add DOW-UAP-D017_general_correspondence_sandia codex audit report(s)`

```bash
git add review_reports/codex_audit_20260531_ai_summary_DOW-UAP-D017_general_correspondence_sandia_note_version.md
git commit -m 'docs: add DOW-UAP-D017_general_correspondence_sandia codex audit report(s)'
```

### DOW-UAP-PR050_4_UAP_Formation_Iran  [要確認]

- note_drafts/ai_summary_DOW-UAP-PR050_4_UAP_Formation_Iran_note_version.md
- review_reports/codex_audit_20260613_DOW-UAP-PR050_4_UAP_Formation_Iran.md
- review_reports/codex_audit_20260613_DOW-UAP-PR050_4_UAP_Formation_Iran_iter2.md

**commit message案:** `docs: add DOW-UAP-PR050_4_UAP_Formation_Iran codex audit report(s)`

```bash
git add note_drafts/ai_summary_DOW-UAP-PR050_4_UAP_Formation_Iran_note_version.md review_reports/codex_audit_20260613_DOW-UAP-PR050_4_UAP_Formation_Iran.md review_reports/codex_audit_20260613_DOW-UAP-PR050_4_UAP_Formation_Iran_iter2.md
git commit -m 'docs: add DOW-UAP-PR050_4_UAP_Formation_Iran codex audit report(s)'
```

### DOW-UAP-PR051_Syrian_UAP_instant_acceleration  [要確認]

- note_drafts/ai_summary_DOW-UAP-PR051_Syrian_UAP_instant_acceleration_note_version.md
- review_reports/codex_audit_20260614_DOW-UAP-PR051_Syrian_UAP_instant_acceleration.md
- review_reports/codex_audit_20260614_DOW-UAP-PR051_Syrian_UAP_instant_acceleration_iter2.md

**commit message案:** `docs: add DOW-UAP-PR051_Syrian_UAP_instant_acceleration codex audit report(s)`

```bash
git add note_drafts/ai_summary_DOW-UAP-PR051_Syrian_UAP_instant_acceleration_note_version.md review_reports/codex_audit_20260614_DOW-UAP-PR051_Syrian_UAP_instant_acceleration.md review_reports/codex_audit_20260614_DOW-UAP-PR051_Syrian_UAP_instant_acceleration_iter2.md
git commit -m 'docs: add DOW-UAP-PR051_Syrian_UAP_instant_acceleration codex audit report(s)'
```

### ODNI-UAP-D001  [要確認]

- review_reports/codex_audit_20260531_ODNI-UAP-D001.md

**commit message案:** `docs: add ODNI-UAP-D001 codex audit report(s)`

```bash
git add review_reports/codex_audit_20260531_ODNI-UAP-D001.md
git commit -m 'docs: add ODNI-UAP-D001 codex audit report(s)'
```

### ODNI-UAP-D001_usper_narrative_senior_usic  [要確認]

- note_drafts/ai_summary_ODNI-UAP-D001_usper_narrative_senior_usic_note_version.md

**commit message案:** `docs: add ODNI-UAP-D001_usper_narrative_senior_usic related files`

```bash
git add note_drafts/ai_summary_ODNI-UAP-D001_usper_narrative_senior_usic_note_version.md
git commit -m 'docs: add ODNI-UAP-D001_usper_narrative_senior_usic related files'
```

### release02_intro  [要確認]

- note_drafts/release02_intro_note_version.md
- review_reports/codex_audit_20260530_release02_intro.md

**commit message案:** `docs: add release02_intro note draft and audit reports`

```bash
git add note_drafts/release02_intro_note_version.md review_reports/codex_audit_20260530_release02_intro.md
git commit -m 'docs: add release02_intro note draft and audit reports'
```

### western_us_event_slides_20260508  [要確認]

- note_drafts/ai_summary_western_us_event_slides_20260508_note_version.md
- review_reports/codex_audit_20260602_ai_summary_western_us_event_slides_20260508_note_version.md

**commit message案:** `docs: add western_us_event_slides_20260508 codex audit report(s)`

```bash
git add note_drafts/ai_summary_western_us_event_slides_20260508_note_version.md review_reports/codex_audit_20260602_ai_summary_western_us_event_slides_20260508_note_version.md
git commit -m 'docs: add western_us_event_slides_20260508 codex audit report(s)'
```

---

## 4. 直近commitログ（参考）

- 3ef9fff feat: add IMG direct-download fallback for war.gov medialinks
- 5148eaa feat: support Release 03 catalog and download history tracking
- 94778d3 docs: record DOW-UAP-PR051 publication and add VID draft rules
- 07ad0bf docs: record DOW-UAP-PR050 publication and Codex iter2 PASS
- 5c7eab7 docs: record DOE-UAP-D003 publication and Codex iter2 PASS
- 35c7804 docs: record DOE-UAP-D002 publication and Codex iter2 PASS
- 4d493d7 feat: add post-publish workflow helper
- 27331ba feat: show Finder commands for final review assets
- 357ccc9 docs: record DOE-UAP-D001 publication and semiauto updates
- adca269 docs: record Claude-Codex semiauto PoC completion

---

## 5. 安全確認

- [ ] git add / commit / push は自動実行されていない
- [ ] Mac mini pull は自動実行されていない
- [ ] workflow.db は変更されていない
- [ ] source_registry.csv は変更されていない
- [ ] metadata/uap-csv-cache.csv は変更されていない
