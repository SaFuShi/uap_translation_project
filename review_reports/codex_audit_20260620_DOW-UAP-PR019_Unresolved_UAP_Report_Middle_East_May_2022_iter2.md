---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 3
WARN: 3
UNVERIFIABLE: 0
PASS: 8
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは検出なし。
P1-1a BLOCK source_registry.csv に DOW-UAP-PR019 動画記事の登録がなく、タイトルも #TBD のまま。
P1-1b BLOCK Release 表記がローカル catalog と不一致。metadata/files_catalog.csv では当該動画は 2026年05月08日公開・release_1 系だが、本文タイトルと出典に Release 02 とある。
P1-1c BLOCK WAR.GOV 出典が https://www.war.gov/UFO/ トップページのまま。対象資料の直接参照としては不十分。
P1-1d PASS Incident Date はファイル名 May_2022 由来であることを明記しており、本文内矛盾なし。
P1-1e PASS Related Location は metadata/files_catalog.csv の Middle East と一致。
P1-2 PASS 動画技術情報はローカル metadata と概ね一致。約5.4秒、1920x1080、30fps、H.264、AAC、約6.5MB。
P1-3 PASS DVIDS は初出で「国防映像情報配信サービス」と補足あり。
P1-5 WARN 同一 DVIDS ID 1006056 に対応する PDF dow-uap-d10-mission-report-middle-east-may-2022.pdf は source_registry #028 で公開済み。動画記事としての独立登録・重複扱いの整理が必要。
P2-1 WARN 所定構成のうち「注意点」セクションが独立見出しとして欠落し、免責も末尾注記に分散している。
P2-1b PASS 要点は3項目の番号付き太字で構成されている。
P2-3 PASS UAP対象物の正体・種別・行動意図を断定せず、確認困難と留保している。
IMG-1 WARN 黒塗り矩形を「3箇所」とする記述は代表フレーム上の複数矩形配置と不整合。上部・左端・右上・右下など分布表現の方が安全。
IMG-2 PASS 視覚観察とファイル名・メタデータ由来情報は別セクションで分離されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: P1-5 | DVIDS ID：1006056（DVIDS＝国防映像情報配信サービス） | source_registry 上の既公開PDF #028 との関係を動画記事メタデータ側で明確化。
W-02: P2-1 | AI解析メモの後に出典が続き、独立した注意点セクションがない | 「## 注意点」を追加し、未確認事項・視覚観察の限界・音声未扱いを集約。
W-03: IMG-1 | 黒塗り矩形が上部・左下・右下の3箇所 | 「黒塗り矩形が上部、左端付近、右上、右下など複数箇所に確認できる」。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---