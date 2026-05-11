# TEXT_LAYER_DETECTION_SPEC

## 目的

raw_pdf 内のPDFについて、ページごとにテキストレイヤーの有無を確認し、
OCRが必要かどうかを判定する。

## 実装対象

scripts/detect_text_layer.py

## 参照必須ファイル

- PROJECT_SPEC.md
- scripts/PDF_TO_IMAGES_SPEC.md
- classification/classification_schema.md

## 入力

raw_pdf/ 配下のPDFファイル。

## 出力

metadata/text_layer_report.csv

## 出力項目

- pdf_file
- page_number
- has_text_layer
- extracted_char_count
- sample_text
- ocr_needed
- reason
- notes

## 判定方針

- PDF内に十分なテキストが埋め込まれている場合:
  - has_text_layer = true
  - ocr_needed = false

- テキストがない、または極端に少ない場合:
  - has_text_layer = false
  - ocr_needed = true

- テキストがあるが文字数が少ない場合:
  - has_text_layer = partial
  - ocr_needed = true
  - notes に「部分的なテキストレイヤーの可能性」と記録する

## 完成条件

1. raw_pdf 内のPDFを検出できる
2. ページごとにテキスト抽出を試行できる
3. metadata/text_layer_report.csv を生成できる
4. OCRが必要かどうかをページ単位で判定できる
5. 元PDFは変更・削除しない
6. エラー時も処理全体を止めず記録する
7. Python3で実行できる

## 非対象

今回は以下を実装しない。

- OCR本文抽出
- 翻訳
- 要約
- note整形
- 外部API利用

## 実行イメージ

python3 scripts/detect_text_layer.py

## セキュリティ・運用ルール

- chmod 777 を使用しない
- root実行を前提にしない
- 元PDFを変更・削除しない
- 外部APIへPDFを送信しない
- 必要最小限の権限で動作する
