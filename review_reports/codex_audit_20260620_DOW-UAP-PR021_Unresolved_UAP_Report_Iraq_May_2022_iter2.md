---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 0
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上ネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1-FILENAME BLOCK review_logs/source_registry.csv に DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022.mp4 の登録がなく、同一DVIDS ID 1006059では #038 のPDFのみ登録されている。
P1-1-RELEASE PASS Release Date は 2026年05月08日で、metadata/files_catalog.csv の対象MP4行の 5/8/26 と一致する。
P1-1-LOCATION PASS Related Location は Iraq と記載され、metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-INCIDENT PASS Incident Date はファイル名由来の 2022年5月として留保され、具体日不明も明記されている。
P1-2-TECH PASS ffprobe上の MP4・1920×1080・30fps・約10.27秒・H.264・AAC音声ありは本文の技術メタデータと概ね整合する。
P1-5 WARN source_registry未登録のため、article_id・status・重複有無・公開済み重複の正式照合が完了できない。
P2-1 WARN 記事構成に独立した「注意点」セクションがなく、タイトルも「#TBD」のまま残っている。
P2-2 WARN 「IRセンサー」の IR が初出時に日本語補足されていない。
P2-3 WARN 「担当AORはIraq」と記述しているが、確認できたローカル metadata は Related Location=Iraq であり、AORとしての断定はやや強い。
P2-4 PASS 日本向け換算が必要な英米単位の本文記述は確認されない。
P2-5 PASS note投稿互換性を損なう表・引用ブロック・長文英文引用・複雑なネストは確認されない。
IMG-1 PASS 視覚観察とファイル名・メタデータ由来情報はセクションで分離されている。
IMG-2 PASS IR推定、砂漠または荒野、対象物確認困難などに留保表現があり、物体種別・行動意図の断定は確認されない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry管理 | ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前に対象MP4を source_registry.csv に登録し、article_id・status・重複有無を照合する。
W-02: 記事構成 | # 【概要版#TBD】DoW DOW-UAP-PR021：... | article_id 確定後に #TBD を除去し、必要に応じて独立した注意点セクションを設ける。
W-03: 略語補足 | グレースケールの俯瞰映像（IRセンサーと推定されるが確認できない） | IR（赤外線）センサーと推定されるが確認できない、のように初出補足する。
W-04: AOR表現 | 担当AOR（Area of Responsibility：担当作戦地域）はIraqと記録されています。 | ローカル metadata で確認できる範囲に合わせ、「関連地域はIraqと記録されています」などに弱める。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---