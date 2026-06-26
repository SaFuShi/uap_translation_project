# VLM Phase 3 — Full 50-sample Evaluation Report

- 実施日時: 2026-06-26 06:53:46
- モデル: `qwen2.5-vl-7b-instruct`
- API: `http://127.0.0.1:1234/v1/chat/completions`
- 評価サンプル数: 50
- 合計処理時間: 232s (3.9分)

## サマリー

| 指標 | 結果 |
|------|------|
| JSON parse 成功件数 | 50 / 50 (100%) |
| 平均応答時間 | 4.6s |
| visible_candidate=true 件数 | 24 / 50 |
| E_known_miss_case 検出 | 1/1 **OK** ✓ |
| C_no_visible_target 誤検出 | 6/15 **誤検出 6件** ✗ |
| D_sensor_ui_background 誤検出 | 1/3 **誤検出 1件** ✗ |

## カテゴリ別 visible_candidate 件数

| category | samples | visible=true | visible=false | parse_fail |
|----------|---------|--------------|---------------|------------|
| A_clear_candidate | 11 | 11 | 0 | 0 |
| B_small_unclear | 20 | 5 | 15 | 0 |
| C_no_visible_target | 15 | 6 | 9 | 0 |
| D_sensor_ui_background | 3 | 1 | 2 | 0 |
| E_known_miss_case | 1 | 1 | 0 | 0 |

## confidence 分布

- high (≥0.7): 24件
- mid  (0.3–0.69): 0件
- low  (<0.3): 26件

## E_known_miss_case 詳細

- vlm_0001 | visible=True | conf=0.75 | 不明瞭な輝点、周囲に放射状のパターン

## C_no_visible_target 誤検出一覧

- vlm_0019 | R02-031 | conf=0.7 | 不明瞭な形状の暗い物体、背景との明確な区別は困難。
- vlm_0021 | R02-031 | conf=0.7 | 不明瞭な黒い形状、背景との明確な区別は難しい。
- vlm_0033 | R02-036 | conf=0.7 | 白い線と点の集合、背景との明確な区別
- vlm_0045 | R02-040 | conf=0.7 | 赤い線状の光、背景との明確な区別あり。
- vlm_0046 | R02-040 | conf=0.7 | 小さな光点、背景と明確に区別できる
- vlm_0047 | R02-040 | conf=0.7 | 赤い光点、周囲は暗く、背景との明確な区別

## D_sensor_ui_background 誤検出一覧

- vlm_0049 | R02-041 | conf=0.8 | 黄色い球体、背景に星が見える

## 失敗画像一覧

- なし

## 次フェーズ進行判断

- JSON parse 安定性: 100% (OK)
- 平均応答時間: 4.6s (OK)
- E 検出率: 1/1 (OK)
- C 誤検出: 6件 (NG)
- D 誤検出: 1件 (OK)

**→ 次フェーズへ進む: REVIEW NEEDED**

## 全サンプル結果

