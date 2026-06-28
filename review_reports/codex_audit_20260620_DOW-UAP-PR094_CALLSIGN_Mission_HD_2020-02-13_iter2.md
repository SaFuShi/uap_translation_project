---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 0
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・複雑ネスト・Codex注釈ブロックは確認されない。
P1-1-FILE BLOCK review_logs/source_registry.csv に DOW-UAP-PR094_CALLSIGN_Mission_-_HD_2020-02-13.mp4 の登録が確認できない。
P1-1-URL PASS WAR.GOV公開ページとDVIDS直接URLが分離され、DVIDS ID 1007722 と一致している。
P1-1-DATE PASS Release Date は YYYY年MM月DD日形式、Incident Date はファイル名由来の 2020年2月13日 として記述されている。
P1-2-META PASS ffprobeおよび thumbnails metadata と、1280×720・H.264・30fps・約299.8秒・音声ありの記述が整合している。
P1-3-ORG WARN CENTCOM の補足が標準文言「米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍」より不足している。
P1-5-DUP WARN source_registry 未登録のため、status・SHA重複・公開済み重複の照合が未完了。
P2-1-STRUCT WARN 構成上、「注意点」「免責」に相当する独立セクションが不足している。
P2-1-KEY PASS 要点は3項目の番号付き太字で記述されている。
P2-1-SOURCE PASS 出典セクションにWAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-3-OBJECTIVITY WARN 冒頭の「グレースケールIR映像クリップ」がIR由来を断定調にしており、後続の留保表現と強さが揺れている。
P2-5-READABILITY PASS 直訳臭の強い表現や大量の生ログ貼り付けは確認されない。
IMG-1-SEPARATION PASS 視覚観察情報とファイル名・メタデータ由来情報を分ける方針が明示されている。
IMG-2-DYNAMIC PASS 移動・追跡・消失・分裂等を映像目視だけで確定断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍。AOR＝担当作戦地域）
W-02: source_registry整合性 | source_registry 未登録 | source_registry登録後に status・hash・重複照合結果を確認する
W-03: 記事構成 | AI解析メモの後に出典へ進み、独立した注意点・免責がない。 | 「## 注意点」「## 免責」を独立セクションとして追加する
W-04: 表現の客観性 | 本記事は約300秒（5分）のグレースケールIR映像クリップを扱います。 | 本記事は約300秒（5分）のグレースケール映像クリップを扱います。IRセンサー由来の可能性はありますが、映像フレームのみからは確認できません。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---