---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 3
UNVERIFIABLE: 0
PASS: 11
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 WARN source_registry.csv に当該PR066の登録がなく、タイトルも「#TBD」のまま。本文末でも未登録と明記されており、公開前メタデータとして未確定。
P1-2 PASS 日付・動画秒数・解像度・フレームレート・ビットレート・ファイルサイズ・音声有無は files_catalog / ffprobe / thumbnail metadata と整合。
P1-3 WARN AOR が未展開のまま出ている。一般読者向けに「担当区域」等の短い補足が必要。
P1-5 PASS PR066は files_catalog.csv に存在し、同一DVIDS IDの別記事・公開済み重複は検出されない。
P2-1 PASS 構成はメタデータ→要点3項目→AI読解→注意点→出典→免責の順で、視覚観察記事として冒頭警告もある。
P2-2 PASS USCG、DVIDS、C-144/HC-144、AFB、VID、FHD、AAC、HUD、TIC TAC、IR hot は概ね本文内で補足されている。
P2-3 PASS 視覚確認できた内容とファイル名・メタデータ由来情報が分離され、対象物の正体・種別・意図は断定していない。
P2-4 PASS 換算対象となる速度・高度・距離などの米国単位は本文に出ていない。
P2-5 PASS note投稿互換上の禁止形式はなく、直訳臭・大量英文・生ログ貼付も見当たらない。
P2-6 PASS 日本語読者向けにDVIDS、米沿岸警備隊、タインドール空軍基地、チックタック形状、解像度などの説明がある。
IMG-1 PASS 視覚観察と解釈の分離は概ね維持されており、ファイル名由来情報は別セクションで明示されている。
IMG-2 WARN 「物体が左上端へ移動」という見出しが、物体自体の移動を確定した表現に見える。画角変化との切り分けが必要。
SRC-1 PASS 出典には WAR.GOV公開ページ、DVIDS直接URL、DVIDS ID、元ファイル名、代表フレームが記載されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ / タイトル・末尾 | 「#TBD」「source_registry 未登録」 | source_registry 登録と article_id 付番後、タイトルの #TBD と末尾の未登録注記を公開用表記へ更新する。
W-02: ファイル名・メタデータ由来の情報 | 「担当AOR：Southeastern United States（files_catalog.csv より）」 | 「担当区域（AOR）：Southeastern United States（南東部米国）（files_catalog.csv より）」のように補足する。
W-03: 映像から視覚的に確認できる情報 | 「00:15（映像角度変化・物体が左上端へ移動）」 | 「00:15（映像角度変化・物体が左上端付近に確認）」のように、物体自体の移動断定を避ける。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---