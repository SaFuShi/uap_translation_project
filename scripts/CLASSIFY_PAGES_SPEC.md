# CLASSIFY_PAGES_SPEC

## 目的

page_images に生成されたPNGページ画像を仮分類し、
OCR・翻訳処理へ進めるための処理ルートを決める。

この分類は、分類自体が目的ではなく、
OCR精度を高め、人間確認を最小化するために行う。

## 実装対象

scripts/classify_pages.py

## 参照必須ファイル

- PROJECT_SPEC.md
- classification/classification_schema.md

## 入力

page_images/ 配下のPNGファイル。

例:

page_images/
└── 65_hs1-834228961_62-hq-83894_section_10/
    ├── page_0001.png
    ├── page_0002.png
    └── page_0003.png

## 出力

classification/page_classification.csv

## 出力項目

- pdf_file
- page_number
- image_file
- classification
- confidence
- ocr_recommended
- processing_action
- review_required
- reason
- notes

## 分類カテゴリ

- typed_text
- handwritten
- newspaper_or_print_clipping
- mixed_annotation
- image_or_photo
- admin_or_cover
- unreadable

## processing_action

- run_ocr
- try_ocr
- try_layout_ocr
- try_vision_or_review
- extract_metadata
- skip_ocr
- skip_and_record

## 基本方針

- まずは仮分類でよい
- 判断に迷うページは review_required = true にする
- OCR可能性があるページは、分類で止めず一度OCRへ回す
- 手書き中心ページは通常OCRの主対象にしない
- タイプ文書に手書きメモが混在する場合は mixed_annotation とする
- 人間確認は失敗・低信頼・判読困難ページに限定する

## 完成条件

1. page_images 配下のPNGを検出できる
2. PDFごとのサブフォルダ構造を維持して処理できる
3. ページごとに仮分類できる
4. classification/page_classification.csv を生成できる
5. processing_action と review_required を出力できる
6. エラー時も処理全体を止めず記録する
7. Python3で実行できる
8. 元画像ファイルは変更・削除しない

## 非対象

今回は以下を実装しない。

- OCR本文抽出
- 翻訳
- 要約
- note整形
- 完全な画像理解AI分類
- 外部API利用

## 実装方針

最初は完全なAI画像分類ではなく、
画像サイズ・縦横比・明暗・文字密度などの簡易特徴量と、
ファイル構造をもとにした仮分類でよい。

分類精度よりも、
次工程へ進めるための routing 情報を残すことを優先する。

## セキュリティ・運用ルール

- chmod 777 を使用しない
- root実行を前提にしない
- 元画像を変更・削除しない
- 外部APIへ画像を送信しない
- 必要最小限の権限で動作する

## 実行イメージ

python3 scripts/classify_pages.py
