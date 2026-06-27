# Commit Plan: Media Inspector v2

- 作成日: 2026-06-27
- 対象ブランチ: main
- ステータス: **実行待ち（git add は未実施）**

---

## 1. git status 現況サマリー

```
修正済み (M):
  metadata/files_catalog.csv          ← 除外（本 commit 対象外）
  metadata/uap-csv-cache.csv          ← 除外（.gitignore 対象だが追跡済）
  note_drafts/ai_summary_PR059_*.md   ← 除外（note_drafts 禁止）
  note_drafts/release02_intro_*.md    ← 除外（note_drafts 禁止）
  review_logs/source_registry.csv     ← 除外（source_registry 禁止）
  scripts/publish_done.py             ← 除外（別 commit）

未追跡 (??):
  data/adaptive_frames/               ← 除外（PNG 画像ディレクトリ）
  data/frame_delta_runs/              ← 部分採用（v2 CSV/summary のみ）
  data/vlm_runs/phase2_5sample_*/     ← 除外（別 commit 候補）
  docs/media_inspector_architecture_v2.md    ← ✅ 採用
  docs/release02_article_template_v1.md      ← 除外（別 commit）
  logs/notebooklm/*                   ← 除外（別 commit: Release02 publish batch）
  note_drafts/*                       ← 除外（note_drafts 禁止）
  published_articles/*                ← 除外（別 commit）
  review_reports/*                    ← 部分採用（下記リスト参照）
  scripts/extract_frames_targeted.py  ← 除外（Adaptive Pipeline v1 batch）
  scripts/frame_delta_analyzer.py     ← 除外（Adaptive Pipeline v1 batch）
  scripts/frame_delta_v2.py           ← ✅ 採用
  scripts/generate_ai_observation_report.py  ← ✅ 採用
  scripts/update_release02_draft_ids.py      ← 除外（別 commit）
```

---

## 2. 本 commit の採用ファイル一覧（15件）

### 採用理由の凡例

- **[NEW-CORE]** Media Inspector v2 の核心（スクリプト・設計）
- **[NEW-RESULT]** v2 パイプラインの検証結果（Delta CSV / summary / Report）
- **[NEW-PLAN]** 採用決定・計画文書
- **[NEW-HIST]** 旧方式の参照用記録（歴史的経緯として保持）

### スクリプト（2件）

| # | ファイル | 分類 | 備考 |
|---|--------|------|------|
| 1 | `scripts/frame_delta_v2.py` | [NEW-CORE] | CUT誤分類修正・3条件AND化・734行 |
| 2 | `scripts/generate_ai_observation_report.py` | [NEW-CORE] | AI Observation Report自動生成・1252行 |

### ドキュメント（1件）

| # | ファイル | 分類 | 備考 |
|---|--------|------|------|
| 3 | `docs/media_inspector_architecture_v2.md` | [NEW-CORE] | v2設計全体像・v1→v2変更理由・タイムコードルール定義 |

### レビューレポート（8件）

| # | ファイル | 分類 | 備考 |
|---|--------|------|------|
| 4 | `review_reports/ai_observation_report_design_20260627.md` | [NEW-CORE] | AI Observation Report仕様書 |
| 5 | `review_reports/unpublished_vid_reanalysis_plan_20260626.md` | [NEW-PLAN] | 未公開VID41件のv2 Pipeline処理計画 |
| 6 | `review_reports/frame_delta_v2_adoption_report_20260627.md` | [NEW-PLAN] | v2正式採用判定レポート・PR059/PR060検証結果 |
| 7 | `review_reports/commit_plan_media_inspector_v2_20260627.md` | [NEW-PLAN] | このファイル自体 |
| 8 | `review_reports/pr059_source_video_review_guide_20260627.md` | [NEW-HIST] | 旧 Human Q&A 型の最終例（廃止済・参照用） |
| 9 | `review_reports/DOW-UAP-PR059_NAG_UAP_1_Jun_20_ai_observation_report_20260627.md` | [NEW-RESULT] | PR059 AI Observation Report（v1 delta ベース） |
| 10 | `review_reports/pr060_ai_observation_report_20260627.md` | [NEW-RESULT] | PR060 AI Observation Report（v1 delta ベース） |

### データ（v2 delta のみ、4件）

