---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 6
UNVERIFIABLE: 0
PASS: 8
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 PASS ファイル名・Release Date・Incident Date・DVIDS ID は metadata/files_catalog.csv の対象行と矛盾しない。
P1-2 PASS duration 約298.5秒、1280×720、30fps、H.264、音声ありの技術記述はローカル素材情報と整合する。
P1-3 PASS FL・速度・高度・MGRS・機密区分など、本記事で補足必須となる未説明項目は検出されない。
P1-5 PASS metadata/files_catalog.csv 上で対象動画の同名重複は検出されず、PR088とは DVIDS ID が異なる別ファイルとして区別されている。
P2-1 WARN 所定構成のうち「注意点」「免責」に相当する独立セクションがない。
P2-2 WARN CENTCOM の初出補足が標準文言より不足しており、「米国中央軍」「米軍の統合軍」の説明が明示されていない。
P2-3 PASS 物体の正体・種別・行動意図は断定せず、「確認できない」「可能性」等の留保がある。
P2-4 PASS 日本向け換算が必要な速度・高度・距離などの単位記述は本文に出ていない。
P2-5 WARN 出典欄に thumbnails 配下の内部パスが公開本文として残っている。
P2-6 PASS DVIDS、AOR、MP4、H.264 など読者理解に必要な最低限の補足は概ね付いている。
VID-1 WARN 「グレースケールIR映像」「均一グレーIR」など、IR映像と断定する表現が留保表現と混在している。
IMG-1 WARN frame_0000 では濃淡や地表状テクスチャが見えるため、「均一グレーの背景」は視覚記述として過度に単純化されている。
P3-1 WARN source_registry 未登録および記事番号 #TBD のままで、公開前管理情報が未確定。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: P2-1 記事構成 | 注意点・免責の独立セクションなし | 「## 注意点」「## 免責」を追加し、視覚観察記事としての限界と非断定方針を整理する。
W-02: P2-2 軍事略語・組織名 | CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）に近い補足へ統一する。
W-03: P2-5 出典表記 | 代表フレーム：thumbnails/DOW-UAP-PR089_31_AUG_CALLSIGN_CALLSIGN_Observes_UAP_part2/frame_0000.png | 掲載画像出典：DOW-UAP-PR089_31_AUG_CALLSIGN_CALLSIGN_Observes_UAP_part2.mp4 より抽出（動画内00:00時点）のように公開向け表記へ置換する。
W-04: VID-1 映像種別 | 本記事は約299秒（4分59秒）のグレースケールIR映像クリップを扱います。 | グレースケール映像（IR映像の可能性はあるが確認できない）など、IR断定を避ける。
W-05: IMG-1 視覚観察精度 | 均一グレーの背景 | 濃淡のあるグレー背景、または地表状の濃淡が見える背景、など実フレームに合わせる。
W-06: P3-1 source_registry整合性 | source_registry 未登録／【概要版#TBD】 | source_registry 登録後に article_id を付与し、タイトルの #TBD を確定番号へ置換する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---