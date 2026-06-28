---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 3
UNVERIFIABLE: 0
PASS: 11
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-REG PASS タイトルに「#R02-090」が明記されており、末尾にarticle_id（R02-090 / #2_090 / publish_order: 2090）が正式採番済みとして記録されている。source_registry.csv への登録は公開キュー投入時に実施予定と明記されており、外部登録待ちとして許容。
P1-META PASS ファイル名（DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission.mp4）、Release Date（2026年05月22日）、DVIDS ID（1007708）は metadata/files_catalog.csv と整合する。Related Location は files_catalog.csv 上も「未記録（空欄）」であり、本ドラフトの「不明」記述と整合する。
P1-DATE PASS Incident Date は files_catalog.csv・ファイル名双方に日時情報なしであり、本ドラフトが「不明」と記述していることと整合する。AARO説明文引用内の「2026年03月06日」（議会要請日）はゼロ埋め形式で記述されている。
P1-SOURCE PASS DVIDS URL は https://www.dvidshub.net/video/1007708 として記載され、files_catalog.csv の dvids_video_id（1007708）と一致する。WAR.GOV URL も出典セクションに記載あり。
P1-TECH PASS ffprobe値はドラフト記載の495.54秒（8分15秒）、1920×1080、24fps、H.264（High Profile）、AAC 48kHz ステレオ、約514 MB、映像ビットレート約8,194 kbps と整合する。BT.709・エンコーダ情報も正確に記載されている。
P2-STRUCT PASS AI解析メモが出典セクション後（※免責の直前）の所定位置に配置されている。
P2-DRAFTNOTE PASS 「note転記後にこの行を削除」という制作メモ行は存在しない。
P2-KEYPOINT PASS 要点は番号付き太字で3項目に整理されており、各項目が映像観察・AARO説明・メタデータ由来の根拠とともに記述されている。
P2-WARNING PASS 冒頭に動画映像・視覚観察記事である旨の警告があり、確認事実・AARO説明文由来情報・メタデータ由来情報の3分類方針が明記されている。物体の正体・種別・行動意図を断定しない姿勢が明示されている。
P2-ABBR PASS DVIDS（国防映像情報配信サービス）、AARO（全領域異常解決局）、HUD（Heads-Up Display・視界内に重ねて表示されるセンサー情報画面）、BT.709（ITU-R BT.709・デジタルHD映像の標準色空間規格）、USO（Unidentified Submerged Object）はいずれも初出時に日本語補足が付されている。DoW は文書メタデータで「Department of War（米国防省）」として展開されている。
P2-OBJECTIVITY PASS UFO論壇的表現・異星人等の断定表現はなく、「とみられる」「確認できます」「確認できません」「とされています」「推定される」等の留保表現が一貫して使用されている。「USO Formation」の名称はアップローダー定義のタイトルである旨が注意点セクションで明記されている。
M1-VISUAL WARN 代表フレームとして frame_0060（01:00）のみをキャプションに掲載しているが、4つの輝点編隊が最も明確に確認できる frame_0180（03:00）への言及が「この資料の要点 §2」本文のみで行われており、キャプションまたは別途の視覚補足が存在しない。読者が最重要フレームに辿り着くまでの補助が弱い。
M6-PROVENANCE-CAVEAT PASS chain-of-custody 未確立・デジタル改変済みの事実がAAROの情報として複数箇所（要点§3・注意点セクション）に明記されている。
M8-AARO-DESC WARN 本ドラフトは AARO 説明文（タイムコード付き）を「AARO 説明文」セクションとして AI読解内に展開しているが、ドラフトのセクション階層上、AARO 説明文は「## AI読解」の下に配置されており、AARO 説明文が「AIによる解析」と誤解される可能性がある。AARO 説明文は「## 文書メタデータ」と同列の独立セクション（例：「## AARO 公式説明」）として配置する方が適切。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 代表フレームキャプション | frame_0060（01:00）のみ掲載 | frame_0180（03:00）の「4輝点がライン状に並ぶ最明確フレーム」への視覚的補助を追加する。キャプション末尾に「※ 03:00時点に4輝点が最も明確（frame_0180参照）」等の一文を追記するか、本文参照誘導を強化する。
W-02: セクション配置 | AARO説明文が ## AI読解 の下位に配置 | AARO 説明文は一次資料（政府公式情報）であり、AIによる解析とは明確に異なる。「## AI読解」から独立した「## AARO 公式説明（war.gov より）」として ## 文書メタデータ と ## AI読解 の間に配置することを推奨。
W-03: IR略語 | 本文中「IR映像」「赤外線センサー」が混在 | 本文全体を通じてIR（Infrared・赤外線）の注釈はタイトル行に「赤外線映像（8分15秒）」と日本語訳が使われているが、「IR映像」とのみ記述されている箇所（AI解析メモ行等）で初出注釈を確認するか、全件「赤外線（IR）映像」に統一することを検討する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---
