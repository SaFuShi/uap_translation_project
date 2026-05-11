# Page Classification Schema

## 目的

この分類は、ページを整理すること自体が目的ではなく、
OCR・翻訳・要約の処理ルートを切り替えるために行う。

## 基本方針

- 分類は最初から細かくしすぎない
- 判断に迷う場合は mixed_annotation または unreadable に寄せる
- 分類結果には、必ず理由とOCR推奨可否を残す
- 今後別形式の文書が出た場合は分類を追加する

## 分類カテゴリ

### typed_text

タイプされた英文が中心のページ。

OCR推奨: true

例:
- 通常の報告書
- 手紙
- メモランダム
- タイプライター文書

### handwritten

手書き文字が中心のページ。

OCR推奨: false

理由:
通常OCRでは精度が低いため、LLM画像理解や手動確認を優先する。

### newspaper_or_print_clipping

新聞・雑誌・切り抜きなど、段組や見出しがあるページ。

OCR推奨: conditional

理由:
通常OCRでは読み順が崩れる可能性があるため、レイアウト認識が必要。

### mixed_annotation

タイプ文書に手書き注釈・スタンプ・赤字・管理番号などが混在するページ。

OCR推奨: conditional

理由:
本文OCRは可能だが、注釈やスタンプを本文と分ける必要がある。

### image_or_photo

写真・図版・映像キャプチャ・地図などが中心のページ。

OCR推奨: false

理由:
文字抽出よりも画像説明・メタデータ抽出を優先する。

### admin_or_cover

表紙・管理票・ファイル管理ページ。

OCR推奨: metadata_only

理由:
本文翻訳よりも、ケース番号・機関名・公開情報などのメタデータ抽出を優先する。

### unreadable

文字が潰れている、低解像度、破損、極端に薄いなど判読困難なページ。

OCR推奨: false

理由:
誤認識リスクが高いため、無理に翻訳しない。

## 出力項目

分類結果は、ページごとに以下を記録する。

- pdf_file
- page_number
- image_file
- classification
- confidence
- ocr_recommended
- reason
- notes

## OCRルーティング方針

- typed_text:
  通常OCRへ送る

- newspaper_or_print_clipping:
  レイアウト認識対応OCR、またはLLM画像理解へ送る

- mixed_annotation:
  本文OCRと注釈抽出を分ける

- handwritten:
  通常OCRではなくLLM画像理解または人間確認へ送る

- image_or_photo:
  OCRせず画像説明へ送る

- admin_or_cover:
  本文翻訳ではなくメタデータ抽出へ送る

- unreadable:
  処理対象外として記録する

## 自動処理優先ルール

このプロジェクトでは、人間確認を最小化するため、
分類後すぐに人間確認へ回すのではなく、
可能なページは一度自動処理を試す。

### 追加出力項目

分類結果には以下も追加する。

- processing_action
- review_required

### processing_action の種類

- run_ocr:
  通常OCRを実行する

- try_ocr:
  OCR可能性があるため一度OCRを試す

- try_layout_ocr:
  新聞・雑誌切り抜きなど、レイアウトを意識したOCRを試す

- try_vision_or_review:
  手書き中心など、通常OCRでは難しいためLLM画像理解または人間確認へ回す

- extract_metadata:
  表紙・管理票からメタデータ抽出を行う

- skip_ocr:
  OCRせず記録のみ行う

- skip_and_record:
  判読困難として記録する

### 自動ルーティング方針

- typed_text:
  processing_action = run_ocr
  review_required = false

- mixed_annotation:
  processing_action = try_ocr
  review_required = true

- newspaper_or_print_clipping:
  processing_action = try_layout_ocr
  review_required = true

- handwritten:
  processing_action = try_vision_or_review
  review_required = true

- image_or_photo:
  processing_action = skip_ocr
  review_required = false

- admin_or_cover:
  processing_action = extract_metadata
  review_required = false

- unreadable:
  processing_action = skip_and_record
  review_required = true

## 手書き文書の扱い

手書き中心ページは、通常OCRでは精度が低い可能性が高いため、
最初から通常OCRの主対象にはしない。

ただし、タイプ文書に手書きメモが混在する場合は、
タイプ本文だけOCRを試し、手書き部分は注釈候補として記録する。