| # | ファイル | 分類 | 備考 |
|---|--------|------|------|
| 11 | `data/frame_delta_runs/20260627_v2/DOW-UAP-PR059_NAG_UAP_1_Jun_20/frame_delta.csv` | [NEW-RESULT] | PR059 v2 delta・97行 |
| 12 | `data/frame_delta_runs/20260627_v2/DOW-UAP-PR059_NAG_UAP_1_Jun_20/summary.md` | [NEW-RESULT] | PR059 v2 delta summary |
| 13 | `data/frame_delta_runs/20260627_v2/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/frame_delta.csv` | [NEW-RESULT] | PR060 v2 delta・96行（CUT=2修正済） |
| 14 | `data/frame_delta_runs/20260627_v2/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/summary.md` | [NEW-RESULT] | PR060 v2 delta summary |

**採用合計: 14ファイル**（このファイル自身=15件目は commit_plan そのもの）

---

## 3. 除外ファイルの整理

### 除外理由 A: 永続的禁止（ルール）

| ファイル | 理由 |
|--------|------|
| `note_drafts/*`（全件） | note_drafts 変更禁止ルール |
| `review_logs/source_registry.csv` | source_registry 禁止ルール |
| `metadata/uap-csv-cache.csv` | .gitignore 対象（変更追跡不要） |
| `data/adaptive_frames/` | PNG 画像ディレクトリ（原則対象外） |

### 除外理由 B: 別 commit に分割

| ファイル | 推奨 commit |
|--------|-----------|
| `scripts/frame_delta_analyzer.py` | `feat: add Adaptive Pipeline v1 scripts` |
| `scripts/extract_frames_targeted.py` | 同上 |
| `data/frame_delta_runs/20260626/`（PR053-PR059 v1） | 同上 |
| `data/frame_delta_runs/20260627/`（PR060 v1、ネスト構造あり） | 同上 |
| `scripts/publish_done.py`（修正済M） | `fix: update publish workflow` |
| `metadata/files_catalog.csv`（修正済M） | 上記と同 commit |
| `logs/notebooklm/*` | `record: add publish logs PR026-PR049+FBI` |
| `published_articles/*` | 同上 |
| `docs/release02_article_template_v1.md` | `feat: add Release02 article template v1` |
| `scripts/update_release02_draft_ids.py` | 同上 |
| `data/vlm_runs/phase2_5sample_20260626/` | `data: add VLM phase2 5sample run` |

### 除外理由 C: 保留（別途整理）

| 対象 | 件数 | 理由 |
|------|------|------|
| `review_reports/codex_audit_*` | 150件超 | Codex Audit batch として別途まとめて commit |
| `review_reports/release02_*` | 15件超 | Release02 計画・整理 batch として別途 |
| `review_reports/rule_candidates_*` | 8件 | ルール候補 batch |
| その他 review_reports（バッチ状況・計画） | 多数 | 上記バッチに統合検討 |

### 除外理由 D: jsonl ファイル（全件除外）

`data/frame_delta_runs/*/frame_delta.jsonl` は CSV と同一データの JSON-Lines 形式。
再生成可能・容量増加のみのため git 管理不要。

---

## 4. git add コマンド（確認後に実行）

```bash
# ── スクリプト ──
git add scripts/frame_delta_v2.py
git add scripts/generate_ai_observation_report.py

# ── ドキュメント ──
git add docs/media_inspector_architecture_v2.md

# ── レビューレポート ──
git add review_reports/ai_observation_report_design_20260627.md
git add review_reports/unpublished_vid_reanalysis_plan_20260626.md
git add review_reports/frame_delta_v2_adoption_report_20260627.md
git add review_reports/commit_plan_media_inspector_v2_20260627.md
git add review_reports/pr059_source_video_review_guide_20260627.md
git add "review_reports/DOW-UAP-PR059_NAG_UAP_1_Jun_20_ai_observation_report_20260627.md"
git add review_reports/pr060_ai_observation_report_20260627.md

# ── データ（v2 delta のみ・jsonl は除外）──
git add "data/frame_delta_runs/20260627_v2/DOW-UAP-PR059_NAG_UAP_1_Jun_20/frame_delta.csv"
git add "data/frame_delta_runs/20260627_v2/DOW-UAP-PR059_NAG_UAP_1_Jun_20/summary.md"
git add "data/frame_delta_runs/20260627_v2/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/frame_delta.csv"
git add "data/frame_delta_runs/20260627_v2/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/summary.md"
```

