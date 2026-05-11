# Claude Code 実行プロンプト：Page Classification

以下の仕様書を確認した上で、
UAP公開文書 翻訳・要約プロジェクト用の
ページ仮分類ツールを実装してください。

## 参照必須ファイル

- PROJECT_SPEC.md
- classification/classification_schema.md
- scripts/CLASSIFY_PAGES_SPEC.md

## 今回の実装対象

scripts/classify_pages.py

## 今回の目的

page_images 配下のPNGページ画像を読み取り、
OCR・翻訳処理へ進めるための仮分類と処理ルートをCSVへ出力すること。

## 出力先

classification/page_classification.csv

## 完成条件

- page_images 配下のPNGを検出できる
- PDFごとのサブフォルダ構造を維持して処理できる
- ページごとに仮分類できる
- classification/page_classification.csv を生成できる
- processing_action と review_required を出力できる
- エラー時も処理全体を止めず記録する
- Python3で実行できる
- 元画像ファイルは変更・削除しない

## 非対象

今回は以下を実装しない。

- OCR本文抽出
- 翻訳
- 要約
- note整形
- 完全な画像理解AI分類
- 外部API利用

## 実装方針

最初は完全なAI分類ではなく、
画像サイズ・縦横比・明暗・文字密度などの簡易特徴量を使った
軽量な仮分類でよい。

分類精度100%ではなく、
次工程へ進めるための routing 情報を残すことを優先してください。

## 必須出力項目

CSVには以下を含めてください。

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

## 重要な考え方

分類は目的ではありません。
OCR精度を高めるための前処理です。

判断に迷うページは review_required = true とし、
OCR可能性があるページは処理を止めず try_ocr または try_layout_ocr に回してください。

## セキュリティ・運用ルール

- chmod 777 を使用しない
- root実行を前提にしない
- 元画像を変更・削除しない
- 外部APIへ画像を送信しない
- 必要最小限の権限で動作する

## 必須報告

実装後、以下を報告してください。

1. 実装内容
2. 使用ライブラリ
3. 実行手順
4. 生成されたCSVのサンプル
5. 自己検証結果
6. 限界・今後改善すべき点
