---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 5
UNVERIFIABLE: 0
PASS: 9
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・複雑ネスト・Codex注釈ブロックは検出されない。
P1-1 WARN Incident Date の根拠説明が不正確。年はメタデータ由来、月日はファイル名由来として分ける必要がある。
P1-2 PASS 再生時間・解像度・フレームレート・音声有無はローカル metadata.json と概ね整合する。
P1-3 PASS DVIDS は初出で「国防映像情報配信サービス」と補足されている。
P1-4 PASS Misrep/MDR/JSIR/CSP 等の番号類は本文に出ていない。
P1-5 WARN source_registry 未登録のため、article_id・登録状態・重複状態の公開前整合性が未完了。
P2-1 WARN 標準構成の「注意点」「免責」が独立セクションとして欠落している。
P2-2 PASS CENTCOM/AOR は読者向け補足があり、重大な略語未補足はない。
P2-3 WARN 「2機のCALLSIGNがUAPを観測」はファイル名からの推定を超えており、確認事実と解釈の分離が弱い。
P2-4 PASS 距離・高度・速度・重量など換算を要する数値は出ていない。
P2-5 PASS 直訳臭・大量OCRログ・英文引用・note非互換フォーマットは検出されない。
P2-6 PASS 数値・略語注釈は本文理解を妨げる水準ではない。
IMG-1 WARN 「グレースケールIR映像」「均一グレーIR」が、IRセンサー未確認の留保と混在している。
IMG-2 PASS 移動・追跡・消失・分裂等を確定事実として断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | Incident Date：2020年8月31日（ファイル名「31_AUG」より） | 2020年はメタデータ由来、8月31日はファイル名由来として分ける。
W-02: 出典末尾 | source_registry 未登録 | 公開前に source_registry 登録後、article_id・重複・status を再確認する前提を明記する。
W-03: 記事構成 | 注意点・免責の独立セクションなし | 出典後またはAI解析メモ前後に「注意点」「免責」を通常見出しで追加する。
W-04: この資料の要点 | 2020年8月31日に2機のCALLSIGNがUAPを観測した事案 | 「CALLSIGN」2件が2機を意味するかは未確認として、「2つのCALLSIGN表記を含むファイル名」程度に留める。
W-05: 映像から視覚的に確認できる情報 | グレースケールIR映像／均一グレーIR | 「グレースケール映像。IRセンサー由来と推定されるが確認できない」に統一する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---