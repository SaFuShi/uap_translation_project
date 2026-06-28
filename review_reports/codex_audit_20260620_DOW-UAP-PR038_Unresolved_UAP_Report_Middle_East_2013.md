---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 5
UNVERIFIABLE: 2
PASS: 6
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013.mp4 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-META PASS metadata/files_catalog.csv の対象行と、ファイル名、Agency、Related Location、File Type、DVIDS ID は一致する。
P1-DATE BLOCK 本文の Release Date は 2026年05月22日だが、metadata/files_catalog.csv の対象行は 5/8/26 であり、公開日メタデータに不一致がある。
P1-URL PASS 動画記事として WAR.GOV 公開ページと DVIDS URL が併記され、DVIDS ID 1006088 と整合する。
P1-TECH WARN ffprobe 実測および metadata.json では bit_rate が約2,308 kbpsだが、本文は 2,204 kbps と記載している。
P1-DUP UNVERIFIABLE source_registry 未登録のため、同一SHA256重複・公開済み記事との registry ベース重複確認は完了できない。
P2-STRUCT WARN 構成は概ね揃うが、チェックリスト上の「注意点」および明示的な「免責」セクションが独立見出しとして存在しない。
P2-KEYPOINTS PASS 「この資料の要点」は3項目で記述されている。
P2-SOURCE PASS 出典に WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-TITLE WARN タイトルに #TBD が残っており、公開用 article_id 確定前の状態である。
P2-DRAFTNOTE WARN 「note転記後にこの行を削除」という作業メモが本文中に残っている。
P2-OBJECTIVITY WARN 「旧世代のスタイル」「2013年当時の撮影システムを反映している可能性」は、視覚観察から一段進んだ解釈であり、根拠区分の分離が弱い。
P2-IMAGE PASS 代表フレーム実見上、グレー背景、ビネット、グレー色クロスヘア、N表示、多数の黒塗り矩形、小さな青またはシアン点の記述は視覚情報と概ね整合する。
P3-REG UNVERIFIABLE source_registry 未登録のため、article_id 連番、status、note_url、published_date、draft_path の整合性は確認不能。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像メタデータ | ビットレート：2,204 kbps | ffprobe 実測または metadata.json に合わせて約2,308 kbpsとする。
W-02: 記事構成 | 注意点および明示的な免責セクションなし | AI読解後に「注意点」、出典後に「免責」を独立セクションとして置く。
W-03: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR038... | article_id 確定後に #TBD を除去した公開用タイトルへ確定する。
W-04: 代表フレーム行 | → 使用ファイル：...（note転記後にこの行を削除） | 公開本文では作業メモを削除し、画像キャプションのみ残す。
W-05: この資料の要点 | 旧世代のスタイル／2013年当時の撮影システムを反映している可能性 | 「本映像ではグレー色UI、ビネット、多数の黒塗り矩形が確認できる」に留めるか、解釈として明確に分離する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---