---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 6
UNVERIFIABLE: 0
PASS: 8
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長文英文引用、2階層以上ネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の対象行およびローカルMP4名と一致する。
P1-1-REGISTRY BLOCK review_logs/source_registry.csv に対象MP4 / DVIDS ID 1006111 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-1-RELEASE-DATE BLOCK ドラフトの Release Date は 2026年05月22日だが、metadata/files_catalog.csv / metadata/uap-csv-cache.csv の対象行は 5/8/26 であり、一次メタデータと不一致。
P1-1-LOCATION PASS Related Location は files_catalog.csv / uap-csv-cache.csv の North America と一致する。
P1-1-URL PASS 動画記事として WAR.GOV 公開ページ、DVIDS ID、DVIDS URL が併記され、DVIDS ID 1006111 と整合する。
P1-2-TECH PASS ffprobe実測上、109.2秒、1920×1080、30fps、H.264、AAC、映像ビットレート約1,161kbpsの本文記述は整合する。
P1-5-DUP WARN source_registry未登録のため、registryベースのstatus、SHA256重複、公開済み重複の正式確認が未完了。
P1-SOURCE WARN metadata/uap-csv-cache.csv の公式説明にある提出主体、AARO、IRセンサー、動画内時系列、注意書きが本文に十分反映されていない。
P2-1-STRUCT WARN 「注意点」見出しと出典後の免責セクションが標準構成上は不足している。
P2-1-POINTS PASS 要点は3項目の番号付き太字で記述されている。
P2-5-DRAFTNOTE WARN 「note転記後にこの行を削除」という作業メモが本文中に残っている。
P2-5-TITLE WARN タイトルに #TBD が残っており、公開用article_id確定前の状態である。
P2-3-OBJECTIVITY WARN 「飛行体状」「翼とみられる構造」は視覚的印象として留保はあるが、公式説明の「areas of contrast」より物体種別寄りの解釈が強い。
IMG-2 PASS 移動・消失・分裂などの動作を確定事実として断定していない。
IMG-4 PASS 画像のみの判断に「推定されるが確認できない」「とみられる」「正体は確認できない」等の留保がある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry重複管理 | 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前にregistry登録を完了し、status、draft_path、重複有無を確認する。
W-02: 公式説明反映 | IRまたは低照度カメラと推定されるが確認できない | 公式メタデータ由来として「赤外線センサー搭載の米軍プラットフォーム」と分けて記述する。
W-03: 公式説明反映 | 映像フレーム目視確認済み（4フレーム・30秒間隔） | 公式説明にある00:00-01:48の時系列説明を、視覚観察とは別に要約反映する。
W-04: 記事構成 | AI解析メモ後に出典が続き、出典後の免責見出しがない | 注意点、出典、免責の標準順に整理する。
W-05: note投稿前残存行 | → 使用ファイル：thumbnails/DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026/frame_0000.png（note転記後にこの行を削除） | 公開本文では作業メモを削除し、必要なら画像キャプションのみ残す。
W-06: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR049... | article_id確定後に #TBD を除去した公開用タイトルへ確定する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---