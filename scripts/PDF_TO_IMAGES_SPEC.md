# PDF_TO_IMAGES_SPEC

## 目的

raw_pdf フォルダ内のPDFを、ページごとのPNG画像に変換する。

## 影響範囲

- 読み込み元: raw_pdf/
- 出力先: page_images/
- 元PDFは変更しない
- 削除処理は行わない

## 作成するファイル

scripts/pdf_to_images.py

## 入力

raw_pdf/ に保存されたPDFファイル。

## 出力

PDFごとに page_images/ 内へサブフォルダを作成する。

例:

page_images/
└── 65_hs1-834228961_62-hq-83894_section_10/
    ├── page_0001.png
    ├── page_0002.png
    └── page_0003.png

## 完成条件

1. raw_pdf 内のPDFを検出できる
2. PDFごとにサブフォルダを作成する
3. 各ページを PNG として保存する
4. 元PDFファイル名は変更しない
5. エラー時に処理全体を止めず、エラー内容を表示する
6. Mac Studio のローカル環境で動作する
7. Python3 で実行できる
8. 文系非エンジニアでも再実行できる

## 非対象

- OCR
- 翻訳
- 要約
- note整形
- PDFの自動ダウンロード

## 実行イメージ

python3 scripts/pdf_to_images.py

## 注意点

- まずは1つのPDFで動作確認する
- 依存ライブラリが必要な場合は、インストール方法も明記する
- chmod 777 や root 実行は使わない
