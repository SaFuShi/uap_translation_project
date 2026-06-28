---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 4
UNVERIFIABLE: 0
PASS: 8
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは検出されない。
P1-1a BLOCK Release Date が metadata/files_catalog.csv の release_date=5/8/26 と不一致。ドラフトは「2026年05月22日」。
P1-1b BLOCK 出典の WAR.GOV がトップページのみで、files_catalog.csv にある対象直接URLが本文・出典に記載されていない。
P1-1c WARN source_registry.csv に当該PR036動画の登録がなく、ドラフト末尾でも未登録と明記されている。
P1-2 PASS ffprobe値は概ね整合。1920×1080、30fps、約137.37秒、H.264、AAC音声あり。
P1-3 PASS DVIDS は初出で補足されている。MGRS、MISREP、JSIR等の該当略語は本文に出ない。
P1-5 PASS 既存 source_registry.csv の #036 withdrawn_duplicate、#036b published、#017 hold は整合。
P2-1a WARN 構成上、「注意点」および明示的な「免責」セクションが不足している。
P2-1b PASS 「この資料の要点」は3項目で記述されている。
P2-1c PASS 冒頭に動画映像・視覚観察記事である警告があり、限定的な根拠区分も示されている。
P2-3 WARN 「多くのRelease 02映像」「珍しい多色UI」という比較評価の根拠が本文内で確認できない。
P2-5 PASS note投稿互換上の禁止フォーマットは検出されない。
IMG-1 WARN 「トラッキング映像」は機器動作の解釈に踏み込む表現で、視覚観察との分離が不十分。
IMG-2 PASS 「船とみられる」「推定されるが確認できない」など、画像判断には概ね留保が付いている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | 公開前監査では source_registry 登録後のID・ステータス・URL整合を確認できる状態にする。
W-02: 記事構成 | 明示的な「注意点」「免責」セクションがない。 | AI読解後に注意点、出典後に免責を独立セクションとして置く。
W-03: この資料の要点 | 「多くのRelease 02映像がシアン/マゼンタのUIマーカーを使用する中、本映像は…」 | 比較根拠を出典化するか、「本映像ではグリーン・赤・黄色のマーカーが確認できます」に留める。
W-04: タイトル・要点 | 「多色UIトラッキング映像」 | 「多色UI表示を含む映像」など、トラッキング動作を断定しない表現にする。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---