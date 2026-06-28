---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 3
WARN: 4
UNVERIFIABLE: 0
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS note_drafts 禁止フォーマット（Markdown table、引用ブロック、長い英文引用、2階層以上ネスト、Codex注釈ブロック）は検出されない。
P1-1-FILENAME BLOCK source_registry.csv に DOW-UAP-PR057a_Spherical_UAP_in_clouds.mp4 の登録がなく、記事ファイル名と registry 登録名の整合性を満たしていない。
P1-1-SOURCEURL BLOCK WAR.GOV 出典が https://www.war.gov/UFO/ のトップページ表記で、対象メディアの直接URLになっていない。
P1-1-DATE PASS Release Date は 2026年05月22日 形式で統一され、files_catalog.csv の 2026-05-22 と整合する。
P1-1-INCIDENT PASS Incident Date は 2023年として files_catalog.csv と整合し、具体日付不明の留保もある。
P1-2-NUM PASS ffprobe由来の再生時間、解像度、fps、ビットレート、ファイルサイズ等は原文値として扱われ、換算値のみの独立記述はない。
P2-1-STRUCTURE PASS 構成はメタデータ、要点、AI読解、注意点、出典、免責に沿っている。
P2-1-SOURCES PASS 出典セクションに WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-2-ABBREV PASS INDOPACOM と DVIDS は初出付近で日本語補足されている。
P2-3-OBJECTIVITY WARN 「オレンジ色の追尾UIが全編で確認できる」は、本文では0〜45秒・5秒間隔の10フレーム確認に限定されており、確認範囲を超える表現。
IMG-1 WARN 「追尾UI」「追尾マーカー」「追尾ブラケット」など、画面表示の視覚観察と機器動作・追尾解釈の分離が一部弱い。
IMG-2 WARN PR057b について「同一事案の別角度記録の可能性」としているが、同一DVIDS ID以外の根拠が本文内で限定的。
P2-5-EDITORIAL WARN 「note転記後にこの行を削除」という編集指示が note_drafts 本文に残っている。
P3-REGISTRY BLOCK 本文末尾で source_registry 未登録と明記されており、article_id 付番・status・draft_path 等の registry 整合性チェックを通過できない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: この資料の要点 | オレンジ色の追尾UIが全編で確認できる | 「確認した0〜45秒の抽出フレームでは、オレンジ色のクロスヘア等の画面表示が確認できる」へ限定する。
W-02: 映像から視覚的に確認できる情報 | 追尾マーカー／追尾ブラケット／追尾ロックの状態変化 | 視覚観察は「クロスヘア状表示」「矩形コーナー表示」とし、追尾・ロックは「可能性」またはファイル名・UI解釈由来として分離する。
W-03: この資料の要点 | 同一事案の別角度記録の可能性がある | 「同一DVIDS IDを共有する関連ファイルだが、同一事案・別角度かは不明」に弱める。
W-04: 代表フレーム直前 | → 使用ファイル：...（note転記後にこの行を削除） | 公開用本文から編集指示を削除し、必要なら通常のキャプションだけ残す。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---