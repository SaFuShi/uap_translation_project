---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 14
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長い英文引用、2階層以上のネスト箇条書き、Codex注釈ブロックは検出されない。
P1-1 PASS metadata/files_catalog.csv のファイル名、公開日、Incident Date、Related Location、DVIDS ID と整合している。
P1-2 PASS ffprobe値（MP4、H.264、1920x1080、30fps、46.77秒、835kbps、AAC音声、4.66MB、2ストリーム）はローカル動画実体および thumbnails メタデータと整合している。
P1-3 PASS NORTHCOM、NORAD、USAF ANG、DVIDS は初出付近で日本語補足されている。
P1-5 PASS 同一スラッグ、同一DVIDS ID、公開済み記事との明確な重複は検出されない。
P2-1 PASS 構成は「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」に概ね適合し、要点は3項目で記述されている。
P2-1 WARN note転記用の作業メモ行が本文内に残存している。
P2-3 WARN 「追尾」「ロックオンボックス」「IR映像」が確定調で反復され、視覚観察と機器動作解釈の分離がやや弱い。
P2-3 PASS 兵器使用、撃墜、物体の正体、2023年2月事案との対応関係は断定されず、ファイル名・メタデータ由来情報と映像フレーム由来情報が区別されている。
P2-4 PASS 換算対象となる速度・高度・距離・重量等の単位記述は本文に含まれていない。
P2-5 PASS OCRログ、生英文大量引用、直訳崩れ、表、引用ブロック、Codex注釈、複雑なネスト箇条書きは検出されない。
P2-6 PASS 日本語読者向けに主要略語・組織名・機材名の補足が付されている。
M1 PASS 動画内容について、撃墜・兵器使用・クロスヘア状態変化の機器的意味を確定事実として断定していない。
M4 PASS 代表フレーム、抽出時刻、サムネイル出典が記事内に記載されている。
M5 PASS war.gov URL と DVIDS URL が併記され、DVIDS URL の ID は files_catalog.csv の dvids_video_id と一致している。
M6 PASS 音声トラックありと記述しつつ、音声内容は確認対象外であることを明記している。
P3 WARN review_logs/source_registry.csv に当該記事が未登録・article_id 未付番である。
OUT-1 BLOCK 読み取り専用サンドボックスにより、指定レポートファイルへの今回結果の保存は実行できなかった。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 画像差し込み行 | → 使用ファイル：thumbnails/DOW-UAP-PR071/frame_0020.png（note転記後にこの行を削除） | 公開本文から削除する。
W-02: 映像記述全般 | 追尾クロスヘア／矩形ロックオンボックス／IR映像 | 「クロスヘア状表示」「矩形表示」「赤外線センサー映像と推定されるグレースケール映像」など、視覚観察と推定を明確に分ける。
W-03: source_registry | 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です | 公開前に review_logs/source_registry.csv 登録と article_id 付番を完了する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---