| sample_id | category | article_id | visible | conf | parse | location |
|-----------|----------|------------|---------|------|-------|----------|
| vlm_0001 | E_known_miss_case | R02-025 | True | 0.75 | True | 中央 |
| vlm_0002 | A_clear_candidate | R02-025 | True | 0.7 | True | 中央やや右上 |
| vlm_0003 | A_clear_candidate | R02-025 | True | 0.7 | True | 中央やや下 |
| vlm_0004 | A_clear_candidate | R02-025 | True | 0.7 | True | 中央やや下 |
| vlm_0005 | B_small_unclear | R02-026 | False | 0.1 | True | 中央やや右上 |
| vlm_0006 | B_small_unclear | R02-026 | False | 0.1 | True | 中央やや右上 |
| vlm_0007 | C_no_visible_target | R02-027 | False | 0.1 | True | 中央やや上部 |
| vlm_0008 | C_no_visible_target | R02-027 | False | 0.1 | True | 中央 |
| vlm_0009 | C_no_visible_target | R02-027 | False | 0.1 | True | 中央やや下 |
| vlm_0010 | B_small_unclear | R02-028 | False | 0.1 | True | 中央やや右上 |
| vlm_0011 | B_small_unclear | R02-028 | False | 0.1 | True | 中央やや左上 |
| vlm_0012 | B_small_unclear | R02-028 | False | 0.1 | True | 中央やや右上 |
| vlm_0013 | B_small_unclear | R02-029 | False | 0.1 | True | 中央やや下 |
| vlm_0014 | B_small_unclear | R02-029 | False | 0.1 | True | 中央やや上部 |
| vlm_0015 | B_small_unclear | R02-029 | False | 0.1 | True | 中央やや下 |
| vlm_0016 | C_no_visible_target | R02-030 | False | 0.1 | True | 中央やや左上 |
| vlm_0017 | C_no_visible_target | R02-030 | False | 0.1 | True | 中央やや左上 |
| vlm_0018 | C_no_visible_target | R02-030 | False | 0.1 | True | 中央やや左上 |
| vlm_0019 | C_no_visible_target | R02-031 | True | 0.7 | True | 中央 |
| vlm_0020 | C_no_visible_target | R02-031 | False | 0.1 | True | 中央やや左上 |
| vlm_0021 | C_no_visible_target | R02-031 | True | 0.7 | True | 中央 |
| vlm_0022 | B_small_unclear | R02-032 | True | 0.75 | True | 中央上部 |
| vlm_0023 | B_small_unclear | R02-032 | True | 0.8 | True | 中央上部 |
| vlm_0024 | B_small_unclear | R02-032 | True | 0.8 | True | 中央上部 |
| vlm_0025 | A_clear_candidate | R02-033 | True | 0.7 | True | 中央やや右上 |
| vlm_0026 | A_clear_candidate | R02-033 | True | 0.7 | True | 中央やや上部 |
| vlm_0027 | B_small_unclear | R02-034 | False | 0.1 | True | 中央 |
| vlm_0028 | B_small_unclear | R02-034 | False | 0.1 | True | 中央 |
| vlm_0029 | B_small_unclear | R02-034 | True | 0.7 | True | 中央 |
| vlm_0030 | B_small_unclear | R02-035 | False | 0.1 | True | 中央やや上部 |
| vlm_0031 | B_small_unclear | R02-035 | False | 0.1 | True | 中央やや上部 |
| vlm_0032 | B_small_unclear | R02-035 | False | 0.1 | True | 中央やや上部 |
| vlm_0033 | C_no_visible_target | R02-036 | True | 0.7 | True | 中央 |
| vlm_0034 | C_no_visible_target | R02-036 | False | 0.1 | True | 右上 |
| vlm_0035 | C_no_visible_target | R02-036 | False | 0.1 | True | 右上 |
| vlm_0036 | B_small_unclear | R02-037 | False | 0.1 | True | 中央やや下 |
| vlm_0037 | B_small_unclear | R02-037 | True | 0.7 | True | 中央やや下 |
| vlm_0038 | B_small_unclear | R02-037 | False | 0.1 | True | 画面右上 |
| vlm_0039 | A_clear_candidate | R02-038 | True | 0.7 | True | 中央やや上 |
| vlm_0040 | A_clear_candidate | R02-038 | True | 0.7 | True | 中央やや右上 |
| vlm_0041 | A_clear_candidate | R02-038 | True | 0.7 | True | 中央やや左上 |
| vlm_0042 | A_clear_candidate | R02-039 | True | 0.7 | True | 中央上部 |
| vlm_0043 | A_clear_candidate | R02-039 | True | 0.7 | True | 中央やや上部 |
| vlm_0044 | A_clear_candidate | R02-039 | True | 0.7 | True | 中央やや左上 |
| vlm_0045 | C_no_visible_target | R02-040 | True | 0.7 | True | 中央上部 |
| vlm_0046 | C_no_visible_target | R02-040 | True | 0.7 | True | 中央やや左上 |
| vlm_0047 | C_no_visible_target | R02-040 | True | 0.7 | True | 中央やや上部 |
| vlm_0048 | D_sensor_ui_backgrou | R02-041 | False | 0.1 | True | 画像全体 |
| vlm_0049 | D_sensor_ui_backgrou | R02-041 | True | 0.8 | True | 右上 |
| vlm_0050 | D_sensor_ui_backgrou | R02-042 | False | 0.1 | True | 画像全体 |

## 出力ファイル

- `data/vlm_runs/phase3_full50_20260626/results.csv`
- `data/vlm_runs/phase3_full50_20260626/results.jsonl`
- `data/vlm_runs/phase3_full50_20260626/raw_responses/` (50件)

