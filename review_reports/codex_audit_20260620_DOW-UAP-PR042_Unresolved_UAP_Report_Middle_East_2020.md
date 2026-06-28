---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 5
UNVERIFIABLE: 0
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-META-ID PASS File Name・DVIDS ID 1006097・Related Location Arabian Gulf は metadata/files_catalog.csv の対象行と一致する。
P1-META-DATE BLOCK ドラフトの Release Date は 2026年05月22日だが、metadata/files_catalog.csv / metadata/uap-data.csv / metadata/uap-csv-cache.csv は 5/8/26 で不一致。
P1-INCIDENT PASS Incident Date は 2020年由来として留保され、本文内の観測日時と矛盾しない。
P1-SOURCE PASS 動画記事として WAR.GOV公開ページ、DVIDS ID、DVIDS URL が併記されている。
P1-TECH PASS raw_media/video の ffprobe 実測値は約293.17秒、1920×1080、H.264、AACで、ドラフトの技術情報と概ね一致する。
P1-OFFICIAL-DESC WARN metadata/uap-data.csv の公式説明にある USCENTCOM提出、AARO、口頭・文書説明なし、動画説明の非分析判断という重要な制約が本文に十分反映されていない。
P2-STRUCT WARN チェックリスト上の「注意点」「免責」に相当する独立セクションが不足している。
P2-KEYPOINTS PASS 要点は3項目の番号付き太字で記述されている。
P2-AIMEMO PASS AI解析メモは区切り線付きで出典前に配置されている。
P2-TERMS WARN 「IRセンサー」のIRが一般読者向けに初出補足されていない。
P2-OBJECTIVITY PASS 物体種別・意図・正体を断定せず、「確認できない」「可能性がある」等の留保がある。
P2-DRAFT-RESIDUE WARN note本文内に「note転記後にこの行を削除」という作業メモが残っている。
P3-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020.mp4 / DVIDS ID 1006097 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 一次資料説明 | 本記事は約293秒（4分53秒）のグレースケール映像クリップを扱います。 | USCENTCOM提出、AARO、報告者による口頭・文書説明なし、動画説明は分析判断ではない旨を注意点に短く追加する。
W-02: 記事構成 | ⚠️ source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。公開前に source_registry への登録が必要です。 | 「注意点」「免責」を独立見出しとして設け、構成を メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責 に揃える。
W-03: AI読解 | グレースケールの映像（IRセンサーと推定されるが確認できない） | 「IR（赤外線）センサーと推定されるが確認できない」にする。
W-04: 代表フレーム | → 使用ファイル：thumbnails/DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_2020/frame_0000.png（note転記後にこの行を削除） | note投稿用本文から作業メモを削除し、必要なら画像キャプションのみ残す。
W-05: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR042：中東（アラビア湾）2020年UAPとされる事案映像・ノイズが多い映像と青い点マーカー複数（ファイル名より）──Arabian Gulf・米国防省公開・Release 02 | article_id 確定後に #TBD を除去した公開用タイトルへ確定する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---