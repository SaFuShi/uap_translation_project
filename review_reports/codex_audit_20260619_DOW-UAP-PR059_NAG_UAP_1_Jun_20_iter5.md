---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 3
UNVERIFIABLE: 2
PASS: 9
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマット（Markdown table、引用ブロック、長文英文引用、2階層以上ネスト箇条書き、Codex注釈ブロック）は検出されない
P1-1 WARN source_registry未登録のため公開前メタデータ管理が未完了。ドラフト末尾にも未登録注記あり
P1-2 PASS 動画メタデータ値はローカルffprobeおよびthumbnails metadata.jsonと概ね一致する
P1-3 PASS CENTCOM、AOR、DVIDS、HUD等の主要略語は初出付近で日本語補足されている
P1-4 PASS Misrep/MDR/JSIR等の番号類は本文に出現せず対象外
P1-5 UNVERIFIABLE source_registry未登録のため当該資料のregistry上のstatus、SHA256重複、公開済み重複は確認不能
P2-1 WARN 画像差し込み用の作業指示行「note転記後にこの行を削除」が本文内に残存している
P2-2 PASS 軍事略語・専門用語は本記事の範囲では読者向け補足が概ね足りている
P2-3 WARN 物体の出現開始フレームについて、要点ではframe_0060、タイムライン/AI解析メモではframe_0030付近となっており記事内で揺れがある
P2-4 PASS 高度・速度・距離などの換算対象となる原文単位値は本文に実質出現しない
P2-5 PASS 読みやすさ上の重大な崩れ、直訳臭、表、引用ブロック、生英文貼付は検出されない
P2-6 PASS 日本語読者向けの注釈は本記事の範囲では概ね充足している
IMG-1 PASS 視覚観察と解釈は概ね分離され、「推定」「確認できない」「可能性」等の留保がある
P3-1 UNVERIFIABLE source_registry.csvに当該PR059/article_id未登録のためPhase 3の連番・status・note_url整合性は確認不能
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry整合性 | ⚠️ source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前にsource_registryへ登録し、article_id、status、URL、重複確認状態を確定する
W-02: note投稿本文 | → 使用ファイル：thumbnails/DOW-UAP-PR059_NAG_UAP_1_Jun_20/frame_0240.png（note転記後にこの行を削除） | note投稿本文から作業指示行を削除し、必要なら画像キャプションのみ残す
W-03: 内部整合性 | frame_0060（01:00）から白い明るい点状の物体が確認でき始め / frame_0030：フレーム左端付近に小さな白い点（物体候補）が確認できる | 出現開始を「frame_0030では物体候補、frame_0060以降でより明確」などに統一する
---WARN_DETAILS_END---
---CODEX_AUDIT_END---