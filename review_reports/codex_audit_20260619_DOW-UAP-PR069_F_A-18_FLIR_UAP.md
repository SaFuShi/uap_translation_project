---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 5
UNVERIFIABLE: 1
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 BLOCK review_logs/source_registry.csv に対象ファイルの登録がなく、記事タイトルも「#TBD」のため article_id 未付番状態。公開前の provenance 要件を満たさない。
P1-1-META PASS metadata/files_catalog.csv 上の対象行と、ドラフトのファイル名・Release Date・Incident Date・NORTHCOM・DVIDS ID は整合している。
P1-2 PASS ffprobeメタデータ、動画長、解像度、フレームレート、ビットレート、ファイルサイズ、音声トラックの記述はローカル実体と整合している。
P1-5 UNVERIFIABLE source_registry 未登録のため、registry status・SHA256重複・公開済み記事重複の確認が完了できない。
P2-1 WARN 代表フレーム差し込み用の作業メモ「note転記後にこの行を削除」が本文内に残存している。
P2-1-STRUCT PASS 「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」の主要構成と、3項目の要点は満たしている。
P2-2 WARN AOR が「担当AOR」として略語のまま出ており、初出補足が弱い。
P2-2-DVIDS PASS DVIDS は「国防映像情報配信サービス」として補足されている。
P2-3 PASS 宇宙人・異星人等の論壇的表現はなく、対象物の正体や行動意図は断定していない。
P2-5 PASS OCRログ・生英文大量貼付・直訳臭の強い定型表現は検出されない。
P2-6 PASS F/A-18、FLIR、NORTHCOM には概ね日本語注釈が付いている。
IMG-1 WARN 「典型的なFLIRシステムUI」「特有の表示形式」は、映像フレーム視認だけでは根拠が強すぎる。
IMG-2 WARN frame_0025 の「映像有効領域が中央付近の矩形に収縮」「FOV枠が小さな領域に収縮」は、代表フレーム上の見え方と整合しにくい。
IMG-3 WARN 「対象は視野外」とする記述は、対象同一性自体が未確認であるため断定が強い。
IMG-4 PASS ファイル名・メタデータ由来情報と映像フレーム由来情報は明示的に区分されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 代表フレーム行 | 「→ 使用ファイル：thumbnails/DOW-UAP-PR069_F_A-18_FLIR_UAP/frame_0000.png（note転記後にこの行を削除）」 | 公開本文から作業メモ行を削除する。
W-02: 文書メタデータ | 「NORTHCOM担当区域（files_catalog.csv より。NORTHCOM＝U.S. Northern Command：米北方軍。北米大陸を担当AORとする米軍統合戦闘コマンド）」 | 「AOR（Area of Responsibility：担当区域）」のように初出補足する。
W-03: 要点・注意点 | 「典型的なFLIRシステムのUI」「F/A-18のFLIRシステム（ATFLIR等）に特有の表示形式」 | 「FLIR映像で見られる形式と整合する表示」など、外部背景情報として留保を付ける。
W-04: frame_0025記述 | 「映像有効領域が中央付近の矩形に収縮した状態」「FOV枠が画面中央付近の小さな領域に収縮」 | 「画面表示や背景の見え方が変化し、中央付近のUI表示と黒塗り矩形が確認できる」など視覚事実に寄せる。
W-05: 要点3 | 「対象は視野外または確認困難」 | 「画面上部の明るい点はこのフレームでは確認困難」など、対象同一性を断定しない表現にする。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---