# Codex 監査レポート 20260531 — DOW-UAP-D017

**監査日**: 2026-05-31  
**監査者**: Codex  
**監査対象**: `note_drafts/ai_summary_DOW-UAP-D017_general_correspondence_sandia_note_version.md`  
**対象資料**: `raw_pdf/DOW-UAP-D017_General_Correspondence_Of_Sandia.pdf`  
**出力先**: `review_reports/codex_audit_20260531_ai_summary_DOW-UAP-D017_general_correspondence_sandia_note_version.md`

**参照資料**:
- `docs/codex_audit_role.md`
- `docs/audit_checklist_v1.md`
- `docs/release02_pdf_visual_policy.md`
- `docs/release02_media_processing_policy_v1.md`
- `docs/release02_audio_video_pipeline_design.md`
- `review_logs/codex_feedback_log.md`
- `metadata/files_catalog.csv`
- `worker_outputs/ocr_review_summary_20260529.csv`
- `worker_outputs/ocr_challenge_candidates_20260529.csv`

---

## 総合判定

**WARN**

公開を止めるBLOCKはありません。  
主要な強い表現（緑色火球、数千人、18ヶ月、機密施設近傍、Sighting No.175、p.62が実質白紙）は、おおむね原文またはOCR/画像確認と整合しています。

ただし、メタデータの agency 表記、LaPaz博士の否定範囲、Sighting No.175写真欠落理由の推測、長い英文抜粋、画像素材パスに修正推奨があります。

---

## サマリー

- PASS: 7
- WARN: 6
- BLOCK: 0
- UNVERIFIABLE: 0

---

## WARN

### W-01: Agency欄がカタログ上の発行機関と内部文書作成機関を混在させている

**該当箇所**
- 8行目: `Agency：Department of the Air Force... / UNMほか`

**判定**: WARN

**理由**  
`metadata/files_catalog.csv` の agency は `Department of War`。ドラフトの記述は文書束内に登場する作成・関与機関としては妥当だが、メタデータ欄の `Agency` としてはカタログ値とずれる。

**修正案**

```
- Agency（catalog）：Department of War
- 文書内の主な作成・関与機関：Department of the Air Force / 17th District OSI / AFSWP / Sandia Base / UNM Institute of Meteoritics ほか
```

---

### W-02: 「流星でも隕石でもない」がLaPaz博士の否定範囲をやや強く圧縮している

**該当箇所**
- 1行目: `「流星でも隕石でもない」`
- 40行目: `「流星でも隕石でもない」ことを示す10項目`
- 72行目: `明確に非流星`
- 122行目: `「流星・隕石ではない」と断言`
- 181行目: `「流星・隕石ではない」と結論づけました`

**判定**: WARN

**理由**  
原文p.76では、LaPaz博士は12月12日の火球について `definitely non-meteoric` と述べ、他の緑色火球も同様である可能性が高いと書いている。また10項目では、通常の流星および隕石落下の特徴との違いを列挙している。  
したがって「非流星」は強く根拠がある。一方、「隕石でもない」と断言するより、「通常の隕石落下の特徴とも合わない」とした方が、否定対象と未特定性の区別が明確になる。

**修正案**

タイトル:

```
# 「通常の流星とは異なる」──1948〜1950年、ニューメキシコの緑色火球とLaPaz博士の18ヶ月調査・米軍機密文書116ページ【AI概要版】
```

122行目:

```
※ LaPaz は12月12日の火球を「明確に非流星」とし、一般的な流星・隕石落下の特徴とも合わないと分析しています。ただし、正体は特定していません。
```

181行目:

```
- LaPaz博士は、通常の流星・隕石落下では説明しにくい差異を示しましたが、「何であるか」の特定はしていません。本記事も正体を断定しません
```

---

### W-03: Sighting No.175の写真欠落理由を推測しすぎている

**該当箇所**
- 97行目: `物理的な写真として管理されていたと推定されますが、スキャン時点では既に外れていたか、別途保管されていると見られます`

**判定**: WARN

**理由**  
p.21の目録には `Photo of Sighting No. 175 w/comments` があり、p.61には写真分析の説明がある。p.62は画像確認上ほぼ白紙で、`worker_outputs/ocr_challenge_candidates_20260529.csv` でも0字・白紙/図版判定。  
ただし、写真がなぜ現行PDFにないのかは原文から確認できない。物理写真の別管理、スキャン時点の欠落、別保管はいずれも推測。

**修正案**

```
なお、この写真（Sighting No. 175）は文書の目録（p.21）に添付物として記載されていますが、現行のデジタル公開版では、写真本体に相当するページ（p.62）はほぼ白紙で、写真は確認できません。欠落理由は本文書からは不明です。
```

---

### W-04: 原文抜粋が長く、note投稿互換上のWARN対象

**該当箇所**
- 117行目: 約239字
- 129行目: 約408字
- 149行目: 約385字
- 159行目: 約236字

**判定**: WARN

**理由**  
引用ブロック形式ではないためBLOCKではないが、`docs/audit_checklist_v1.md` の「長い英文引用（目安200字超）」に該当する。特に129行目と149行目は長く、note上で読みにくくなる可能性がある。

**修正案**

129行目は以下程度に分割・短縮。

