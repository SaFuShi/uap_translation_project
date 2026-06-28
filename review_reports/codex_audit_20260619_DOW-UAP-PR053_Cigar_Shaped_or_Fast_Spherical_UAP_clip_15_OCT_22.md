---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 6
UNVERIFIABLE: 0
PASS: 7
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマットは検出されない。
P1-1 BLOCK Source URL が WAR.GOV トップページのままで、対象資料への直接URLになっていない。
P1-1 PASS ファイル名、公開日、DVIDS ID、動画メタデータは整合。
P1-2 PASS 日付・時間・動画長・解像度等の数値は一貫。
P1-3 PASS CENTCOM は初出で日本語補足あり。
P2-1 PASS 構成と要点3項目は基準に適合。
P2-1 WARN 画像差し込み用の作業メモが本文内に残存。
P2-3 WARN 「センサーが対象を追尾」は機器動作の断定寄り。
P2-3 WARN 高速移動確認に関する記述が確認範囲を超えて読める。
P2-3 PASS 正体・種別・形状確定は断定回避されている。
P2-5 PASS 表、引用ブロック、大量英文、Codex注釈なし。
P2-5 WARN 赤外線映像推定の留保をより近接表示すべき。
IMG-1 WARN 「追尾対象」「空中」など一部解釈語が観察事実に近い。
P3 WARN source_registry.csv 未登録・article_id 未付番。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 画像差し込み行 | → 使用ファイル：thumbnails/DOW-UAP-PR053/frame_0005.png（note転記後にこの行を削除） | 公開本文から削除する。
W-02: この資料の要点 | グレースケールの俯瞰映像でセンサーが地上の対象を追尾している | 追尾クロスヘアと明るい対象らしき領域が確認できる、に弱める。
W-03: 注意点 | 映像を通して視聴することで確認できます | 全編視聴での確認結果と抽出フレーム確認を分ける。
W-04: タイトル・映像説明 | 赤外線映像と推定／赤外線センサー映像の特徴を示す | センサー種別未確認を同じ文脈で明記する。
W-05: 俯瞰映像の地上コンテキスト | UAP（追尾対象）は地上ではなく空中にあるとみられます | 高度・距離・前後関係は確認不可、とする。
W-06: source_registry | source_registry.csv への登録・article_id の付番が未実施です | 公開前に登録と付番を完了する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---