---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・複雑ネスト・Codex注釈ブロックは検出なし。
P1-1 BLOCK メタデータ不整合あり。metadata/uap-csv-cache.csv と files_catalog.csv では Release Date は 2026年06月12日、Incident Date は October, 2023 だが、本文は 2026年05月22日・Release 02・月日不明としている。
P1-2 PASS ffprobe由来の動画情報は概ね整合。310 kbps は video stream bitrate として確認可能。
P1-3 PASS FBI・DVIDS は日本語補足あり。該当する基地名・部隊名・MGRS・機密区分の未説明問題はなし。
P1-4 PASS Misrep・MDR・JSIR・CSP/MRO 等の番号類は本文に該当なし。
P1-5 PASS ローカル確認範囲では同一記事ドラフト重複は主要問題として検出なし。
P2-1 WARN 構成は概ね標準順だが、末尾に明示的な免責セクションがない。
P2-2 PASS 軍事略語・専門用語の未補足による主要な読解支障はなし。
P2-3 PASS 視覚確認情報と推定・未確認情報は概ね分離されている。
P2-4 PASS 換算対象となる速度・高度・距離等の主要単位は本文に該当なし。
P2-5 WARN note転記用の作業メモ行が本文に残っている。
P2-6 PASS 日本語読者向けの組織名・略語補足は必要範囲で記載あり。
P3 WARN source_registry 未登録・article_id 未付番のため、公開前の registry 整合性が未完了。
IMG-1 PASS 画像記事として、視覚観察と解釈は概ね分離され、「推定」「確認できない」の留保もある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 構成 | （明示的な「免責」セクションなし） | 出典後に「## 免責」を置き、公開資料・映像フレーム確認に基づく概要であり物体の正体や意図を断定しない旨を短く明記する。
W-02: 代表フレーム | → 使用ファイル：thumbnails/FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023/frame_0030.png（note転記後にこの行を削除） | note投稿本文から作業メモ行を削除し、必要なら画像キャプションのみ残す。
W-03: source_registry | ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。公開前に source_registry への登録が必要です。 | 公開前に source_registry 登録と article_id 付番を完了し、本文末尾の内部管理メモは削除する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---