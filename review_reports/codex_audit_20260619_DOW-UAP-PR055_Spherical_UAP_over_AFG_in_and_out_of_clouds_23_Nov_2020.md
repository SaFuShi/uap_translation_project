---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 2
UNVERIFIABLE: 0
PASS: 11
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 BLOCK source_registry.csv に DOW-UAP-PR055 の登録がなく、本文でも article_id 未付番・source_registry 未登録と明記されている。
P1-1b PASS files_catalog.csv 上のファイル名・Agency・Release Date・DVIDS ID と本文メタデータは概ね一致する。
P1-1c PASS Incident Date はファイル名由来の 2020年11月23日として明記され、files_catalog.csv の「2020」との差分も説明されている。
P1-2 PASS ffprobe 技術情報は実ファイルの codec・解像度・fps・duration・size・bitrate と整合する。
P1-3 PASS CENTCOM と DVIDS は初出付近で日本語補足されている。
P1-5 PASS raw_media/video 内で同一 SHA256 の重複動画は検出されない。
P2-1 PASS 構成はメタデータ→要点→AI読解→注意点→出典→免責の順で、要点は3項目。
P2-1b PASS 動画・視覚観察記事として冒頭警告があり、確認事実と由来情報を分ける方針が示されている。
P2-3 WARN タイトルと要点見出しで「追尾された」「追尾マーカー」と強めに表現しているが、本文では追尾状態・対象対応が未確認とされており、表現強度に差がある。
P2-3b PASS 物体の正体・種別・意図・大きさ・距離・速度は断定していない。
P2-5 WARN 本文中に「note転記後にこの行を削除」という作業メモが残っている。
P2-6 PASS 数値・単位は動画秒数、解像度、fps、MB、kbps中心で、読者理解を阻害する未換算の軍事単位はない。
IMG-1 PASS 視覚観察とファイル名・メタデータ由来情報はセクション分離され、画像のみの判断には留保が付いている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: タイトル・要点 | 「球形UAPが雲間を出入りしながら追尾された映像」「クロスヘア追尾マーカー」 | 「追尾表示らしきクロスヘアが確認される映像」「クロスヘア状表示（追尾マーカーの可能性）」など、未確認性を見出し側にも反映する。
W-02: 代表フレーム挿入部 | 「→ 使用ファイル：...（note転記後にこの行を削除）」 | 公開用本文から作業メモ行を削除し、キャプション本文のみ残す。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---