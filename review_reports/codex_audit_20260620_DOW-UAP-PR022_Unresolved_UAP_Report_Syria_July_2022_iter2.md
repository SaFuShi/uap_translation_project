---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 1
UNVERIFIABLE: 0
PASS: 13
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-1 PASS ファイル名、Incident Date、Location、DVIDS IDの由来はファイル名・files_catalog.csv・DVIDSとして分離されている。
P1-2 PASS 動画メタデータの数値はローカルffprobe値と整合し、換算値の過剰断定は確認されない。
P1-3 PASS DVIDS、FOVなど本文に出る略語は必要範囲で補足されている。
P1-5 WARN source_registry.csv に当該MP4記事の登録がなく、タイトルも #TBD のまま。
P2-1 PASS 構成はメタデータ、要点、AI読解、注意点、出典、免責の順で整っている。
P2-2 PASS 本記事で使用される軍事略語・専門用語に重大な未補足は確認されない。
P2-3 PASS 視覚確認事実と推定・未確認事項は概ね分離され、物体種別や意図の断定はない。
P2-4 PASS 単位換算が必要な速度・高度・距離等の記述はなく、動画仕様値中心で矛盾は確認されない。
P2-5 PASS note投稿互換上の禁止要素は確認されない。
P2-6 PASS 日本語読者向けに「シリア」「動画」「視野角」等の補足があり、読み戻し負荷は低い。
VID-1 PASS 視覚観察とファイル名・メタデータ由来情報がセクション単位で分離されている。
VID-2 PASS 「複数センサー」「白い物体」等は「とみられる」「確認できません」と留保されている。
VID-3 PASS 「移動」「追跡」「消失」「分裂」等の動作を確定事実として断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: P1-5 / 文書メタデータ・末尾注記 | 「【概要版#TBD】」「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施」 | source_registry.csv にPR022記事を登録し、article_id・source_url・sha256・draft_path等を確定したうえで、タイトルの #TBD を正式IDへ置換する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---