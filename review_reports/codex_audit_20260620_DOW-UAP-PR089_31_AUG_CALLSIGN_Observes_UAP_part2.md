---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 6
UNVERIFIABLE: 0
PASS: 8
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 PASS ファイル名・Release Date・Incident Date・DVIDS ID は metadata/files_catalog.csv およびローカル動画メタデータと矛盾しない。
P1-2 PASS ffprobe上の duration=298.5秒、1280x720、30fps、H.264、音声ありと本文の技術記述は概ね整合する。
P1-3 PASS FL・速度・高度・MGRS・機密区分など、本記事に該当する未補足の番号・単位項目はない。
P1-5 PASS metadata/files_catalog.csv 上で対象動画の同名重複は確認されず、PR088との関連も DVIDS ID 別ファイルとして区別されている。
P2-1 WARN 所定構成のうち「注意点」「免責」に相当する独立セクションがなく、公開前作業メモも本文内に残っている。
P2-2 WARN CENTCOM の初出補足が標準文言より不足しており、「米国中央軍」「米軍の統合軍」の説明が明示されていない。
P2-3 PASS 物体の正体・種別・行動意図は断定せず、「確認できない」「可能性」等の留保がある。
P2-4 PASS 日本向け換算が必要な速度・高度・距離などの単位記述は本文に出ていない。
P2-5 WARN 「note転記後にこの行を削除」という編集メモが note_drafts 本文内に残っている。
P2-6 PASS DVIDS、AOR、MP4、H.264 など読者理解に必要な最低限の補足は概ね付いている。
IMG-1 WARN 「グレースケールIR映像」と断定している箇所があり、IRセンサー未確認という留保と混在している。
IMG-2 PASS 「移動」「追跡」「消失」「分裂」などの動的事象を確定事実として断定していない。
IMG-3 WARN frame_0000 は濃淡や地表状テクスチャが見えるため、「均一グレーの背景」は視覚記述として過度に単純化されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: P2-1 記事構成 | 注意点・免責の独立セクションなし | 「## 注意点」「## 免責」を出典前後の所定位置に追加し、視覚観察記事としての限界と非断定方針を整理する。
W-02: P2-2 軍事略語・組織名 | CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）に近い補足へ統一する。
W-03: P2-5 note投稿互換 | → 使用ファイル：thumbnails/...（note転記後にこの行を削除） | 公開用本文から削除し、画像キャプションのみを残す。
W-04: IMG-1 画像記事・機器解釈 | グレースケールIR映像（IRセンサーと推定されるが確認できない） | グレースケール映像（IR映像の可能性があるが確認できない）のように、IR断定を避ける。
W-05: IMG-3 視覚観察精度 | 均一グレーの背景 | 濃淡のあるグレー背景、または地表状の濃淡が見える背景、など実フレームに合わせる。
W-06: P3-1 source_registry整合性 | source_registry 未登録／【概要版#TBD】 | source_registry 登録後に article_id を付与し、タイトルの #TBD を確定番号へ置換する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---