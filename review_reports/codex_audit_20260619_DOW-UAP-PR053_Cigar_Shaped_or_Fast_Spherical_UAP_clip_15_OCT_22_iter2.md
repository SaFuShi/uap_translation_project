---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 5
UNVERIFIABLE: 0
PASS: 9
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS note投稿禁止フォーマットは検出されない。
P1-1 PASS metadata/files_catalog.csv のファイル名、公開日、Related Location、DVIDS ID と整合している。
P1-2 PASS ffprobeメタデータ、動画長、解像度、フレームレート、ファイルサイズの記述は整合している。
P1-3 PASS CENTCOM は初出で日本語補足されている。
P1-5 PASS 同一内容の重複動画は検出されない。
P2-1 PASS 構成は「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」に概ね適合し、要点も3項目。
P2-1 WARN note転記用の作業メモが本文内に残存している。
P2-3 WARN 「追尾」「追尾対象」が機器動作・対象同一性の断定寄りに読める。
M1 WARN 高速移動について、抽出フレーム確認と全編視聴確認の範囲が混在して読める。
P2-5 PASS Markdown table、引用ブロック、長い英文引用、Codex注釈ブロック、複雑なネスト箇条書きは検出されない。
M4 PASS サムネイル出典と代表フレーム情報は記事内に記載され、キャプションにセンセーショナルな断定はない。
M5 PASS war.gov URL と DVIDS URL が併記され、DVIDS ID は files_catalog.csv と一致している。
P3 WARN source_registry.csv 未登録・article_id 未付番である。
M7 WARN DVIDS の日本語補足がなく、一般読者向けの略語説明として不足している。
OUT-1 BLOCK 読み取り専用サンドボックスにより、指定レポートファイルへの今回結果の保存は実行できなかった。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 画像差し込み行 | → 使用ファイル：thumbnails/DOW-UAP-PR053/frame_0005.png（note転記後にこの行を削除） | 公開本文から削除する。
W-02: 映像から視覚的に確認できる情報 | 画面中央にセンサー追尾クロスヘア（十字線）が確認できる。追尾対象を画面中央付近に維持している | 画面中央付近にクロスヘア状の表示が確認でき、明るい領域がその周辺に映っている、に弱める。
W-03: 注意点 | この点については、映像を通して視聴することで確認できます | 抽出フレームでは確認できないため、全編視聴で確認する必要があります、に修正する。
W-04: source_registry | source_registry.csv への登録・article_id の付番が未実施です | 公開前に source_registry.csv 登録と article_id 付番を完了する。
W-05: 文書メタデータ・出典 | DVIDS ID：1007709 | DVIDS（国防映像情報配信サービス）ID：1007709 と初出補足する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---