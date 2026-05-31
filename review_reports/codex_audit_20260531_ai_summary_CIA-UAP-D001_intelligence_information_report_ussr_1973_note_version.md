# Codex 監査レポート 20260531 — CIA-UAP-D001

**監査日**: 2026-05-31  
**監査者**: Codex  
**監査対象**: `note_drafts/ai_summary_CIA-UAP-D001_intelligence_information_report_ussr_1973_note_version.md`  
**対象資料**: `raw_pdf/CIA-UAP-D001_Intelligence_Information_Report_USSR_1973.pdf`  
**出力先**: `review_reports/codex_audit_20260531_ai_summary_CIA-UAP-D001_intelligence_information_report_ussr_1973_note_version.md`

**参照資料**:
- `docs/codex_audit_role.md`
- `docs/audit_checklist_v1.md`
- `docs/release02_pdf_visual_policy.md`
- `docs/release02_media_processing_policy_v1.md`
- `docs/release02_audio_video_pipeline_design.md`
- `review_logs/codex_feedback_log.md`
- `metadata/files_catalog.csv`
- `worker_outputs/ocr_review_summary_20260529.csv`

---

## 総合判定

**BLOCK**

UAP目撃段落そのものの要約は概ね原文と整合している。  
ただし、背景説明に原文PDFだけでは確認できない外部知識が本文事実として混入しており、Release 02 の「source_registry / 原文未登録情報を本文へ混ぜない」方針に抵触する。公開前に、背景情報を削除するか、外部背景として明確に分離し、根拠資料を示す必要がある。

---

## サマリー

- PASS: 7
- WARN: 5
- BLOCK: 1
- UNVERIFIABLE: 0

---

## BLOCK

### B-01: 背景説明に原文PDF外の情報が本文事実として混入している

**該当箇所**
- 34行目: `背景：サリ・シャガン試験場とは`
- 36行目: `現在のカザフスタン南部に位置するソ連の主要な防空・対弾道ミサイル試験施設`
- 36行目: `冷戦期を通じて、SA-2...やGALOSH...などの防空・ABMシステムの開発・試験が行われていました`
- 38行目: `当時から米国の諜報機関による監視対象`
- 40行目: `SA-2（System-75）は1960年にU-2偵察機を撃墜したミサイル`
- 40行目: `GALOSH（System-300/Aldan）はソ連の対弾道ミサイル防衛用の迎撃ミサイル`

**問題**  
原文PDFから確認できるのは、主に以下。

- 件名が `The Sary Shagan Weapons Testing Range`
- Country が `USSR`
- System-75 [SA-2]、System-300/Aldan [ABM-1 GALOSH] の弾頭情報
- レーザー兵器実験に関する噂
- Site 7 での未確認現象

一方で、現在の国名・地理、U-2撃墜、冷戦期を通じた施設史、米諜報機関による監視対象だったという説明は、このPDF本文だけでは確認できない。外部背景として書くこと自体は可能だが、現状は記事本文の事実説明に混ざっており、読者が「このPDFから確認できる情報」と誤解するリスクがある。

**公開前に必ず修正すべき理由**  
本プロジェクトでは、公式資料に書かれた内容、投稿者の補足、外部背景を分離する必要がある。とくにRelease 02では、AI生成の背景・組織説明がソース確認なく混入することはAI hallucinationリスクとして扱う。

**修正案 A: 背景セクションを削除・圧縮**

```
## 背景：この報告書の位置づけ

この報告書の件名は「The Sary Shagan Weapons Testing Range」です。本文では、System-75 [SA-2] と System-300/Aldan [ABM-1 GALOSH] の弾頭情報、作業区域、セキュリティフェンス、レーザー兵器実験に関する噂が扱われています。

以下では、原文PDFに含まれる第14段落の未確認現象記録に絞って整理します。
```

**修正案 B: 外部背景として明確に分離**

```
## 外部背景（原文PDF外の補足）

以下は本文PDFの記述ではなく、読者理解のための一般的な歴史背景です。本文要約の根拠には使用しません。

...
```

