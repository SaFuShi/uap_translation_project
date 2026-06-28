---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 4
WARN: 3
UNVERIFIABLE: 0
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS note_drafts 禁止フォーマット（Markdown table、引用ブロック、長い英文引用、2階層以上ネスト、Codex注釈ブロック）は検出されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の DOW-UAP-PR057a_Spherical_UAP_in_clouds.mp4 と一致する。
P1-1-SOURCEURL BLOCK WAR.GOV 出典が https://www.war.gov/UFO/ のトップページ表記で、対象メディアの直接URL扱いになっていない。
P1-1-DATE PASS Release Date は 2026年05月22日、Incident Date は 2023年で metadata/files_catalog.csv と整合する。
P1-2-NUM PASS ffprobe由来の解像度、fps、再生時間、ビットレート、音声コーデック、ファイルサイズは実ファイル情報と概ね整合する。
P1-5-DUPLICATE BLOCK PR057a と PR057b は実ファイルMD5が同一で、metadata/uap-data.csv にも AARO Comment として duplicate と記録されている。
P2-1-STRUCTURE PASS 構成はメタデータ、要点、AI読解、注意点、出典、免責に沿っている。
P2-1-SOURCES PASS 出典セクションに WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-2-ABBREV WARN AOR が「担当AOR」として出るが、初出で略語展開または日本語説明が不足している。
P2-3-OBJECTIVITY WARN 「追尾マーカー」「追尾ブラケット」など、画面表示の視覚観察と機器動作・追尾解釈の分離が一部弱い。
IMG-1 PASS 物体の正体・種別、球形、黄海、2023年などは視覚確認情報とメタデータ由来情報に分離されている。
IMG-2 BLOCK PR057b との関係を「関連する記録の可能性」「直接的な対応関係は不明」としているが、AARO Comment は duplicate と明記しており、一次メタデータと整合しない。
P2-5-EDITORIAL WARN 「note転記後にこの行を削除」という編集指示が note_drafts 本文に残っている。
P3-REGISTRY BLOCK 本文末尾で source_registry 未登録・article_id 未付番と明記されており、公開前記事として registry 整合性チェックを通過できない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | 「Related Location：黄海（Yellow Sea）・INDOPACOM担当区域（files_catalog.csv より。INDOPACOM＝インド太平洋軍）」 | AOR を使う場合は「AOR＝担当区域」など短く補足する。
W-02: 映像説明全般 | 「追尾マーカー」「追尾ブラケット」「追尾ブラケットボックス」 | 視覚観察は「クロスヘア状表示」「矩形コーナー表示」とし、追尾解釈はAARO記述または推定として分離する。
W-03: 代表フレーム直前 | 「→ 使用ファイル：thumbnails/DOW-UAP-PR057_Spherical_UAP_in_clouds/frame_0035.png（note転記後にこの行を削除）」 | 公開用本文から編集指示を削除し、必要なら通常のキャプションだけ残す。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---