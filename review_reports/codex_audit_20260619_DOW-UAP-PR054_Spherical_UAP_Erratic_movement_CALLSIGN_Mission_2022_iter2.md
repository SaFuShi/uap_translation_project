---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 1
PASS: 9
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは確認されない
P1-1 BLOCK review_logs/source_registry.csv に DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022.mp4 の登録がなく、本文でも source_registry 未登録・article_id 未付番と明記されている
P1-2 PASS 動画長・解像度・fps等の数値表記は本文内で一貫しており、過度な換算問題は確認されない
P1-3 PASS EUCOM・AOR・DVIDS は初出付近で日本語補足されている
P1-4 PASS Misrep/MDR/JSIR/CSP/MRO 等の番号類は本文に登場しないため該当問題なし
P1-5 UNVERIFIABLE source_registry.csv 未登録のため article_id・公開状態・重複状態は確認不能
P2-1 WARN 記事タイトルが「#TBD」のままで、公開用記事番号が未確定
P2-2 PASS 主要略語は記事単独理解に必要な範囲で補足されている
P2-3 PASS 視覚観察・ファイル名由来情報・推測は概ね分離され、断定を避けている
P2-4 PASS フィート・ノット等の単位換算対象は本文に登場せず、問題なし
P2-5 WARN note転記作業用の「使用ファイル」削除指示行が本文内に残っている
P2-6 PASS 日本語読者向けの組織名・略語注釈は概ね十分
IMG-1 PASS 視覚観察と解釈は「確認できる」「可能性」「確認できない」で区別されている
IMG-2 WARN 「尾状の明るい領域」という見出し語が、物体の尾・航跡のように読める余地がある
---ITEMS_END---
---WARN_DETAILS_START---
W-01: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR054... | source_registry 登録後に確定 article_id を反映する
W-02: 代表フレーム挿入行 | → 使用ファイル：thumbnails/DOW-UAP-PR054_Spherical_UAP_Erratic_movement_CALLSIGN_Mission_2022/frame_0060.png（note転記後にこの行を削除） | 公開用本文から作業用行を削除する
W-03: 映像タイムライン | 03:00（白い球形物体・雲背景・尾状の明るい領域） | 03:00（白い球形物体・雲背景・右上方向の細長い明るい領域）など、形状観察に限定する
---WARN_DETAILS_END---
---CODEX_AUDIT_END---