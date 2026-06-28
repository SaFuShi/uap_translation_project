---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 10
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上ネスト箇条書き、Codex注釈ブロックは検出されない
P1-1 BLOCK review_logs/source_registry.csv に DOW-UAP-PR059_NAG_UAP_1_Jun_20.mp4 の登録がなく、本文でも source_registry 未登録・article_id 未付番と明記されている
P1-2 PASS ffprobe値は thumbnails metadata.json と整合している
P1-3 PASS CENTCOM、AOR、DVIDS は初出付近で日本語補足されている
P1-5 PASS metadata/files_catalog.csv のファイル名、Agency、Release Date、Related Location、DVIDS ID、file_type は本文メタデータと整合している
P2-1 WARN 記事タイトルが「#TBD」のままで、末尾に source_registry 未登録・article_id 未付番の公開前メモが残っている
P2-2 PASS 対象記事に出る主要略語・組織名は初出時に補足されている
P2-3 WARN 「追尾コーナーブラケット」など、画面表示の視覚観察と機器動作の解釈が一部混在している
P2-4 PASS 単位換算を要する速度・高度・距離等の原文数値は本文にない
P2-5 WARN 代表フレーム指定行に「note転記後にこの行を削除」という作業メモが本文内に残っている
P2-6 PASS 日本語読者向けの基本補足は過不足なく、長すぎる反復注釈は目立たない
IMG-1 PASS 方位表示は読み取り困難な箇所で断定が抑制されている
IMG-2 PASS 物体の正体・種別・行動意図は断定されず、視覚確認範囲とメタデータ由来情報は概ね分離されている
M5 PASS war.gov公開ページと DVIDS URL が併記され、DVIDS URL の ID は files_catalog.csv の dvids_video_id=1007727 と一致している
---ITEMS_END---
---WARN_DETAILS_START---
W-01: タイトル/末尾 | # 【概要版#TBD】、source_registry 未登録、article_id の付番が未実施 | source_registry 登録後に確定 article_id を反映し、未登録注意書きを公開前に削除する
W-02: 注意点 | シアン色の追尾コーナーブラケットが物体周辺を囲む状態 | 「シアン色のコーナーブラケット状表示」など視覚形状を主語にし、追尾機能は確認不能または推定として分ける
W-03: 代表フレーム行 | → 使用ファイル：thumbnails/...（note転記後にこの行を削除） | 公開本文には作業メモを残さず、必要なら画像キャプションのみ残す
---WARN_DETAILS_END---
---CODEX_AUDIT_END---