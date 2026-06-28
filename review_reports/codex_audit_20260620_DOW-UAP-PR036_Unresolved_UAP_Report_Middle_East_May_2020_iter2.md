---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 4
UNVERIFIABLE: 0
PASS: 10
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは検出されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-RELEASE PASS Release Date は 2026年05月08日で、metadata/files_catalog.csv の release_date=5/8/26 と一致する。
P1-1-INCIDENT PASS Incident Date はファイル名由来の「2020年5月」として記述され、metadata/files_catalog.csv の N/A と矛盾しない。
P1-1-LOCATION PASS Related Location は Middle East と記載され、metadata/files_catalog.csv の対象MP4行と一致する。
P1-2 PASS ffprobe値は概ね整合。1920×1080、30fps、137.37秒、H.264、AAC音声、動画ビットレート約8,204kbpsを確認。
P1-3 PASS DVIDS は初出で補足されている。MGRS、MISREP、JSIR等の該当略語は本文に出ない。
P1-5 WARN source_registry.csv に当該PR036動画の登録がなく、記事IDも #TBD のまま。
P2-1a WARN 構成上、「注意点」および明示的な「免責」セクションが不足している。
P2-1b PASS 「この資料の要点」は3項目で記述されている。
P2-3a PASS 「宇宙人」「異星人」等のUFO論壇的断定表現は検出されない。
P2-3b WARN 「多くのRelease 02映像」「珍しい多色UI」という比較評価の根拠が本文内で確認できない。
P2-5 PASS note投稿互換上の禁止フォーマットは検出されない。
IMG-1 WARN 「トラッキング映像」は機器動作の解釈に踏み込む表現で、視覚観察との分離が不十分。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry | 「【概要版#TBD】」「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | source_registry登録後に article_id・status・draft_path と照合できる形にする。
W-02: 記事構成 | 明示的な「注意点」「免責」セクションがない。 | AI読解後に注意点、出典後に免責を独立セクションとして置く。
W-03: この資料の要点 | 「多くのRelease 02映像がシアン/マゼンタのUIマーカーを使用する中、本映像はグリーン・赤・黄色の3色のUIマーカーが確認できます。」 | 比較根拠を出典化するか、「本映像ではグリーン・赤・黄色のマーカーが確認できます」に留める。
W-04: タイトル・要点 | 「多色UIトラッキング映像」 | 「多色UI表示を含む映像」など、トラッキング動作を断定しない表現にする。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---