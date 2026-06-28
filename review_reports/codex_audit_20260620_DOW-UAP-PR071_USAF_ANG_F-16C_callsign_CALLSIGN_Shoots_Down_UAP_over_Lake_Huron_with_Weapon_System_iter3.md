---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 12
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは検出されない。
P1-1 BLOCK review_logs/source_registry.csv に当該MP4の登録がなく、本文末尾でも source_registry 未登録・article_id 未付番と明記されている。
P1-2 PASS 動画仕様は MP4、H.264、1920×1080、30fps、46.766667秒、AAC音声ありで、本文の技術メタデータと整合している。
P1-3 PASS USAF ANG、NORTHCOM、AOR、DVIDS は初出付近で日本語補足されている。
P1-4 PASS Misrep、MDR、JSIR、CSP、MRO 等の番号類は本文に登場しない。
P1-5 PASS ローカル検索範囲では source_registry 上の同一ファイル登録・公開済み重複記事は確認されない。
P2-1 WARN 構成に「注意点」および明示的な免責セクションがなく、チェックリストの標準順序から外れている。
P2-1 WARN タイトルが「#TBD」のままで、公開用 article_id が未確定。
P2-2 PASS 軍事略語・組織名は記事単独理解に必要な範囲で補足されている。
P2-3 WARN 冒頭で「IRセンサー映像クリップ」と断定気味に書いた後、本文では「可能性はあるが確認できない」としており、推定と確認事実の分離が不安定。
P2-4 PASS 速度・高度・距離・重量など、換算対象となる数値単位は本文に登場しない。
P2-5 PASS note投稿互換上の禁止フォーマット、作業メモ行、大量OCRログ、生英文引用は検出されない。
P2-6 PASS 日本語読者向けに、DVIDS、AOR、NORTHCOM、USAF ANG などの補足がある。
IMG-1 PASS 映像冒頭の黒画面、00:15以降のグレースケール俯瞰映像、00:40代表フレームの説明は、抽出フレーム・metadata.json と矛盾しない。
IMG-2 PASS 物体の正体・種別・行動意図、撃墜の詳細、兵器システムの具体内容は断定されていない。
M5 PASS WAR.GOV公開ページ、DVIDS ID、DVIDS URL、元ファイル名が出典欄に記載されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 記事構成 | 出典後に「source_registry 未登録」警告のみがあり、注意点・免責セクションが明示されていない | 「## 注意点」「## 免責」を標準順序に沿って追加し、映像判断の不確実性を整理する。
W-02: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR071... | source_registry 登録後に確定 article_id を反映する。
W-03: 冒頭説明 | 本記事は約47秒のIRセンサー映像クリップを扱います | 「IRセンサー由来の可能性がある約47秒のグレースケール映像クリップ」など、推定であることを初出から明記する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---