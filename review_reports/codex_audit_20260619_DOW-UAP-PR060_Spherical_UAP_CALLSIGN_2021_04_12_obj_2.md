---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 3
UNVERIFIABLE: 0
PASS: 11
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 WARN source_registry.csv に当該ドラフトの登録がなく、article_id が #TBD のまま。公開前の登録・付番が必要。
P1-2 PASS 日付・動画時間・解像度・fps・容量・ビットレート等はローカル ffprobe/metadata と整合している。
P1-3 PASS CENTCOM、AOR、DVIDS、CALLSIGN、obj_2 は初出付近で補足されている。
P1-4 PASS Misrep/MDR/JSIR/CSP/MRO 等の番号類は本文対象外で、未説明による問題はない。
P1-5 PASS files_catalog.csv とのファイル名・DVIDS ID・Release Date・VID種別の整合は確認できる。
P2-1 WARN 画像差し込み用の作業メモ「note転記後にこの行を削除」が本文に残っている。
P2-2 PASS 軍事略語・専門語は記事単独理解に必要な範囲で日本語補足されている。
P2-3 PASS 視覚確認情報とファイル名・メタデータ由来情報が分離され、物体種別や行動意図の断定は避けられている。
P2-4 PASS 換算対象となる高度・速度・距離等の原文単位は本文にほぼ出ておらず、換算不備はない。
P2-5 PASS 直訳臭・大量OCRログ・長文英文引用・note非互換フォーマットは検出されない。
P2-6 PASS 日本語読者向けに動画種別、CENTCOM、DVIDS、AOR、CALLSIGN 等の補足がある。
P3-1 WARN source_registry.csv 未登録のため、article_id 連番・status・note_url・公開管理との整合確認が未完了。
IMG-1 PASS 画像記事追加チェック上、視覚観察と解釈は概ね分離され、「可能性」「確認困難」等の留保もある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ/末尾管理情報 | 「【概要版#TBD】」「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | 公開前に source_registry.csv へ登録し、article_id を確定したうえで #TBD を置換する。
W-02: 代表フレーム挿入部 | 「→ 使用ファイル：...（note転記後にこの行を削除）」 | note本文に残さず、画像挿入作業後はこの作業メモ行を削除する。
W-03: source_registry整合性 | source_registry.csv 未登録のため、article_id 連番・status・note_url・公開管理の整合が確認できない。 | 登録後に P3 source_registry 整合性を再確認する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---