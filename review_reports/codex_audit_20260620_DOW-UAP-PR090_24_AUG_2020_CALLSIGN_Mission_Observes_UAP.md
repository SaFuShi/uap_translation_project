---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 4
UNVERIFIABLE: 1
PASS: 9
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマット（Markdown table、引用ブロック、長い英文引用、2階層以上ネスト、Codex注釈ブロック）は検出されない。
P1-1 PASS File Name、Agency、Release Date、Related Location、File Type、DVIDS ID は metadata/files_catalog.csv の対象行と整合している。
P1-2 WARN Incident Date がドラフトでは「2020年8月24日」と日付まで断定されているが、metadata/files_catalog.csv の incident_date は「2020」のみであり、日付部分はファイル名由来であることの扱いをより明確にする余地がある。
P1-3 WARN CENTCOM/AOR の補足が初出では概ねあるが、標準形「米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍」より短く、後段では AOR の意味補足が省略されている。
P1-4 PASS Misrep、MDR、JSIR、CSP/MRO 等の番号類は本文に出現せず、対象外。
P1-5 WARN source_registry 未登録・article_id 未付番が本文末尾に明記されており、公開前の registry 上の status・重複確認・正式ID整合が未完了。
P2-1 WARN 構成に「注意点」「免責」の独立セクションがなく、冒頭警告と末尾注記に分散している。
P2-2 PASS DVIDS は初出で「国防映像情報配信サービス」と補足され、本文理解を大きく妨げる未説明略語は限定的。
P2-3 WARN 「水田状の景色は東アジアまたは南アジアの可能性もあります」は映像からの視覚観察を超えた地理的推測で、確認事実との分離が不十分。
P2-4 PASS フレームレート、時間、解像度などの技術数値に不整合は検出されない。
P2-5 PASS 日本語は概ね自然で、本文崩れリスクの高い生ログ・英文長文・表形式はない。
P2-6 PASS 日本語読者向けの主要組織・地域・DVIDS補足は最低限付与されている。
IMG-1 PASS 視覚観察とメタデータ由来情報を分ける方針が冒頭およびAI読解内で明示されている。
IMG-2 PASS UAP対象、IRセンサー、地名について断定を避け、「確認困難」「推定されるが確認できない」などの留保がある。
P3-1 UNVERIFIABLE source_registry.csv に当該PR090/article_idが未登録のため、Phase 3 の連番・status・note_url・重複管理は確認不能。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | Incident Date：2020年8月24日（ファイル名「24_AUG_2020」より） | Incident Date：2020年（files_catalog.csv より）。2020年8月24日はファイル名「24_AUG_2020」由来の推定日付として扱う。
W-02: 軍事略語・組織補足 | Related Location：CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍。AOR＝担当作戦地域）
W-03: source_registry整合性 | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前に source_registry 登録、article_id 付番、status・重複確認を完了する。
W-04: 記事構成 | 冒頭警告と末尾の source_registry 注記のみで、注意点・免責の独立セクションがない。 | 「注意点」または「免責」セクションを設け、未確認事項・映像説明の限界・source_registry未登録を整理する。
W-05: 視覚観察と推測の分離 | 水田状の景色は東アジアまたは南アジアの可能性もあります。 | 水田状に見える区画は確認できるが、地域推定は映像フレームのみから確認できない、という表現に留める。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---