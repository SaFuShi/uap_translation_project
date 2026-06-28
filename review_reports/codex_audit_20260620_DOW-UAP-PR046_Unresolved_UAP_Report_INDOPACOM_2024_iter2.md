---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 2
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-FORM PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024.mp4 / DVIDS ID 1006106 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-RELEASE-DATE PASS Release Date 2026年05月08日は metadata/files_catalog.csv の 5/8/26 と整合する。
P1-DIRECT-SOURCE WARN WAR.GOV 出典が https://www.war.gov/UFO/ のトップページ表記のまま。DVIDS直接URLは併記されているが、WAR.GOV側の対象単位URLまたは管理上の直接参照が未整理。
P1-DVIDS PASS DVIDS ID 1006106 は metadata/files_catalog.csv の対象行と一致している。
P1-LOCATION WARN East China Sea は files_catalog.csv 由来の Related Location として一致するが、「担当AORは東シナ海」と読める記述があり、INDOPACOM AOR と関連地点の区別が曖昧。
P1-TECHMETA PASS ffprobe実測値と、本文の約9.9秒・1920×1080・30fps・H.264・AAC・約2.8MB・動画ビットレート2,328kbpsの記述は概ね整合する。
P1-DUP UNVERIFIABLE source_registry 未登録のため、registry ベースの BLOCK 状態、SHA256/MD5重複、公開済み記事重複は確認不能。
P2-STRUCT WARN 構成は概ね揃っているが、末尾の免責が独立した「免責」見出しではなく、source_registry未登録の内部メモも公開本文末尾に残っている。
P2-POINTS PASS 要点は3項目の番号付き太字で記述されている。
P2-ABBREV PASS INDOPACOM、AOR、DVIDS は初出付近で日本語補足または説明があり、記事単独理解性は大きく損なわれていない。
P2-OBJECTIVITY WARN 「Release 02のVID映像の中では対象物が比較的明確に確認できる事例の一つ」は比較対象全体の監査根拠が本文内に示されず、視覚観察を超える相対評価になっている。
P2-IMAGE PASS 視覚観察と解釈は概ね分離され、IRセンサー、海面または空、物体種別について留保が付いている。
P3-REG UNVERIFIABLE source_registry 未登録のため、article_id 連番、status、note_url、published_date、draft_path の整合性は確認不能。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 出典 | 「WAR.GOV：https://www.war.gov/UFO/」 | 対象映像を一意に追跡できる直接URLまたは管理上の直接参照に整理する。
W-02: メタデータ解釈 | 「担当AOR（Area of Responsibility：担当作戦地域）は東シナ海」 | INDOPACOM担当域と Related Location: East China Sea を分けて記述する。
W-03: 構成 | 「※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた『AI概要版』です。」 | 独立した「免責」見出しを設け、公開用免責として整理する。
W-04: 客観性 | 「Release 02のVID映像の中では対象物が比較的明確に確認できる事例の一つです。」 | 比較評価を削除するか、「本フレームでは対象物の輪郭が確認できる」に限定する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---