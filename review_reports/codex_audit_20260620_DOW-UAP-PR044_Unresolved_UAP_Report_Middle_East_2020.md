---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 5
UNVERIFIABLE: 0
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-META-FILENAME PASS File Name は metadata/files_catalog.csv の PR044 行と一致している。
P1-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020.mp4 / DVIDS ID 1006104 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-META-DATE BLOCK ドラフトの Release Date は 2026年05月22日だが、metadata/files_catalog.csv / metadata/uap-csv-cache.csv の対象行は 5/8/26 であり、公開日メタデータが整合していない。
P1-META-LOCATION PASS Related Location は metadata/files_catalog.csv / metadata/uap-csv-cache.csv の Arabian Gulf と一致している。
P1-META-DVIDS PASS DVIDS ID 1006104 と DVIDS URL https://www.dvidshub.net/video/1006104 はドラフト内で一貫している。
P1-TECH WARN ffprobe実測のビットレートは約2,225 kbpsだが、ドラフトは 2,120 kbps と記載しており不一致。
P1-SOURCE-CONTEXT WARN metadata/uap-csv-cache.csv の公式説明にある USCENTCOM提出、AARO提出先、赤外線センサー、音声は視覚内容と無関係、報告者の口頭・文書説明なし、動画説明は分析判断ではない旨が本文に反映されていない。
P2-STRUCT WARN チェックリスト上の「注意点」「免責」に相当する独立セクションが不足している。
P2-KEYPOINTS PASS 要点は3項目の番号付き太字で記述されている。
P2-AIMEMO PASS AI解析メモは区切り線付きで出典前に配置されている。
P2-DRAFT-RESIDUE WARN note本文内に「note転記後にこの行を削除」という作業メモが残っている。
P2-TERMS WARN 「IRセンサー」のIRが一般読者向けに補足されていない。
P2-OBJECTIVITY PASS 物体の正体・種別・行動意図を断定せず、「確認できない」「推定されるが確認できない」等の留保がある。
P2-SOURCES PASS 出典セクションに WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像メタデータ | ビットレート：2,120 kbps | ffprobe実測値または thumbnails 側 metadata.json の 2,225 kbps に統一する。
W-02: 一次資料説明 | 本記事は約312秒（5分12秒）のグレースケール映像クリップを扱います。 | 公式説明由来の USCENTCOM提出、AARO、赤外線センサー、音声は視覚内容と無関係、報告者説明なし、分析判断ではない旨を短く補足する。
W-03: 記事構成 | ⚠️ source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。公開前に source_registry への登録が必要です。 | 「注意点」または「免責」セクションとして分離し、標準構成に揃える。
W-04: 代表フレーム | → 使用ファイル：thumbnails/DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png（note転記後にこの行を削除） | 投稿本文では作業メモを削除し、必要なら画像キャプションのみ残す。
W-05: AI読解 | グレースケールの映像（IRセンサーと推定されるが確認できない） | 「IR（赤外線）センサーと推定されるが確認できない」など、初出で短く補足する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---