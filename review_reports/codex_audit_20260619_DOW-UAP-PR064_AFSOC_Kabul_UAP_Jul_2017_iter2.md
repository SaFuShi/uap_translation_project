---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1 BLOCK review_logs/source_registry.csv に DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017.mp4 の登録がなく、本文でも source_registry 未登録・article_id 未付番と明記されている。
P1-2 PASS ffprobe値（MP4、H.264、640x360、29.97fps、17.68秒、約1,462kbps、AAC音声、3.08MB、2ストリーム）はローカル動画実体およびサムネイルメタデータと整合している。
P1-3 PASS AFSOC、CENTCOM、DVIDS は初出付近で日本語補足されている。
P1-5 PASS metadata/files_catalog.csv のファイル名、Agency、Release Date、DVIDS ID、file_type は本文メタデータと整合している。
P2-1 WARN 代表フレーム挿入用の作業メモ行「note転記後にこの行を削除」が本文内に残っている。
P2-1b WARN AI解析メモが「AI読解」内に置かれており、チェックリスト上の「末尾の所定位置」からは外れている。
P2-2 PASS 軍事略語・組織名は記事単独理解に必要な範囲で補足されている。
P2-3 WARN 「追尾コーナーマーカー」は機器動作の解釈を含むため、画面表示の観察と追尾UIの推定をより明確に分ける必要がある。
P2-5 PASS 直訳臭、生ログ大量貼付、note互換性を損なう表組み・引用ブロックは確認されない。
P2-6 PASS 数値・単位は動画秒数、解像度、fps、MB、kbps中心で、日本語読者向け理解を阻害する未換算の軍事単位はない。
VID-1 PASS 映像から視覚的に確認できる情報と、ファイル名・メタデータ由来情報が別セクションで分離されている。
VID-2 PASS 「IR俯瞰映像」は推定として扱われ、物体の正体・種別・行動意図を断定していない。
M5 PASS war.gov URL と DVIDS URL が併記され、DVIDS URL の ID は files_catalog.csv の dvids_video_id=1007741 と一致している。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 代表フレーム挿入部 | → 使用ファイル：thumbnails/DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017/frame_0005.png（note転記後にこの行を削除） | 公開用本文から作業メモ行を削除し、キャプション本文のみ残す。
W-02: AI解析メモ | **AI解析メモ：** 動画ファイル。ffprobeによる技術情報取得済み。 | AI解析メモを出典後または免責直前など、テンプレートで定義した末尾位置へ移す。
W-03: 視覚観察表現 | 4隅に追尾コーナーマーカーが確認できる。 | 「4隅に同色のコーナーマーカーが確認できる。追尾UI表示の可能性がある」のように、観察事実と解釈を分ける。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---