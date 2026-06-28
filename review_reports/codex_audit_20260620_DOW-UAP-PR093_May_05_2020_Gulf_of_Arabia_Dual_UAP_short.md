---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 6
UNVERIFIABLE: 0
PASS: 8
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマット（Markdown table、引用ブロック、長文英文引用、複雑ネスト、Codex注釈ブロック）は検出なし。
P1-1 WARN source_registry.csv に対象PR093の登録がなく、記事ID・登録上の一次資料整合性が未確定。
P1-2 PASS 再生時間・解像度・フレームレート・音声有無はローカルffprobe結果と整合。
P1-3 PASS DVIDS、CENTCOM、AORなど主要略語には最低限の日本語補足あり。
P1-5 PASS PR093とPR095はMD5が異なる別ファイルであることを確認。
P2-1 WARN 標準構成のうち「注意点」「免責」に相当する独立セクションが欠落。
P2-2 PASS platformを航空機・車両・ドローン等へ根拠なく具体化していない。
P2-3 WARN 「観測したとされる」の表現があり、映像資料では「記録された」とする基準にやや未整合。
P2-4 PASS 日本向け換算が必要な速度・高度・距離等の数値単位は本文に出ていない。
P2-5 WARN note転記作業用の内部行が本文に残っている。
P2-6 PASS 一般読者向けの主要組織名・資料種別・DVIDSの補足は概ね足りている。
IMG-1 WARN 「IR映像」と断定気味の箇所があり、視覚観察とセンサー種別推定の分離が不十分。
IMG-2 PASS Dual UAPの2対象について「確認困難」と留保しており、物体種別・行動意図を断定していない。
IMG-3 WARN PR093とPR095について「ファイル名が同一」とする記述は、PR番号を含む実ファイル名とは不一致。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 登録後に article_id・status・draft_path と照合できる形にする。
W-02: 記事構成 | 注意点・免責に相当する独立セクションがない。 | 出典前後に「注意点」「免責」を独立見出しで追加する。
W-03: 表現の客観性 | CALLSIGNプラットフォームが「Dual UAP（2つのUAP）」を観測したとされる事案の映像です。 | 「Dual UAP（2つのUAP）」として記録された映像です、などに弱める。
W-04: note投稿互換 | → 使用ファイル：thumbnails/...（note転記後にこの行を削除） | 公開本文から作業用行を削除する。
W-05: 画像記事 | グレースケールIR映像 | 「グレースケール映像（IRセンサー由来の可能性はあるが、このフレームだけでは確認できない）」にする。
W-06: 関連ファイル | PR093（30.1秒）とPR095（288.5秒）はファイル名が同一ですが、MD5・再生時間が異なる別ファイルです。 | 「PR番号を除く記述部分が同一の別ファイル」など、実ファイル名との差分を明確化する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---