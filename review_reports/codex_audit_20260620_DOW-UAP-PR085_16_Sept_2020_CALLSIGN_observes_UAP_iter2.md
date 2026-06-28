---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 8
UNVERIFIABLE: 0
PASS: 6
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出なし。
P1-1-METADATA PASS metadata/files_catalog.csv 上の file_name / agency / release_date / AOR / VID / DVIDS ID と本文主要メタデータは一致。
P1-1-SOURCE_REGISTRY BLOCK review_logs/source_registry.csv に DOW-UAP-PR085 の登録なし。本文末尾にも source_registry 未登録・article_id 未付番と明記されており、公開前整合性を満たさない。
P1-1-DATES PASS Release Date は 2026年05月22日形式、Incident Date はファイル名由来の 2020年9月16日として本文内で一貫。
P1-2-META PASS ffprobe / thumbnails metadata 上の 284.17秒、1280×720、H.264、30fps、音声ありと整合。
P1-5-DUP WARN source_registry 未登録のため、status・SHA重複・公開済み重複の照合が未完了。
P2-1-STRUCTURE WARN 「注意点」「免責」に相当する独立セクションがなく、チェックリストの構成順から欠落。
P2-1-KEYPOINTS PASS 要点は番号付き太字で3項目。
P2-1-AI_MEMO WARN AI解析メモが出典前にあり、末尾の所定位置とは言いにくい。
P2-1-SOURCES PASS WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが出典に記載されている。
P2-2-ABBREVIATIONS WARN CENTCOM の補足が標準文言「米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍」より不足している。
P2-3-OBJECTIVITY WARN 「観測映像」「観測した」表現があり、センサー資料では「記録された」寄りが望ましい。
P2-3-INFERENCE WARN 「2機のCALLSIGN」「PR084と連続する可能性」は、ファイル名・メタデータから確認できる事実を超える推定として見える。
IMG-OBSERVATION WARN タイトル・要点・AI解析メモで「IR」と断定調の表現がある一方、本文では「IRセンサー由来の可能性はあるが確認できない」としており、IR種別の事実/推定の分離が不十分。
P1-1-SOURCE_CONTEXT WARN metadata/uap-csv-cache.csv のAARO説明にある「full-motion video camera由来の可能性」「chain-of-custody不足」「情報提供目的で分析判断ではない」趣旨が本文に十分反映されていない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry整合性 | source_registry 未登録 | source_registry登録後に status・hash・重複照合結果を確認する。
W-02: 記事構成 | 「## この資料の要点」「## AI読解」「## 出典」のみで、注意点・免責の独立セクションがない | 「## 注意点」「## 免責」を独立セクションとして追加する。
W-03: AI解析メモ | 「**AI解析メモ：** 動画ファイル。ffprobeによる技術情報取得済み...」 | AI解析メモを出典・免責の後ろなど末尾所定位置へ移動する。
W-04: 文書メタデータ | CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）
W-05: 表現の客観性 | 「UAP観測映像」「CALLSIGNがUAPを観測した事案」 | 「UAPとして記録された映像」「CALLSIGNがUAPを記録したとされる事案」
W-06: 推定表現 | 「2機のCALLSIGNがUAPを観測した事案の映像とされています。PR084（9月17日）と連続する可能性があります。」 | 「ファイル名には CALLSIGN_CALLSIGN_observes_UAP と記載されています。」程度に留め、連続性は根拠がある場合のみ記載する。
W-07: 画像記事表現 | 「均一グレーIR映像」「グレースケールIR映像」「均一グレーIR」 | 「グレースケール映像。IRセンサー映像の可能性はあるが、本文では断定しない」などに統一する。
W-08: 出典文脈 | 「本記事は約284秒（4分44秒）のグレースケールIR映像クリップを扱います。」 | AARO説明に基づき「フルモーション映像カメラ由来の可能性」「チェーン・オブ・カストディ未確立」「分析判断ではない説明文」の留保を注意点に加える。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---