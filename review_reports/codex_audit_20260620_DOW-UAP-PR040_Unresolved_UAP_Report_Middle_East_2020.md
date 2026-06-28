---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 5
UNVERIFIABLE: 1
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上ネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の対象行と一致する。
P1-REG BLOCK review_logs/source_registry.csv に対象MP4の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-DATE WARN 本文の Release Date は 2026年05月22日だが、metadata/files_catalog.csv と metadata/uap-csv-cache.csv は 5/8/26 であり、公開日メタデータに不一致がある。
P1-LOCATION PASS Related Location は files_catalog.csv / uap-csv-cache.csv の Arabian Gulf と一致する。
P1-URL PASS 動画記事として WAR.GOV 公開ページ、DVIDS ID、DVIDS URL が併記されている。
P1-TECH UNVERIFIABLE raw video / thumbnail が確認できず、ffprobe値・視覚観察内容のローカル実測照合は完了できない。
P1-SOURCE WARN metadata/uap-csv-cache.csv の公式説明にある AARO、USCENTCOM、00:10の注記「U/I SMALL THERMAL SIGNATURE」、AARO未編集の説明が本文に反映されていない。
P2-STRUCT WARN チェックリスト上の「注意点」セクションと「免責」セクションが独立見出しとして存在しない。
P2-POINTS PASS 要点は3項目の番号付き太字で記述されている。
P2-DRAFTNOTE WARN 「note転記後にこの行を削除」という作業メモが本文中に残っている。
P2-TERMS PASS DVIDS は初出で補足され、本文内に未補足の主要軍事略語の大量混入は確認されない。
P2-OBJECTIVITY PASS 「とみられる」「確認できない」「断定しません」などの留保があり、視覚観察と推定の分離は概ね保たれている。
P2-TITLE WARN タイトルに #TBD が残っており、公開用 article_id 確定前の状態である。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | Release Date：2026年05月22日（war.gov/UFO/ にて公開・Release 02） | files_catalog.csv / uap-csv-cache.csv の 5/8/26 と Release 02 公開日の扱いを分け、どちらの日付か明確化する。
W-02: 一次資料説明 | AARO did not edit the originally reported material... / U/I SMALL THERMAL SIGNATURE | 公式説明由来の重要情報として、AARO未編集、00:10注記、USCENTCOM提出の概要を事実欄または注意点に短く追加する。
W-03: 記事構成 | 注意点・免責セクションなし | 出典前後に短い「注意点」「免責」見出しを設け、動画説明は分析判断ではない旨を明示する。
W-04: note投稿前残存行 | → 使用ファイル：thumbnails/DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png（note転記後にこの行を削除） | 公開本文では作業メモを削除し、画像キャプションのみ残す。
W-05: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR040... | article_id 確定後に #TBD を除去した公開用タイトルへ確定する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---