---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 3
UNVERIFIABLE: 0
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-META-DATE BLOCK ドラフトの Release Date は 2026年05月22日だが、metadata/files_catalog.csv の release_date は 5/8/26 で不一致。
P1-META-ID PASS File Name・DVIDS ID 1006094・Related Location Arabian Gulf は metadata/files_catalog.csv と一致。
P1-INCIDENT PASS Incident Date は 2020年由来として留保され、本文内の観測日時と矛盾しない。
P1-SOURCE PASS WAR.GOV公開ページに加えて対象映像のDVIDS直接URLが出典に記載されている。
P2-STRUCT WARN 構成上、「注意点」「免責」に相当する独立セクションが不足している。
P2-KEYPOINTS PASS 要点は3項目の番号付き太字で記述されている。
P2-AIMEMO PASS AI解析メモは区切り線付きで出典前に配置されている。
P2-SOURCES PASS 出典セクションにDVIDS URL・元ファイル名・代表フレームが記載されている。
P2-TERMS WARN 「IRセンサー」のIRが一般読者向けに補足されていない。
P2-OBJECTIVITY PASS 物体の正体・種別・行動意図を断定せず、確認事実と留保が区別されている。
P2-IMAGE PASS 視覚観察と解釈は概ね分離され、「みられる」「確認できない」等の留保がある。
P2-DRAFT-RESIDUE WARN note本文内に「note転記後にこの行を削除」という作業メモが残っている。
P3-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020.mp4 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 構成 | ⚠️ source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。公開前に source_registry への登録が必要です。 | 「注意点」または「免責」セクションとして分離し、本文構成を メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責 に揃える。
W-02: AI読解 | グレースケールの映像（IRセンサーと推定されるが確認できない） | 「IR（赤外線）センサーと推定されるが確認できない」など、初出で短く補足する。
W-03: 代表フレーム | → 使用ファイル：thumbnails/DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png（note転記後にこの行を削除） | note投稿用本文から作業メモ部分を削除し、必要なら画像キャプションだけを残す。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---