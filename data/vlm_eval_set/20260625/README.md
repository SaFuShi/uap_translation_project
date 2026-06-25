# VLM Evaluation Set

## Purpose

Mac Studio上のローカルVLM候補を、同一のUAPフレーム画像セットで比較するための評価セットです。

## Categories

- A_clear_candidate: UAPらしき対象が比較的明確に映っている可能性があるフレーム (11 samples)
- B_small_unclear: 小さい点・輝点・黒点・不鮮明対象の可能性があるフレーム (20 samples)
- C_no_visible_target: 対象が見えない、または地形・建物・センサー画面のみの可能性があるフレーム (15 samples)
- D_sensor_ui_background: センサーUI、地形、建物、雲、海面など背景理解用 (3 samples)
- E_known_miss_case: 人間が見落としを発見した既知ケース (1 samples)

## Evaluation Method

1. `manifest.csv` または `manifest.json` の順に `images/` 配下の画像をローカルVLMへ渡す。
2. 各モデルの出力を sample_id 単位で保存する。
3. 対象物の有無、位置説明、背景/UIとの区別、不確実性表現を比較する。
4. `expected_human_label` は初期値 `TBD` のため、人間確認後に補正する。

## Suggested Prompt

> この画像をUAP動画フレームとして観察してください。対象物候補が見えるか、位置、形状、明るさ、背景/センサーUIとの区別、不確実性を日本語で簡潔に答えてください。断定できない場合は断定しないでください。

## Notes

- このセットは rule-based placeholder ラベルで作成されており、正解ラベルではありません。
- 元画像、note_drafts、workflow.db、source_registry.csv は変更していません。
- S_CLASS レコードは除外対象です。
- 外部API評価ではなく、ローカルVLM比較用です。

## Human Label Correction

`manifest.csv` の `expected_human_label` を `visible_candidate`, `small_unclear`, `not_visible`, `ui_background`, `known_miss` などに手動更新してください。補足は `notes` に追記します。
