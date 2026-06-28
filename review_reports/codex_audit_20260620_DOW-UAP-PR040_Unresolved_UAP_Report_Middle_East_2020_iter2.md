---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上ネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の対象行と一致する。
P1-REG BLOCK review_logs/source_registry.csv に対象MP4 / DVIDS ID 1006093 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-DATE PASS Release Date は metadata/files_catalog.csv の 5/8/26 と整合し、YYYY年MM月DD日形式で記述されている。
P1-LOCATION PASS Related Location は metadata/files_catalog.csv の Arabian Gulf と一致する。
P1-URL PASS 動画記事として WAR.GOV 公開ページ、DVIDS ID、DVIDS URL が併記されている。
P1-TECH WARN ffprobe実測では全体ビットレートが約3,720kbpsだが、本文は3,616kbpsとしており、参照値の不一致がある。
P2-STRUCT WARN チェックリスト上の「注意点」セクションと「免責」セクションが独立見出しとして存在しない。
P2-POINTS PASS 要点は3項目の番号付き太字で記述されている。
P2-SOURCE-CAPTION PASS 代表フレーム行は画像キャプションとして記述され、note転記用の作業メモは確認されない。
P2-TERMS PASS DVIDS は初出で補足され、本文内に未補足の主要軍事略語の大量混入は確認されない。
P2-OBJECTIVITY PASS 「とみられる」「確認できない」「断定しません」などの留保があり、視覚観察と推定の分離は概ね保たれている。
P2-TITLE WARN タイトルに #TBD が残っており、公開用 article_id 確定前の状態である。
IMG-AUDIT PASS 視覚観察と解釈は概ね分離され、「移動」「追跡」「消失」等の確定的な動態断定は確認されない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像メタデータ | ビットレート：3,616 kbps | ffprobe実測値または thumbnails metadata の約3,720kbpsに合わせるか、どのストリーム値かを明示する。
W-02: 記事構成 | 注意点・免責セクションなし | 出典前後に短い「注意点」「免責」見出しを設け、動画説明は分析判断ではない旨を明示する。
W-03: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR040... | article_id 確定後に #TBD を除去した公開用タイトルへ確定する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---