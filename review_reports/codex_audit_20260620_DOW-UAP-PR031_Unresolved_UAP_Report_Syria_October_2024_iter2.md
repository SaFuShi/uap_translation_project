---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 2
UNVERIFIABLE: 0
PASS: 12
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 PASS File Name・Agency・Release Date・Related Location・DVIDS ID は metadata/files_catalog.csv の対象MP4行および metadata/uap-csv-cache.csv と整合している。
P1-1-INCIDENT PASS Incident Date はファイル名由来の 2024年10月として明記され、具体日不明の留保がある。
P1-1-SOURCE PASS WAR.GOV公開ページに加え、対象映像の DVIDS 直接URLが示されている。
P1-2 PASS 動画メタデータの再生時間・解像度・フレームレート・形式・音声記述に重大な矛盾はない。
P1-3 PASS DVIDS は初出で日本語補足され、その他の重大な未説明略語は検出されない。
P1-5 WARN source_registry.csv に当該MP4記事の登録がなく、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P2-1 WARN タイトルに「#TBD」が残っており、公開前の記事番号・article_id 確定が未完了。
P2-1-POINTS PASS 「この資料の要点」は3項目の番号付き太字で記述されている。
P2-3 PASS 物体の正体・種別・行動意図は断定せず、視覚確認情報とファイル名・メタデータ由来情報を分離している。
P2-4 PASS 換算を要する高度・速度・距離などの単位記述は本文にない。
P2-5 PASS note投稿互換上の禁止形式はなく、直訳臭・大量英文・生ログ貼付も見当たらない。
P2-6 PASS Syria、VID、MP4、FHD、H.264、AAC など読者向けに必要な最低限の補足がある。
IMG-1 PASS 視覚観察と解釈は分離され、「推定されるが確認できない」「明確に確認できない」などの留保が維持されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry管理 | ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。公開前に source_registry への登録が必要です。 | 公開前に source_registry.csv へ登録し、article_id 付番後に当該注記を削除または管理用メモへ分離する。
W-02: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR031：シリア2024年10月UAPとされる事案映像（ファイル名より）──Syria・米国防省公開・Release 02 | article_id 確定後に「#TBD」を正式番号へ置換する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---