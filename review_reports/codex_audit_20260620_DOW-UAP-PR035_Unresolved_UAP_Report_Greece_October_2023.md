---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 1
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-RELEASE BLOCK ドラフトの Release Date は 2026年05月22日だが、metadata/files_catalog.csv と metadata/uap-data.csv の対象PR035行は 5/8/26 であり、公開日メタデータが一致しない。
P1-1-LOCATION PASS Related Location は Greece と記載され、metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-DVIDS PASS DVIDS ID 1006082 と DVIDS URL https://www.dvidshub.net/video/1006082 は metadata/files_catalog.csv の dvids_video_id と一致する。
P1-1-RELATED PASS 関連PDF URL は metadata/files_catalog.csv の dow-uap-d35-mission-report-greece-october-2023.pdf と一致する。
P1-2 UNVERIFIABLE ローカル実体MP4またはffprobe出力ファイルを確認できず、ドラフト記載の24.5秒・685 kbps・約2.1 MBは独立検証できない。
P1-3 PASS DVIDS は初出で「国防映像情報配信サービス」と補足されている。
P1-5 WARN source_registry.csv には同一DVIDS IDのPDF #044のみ登録があり、対象MP4記事は未登録。ドラフト末尾にも source_registry 未登録と明記されている。
P2-1 WARN タイトルに「#TBD」が残り、本文中に「note転記後にこの行を削除」という作業用注記が残っている。
P2-2 WARN 「IR」が初出で日本語補足されていない。
P2-3 PASS 物体の正体・種別・行動意図は断定せず、確認事実と推定を概ね分離している。
P2-4 PASS 換算を要する高度・速度・距離等の数値は本文にない。
P2-5 PASS note投稿互換上の禁止形式はなく、直訳臭・大量英文・生ログ貼付も見当たらない。
P2-6 PASS DVIDS、VID、H.264、AACなど主要な識別子・形式名には概ね必要範囲で補足がある。
VID-1 PASS 視覚観察とファイル名・メタデータ由来情報がセクション単位で分離されている。
VID-2 PASS 「移動」「追跡」「消失」「分裂」等を確定事実として断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry管理 | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です」 | 公開前に対象MP4を source_registry.csv に登録し、article_id・status・重複有無を照合する。
W-02: タイトル・作業注記 | 「【概要版#TBD】」「note転記後にこの行を削除」 | article_id 確定後に #TBD を置換し、作業用注記を本文から削除する。
W-03: 略語補足 | 「グレースケールの空映像（IRセンサーと推定されるが確認できない）」 | 初出で「IR（赤外線）センサーと推定されるが確認できない」など日本語補足を追加する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---