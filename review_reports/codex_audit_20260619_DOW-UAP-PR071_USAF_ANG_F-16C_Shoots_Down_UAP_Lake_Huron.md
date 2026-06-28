---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 8
UNVERIFIABLE: 0
PASS: 9
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマットは検出されない。
P1-1 PASS metadata/files_catalog.csv のファイル名、公開日、Incident Date、Related Location、DVIDS ID と整合している。
P1-2 PASS ffprobeメタデータ、動画長、解像度、フレームレート、ファイルサイズ、音声トラックの記述はローカル実体と整合している。
P1-5 PASS 同一スラッグ・同一DVIDS IDの記事重複は検出されない。
P2-1 PASS 構成は「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」に概ね適合し、要点も3項目。
P2-1 WARN note転記用の作業メモが本文内に残存している。
P2-2 WARN DVIDS の日本語補足がなく、一般読者向けの略語説明として不足している。
P2-2 WARN USAF ANG の日本語補足はあるが、略語自体の展開がなく記事単独理解性が弱い。
P2-3 WARN 「追尾」「ロックオン」「IRセンサー映像」が確定調で反復され、視覚観察と機器動作解釈の分離がやや弱い。
P2-3 WARN 「センサー初期化またはレンズキャップ」「センサー終了またはキャップ」は映像から直接確認できない機器状態の推定として強い。
P2-5 PASS Markdown table、引用ブロック、長い英文引用、Codex注釈ブロック、複雑なネスト箇条書きは検出されない。
P2-6 WARN NORTHCOM は初出で補足されているが、後段の NORAD は日本語補足なしで出ている。
M4 PASS サムネイル出典と代表フレーム情報は記事内に記載されている。
M5 WARN DVIDS ID があるが、DVIDS URL（https://www.dvidshub.net/video/1007784）が出典欄に含まれていない。
M6 PASS ファイル名・メタデータ由来情報と映像フレーム由来情報は明示的に区分されている。
M6 PASS 音声トラックありとしつつ、音声内容は確認対象外であることを明記している。
P3 WARN review_logs/source_registry.csv に当該記事が未登録・article_id 未付番である。
OUT-1 BLOCK 読み取り専用サンドボックスにより、指定レポートファイルへの今回結果の保存は実行できなかった。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 画像差し込み行 | → 使用ファイル：thumbnails/DOW-UAP-PR071/frame_0020.png（note転記後にこの行を削除） | 公開本文から削除する。
W-02: 文書メタデータ・出典 | DVIDS ID：1007784 | DVIDS（国防映像情報配信サービス）ID：1007784 と初出補足する。
W-03: この資料の要点 | 米空軍州兵（USAF ANG）所属のF-16C戦闘機 | USAF ANG（U.S. Air Force Air National Guard：米空軍州兵）所属のF-16C戦闘機、と補足する。
W-04: この資料の要点・AI読解 | IRセンサー映像が確認できます／追尾中／ロックオンボックス | 赤外線センサー映像と推定されるグレースケール映像、クロスヘア状表示、矩形表示、のように視覚観察へ寄せる。
W-05: 映像から視覚的に確認できる情報 | センサー映像の初期化またはレンズキャップ状態と推定される／センサー終了またはキャップと推定 | 黒画面の理由は映像のみから確認できない、と弱める。
W-06: 外部背景情報 | 2023年02月12日に公表された北米防衛（NORAD/NORTHCOM）関連の事案 | NORAD（北米航空宇宙防衛司令部）を初出補足する。
W-07: 出典 | DVIDS ID：1007784（war.gov公開・Release 02） | DVIDS URL：https://www.dvidshub.net/video/1007784 を追記する。
W-08: source_registry | 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です | 公開前に review_logs/source_registry.csv 登録と article_id 付番を完了する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---