# METADATA_DOWNLOADER_SPEC

## 目的

WAR.GOV/UFO に掲載されている公開ファイル一覧を取得し、
各ファイルのメタデータをCSV化する。

さらに、PDFファイルについては未取得のものだけ raw_pdf/ に保存する。

## 実装対象

scripts/fetch_war_gov_catalog.py

## 対象URL

https://www.war.gov/UFO/

## 入力

WAR.GOV/UFO の公開ページ。

## 出力

metadata/files_catalog.csv

## 出力項目

- file_name
- agency
- release_date
- incident_date
- incident_location
- file_type
- source_url
- download_url
- downloaded
- downloaded_at
- notes

## 基本方針

- まずはPDFを優先する
- 元ファイル名は変更しない
- 既に raw_pdf/ に存在するPDFは再ダウンロードしない
- メタデータ取得を優先する
- ダウンロードに失敗しても処理全体を止めない
- WAR.GOVのページ構造が変わる可能性を考慮する

## 完成条件

1. WAR.GOV/UFO の一覧ページへアクセスできる
2. ファイル名・Agency・Release Date・Incident Date・Incident Location・Type を取得できる
3. metadata/files_catalog.csv を生成できる
4. PDFファイルだけを判定できる
5. 未取得PDFだけ raw_pdf/ へ保存できる
6. 元ファイル名を変更しない
7. 取得日時を記録できる
8. エラー時も処理全体を止めず記録する
9. Python3で実行できる

## 非対象

今回は以下を実装しない。

- OCR
- 翻訳
- 要約
- note整形
- 動画・画像ファイルの処理
- 自動投稿

## 実装方針

まずWAR.GOV/UFOページ構造を調査する。

以下を確認する。

- 静的HTMLから一覧取得できるか
- ページ内にJSONデータが埋め込まれているか
- ダウンロードURLがHTML内に存在するか
- JavaScript描画が必要か
- Playwright等が必要か

最初は可能な限り requests / BeautifulSoup など軽量な方法を優先する。

静的取得が難しい場合のみ、Playwright等の利用を検討する。

## セキュリティ・運用ルール

- chmod 777 を使用しない
- root実行を前提にしない
- 必要最小限の権限で動作する
- 外部送信はWAR.GOVへの取得リクエストに限定する
- 元PDFを変更・削除しない
- 既存ファイルを上書きしない

## 実行イメージ

python3 scripts/fetch_war_gov_catalog.py

## 重要

このツールは、翻訳やOCRより前の入口処理である。

目的は、
「どのファイルが公開されているか」
「どれを取得済みか」
「どれを記事化候補にするか」
を管理することである。
