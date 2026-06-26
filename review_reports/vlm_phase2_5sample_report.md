# VLM Phase 2 — 5-sample Category PoC Report

- 実施日時: 2026-06-26 06:45:10
- モデル: `qwen2.5-vl-7b-instruct`
- API: `http://127.0.0.1:1234/v1/chat/completions`
- 評価サンプル数: 5

## サマリー

| 指標 | 結果 |
|------|------|
| JSON parse 成功件数 | 5 / 5 |
| 平均応答時間 | 4.4s |
| E_known_miss_case 検出 | **OK** ✓ |
| C_no_visible_target 誤検出 | **誤検出なし** ✓ |
| D_sensor_ui_background 誤検出 | **誤検出なし** ✓ |

## 各サンプル詳細

### vlm_0002 — A_clear_candidate

- article_id: R02-025 / #2_025
- image: `data/vlm_eval_set/20260625/images/vlm_0002_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_frame_0000.png`
- response_time: 5.48s
- parse_success: True

**VLM JSON:**

```json
{
  "visible_candidate": true,
  "confidence": 0.7,
  "location": "中央やや右上",
  "description": "小さな光点、背景より明るい",
  "visual_confirmation_only": true,
  "speculation": false
}
```

### vlm_0005 — B_small_unclear

- article_id: R02-026 / #2_026
- image: `data/vlm_eval_set/20260625/images/vlm_0005_DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020_frame_0000.png`
- response_time: 5.34s
- parse_success: True

**VLM JSON:**

```json
{
  "visible_candidate": false,
  "confidence": 0.1,
  "location": "中央やや右上",
  "description": "不明瞭な形状、暗い背景と比較して若干明るい。",
  "visual_confirmation_only": true,
  "speculation": false
}
```

### vlm_0007 — C_no_visible_target

- article_id: R02-027 / #2_027
- image: `data/vlm_eval_set/20260625/images/vlm_0007_DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020_frame_0000.png`
- response_time: 5.34s
- parse_success: True

**VLM JSON:**

```json
{
  "visible_candidate": false,
  "confidence": 0.1,
  "location": "中央やや上部",
  "description": "不明瞭な形状、雲のような背景との区別困難",
  "visual_confirmation_only": true,
  "speculation": false
}
```

### vlm_0048 — D_sensor_ui_background

- article_id: R02-041 / #2_041
- image: `data/vlm_eval_set/20260625/images/vlm_0048_FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023_frame_0000.png`
- response_time: 5.22s
- parse_success: True

**VLM JSON:**

```json
{
  "visible_candidate": false,
  "confidence": 0.1,
  "location": "画像全体",
  "description": "暗い背景に浮かぶ不明瞭な形状",
  "visual_confirmation_only": true,
  "speculation": false
}
```

### vlm_0001 — E_known_miss_case

- article_id: R02-025 / #2_025
- image: `data/vlm_eval_set/20260625/images/vlm_0001_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_frame_0030.png`
- response_time: 0.83s
- parse_success: True

**VLM JSON:**

```json
{
  "visible_candidate": true,
  "confidence": 0.7,
  "location": "中央",
  "description": "不明瞭な光点、周囲に放射状のパターン",
  "visual_confirmation_only": true,
  "speculation": false
}
```

## 50枚評価への進行判断

- JSON parse 安定性: 5/5 (OK)
- 平均応答時間: 4.4s (OK (<30s))
- E_known_miss_case 検出: OK
- C/D 誤検出: OK（誤検出なし）

**→ 50枚評価に進む: YES**

## 出力ファイル

- `data/vlm_runs/phase2_5sample_20260626/results.csv`
- `data/vlm_runs/phase2_5sample_20260626/results.jsonl`
- `data/vlm_runs/phase2_5sample_20260626/raw_responses/`
- `data/vlm_runs/phase2_5sample_20260626/README.md`

