# Claude Code 実行プロンプト：Text Layer Detection

以下の仕様書を確認した上で、
UAP公開文書 翻訳・要約プロジェクト用の
PDFテキストレイヤー検出ツールを実装してください。

## 参照必須ファイル

- PROJECT_SPEC.md
- scripts/TEXT_LAYER_DETECTION_SPEC.md
- classification/classification_schema.md

## 今回の実装対象

scripts/detect_text_layer.py

## 今回の目的

raw_pdf 配下のPDFについて、
ページごとにテキストレイヤーの有無を確認し、
OCRが必要かどうかを判定すること。

## 出力先

metadata/text_layer_report.csv

## 完成条件

- raw_pdf 内のPDFを検出できる
- ページごとにテキスト抽出を試行できる
- metadata/text_layer_report.csv を生成できる
- OCRが必要かどうかをページ単位で判定できる
- 元PDFは変更・削除しない
- エラー時も処理全体を止めず記録する
- Python3で実行できる

## 非対象

今回は以下を実装しない。

- OCR本文抽出
- 翻訳
- 要約
- note整形
- 外部API利用

## 判定方針

- 十分なテキストが埋め込まれているページ:
  - has_text_layer = true
  - ocr_needed = false

- テキストがない、または極端に少ないページ:
  - has_text_layer = false
  - ocr_needed = true

- テキストが少量だけあるページ:
  - has_text_layer = partial
  - ocr_needed = true

## 必須出力項目

CSVには以下を含めてください。

- pdf_file
- page_number
- has_text_layer
- extracted_char_count
- sample_text
- ocr_needed
- reason
- notes

## セキュリティ・運用ルール

- chmod 777 を使用しない
- root実行を前提にしない
- 元PDFを変更・削除しない
- 外部APIへPDFを送信しない
- 必要最小限の権限で動作する

## 必須報告

実装後、以下を報告してください。

1. 実装内容
2. 使用ライブラリ
3. 実行手順
4. 生成されたCSVのサンプル
5. 自己検証結果
6. 限界・今後改善すべき点

## 重要

このツールの目的は、OCRそのものではなく、
OCRが必要なページと不要なページを分けることです。
