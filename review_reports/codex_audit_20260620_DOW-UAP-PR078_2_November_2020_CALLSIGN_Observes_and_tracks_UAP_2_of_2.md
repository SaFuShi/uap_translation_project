---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 4
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない
P1-1 PASS ファイル名・公開日・Incident Date・CENTCOM・DVIDS IDの本文内整合は概ね保たれている
P1-2 PASS 数値は動画時間・解像度・fps中心で、単位換算の重大な不整合は検出されない
P1-3 PASS DVIDSは初出で説明され、CENTCOMも中央軍および担当地域の補足がある
P1-5 WARN source_registry未登録であることが本文末尾に明記されており、公開前登録が未完了
P2-1 WARN 構成上、独立した「注意点」および「免責」セクションが不足している
P2-1 PASS 要点は3項目の番号付き太字で記述されている
P2-2 PASS AOR・DVIDS・CENTCOMなど主要略語には日本語補足がある
P2-3 PASS 物体の正体・種別・行動意図を断定しない方針は明記されている
P2-3 WARN 「追跡」「継続映像」「同一事案」など、ファイル名由来の解釈が一部で確定調に寄っている
P2-5 PASS OCRログや生英文の大量貼り付けはない
P2-5 PASS タイトルは対象ファイル・日付・2 of 2・PR077関連という本文内容と概ね一致している
IMG-1 WARN 「グレースケールIR俯瞰映像」「水面IRグレースケール」が、確認不能注記と併存しつつIR断定に読める
IMG-2 PASS 視覚観察情報とファイル名・メタデータ由来情報はセクションで分離されている
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry | ⚠️ source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前に登録完了後、記事ID・登録済み状態に更新する
W-02: 記事構成 | 「注意点」「免責」の独立セクションがない | 出典前後に注意点・免責を明示し、映像記事としての確認限界を整理する
W-03: この資料の要点 | PR077（1 of 2）の継続映像（2 of 2）です。同日・同一事案の後続クリップとみられます。 | 「2 of 2の関連クリップとみられる」など、継続・同一事案の断定を弱める
W-04: 映像表現 | グレースケールIR俯瞰映像／水面IRグレースケール | 「グレースケール俯瞰映像（IR映像の可能性があるが未確認）」に統一する
---WARN_DETAILS_END---
---CODEX_AUDIT_END---