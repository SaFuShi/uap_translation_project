---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 0
PASS: 9
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 BLOCK Release Date がドラフトでは「2026年05月22日」だが、metadata/files_catalog.csv では当該ファイルの release_date が「5/8/26」であり、一次メタデータと不一致。
P1-2 WARN ffprobe由来の技術値がローカル metadata.json / ffprobe 実測値と一部不一致。ドラフトは「1,834 kbps」「約14.9 MB」だが、実測は bit_rate 1,938,505 bps、size 15,992,674 bytes。
P1-3 PASS DVIDS は初出で日本語補足されている。
P1-5 WARN source_registry.csv に当該ファイルの登録がなく、ドラフト末尾にも「source_registry 未登録」と明記されている。
P2-1 WARN タイトルに「#TBD」が残り、本文中に「note転記後にこの行を削除」という作業用注記が残っている。
P2-2 WARN 「IR」が初出で日本語補足されていない。
P2-3 PASS 物体の正体・種別・行動意図は断定せず、確認事実と推定を概ね分離している。
P2-4 PASS 換算を要する高度・速度・距離等の数値は本文にない。
P2-5 PASS note投稿互換上の禁止形式は検出されない。
P2-6 PASS DVIDS など主要な組織・識別子には読者向け補足がある。
IMG-1 PASS 視覚観察と解釈は概ね分離されている。
IMG-2 PASS 「移動」「追跡」「消失」「分裂」等を確定事実として断定していない。
IMG-4 PASS 画像・映像のみの判断に「みられる」「確認できない」等の留保がある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像メタデータ | 「再生時間：66.0秒 | ビットレート：1,834 kbps | ファイルサイズ：約14.9 MB」 | ローカル実測値に合わせ「再生時間：66.0秒 | ビットレート：約1,939 kbps | ファイルサイズ：約16.0 MB（約15.25 MiB）」等に修正。
W-02: source_registry | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です」 | 公開前に source_registry 登録と article_id 付番を完了し、本文の未登録注記を削除。
W-03: タイトル・作業注記 | 「【概要版#TBD】」「note転記後にこの行を削除」 | article_id 確定後に #TBD を置換し、作業用注記を本文から削除。
W-04: 略語補足 | 「右がグレースケール（IRとみられる）」 | 初出で「IR（赤外線映像とみられるが確認できない）」など日本語補足を追加。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---