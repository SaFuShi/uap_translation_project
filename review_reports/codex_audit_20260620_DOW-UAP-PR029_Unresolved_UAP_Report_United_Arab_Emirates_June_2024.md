---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 0
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層以上ネスト・Codex注釈ブロックは検出されない。
P1-1a PASS File Name は metadata/files_catalog.csv の対象行と一致する。
P1-1b BLOCK Release Date / Release 表記がローカルカタログと不一致。metadata/files_catalog.csv と metadata/uap-data.csv は 5/8/26、本文は 2026年05月22日・Release 02。
P1-1c PASS Incident Date はファイル名由来の 2024年6月として留保され、具体日付不明も明記されている。
P1-1d PASS Related Location は files_catalog.csv の Gulf of Oman と一致し、United Arab Emirates との不一致可能性も明記されている。
P1-2 WARN ffprobe由来のビットレート・ファイルサイズがローカル実測値と軽微に不一致。
P1-3 PASS DVIDS と AOR は本文内で日本語補足されている。
P1-5 WARN source_registry.csv 未登録・article_id 未付番のまま。
P2-1 PASS 構成はメタデータ、要点、AI読解、注意点、出典、免責の順で、要点も3項目。
P2-2 PASS 本文で使用される略語・組織名は過不足なく補足され、重大な未説明略語は検出されない。
P2-3 WARN 「トラッキングボックス」が機器動作の解釈に読めるため、視覚観察と機能推定の分離がやや弱い。
P2-4 PASS ノット・フィート等の換算対象単位は本文に出ていない。
P2-5 WARN note転記用の内部作業行が本文に残っている。
IMG-1 PASS 物体種別・正体・行動意図は断定されず、可能性表現と確認不能の留保がある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像メタデータ | ビットレート：5,562 kbps | ffprobe実測または thumbnails metadata に合わせて「約5,668 kbps」などへ統一する。
W-02: source_registry関係 | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前に source_registry へ登録し、タイトルの #TBD も確定 article_id に合わせる。
W-03: 表現の客観性 | シアン色の大きな矩形トラッキングボックス | 「シアン色の大きな矩形表示」など、追跡機能の断定を避ける表現にする。
W-04: note投稿前残存行 | → 使用ファイル：thumbnails/DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Emirates_June_2024/frame_0000.png（note転記後にこの行を削除） | note本文から削除し、画像キャプションだけを残す。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---