---

## 5. 推奨 commit message

```
feat: implement Media Inspector v2 - AI Observation Report pipeline

CUT誤分類問題（PR060でCUT=41の誤検出）を根本解消。
frame_delta_v2.py でCUT判定を「brightness急変 AND tracking失敗 AND
scene_structure破綻」の3条件ANDに変更し、大型オブジェクト移動を
CUTから除外。generate_ai_observation_report.py でAI Observation
Report型のセグメント別自動レポートを実装。PR059/PR060で検証完了。

Changes:
- scripts/frame_delta_v2.py: CUT 3条件AND化、ZOOM_BLOOM/CAMERA_TRACK追加
- scripts/generate_ai_observation_report.py: AI Observation Report自動生成
- docs/media_inspector_architecture_v2.md: v2アーキテクチャ設計定義
- review_reports/ai_observation_report_design_20260627.md: 仕様書
- review_reports/frame_delta_v2_adoption_report_20260627.md: 採用判定レポート
- review_reports/unpublished_vid_reanalysis_plan_20260626.md: v2 Pipeline計画
- data/frame_delta_runs/20260627_v2/: PR059/PR060 v2 delta検証結果

Verified:
  PR059: CUT v1=8 → v2=2, STATIC=39 → OBJECT_MOVE=73
  PR060: CUT v1=41 → v2=2, OBJECT_MOVE=51 → 80
```

---

## 6. 次回 commit の予定（参考）

| 優先度 | commit タイトル | 対象ファイル数 |
|--------|--------------|------------|
| 高 | `feat: add Adaptive Pipeline v1 scripts and delta runs` | ~20件（frame_delta_analyzer.py, extract_frames_targeted.py, data/frame_delta_runs/20260626/ and 20260627/） |
| 中 | `fix: update publish workflow and files_catalog` | 2件（scripts/publish_done.py, metadata/files_catalog.csv） |
| 中 | `record: add publish logs and published articles PR026-PR053+FBI` | ~50件（logs/notebooklm/*, published_articles/*） |
| 低 | `chore: add codex audit reports batch` | 150件超（review_reports/codex_audit_*） |
| 低 | `chore: add Release02 planning reports` | 20件超（review_reports/release02_*, rule_candidates_*） |

---

## 7. 安全チェックリスト（commit 前確認）

- [ ] `git status` で M ファイル（note_drafts, source_registry, workflow.db）が staging に入っていないか確認
- [ ] `git diff --cached` でステージング内容を目視確認
- [ ] `data/adaptive_frames/` が staging に入っていないか確認
- [ ] `*/frame_delta.jsonl` が staging に入っていないか確認
- [ ] `note_drafts/*` が staging に入っていないか確認
- [ ] commit message にファイルパスの誤りがないか確認

---

## 8. 注意事項

### data/frame_delta_runs/20260627/ の nested 構造

PR060 の v1 delta run は以下のネスト構造になっている（スクリプトが --output-dir にソースIDを含んだ際の二重ネスト）:

```
data/frame_delta_runs/20260627/
└── DOW-UAP-PR060_.../
    └── DOW-UAP-PR060_.../   ← ネストされた同名ディレクトリ
        ├── frame_delta.csv
        ├── frame_delta.jsonl
        └── summary.md
```

v2 では正常な構造:
```
data/frame_delta_runs/20260627_v2/
└── DOW-UAP-PR060_.../
    ├── frame_delta.csv  ← 直下に配置
    ├── frame_delta.jsonl
    └── summary.md
```

本 commit では v2 のみ採用。v1 ネスト構造ファイルは Adaptive Pipeline v1 commit に含める。

### PR059/PR060 AI Observation Report の delta ベース

現在の AI Observation Report（#8, #9）は **v1 delta をベース**に生成されている。
v2 delta で再生成すると以下が変わる:
- PR060: 「31回のシーン急変」→「対象物の継続移動」
- PR059: セグメントEの CUT 件数記述が更新

再生成は PR061 以降の v2 パイプライン確立後に実施予定。
本 commit では v1 ベースのまま記録として保存する。
