---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 2
UNVERIFIABLE: 0
PASS: 12
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層以上ネスト・Codex注釈ブロックは検出なし。
P1-1 PASS 動画記事として確認可能な範囲でファイル名・公開日・機関・地域・DVIDS URLは整合。WAR.GOVトップページ併記は動画公開ページとして扱い、PDF直接URL要件は適用外。
P1-2 PASS 速度・高度・Zulu時刻等の数値換算対象は本文に該当なし。動画メタデータ値は確認情報として区分されている。
P1-3 PASS FBI・DVIDSは日本語補足あり。基地名・部隊名・MGRS・機密区分の未説明問題は該当なし。
P1-4 PASS Misrep・MDR・JSIR・CSP/MRO等の番号類は本文に該当なし。
P1-5 PASS 本文上、既存公開記事との内容重複を示す記述は検出なし。
P2-1 WARN 標準構成のうち、出典後の明示的な免責セクションがない。
P2-2 PASS 軍事略語・専門用語の未補足による主要な読解支障はなし。
P2-3 PASS 視覚確認情報と推定・未確認情報は概ね分離され、物体の正体・意図を断定していない。
P2-4 PASS 換算対象となる速度・高度・距離等の主要単位は本文に該当なし。
P2-5 PASS note投稿互換上の禁止フォーマット、長文英文引用、複雑ネストは検出なし。記事タイトルも本文内容と概ね一致。
P2-6 PASS 日本語読者向けの組織名・略語補足は必要範囲で記載あり。
P3 WARN source_registry未登録・article_id未付番の内部管理状態が本文末尾に残っている。
IMG-1 PASS 画像・映像記事として、視覚観察と解釈は概ね分離され、「推定」「確認できない」の留保もある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 構成 | 出典後に明示的な「免責」セクションがない | 出典後に「## 免責」を置き、公開資料・映像フレーム確認に基づく概要であり、物体の正体や意図を断定しない旨を短く明記する。
W-02: source_registry | ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。公開前に source_registry への登録が必要です。 | 公開前にsource_registry登録とarticle_id付番を完了し、公開用本文から内部管理メモを削除する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---