---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 5
UNVERIFIABLE: 0
PASS: 11
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv および raw_media/video の対象MP4ファイル名と一致する。
P1-1-RELEASE PASS Release Date は 2026年05月08日で、metadata/files_catalog.csv の 5/8/26 と一致する。
P1-1-LOCATION PASS Related Location は Greece と記載され、metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-DVIDS PASS DVIDS ID 1006073 と DVIDS URL https://www.dvidshub.net/video/1006073 は metadata/files_catalog.csv の dvids_video_id と一致する。
P1-1-URL PASS 動画記事として DVIDS の対象映像直接URLが記載されている。metadata/files_catalog.csv には関連PDF直接URLが未登録のため、WAR.GOV個別URL不記載は本件ではBLOCK扱いしない。
P1-2 WARN ffprobe由来の総ビットレート・ファイルサイズがローカル metadata.json / ffprobe 実測値と不一致。ドラフトは「1,834 kbps」「約14.9 MB」だが、実測は bit_rate 1,938,505 bps、size 15,992,674 bytes、metadata.json は file_size_mb 15.25 / bit_rate_kbps 1938。
P1-3 PASS DVIDS は初出で「国防映像情報配信サービス」と補足されている。
P1-5 WARN review_logs/source_registry.csv に対象MP4記事の登録が確認できず、ドラフト末尾にも source_registry 未登録と明記されている。
P2-1 WARN タイトルに「#TBD」が残っている。
P2-2 WARN 「IR」が初出で日本語補足されていない。
P2-3 PASS 物体の正体・種別・行動意図は断定せず、確認事実と推定を概ね分離している。
P2-4 PASS 換算を要する高度・速度・距離等の数値は本文にない。
P2-5 PASS note投稿互換上の禁止形式はなく、直訳臭・大量英文・生ログ貼付も見当たらない。
P2-6 PASS DVIDS、VID、H.264、AACなど主要な識別子・形式名には概ね必要範囲で補足がある。
VID-1 WARN 代表フレーム確認上、左パネルは青空を伴うカラー映像というより灰色調映像に見え、右パネルの「小さなオレンジ色の物体」も独立対象としては確認が弱い。視覚観察と色・センサー解釈の分離が不足している。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像メタデータ | 「再生時間：66.0秒 | ビットレート：1,834 kbps | ファイルサイズ：約14.9 MB」 | ローカル実測値に合わせ「再生時間：66.0秒 | ビットレート：約1,939 kbps | ファイルサイズ：約16.0 MB（約15.25 MiB）」等に修正。
W-02: source_registry管理 | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です」 | 公開前に対象MP4を source_registry.csv に登録し、article_id・status・重複有無を照合する。
W-03: タイトル | 「【概要版#TBD】」 | article_id 確定後に #TBD を正式番号へ置換する。
W-04: 略語補足 | 「右がグレースケール（IRとみられる）」 | 初出で「IR（赤外線）」などの日本語補足を追加する。
W-05: 視覚観察 | 「左がカラー（可視光とみられる）」「白い雲・青空の背景」「右パネル（グレースケール）：同様の場面でオレンジ色とみられる小さな物体が確認できる」 | 「左は灰色調の映像に見えるが、可視光かどうかは確認できない」「右パネルではオレンジ色の照準表示が確認できる。独立した物体色としては確認不能」など、フレームで確認できる範囲に限定する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---