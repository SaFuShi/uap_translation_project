# VLM Connection Test Report

- 実施日時: 2026-06-26 06:37:29
- 対象画像: `data/vlm_eval_set/20260625/images/vlm_0001_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_frame_0030.png`
- API: `http://127.0.0.1:1234/v1/chat/completions`
- モデル: `qwen2.5-vl-7b-instruct`
- 応答時間: 6.1s

## 接続テスト結果

- **API接続: OK**

## VLM JSON 出力

- **JSON出力: OK**

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

## フィールド確認

- `visible_candidate`: True — OK
- `confidence`: 0.7 — OK
- `location`: 中央 — OK
- `visual_confirmation_only`: True — OK
- `speculation`: False — OK

## 既知見落としフレーム検出評価

- カテゴリ: E_known_miss_case（人間が見落としを発見した既知ケース）
- 期待: VLMが対象物を検出できるか
- visible_candidate: True
- confidence: 0.7

**→ VLMは対象物を検出できた（見落としなし）**

## API レスポンス詳細

- model: qwen2.5-vl-7b-instruct
- prompt_tokens: 2983
- completion_tokens: 61
- finish_reason: stop

