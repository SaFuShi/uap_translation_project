# Claude Code 実行プロンプト：Metadata Downloader

以下の仕様書を確認した上で、
UAP公開文書 翻訳・要約プロジェクト用の
WAR.GOV/UFO メタデータ取得・PDFダウンロードツールを実装してください。

## 参照必須ファイル

- PROJECT_SPEC.md
- scripts/METADATA_DOWNLOADER_SPEC.md

## 今回の実装対象

scripts/fetch_war_gov_catalog.py

## 今回の目的

WAR.GOV/UFO に掲載されている公開ファイル一覧を取得し、
各ファイルのメタデータを metadata/files_catalog.csv に保存する。

さらに、PDFファイルについては、
未取得のものだけ raw_pdf/ に保存する。

## 対象URL

https://www.war.gov/UFO/

## 重要な実装方針

まず大量ダウンロードではなく、
ページ構造の調査を優先してください。

以下を確認してください。

- 静的HTMLから一覧取得できるか
- ページ内にJSONデータが埋め込まれているか
- ダウンロードURLがHTML内に存在するか
- JavaScript描画が必要か
- Playwright等が必要か

最初は requests / BeautifulSoup など軽量な方法を優先してください。
静的取得が難しい場合のみ、Playwright等の利用を検討してください。

## 出力先

metadata/files_catalog.csv

## 必須出力項目

CSVには以下を含めてください。

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

## セキュリティ・運用ルール

- chmod 777 を使用しない
- root実行を前提にしない
- 必要最小限の権限で動作する
- 外部送信はWAR.GOVへの取得リクエストに限定する
- 元PDFを変更・削除しない
- 既存ファイルを上書きしない
- 大量アクセスにならないよう配慮する

## 必須報告

実装後、以下を報告してください。

1. ページ構造の調査結果
2. 実装内容
3. 使用ライブラリ
4. 実行手順
5. 生成されたCSVサンプル
6. ダウンロード結果
7. エラー・限界・今後改善すべき点

## 重要

このツールは、翻訳やOCRより前の入口処理です。

目的は、
「どのファイルが公開されているか」
「どれを取得済みか」
「どれを記事化候補にするか」
を管理することです。
