# Commit Plan vs Staged Files 突合レポート

- 作成日: 2026-06-26
- 参照: `review_reports/commit_plan_media_evolution_20260626.md`
- 参照: `git diff --cached --name-only`（72件）
- 突合方法: Python set演算（機械的照合）

---

## 結論サマリー

| 項目 | 結果 |
|------|------|
| plan記載・未stage | **0件（問題なし）** |
| stage済み・plan未記載 | **1件（下記参照）** |
| plan展開後ファイル数 | 71件 |
| stage済みファイル数 | 72件 |
| 差分 | **1件** |
| 想定外ファイルの混入 | なし |
| 除外対象（note_drafts/published_articles/source_registry/metadata/workflow.db）の混入 | **なし** |

---

## 1. commit planに記載されているが stage されていないファイル

```
なし
```

commit plan（セクションA+B）に記載された全ファイルはステージ済み。欠落なし。

---

## 2. stage済みだが commit plan（A+B）に記載されていないファイル

```
EXTRA: review_reports/commit_plan_media_evolution_20260626.md
```

**このファイルはステージに含めて問題ない。**
ユーザーが `git add` コマンドに明示的に指定したファイルであり、今回のcommitの作業記録として適切。
commit plan のセクションA/Bへの明示的な追記は不要（meta文書のため）。

---

## 3. 「69件」と「72件」の差分について

### 結論: 「69件」は集計ミスだった。正確な差分は **71 vs 72 = 1件**

| 段階 | 件数 | 説明 |
|------|------|------|
| commit plan セクションE git addコマンド | 17パス | ディレクトリ `data/vlm_runs/phase3_full50_20260626/` を1パスとして記載 |
| ユーザー git add 実行時の実際のパス | 18パス | `review_reports/commit_plan_media_evolution_20260626.md` を追加 |
| plan展開後（ディレクトリ→個別ファイル） | **71件** | 17パス → 55件（vlm_runs）+ 16件（その他） |
| stage済み実数 | **72件** | 71件 + commit_plan_media_evolution_20260626.md |

「69件」という数字は、以前の集計で `data/vlm_runs/phase3_full50_20260626/` を1件としてカウントしたことによる誤りだった。

---

## 4. data/vlm_runs/phase3_full50_20260626/ 配下の内訳（55件）

| 種別 | 件数 | 内容 |
|------|------|------|
| `raw_responses/vlm_XXXX_raw.txt` | **50件** | VLM生応答テキスト（vlm_0001〜vlm_0050） |
| `results.csv` | 1件 | VLM推論結果集計 |
| `results.jsonl` | 1件 | VLM推論詳細ログ（JSON Lines） |
| `score_summary.csv` | 1件 | F1スコアサマリー |
| `article_revision_candidates.csv` | 1件 | 修正候補CSV |
| `published_article_evolution.csv` | 1件 | Evolution判定CSV（R02-041: done） |
| **合計** | **55件** | |

---

## 5. raw_responses 50件をcommitに含めるべきか

### 現在の状態
- 50件すべてがステージ済み（`data/vlm_runs/phase3_full50_20260626/` を丸ごと add したため）
- commit plan には `raw_responses/ — 生応答JSON` と記載あり（明示的に除外していない）
- 容量: 200KB（git的に問題ない範囲）

### 含める場合のメリット
- Phase 3 実行の完全な再現記録になる
- 将来のモデル比較・再評価時に元応答を参照できる
- 容量は200KBで軽量

### 除外する場合のメリット
- commit がすっきりする（55件 → 5件）
- raw応答はログとしての性格が強く、成果物ではない
- `results.csv` / `results.jsonl` があれば再現性は十分

### 判断

`raw_responses/` 50件については **ユーザーの判断を仰ぐ**。

- **含める（現状のまま）**: 容量軽量・完全記録として適切
- **除外する**: `git restore --staged data/vlm_runs/phase3_full50_20260626/raw_responses/` で取り消し可能

---

## ステージ済みファイル完全リスト（72件）

```
data/vlm_eval_set/20260625/ground_truth.csv                          ← A-3
data/vlm_runs/phase3_full50_20260626/article_revision_candidates.csv ← A-3
data/vlm_runs/phase3_full50_20260626/published_article_evolution.csv ← A-3
data/vlm_runs/phase3_full50_20260626/raw_responses/vlm_0001_raw.txt ← A-3
  ... (vlm_0002 〜 vlm_0049 略)
data/vlm_runs/phase3_full50_20260626/raw_responses/vlm_0050_raw.txt ← A-3
data/vlm_runs/phase3_full50_20260626/results.csv                     ← A-3
data/vlm_runs/phase3_full50_20260626/results.jsonl                   ← A-3
data/vlm_runs/phase3_full50_20260626/score_summary.csv               ← A-3
docs/media_inspector_ground_truth_v1.md                              ← A-2
docs/published_article_evolution_agent_v1.md                         ← A-2
review_reports/article_revision_candidates_20260626.md               ← A-4
review_reports/article_revision_high6_confirmed_20260626.md          ← A-4
review_reports/commit_plan_media_evolution_20260626.md               ← ★ plan未記載・問題なし
review_reports/published_article_evolution_plan_20260626.md          ← A-4
review_reports/published_article_evolution_report_20260626.md        ← A-4
review_reports/r02_041_note_update_diff_20260626.md                  ← B
review_reports/vlm_connection_test.md                                ← B
review_reports/vlm_phase2_5sample_report.md                          ← B
review_reports/vlm_phase3_full50_report.md                           ← B
review_reports/vlm_phase3_human_review_targets.md                    ← B
review_reports/vlm_score_qwen2_5_vl_7b_20260626.md                  ← A-4
scripts/article_revision_candidate.py                                ← A-1
scripts/published_article_evolution.py                               ← A-1
scripts/score_vlm_vs_ground_truth.py                                 ← A-1
```

---

## 次のアクション

| 選択肢 | コマンド |
|--------|---------|
| raw_responses を除外してcommit | `git restore --staged data/vlm_runs/phase3_full50_20260626/raw_responses/` → commit |
| 現状のまま（raw_responses込み72件）でcommit | そのままcommit |
