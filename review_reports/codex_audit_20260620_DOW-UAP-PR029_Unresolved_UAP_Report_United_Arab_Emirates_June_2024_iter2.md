---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層以上ネスト・Codex注釈ブロックは検出されない。
P1-1a PASS File Name は metadata/files_catalog.csv の対象行およびローカル動画ファイル名と一致する。
P1-1b PASS Release Date は metadata/files_catalog.csv および DVIDS Date Posted の 2026年05月08日と整合する。
P1-1c BLOCK Incident Date が DVIDS の Date Taken: 06.01.2024 と不整合。本文は「2024年6月」「具体的な日付は不明」としており、直接出典で確認できる日付を反映していない。
P1-1d PASS Related Location は metadata/files_catalog.csv の Gulf of Oman と一致し、United Arab Emirates との不一致可能性も明記されている。
P1-2 WARN ffprobe由来のビットレート・ファイルサイズ表記がローカル実測値と軽微に不一致。
P1-3 PASS DVIDS と AOR は本文内で日本語補足されている。
P1-5 WARN source_registry.csv 未登録・article_id 未付番のまま。
P2-1 PASS 構成はメタデータ、要点、AI読解、注意点、出典、免責の順で、要点も3項目。
P2-2 PASS 本文で使用される略語・組織名は過不足なく補足され、重大な未説明略語は検出されない。
P2-3 WARN 「トラッキングボックス」が機器動作の解釈に読めるため、視覚観察と機能推定の分離がやや弱い。
P2-4 PASS ノット・フィート等の換算対象単位は本文に出ていない。
P2-5 PASS note投稿互換上の重大な本文崩れ要因は検出されない。
IMG-1 PASS 物体種別・正体・行動意図は断定されず、可能性表現と確認不能の留保がある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像メタデータ | ビットレート：5,562 kbps | ffprobe実測または thumbnails metadata に合わせて「約5,668 kbps」などへ統一する。
W-02: source_registry関係 | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前に source_registry へ登録し、タイトルの #TBD も確定 article_id に合わせる。
W-03: 表現の客観性 | シアン色の大きな矩形トラッキングボックス | 「シアン色の大きな矩形表示」など、追跡機能の断定を避ける表現にする。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---