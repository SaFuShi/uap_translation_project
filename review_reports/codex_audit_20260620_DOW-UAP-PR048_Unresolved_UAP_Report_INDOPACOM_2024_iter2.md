---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマット（Markdown表・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロック）は検出されない
P1-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024.mp4 / DVIDS ID 1006110 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている
P1-1 PASS File Name・Release Date・Related Location・DVIDS ID は metadata/files_catalog.csv および metadata/uap-csv-cache.csv と整合
P1-2 PASS Incident Date はファイル名由来の「2024年」として留保されており本文内矛盾はない
P1-3 PASS ffprobe由来の再生時間・解像度・フレームレート・音声情報はローカル動画と整合
P1-4 PASS 出典に WAR.GOV 公開ページ、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている
P2-1 WARN 標準構成上の「注意点」「免責」セクションが独立しておらず、公開前管理メモが末尾に残っている
P2-2 WARN AOR が本文中で未説明の略語として出現している
P2-3 WARN 視覚観察記事として「特殊」「珍しい」の比較表現に根拠が示されていない
P2-4 PASS 要点は3項目で構成されている
P2-5 PASS UFO論壇的表現や物体正体の断定は検出されない
P2-6 PASS タイトルと本文内容は概ね一致している
IMG-1 PASS 視覚観察情報とファイル名・メタデータ由来情報を分離して記述している
IMG-2 PASS UAP候補の正体・種別・行動意図について留保がある
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 記事構成 | 「⚠️ source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です」 | 公開前管理メモは公開用本文から除外し、必要なら独立した注意点・免責セクションに整理する
W-02: この資料の要点 | 「AORは『Indo-PACOM』と記録されています」 | 「AOR（Area of Responsibility：担当作戦地域）は『Indo-PACOM』と記録されています」にする
W-03: この資料の要点・AI解析メモ | 「特殊な映像です」「Release 02 VIDでは珍しい地上構造物」 | 比較根拠を示せない場合は「下部に地上構造物とみられるものが確認できる」程度に留める
---WARN_DETAILS_END---
---CODEX_AUDIT_END---