# Claude Code 実行プロンプト：OCR Execution

以下の仕様書を確認した上で、
UAP公開文書 翻訳・要約プロジェクト用の
OCR実行ツールを実装してください。

## 参照必須ファイル

- PROJECT_SPEC.md
- classification/classification_schema.md
- scripts/CLASSIFY_PAGES_SPEC.md
- scripts/TEXT_LAYER_DETECTION_SPEC.md
- scripts/OCR_EXECUTION_SPEC.md

## 今回の実装対象

scripts/run_ocr.py

## 今回の目的

Page Classification と Text Layer Detection の結果を利用し、
OCR対象ページについて本文抽出を行う。

このフェーズでは、
typed_text を主対象として、
OCR精度・失敗パターン・routing妥当性を検証する。

## 入力

- classification/page_classification.csv
- metadata/text_layer_report.csv
- page_images/**/*.png

## 出力

extracted_text/ocr_results.csv

## OCR対象条件

以下を満たすページをOCR対象とする。

- ocr_needed = true
- classification = typed_text
  または
- processing_action = run_ocr
  または
- processing_action = try_ocr

## 非対象

今回は以下をOCR対象にしない。

- handwritten
- image_or_photo
- unreadable

また、
newspaper_or_print_clipping は
本格対応前のため限定対応とする。

## 必須出力項目

CSVには以下を含めてください。

- pdf_file
- page_number
- image_file
- classification
- ocr_engine
- extracted_text
- extracted_char_count
- confidence_estimate
- review_required
- reason
- notes

## OCR方針

まずは typed_text を主対象とする。

mixed_annotation は、
本文抽出を優先し、
スタンプ・手書き注釈は無理に読まない。

newspaper_or_print_clipping は、
レイアウト崩れが発生する可能性があるため、
review_required = true を推奨する。

## OCRエンジン

まずはローカルOCRを優先する。

候補:
- Tesseract OCR
- pytesseract

## 完成条件

1. OCR対象ページを抽出できる
2. OCR本文抽出できる
3. extracted_text/ocr_results.csv を生成できる
4. review_required を適切に設定できる
5. エラー時も処理全体を止めず記録する
6. Python3で実行できる
7. 元画像ファイルを変更・削除しない

## 非対象

今回は以下を実装しない。

- 翻訳
- 要約
- note整形
- 外部API OCR
- 完全な新聞レイアウトOCR
- 高度な手書きOCR

## セキュリティ・運用ルール

- chmod 777 を使用しない
- root実行を前提にしない
- 元画像を変更・削除しない
- 外部APIへ画像送信しない
- 必要最小限の権限で動作する

## 必須報告

実装後、以下を報告してください。

1. 実装内容
2. 使用ライブラリ
3. 実行手順
4. OCR結果サンプル
5. 自己検証結果
6. OCR破綻パターン
7. 今後改善すべき点

## 重要

このフェーズでは、
OCR精度100%ではなく、
「どのページでOCRが破綻するか」
を把握することを重視する。

失敗ページを review_required として蓄積し、
routing改善へ繋げてください。
