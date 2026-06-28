---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 0
PASS: 9
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは検出されない。
P1-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR073 / DVIDS ID 1007790 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-CATALOG PASS metadata/files_catalog.csv のファイル名、Agency、Release Date、Incident Date、Related Location、File Type、DVIDS ID は本文メタデータと整合する。
P1-TECH PASS thumbnails metadata.json の duration_sec 88.57、resolution 608x1080、frame_rate 30/1、video_codec h264、has_audio true と本文の技術情報は整合する。
P1-SOURCE PASS 動画記事として WAR.GOV 公開ページと DVIDS URL https://www.dvidshub.net/video/1007790 が併記され、DVIDS ID と整合する。
P1-DUP WARN source_registry 未登録のため、registry status・SHA256重複・公開済み記事重複の正式確認が完了していない。
P2-STRUCT WARN 標準構成のうち「注意点」「免責」が独立見出しとして存在せず、冒頭注意書きと末尾注記に分散している。
P2-KEYPOINT PASS 要点は番号付き太字で3項目に整理されている。
P2-FRAME PASS 代表フレーム参照は thumbnails/DOW-UAP-PR073_.../frame_0030.png として存在し、00:30時点の記述と整合する。
P2-IMAGE PASS 縦位置608×1080、広範な黒塗り、中央付近の白色クロスヘア、小さな矩形枠の記述は視覚情報として留保付きで記述されている。
P2-OBJECTIVITY WARN 冒頭で「IRセンサー映像クリップ」と断定調だが、後続では「IRセンサーと推定されるが確認できない」としており、推定扱いが一貫していない。
P2-TITLE WARN タイトルに「#TBD」が残っており、公開用 article_id 確定前の状態である。
P2-TERMS PASS DVIDS は初出で「国防映像情報配信サービス」と補足され、未補足の主要軍事略語の混入は目立たない。
P2-READABILITY PASS OCRログ、生英文大量貼付、直訳崩れ、UFO論壇的表現、物体正体・種別・行動意図の断定は確認されない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: P1-DUP | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | source_registry 登録後に status・重複・article_id を再確認できる状態にする。
W-02: P2-STRUCT | AI解析メモの後に出典が続き、独立した注意点・免責セクションがない | 「## 注意点」「## 免責」を独立見出し化し、未確認事項・視覚観察の限界・断定回避を集約する。
W-03: P2-OBJECTIVITY | 本記事は約89秒の縦位置IRセンサー映像クリップを扱います。 | 「IRセンサーと推定される縦位置映像クリップ」など、推定扱いに統一する。
W-04: P2-TITLE | # 【概要版#TBD】DoW DOW-UAP-PR073：... | article_id 確定後に #TBD を除去した公開用タイトルへ確定する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---