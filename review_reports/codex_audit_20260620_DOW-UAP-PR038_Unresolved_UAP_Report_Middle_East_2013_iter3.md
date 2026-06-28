---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 6
UNVERIFIABLE: 2
PASS: 5
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013.mp4 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-META PASS metadata/files_catalog.csv および metadata/uap-csv-cache.csv と、ファイル名、Agency、Release Date、Related Location、File Type、DVIDS ID は概ね一致する。
P1-DVIDS-STATUS WARN metadata/uap-csv-cache.csv の DVIDS Video Title は「Resolved as an Aircraft, Middle East 2013」だが、タイトル・要点では「未解決」側の印象が強く、公式タイトルとの優先関係が弱い。
P1-OFFICIAL-DESC WARN metadata/uap-csv-cache.csv の公式説明にある USCENTCOM、AARO、IRセンサー、米軍プラットフォーム、映像内の時刻別描写が本文で十分に反映・区分されていない。
P1-TECH WARN ffprobe の format bit_rate は約2,308 kbpsで、本文の「ビットレート：2,204 kbps」は video stream 側の値としては整合するが、コンテナ欄のラベルとしては不明確。
P1-DUP UNVERIFIABLE source_registry 未登録のため、同一SHA256重複・公開済み記事との registry ベース重複確認は完了できない。
P2-STRUCT WARN 構成は概ね揃うが、チェックリスト上の「注意点」および明示的な「免責」セクションが独立見出しとして存在しない。
P2-KEYPOINTS PASS 「この資料の要点」は3項目で記述されている。
P2-SOURCE PASS 出典に WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-TITLE WARN タイトルに #TBD が残っており、公開用 article_id 確定前の状態である。
P2-OBJECTIVITY WARN 「旧世代のスタイル」「2013年当時の撮影システムを反映している可能性」は、視覚観察から一段進んだ解釈であり、根拠区分の分離が弱い。
P2-IMAGE PASS 代表フレーム記述は、グレー背景、ビネット、グレー色クロスヘア、N表示、多数の黒塗り矩形、小さな青またはシアン点の視覚情報として概ね整合する。
P3-REG UNVERIFIABLE source_registry 未登録のため、article_id 連番、status、note_url、published_date、draft_path の整合性は確認不能。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: DVIDSタイトル | DVIDS Video Title：「Resolved as an Aircraft, Middle East 2013」／未解決UAP事案の映像とされています | 公式タイトルでは航空機として解決済み、ファイル名では Unresolved と分かれる旨を要点または注意点で明確化する。
W-02: 公式説明反映 | 映像（IRセンサーと推定されるが確認できない） | 公式説明由来の情報として「IRセンサー」「米軍プラットフォーム」「USCENTCOM」「AARO」を視覚観察とは別枠で記載する。
W-03: 映像メタデータ | ビットレート：2,204 kbps | format全体なら約2,308 kbps、映像ストリームなら約2,204 kbpsとラベルを分ける。
W-04: 記事構成 | 注意点および明示的な免責セクションなし | AI読解後に「注意点」、出典後に「免責」を独立セクションとして置く。
W-05: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR038... | article_id 確定後に #TBD を除去した公開用タイトルへ確定する。
W-06: この資料の要点 | 旧世代のスタイル／2013年当時の撮影システムを反映している可能性 | 「本映像ではグレー色UI、ビネット、多数の黒塗り矩形が確認できる」に留めるか、解釈として明確に分離する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---