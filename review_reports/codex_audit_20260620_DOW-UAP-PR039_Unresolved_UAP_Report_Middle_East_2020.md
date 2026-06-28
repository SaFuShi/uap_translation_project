---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 3
UNVERIFIABLE: 0
PASS: 9
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・複雑なネスト箇条書き・Codex注釈ブロックは確認されない。
P1-META-FILENAME PASS ドラフトの File Name は metadata/files_catalog.csv の PR039 行と一致している。
P1-META-REGISTRY BLOCK review_logs/source_registry.csv に DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_2020.mp4 / DVIDS ID 1006089 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-META-DATE BLOCK ドラフトは Release Date を 2026年05月22日と記載しているが、metadata/files_catalog.csv の PR039 行は 5/8/26 であり、メタデータ日付が整合していない。
P1-META-LOCATION PASS Related Location は metadata/files_catalog.csv の PR039 行と同じ Arabian Gulf と記載されている。
P1-META-DVIDS PASS DVIDS ID 1006089 と DVIDS URL https://www.dvidshub.net/video/1006089 はドラフト内で一貫している。
P1-NUMERIC WARN 映像メタデータのビットレートがドラフトでは 2,229 kbps、thumbnails 側 metadata.json では 2,342 kbps で不一致。
P1-DUP PASS PR037 とは DVIDS ID が異なる映像として区別され、同一性を断定していない。
P2-STRUCT WARN 「注意点」セクションが独立見出しとして置かれておらず、AI解析メモと免責の配置も標準順からずれている。
P2-POINTS PASS 「この資料の要点」は3項目の番号付き太字で構成されている。
P2-VISUAL-SEPARATION PASS 視覚観察情報とファイル名・メタデータ由来情報は見出しで分離されている。
P2-INTERPRETATION PASS IRセンサー、船着き場、UAP候補などの解釈には「推定」「みられる」「確認できない」の留保がある。
P2-FORMAT-NOTE WARN 「note転記後にこの行を削除」という編集メモが本文中に残っている。
P2-SOURCES PASS 出典セクションに WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: P1-NUMERIC | 「ビットレート：2,229 kbps」 | thumbnails 側 metadata.json の 2,342 kbps と照合し、確認済みの値に統一する。
W-02: P2-STRUCT | 「AI解析メモ」が出典前にあり、独立した「注意点」セクションがない | AI読解の後に注意点を独立見出しで置き、出典後に免責を整理する。
W-03: P2-FORMAT-NOTE | 「→ 使用ファイル：...（note転記後にこの行を削除）」 | 投稿本文では編集メモを削除し、必要なら画像キャプションのみ残す。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---