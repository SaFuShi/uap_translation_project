---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-METADATA BLOCK ドラフトの Release Date は 2026年05月22日だが、metadata/files_catalog.csv と metadata/uap-csv-cache.csv の対象PR032行は 5/8/26 であり、公開日メタデータが一致しない。
P1-1-LOCATION PASS Related Location は Syria と記載され、metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-RELATION WARN 「同日・同地域」「同一事案」は、ファイル名だけでは日単位まで確認できず、本文内の根拠表示が「同時期・同地域」より強い。
P1-2 PASS ffprobe実測値と本文の再生時間・解像度・フレームレート・動画ビットレート・ファイルサイズ・音声AACの記述は概ね一致する。
P1-3 PASS DVIDS は初出で日本語補足されている。
P1-5 WARN source_registry.csv に当該ファイルの登録がなく、ドラフト末尾にも「source_registry 未登録」と明記されている。
P2-1 WARN 記事構成に独立した「注意点」セクションがなく、タイトルの「#TBD」と「note転記後にこの行を削除」という作業用注記が残っている。
P2-2 WARN 「IR」が初出で日本語補足されていない。
P2-3 PASS 物体の正体・種別・行動意図は断定せず、確認事実と推定を概ね分離している。
P2-4 PASS 換算を要する高度・速度・距離等の数値は本文にない。
P2-5 PASS note投稿互換上の禁止形式はなく、直訳臭・大量英文・生ログ貼付も見当たらない。
P2-6 PASS DVIDS、VID、FHD、H.264、AACなど主要な略語・形式名には概ね必要範囲で補足がある。
IMG-1 PASS 視覚観察とファイル名・メタデータ由来情報がセクション単位で分離されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 関連映像の根拠表現 | 「同日・同地域の映像とされています」「同一事案の関連映像と推定されます」 | 「同時期・同地域の関連映像と推定されます」など、日単位・同一事案の断定を避ける。
W-02: source_registry管理 | 「#TBD」「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施」 | source_registry登録・article_id付番後に #TBD と未登録注記を解消する。
W-03: 記事構成・作業注記 | 「note転記後にこの行を削除」 | 作業用注記を本文から削除し、必要な留保は独立した「注意点」セクションに整理する。
W-04: 略語補足 | 「IRセンサーと推定されるが確認できない」 | 初出で「IR（赤外線）センサーと推定されるが確認できない」など日本語補足を追加する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---