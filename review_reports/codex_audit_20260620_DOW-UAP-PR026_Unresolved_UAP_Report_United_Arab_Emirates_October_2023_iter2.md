---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 3
UNVERIFIABLE: 0
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは検出されない。
P1-1a BLOCK source_registry.csv / workflow.db に対象 PR026 動画記事の登録が確認できず、タイトルも「#TBD」のまま。
P1-1b BLOCK 出典・メタデータの WAR.GOV がトップページ https://www.war.gov/UFO/ のみで、対象資料の直接URLが本文に明示されていない。
P1-1c PASS Release Date は 2026年05月08日で、metadata/files_catalog.csv の PR026 行「5/8/26」と整合する。
P1-2 PASS 再生時間・解像度・動画形式・音声ありの技術メタデータは thumbnails metadata.json と概ね整合する。
P1-5 WARN source_registry 未登録のため、status、重複、公開管理、article_id 連番の正式整合が未完了。
P2-1 WARN 構成上「注意点」見出しが独立しておらず、末尾に公開前管理メモが本文として残っている。
P2-2 PASS DVIDS は初出で「国防映像情報配信サービス」と補足され、未説明の主要軍事略語は目立たない。
P2-3 PASS 視覚確認情報とファイル名・メタデータ由来情報は分離され、物体正体・種別・意図の断定は避けられている。
P2-4 PASS 単位換算を要するノット・フィート・MPH等の数値は本文に出ていない。
P2-5 WARN AI解析メモは「8フレーム・5秒間隔」とするが、thumbnails metadata.json では frame_count 9 と記録されている。
P2-6 PASS 日本語読者向けに United Arab Emirates、動画、DVIDS、FHD 等の補足があり、過度に長い注釈もない。
IMG-1 PASS 画像記事追加チェックとして、視覚観察と推定表現は概ね分離され、「移動」「追跡」「消失」等の断定はない。
IMG-2 PASS 「IRセンサーと推定されるが確認できない」など、機器・物体解釈には留保が付いている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry整合性 | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | registry登録、article_id確定、status・重複状態確認を完了した状態にする。
W-02: 記事構成 | 「⚠️ **source_registry 未登録：** ...」 | 公開用本文から管理メモを除外し、必要なら監査・管理側に分離する。
W-03: AI解析メモ | 「映像フレーム目視確認済み（8フレーム・5秒間隔）」 | thumbnails metadata.json の frame_count 9 に合わせるか、実際に確認した枚数だけを明記する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---