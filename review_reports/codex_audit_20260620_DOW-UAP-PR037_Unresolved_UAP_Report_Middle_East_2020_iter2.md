---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 4
UNVERIFIABLE: 2
PASS: 7
MODEL: GPT-5 Codex
---ITEMS_START---
P0-FORMAT PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは確認されない。
P1-REG BLOCK review_logs/source_registry.csv に DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_2020.mp4 / DVIDS ID 1006087 の登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P1-CATALOG PASS metadata/files_catalog.csv の対象行と、ファイル名、Agency、Release Date、Related Location、File Type、DVIDS ID は一致する。
P1-URL PASS 動画記事として WAR.GOV 公開ページと DVIDS URL が併記され、DVIDS ID 1006087 と整合する。
P1-OFFICIAL-DESC WARN metadata/uap-csv-cache.csv にある公式説明文のうち、USCENTCOM提出、AARO宛、IRセンサー、米軍プラットフォーム、00:06-00:08のarea of contrast説明が本文に反映されていない。
P1-TECH PASS ffprobe値と本文の解像度、30fps、9.8秒、H.264、映像ビットレート6,866 kbps、AAC音声の記述は整合する。
P1-DUP UNVERIFIABLE source_registry 未登録のため、同一SHA256重複・公開済み記事との registry ベース重複確認は完了できない。
P2-STRUCT WARN 構成は概ね揃うが、チェックリスト上の「注意点」セクションが独立見出しとして存在しない。
P2-SOURCE PASS 出典に WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-TITLE WARN タイトルに #TBD が残っており、公開用 article_id 確定前の状態である。
P2-TERMS PASS DVIDS、AOR は初出付近で補足され、本文内の主要略語は概ね説明されている。
P2-OBJECTIVITY PASS 「とみられる」「確認できない」「断定しません」などの留保があり、確認事実と推定の区別は概ね保たれている。
P2-IMAGE WARN 代表フレームの船状物体やシアンUIの視覚記述は整合するが、公式説明にある00:06-00:08の対象描写が扱われず、2フレーム目視範囲に限定された記事であることが本文上やや弱い。
P3-REG UNVERIFIABLE source_registry 未登録のため、article_id 連番、status、note_url、published_date、draft_path の整合性は確認不能。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 公式説明 | 本文ではDVIDS IDのみ記載し、USCENTCOM提出・AARO宛・IRセンサー・米軍プラットフォーム・00:06-00:08のarea of contrast説明が未反映 | 公式説明由来情報として、確認できる範囲を留保付きで短く追加する。
W-02: 記事構成 | 注意点セクションなし | 出典前に短い「注意点」見出しを設け、視覚観察記事としての留保を集約する。
W-03: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR037... | article_id 確定後に #TBD を除去した公開用タイトルへ確定する。
W-04: 映像範囲 | 映像フレーム目視確認済み（2フレーム） | 00:06-00:08の公式動画説明が未検証なら、本文の観察範囲が抽出2フレーム中心であることを明確化する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---