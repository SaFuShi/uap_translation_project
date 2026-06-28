---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 6
UNVERIFIABLE: 0
PASS: 8
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS note互換禁止形式（Markdown table、引用ブロック、長文英文引用、2階層以上ネスト箇条書き、Codex注釈ブロック）は検出されない。
P1-1 WARN source_registry 未登録で article_id 未付番のため、タイトルに #TBD が残っている。
P1-2 PASS Incident Date、Release Date、DVIDS ID、動画メタデータは files_catalog・ffprobe・thumbnail metadata と概ね整合する。
P1-3 WARN CENTCOM の初出補足が標準形「米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍」より弱い。
P1-5 PASS files_catalog に該当行があり、ローカル raw_media/video と thumbnails の実体も確認できる。
P2-1 WARN 標準構成のうち「注意点」「免責」に相当する独立セクションがなく、note転記用の削除指示行が本文中に残っている。
P2-2 PASS DVIDS、AOR、動画/MP4など主要用語には最低限の日本語補足がある。
P2-3 WARN 「観測映像」「UAPを観測した事案」が、センサー記録としての中立表現よりやや断定的。
P2-4 PASS 換算対象となる高度・速度・距離などの数値はなく、秒/分・解像度の記述に問題はない。
P2-5 PASS 直訳臭や大量OCRログ、長文引用、表組みは見当たらず、読みやすさは概ね保たれている。
P2-6 PASS 日本語読者向けの基本注釈は概ね付与されている。
IMG-1 WARN 「IR映像」がタイトル・本文で事実として反復される一方、確認不能の留保が一部に限られている。
IMG-2 WARN ファイル名の CALLSIGN_CALLSIGN から「2機」と読むのは、ファイル名・映像だけでは根拠が不足する。
IMG-3 PASS 移動・追跡・消失・分裂などの動作を映像から確定事実として断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ/タイトル | # 【概要版#TBD】... / source_registry 未登録 | article_id 付番後に #TBD を実番号へ置換し、source_registry 登録状態と一致させる。
W-02: 文書メタデータ | CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）程度に補足する。
W-03: 記事構成 | → 使用ファイル：...（note転記後にこの行を削除） | 公開用本文から削除し、「注意点」「免責」に相当する短い独立セクションを追加する。
W-04: タイトル/要点 | 観測映像 / UAPを観測した事案の映像 | 「記録映像」「UAPとして扱われた対象が記録された映像」など、記録ベースの表現に寄せる。
W-05: タイトル/AI読解 | グレースケールIR映像 | IRであることがソース上確認できない場合は「グレースケール映像（IRの可能性はあるが未確認）」に統一する。
W-06: この資料の要点 | 2020年8月8日に2機のCALLSIGNがUAPを観測した事案 | 「CALLSIGN_CALLSIGN を含むファイル名から、2020年8月8日のUAP observation 映像とされる」程度に留める。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---