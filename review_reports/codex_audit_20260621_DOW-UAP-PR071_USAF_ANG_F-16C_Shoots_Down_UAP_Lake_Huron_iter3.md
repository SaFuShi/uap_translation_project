---CODEX_AUDIT_START---
VERDICT: PASS
BLOCK: 0
WARN: 1
UNVERIFIABLE: 0
PASS: 13
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-REG PASS タイトルに「#R02-062」が明記されており、末尾に article_id（R02-062 / #2_062 / publish_order: 2062）が正式採番済みとして記録されている。source_registry.csv への登録は公開キュー投入時に実施予定と明記されており、外部登録待ちとして許容。iter2 P3 WARN（source_registry未登録）は採番によって実質解消。
P1-META PASS ファイル名（DOW-UAP-PR071_USAF_ANG_F-16C_callsign_CALLSIGN_Shoots_Down_UAP_over_Lake_Huron_with_Weapon_System_12.mp4）、Release Date（2026年05月22日）、DVIDS ID（1007784）、Incident Date（2023年）、Related Location（NORTHCOM）は metadata/files_catalog.csv と整合する。DVIDS URL は文書メタデータセクション（https://www.dvidshub.net/video/1007784）および出典セクションの双方に記載されている。
P1-DATE PASS Incident Date は「2023年（files_catalog.csv より）」として明記されており、具体的日付が映像フレームから確認不可であることが注記されている。
P1-SOURCE PASS DVIDS URL（https://www.dvidshub.net/video/1007784）が文書メタデータに追加され、files_catalog.csv の dvids_video_id（1007784）と一致する。WAR.GOV URL も記載あり。
P1-TECH PASS ffprobe値（MP4、H.264、1920×1080、30fps、46.77秒、835 kbps、AAC、4.66 MB、2ストリーム）はドラフト記載と整合する。
P2-STRUCT PASS 構成は「メタデータ → 要点 → AI読解（映像メタデータ / タイムライン分析 / ファイル名情報 / 外部背景情報 / AI解析メモ）→ 注意点 → 出典 → 免責 → article_id フッター」で整合している。iter2 P2-1 PASS と同等の構成が維持されている。
P2-DRAFTNOTE PASS 作業メモ行「→ 使用ファイル：...（note転記後にこの行を削除）」は本文から除去されている。iter2 W-01 解消済み。
P2-KEYPOINT PASS 要点は番号付き太字で3項目に整理されており、各項目が映像観察またはファイル名・メタデータ由来の根拠とともに記述されている。F-16CによるUAP撃墜・追尾クロスヘアの状態変化・NORTHCOM/Lake Huron背景事案が適切に分離されている。
P2-WARNING PASS 冒頭に動画映像・視覚観察記事である旨の警告があり、確認事実とファイル名由来情報の分離方針が明記されている。撃墜・兵器使用・2023年2月事案との対応は断定されていない。
P2-ABBR PASS DVIDS（国防映像情報配信サービス）、NORTHCOM（米北方軍・北米防衛担当）、NORAD（北米航空宇宙防衛司令部）、USAF ANG（U.S. Air Force Air National Guard：米空軍州兵）はいずれも初出時に日本語補足または英語展開が付されている。
P2-OBJECTIVITY PASS UFO論壇的表現・異星人等の断定表現はなく、「とみられます」「確認できません」「可能性はありますが」「断定しません」等の留保表現が一貫して使用されている。
M1-VISUAL PASS frame_0020（00:20）を代表フレームとし、「追尾対象が最も明確に確認できるフレーム」として出典セクションに記載。thumbnails/DOW-UAP-PR071_USAF_ANG_F-16C_callsign_CALLSIGN_Shoots_Down_UAP_over_Lake_Huron_with_Weapon_System_12/ の長名ディレクトリを参照しており、ソースファイルの命名規則と整合する。
M6-PROVENANCE-CAVEAT WARN iter2 W-02（P2-3）継続：「追尾クロスヘア」「ロックオンボックス」「IR映像」が確定調で使用されている箇所がある。ただし要点・注意点セクションでは「と推定されるが確認できない」「映像のみから確認できない」等の留保が付されており、BLOCK 判定には至らない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像記述表現 | 「追尾クロスヘア」「ロックオンボックス」「IR映像」が確定調で使用される箇所がある | 公開前に「クロスヘア状表示」「矩形表示」「赤外線センサー映像と推定されるグレースケール映像」等の表現に統一することを推奨するが、注意点セクションで留保が明示されているため公開ブロックではない。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---
