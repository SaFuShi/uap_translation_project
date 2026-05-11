# CLASSIFY_PAGES_V2_NOTES

## 目的

OCR実行結果から判明した失敗パターンをもとに、
classify_pages.py の分類・routing精度を改善する。

## 現在の問題

### 1. typed_text 誤分類

typed_text と判定されたページの一部で、
OCR結果が0字になるケースが確認された。

これは、ページ分類が「OCR向き」と判定していても、
実際にはOCR対象として不適切なページが含まれている可能性を示す。

### 2. confidence の罠

OCRの confidence が高くても、
抽出文字数が0字または極端に少ないケースがある。

そのため、confidence だけで成功判定しない。

### 3. aged paper 問題

古い紙、黄ばみ、スタンプ、劣化、ノイズにより、
typed_text / mixed_annotation / admin_or_cover の判定が不安定になる。

### 4. newspaper layout 問題

新聞・雑誌切り抜きは文字数が多く抽出できても、
読み順が崩れる可能性が高い。

## v2改善方針

- typed_text 判定を厳しくする
- OCR結果0字のページは review_required = true に格上げする
- confidence と extracted_char_count を組み合わせて評価する
- aged paper を typed_text と誤判定しないよう特徴量を調整する
- newspaper_or_print_clipping は原則 review_required = true とする
- admin_or_cover は本文OCRではなく metadata extraction に寄せる

## 成功判定の考え方

OCR成功は confidence だけで判断しない。

以下を組み合わせて判断する。

- extracted_char_count
- confidence_estimate
- classification
- processing_action
- review_required
- notes

## 次の実装候補

1. classify_pages.py の typed_text 判定条件を改善
2. run_ocr.py 側で 0字抽出を failure として記録
3. ocr_results.csv から failure_cases.csv を生成
4. routing改善前後でOCR成功率を比較
