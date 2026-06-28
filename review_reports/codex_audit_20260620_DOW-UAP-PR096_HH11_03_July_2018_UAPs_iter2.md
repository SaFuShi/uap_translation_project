---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 4
UNVERIFIABLE: 1
PASS: 9
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・複雑ネスト・Codex注釈ブロックは検出されない。
P1-1 WARN source_registry 未登録・article_id 未付番が本文末尾で明記されており、公開前メタデータ整備が未完了。
P1-2 PASS 2018年7月3日、2026年05月22日、約79.1秒、1280×720、30fps、音声ありは files_catalog および ffprobe 結果と整合。
P1-3 PASS CENTCOM、AOR、DVIDS は初出付近で日本語補足されている。
P1-5 UNVERIFIABLE source_registry 行が未登録のため、BLOCK状態・重複・article_id整合性は最終確認不能。
P2-1 WARN 標準構成のうち「注意点」「免責」に相当する独立セクションが不足。
P2-2 PASS Release 02動画記事として必要な主要略語補足は概ね充足。
P2-3 WARN センサー・映像由来の記述で「観測した」が使われており、チェックリスト上は「記録された」表現が望ましい。
P2-4 PASS 秒・解像度・フレームレート中心で、換算必須の高度・速度・距離単位は検出されない。
P2-5 PASS note投稿互換上の禁止フォーマットおよび編集メモ混入は検出されない。
P2-6 PASS 日本語読者向けの組織名・ファイル種別・DVIDS補足は最低限ある。
IMG-1 WARN 「グレースケールIR映像」という断定調の表現と「IRセンサー由来の可能性はあるが確認できない」が混在している。
IMG-2 PASS 移動・追跡・消失・分裂・複数化などの映像挙動を確定事実として断定していない。
IMG-3 PASS ヘリコプター、センサーアーティファクト、ズーム倍率などの根拠なき物体・機器解釈は検出されない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 登録後に article_id と台帳整合を確認する。
W-02: 記事構成 | AI読解の後に注意点・免責の独立セクションがない。 | 「注意点」「免責」を出典前後の所定位置に追加する。
W-03: この資料の要点 | 複数のUAP（「UAPs」と複数形）を観測した事案 | 映像・ファイル名由来の表現として「記録された事案」などに弱める。
W-04: 冒頭・要点・AI解析メモ | グレースケールIR映像 | 「グレースケール映像（IRの可能性があるが未確認）」など、視覚観察とセンサー解釈を分離する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---