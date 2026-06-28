---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 5
UNVERIFIABLE: 0
PASS: 8
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・複雑ネスト・Codex注釈ブロックなし。
P1-1 BLOCK Source URL が WAR.GOV トップページ URL のまま。チェックリスト上、対象資料の直接 URL でない場合は BLOCK。
P1-2 PASS 数値・単位は動画長、解像度、fps 等で、原値と補助情報の矛盾なし。
P1-3 WARN CENTCOM の説明はあるが、標準補足「米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍」には不足。
P1-4 PASS Misrep・MDR・JSIR・CSP/MRO 等の番号類は本文に出ていない。
P1-5 WARN 対象は review_logs/source_registry.csv に未登録。ドラフト末尾にも未登録と明記あり。
P2-1 WARN 構成に独立した「注意点」および「免責」セクションがない。
P2-2 WARN CENTCOM 初出補足が標準文言より弱い。
P2-3 PASS UAP対象やシアン点の意味は留保され、確認事実と推測は概ね分離されている。
P2-4 PASS 換算対象となる高度・速度・距離等の単位記述なし。
P2-5 PASS note投稿互換を崩す表・引用ブロック・長文英文引用・複雑ネストなし。タイトルと本文内容も整合。
P2-6 PASS 主要略語 DVIDS・AOR は補足あり。数値単位は動画仕様中心で読解上の換算不足なし。
P3 WARN article_id 未付番・source_registry 未登録のため、registry 整合性が未完了。
IMG-1 WARN 「標準的なDOW-UAP映像のUIスタイル」は視覚観察を超えた比較・解釈で、根拠範囲が本文内で示されていない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）
W-02: 出典・登録状態 | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前に source_registry 登録と article_id 付番を完了し、本文の未登録注記を更新する。
W-03: 記事構成 | 注意点・免責の独立セクションがない。 | 出典前後に「注意点」「免責」を独立見出しとして追加する。
W-04: ファイル名・メタデータ由来の情報 | AOR：CENTCOM（中央軍）（files_catalog.csv より） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）（files_catalog.csv より）
W-05: この資料の要点 | これはDOW-UAP映像に多く見られる標準的なUIスタイルです。 | 「中央クロスヘアと複数のシアン点が表示されています」に留めるか、比較根拠を明示する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---