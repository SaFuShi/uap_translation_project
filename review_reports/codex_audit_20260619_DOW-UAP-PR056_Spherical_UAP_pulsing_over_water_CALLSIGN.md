---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 3
UNVERIFIABLE: 0
PASS: 11
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは確認されない
P1-1 PASS files_catalog.csv の対象行とファイル名・Agency・Release Date・Incident Date不明・AOR不明・DVIDS ID が整合している
P1-2 PASS FL・速度・高度・Zulu時刻などの数値換算矛盾は確認されない
P1-3 PASS MGRS・基地名・部隊名・機密区分など未補足問題の対象記述は確認されない
P1-4 PASS Misrep・MDR・JSIR・CSP/MRO等の番号類は本文に出ていない
P1-5 PASS 同一DVIDS IDまたは同一ファイル名の公開済み重複は確認されない
P2-1 PASS 構成はメタデータ→要点→AI読解→注意点→出典→免責に概ね沿い、要点も3項目
P2-2 PASS DVIDS は初出補足あり、その他の軍事略語未補足リスクは低い
P2-3 PASS 確認事実と推測・解釈は概ね分離され、物体正体の断定は避けられている
P2-4 PASS 日本向け換算が必要な英米単位の未換算問題は確認されない
P2-5 WARN note転記用の内部作業行が本文に残っている
P2-6 PASS 日本語読者向け注釈は過不足が大きくなく、過度な専門語放置は確認されない
P3-1 WARN source_registry.csv 未登録・article_id #TBD の状態が本文末尾に残っている
IMG-2 WARN タイトルで「移動する映像」と断定的に読める表現があり、画像記事追加チェックの「移動」確定表現リスクに該当
---ITEMS_END---
---WARN_DETAILS_START---
W-01: P2-5 note転記用内部行 | → 使用ファイル：thumbnails/DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN/frame_0000.png（note転記後にこの行を削除） | 公開本文から削除する、または通常の掲載画像出典文に置換する
W-02: P3-1 source_registry未登録 | ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。公開前に source_registry への登録が必要です。 | 登録完了後、article_idを反映し、この内部注記は公開本文から削除する
W-03: IMG-2 タイトル | # 【概要版#TBD】DoW DOW-UAP-PR056：球形UAPとされる物体が水面上で点滅・移動する映像（ファイル名より）──担当AOR不明・米国防省公開・Release 02 | 「球形UAPとされる物体が水面上で点滅しているとされる映像（ファイル名より）──映像内では位置変化の可能性あり」など、移動を確定しない表現にする
---WARN_DETAILS_END---
---CODEX_AUDIT_END---