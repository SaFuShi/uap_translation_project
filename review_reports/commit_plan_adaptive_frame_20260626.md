# Commit Plan — Adaptive Frame Extraction + Release02 VID Pipeline 更新

- 作成日: 2026-06-26
- 対象コミット: feat: adopt adaptive frame extraction for Release02 pipeline
- 作成者: SaFuShi
- 状態: **計画済み・git add 未実施**

---

## 1. commit 対象ファイル一覧

### ■ scripts（新規 2件）

| ファイル | git状態 | 説明 |
|---------|---------|------|
| `scripts/extract_frames_adaptive.py` | `??` | Adaptive Frame 抽出スクリプト（ADAPTIVE_RULES v1.1） |
| `scripts/run_vlm_on_adaptive.py` | `??` | VLM バッチ実行スクリプト（Qwen2.5-VL-7B / LM Studio）|

> `scripts/run_vlm_on_adaptive.py` はユーザー指示の対象候補リストに明示されていないが、パイプライン再現に必須のため含める。

---

### ■ note_drafts（4件 / PR043〜046 Adaptive addendum 反映済み）

| ファイル | git状態 | 変更内容 |
|---------|---------|---------|
| `note_drafts/ai_summary_DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025_note_version.md` | `??` | Adaptive addendum 追記（VLM 0検出・UAP対象物なし確認） |
| `note_drafts/ai_summary_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_note_version.md` | `M` | Adaptive addendum 追記（後半区間273-312s・VLM過検出訂正） |
| `note_drafts/ai_summary_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_note_version.md` | `M` | Adaptive addendum 追記（後半区間48-57s・映像終端まで継続確認） |
| `note_drafts/ai_summary_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md` | `??` | Adaptive addendum 追記（全区間変化なし・形状両義性・移動判断不可） |

> ⚠️ **除外**: 同ディレクトリの `.bak` ファイルはすべて除外する。

---

### ■ review_reports（4件 新規）

| ファイル | git状態 | 説明 |
|---------|---------|------|
| `review_reports/adaptive_frame_extraction_plan_20260626.md` | `??` | Adaptive Frame 設計・dry-run 計画（v1.1） |
| `review_reports/adaptive_frame_vlm_comparison_20260626.md` | `??` | Adaptive Frame × VLM 比較評価（人間確認結果含む） |
| `review_reports/release02_publish_restart_decision_20260626.md` | `??` | 公開再開判定レポート（PR043起点バッチ #2_030〜033）|
| `review_reports/commit_plan_adaptive_frame_20260626.md` | `??` | 本ファイル |

---

### ■ data（推奨: VLM結果 CSV のみ / 画像 PNG は除外）

| ディレクトリ | サイズ | 判定 | 理由 |
|-------------|--------|------|------|
| `data/vlm_runs/adaptive_poc_20260626/` | 132K（CSV 5件） | ✅ **含める** | VLM評価結果は再現不可（LLM出力）・意思決定の証拠 |
| `data/adaptive_frames/20260626/` | 82MB（PNG 135枚） | ❌ **除外推奨** | バイナリ・大容量・スクリプトで再生成可能 |
| `data/vlm_runs/phase2_5sample_20260626/` | 32K | ❌ **除外** | 本コミットスコープ外（前段階PoC） |

> `data/adaptive_frames/` を git 管理から永続除外したい場合は `.gitignore` に `data/adaptive_frames/` を追記することを推奨。

---

### ■ docs（変更なし・除外）

| ファイル | git状態 | 判定 |
|---------|---------|------|
| `docs/published_article_evolution_agent_v1.md` | committed（変更なし） | 除外 |
| `docs/media_inspector_ground_truth_v1.md` | committed（変更なし） | 除外 |

---

## 2. 除外一覧

