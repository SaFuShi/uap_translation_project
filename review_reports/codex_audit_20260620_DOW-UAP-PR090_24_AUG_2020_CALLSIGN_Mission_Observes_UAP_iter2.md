---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 5
UNVERIFIABLE: 1
PASS: 8
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマット（Markdown table、引用ブロック、長い英文引用、2階層以上ネスト、Codex注釈ブロック）は検出されない。
P1-1 PASS File Name、Agency、Release Date、Related Location、File Type、DVIDS ID は metadata/files_catalog.csv および対象動画メタデータと概ね整合している。
P1-2 PASS ffprobe 上の MP4、1280x720、30fps、298.0秒、音声ありの記述は対象動画と整合している。
P1-3 WARN CENTCOM/AOR の補足はあるが、標準形「米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍」より短く、後段の再出時補足も弱い。
P1-4 PASS Misrep、MDR、JSIR、CSP/MRO 等の番号類は本文に出現せず、対象外。
P1-5 WARN source_registry 未登録・article_id 未付番が本文末尾に明記されており、公開前の registry 上の status・重複確認・正式ID整合が未完了。
P2-1 WARN 構成に「注意点」「免責」の独立セクションがなく、冒頭警告と末尾注記に分散している。
P2-2 PASS DVIDS は初出で「国防映像情報配信サービス」と補足され、本文理解を大きく妨げる未説明略語は限定的。
P2-3 WARN 冒頭で「グレースケールIR俯瞰映像クリップ」と断定しており、後続の「IRセンサー由来の可能性はあるが確認できない」と矛盾気味。
P2-4 PASS 時間・解像度・フレームレートなどの技術数値に不自然な換算・単位問題は検出されない。
P2-5 PASS 日本語は概ね自然で、本文崩れリスクの高い生ログ・英文長文・表形式はない。
IMG-1 WARN 「水田状の景色は東アジアまたは南アジアの可能性もあります」は映像からの視覚観察を超えた地理的推測で、確認事実との分離が不十分。
IMG-2 PASS UAP対象・地名については「確認困難」「確認できません」として断定を避けている。
P3-1 UNVERIFIABLE review_logs/source_registry.csv に当該PR090/article_idが未登録のため、Phase 3 の連番・status・note_url・重複管理は確認不能。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 軍事略語・組織補足 | Related Location：CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍。AOR＝担当作戦地域）に修正する。
W-02: source_registry整合性 | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前に source_registry 登録、article_id 付番、status・重複確認を完了する。
W-03: 記事構成 | 冒頭警告と末尾の source_registry 注記のみで、注意点・免責の独立セクションがない。 | 「注意点」または「免責」セクションを設け、未確認事項・映像説明の限界・source_registry未登録を整理する。
W-04: 映像種別の断定 | 本記事は約298秒（4分58秒）のグレースケールIR俯瞰映像クリップを扱います。 | 「グレースケールの俯瞰映像クリップ」に留め、IR由来は「可能性はあるが確認できない」と別記する。
W-05: 視覚観察と推測の分離 | 水田状の景色は東アジアまたは南アジアの可能性もあります。 | 水田状に見える区画は確認できるが、地域推定は映像フレームのみから確認できない、という表現に留める。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---