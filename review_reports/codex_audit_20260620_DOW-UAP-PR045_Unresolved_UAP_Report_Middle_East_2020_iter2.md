---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 5
UNVERIFIABLE: 0
PASS: 9
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、長文英文引用、2階層以上ネスト箇条書き、Codex注釈ブロックは確認されない。
P1-1-FILENAME PASS File Name は metadata/files_catalog.csv の対象行と一致する。
P1-1-REGISTRY BLOCK 本文末尾に source_registry 未登録・article_id 未付番と明記されており、公開前管理要件を満たしていない。
P1-1-RELEASE-DATE PASS Release Date 2026年05月08日は metadata/files_catalog.csv / metadata/uap-csv-cache.csv の 5/8/26 と一致する。
P1-1-LOCATION PASS Related Location は Southern United States として metadata/files_catalog.csv / metadata/uap-csv-cache.csv と一致し、ファイル名 Middle East との不一致も明示されている。
P1-1-URL PASS 動画記事として WAR.GOV 公開ページ、DVIDS ID、DVIDS URL が併記され、DVIDS ID 1006105 と整合する。
P1-2-TECH WARN ローカル監査時に対象MP4が確認できず、ffprobe由来の詳細値と代表フレーム記述を再現検証できない。
P1-SOURCE WARN metadata/uap-csv-cache.csv の公式説明にある提出主体、AARO、IRセンサー、動画内時系列、AAROコメントが本文に十分反映されていない。
P2-1-STRUCT WARN AI解析メモが注意点・出典より前にあり、標準構成の「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」から外れている。
P2-1-POINTS PASS 要点は3項目の番号付き太字で記述されている。
P2-2-ABBREV WARN 公式説明を本文へ反映する場合、AARO は初出で「全領域異常解決局／米国防総省のUAP調査組織」と補足する必要がある。
P2-3-OBJECTIVITY PASS 「確認できない」「断定しません」「とみられる」等の留保があり、視覚観察と推定の分離は概ね保たれている。
P2-5-FORMAT PASS note投稿互換上の禁止フォーマットは確認されない。
P2-5-TITLE WARN タイトルに #TBD が残っており、公開用article_id確定前の状態である。
P2-IMAGE PASS 視覚観察と解釈の区分は概ね維持され、物体種別・行動意図の断定は避けられている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 技術・画像検証 | 映像メタデータ（ffprobe解析より）／代表フレーム記述 | 対象MP4または検証済み代表フレームの所在を監査可能にし、ffprobe値・視覚記述を再確認する。
W-02: 公式説明反映 | グレースケールの映像（IRセンサーと推定されるが確認できない） | 公式メタデータ由来として、IRセンサー、提出主体、口頭・文書説明なし、時系列、AAROコメントを別枠で反映する。
W-03: 記事構成 | AI解析メモが注意点・出典より前にある | AI解析メモ、注意点、出典、免責の配置を標準順に整理する。
W-04: 略語補足 | AARO | 本文でAAROを扱う場合は「AARO（全領域異常解決局／米国防総省のUAP調査組織）」と初出補足する。
W-05: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR045... | article_id確定後に #TBD を除去した公開用タイトルへ確定する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---