この場合は、外部背景の根拠資料を別途示すこと。

---

## WARN

### W-01: 配布日「1973年12月」の根拠が弱い

**該当箇所**
- 28行目: `1973年12月に配布されたと記録されています`
- 166行目: `配布日：1973年12月（推定）`

**判定**: WARN

**理由**  
原文p.1には `DATE DISTR.` があるが、画像・埋め込みテキストとも年の判読が不安定。`DOI` は `November 1972-November 1973`、UAP目撃は `late summer 1973` と読めるが、配布年を「1973年12月」と断定する根拠は監査時点では弱い。`metadata/files_catalog.csv` の `incident_date=12/20/73` と、本文中のUAP目撃時期・配布日が混在している可能性もある。

**修正案**

28行目:

```
報告書はドイツで入手された情報に基づくものと記録されています。配布日は原文画像上で判読が難しく、本記事では断定しません。
```

166行目:

```
- 情報対象期間：1972年11月〜1973年11月
- UAP目撃時期：1973年晩夏
- 配布日：原文画像上で判読困難
```

---

### W-02: メタデータの incident date / location と本文側の粒度差を明示した方がよい

**該当箇所**
- 10行目: `Incident Date：1973年晩夏`
- 11行目: `Incident Location：ソ連・サリ・シャガン兵器試験場...Site 7`

**判定**: WARN

**理由**  
`metadata/files_catalog.csv` では `incident_date=12/20/73`、`incident_location=USSR`。本文はPDF第14段落からUAP目撃時期を `late summer 1973`、目撃場所を `Site 7` と読み替えており、原文に基づく精緻化としては妥当。  
ただし、台帳値と本文値の粒度が異なるため、読者向けには「カタログ上の値」と「本文から読める目撃記録」を分けるとより安全。

**修正案**

```
- Catalog Incident Date：12/20/73（metadata/files_catalog.csv 上の値）
- 本文上の目撃時期：1973年晩夏（late summer 1973）
- Catalog Location：USSR
- 本文上の目撃場所：Sary Shagan Weapons Testing Range 内 Site 7
```

note本文では冗長なら、脚注的に「本文中のUAP目撃時期は原文第14段落に基づく」と補足するだけでもよい。

---

### W-03: 原文抜粋が長く、note投稿互換上のWARN対象

**該当箇所**
- 96〜97行目: 約323字
- 109行目: 約288字
- 119行目: 約273字

**判定**: WARN

**理由**  
引用ブロック形式ではないためBLOCKではないが、`docs/audit_checklist_v1.md` の「長い英文引用（目安200字超）」に該当する。note投稿時の読みづらさ・レイアウト崩れリスクを下げるため、抜粋を短くする方がよい。

**修正案**

109行目は以下程度に短縮。

```
"Source observed an unidentified phenomenon at Site 7..."
"...a sharp (bright) green circular object or mass in the sky."
```

119行目は以下程度に短縮。

```
"the green circle widened..."
"several green concentric circles formed around the mass."
"There was no sound..."
```

---

### W-04: 背景資料記事としての注意書きがやや弱い

**該当箇所**
- 26〜30行目

**判定**: WARN

**理由**  
このPDFはUAP単独の目撃報告書ではなく、主題はサリ・シャガン試験場の施設・弾頭技術情報で、UAP記録は末尾の1段落。本文30行目でその点は説明されているが、Release 02の歴史資料記事としては、冒頭でより明確に「本資料はUAP目撃事案のみを扱った報告書ではありません」と示す方が安全。

**修正案**

```
本資料はUAP目撃事案だけを扱った報告書ではありません。主題はサリ・シャガン兵器試験場に関するCIA情報報告であり、UAPに関する記述は末尾の1段落です。
```

---

### W-05: 画像素材の実在確認ができない

**該当箇所**
- 21〜22行目: p.1画像プレースホルダー
- 86〜87行目: p.3画像プレースホルダー
- 169行目: `使用画像：CIA-UAP-D001... p.1・p.3`

**判定**: WARN

