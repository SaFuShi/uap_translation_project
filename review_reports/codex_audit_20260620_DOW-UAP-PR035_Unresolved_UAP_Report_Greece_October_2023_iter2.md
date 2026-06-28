---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 3
WARN: 2
UNVERIFIABLE: 0
PASS: 13
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-SOURCE-REGISTRY BLOCK review_logs/source_registry.csv に対象MP4「DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October_2023.mp4」の登録が確認できず、本文末尾にも source_registry 未登録と明記されている。
P1-1-SOURCE-URL BLOCK 出典・メタデータの WAR.GOV URL がトップページ https://www.war.gov/UFO/ のみで、metadata/files_catalog.csv / metadata/uap-data.csv の対象直接URL https://www.war.gov/medialink/ufo/release_1/dow-uap-d35-mission-report-greece-october-2023.pdf が本文にない。
P1-1-RELEASE PASS Release Date 2026年05月08日は metadata/files_catalog.csv / metadata/uap-data.csv の 5/8/26 と一致する。
P1-1-INCIDENT PASS Incident Date は「2023年10月（ファイル名より）」として限定され、対象VID行の N/A およびタイトル情報と重大な矛盾はない。
P1-1-LOCATION PASS Related Location は Greece と記載され、metadata/files_catalog.csv の対象MP4行と一致する。
P1-1-DVIDS PASS DVIDS ID 1006082 と DVIDS URL https://www.dvidshub.net/video/1006082 は対象メタデータと一致する。
P1-2-VIDEO-META BLOCK 実MP4の ffprobe では video avg_frame_rate / r_frame_rate が 10/1 だが、ドラフトは「フレームレート：30fps」と記載しており技術メタデータが一致しない。
P1-3-DVIDS PASS DVIDS は初出で「国防映像情報配信サービス」と補足されている。
P2-1-STRUCTURE PASS 構成は概ね「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」に沿っている。
P2-2-ABBREV WARN 「IR」が初出で日本語補足されていない。
P2-3-OBJECTIVITY WARN 「空映像」「雲とみられる背景」の断定的表現は、metadata/uap-data.csv の公式説明「ocean background」「land」と整合しにくく、代表フレームのみからも断定が強い。
P2-4 PASS 換算を要する高度・速度・距離等の数値は本文にない。
P2-5 PASS note投稿互換上の禁止形式はなく、直訳臭・大量英文・生ログ貼付も見当たらない。
P2-6 PASS DVIDS、VID、H.264、AACなど主要な識別子・形式名には概ね必要範囲で補足がある。
VID-1 PASS 視覚観察とファイル名・メタデータ由来情報がセクション単位で分離されている。
VID-2 PASS 「移動」「追跡」「消失」「分裂」等を確定事実として断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 略語補足 | 「グレースケールの空映像（IRセンサーと推定されるが確認できない）」 | 「IR（赤外線）センサー」など初出で日本語補足する。
W-02: 視覚観察の断定 | 「グレースケールの空映像」「薄いグレーの空・雲とみられる背景」 | 一次メタデータの説明に合わせ、「水面または地表背景と説明されるグレースケール映像」など、空・雲断定を避ける。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---