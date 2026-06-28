---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上ネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1-REGISTRY BLOCK review_logs/source_registry.csv に対象ファイル名または DVIDS ID 1010263 の登録が確認できず、タイトルも #TBD のまま。
P1-1-RELEASE PASS Release Date は 2026年06月12日で、metadata/files_catalog.csv の 6/12/26 と整合する。
P1-1-INCIDENT PASS Incident Date は 2021年11月で、metadata/files_catalog.csv の November, 2021 と整合する。
P1-1-LOCATION PASS Related Location は Northeastern United States で、metadata/files_catalog.csv と整合する。
P1-2-VIDEO-META WARN ffprobe および thumbnails metadata.json の bit_rate は約4,018 kbps だが、本文は 3,918 kbps と記載している。
M5-DVIDS PASS DVIDS URL は https://www.dvidshub.net/video/1010263 で、metadata/files_catalog.csv の dvids_video_id 1010263 と一致する。
M5-WARGOV PASS 動画記事として WAR.GOV 公開ページ https://www.war.gov/UFO/ が記載されている。
M4-THUMB PASS 代表フレームのパスとキャプションが本文および出典に明記されている。
M6-AUDIO PASS 音声トラックありとは記載しているが、文字起こし未実施の発言内容は記述していない。
IMG-1 PASS 視覚観察とファイル名・メタデータ由来情報を分離している。
IMG-2 PASS 移動、追跡、消失、分裂、複数化などの動的挙動を確定事実として断定していない。
P2-1-STRUCT WARN 標準構成の「注意点」「免責」セクションが独立しておらず、末尾構成がチェックリスト順に不足している。
P2-5-TITLE WARN 記事タイトル冒頭が「FBI FBI-UAP-PR001」となっており、FBI が重複して読みにくい。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像メタデータ | ビットレート：3,918 kbps | ffprobe / thumbnails metadata.json に合わせて「ビットレート：約4,018 kbps」に修正する。
W-02: 記事構成 | 出典の後に source_registry 未登録注記のみがあり、独立した注意点・免責セクションがない。 | 「注意点」と「免責」を標準構成として追加し、視覚観察記事の限界を明示する。
W-03: タイトル | # 【概要版#TBD】FBI FBI-UAP-PR001：北東部米国2021年「三角形オーブ」とされる事案映像 | article_id 確定後に #TBD を置換し、「FBI FBI-UAP-PR001」の重複を解消する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---