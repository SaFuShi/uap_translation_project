---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 7
UNVERIFIABLE: 0
PASS: 6
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出なし。
P1-1-METADATA PASS metadata/files_catalog.csv 上の file_name / agency / release_date / AOR / VID / DVIDS ID と本文主要メタデータは一致。
P1-1-SOURCE_REGISTRY BLOCK review_logs/source_registry.csv に DOW-UAP-PR083 の登録なし。本文末尾にも source_registry 未登録・article_id 未付番と明記されており、公開前整合性を満たさない。
P1-1-DATES PASS Release Date は 2026年05月22日形式、Incident Date はファイル名由来の 2020年10月7日として本文内で一貫。
P1-2-META PASS duration 274.07秒、1280×720、H.264、30fps、音声ありは thumbnails metadata / ffprobe と整合する。
P1-5-DUP WARN source_registry 未登録のため、status・SHA重複・公開済み重複の照合が未完了。
P2-1-STRUCTURE WARN 「注意点」「免責」に相当する独立セクションがなく、チェックリストの構成順から欠落。
P2-1-KEYPOINTS PASS 要点は番号付き太字で3項目。
P2-1-AI_MEMO WARN AI解析メモが出典前にあり、末尾の所定位置とは言いにくい。
P2-1-SOURCES PASS WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが出典に記載されている。
P2-2-ABBREVIATIONS WARN CENTCOM の補足が標準文言「米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍」より不足している。
P2-3-OBJECTIVITY WARN 「観測映像」「観測した」表現があり、センサー資料では「記録された」寄りが望ましい。
IMG-OBSERVATION WARN タイトル・要点で「IRグレースケール俯瞰映像」と断定調の表現がある一方、本文では「IRセンサーと推定されるが確認できない」としており、IR種別の事実/推定の分離が不十分。
P2-5-WORKLINE WARN note転記作業用の「使用ファイル」削除指示行が本文内に残っている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry整合性 | source_registry 未登録 | source_registry登録後に status・hash・重複照合結果を確認する。
W-02: 記事構成 | 「## この資料の要点」「## AI読解」「## 出典」のみで、注意点・免責の独立セクションがない | 「## 注意点」「## 免責」を独立セクションとして追加する。
W-03: AI解析メモ | 「**AI解析メモ：** 動画ファイル。ffprobeによる技術情報取得済み...」 | AI解析メモを出典・免責の後ろなど末尾所定位置へ移動する。
W-04: 文書メタデータ | CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）
W-05: 表現の客観性 | 「UAP観測映像」「CALLSIGNがUAPを観測した事案」 | 「UAPとして記録された映像」「CALLSIGNがUAPを記録したとされる事案」
W-06: 画像記事表現 | 「市街地のIRグレースケール俯瞰映像」 | 「グレースケール俯瞰映像。IRセンサー映像の可能性はあるが、本文では断定しない」などに統一する。
W-07: 代表フレーム挿入行 | → 使用ファイル：thumbnails/DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP/frame_0000.png（note転記後にこの行を削除） | 公開用本文から作業用行を削除する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---