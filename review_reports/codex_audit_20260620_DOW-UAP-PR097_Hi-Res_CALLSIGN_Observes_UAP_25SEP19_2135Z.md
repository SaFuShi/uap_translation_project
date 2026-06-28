---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 6
UNVERIFIABLE: 0
PASS: 8
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマット（Markdown table、引用ブロック、長文英文引用、複雑ネスト、Codex注釈ブロック）は検出なし。
P1-1 WARN source_registry.csv に対象PR097の登録がなく、article_id・登録上の一次資料整合性が未確定。
P1-2 PASS 再生時間299.4秒、1280×720、H.264、30fps、音声ありはローカルffprobeおよびサムネイルmetadataと整合。
P1-3 PASS DVIDS、CENTCOM、AORなど主要略語には最低限の日本語補足あり。
P1-5 PASS PR097と関連PR099はMD5が異なる別ファイルであることを確認。
P2-1 WARN 標準構成のうち「注意点」「免責」に相当する独立セクションが欠落。
P2-2 PASS Release 02動画記事として必要な主要略語補足は概ね充足。
P2-3 WARN 「観測映像」「観測した」とする表現があり、チェックリスト上は映像資料では「記録された」表現が望ましい。
P2-4 PASS 日本向け換算が必要な速度・高度・距離等の数値単位は本文に出ていない。
P2-5 WARN note転記作業用の内部行が本文に残っている。
P2-6 PASS 一般読者向けの組織名・資料種別・DVIDSの補足は概ね足りている。
IMG-1 WARN 「グレースケールIR映像」という断定調の箇所があり、視覚観察とセンサー種別推定の分離が不十分。
IMG-2 WARN PR099との関係を「同一事案の異なる時間帯のクリップ」としているが、本文内根拠は同日・類似ファイル名・時刻差にとどまる。
IMG-3 PASS ヘリコプター、センサーアーティファクト、ズーム倍率などの根拠なき物体・機器解釈は検出されない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 登録後に article_id・status・draft_path と照合できる形にする。
W-02: 記事構成 | 注意点・免責に相当する独立セクションがない。 | 出典前後に「注意点」「免責」を独立見出しで追加する。
W-03: タイトル・本文 | UAP観測映像 / CALLSIGNによるHi-Res（高解像度）UAP観測映像 | 「UAPが記録された映像」「CALLSIGN関連ファイルに記録された映像」などに弱める。
W-04: note投稿互換 | → 使用ファイル：thumbnails/...（note転記後にこの行を削除） | 公開本文から作業用行を削除する。
W-05: 画像記事 | グレースケールIR映像 | 「グレースケール映像（IRセンサー由来の可能性はあるが、このフレームだけでは確認できない）」にする。
W-06: 関連ファイル | 同一事案の異なる時間帯のクリップとみられます | 「同日・類似ファイル名・時刻違いの関連クリップとみられます」に弱める。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---