---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 5
UNVERIFIABLE: 0
PASS: 8
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・複雑ネスト・Codex注釈ブロックは確認されない。
P1-1-FILE BLOCK review_logs/source_registry.csv に DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP.mp4 の登録が確認できない。
P1-1-URL PASS WAR.GOV公開ページとDVIDS直接URLが分離され、DVIDS ID 1007804 と一致している。
P1-1-DATE PASS Release Date は YYYY年MM月DD日形式、Incident Date はファイル名由来の 2021年1月3日 と矛盾しない。
P1-2-META PASS duration 297.4秒、1280×720、H.264、30fps、音声ありは thumbnails metadata と整合する。
P1-3-ORG WARN CENTCOM の補足が標準文言「米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍」より不足している。
P1-5-DUP WARN source_registry 未登録のため、status・SHA重複・公開済み重複の照合が未完了。
P2-1-STRUCT WARN 構成上、「注意点」「免責」に相当する独立セクションが不足している。
P2-1-KEY PASS 要点は3項目の番号付き太字で記述されている。
P2-1-SOURCE PASS 出典セクションにWAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-3-OBJECTIVITY WARN 「観測映像」「観測した事案」の表現があり、センサー資料では「記録映像」「記録された事案」寄りが望ましい。
IMG-1-SEPARATION WARN オレンジ色マーカーについて、視覚観察と「UAP対象の位置を示す」解釈が同一文内で近接している。
IMG-2-DYNAMIC PASS 移動・追跡・消失・分裂等を映像目視だけで確定断定していない。
M5-DVIDS PASS files_catalog.csv の dvids_video_id 1007804 と記事内DVIDS URLが一致している。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）
W-02: source_registry整合性 | source_registry 未登録 | source_registry登録後に status・hash・重複照合結果を確認する
W-03: 記事構成 | AI解析メモの後に出典へ進み、独立した注意点・免責がない | 「## 注意点」「## 免責」を独立セクションとして追加する
W-04: 表現の客観性 | UAP観測映像／UAPを観測した事案 | UAP記録映像／UAPとして記録された事案
W-05: 画像記事 | オレンジ色の小さなマーカーが複数確認でき、これらがUAP対象の位置を示すマーカーとみられますが確認できません。 | オレンジ色の小さなマーカーが複数表示されている。何を示す表示かは確認できない。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---