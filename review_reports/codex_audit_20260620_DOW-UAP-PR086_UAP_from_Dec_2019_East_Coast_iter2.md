---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 8
UNVERIFIABLE: 0
PASS: 6
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長い英文引用・2階層以上ネスト・Codex注釈ブロックは確認されない。
P1-1 PASS ファイル名・DVIDS ID・Release Date・動画技術メタデータは files_catalog.csv、サムネイルmetadata、ffprobe結果と整合する。
P1-2 PASS Incident Date はファイル名由来の「Dec_2019」として明示され、本文内の年月と矛盾しない。
P1-3 PASS NORTHCOM・AOR・DVIDS など主要略語には日本語補足がある。
P2-1 WARN 標準構成のうち「注意点」「免責」セクションが明示されていない。
P2-3A WARN 「観測された」の表現が複数箇所にあり、記録映像記事の標準表現としては「記録された」が望ましい。
P2-3B WARN 「Release 02動画の中で最も視覚的に鮮明な映像の一つ」という比較評価の根拠が本文内で示されていない。
P2-3C WARN 「米国東海岸」とする箇所は、ファイル名の East Coast と NORTHCOM からの推定であることがやや弱い。
IMG-1 WARN 「カラー可視光映像（非IR）」が一部で断定的で、確認不能とする本文方針と揺れている。
IMG-2 WARN 「白い球体（オーブ）」が一部で形状・種別の断定に近く、画像記事の留保基準では弱い。
IMG-3 PASS 移動・追跡・消失・分裂などの動的挙動は確定事実として記述されていない。
P2-5 PASS OCRログ・生英文大量引用・直訳調の著しい破綻は確認されない。
P2-6 PASS 数値単位は動画尺・解像度・fps中心で、日本向け換算不足に該当する大きな距離・高度・速度はない。
P3-1 WARN source_registry.csv 未登録・article_id 未付番であり、公開前メタデータ整合性が未完了。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 記事構成 | 「## 注意点」「## 免責」に相当する独立セクションがない | 出典前に注意点、末尾に免責を明示する。
W-02: 客観表現 | 「2019年12月に米国東海岸で観測されたUAPの映像」 | 「2019年12月に東海岸で記録されたとされるUAP映像」などにする。
W-03: 比較評価 | 「Release 02のDOW-UAP映像の中で最も視覚的に鮮明な事案の一つ」 | 根拠を示すか、「視覚的に比較的確認しやすい映像」に弱める。
W-04: 地域推定 | 「米国東海岸での事案とみられます」 | 「NORTHCOM管轄の東海岸での事案とみられます」など、確認済み範囲に寄せる。
W-05: センサー種別 | 「カラー可視光映像（非IR）」 | 「カラー可視光映像とみられるが、センサー種別は確認できない」に統一する。
W-06: 形状断定 | 「白い球体（オーブ）が明確に確認できる」 | 「白い円形・点状の物体が確認できる。球体状に見えるが形状は断定できない」にする。
W-07: 画像記事の留保 | タイトル「白い球体（オーブ）UAP映像」 | 「白い球体状に見える物体」など留保を入れる。
W-08: source_registry | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施」 | 公開前に source_registry.csv 登録と article_id 付番を行う。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---