---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 2
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-FORMAT PASS Markdown table、引用ブロック、長文英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020.mp4 / DVIDS ID 1006089 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-CATALOG PASS File Name、Agency、Release Date、Related Location、File Type、DVIDS ID は metadata/files_catalog.csv / metadata/uap-csv-cache.csv の対象行と整合する。
P1-URL PASS 動画記事として WAR.GOV 公開ページと DVIDS URL が併記され、DVIDS ID 1006089 と整合する。
P1-OFFICIAL-DESC WARN metadata/uap-csv-cache.csv の公式説明にある USCENTCOM提出、AARO宛、赤外線センサー、米軍プラットフォーム、報告者説明なし、00:03-00:05の淡いコントラスト領域説明、分析判断ではない旨が本文に反映されていない。
P1-TECH PASS ffprobe実測と本文の 1920×1080、30fps、5.8秒、H.264、AAC音声、映像ビットレート約2,229 kbps は整合する。
P1-DUP UNVERIFIABLE source_registry 未登録のため、registry ベースの同一SHA256重複・公開済み記事重複確認は完了できない。
P2-STRUCT WARN チェックリスト上の標準構成にある独立した「注意点」セクションと「免責」セクションが不足している。
P2-POINTS PASS 「この資料の要点」は3項目の番号付き太字で構成されている。
P2-VISUAL-SEPARATION PASS 視覚観察情報とファイル名・メタデータ由来情報は見出しで分離されている。
P2-TERMS WARN 「IRセンサー」のIRが一般読者向けに「赤外線」と補足されていない。
P2-OBJECTIVITY PASS 「推定されるが確認できない」「みられる」「断定しません」などの留保があり、確認事実と推定の区別は概ね保たれている。
P2-TITLE WARN タイトルに #TBD が残っており、公開用 article_id 確定前の状態である。
P3-REG UNVERIFIABLE source_registry 未登録のため、article_id連番、status、note_url、published_date、draft_path の整合性は確認不能。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 公式説明 | 本文全体で、USCENTCOM提出・AARO宛・赤外線センサー・米軍プラットフォーム・00:03-00:05の淡いコントラスト領域説明が未反映 | 公式説明由来情報として、確認できる範囲を留保付きで短く追加する。
W-02: 記事構成 | 独立した「注意点」「免責」セクションなし | AI読解後に短い注意点、出典後に免責を置き、動画説明は分析判断ではない旨も整理する。
W-03: AI読解 | グレースケールの俯瞰映像（IRセンサーと推定されるが確認できない） | 「IR（赤外線）センサーと推定されるが確認できない」など、初出で短く補足する。
W-04: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR039... | article_id 確定後に #TBD を除去した公開用タイトルへ確定する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---