---CODEX_AUDIT_START---
VERDICT: PASS
BLOCK: 0
WARN: 0
UNVERIFIABLE: 0
PASS: 14
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-REG PASS タイトルに「#R02-090」が明記されており、末尾にarticle_id（R02-090 / #2_090 / publish_order: 2090）が正式採番済みとして記録されている。source_registry.csv への登録は公開キュー投入時に実施予定と明記されており、外部登録待ちとして許容。
P1-META PASS ファイル名（DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission.mp4）、Release Date（2026年05月22日）、DVIDS ID（1007708）は metadata/files_catalog.csv と整合する。Related Location は files_catalog.csv 上も「未記録（空欄）」であり、本ドラフトの「不明」記述と整合する。
P1-DATE PASS Incident Date は files_catalog.csv・ファイル名双方に日時情報なしであり、本ドラフトが「不明」と記述していることと整合する。AARO公式説明内の「2026年03月06日」（議会要請日）はゼロ埋め形式で記述されている。
P1-SOURCE PASS DVIDS URL は https://www.dvidshub.net/video/1007708 として記載され、files_catalog.csv の dvids_video_id（1007708）と一致する。WAR.GOV URL も出典セクションに記載あり。
P1-TECH PASS ffprobe値はドラフト記載の495.54秒（8分15秒）、1920×1080、24fps、H.264（High Profile）、AAC 48kHz ステレオ、約514 MB、映像ビットレート約8,194 kbps と整合する。BT.709（注釈あり）・エンコーダ情報も正確に記載されている。
P2-STRUCT PASS AI解析メモが出典セクション後（※免責の直前）の所定位置に配置されている。
P2-DRAFTNOTE PASS 「note転記後にこの行を削除」という制作メモ行は存在しない。
P2-KEYPOINT PASS 要点は番号付き太字で3項目に整理されており、各項目が映像観察・AARO説明・メタデータ由来の根拠とともに記述されている。
P2-WARNING PASS 冒頭に動画映像・視覚観察記事である旨の警告があり、確認事実・AARO説明文由来情報・メタデータ由来情報の3分類方針が明記されている。物体の正体・種別・行動意図を断定しない姿勢が明示されている。
P2-ABBR PASS DVIDS（国防映像情報配信サービス）、AARO（全領域異常解決局）、HUD（Heads-Up Display・視界内に重ねて表示されるセンサー情報画面）、BT.709（ITU-R BT.709・デジタルHD映像の標準色空間規格）、USO（Unidentified Submerged Object）、IR（赤外線）はいずれも初出時に日本語補足が付されている。DoW は文書メタデータで「Department of War（米国防省）」として展開されている。FHD は文書メタデータの「FHD MP4 495.5秒」の初出を「FHD（Full High Definition・1920×1080）」として展開済み。
P2-OBJECTIVITY PASS UFO論壇的表現・異星人等の断定表現はなく、「とみられる」「確認できます」「確認できません」「とされています」「推定される」等の留保表現が一貫して使用されている。「USO Formation」の名称はアップローダー定義のタイトルである旨が注意点セクションで明記されている。
M1-VISUAL PASS iter1 W-01 解消済み。frame_0060（01:00）のキャプション末尾に「※ 03:00時点（frame_0180）では4つの輝点がライン状に並んだ状態が最も明確に確認できる。」が追記されており、最重要フレームへの視覚的補助が確保されている。
M6-PROVENANCE-CAVEAT PASS chain-of-custody 未確立・デジタル改変済みの事実がAAROの情報として複数箇所（要点§3・AARO公式説明セクション・注意点セクション）に明記されている。
M8-AARO-DESC PASS iter1 W-02 解消済み。AARO 説明文は「## AARO 公式説明（war.gov より）」として ## 文書メタデータ の直後・フレームキャプションの前に独立セクションとして配置されており、AI読解とは明確に区別されている。
---ITEMS_END---
---CODEX_AUDIT_END---
