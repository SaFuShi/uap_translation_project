---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-META-FILENAME PASS File Name は metadata/files_catalog.csv の PR044 行と一致している。
P1-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020.mp4 / DVIDS ID 1006104 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-META-DATE PASS Release Date 2026年05月08日は metadata/files_catalog.csv の 5/8/26 と整合している。
P1-META-LOCATION PASS Related Location は metadata/files_catalog.csv の Arabian Gulf と一致している。
P1-META-DVIDS PASS DVIDS ID 1006104 と DVIDS URL https://www.dvidshub.net/video/1006104 はドラフト内で一貫している。
P2-STRUCT WARN チェックリスト上の「注意点」「免責」に相当する独立セクションが不足している。
P2-KEYPOINTS PASS 要点は3項目の番号付き太字で記述されている。
P2-AIMEMO PASS AI解析メモは区切り線付きで出典前に配置されている。
P2-TERMS WARN 「IRセンサー」のIRが一般読者向けに補足されていない。
P2-IMAGE-SEPARATION WARN PR036との類似から同一または類似システムの可能性に触れる記述が、視覚観察項目内に混在している。
P2-OBJECTIVITY PASS 物体の正体・種別・行動意図を断定せず、「確認できない」「推定されるが確認できない」等の留保がある。
P2-SOURCES PASS 出典セクションに WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-READABILITY PASS 直訳臭や大量の生英文・OCRログ貼付は確認されない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 記事構成 | ⚠️ source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。公開前に source_registry への登録が必要です。 | 「注意点」または「免責」セクションとして分離し、標準構成に揃える。
W-02: AI読解 | グレースケールの映像（IRセンサーと推定されるが確認できない） | 「IR（赤外線）センサーと推定されるが確認できない」など、初出で短く補足する。
W-03: この資料の要点 | PR036でも類似した赤矢印マーカーが確認されており、同一または類似したシステムによる記録の可能性がありますが確認できません。 | 視覚観察とは別に「比較上の参考」または「解釈上の注意」として分離する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---