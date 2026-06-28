---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 5
UNVERIFIABLE: 0
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマット（Markdown表・引用ブロック・長文英文引用・2階層以上ネスト・Codex注釈ブロック）は検出されない。
P1-1 PASS ファイル名・公開日・DVIDS ID・技術メタデータは files_catalog / ローカル動画情報と概ね整合する。
P1-2 PASS 速度・高度・FL・Zulu時刻などの換算対象数値は本文に出ておらず、数値矛盾は検出されない。
P1-3 PASS DVIDS は初出で補足され、MGRS・Misrep・MDR・JSIR・機密区分など未補足対象語は本文に出ていない。
P1-5 PASS 同一ファイル名の既存公開記事・明示的な重複・BLOCK状態は確認されない。
P2-1 WARN 記事構成で「注意点」および「免責」セクションが独立しておらず、所定順序から外れている。
P2-2 WARN CENTCOM / AOR の初出補足が標準形に不足している。
P2-3 WARN センサー映像記事で「観測映像」「観測した事案」など、記録ベースではなく観測断定寄りの表現が残っている。
P2-4 PASS 単位換算対象となるフィート・ノット・MPH・重量などは本文に出ておらず、換算誤りは検出されない。
P2-5 PASS 本文はnote互換の単純な構造で、表・引用ブロック・OCRログ大量貼付・複雑ネストは検出されない。
P2-6 PASS 日本語読者向けの基礎補足は概ねあり、DVIDS・CENTCOM・AORなどは最低限の説明がある。
P3-1 WARN source_registry.csv に当該動画が未登録で、article_id 付番・公開管理上の整合性が未完了。
IMG-1 WARN 「シアン点が示す別の物体」「UAP候補」など、画面表示の視覚観察とUAP対象解釈が一部近接している。
IMG-4 PASS 「タンカーとみられる」「確認困難」など、画像のみの判断には概ね留保が付いている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 記事構成 | 「## AI読解」後に独立した注意点・免責セクションがない | 「## 注意点」「## 免責」を出典前後の所定位置に独立セクションとして追加する
W-02: 軍事略語 | 「CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア）」 | 「USCENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）」「AOR（Area of Responsibility：担当作戦地域）」の形に寄せる
W-03: 客観表現 | 「UAP観測映像」「UAPを観測した事案」 | 「UAPが記録された映像」「UAPが記録された事案とされています」など記録ベースにする
W-04: source_registry | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施」 | 公開前に source_registry.csv へ登録し、article_id・公開管理情報を確定する
W-05: 画像記事 | 「UAP対象はこの大型船ではなく、周囲のシアン点が示す別の物体とみられます」「シアン点複数（UAP候補）」 | 「周囲にシアン点が複数表示されている。これらが何を示すかは本文だけでは確認できない」程度に留める
---WARN_DETAILS_END---
---CODEX_AUDIT_END---