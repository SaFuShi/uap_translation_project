---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 0
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長文英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1-FILENAME BLOCK review_logs/source_registry.csv に対象MP4 DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December_2022.mp4 の登録がなく、同一DVIDS ID 1006062 では #039 のPDFのみ published 登録済み。
P1-1-METADATA PASS Release Date は 2026年05月08日形式で統一され、Incident Date はファイル名由来の2022年12月として限定表示されている。
P1-1-SOURCE WARN WAR.GOV はトップページURLのみで、war.gov側の対象メディア直接URLはPDF報告書URLとして metadata/files_catalog.csv に存在する。DVIDS直接URLは併記されている。
P1-2 PASS FL、速度、高度、Zulu時刻などの換算・時刻整合チェック対象となる数値記述は本文にない。
P1-3 PASS DVIDS は初出で「国防映像情報配信サービス」と補足され、未説明の軍事略語の過剰使用は限定的。
P1-5-DUP WARN 同一DVIDS ID 1006062 のPDF記事 #039 が既に published であり、動画記事としての独立登録・既存PDF記事との関係整理が必要。
P2-1-STRUCTURE WARN 標準構成の「注意点」「免責」セクションが独立見出しとして存在せず、末尾注記と冒頭警告に分散している。
P2-1-POINTS PASS 要点は番号付き太字で3項目。
P2-1-SOURCES PASS 出典セクションにWAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-2 PASS AOR、DVIDS など主要略語は初出付近で補足されている。
P2-3 PASS 視覚確認情報、ファイル名・メタデータ由来情報、推定・未確認事項が概ね分離され、物体種別や行動意図を断定していない。
P2-5-TITLE WARN タイトルが「#TBD」のままで、source_registry 未登録・article_id 未付番状態が本文末尾にも残っている。
P2-IMAGE PASS 画像・映像記事として、IRセンサーは「推定されるが確認できない」、車両は「みられる」、UAP対象物は「確認困難」と留保されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 出典URL | WAR.GOV：https://www.war.gov/UFO/ | 対象メディアまたは関連報告書の直接URLを一次出典として明示し、トップページURLは公開コレクション案内として分ける。
W-02: source_registry関係 | DVIDS ID：1006062（war.gov公開・Release 02） | 既公開PDF #039 と対象MP4記事の関係をregistry側で整理し、動画記事として独立登録する。
W-03: 記事構成 | 出典後に source_registry 未登録注記のみがあり、独立した注意点・免責セクションがない。 | 「注意点」「免責」を標準順序に沿って独立見出し化し、映像判断の限界を整理する。
W-04: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR023：イラク2022年12月UAPとされる事案映像（ファイル名より）──Iraq・米国防省公開・Release 02 | source_registry 登録後に確定 article_id を反映する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---