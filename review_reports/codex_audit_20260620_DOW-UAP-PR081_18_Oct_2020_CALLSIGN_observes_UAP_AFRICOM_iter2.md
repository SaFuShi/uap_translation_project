---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出なし。
P1-1-METADATA PASS metadata/files_catalog.csv 上の file_name / agency / release_date / AOR / VID / DVIDS ID と本文主要メタデータは概ね一致。
P1-1-SOURCE_REGISTRY BLOCK review_logs/source_registry.csv に DOW-UAP-PR081 の登録なし。本文末尾にも source_registry 未登録と明記されており、公開前整合性を満たさない。
P1-1-DATES PASS Release Date は 2026年05月22日形式、Incident Date はファイル名由来の 2020年10月18日として本文内で一貫。
P1-1-SOURCE_URL PASS WAR.GOV公開ページに加え、対象映像の直接参照先として DVIDS URL が記載されている。
P1-5-STATUS PASS source_registry.csv 上で当該ファイルが BLOCK 状態になっている事実は検出されない。
P2-1-STRUCTURE WARN 「注意点」「免責」に相当する独立セクションがなく、チェックリストの構成順から欠落。
P2-1-KEYPOINTS PASS 要点は番号付き太字で3項目。
P2-1-AI_MEMO WARN AI解析メモが出典前にあり、末尾の所定位置とは言いにくい。
P2-1-SOURCES PASS WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが出典に記載されている。
P2-2-ABBREVIATIONS PASS AFRICOM、AOR、DVIDS は初出付近で日本語補足あり。
P2-3-OBJECTIVITY PASS UAP対象の正体・種別・行動意図を断定せず、「確認困難」「確認できない」と留保している。
P2-5-DRAFT_NOTE PASS note投稿互換を損なう作業メモ、Markdown表、引用ブロックは検出なし。
IMG-OBSERVATION WARN 「カラーIR俯瞰映像」と断定調の表現が複数箇所にある一方で「IRセンサー由来の可能性はあるが確認できない」とも書いており、IR種別の事実/推定の分離が不十分。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 記事構成 | 「## この資料の要点」「## AI読解」「## 出典」のみで、注意点・免責の独立セクションがない | 「## 注意点」「## 免責」を追加し、映像視覚観察記事としての限界を整理する。
W-02: AI解析メモ | 「**AI解析メモ：** 動画ファイル。ffprobeによる技術情報取得済み...」 | AI解析メモを出典・免責の後ろなど末尾所定位置へ移動する。
W-03: 画像記事表現 | 「カラーIR俯瞰映像（IRセンサー由来の可能性はあるが確認できない）」 | 「カラー俯瞰映像。IRセンサー映像の可能性はあるが、本文では断定しない」などに統一する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---