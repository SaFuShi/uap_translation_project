---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1-FILENAME WARN review_logs/source_registry.csv に対象MP4の登録がなく、タイトルも「#TBD」のまま。本文末でも source_registry 未登録と明記されている。
P1-1-METADATA BLOCK ドラフトの Release Date は 2026年05月22日だが、metadata/files_catalog.csv と metadata/uap-csv-cache.csv の対象PR027行は 5/8/26 であり、公開日メタデータが一致しない。
P1-1-LOCATION PASS Related Location は United Arab Emirates と記載され、metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-INCIDENT PASS Incident Date はファイル名由来の 2023年10月として留保され、具体日不明も明記されている。
P1-2 PASS 速度・高度・FL・Zulu時刻など、換算検証対象となる数値記述は本文にない。
P1-5 WARN source_registry未登録のため、article_id・status・重複有無・公開済み重複の正式照合が完了できない。
P2-1 WARN 記事構成に独立した「注意点」セクションがなく、タイトルも「#TBD」のまま残っている。
P2-2 PASS DVIDS、VID、FHD、H.264、AACなど本文で使用される略語・形式名は概ね必要範囲で補足されている。
P2-3 PASS 視覚確認事実と推定・未確認事項は概ね分離され、物体種別や行動意図の断定はない。
P2-4 PASS 日本向け換算が必要な英米単位の本文記述は確認されない。
P2-5 PASS note投稿互換上の禁止形式はなく、直訳臭・大量英文・生ログ貼付も見当たらない。
IMG-1 PASS 視覚観察とファイル名・メタデータ由来情報がセクション単位で分離されている。
IMG-2 PASS 「IRセンサーと推定されるが確認できない」「とみられる」「確認できない」などの留保があり、画像のみで機器・物体種別を断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry管理 | 「#TBD」「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施」 | source_registry.csv にPR027記事を登録し、article_id・source_url・status・重複有無を確定したうえで、タイトルの #TBD を正式IDへ置換する。
W-02: 記事構成 | 独立した「注意点」セクションがない | 視覚観察記事としての留保・音声未扱い・物体識別不能などを「注意点」セクションに整理する。
W-03: 文書メタデータ | 「Release Date：2026年05月22日」 | metadata/files_catalog.csv / metadata/uap-csv-cache.csv の対象PR027行に合わせて公開日を再確認し、日付を一致させる。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---