| 除外対象 | 理由 |
|---------|------|
| `thumbnails/` | .gitignore 管理済み |
| `workflow.db` | .gitignore 管理済み |
| `review_logs/source_registry.csv` | 変更禁止（運用上の制約） |
| `metadata/` | .gitignore 管理済み（uap-csv-cache.csv）・変更禁止 |
| `published_articles/` | スコープ外 |
| `logs/notebooklm/` | スコープ外 |
| `note_drafts/*.bak` | バックアップ・不要 |
| `data/adaptive_frames/20260626/` | バイナリ大容量・再生成可能 |
| `data/vlm_runs/phase2_5sample_20260626/` | スコープ外（前段階PoC） |
| `scripts/publish_done.py` | M だが本コミットと無関係 |
| `note_drafts/` (PR043〜046 以外) | スコープ外（他記事の下書き） |
| `review_reports/codex_audit_*` | スコープ外（別イニシアチブ） |
| `review_reports/apply_article_template_*` | スコープ外 |
| `review_reports/commit_plan_vs_staged_diff_20260626.md` | スコープ外（別コミット計画） |
| `docs/release02_article_template_v1.md` | スコープ外 |

---

## 3. 推奨 git add コマンド

```bash
# scripts（新規）
git add scripts/extract_frames_adaptive.py
git add scripts/run_vlm_on_adaptive.py

# note_drafts（PR043〜046 のみ・.bak は含めない）
git add note_drafts/ai_summary_DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025_note_version.md
git add note_drafts/ai_summary_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_note_version.md
git add note_drafts/ai_summary_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_note_version.md
git add note_drafts/ai_summary_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md

# review_reports（Adaptive PoC 関連 4件）
git add review_reports/adaptive_frame_extraction_plan_20260626.md
git add review_reports/adaptive_frame_vlm_comparison_20260626.md
git add review_reports/release02_publish_restart_decision_20260626.md
git add review_reports/commit_plan_adaptive_frame_20260626.md

# data（VLM 結果 CSV のみ）
git add data/vlm_runs/adaptive_poc_20260626/
```

---

## 4. 推奨 commit message

```
feat: adopt adaptive frame extraction for Release02 VID pipeline (PR043-046)

- Add scripts/extract_frames_adaptive.py: 2s (<15s) / 3s (≥15s) interval,
  no max-frames cap (ADAPTIVE_RULES v1.1)
- Add scripts/run_vlm_on_adaptive.py: Qwen2.5-VL-7B batch runner via LM Studio
- PoC on PR043-046: 135 frames extracted, VLM evaluated (0–100% detection)
- Human review confirms VLM over-detects military UI overlays as UAP candidates
- Update note_drafts PR043-046 with Adaptive addendum (2026-06-26)
- Add decision report: PR043 batch (#2_030–#2_033) cleared for publication
```

> ユーザー指定の短縮版: `feat: adopt adaptive frame extraction for Release02 pipeline`
> ※ 詳細版を本文に持たせることを推奨。

---

## 5. 想定 staged ファイル数

| カテゴリ | ファイル数 |
|---------|-----------|
| scripts | 2 |
| note_drafts | 4 |
| review_reports | 4 |
| data/vlm_runs CSV | 5（ディレクトリ内） |
| **合計** | **15** |

> `data/adaptive_frames/` 135枚 PNG は除外のため git add しない。

---

## 6. 実行前確認チェックリスト

- [ ] `git add .` を**実行していない**こと
- [ ] `.bak` ファイルが staging に含まれていないこと（`git status --short` で確認）
- [ ] `thumbnails/` `workflow.db` `source_registry.csv` が staging に含まれていないこと
- [ ] `data/adaptive_frames/` の PNG が staging に含まれていないこと
- [ ] `note_drafts/` の PR043〜046 以外が含まれていないこと
- [ ] `git diff --cached` で差分を最終確認してからコミット

---

## 7. 推奨オプション: .gitignore 追記

`data/adaptive_frames/` を今後も管理外にする場合:

```
# Adaptive Frame 抽出画像（再生成可能・大容量バイナリ）
data/adaptive_frames/
```

（実施は別タスクで。本コミットには含めない）