```
"A logical explanation was not proffered..."
"the phenomena existed and ... should be studied scientifically..."
"continued occurrence ... in the vicinity of sensitive installations is cause for concern."
```

149行目は以下程度に短縮。

```
"the object ... was not the moon..."
"it was not Venus or any other planet..."
"it was not a bright fixed star slightly out of focus..."
```

---

### W-05: 使用画像パスの実在確認ができない

**該当箇所**
- 20〜21行目: p.21画像プレースホルダー
- 107〜108行目: p.10画像プレースホルダー
- 198行目: `page_images/DOW-UAP-D017_General_Correspondence_Of_Sandia/`

**判定**: WARN

**理由**  
キャプション本文は、資料名・ページ・機密解除済み・視覚的参考・非断定を含み、`docs/release02_pdf_visual_policy.md` と整合している。  
ただし監査時点で、`page_images/` 配下に `DOW-UAP-D017_General_Correspondence_Of_Sandia/` は確認できなかった。

**修正案**

画像を使用する場合は、公開前にp.10・p.21の画像素材を生成・確認する。画像を使わない場合は、20〜21行目、107〜108行目、198行目の画像関連記述を削除または保留表示にする。

---

### W-06: 小さな表記ミス

**該当箇所**
- 172行目: `NARAsタンプ`

**判定**: WARN

**修正案**

```
NARAスタンプ
```

---

## 観点別チェック

### 1. 公式資料・LaPaz博士の見解・記事側推論の分離

**判定**: WARN

LaPaz博士の見解、OSIサマリー、記事側の注意事項は概ね分離されている。  
ただし、「流星でも隕石でもない」は見出し・注意事項で強く圧縮されているため、W-02の修正推奨。

### 2. メタデータ整合性

**判定**: WARN

一致:

- file_name: `DOW-UAP-D017_General_Correspondence_Of_Sandia.pdf`
- release_date: `2026-05-22`
- file_type: `PDF`
- download_url: 一致
- page_count: PyMuPDFで116ページ確認

注意:

- `metadata/files_catalog.csv` の agency は `Department of War`。8行目は内部関与機関リストとしては有用だが、Agency欄としてはW-01。
- `metadata/files_catalog.csv` の incident_date は `1948-1950`、location は `New Mexico`。ドラフトの `1948年12月〜1950年5月` と `ニューメキシコ州 / テキサス州一部` は本文根拠に基づく精緻化として妥当。

### 3. 強い表現の根拠

**判定**: PASS / WARN

根拠あり:

- `緑色火球`: 原文の `green fireballs`
- `機密施設近傍`: p.21 `vicinity of sensitive military and government installations`
- `数千人が目撃`: p.82 `several thousand persons in New Mexico and Texas`
- `18ヶ月`: p.21 `during the past 18 months`
- `論理的説明なし`: p.21 `A logical explanation was not proffered`
- `72件 / 5%未満`: p.64に記載

注意:

- `流星でも隕石でもない` はW-02の通り、非流星・通常の隕石落下との差異として表現を少し弱める方が安全。

### 4. LaPaz博士が否定している対象と未特定性

**判定**: PASS / WARN

95行目、122行目、181〜182行目で「正体を特定していない」「政府公式見解とは限らない」と明記されている点は良い。  
否定対象の表現だけW-02として修正推奨。

### 5. Sighting No.175

**判定**: WARN

p.61の写真分析、p.21の添付物リストは原文根拠あり。p.62がほぼ白紙で写真が確認できない点も画像確認およびOCR challenge候補と整合。  
ただし欠落理由の推測はW-03。

### 6. p.62の扱い

**判定**: PASS

p.62は画像上ほぼ白紙で、`worker_outputs/ocr_challenge_candidates_20260529.csv` でも `0字・conf=95.0（白紙/図版判定）`。ドラフトの「現行デジタル版ではほぼ白紙」「写真本体は未収録」は安全な扱い。

### 7. 外部背景知識の混入

**判定**: PASS

記事内の機関名・LaPaz博士の肩書・Los Alamos会議参加機関・Land-Air契約・Stanfield伍長・Datil等は、確認した範囲ではPDF本文に根拠がある。原文PDF外の歴史背景を事実として大きく混ぜている箇所は見当たらない。

### 8. 原文抜粋の長さ

**判定**: WARN

W-04参照。

### 9. 画像キャプション

**判定**: PASS / WARN

キャプション方針はPASS。画像素材パスの実在確認だけW-05。

### 10. note投稿互換性

**判定**: PASS

以下は検出されなかった。

- Markdown table
- 引用ブロック
- コードブロック
- Codex注釈ブロック
- 2階層以上のネスト箇条書き

長い英文抜粋はW-04。

### 11. AI利用上の留保・ディスクレイマー

**判定**: PASS

33行目、175行目、181〜186行目で、UAPという現代語への整理、正体・起源を断定しないこと、LaPaz博士個人見解と政府公式見解の区別、AI処理の限界が明記されている。

---

## BLOCK

なし。

---

## 最終判定

**WARN（公開可・修正推奨）**

公開前に優先して直すべき点は、W-01（Agency欄）、W-02（LaPaz博士の否定範囲）、W-03（Sighting No.175写真欠落理由の推測）、W-04（長い英文抜粋）です。  
これらを直せば、DOW-UAP-D017の概要記事としては公開可能水準に近い。
