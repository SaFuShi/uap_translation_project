# VLM Score Report — qwen2.5-vl-7b-instruct

- 実施日時: 2026-06-26 07:26:51
- モデル: `qwen2.5-vl-7b-instruct`
- run_id: `phase3_full50_20260626`
- ground_truth: `data/vlm_eval_set/20260625/ground_truth.csv`
- results: `data/vlm_runs/phase3_full50_20260626/results.csv`
- score_csv: `data/vlm_runs/phase3_full50_20260626/score_summary.csv`

---

## 1. Gold スコア（人間目視 ground truth 7件）

Ground truth に登録された 7 件中 7 件が results.csv と突合できた。

### Overall

| scope | n | TP | FP | TN | FN | Precision | Recall | F1 |
|-------|---|----|----|----|----|-----------|--------|----|
| overall (gold) | 7 | 6 | 1 | 0 | 0 | 85.7% | 100.0% | 92.3% |

### Category 別（gold）

| category | n | TP | FP | TN | FN | Precision | Recall | F1 |
|----------|---|----|----|----|----|-----------|--------|----|
| C_no_visible_target | 6 | 5 | 1 | 0 | 0 | 83.3% | 100.0% | 90.9% |
| D_sensor_ui_background | 1 | 1 | 0 | 0 | 0 | 100.0% | 100.0% | 100.0% |

### comparison_label 分布（gold）

| comparison_label | 件数 |
|-----------------|------|
| Partial Match | 3 |
| Match | 3 |
| Description Gap | 1 |
| False Positive | 1 |
| Acceptable | 1 |
| Missed Secondary Objects | 1 |

### human_verdict 分布

| human_verdict | 件数 |
|--------------|------|
| label_error | 6 |
| false_positive | 1 |

### 詳細指標（gold）

- description_gap 件数: 1
- missed_secondary_objects 件数: 1
- label_error 件数: 6
- review_required 件数: 6

---

## 2. Proxy スコア（カテゴリラベルを正解とした全50件）

B_small_unclear (20 件) は ambiguous のため除外。30 件でスコアを算出。

### Overall

| scope | n | TP | FP | TN | FN | Precision | Recall | F1 |
|-------|---|----|----|----|----|-----------|--------|----|
| overall (proxy) | 30 | 12 | 7 | 11 | 0 | 63.2% | 100.0% | 77.4% |

### Category 別（proxy）

| category | n | TP | FP | TN | FN | Precision | Recall | F1 |
|----------|---|----|----|----|----|-----------|--------|----|
| A_clear_candidate | 11 | 11 | 0 | 0 | 0 | 100.0% | 100.0% | 100.0% |
| C_no_visible_target | 15 | 0 | 6 | 9 | 0 | 0.0% | 0.0% | 0.0% |
| D_sensor_ui_background | 3 | 0 | 1 | 2 | 0 | 0.0% | 0.0% | 0.0% |
| E_known_miss_case | 1 | 1 | 0 | 0 | 0 | 100.0% | 100.0% | 100.0% |

---

## 3. サンプル別詳細（gold 7件）

| sample_id | category | human_visible | vlm_visible | human_conf | vlm_conf | human_verdict | comparison_label |
|-----------|----------|---------------|-------------|------------|----------|---------------|-----------------|
| vlm_0019 | C_no_visible_target | True | True | 0.6 | 0.7 | label_error | Partial Match / Description Gap |
| vlm_0021 | C_no_visible_target | False | True | 0.9 | 0.7 | false_positive | False Positive / Acceptable |
| vlm_0033 | C_no_visible_target | True | True | 0.6 | 0.7 | label_error | Partial Match |
| vlm_0045 | C_no_visible_target | True | True | 0.9 | 0.7 | label_error | Match |
| vlm_0046 | C_no_visible_target | True | True | 0.85 | 0.7 | label_error | Match |
| vlm_0047 | C_no_visible_target | True | True | 0.8 | 0.7 | label_error | Match |
| vlm_0049 | D_sensor_ui_background | True | True | 0.9 | 0.8 | label_error | Partial Match / Missed Secondary Objects |

---

## 4. 総合評価

- Gold F1: **92.3%** (Precision 85.7% / Recall 100.0%)
- Proxy F1: **77.4%**
- C_no_visible_target 誤検出（proxy）: 6 件
  （うち label_error 確定: 6 件）
- D_sensor_ui_background 誤検出（proxy）: 1 件

**→ 判定: 良好。次モデル比較へ進める。**

### 次モデル比較時の基準

- 同一 ground_truth.csv を使用
- Gold F1 がこのスコアを上回るか確認
- missed_secondary_objects の改善（特に vlm_0049 の赤い光源2個）
- C/D 誤検出率の低減

