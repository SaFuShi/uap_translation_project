---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 5
UNVERIFIABLE: 2
PASS: 7
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020.mp4 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-CATALOG PASS metadata/files_catalog.csv の対象行と、ファイル名、Agency、Related Location、File Type、DVIDS ID は一致する。
P1-DATE WARN 本文の Release Date は 2026年05月22日だが、metadata/files_catalog.csv の対象行は 5/8/26 であり、公開日メタデータに不一致がある。
P1-URL PASS 動画記事として WAR.GOV 公開ページと DVIDS URL が併記され、DVIDS ID 1006087 と整合する。
P1-TECH WARN ffprobe 実測では bit_rate=6,974,606 bps、metadata.json では 6974 kbps であり、本文の 6,866 kbps と一致しない。
P1-DUP UNVERIFIABLE source_registry 未登録のため、同一SHA256重複・公開済み記事との registry ベース重複確認は完了できない。
P2-STRUCT WARN 構成は概ね揃うが、チェックリスト上の「注意点」セクションが独立見出しとして存在しない。
P2-SOURCE PASS 出典に WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-TITLE WARN タイトルに #TBD が残っており、公開用 article_id 確定前の状態である。
P2-DRAFTNOTE WARN 「note転記後にこの行を削除」という作業メモが本文中に残っている。
P2-TERMS PASS DVIDS、AOR は初出付近で補足され、未補足の主要軍事略語の混入は確認されない。
P2-OBJECTIVITY PASS 「とみられる」「確認できない」「断定しません」などの留保があり、確認事実と推定の区別は概ね保たれている。
P2-IMAGE PASS 代表フレーム実見上、海面俯瞰、船状物体、シアン色UI、N表示、黒塗り矩形の記述は視覚情報と整合する。
P3-REG UNVERIFIABLE source_registry 未登録のため、article_id 連番、status、note_url、published_date、draft_path の整合性は確認不能。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | Release Date：2026年05月22日 | files_catalog.csv の 5/8/26 と Release 02 公開日の扱いを分け、どちらの日付か明確化する。
W-02: 映像メタデータ | ビットレート：6,866 kbps | ffprobe 実測値に合わせて約6,975 kbps、または metadata.json に合わせて約6,974 kbps とする。
W-03: 記事構成 | 注意点セクションなし | 出典前に短い「注意点」見出しを設け、視覚観察記事としての留保を集約する。
W-04: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR037... | article_id 確定後に #TBD を除去した公開用タイトルへ確定する。
W-05: 代表フレーム行 | → 使用ファイル：...（note転記後にこの行を削除） | 公開本文では作業メモを削除し、画像キャプションのみ残す。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---