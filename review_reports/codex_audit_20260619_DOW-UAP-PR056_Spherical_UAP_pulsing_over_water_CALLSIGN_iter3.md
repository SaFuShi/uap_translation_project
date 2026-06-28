---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 2
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の対象行と一致する。
P1-1-SOURCEURL BLOCK WAR.GOV 出典が https://www.war.gov/UFO/ のトップページ表記で、対象メディアの直接URL扱いになっていない。
P1-1-DATE PASS Release Date は 2026年05月22日、Incident Date 不明、AOR不明の扱いは metadata/files_catalog.csv と整合する。
P1-2-NUM PASS ffprobe由来の codec・解像度・fps・duration・bitrate・音声コーデック・ファイルサイズは本文内で矛盾していない。
P1-3-ABBREV PASS AOR は初出付近で Area of Responsibility：担当作戦地域、DVIDS は国防映像情報配信サービスとして補足されている。
P1-4 PASS Misrep・MDR・JSIR・CSP/MRO等の番号類は本文に出ていない。
P1-5-MEDIA PASS metadata/files_catalog.csv に対象動画ファイルの登録があり、DVIDS ID 1007718 と本文記述は一致する。
P2-1-STRUCTURE PASS 構成はメタデータ、要点、AI読解、注意点、出典、免責に沿っており、要点は3項目。
P2-1-SOURCES PASS 出典セクションに WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-3-OBJECTIVITY WARN 「追尾表示らしき表示」「追尾マーカー」など、画面表示の視覚観察と機器動作・追尾解釈の分離が一部弱い。
IMG-1 PASS 視覚観察とファイル名・メタデータ由来情報はセクション分離され、画像のみの判断には留保が付いている。
P2-5-EDITORIAL WARN 「note転記後にこの行を削除」という編集指示が note_drafts 本文に残っている。
P3-REGISTRY BLOCK 本文末尾で source_registry 未登録・article_id 未付番と明記されており、公開前記事として registry 整合性チェックを通過できない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像説明全般 | 「追尾表示らしき表示」「追尾マーカーと推定されるが確認できない」 | 視覚観察は「クロスヘア状表示」「十字型表示」とし、追尾解釈は推定として別文で分離する。
W-02: 代表フレーム直前 | 「→ 使用ファイル：thumbnails/DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN/frame_0000.png（note転記後にこの行を削除）」 | 公開用本文から編集指示を削除し、必要なら通常のキャプションだけ残す。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---