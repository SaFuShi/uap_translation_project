---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 2
UNVERIFIABLE: 0
PASS: 12
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 WARN source_registry.csv に当該PR065の登録がなく、タイトルも「#TBD」のまま。本文末でも未登録と明記されており、公開前メタデータとして未確定。
P1-2 PASS 日付・動画秒数・解像度・フレームレート・ビットレート・ファイルサイズ・音声有無は files_catalog / ffprobe と整合。
P1-3 WARN AOR が未展開のまま出ている。一般読者向けに「担当区域」等の短い補足が必要。
P1-5 PASS PR065は files_catalog.csv に存在し、同一DVIDS IDの別記事・公開済み重複は検出されない。
P2-1 PASS 構成はメタデータ→要点3項目→AI読解→注意点→出典→免責の順で、視覚観察記事として冒頭警告もある。
P2-2 PASS USCG、DVIDS、C-144/HC-144、AFB、VID、SD、AAC、HUD、TIC TAC、IR hot は概ね本文内で補足されている。
P2-3 PASS 視覚確認できた内容とファイル名・メタデータ由来情報が分離され、対象物の正体・種別・意図は断定していない。
P2-4 PASS 換算対象となる速度・高度・距離などの米国単位は本文に出ていない。
P2-5 PASS note投稿互換上の禁止形式はなく、直訳臭・大量英文・生ログ貼付も見当たらない。
P2-6 PASS 日本語読者向けに低解像度、DVIDS、米沿岸警備隊、タインドール空軍基地、チックタック形状などの説明がある。
IMG-1 PASS 視覚観察と解釈の分離は維持されており、抽出フレームで対象物を確認できない旨が明記されている。
IMG-2 PASS 移動・追跡・消失・分裂などを確定事実として断定していない。
SRC-1 PASS 出典には WAR.GOV公開ページ、DVIDS直接URL、DVIDS ID、元ファイル名、代表フレームが記載されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ / タイトル・末尾 | 「#TBD」「source_registry 未登録」 | source_registry 登録と article_id 付番後、タイトルの #TBD と末尾の未登録注記を公開用表記へ更新する。
W-02: ファイル名・メタデータ由来の情報 | 「担当AOR：Southeastern United States（files_catalog.csv より）」 | 「担当区域（AOR）：Southeastern United States（南東部米国）（files_catalog.csv より）」のように補足する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---