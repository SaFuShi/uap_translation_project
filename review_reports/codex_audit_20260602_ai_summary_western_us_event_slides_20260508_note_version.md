# Codex 監査レポート 20260602 — ai_summary_western_us_event_slides_20260508_note_version

**監査日**: 2026-06-02  
**監査対象**: note_drafts/ai_summary_western_us_event_slides_20260508_note_version.md  
**監査者**: Codex（Claude Code 内蔵監査フェーズ）  
**原資料**: western_us_event_slides_5.08.2026.pdf（4ページ、テキスト層あり、Unclassified）

---

## サマリー

| 判定 | 件数 |
|------|------|
| ✅ PASS | 22 |
| ⚠️ WARN | 5 |
| 🔴 BLOCK | 0 |
| ❓ UNVERIFIABLE | 2 |

**総合判定**: ⚠️ WARN（公開可・修正推奨）

BLOCKなし。WARNは英文引用の長さ（W-03〜W-05）と軽微なフォーマット問題（W-01、W-02）。修正後の公開を推奨。

---

## 判定詳細

### Phase 0: note投稿フォーマットチェック

| 項目 | 判定 | 備考 |
|------|------|------|
| Markdown table禁止 | ✅ | 本文なし |
| 引用ブロック（`>`）禁止 | ✅ | 本文なし |
| 2階層以上ネスト箇条書き禁止 | ✅ | すべて単層 |
| Codex注釈ブロック禁止 | ✅ | 混入なし |
| 長い英文引用（200字超） | ⚠️ W-03〜05 | 原文抜粋①②③が200字超 |

---

### Phase 1: Provenance Audit

| 項目 | 判定 | 備考 |
|------|------|------|
| ファイル名整合性 | ✅ | 資料名・ファイル名一致 |
| 直接PDF URL | ⚠️ W-01 | 出典情報内には記載あり。フッター「Source URL」はトップページのまま |
| Incident Date整合性 | ✅ | 「2023年」で一貫 |
| Incident Location整合性 | ✅ | 「米国西部（非公開）」で一貫 |
| 推定値の明記 | ✅ | 目撃距離推定・AARO測定値が明確に区別されている |
| source_registry.csv BLOCK状態確認 | ❓ | source_registryに未登録（候補段階）。BLOCK事由なし |
| 重複チェック（MD5） | ❓ | MD5クロスチェック未実施 |

---

### Phase 2: 日本語 UX レビュー

**P2-1 記事構成**

| 項目 | 判定 | 備考 |
|------|------|------|
| 構成順（メタデータ→要点→AI要約→注意→出典→免責） | ✅ | 準拠 |
| 要点項目数 | ⚠️ W-02 | 7項目（基準3項目、4以上はWARN） |
| 限定情報記事警告 | ✅ | 該当なし（フルテキスト資料） |
| 出典セクションに元PDF URLと元ファイル名 | ✅ | 両方記載あり |
| 免責文 | ✅ | 末尾に記載 |

**P2-2 略語・専門用語**

| 略語 | 判定 | 備考 |
|------|------|------|
| USPER | ✅ | 初出で「U.S. Person、連邦法執行機関の特別捜査官」と説明。本文中も繰り返し付記 |
| AARO | ✅ | 初出「全領域異常解決局・米国防総省のUAP調査機関」。6箇所で注釈あり |
| NVG | ✅ | 初出「暗視ゴーグル（Night Vision Goggles）」。4箇所で注釈あり |
| UAP | ✅ | 「未確認異常現象」と説明 |

**P2-3 表現の客観性・中立性**

| 項目 | 判定 | 備考 |
|------|------|------|
| UFO/宇宙人/異星人表現 | ✅ | 使用なし |
| 断定表現（物体種別） | ✅ | 「目撃した」「証言した」「報告している」で統一 |
| 推測・事実の区別 | ✅ | AARO測定値とUSPER証言が明確に分離されている |
| 「透明性を持っていた可能性を示唆」 | ✅ | 証言ベースの表現。適切な留保あり |
| 「サウロンの目」比喩 | ✅ | 「目撃者自身の言葉による表現であり、形状の断定ではありません」と注記 ✅ |

**P2-4 単位換算**

| 単位 | 換算 | 判定 |
|------|------|------|
| 2〜3フィート | 約0.6〜0.9メートル | ✅（1ft=0.3048m、誤差0%）|
| 15〜20マイル/時 | 約24〜32キロメートル | ✅（1mph=1.609km、誤差<1%）|
| 4フィート | 約1.2メートル | ✅（誤差0%）|
| 50ヤード | 約46メートル | ✅（50×0.9144=45.7m、誤差<1%）|
| メートル単位値 | 変換不要 | ✅ |

