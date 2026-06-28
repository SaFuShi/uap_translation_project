---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 3
WARN: 4
UNVERIFIABLE: 0
PASS: 7
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、ネスト箇条書き、Codex注釈ブロックは検出されません。
P1-1-FILENAME PASS files_catalog.csv の動画行に対象ファイル名 DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October_2024.mp4 が存在します。
P1-1-RELEASE BLOCK ドラフトは Release Date を 2026年05月22日としていますが、files_catalog.csv の対象動画行は 5/8/26 で不一致です。
P1-1-SOURCE BLOCK 出典・メタデータの WAR.GOV が https://www.war.gov/UFO/ のトップページで、対象資料の直接 war.gov URL が記事内に示されていません。
P1-1-INCIDENT PASS Incident Date はファイル名由来の 2024年10月として明記され、具体日不明の留保があります。
P1-2-METADATA PASS ffprobe値は動画5.13秒、1920x1080、30fps、H.264、AAC、約629KBで、本文の技術記述と概ね整合します。
P1-3-ABBREV WARN IIR/IR が本文で使われていますが、IIR は未説明で、IR との関係も不明です。
P1-5-REGISTRY WARN source_registry.csv に対象行がなく、ドラフト自身も source_registry 未登録・article_id 未付番と記載しています。
P2-1-STRUCTURE WARN 標準構成上の独立した「注意点」セクションがありません。
P2-1-POINTS PASS 「この資料の要点」は3項目の番号付き太字で記述されています。
P2-3-OBJECTIVITY PASS 物体種別・行動意図を断定せず、視覚確認情報とファイル名・メタデータ由来情報を分離しています。
P2-5-NOTEFORMAT PASS note投稿互換上の禁止形式は検出されません。
P2-5-EDITORIAL WARN 「note転記後にこの行を削除」という編集指示が本文中に残っています。
IMG-1 PASS 画像記事として、視覚観察と解釈は概ね分離され、「確認できない」「推定されるが確認できない」などの留保があります。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: AI読解/要点 | IIR/IRセンサーとみられるグレースケールの俯瞰映像です。 | 「IRセンサーと推定されるが確認できない」に統一し、IIRを使う場合は初出で補足する。
W-02: メタデータ/末尾注記 | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前に source_registry 登録と article_id 付番を完了し、本文注記を削除または管理用メモへ移す。
W-03: 記事構成 | 独立した「注意点」セクションがない。 | 「## 注意点」を設け、映像のみから断定できない事項を短く整理する。
W-04: 代表フレーム | → 使用ファイル：thumbnails/.../frame_0000.png（note転記後にこの行を削除） | note投稿前に編集指示行を削除し、必要なら画像キャプションのみ残す。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---