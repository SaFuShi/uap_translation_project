---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 3
WARN: 4
UNVERIFIABLE: 0
PASS: 7
MODEL: gpt-5
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、ネスト箇条書き、Codex注釈ブロックの混入は確認されない。
P1-1-FILE PASS File Name は metadata/files_catalog.csv および raw_media/video の対象ファイル名と一致する。
P1-1-RELEASE BLOCK files_catalog.csv の release_date は 5/8/26 だが、本文は Release Date を 2026年05月22日としており一次メタデータと不一致。
P1-1-SOURCE BLOCK 出典・メタデータの WAR.GOV が https://www.war.gov/UFO/ のトップページのみで、files_catalog.csv にある対象資料の直接URLが本文に記載されていない。
P1-1-DATE BLOCK Incident Date は「2024年10月・具体的な日付は不明」としながら、要点で「PR031・PR032と同一日」と記述しており、日付不明情報から同一日を推定している。
P1-2 PASS 動画の解像度、フレームレート、再生時間、音声AAC、ファイルサイズ概算はローカル ffprobe / thumbnail metadata と大きく矛盾しない。
P1-3 PASS DVIDS は初出で「国防映像情報配信サービス」と補足されている。
P1-5 WARN source_registry.csv に対象記事の登録が確認できず、article_id・status・重複確認の正式管理が未完了。
P2-1-STRUCT PASS 冒頭注意、文書メタデータ、要点、AI読解、注意点、出典、免責に相当する構成は揃っている。
P2-1-KEYPOINTS PASS 「この資料の要点」は3項目の番号付き太字で記述されている。
P2-1-AIMEMO WARN AI解析メモが注意点・出典より前に置かれており、チェックリストの「末尾の所定位置」要件から外れる。
P2-3 PASS 視覚確認できる情報と未確認事項の留保が概ね分離され、物体種別・意図の断定は避けられている。
P2-5-EDITORIAL WARN 「note転記後にこの行を削除」という編集指示が本文中に残っている。
P2-5-MGMT WARN 末尾の source_registry 未登録メモは公開前管理情報であり、公開用本文からは分離が必要。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry整合性 | 「⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | 公開前に registry 登録、article_id 確定、status・重複状態の確認を完了する。
W-02: AI解析メモ位置 | 「**AI解析メモ：** 動画ファイル。ffprobeによる技術情報取得済み。」 | AI解析メモをチェックリスト上の所定位置に移動する。
W-03: 編集指示混入 | 「→ 使用ファイル：...（note転記後にこの行を削除）」 | 公開用本文から編集指示行を削除し、画像キャプションのみ残す。
W-04: 公開前管理メモ | 「source_registry 未登録・article_id の付番が未実施」 | 管理メモはレビュー・運用ログ側に分離し、note本文には掲載しない。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---