**P2-5 読みやすさ**

| 項目 | 判定 | 備考 |
|------|------|------|
| OCR生ログ混入 | ✅ | なし |
| Markdown table混入 | ✅ | なし |
| 英文引用（200字超） | ⚠️ W-03〜05 | 原文抜粋①②③が200字超。詳細下記 |
| 直訳臭 | ✅ | 自然な日本語 |

**P2-6 日本語読者向けチェック**

| 項目 | 判定 | 備考 |
|------|------|------|
| 単位換算（全出現箇所） | ✅ | フィート・マイル・ヤード全箇所で換算付き |
| 略語注釈（読者が戻らず読める頻度） | ✅ | USPER/AARO/NVGとも繰り返し注釈あり |
| 注釈の過剰・読みにくさ | ✅ | 適切な長さ |

---

## WARN 詳細

**W-01: フッター「Source URL」がトップページURL**

- 対象箇所：末尾「Source URL：https://www.war.gov/UFO/」
- 問題：チェックリストP1-1は「Source URL」を直接PDFのURLにすることを要求している
- ただし：出典情報セクション内に「直接URL：https://www.war.gov/medialink/ufo/release_1/western_us_event_slides_5.08.2026.pdf」が明記されており、直接URLは資料内に存在する
- 修正案：フッターの「Source URL」を直接PDFのURLに変更するか、「Source URL（PDFダウンロード）：https://www.war.gov/medialink/ufo/release_1/western_us_event_slides_5.08.2026.pdf」とする

---

**W-02: 要点項目が7項目（基準は3項目）**

- 対象箇所：「この資料の要点」セクション（7項目）
- 問題：チェックリストP2-1は3項目を基準とし、4以上でWARN
- 備考：DOW-UAP-D017でも同様の7項目で運用されており、ユーザーが承認済みのパターン。過去WARNとして受理されている
- 修正案：現状維持でも可。3〜4項目に絞る場合は「複数チームによる独立目撃」「AAAROによる大型オーブ事後測定（距離1,050m・直径12〜18m）」「光線を遮断した透明な凧型物体」の3点が核心

---

**W-03: 原文抜粋①が200字超（約280字）**

- 対象箇所：【原文抜粋】①「オーブがオーブを射出した」（p.1）
- 問題：英文引用が200字を超えており、noteでの表示崩れリスクがある
- 修正案：後半の "This is stated to have occurred at least five times." を削除し、【要訳】側に吸収する（約200字以下になる）

---

**W-04: 原文抜粋②が200字超（約210字）**

- 対象箇所：【原文抜粋】②「AARO事後測定」（p.2）
- 問題：2文あわせて210字程度
- 修正案：「Measurements later gathered by AARO assess the object to have been ~1050 meters away from the observers, and between 12-18 meters in diameter.」と1文に短縮（「…」省略でも可）

---

**W-05: 原文抜粋③が200字超（約265字）**

- 対象箇所：【原文抜粋】③「NVGで見た暗い凧型物体」（p.3）
- 問題：265字程度
- 修正案：「…and that once the lights were off, a "very thin line" remained.」のみに短縮し、前文は【要訳】側に移す（約130字になる）

---

## UNVERIFIABLE 詳細

**U-01: source_registry.csv 登録状態**

この資料はsource_registry.csvに未登録の候補段階のため、連番整合性・BLOCK状態の確認が行えない。公開前にsource_registry.csvへの登録が必要。

**U-02: MD5クロスチェック（重複確認）**

raw_pdf/ 内の既存ファイルとのMD5クロスチェックは未実施。war.gov側の異ファイル名重複リスクあり（既知事例：#069）。公開前の確認を推奨。

---

## 総評

本ドラフトはBLOCKなし。構成・中立性・単位換算・略語注釈はいずれも基準を満たしている。

WARNの中核は英文引用の長さ（W-03〜W-05）であり、3箇所の短縮修正が推奨される。W-01（フッターSource URL）とW-02（要点項目数）は軽微で、過去のユーザー承認事例がある。

修正後、公開可と判断する。

---

## 次のアクション（人間確認待ち）

- W-01〜W-05の修正要否を判断する
- 修正した場合はドラフトを更新する
- source_registry.csvへの登録（公開前）
- note上での記事番号付与（【概要版#2_004】等）

---

## 追記監査（Codex再確認 2026-06-02）

**追記理由**: ユーザー依頼に基づく再監査。既存レポートは上書きせず、追加確認結果のみ追記する。  
**最新総合判定**: ⚠️ WARN（BLOCKなし。公開前の軽微修正推奨）

