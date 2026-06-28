---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 5
UNVERIFIABLE: 0
PASS: 8
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマット（Markdown表・引用ブロック・長文英文引用・複雑ネスト・Codex注釈ブロック）は検出されない
P1-1 BLOCK Release Date がドラフト「2026年05月22日」に対し、metadata/files_catalog.csv および metadata/uap-csv-cache.csv は「5/8/26」で不一致
P1-2 PASS Incident Date はファイル名由来の「2024年」として留保されており本文内矛盾はない
P1-3 PASS File Name・DVIDS ID 1006110・Related Location Indo-PACOM はローカルメタデータと整合
P1-4 PASS ffprobe由来の再生時間・解像度・フレームレート・音声情報はローカル動画と整合
P1-5 WARN source_registry.csv に当該ファイルの登録がなく article_id が #TBD のまま
P2-1 WARN 標準構成上の「注意点」「免責」セクションが独立しておらず、公開前注記が末尾に残っている
P2-2 WARN 「note転記後にこの行を削除」という編集指示が本文内に残っている
P2-3 WARN AOR が本文中で未説明の略語として出現している
P2-4 WARN 視覚観察記事として「地面・空」「珍しい地上構造物」の表現がやや断定的・比較根拠不足
P2-5 PASS 要点は3項目で構成されている
P2-6 PASS タイトルと本文内容は概ね一致している
IMG-1 PASS 視覚観察情報とファイル名・メタデータ由来情報を分離して記述している
IMG-2 PASS UAP候補の正体・種別・行動意図について留保がある
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry 未登録 | 「本ドラフトは source_registry.csv への登録・article_id の付番が未実施です」 | 公開前に source_registry へ登録し、article_id を確定する
W-02: 記事構成 | 「⚠️ source_registry 未登録」が出典後の末尾に残っている | 独立した注意点・免責セクションに整理するか、公開用本文から管理メモを除外する
W-03: 代表フレーム指定行 | 「（note転記後にこの行を削除）」 | 公開用本文ではこの編集指示を削除する
W-04: この資料の要点 | 「AORは『Indo-PACOM』と記録されています」 | 「AOR（Area of Responsibility：担当作戦地域）は『Indo-PACOM』と記録されています」にする
W-05: 代表フレーム説明・AI解析メモ | 「下部の暗い領域は地面・風車、上部は空」「Release 02 VIDでは珍しい地上構造物」 | 「地面または地上構造物とみられる」「空域とみられる」に留保し、「珍しい」は削除または比較根拠を明示する
---WARN_DETAILS_END---
---CODEX_AUDIT_END---