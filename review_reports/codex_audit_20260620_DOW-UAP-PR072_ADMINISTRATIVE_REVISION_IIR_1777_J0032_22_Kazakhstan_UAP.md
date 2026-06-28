---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 4
UNVERIFIABLE: 2
PASS: 8
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-1 WARN source_registry.csv に対象ファイルの登録が確認できず、タイトルも「#TBD」のままで article_id 未確定。
P1-2 PASS ffprobe実測値と本文の動画メタデータは概ね整合し、単位・日付時刻の矛盾は確認されない。
P1-3 PASS DVIDS は日本語補足あり。MGRS・基地名・部隊名・機密区分等の未説明リスク対象は本文に出ていない。
P1-4 PASS IIR番号は「推定」と明記され、番号類の過剰断定は確認されない。
P1-5 UNVERIFIABLE source_registry.csv 未登録のため、status・SHA256重複・公開済み記事重複の正式確認ができない。
P2-1 WARN 構成に独立した「注意点」「免責」セクションがなく、末尾に公開前管理メモが残っている。
P2-2 PASS 読者理解に必要な DVIDS 補足があり、未説明の主要軍事略語の多用は確認されない。
P2-3 WARN ADMINISTRATIVE REVISION の意味を「内容の修正または再編集を経た版」とする記述が、ファイル名由来の推定としてはやや断定的。
P2-4 PASS 換算対象となる高度・速度・距離等の原文単位は本文に出ていない。
P2-5 PASS note投稿互換上の禁止フォーマット、直訳臭の強い表現、大量OCRログ、長文英文引用は確認されない。
P2-6 PASS 日本語読者向けの最低限の組織名・地名補足はあり、過長な注釈反復も確認されない。
P3 UNVERIFIABLE source_registry.csv 未登録のため、article_id連番・status・note_url・published_date等の整合確認ができない。
IMG-1 WARN 「強い光源とみられる」など視覚観察から一歩進んだ解釈が一部あり、確認事実との差分をより明確にできる。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ/末尾管理情報 | 「#TBD」「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | source_registry登録後に article_id を確定し、#TBD と公開前管理メモを削除または公開用表記へ更新する。
W-02: 記事構成 | 独立した「注意点」「免責」セクションがない | メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責 の順に揃える。
W-03: この資料の要点 | 「本映像が原版から何らかの修正または再編集を経た版であることを示す可能性があります」 | 「ファイル名上は管理改訂版とされますが、具体的な改訂内容は本文情報だけでは確認できません」などに留める。
W-04: 映像から視覚的に確認できる情報 | 「地平線付近に白い光の放射状パターン（強い光源とみられる）」 | 「白い光の放射状パターンが確認できる。強い光源かどうかは映像フレームのみでは確認できません」と分離する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---