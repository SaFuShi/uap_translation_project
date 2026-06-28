---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1A PASS File Name・Agency・Release Date・Related Location・File Type・DVIDS ID は metadata/files_catalog.csv およびサムネイルメタデータと概ね一致する。
P1-1B WARN Incident Date が metadata/files_catalog.csv / uap-data.csv の "October, 2023" より粗く、「具体的な月・日付は不明」としている。
P1-1C PASS 動画記事として WAR.GOV 公開ページに加え DVIDS 直接URLが記載されている。
P1-2A WARN 映像技術メタデータに不一致あり。metadata.json は bit_rate_kbps=1369、frame_count=1だが、本文は「1,264 kbps」「2フレーム」と記載している。
P1-2B PASS ノット・フィート等の単位換算誤りは該当記述なし。
P1-3 PASS FBI・DVIDS など主要略語は初出付近で日本語補足されている。
P1-5 PASS 対象ファイルは metadata/files_catalog.csv に候補として存在し、DVIDS ID 1010276 と一致する。
P2-1A WARN 標準構成上の「免責」セクションが出典後に独立して存在しない。
P2-1B PASS 「この資料の要点」は3項目の番号付き太字で構成されている。
P2-1C PASS デジタル再現映像・視覚観察記事として冒頭の注意書きがある。
P2-3 PASS 視覚確認情報とファイル名・メタデータ由来情報は概ね分離され、推定表現も使用されている。
P2-5 PASS note投稿互換上の禁止フォーマットは検出されない。
P3-1 BLOCK review_logs/source_registry.csv に PR006 / DVIDS 1010276 の登録が見当たらず、article_id・status・source_registry整合性を満たさない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | Incident Date：2023年（ファイル名「2023」より。具体的な月・日付は不明） | 「Incident Date：2023年10月（metadata/files_catalog.csv より。具体的な日付は不明）」へ修正。
W-02: 映像メタデータ / AI解析メモ | 再生時間：21.3秒 | ビットレート：1,264 kbps / 映像フレーム目視確認済み（2フレーム：frame_0000黒） | 「ビットレート：約1,369 kbps」「映像フレーム目視確認済み（1フレーム：frame_0000黒）」へ修正。
W-03: 記事構成 | 出典セクション後に独立した免責セクションなし | 出典後に「## 免責」相当の短い免責文を追加。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---