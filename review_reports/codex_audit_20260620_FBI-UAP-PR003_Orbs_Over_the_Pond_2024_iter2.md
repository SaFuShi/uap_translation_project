---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 7
UNVERIFIABLE: 0
PASS: 6
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1 WARN File Name、Agency、Release Date、Related Location、DVIDS IDはmetadata/files_catalog.csvと整合するが、Incident Dateはカタログ上「October, 2024」であり、本文の「2024年」「具体的な月・日付は不明」は一次メタデータより粗い。
P1-2 WARN ffprobe実測では動画ストリームは25fpsだが、本文は「30fps」と記載している。
P1-3 PASS FBI、DVIDSなど本文に出る主要固有名詞・略語は最低限補足されている。
P1-4 PASS Misrep、MDR、JSIR、CSP/MRO等の番号類は本文に登場しない。
P1-5 WARN review_logs/source_registry.csv に対象MP4の登録が確認できず、status・重複・公開済み記事との正式照合が未完了。
P2-1 WARN 標準構成のうち「注意点」「免責」相当の独立セクションがない。
P2-2 PASS ISR、FMV、MISREP、AARO等の未補足問題を生む軍事略語は本文中心部に登場しない。
P2-3 WARN 「Release 02のDOW-UAP映像は全て横位置」「FBI提出素材に特有」など、比較・特徴づけの根拠範囲が本文内で示されていない。
P2-4 PASS ノット、MPH、フィート等の単位換算対象は本文に登場しない。
P2-5 WARN タイトルに「FBI FBI-UAP-PR003」と機関名重複があり、「#TBD」の公開前表記も残っている。
P2-6 PASS FBI、DVIDS、縦位置、MP4等には日本語補足があり、読者理解を大きく阻害する未注釈語は確認されない。
P3 BLOCK source_registry.csv 未登録のため、article_id、status、draft_path、published_date、note_url の整合性チェックを通過できない。
IMG-1 WARN 視覚観察とメタデータ由来情報の分離方針は明記されているが、「スマートフォンまたは民間カメラと推定」「撮影機材は確認できない」は、uap-data上のiPhone撮影説明と整合しない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | Incident Date：2024年（ファイル名「2024」より。具体的な月・日付は不明） | metadata/files_catalog.csv / uap-data に合わせ「2024年10月（カタログ由来。具体的な日付は不明）」とする。
W-02: 映像メタデータ | フレームレート：30fps | ffprobe実測に合わせて「25fps」に修正する。
W-03: source_registry管理 | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 登録後に article_id、status、重複有無を確認する。
W-04: 記事構成 | 冒頭警告と末尾のsource_registry注記のみで、注意点・免責の独立セクションがない。 | 「注意点」「免責」セクションを独立させ、未確認事項と管理メモを整理する。
W-05: 比較評価 | 縦位置映像はRelease 02ではFBI映像（PR003・PR004）のみ確認 | 比較根拠を示すか、「本映像は縦位置映像です」程度に限定する。
W-06: タイトル | # 【概要版#TBD】FBI FBI-UAP-PR003 | article_id確定後に #TBD を解消し、「FBI」の重複を除去する。
W-07: 画像記事表現 | 可視光カメラ・スマートフォンまたは民間カメラと推定されるが確認できない | uap-data由来情報として「民間人がiPhoneで撮影した映像と説明されている」と根拠を分けて記述する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---