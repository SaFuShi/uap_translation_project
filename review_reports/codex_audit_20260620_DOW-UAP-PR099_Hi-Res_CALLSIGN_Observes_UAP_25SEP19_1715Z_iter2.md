---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 0
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマット（Markdown table、引用ブロック、長文英文引用、2階層以上ネスト、Codex注釈ブロック）は検出なし
P1-1-FILE BLOCK review_logs/source_registry.csv に DOW-UAP-PR099 / DVIDS 1007738 の登録がなく、ファイル名・status・重複状態を台帳基準で照合不能
P1-1-DATE WARN metadata/files_catalog.csv の incident_date は 2023 だが、本文はファイル名由来で 2019年9月25日17:15Z と記述しており、ローカルメタデータ間に不一致あり
P1-1-URL PASS 動画記事として WAR.GOV 公開ページと DVIDS 直接URLが併記されている
P1-2-TIME PASS 25SEP19_at_1715Z 由来の日時表記は本文内で一貫
P1-2-MEDIA PASS ffprobe/metadata.json と本文の 291.4秒、4:51、1280x720、30fps、H.264、音声ありは整合
P1-3-ABBR PASS DVIDS、AOR、CENTCOM は本文内で日本語補足あり
P1-5-DUP PASS source_registry登録済み記事との直接重複は rg 検索範囲では検出なし
P2-1-STRUCT WARN 「注意点」「免責」セクションが明示されておらず、構成要件が一部不足
P2-1-POINTS PASS 要点は3項目の番号付き太字で記述
P2-3-OBJECTIVITY PASS UAP対象の正体・種別・行動意図は断定せず、視覚確認情報とメタデータ由来情報を分離
P2-5-READABILITY PASS OCRログ・生英文大量貼付・直訳臭・複雑なネスト箇条書きは検出なし
IMG-IR WARN 「IR」表現が、確認不能という留保と併記されつつ複数箇所で断定的に出ている
IMG-REL WARN PR097との「同一事案」関係は、同日・時刻違い以上の根拠が本文中で確認できず推定が強い
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | metadata/files_catalog.csv では PR099 の incident_date が 2023、本文では「2019年9月25日 17:15Z」 | ファイル名由来の2019表記は維持しつつ、files_catalog側の incident_date 不一致を確認・修正対象として扱う
W-02: 記事構成 | 「注意点」「免責」セクションが明示されていない | 出典後またはAI読解後に、視覚観察記事としての注意点と免責を独立見出しで追加
W-03: 冒頭・画像キャプション・AI読解 | 「グレースケールIR俯瞰映像」 | 「グレースケールの俯瞰映像（IR映像の可能性はあるが、本文上は確認不能）」に統一
W-04: この資料の要点 | 「同日・同一事案の異なる時刻のクリップ。本映像が先行」 | 「同日の別クリップの可能性。本映像の時刻がPR097より先行」に弱める
---WARN_DETAILS_END---
---CODEX_AUDIT_END---