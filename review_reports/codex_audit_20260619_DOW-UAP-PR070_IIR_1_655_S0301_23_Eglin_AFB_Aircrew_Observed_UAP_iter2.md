---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-REG BLOCK review_logs/source_registry.csv に対象PR070の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-META PASS ファイル名、Release Date、DVIDS ID、Related Location は metadata/files_catalog.csv および metadata/uap-csv-cache.csv と整合する。
P1-DATE PASS Incident Date は DVIDSタイトル由来の「13 Feb 23」として本文に反映されている。
P1-SOURCE PASS DVIDS URL は https://www.dvidshub.net/video/1007783 として記載され、files_catalog.csv の dvids_video_id と一致する。
P1-TECH PASS ffprobe値はドラフト記載の30.1秒、1920×1080、30fps、H.264、AAC、約35MB、約9,980kbpsと整合する。
P2-STRUCT WARN AI解析メモがAI読解内に置かれており、チェックリストの「末尾の所定位置」とはずれている。
P2-DRAFTNOTE WARN 「note転記後にこの行を削除」という制作メモが本文中に残っている。
P2-KEYPOINT PASS 要点は番号付き太字で3項目に整理されている。
P2-WARNING PASS 冒頭に動画映像・視覚観察記事である旨の警告があり、確認事実とメタデータ由来情報の分離方針が明記されている。
P2-ABBR PASS DVIDS、IIR、AFB は本文中で日本語補足または英語展開が付されている。
P2-OBJECTIVITY PASS UFO論壇的表現や異星人等の断定表現はなく、正体・種別・意図を断定しない姿勢が維持されている。
M1-VISUAL PASS 視覚観察とファイル名・メタデータ由来情報が見出しで分離され、画像判断には留保が付されている。
M6-PROVENANCE-CAVEAT WARN uap-csv-cache.csv にあるAAROの説明、NORTHCOM AOR、chain-of-custody不足の注意書きが本文に反映されていない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: AI読解 | **AI解析メモ：** 動画ファイル。ffprobeによる技術情報取得済み。 | AI解析メモは出典後または免責直前の所定位置に移す。
W-02: 代表フレーム直前 | → 使用ファイル：thumbnails/.../frame_0010.png（note転記後にこの行を削除） | 制作メモ行は本文から除き、必要ならキャプションだけを残す。
W-03: 出典・注意点 | 本文全体でAARO説明文のchain-of-custody注意とNORTHCOM AORが未反映 | AARO説明由来の注意として、NORTHCOM担当区域、2023年3月に分類ネットワークへアップロード、chain-of-custody不足、説明文は分析判断・調査結論ではない旨を短く補う。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---