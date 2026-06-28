---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 2
UNVERIFIABLE: 0
PASS: 11
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 BLOCK Release Date が本文「2026年05月22日」と metadata/files_catalog.csv・uap-data.csv「5/8/26」で不一致。
P1-2 PASS 再生時間・解像度・フレームレート・ビットレート・音声情報は ffprobe 結果と概ね整合。
P1-3 PASS INDOPACOM・AOR・DVIDS の補足は記事単独理解に必要な範囲で記載されている。
P1-4 PASS Misrep・MDR・JSIR・CSP/MRO 等の番号類は本文に出現せず、該当違反なし。
P1-5 PASS 同一ファイル名・DVIDS ID の重複記事は確認されず、BLOCK 状態の既存登録も検出されない。
P2-1 WARN 標準構成のうち「注意点」「免責」セクションが独立していない。
P2-2 PASS 軍事略語・専門用語の未補足による重大な読みづらさは確認されない。
P2-3 PASS 視覚観察と推測は概ね分離され、物体の正体・種別・意図を断定していない。
P2-4 PASS 単位換算の誤り・過精密換算・原文値欠落は確認されない。
P2-5 PASS note投稿互換上の禁止フォーマットはなく、タイトルと本文内容も概ね一致。
P2-6 PASS 日本語読者向けの組織名・略語補足は必要範囲で付されている。
P3-1 WARN source_registry.csv に当該記事の article_id 登録がなく、タイトルも #TBD のまま。
IMG-1 PASS 画像記事として、視覚観察には「確認できる」「可能性があるが確認できない」等の留保がある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 記事構成 | AI読解の後に出典へ進み、独立した「注意点」「免責」セクションがない | 「注意点」と「免責」を標準構成として独立セクション化する。
W-02: source_registry | 「source_registry 未登録」「【概要版#TBD】」 | source_registry 登録後、article_id を確定し #TBD を置換する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---