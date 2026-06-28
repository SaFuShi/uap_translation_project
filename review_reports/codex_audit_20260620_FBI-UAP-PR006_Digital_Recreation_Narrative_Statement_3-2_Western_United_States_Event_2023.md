---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 4
UNVERIFIABLE: 0
PASS: 8
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1A BLOCK Release Date が metadata/files_catalog.csv の release_date=6/12/26 と不一致。ドラフトは「2026年05月22日」「Release 02」と記載している。
P1-1B WARN Incident Date が metadata/files_catalog.csv の "October, 2023" より粗く、「2023年」のみになっている。
P1-1C PASS ファイル名・Agency・Related Location・DVIDS ID・File Type の基本整合性はローカル資料と一致する。
P1-2A WARN 技術メタデータに不一致あり。ffprobe/metadata.json は bit_rate 約1,369 kbps、frame_count=1だが、本文は「1,264 kbps」「2フレーム」と記載している。
P1-2B PASS ノット・フィート等の単位換算誤りは該当記述なし。
P1-3 PASS FBI・DVIDS など主要略語は初出付近で日本語補足されている。
P2-1A WARN 標準構成上の「免責」セクションが出典後に独立して存在しない。
P2-1B PASS 「この資料の要点」は3項目の番号付き太字で構成されている。
P2-3 PASS 視覚確認情報とファイル名・メタデータ由来情報は概ね分離され、推定表現も使用されている。
P2-5A WARN 「note転記後にこの行を削除」という作業指示が本文に残っている。
P2-5B PASS note投稿互換上の禁止フォーマットは検出されない。
IMG-1 PASS 画像・映像記事として、黒画面の視覚観察とCGI等の解釈は概ね分離されている。
P3-1 BLOCK review_logs/source_registry.csv に PR006 / DVIDS 1010276 の登録が見当たらず、article_id・status・source_registry整合性を満たさない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | Incident Date：2023年（ファイル名「2023」より。具体的な月・日付は不明） | files_catalog.csv を根拠にするなら「Incident Date：2023年10月（files_catalog.csv より。具体的な日付は不明）」へ修正。
W-02: 映像メタデータ / AI解析メモ | 再生時間：21.3秒 | ビットレート：1,264 kbps / 映像フレーム目視確認済み（2フレーム：frame_0000黒） | 「ビットレート：約1,369 kbps」「映像フレーム目視確認済み（1フレーム：frame_0000黒）」へ修正。
W-03: 記事構成 | 出典セクション後に独立した免責セクションなし | 出典後に「## 免責」相当の短い免責文を追加。
W-04: 代表フレーム行 | → 使用ファイル：...（note転記後にこの行を削除） | 公開用本文から作業指示を削除し、必要なら画像キャプションのみ残す。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---