**理由**  
キャプション内容は `docs/release02_pdf_visual_policy.md` の「出典・視覚的参考・非断定」方針に沿っている。  
ただし監査時点で `page_images/` 配下にCIA-UAP-D001用の画像ディレクトリは確認できなかった。note公開時に実画像が未挿入のままプレースホルダーが残ると不自然。

**修正案**

画像を使用する場合は、公開前にp.1・p.3の画像素材を生成・確認する。画像を使わない場合は、21〜22行目、86〜87行目、169行目を削除する。

---

## 観点別チェック

### 1. 公式資料・情報源主観・記事側推論の分離

**判定**: WARN

UAP目撃部分は、原文・情報源の観察・CIAフィールドコメントがよく分離されている。  
一方、背景説明では外部背景と原文情報の境界が曖昧。B-01参照。

### 2. メタデータ整合性

**判定**: WARN

`metadata/files_catalog.csv` と一致:

- file_name: `CIA-UAP-D001_Intelligence_Information_Report_USSR_1973.pdf`
- agency: `Central Intelligence Agency`
- release_date: `2026-05-22`
- file_type: `PDF`
- ocr_status: `not_needed`
- download_url: 一致

注意点:

- `files_catalog.csv` の `incident_date` は `12/20/73`、本文のUAP目撃時期は `late summer 1973`
- `files_catalog.csv` の `incident_location` は `USSR`、本文のUAP目撃場所は `Site 7`

本文値は原文第14段落に基づくため不正ではないが、台帳値との差は補足推奨。

### 3. UAP / UFO 断定表現

**判定**: PASS

「UFO」「宇宙人」「異星人」「地球外由来」「決定的証拠」等の煽り・断定表現はない。タイトルの「緑の円形現象」も原文の `green circular object or mass` に対応しており、過度な誇張ではない。

### 4. 現象描写の原文整合

**判定**: PASS

以下はいずれも原文第14段落と整合。

- 1973年晩夏の夜
- Site 7
- カナダとソ連のスポーツ競技をテレビで見ていた
- 西方向、仰角約70度
- 明るい緑色の円形の物体または塊
- 10〜15秒以内に拡大
- 複数の緑色同心円
- 数分で色が消えた
- 音・爆発音なし
- 情報源にも意見なし、噂なし、追加詳細なし

### 5. `laser weapons` / ミサイル関連記述

**判定**: PASS / WARN

60行目の「レーザー兵器実験が行われているという噂」は、原文の `According to hearsay...` に基づいており、噂として扱えている。  
ただし、背景セクションでミサイル史を外部知識として足している点はB-01。

### 6. OCR / テキスト品質

**判定**: PASS

本文142〜144行目のPyMuPDF文字数は、監査時点の再抽出結果と一致。

- p.1: 1,200字
- p.2: 1,809字
- p.3: 1,184字

`metadata/text_layer_report.csv` では改行等の扱いが異なるため 1,152 / 1,763 / 1,147字だが、いずれも `text layer present, OCR not needed` で整合。  
`worker_outputs/ocr_review_summary_20260529.csv` にはCIA-UAP-D001の個別行は確認できなかった。

### 7. note投稿互換性

**判定**: PASS / WARN

以下は検出されなかった。

- Markdown table
- 引用ブロック
- コードブロック
- Codex注釈ブロック
- 2階層以上のネスト箇条書き

ただし、200字超の英文抜粋が複数あるため W-03。

### 8. 画像キャプション

**判定**: PASS / WARN

キャプション文は、資料名・ページ番号・機密解除済み・視覚的参考・画像単体で断定しない旨を含み、方針と整合。  
素材実在確認のみ W-05。

### 9. AI利用上の留保・ディスクレイマー

**判定**: PASS

30行目、154〜156行目、175行目で、UAPの正体・起源を断定しないこと、AI処理には誤変換・誤訳があり得ること、投稿者が米政府・AARO等と無関係であることが明記されている。

---

## 最終判定

**BLOCK**

公開前に最低限 B-01 を修正すること。  
そのうえで W-01〜W-05 を処理すれば、UAP目撃段落の要約としては公開可能水準に近い。
