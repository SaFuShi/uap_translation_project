---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 4
UNVERIFIABLE: 0
PASS: 11
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-METADATA PASS Release Date 2026年05月08日、Related Location Syria、DVIDS ID 1006078 は metadata/files_catalog.csv / metadata/uap-csv-cache.csv の対象行と整合する。
P1-1-RELATION WARN 「同日・同地域」は、ファイル名上は October 2024 までで日単位の根拠が本文中に示されていない。
P1-2 PASS 高度・速度・Zulu時刻など換算・時刻整合を要する数値は本文にない。
P1-3 PASS DVIDS は初出で日本語補足されている。
P1-5 WARN source_registry.csv への登録・article_id付番が未実施であることが本文末尾に残っている。
P2-1 WARN 構成に独立した「注意点」セクションがなく、タイトルにも「#TBD」が残っている。
P2-2 WARN 「IR」が初出で日本語補足されていない。
P2-3 PASS 物体の正体・種別・行動意図は断定せず、確認事実と推定を概ね分離している。
P2-4 PASS 換算を要する高度・速度・距離等の数値は本文にない。
P2-5 PASS note投稿互換上の禁止形式はなく、直訳臭・大量英文・生ログ貼付も見当たらない。
P2-6 PASS DVIDS、VID、FHD、H.264、AACなど主要な略語・形式名には概ね必要範囲で補足がある。
IMG-1 PASS 視覚観察とファイル名・メタデータ由来情報がセクション単位で分離されている。
IMG-2 PASS 「UAP対象物は確認困難」など留保があり、移動・追跡・消失等の映像解釈を確定事実として断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 関連映像の根拠表現 | 「同日・同地域の映像とされています」 | 「同時期・同地域の映像と推定されます」など、日単位の断定を避ける。
W-02: source_registry管理 | 「#TBD」「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施」 | source_registry登録・article_id付番後に #TBD と未登録注記を解消する。
W-03: 記事構成 | 独立した「注意点」セクションがない | 冒頭警告または免責部分とは別に、確認できる情報と確認できない情報を「注意点」として整理する。
W-04: 略語補足 | 「IRセンサーと推定されるが確認できない」 | 初出で「IR（赤外線）センサーと推定されるが確認できない」など日本語補足を追加する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---