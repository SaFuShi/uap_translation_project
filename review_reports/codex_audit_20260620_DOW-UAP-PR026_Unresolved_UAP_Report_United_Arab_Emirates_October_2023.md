---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 3
WARN: 4
UNVERIFIABLE: 0
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは検出されない。
P1-1a BLOCK source_registry.csv / workflow.db に対象 PR026 動画記事の登録が確認できず、タイトルも「#TBD」のまま。
P1-1b BLOCK Release Date が本文では「2026年05月22日」だが、metadata/files_catalog.csv の PR026 行は「5/8/26」で不一致。
P1-1c BLOCK 出典・メタデータの WAR.GOV がトップページ https://www.war.gov/UFO/ のみで、files_catalog.csv 上の直接URLが本文に明示されていない。
P1-2 PASS 再生時間・解像度・動画形式・音声ありの技術メタデータは ffprobe 実測値と概ね整合する。
P1-5 WARN source_registry 未登録のため、status、重複、公開管理、article_id 連番の正式整合が未完了。
P2-1 WARN 構成上「注意点」見出しが独立しておらず、末尾に公開前管理メモが本文として残っている。
P2-2 PASS DVIDS は初出で「国防映像情報配信サービス」と補足され、未説明の主要軍事略語は目立たない。
P2-3 PASS 視覚確認情報とファイル名・メタデータ由来情報は分離され、物体正体・種別・意図の断定は避けられている。
P2-4 PASS 単位換算を要するノット・フィート・MPH等の数値は本文に出ていない。
P2-5a WARN 「note転記後にこの行を削除」という作業指示が本文に残っている。
P2-5b WARN AI解析メモは「8フレーム・5秒間隔」とするが、thumbnails metadata.json では frame_count 9 と記録されている。
P2-6 PASS 日本語読者向けに United Arab Emirates、動画、DVIDS、FHD 等の補足があり、過度に長い注釈もない。
IMG-1 PASS 画像記事追加チェックとして、視覚観察と推定表現は概ね分離され、「移動」「追跡」「消失」等の断定はない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry整合性 | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | 公開前に registry 登録、article_id 確定、status・重複状態の確認を完了する。
W-02: 記事構成 | 「⚠️ **source_registry 未登録：** ...」 | 公開用本文から管理メモを除外し、必要なら監査・管理側に分離する。
W-03: 投稿前作業指示 | 「→ 使用ファイル：...（note転記後にこの行を削除）」 | note本文に残さず、画像配置作業用メモとして管理側に移す。
W-04: AI解析メモ | 「映像フレーム目視確認済み（8フレーム・5秒間隔）」 | thumbnails metadata.json の frame_count 9 に合わせるか、実際に確認した枚数だけを明記する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---