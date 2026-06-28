---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 5
UNVERIFIABLE: 0
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1a PASS File Name は metadata/files_catalog.csv および raw_media/video の対象ファイル名と一致する。
P1-1b BLOCK Release Date がドラフトでは「2026年05月22日」だが、metadata/files_catalog.csv では当該ファイルの release_date が「5/8/26」であり、一次メタデータと不一致。
P1-1c BLOCK WAR.GOV はトップページのみで、metadata/files_catalog.csv / uap-csv-cache.csv にある対象関連資料の直接URL「https://www.war.gov/medialink/ufo/release_1/dow-uap-d33-mission-report-greece-october-2023.pdf」が本文に記載されていない。
P1-1d PASS Incident Date はファイル名由来の「2023年10月」として留保され、具体日付不明も明記されている。
P1-1e PASS Related Location は files_catalog.csv の Greece と一致する。
P1-2 PASS ffprobe由来の解像度、フレームレート、再生時間、ビットレート、音声AACはローカル実測値と大きく矛盾しない。
P1-3 PASS DVIDS は初出で「国防映像情報配信サービス」と補足されている。
P1-5 WARN source_registry.csv に対象映像記事の登録が確認できず、article_id・status・重複確認の正式管理が未完了。
P2-1 WARN 構成に「注意点」および公開用の免責に相当する末尾セクションが不足し、AI解析メモも出典より前に置かれている。
P2-2 WARN 「IR」が初出で日本語補足されていない。
P2-3 WARN 「海面または空とみられる」が一部で留保なしに読め、視覚観察と解釈の分離がやや弱い。
P2-5 WARN タイトルの「#TBD」と「note転記後にこの行を削除」という編集指示が本文中に残っている。
IMG-2 PASS 「移動」「追跡」「消失」「分裂」等を映像観察から確定事実として断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry整合性 | 「⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | 公開前に source_registry 登録、article_id 確定、status・重複状態の確認を完了する。
W-02: 記事構成 | 「**AI解析メモ：** 動画ファイル。ffprobeによる技術情報取得済み。」 | 注意点セクションと免責文を追加し、AI解析メモを所定位置へ移動する。
W-03: 略語補足 | 「グレースケールの映像（IRセンサーと推定されるが確認できない）」 | 初出で「IR（赤外線）」などの日本語補足を追加する。
W-04: 表現の客観性 | 「均一なグレーの背景（海面または空とみられる）」 | 「海面または空の可能性があるが、映像のみからは確認できない」など留保を明示する。
W-05: 編集指示混入 | 「【概要版#TBD】」「→ 使用ファイル：...（note転記後にこの行を削除）」 | article_id 確定後に #TBD を置換し、作業用注記を本文から削除する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---