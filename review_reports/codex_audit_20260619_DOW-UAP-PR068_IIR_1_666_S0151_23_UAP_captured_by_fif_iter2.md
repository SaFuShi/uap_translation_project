---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 1
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 BLOCK review_logs/source_registry.csv に対象ファイルの登録がなく、記事タイトルも「#TBD」のため article_id 未付番状態。公開前の provenance 要件を満たさない。
P1-1-META PASS metadata/files_catalog.csv およびローカル動画メタデータと、ドラフトのファイル名・Release Date・Incident Date・NORTHCOM・DVIDS ID・映像仕様は整合している。
P1-2 PASS 速度・高度・FL・Zulu時刻など、換算誤りを生む数値記述は本文にない。
P1-3 PASS IIR・NORTHCOM・DVIDS は初出付近で日本語補足されている。
P1-5 UNVERIFIABLE source_registry 未登録のため、SHA256重複・公開済み記事重複・registry status の確認が完了できない。
P2-1 WARN タイトルの「#TBD」と本文中の「note転記後にこの行を削除」が公開用ドラフト本文に残っている。
P2-1-STRUCT PASS 「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」の主要構成と、3項目の要点は満たしている。
P2-2 WARN AOR が「担当AOR」として初出しており、初出時の展開補足が弱い。
P2-3 PASS 宇宙人・異星人等の論壇的表現はなく、対象物の正体や行動意図は断定していない。
P2-5 PASS OCRログ・生英文大量貼付・直訳臭の強い定型表現は検出されない。
IMG-1 WARN 赤いボーダーを「筐体外縁またはビューファインダー枠」とする解釈は、映像フレームのみでは根拠不足。
IMG-2 PASS 対象物の移動・追跡・消失・分裂・複数化などを確定事実として断定していない。
IMG-3 PASS 画像由来の記述に「確認できる」「可能性がある」「確認できない」の留保が付いている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: タイトル・代表フレーム行 | 「#TBD」「（note転記後にこの行を削除）」 | article_id 付番後に #TBD を置換し、転記作業メモ行は本文から削除する。
W-02: 文書メタデータ | 「担当AOR」 | 「AOR（Area of Responsibility：担当区域）」のように初出補足する。
W-03: 赤いボーダーの解釈について | 「センサー筐体の外縁またはビューファインダー枠の映り込みとみられます」 | 「赤い帯状の外枠が確認できる。機材由来か画面表示由来かは映像のみでは確認できない」に弱める。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---