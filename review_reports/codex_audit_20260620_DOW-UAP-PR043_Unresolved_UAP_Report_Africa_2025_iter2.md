---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 2
UNVERIFIABLE: 0
PASS: 14
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 PASS File Name、Release Date、Incident Date、Related Location、DVIDS ID は metadata/files_catalog.csv と概ね整合する。
P1-1 WARN files_catalog.csv の Djibouti を「担当AOR」と表現しており、関連地点と担当作戦地域の区別が曖昧。
P1-2 PASS 動画長・解像度・ファイルサイズ・音声・DVIDS ID はローカルMP4/サムネイルメタデータと概ね整合する。
P1-3 PASS DVIDS と AOR は本文内で補足されている。
P1-5 WARN source_registry.csv に対象MP4の登録がなく、article_id も #TBD のまま。
P2-1 PASS 構成はメタデータ、要点、AI読解、注意点、出典、免責の流れで成立している。
P2-2 PASS 本文で使われる主要略語・専門語は限定的で、読解上の致命的な未補足はない。
P2-3 PASS 視覚事実と推測は概ね分離され、物体正体・種別・行動意図の断定は避けられている。
P2-4 PASS 換算が必要な高度・速度・距離などの単位値は本文中にない。
P2-5 PASS 生ログ大量貼付・直訳臭の多発・note非互換形式は確認されない。
P2-6 PASS 日本語読者向けの構成・注意書きは概ね成立している。
IMG-1 PASS 視覚観察と解釈は「確認できる」「みられるが確認できない」で概ね分離されている。
IMG-2 PASS 移動・追跡・消失・分裂などの動作を確定事実として記述していない。
IMG-3 PASS 航空機窓枠・IRセンサー等の解釈には留保が付いている。
IMG-4 PASS 画像のみの判断に「推定」「みられる」「確認できない」等の留保がある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: この資料の要点 | アフリカ（担当AOR（Area of Responsibility：担当作戦地域）はジブチ） | 「アフリカ（関連地点：ジブチ）」など、files_catalog由来の地点情報として記述する。
W-02: source_registry 未登録 | 本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | 公開前メタデータとして source_registry 登録後に article_id と登録情報を反映する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---