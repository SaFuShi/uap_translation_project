---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 2
WARN: 2
UNVERIFIABLE: 0
PASS: 10
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1 PASS ファイル名、Release Date、Incident Date、Location、DVIDS ID は files_catalog.csv および抽出メタデータと矛盾しない。
P1-2 PASS 再生時間、解像度、ビットレート、音声有無、フレーム抽出数は thumbnails 配下 metadata.json と整合する。
P1-3 PASS USCG、C-144、DVIDS、AOR、AFB は初出または近接箇所で日本語補足されている。
P1-5 BLOCK source_registry.csv に当該ファイルの登録が確認できず、本文末尾にも source_registry 未登録・article_id 未付番と明記されている。
P2-1 PASS 構成はメタデータ、要点、AI読解、注意点、出典、免責の順で、要点も3項目で記述されている。
P2-1 BLOCK note転記用の内部作業行「→ 使用ファイル：...（note転記後にこの行を削除）」が本文内に残っている。
P2-2 PASS 記事単独理解に必要な主要略語・組織名・機材名の補足は概ね足りている。
P2-3 WARN 「IR hot（赤外線で熱源として確認）」はファイル名由来の評価を物理的熱源確認のように読ませる可能性がある。
P2-3 PASS 視覚観察とファイル名・メタデータ由来情報は別セクションで分離され、物体の正体・種別・行動意図は断定していない。
P2-3 PASS 「移動」「追尾」「視野外」等は留保付きで、映像フレームのみから確認できない範囲を明示している。
P2-5 WARN タイトルの「【概要版#TBD】」は article_id 未付番状態を示しており、公開用タイトルとしては未確定要素が残る。
P2-6 PASS 日本語読者向けに HC-144 Ocean Sentry、DVIDS、Tyndall AFB、AOR などの補足が入っている。
IMG-1 PASS 画像・動画記事として、視覚観察と形状評価の留保があり、機器動作や対象同一性を過度に断定していない。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: ファイル名・メタデータ由来の情報 | センサー評価：IR hot（赤外線で熱源として確認）（ファイル名より） | センサー評価：IR hot（赤外線上で高温表示とされる、というファイル名由来の情報。実際の熱源性は本文では断定しない）
W-02: タイトル | # 【概要版#TBD】DoW DOW-UAP-PR066：USCG C-144からの「TIC TAC IR hot」とされる映像・クリップ1（ファイル名より）──南東部米国・2024年4月24日・米国防省公開・Release 02 | article_id 確定後に #TBD を除去した公開用タイトルへ確定する
---WARN_DETAILS_END---
---CODEX_AUDIT_END---