---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 2
UNVERIFIABLE: 0
PASS: 12
MODEL: gpt-5
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 PASS files_catalog.csv上のファイル名・Agency・Release Date・DVIDS ID・Locationと本文記述は整合する。
P1-2 PASS ffprobeおよびmetadata.jsonの動画仕様（289.27秒、4:49、1280x720、30fps、H.264、AAC、約207.65MB、6021kbps）は本文と整合する。
P1-3 PASS CENTCOM、AOR、DVIDSは初出付近で日本語補足されている。
P1-5 WARN source_registry.csv未登録のため、article_id・status・重複チェックの正式管理が未完了。
P2-1 WARN note転記後に削除すべき作業メモ行が本文内に残っている。
P2-2 PASS FMV/ISR等の未説明略語は本文主要部に出ておらず、専門語補足の不足は目立たない。
P2-3 PASS 物体の正体・種別・行動意図を断定せず、視覚観察とメタデータ由来情報を分離している。
P2-4 PASS 数値・単位は動画尺、解像度、fps、容量等が中心で、換算・精度に重大な問題はない。
P2-5 PASS 記事タイトルと本文内容は一致し、PR063以外の別ファイル番号混入は検出されない。
P2-6 PASS 日本語読者向けにCENTCOM/DVIDS/AORなどの注釈があり、本文理解を大きく妨げない。
IMG-1 PASS 視覚観察（シアンマーカー、黒塗り、クロスヘア状表示、地形）と解釈は分離されている。
IMG-2 PASS 「移動」「追跡」「消失」「分裂」「複数化」等を確定事実として断定していない。
SRC-1 PASS PR060/PR061/PR062との関連は「推定」として留保され、同日関連ファイルの記述もfiles_catalog.csvと整合する。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry管理 | ⚠️ **source_registry 未登録：** 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。公開前に source_registry への登録が必要です。 | 公開前管理事項として妥当だが、監査上はsource_registry.csv登録後にarticle_id・status・重複有無を確認する必要がある。
W-02: note投稿本文 | → 使用ファイル：thumbnails/DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2/frame_0030.png（note転記後にこの行を削除） | note本文には残さず、画像差し込み作業用メモとして削除する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---