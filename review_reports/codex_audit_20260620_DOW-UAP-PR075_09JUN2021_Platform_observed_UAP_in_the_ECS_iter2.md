---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 6
UNVERIFIABLE: 0
PASS: 7
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・複雑ネスト・Codex注釈ブロックは検出されない。
P1-1 WARN source_registry未登録のため article_id 付番・registry上のファイル名照合が公開前未完了。
P1-2 PASS 日付・動画時間・解像度・フレームレート等の数値はドラフト内で矛盾しない。
P1-3 PASS MGRS・基地名・部隊名・機密区分など該当する固有名詞補足不足は検出されない。
P1-4 PASS Misrep/MDR/JSIR/CSP/MRO等の番号類は本文に出現しない。
P1-5 WARN source_registry未登録のため registry上の重複・status確認が完了していない。
P2-1 WARN 所定構成のうち「注意点」「免責」の独立セクションがない。
P2-2 BLOCK platform を「機体・船舶等の観測機器搭載プラットフォーム」と具体化しており、ファイル名だけでは根拠不足。
P2-3 WARN センサー映像記事として「観測した」表現があり、「記録された」への抑制が必要。
P2-4 PASS ノット・フィート・マイル等の単位換算対象は検出されない。
P2-5 PASS note投稿互換上の禁止フォーマットおよびタイトルと本文内容の不一致は検出されない。
P2-6 PASS DVIDS・ECSなど主要略語には日本語補足がある。
IMG-1 WARN 視覚観察欄に「コンデンスト・トレールまたは光の軌跡」という物体解釈が混在している。
IMG-4 WARN 「IR映像」と断定的に書く箇所があり、IRセンサー未確認という留保と表現が競合する。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です」 | 公開前に source_registry 登録・article_id 付番後、registry照合を完了する。
W-02: Phase 1 重複・status確認 | 「source_registry 未登録」 | registry登録後に status・重複・既存公開記事との重複を確認する。
W-03: 記事構成 | 「AI読解」後に「出典」へ進み、独立した注意点・免責セクションがない | 「## 注意点」「## 免責」を独立見出しとして追加し、確認不能事項と非断定方針を整理する。
W-04: 表現の客観性 | 「UAPを観測した事案の映像とされています」 | 「UAPとして記録された事案の映像とされています」など、記録ベースの表現にする。
W-05: 画像記事 | 「白い長い線状物体（水平方向・コンデンスト・トレールまたは光の軌跡とみられるが確認できない）」 | 視覚観察は「白い長い線状物体」に留め、コンデンスト・トレール等は別の解釈欄に移す。
W-06: 映像説明 | 「グレースケールIR映像」 | 「グレースケール映像。IRセンサー由来の可能性はあるが確認できない」へ統一する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---