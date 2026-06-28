---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 5
UNVERIFIABLE: 0
PASS: 8
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・複雑ネスト・Codex注釈ブロックは確認されない。
P1-1-FILE BLOCK review_logs/source_registry.csv に DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAP_s.mp4 の登録が確認できない。
P1-1-URL PASS WAR.GOV公開ページとDVIDS直接URLが分離され、DVIDS ID 1007816 と files_catalog.csv が一致している。
P1-1-DATE PASS Release Date は YYYY年MM月DD日形式、Incident Date はファイル名由来の 2020年10月29日 と矛盾しない。
P1-2-META PASS duration 240.57秒、1920×1080、H.264、30fps、音声ありは thumbnails metadata / ffprobe と整合する。
P1-3-ORG WARN CENTCOM の補足が標準文言「米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍」より不足している。
P1-5-DUP WARN source_registry 未登録のため、status・SHA重複・公開済み重複の照合が未完了。
P2-1-STRUCT WARN 構成上、「注意点」「免責」に相当する独立セクションが不足している。
P2-1-KEY PASS 要点は3項目の番号付き太字で記述されている。
P2-1-SOURCE PASS 出典セクションにWAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-3-OBJECTIVITY WARN 「観測事案」「観測した」表現があり、センサー資料では「記録された」寄りが望ましい。
IMG-1-SEPARATION PASS 視覚観察・ファイル名由来情報・未確認事項は概ね分離されている。
IMG-2-DYNAMIC PASS 移動・追跡・消失・分裂等を映像目視だけで確定断定していない。
P2-5-WORKLINE WARN note転記作業用の「使用ファイル」削除指示行が本文内に残っている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）
W-02: source_registry整合性 | source_registry 未登録 | source_registry登録後に status・hash・重複照合結果を確認する
W-03: 記事構成 | AI解析メモの後に出典へ進み、独立した注意点・免責がない | 「## 注意点」「## 免責」を独立セクションとして追加する
W-04: 表現の客観性 | 「3つの速く動くUAP」を観測したとされる事案／観測事案 | 「3つの速く動くUAP」として記録されたとされる事案／記録事案
W-05: 代表フレーム挿入行 | → 使用ファイル：thumbnails/DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAP_s/frame_0000.png（note転記後にこの行を削除） | 公開用本文から作業用行を削除する
---WARN_DETAILS_END---
---CODEX_AUDIT_END---