### 参照・照合結果

- 指定対象資料 `raw_pdf/ai_summary_western_us_event_slides_20260508.pdf` はローカルに存在しない。
- 実在する対応PDFは `raw_pdf/western_us_event_slides_5.08.2026.pdf`。
- `metadata/files_catalog.csv` の該当行は `western_us_event_slides_5.08.2026.pdf / Department of War / 2026-05-08 / 2023 / Western United States`。
- PDF本文は4ページすべてテキスト抽出可能。主要数値（約1,050m、12-18m、2-3 feet、15-20mph、4 feet、50 yards）はPDF本文と対応。
- `worker_outputs/ocr_review_summary_20260529.csv` と `worker_outputs/ocr_challenge_candidates_20260529.csv` には該当行なし。ドラフト本文の「OCRエラーなし」はPDFテキスト層の直接抽出結果とは整合するが、指定OCRサマリCSVからは確認できない。

### 追加WARN

**W-06: 対象資料パスの指定不一致**

- 対象箇所：依頼文の対象資料 `raw_pdf/ai_summary_western_us_event_slides_20260508.pdf`
- 確認結果：このパスのPDFは存在しない。実ファイルは `raw_pdf/western_us_event_slides_5.08.2026.pdf`
- 影響：ドラフト本文のファイル名・直接URL・files_catalog.csv とは整合しているため、記事内容のBLOCKではない
- 修正案：監査・制作メモ側の対象資料名を `raw_pdf/western_us_event_slides_5.08.2026.pdf` に統一する

**W-07: AAROの誤記（AAARO）**

- 対象箇所：`この資料の要点`
- 該当文：`AAAROによる大型オーブの事後測定`
- 問題：本文・PDF・カタログ上の組織名は `AARO`。`AAARO` は単純誤記
- 修正案：`AAROによる大型オーブの事後測定`

**W-08: 画像キャプションは未検証**

- 対象箇所：`使用ビジュアル候補：p.2（Artist Rendering）・p.3（Image 1：USPER6描画再現）・p.4（Image 2：USPER6描画再現）`
- 問題：現ドラフトには画像候補リストはあるが、実際にnoteへ挿入する画像キャプション本文はまだない
- 判定：画像を未挿入のまま公開するなら問題なし。画像を使用する場合は、`release02_pdf_visual_policy.md` に従い、出典・ページ番号・視覚的参考・画像単体で断定しない旨のキャプションが必要
- 修正案：画像使用時は各画像の直下に `▲ Western U.S. Event Slides p.X。... 内容の視覚的参考として掲載。この画像のみで現象の性質を断定するものではありません。` の形式で追加する

### 既存WARNの再確認

- W-01 Source URL：末尾の `Source URL：https://www.war.gov/UFO/` はトップページ。出典情報内に直接URLはあるためBLOCKにはしないが、`Source URL（PDF）：https://www.war.gov/medialink/ufo/release_1/western_us_event_slides_5.08.2026.pdf` へ修正推奨。
- W-03〜W-05 原文抜粋：①約291字、②約205字、③約264字。note互換性の観点から短縮推奨。
- W-02 要点7項目：読みやすさ上のWARN。公開停止理由ではない。

### 追加確認観点への回答

- 公式資料・証言者/報告者の見解・記事側の推論：概ね分離されている。AARO測定値、USPER証言、記事側留保は区別あり。
- file_name / agency / release date / incident date / location：files_catalog.csv と整合。ただし依頼文の対象資料パスのみ不一致。
- PDF外背景知識の混入：重大な混入なし。
- 強い表現・断定表現：`射出`、`遮断`、`ゼロ抵抗` はPDFの `emit/launch`、beam stopping、`zero resistance` に根拠あり。ただしタイトルの「光線を遮断した」は読者に物理的原因断定に見えやすいため、余裕があれば「光線が止まったと証言された」へ弱めるとより安全。
- 原文抜粋：3箇所が長め。短縮推奨。
- note投稿互換性：Markdown table、引用ブロック、コードブロック、Codex注釈ブロックは検出なし。
- 日本語読者向けチェック：feet / miles / yards は日本向け換算あり。NVG・AARO・USPERも注釈あり。該当しない OSI / AFSWP / AEC / UNM / NARA / AFB / FLIR は本文未出現。
- AI利用上の留保・ディスクレイマー：十分。

### 公開可否

**WARN**。BLOCKはないが、公開前に少なくとも `AAARO` 誤記、末尾Source URL、長い英文抜粋3箇所の短縮を推奨する。画像を実際に挿入する場合はキャプション追加も必要。
