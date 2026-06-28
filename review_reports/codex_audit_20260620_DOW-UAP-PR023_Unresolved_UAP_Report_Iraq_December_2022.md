---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 3
WARN: 4
UNVERIFIABLE: 0
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1-FILENAME BLOCK review_logs/source_registry.csv に対象MP4 DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022.mp4 の登録がなく、同一DVIDS ID 1006062では #039 のPDFのみ登録済み。
P1-1-RELEASE-DATE BLOCK metadata/files_catalog.csv の対象MP4行は release_date=5/8/26 だが、本文は Release Date：2026年05月22日としており一次メタデータと矛盾する。
P1-1-LOCATION PASS Related Location は Iraq と記載され、metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-SOURCE WARN WAR.GOV はトップページのみで、ローカルcatalog上の download_url である直接URLが出典に記載されていない。
P1-5-DUP WARN 同一DVIDS ID 1006062 のPDF記事 #039 が既にpublishedであり、動画記事としての独立登録・既存PDF記事との関係整理が必要。
P2-1-STRUCTURE PASS メタデータ、要点3項目、AI読解、出典、免責相当の注意書きがあり、概要版としての構成は概ね満たす。
P2-1-TITLE-REGISTRY WARN タイトルが #TBD のままで、本文末にも source_registry 未登録・article_id 未付番の公開前メモが残っている。
P2-2-ABBREV PASS DVIDS と AOR は本文内で補足され、未説明の主要軍事略語の反復は確認されない。
P2-3-OBJECTIVITY WARN 「担当AORはIraq」と記述しているが、確認できたローカルmetadataは incident_location=Iraq であり、AORとしての断定はやや強い。
P2-4-UNITS PASS 秒、解像度、fps、MB、kbpsなどの技術情報に不自然な換算・単位誤りは確認されない。
P2-5-READABILITY PASS OCR生ログや長い英文引用はなく、note投稿互換上の大きな崩れ要因は確認されない。
IMG-1 PASS 視覚観察と解釈は概ね分離され、「IRセンサーと推定されるが確認できない」など留保もある。
P3-REGISTRY BLOCK 本文末尾で source_registry 未登録・article_id 未付番と明記されており、registry上のstatus、draft_path、重複状態の正式整合性チェックを通過できない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 出典 | WAR.GOV：https://www.war.gov/UFO/ | catalog上の直接URLを出典に追加し、トップページのみの出典にしない。
W-02: source_registry関係 | DVIDS ID：1006062（war.gov公開・Release 02） | 既公開PDF #039 と対象MP4記事の関係をregistry側で整理し、動画記事として独立登録する。
W-03: タイトル/末尾 | # 【概要版#TBD】、source_registry 未登録、article_id の付番が未実施 | registry登録後に確定article_idを反映し、公開前メモを削除する。
W-04: 要点 | 担当AOR（Area of Responsibility：担当作戦地域）はIraqと記録されています。 | ローカルmetadataで確認できる範囲に合わせ、「関連地域はIraqと記録されています」などに弱める。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---