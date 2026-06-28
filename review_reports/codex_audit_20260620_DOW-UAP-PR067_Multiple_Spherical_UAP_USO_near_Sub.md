---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 0
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS note禁止形式（Markdown表・引用ブロック・長文英文引用・複雑ネスト・Codex注釈ブロック）は検出されない。
P1-1 BLOCK review_logs/source_registry.csv に対象MP4の登録がなく、本文も article_id #TBD / source_registry 未登録の状態である。
P1-2 PASS metadata/files_catalog.csv 上のファイル名・Agency・Release Date・DVIDS ID と本文記述は概ね整合する。
P1-3 PASS Incident Date はファイル名由来と明示され、files_catalog.csv 側に観測日未記録である点と矛盾しない。
P1-4 PASS Related Location / AOR は不明として扱われ、files_catalog.csv の空欄と整合する。
P1-5 PASS DVIDS URL の直接リンクが本文メタデータおよび出典に含まれる。
P2-1 WARN AI解析メモが「末尾の所定位置」ではなく、AI読解セクション内の途中に置かれている。
P2-2 PASS 構成は概ね「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」に沿っている。
P2-3 PASS 要点は3項目の番号付き太字で記述されている。
P2-4 PASS DVIDS・AOR・USO など主要略語には初出付近で日本語補足がある。
P2-5 WARN 「交互に出現」は、列挙フレーム上は連続して見える/見えない区間もあり、周期的交替の印象を与える。
P2-6 WARN マゼンタ点を「海面上」と繰り返す表現は、UIマーカーか実体か未確定な点との分離がやや弱い。
P2-7 WARN 「note転記後にこの行を削除」という制作メモが本文中に残っている。
IMG-1 PASS 視覚観察情報とファイル名・メタデータ由来情報は別セクションで分離されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: AI解析メモ | **AI解析メモ：** 動画ファイル。ffprobeによる技術情報取得済み。 | 末尾の免責直前または所定の末尾位置へ移動。
W-02: この資料の要点 | 艦船とみられる物体が見える/見えないフレームが交互に出現する | 「確認できるフレームと確認困難なフレームがある」などに弱める。
W-03: マゼンタ点状マーカー | マゼンタ色の点が海面上に散在した状態で確認できる | 「海面とみられる背景上／画面上に確認できる」に変更。
W-04: 代表フレーム | → 使用ファイル：thumbnails/...（note転記後にこの行を削除） | 公開本文から制作メモ行を除外。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---