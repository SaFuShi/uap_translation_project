---CODEX_AUDIT_START---
VERDICT: PASS
BLOCK: 0
WARN: 1
UNVERIFIABLE: 0
PASS: 13
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-REG PASS タイトルに「#R02-058」が明記されており、末尾に article_id（R02-058 / #2_058 / publish_order: 2058）が正式採番済みとして記録されている。source_registry.csv への登録は公開キュー投入時に実施予定と明記されており、外部登録待ちとして許容。iter2 P1-5 BLOCK 解消済み。
P1-META PASS ファイル名（DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024.mp4）、Release Date（2026年05月22日）、DVIDS ID（1007778）、Related Location（Southeastern United States）は metadata/files_catalog.csv と整合する。関連ファイル PR065（UAP_2・DVIDS 1007777）への言及あり。
P1-DATE PASS Incident Date は「2024年4月24日」としてファイル名由来と明記されており、files_catalog.csv の「2024」と整合する。
P1-SOURCE PASS DVIDS URL は https://www.dvidshub.net/video/1007778 として記載され、files_catalog.csv の dvids_video_id（1007778）と一致する。WAR.GOV URL も出典セクションに記載あり。
P1-TECH PASS ffprobe値はドラフト記載の48.6秒、1920×1080（FHD）、30fps、H.264、AAC、約33 MB、5,840 kbps と整合する。ストリーム数（映像1・音声1）も明記されている。
P2-STRUCT PASS AI解析メモが出典セクション後（※免責の直前）の所定位置に配置されている。
P2-DRAFTNOTE PASS 「note転記後にこの行を削除」という制作メモ行は本文から除去されている。iter2 P2-1 BLOCK 解消済み。
P2-KEYPOINT PASS 要点は番号付き太字で3項目に整理されており、各項目が映像観察またはファイル名・メタデータ由来の根拠とともに記述されている。
P2-WARNING PASS 冒頭に動画映像・視覚観察記事である旨の警告があり、確認事実とメタデータ由来情報の分離方針が明記されている。物体の正体・種別・行動意図を断定しない姿勢が明示されている。
P2-ABBR PASS DVIDS（国防映像情報配信サービス）、USCG（米沿岸警備隊）、FHD（1920×1080）、HUD、AOR（担当作戦地域）、IR はいずれも初出時に日本語補足または英語展開が付されている。
P2-OBJECTIVITY PASS UFO論壇的表現・異星人等の断定表現はなく、「とされる」「と推定されるが確認できない」「一致するかどうかは…断定しません」等の留保表現が一貫して使用されている。「TIC TAC」という名称はファイル名由来である旨が明記されており、視覚的形状との不一致についての留保も注意点セクションに明記されている。
M1-VISUAL PASS frame_0000（00:00）を代表フレームとし、地平線付近の物体が最も明確に確認できるフレームとしてキャプションおよび要点§2 で説明されている。frame_0015・frame_0030・frame_0045 の変化についても記述あり。
M6-PROVENANCE-CAVEAT PASS 映像はRelease 02の政府公開資料（war.gov/UFO/）として明記されており、chain-of-custody に関する断定は行われていない。ファイル名由来情報は「ファイル名より」として出典が区別されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: IR hot 表現 | P2-3 WARN（iter2 継続） | 「IR hot（赤外線で熱源として確認）」はファイル名由来の評価であり、物理的熱源を確認したと断定する読み方を誘発する可能性がある。ただし直後に「ファイル名より」と出典が明示されており、公開前の修正は任意（BLOCK ではない）。修正案：「IR hot（ファイル名記述。赤外線映像での高温物体識別を示す可能性があるが、映像フレームからは直接確認できない）」
---WARN_DETAILS_END---
---CODEX_AUDIT_END---
