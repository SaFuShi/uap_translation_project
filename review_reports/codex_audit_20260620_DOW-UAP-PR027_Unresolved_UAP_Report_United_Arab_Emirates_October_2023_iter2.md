---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 2
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1-FILENAME BLOCK source_registry 未登録が本文で明記され、タイトルも「#TBD」のままで、article_id・正式公開管理の整合が未確定。
P1-1-SOURCE BLOCK WAR.GOV 出典が https://www.war.gov/UFO/ のトップページで、war.gov 側の対象資料直接URLが本文出典として明示されていない。
P1-1-METADATA PASS File Name、Agency、Release Date、Related Location、DVIDS ID は metadata/files_catalog.csv と整合する。
P1-1-INCIDENT PASS Incident Date はファイル名由来の 2023年10月として留保され、具体日不明も明記されている。
P1-2 PASS 再生時間・解像度・フレームレート・音声あり等は thumbnails metadata.json と整合する。
P1-5 WARN source_registry 未登録のため、status、重複、公開済み重複、連番の正式照合が完了できない。
P2-1 WARN 構成上、独立した「注意点」セクションがなく、末尾に公開前管理メモが本文として残っている。
P2-2 PASS DVIDS、VID、FHD、H.264、AACなど本文で使用される略語・形式名は概ね必要範囲で補足されている。
P2-3 PASS 視覚確認情報とファイル名・メタデータ由来情報は分離され、物体正体・種別・行動意図の断定は避けられている。
P2-4 PASS ノット・フィート・MPH等、日本向け換算を要する英米単位の本文記述は確認されない。
P2-5 PASS note投稿互換上の禁止形式はなく、直訳臭・大量英文・生ログ貼付も見当たらない。
IMG-1 PASS 視覚観察と推定表現は概ね分離され、「移動」「追跡」「消失」「分裂」等の断定はない。
IMG-2 PASS 「IRセンサーと推定されるが確認できない」「とみられる」「確認できない」など、画像・映像由来判断に留保が付いている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry整合性 | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | source_registry登録、article_id確定、status・重複状態確認を完了した状態にする。
W-02: 記事構成 | 「⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | 公開用本文から管理メモを除外し、必要な留保は独立した「注意点」セクションに整理する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---