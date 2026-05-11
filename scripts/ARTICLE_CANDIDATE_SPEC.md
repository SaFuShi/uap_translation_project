# ARTICLE_CANDIDATE_SPEC

## 目的

取得済みのWAR.GOV/UFO公開文書の中から、
速報版・詳細版の記事化候補を抽出し、優先順位を付ける。

この処理は、翻訳そのものではなく、
「どの文書から記事化するべきか」を判断するために行う。

## 実装対象

scripts/rank_article_candidates.py

## 参照必須ファイル

- PROJECT_SPEC.md
- metadata/files_catalog.csv
- classification/page_classification.csv
- extracted_text/ocr_results.csv

## 入力

- metadata/files_catalog.csv
- classification/page_classification.csv
- extracted_text/ocr_results.csv

## 出力

metadata/article_candidates.csv

## 出力項目

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

## 基本方針

速報版は、日本の読者が関心を持ちやすい文書を優先する。

詳細版は、WAR.GOVでの公開順・ファイル順に近い形で整理し、
アーカイブとして比較しやすくする。

## recommended_lane

- breaking:
  速報版向き。日本関連・時事性・話題性を優先する。

- detailed:
  詳細版向き。公開順・資料整理・原文対訳向き。

- hold:
  OCR困難、判読困難、記事化優先度が低いもの。

## 日本関連キーワード例

- Japan
- Japanese
- Tokyo
- Okinawa
- Yokota
- Misawa
- Kadena
- Pacific
- East Asia
- Asia
- Far East
- Nippon
- Nihon

## スコアリング例

- 日本関連キーワードあり: +30
- Okinawa / Kadena / Yokota / Misawa など在日米軍関連: +40
- Incident Location に日本・太平洋・東アジア関連: +30
- Agency が FBI / CIA / DoD / NASA: +10
- OCR成功率が高い: +10
- review_required が少ない: +10
- page_count が少ない: +5
- newspaper_or_print_clipping が多い: -10
- unreadable が多い: -20

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

## 実行イメージ

python3 scripts/rank_article_candidates.py

## 重要

このツールの目的は、
記事化対象を選ぶための優先順位付けである。

速報版は読者関心を優先し、
詳細版は資料整理・原典参照性を優先する。
