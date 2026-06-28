---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 2
UNVERIFIABLE: 0
PASS: 12
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 PASS ファイル名・Release Date・Incident Date・Related Location・DVIDS ID はドラフト本文と metadata/files_catalog.csv の対象行で整合している。
P1-2 PASS FL・速度・高度・Zulu時刻などの換算検証対象となる数値記述はない。
P1-3 PASS AFRICOM は初出で「アフリカ軍」と補足され、DVIDS も初出で説明されている。
P1-4 PASS Misrep・MDR・JSIR・CSP/MRO 等の番号類は本文に登場しない。
P1-5 WARN source_registry 未登録・article_id 未付番であり、公開前の登録状態を満たしていない。
P2-1 WARN 構成に独立した「注意点」および「免責」セクションがなく、所定順「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」を満たさない。
P2-2 PASS ISR・FMV・SIGINT・IMINT・AARO・USCENTCOM・MISREP 等の未補足略語は本文に登場しない。
P2-3 PASS 物体の正体・種別・行動意図を断定せず、確認事実と推定を概ね分離している。
P2-4 PASS 単位換算の誤りを生む速度・高度・距離・重量などの記述はない。
P2-5 PASS note_drafts 本文として不適な表・引用ブロック・英文長文引用・Codex注釈ブロック・複雑なネストはない。
P2-6 PASS 日本語読者向けに AFRICOM・AOR・DVIDS などの主要略語補足がある。
IMG-1 PASS 視覚観察と解釈は「確認できる情報」「メタデータ由来の情報」に分けられている。
IMG-2 PASS 移動・追跡・消失・分裂・複数化・物体種別を確定事実として断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry 整合性 | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | 公開前に source_registry.csv へ登録し、article_id を付番する。
W-02: 記事構成 | 現在の構成は「文書メタデータ → 要点 → AI読解 → 出典 → source_registry 未登録注記」で、独立した「注意点」「免責」セクションがない。 | 出典の前後に「## 注意点」「## 免責」を追加し、視覚観察記事としての留保と非断定方針を所定位置に整理する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---