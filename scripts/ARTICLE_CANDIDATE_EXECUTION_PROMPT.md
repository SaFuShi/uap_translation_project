# Claude Code 実行プロンプト：Article Candidate Ranking

以下の仕様書を確認した上で、
記事化候補を優先順位付けするツールを実装してください。

## 参照必須ファイル

- PROJECT_SPEC.md
- scripts/ARTICLE_CANDIDATE_SPEC.md
- metadata/files_catalog.csv
- classification/page_classification.csv
- extracted_text/ocr_results.csv

## 実装対象

scripts/rank_article_candidates.py

## 目的

WAR.GOV/UFO公開文書の中から、
速報版・詳細版の記事化候補を抽出し、
metadata/article_candidates.csv に保存する。

## 重要方針

速報版は、日本関連・読者関心・話題性を優先する。

詳細版は、公開順・資料整理・原文対訳向きの文書を優先する。

## 出力先

metadata/article_candidates.csv

## 必須出力項目

- file_name
- agency
- release_date
- incident_date
- incident_location
- file_type
- page_count
- ocr_success_rate
- review_required_count
- japan_related
- japan_keywords
- candidate_score
- recommended_lane
- reasons
- notes

## 完成条件

1. files_catalog.csv を読み込める
2. OCR結果・分類結果を統合できる
3. 日本関連キーワードを検出できる
4. candidate_score を算出できる
5. recommended_lane を出力できる
6. metadata/article_candidates.csv を生成できる
7. エラー時も処理全体を止めず記録する
8. Python3で実行できる

## 非対象

今回は以下を実装しない。

- 翻訳
- 要約
- note本文生成
- 自動投稿
- 外部API利用

## 必須報告

実装後、以下を報告してください。

1. 実装内容
2. 使用ライブラリ
3. 実行手順
4. article_candidates.csv の上位候補
5. 日本関連候補の有無
6. 速報版候補
7. 詳細版候補
8. 限界・今後改善すべき点

## 重要

このツールは、翻訳そのものではなく、
「どの文書から記事化するべきか」を判断するための入口です。

速報版は読者関心を優先し、
詳細版は資料整理・原典参照性を優先してください。
