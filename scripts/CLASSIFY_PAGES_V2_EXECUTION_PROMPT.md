# Claude Code 実行プロンプト：classify_pages.py v2 改善

以下の仕様書と改善メモを確認した上で、
classify_pages.py の v2 改善を実装してください。

## 参照必須ファイル

- PROJECT_SPEC.md
- classification/classification_schema.md
- scripts/CLASSIFY_PAGES_SPEC.md
- scripts/CLASSIFY_PAGES_V2_NOTES.md
- extracted_text/ocr_results.csv

## 今回の目的

OCR実行結果から判明した failure pattern をもとに、
classify_pages.py の routing 精度を改善する。

今回の主目的は、
OCR精度100%ではなく、
「OCRしてはいけないページを減らすこと」です。

## 今回改善したい問題

### 1. typed_text 誤分類

typed_text と判定されたページの一部で、
OCR結果が0字になった。

OCR向きではないページが、
typed_text と誤判定されている可能性がある。

### 2. confidence の罠

OCR confidence が高くても、
抽出文字数が0字または極端に少ないケースがある。

confidence 単独では成功判定しない。

### 3. aged paper 問題

古い紙、黄ばみ、スタンプ、劣化、ノイズにより、
typed_text / mixed_annotation / admin_or_cover の判定が不安定になる。

### 4. newspaper layout 問題

新聞・雑誌切り抜きは文字数が多く抽出できても、
読み順が崩れる可能性が高い。

## 改善方針

- typed_text 判定条件を厳しくする
- OCR結果0字ページは review_required = true に格上げする
- confidence と extracted_char_count を組み合わせて評価する
- aged paper を typed_text と誤判定しないよう特徴量を調整する
- newspaper_or_print_clipping は review_required = true を優先する
- admin_or_cover は metadata extraction 寄りにする

## 実装対象

scripts/classify_pages.py

## 必須改善項目

- typed_text 判定改善
- aged paper 対応
- OCR failure page の review_required 強化
- confidence と文字数の複合判定
- processing_action 改善
- failure pattern 記録改善

## 非対象

今回は以下を実装しない。

- AI Vision分類
- 外部API利用
- 完全な新聞レイアウト解析
- 手書きOCR
- 翻訳
- 要約

## 完成条件

1. classify_pages.py v2 が動作する
2. OCR routing 精度が改善される
3. typed_text 誤分類が減少する
4. OCR failure page を review_required へ適切に送れる
5. classification/page_classification.csv を更新できる
6. エラー時も処理全体を止めず記録する

## 必須報告

実装後、以下を報告してください。

1. 改善内容
2. typed_text 誤分類改善結果
3. OCR成功率比較
4. aged paper 対応内容
5. review_required 改善内容
6. failure pattern 分析
7. 限界・今後改善すべき点

## 重要

分類精度100%は不要です。

目的は、
OCR routing を改善し、
review_queue を適切に作ることです。

「迷ったら review_required に寄せる」
方針で構いません。
