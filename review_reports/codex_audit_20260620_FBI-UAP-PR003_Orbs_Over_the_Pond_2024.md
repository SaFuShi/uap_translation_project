---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 6
UNVERIFIABLE: 0
PASS: 6
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1 BLOCK metadata/files_catalog.csv では Release Date が 6/12/26、Incident Date が October, 2024 だが、本文は Release Date を 2026年05月22日、Incident Date を 2024年とのみ記載しており一次メタデータと不一致。
P1-2 WARN ffprobe実測では r_frame_rate=25/1、duration=265.280000、bit_rate=8940529 だが、本文はフレームレートを30fpsとしており映像メタデータが不正確。
P1-3 PASS FBI、DVIDSなど本文に出る主要な固有名詞・略語は一般読者向けに最低限補足されている。
P1-4 PASS Misrep、MDR、JSIR、CSP/MRO等の番号類は本文に登場しないため該当問題なし。
P1-5 WARN review_logs/source_registry.csv に FBI-UAP-PR003_Orbs_Over_the_Pond_2024.mp4 の登録が確認できず、status・SHA256重複・公開済み重複の正式確認が未完了。
P2-1 WARN 構成は概ね整理されているが、「注意点」「免責」セクションが独立しておらず、末尾に公開前管理メモが残っている。
P2-2 PASS ISR、FMV、MISREP、AARO等の未補足問題を生む軍事略語は本文中心部に登場しない。
P2-3 WARN 「縦位置映像はFBI提出素材に特有の特徴」など、比較・特徴づけが確認範囲をやや超えて確定的に読める。
P2-4 PASS ノット、フィート、MPH等の単位換算対象は本文に登場せず、解像度・時間表記は日本語読者にも理解可能。
P2-5 WARN タイトルに「FBI FBI-UAP-PR003」と重複表記があり、「#TBD」および「note転記後にこの行を削除」の公開前文言が残っている。
P2-6 PASS FBI、DVIDS、Release 02、縦位置、MP4等には日本語補足があり、読者理解を大きく阻害する未注釈語は確認されない。
P3 BLOCK review_logs/source_registry.csv 未登録のため article_id、status、draft_path、published_date、note_url の整合性チェックを通過できない。
IMG-1 WARN 視覚観察と推定の分離は概ねできているが、「スマートフォンまたは民間カメラ」「FBI提出素材に特有」など、根拠が限定的な解釈が本文要点に残っている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像メタデータ | フレームレート：30fps | ffprobe実測に合わせて「25fps」に修正する。
W-02: source_registry管理 | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | source_registry登録後に article_id、status、重複有無を確認する。
W-03: 記事構成 | 末尾の source_registry 未登録メモ | 公開前管理メモを本文から外し、必要なら注意点・免責セクションへ整理する。
W-04: 客観性 | 縦位置映像はFBI提出素材に特有の特徴と推定されます。 | 「本ドラフトで確認したRelease 02映像群の中では、FBI映像に見られる特徴です」など確認範囲を限定する。
W-05: タイトル | # 【概要版#TBD】FBI FBI-UAP-PR003 | article_id確定後に #TBD を解消し、「FBI」の重複を除去する。
W-06: 画像記事表現 | スマートフォンまたは民間カメラによる撮影と推定されます。 | 「縦位置映像であることは確認できるが、撮影機材は本文時点では確認できない」とする。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---