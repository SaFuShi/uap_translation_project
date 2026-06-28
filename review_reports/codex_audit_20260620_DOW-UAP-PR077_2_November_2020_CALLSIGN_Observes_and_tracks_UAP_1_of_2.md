---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 4
UNVERIFIABLE: 0
PASS: 10
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・複雑ネスト・Codex注釈ブロックは検出されない。
P1-1 WARN source_registry未登録・article_id未付番が本文末尾に明記されており、公開前メタデータ整合性が未完了。
P1-2 PASS 日付・時間・動画時間・解像度・フレームレート等の数値記述に重大な矛盾はない。
P1-3 WARN CENTCOMの初出補足が標準表記「米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍」まで満たしていない。
P1-4 PASS Misrep/MDR/JSIR/CSP/MRO等の番号類は本文に出現しない。
P1-5 PASS ローカル確認範囲では対象動画ファイル・サムネイル・PR078関連ファイルの存在は確認できる。
P2-1 WARN 構成に「注意点」「免責」セクションが明示されていない。
P2-2 WARN 「2機（またはプラットフォーム）のCALLSIGN」としており、CALLSIGN_CALLSIGNから2機と読む解釈がやや具体化されている。
P2-3 PASS 物体の正体・種別・行動意図は断定しておらず、視覚確認情報とメタデータ由来情報の区別は概ね維持されている。
P2-4 PASS 換算を要する速度・高度・距離・重量などの単位は本文に出現しない。
P2-5 PASS note投稿互換を損なう表・引用ブロック・生ログ貼付はない。
P2-6 PASS 日本語読者向けにDVIDS・AOR等の一部補足はあり、過度に長い注釈反復もない。
P3-1 PASS source_registry.csv自体の既存連番・公開済みURL等を本記事が破壊する記述はない。
IMG-1 PASS 視覚観察は「確認できる」「みられる」「推定されるが確認できない」等の留保付きで記述されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | ⚠️ source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。 | source_registry登録・article_id付番後に本文へ反映し、公開用本文から管理メモを削除する。
W-02: 記事構成 | 構成が「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」の順か | 「注意点」と「免責」を明示セクションとして追加する。
W-03: 文書メタデータ | Related Location：CENTCOM（中央軍・AOR：担当作戦地域：中東・中央アジア） | CENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）など標準補足に寄せる。
W-04: この資料の要点 | 2020年11月2日に2機（またはプラットフォーム）のCALLSIGNがUAPを観測・追跡 | 「ファイル名上はCALLSIGN_CALLSIGNと記録された米軍側の機材・システムがUAPを観測・追跡した映像」とし、2機断定を避ける。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---