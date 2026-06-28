---CODEX_AUDIT_START---
VERDICT: PASS
BLOCK: 0
WARN: 0
UNVERIFIABLE: 0
PASS: 14
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-REG PASS タイトルに「#R02-091」が明記されており、末尾にarticle_id（R02-091 / #2_091 / publish_order: 2091）が正式採番済みとして記録されている。source_registry.csv への登録は公開キュー投入時に実施予定と明記されており、外部登録待ちとして許容。
P1-META PASS ファイル名、Release Date（2026年05月22日）、DVIDS ID（1007783）、Related Location（Southeastern United States）は metadata/files_catalog.csv および metadata/uap-csv-cache.csv と整合する。
P1-DATE PASS Incident Date は DVIDSタイトル由来の「2023年2月13日」（ファイル名「on_13_」・uap-csv-cache.csv「13 Feb 23」）として本文に反映されており、ファイル名・メタデータ由来である旨が明記されている。
P1-SOURCE PASS DVIDS URL は https://www.dvidshub.net/video/1007783 として記載され、files_catalog.csv の dvids_video_id（1007783）と一致する。WAR.GOV URL も出典セクションに記載あり。
P1-TECH PASS ffprobe値はドラフト記載の30.1秒、1920×1080、30fps、H.264、AAC、約35MB、約9,980kbpsと整合する。ストリーム数（映像1・音声1）も明記されている。
P2-STRUCT PASS AI解析メモが出典セクション後（※免責の直前）の所定位置に配置されている。iter2 WARN W-01 解消済み。
P2-DRAFTNOTE PASS 「note転記後にこの行を削除」という制作メモ行は本文から除去されている。iter2 WARN W-02 解消済み。
P2-KEYPOINT PASS 要点は番号付き太字で3項目に整理されており、各項目が映像観察またはメタデータ由来の根拠とともに記述されている。
P2-WARNING PASS 冒頭に動画映像・視覚観察記事である旨の警告があり、確認事実とメタデータ由来情報の分離方針が明記されている。物体の正体・種別・行動意図を断定しない姿勢が明示されている。
P2-ABBR PASS DVIDS（国防映像情報配信サービス）、IIR（Imaging Infrared）、AFB（空軍基地）は本文中で日本語補足または英語展開が付されている。NORTHCOM（United States Northern Command）も注意点セクションで英語正式名が記載されている。
P2-OBJECTIVITY PASS UFO論壇的表現や異星人等の断定表現はなく、「とされている」「可能性があります」「確認できません」等の留保表現が一貫して使用されている。
M1-VISUAL PASS 視覚観察とファイル名・メタデータ由来情報が見出しで分離されており（「映像から視覚的に確認できる情報」vs「ファイル名・メタデータ由来の情報」）、画像キャプションにも「推定されるが確認できない」留保が付されている。
M6-PROVENANCE-CAVEAT PASS 注意点セクションに「AOR（作戦責任区域）について」（NORTHCOM・Eglin AFBはフロリダ州・NORTHCOM管轄）および「chain-of-custody（証拠連鎖）について」（分類ネットワークへのアップロード経路不明・AARO説明文は分析判断を示すものではない）が明記されている。iter2 WARN W-03 解消済み。
---ITEMS_END---
---CODEX_AUDIT_END---
