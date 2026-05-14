# プロベナンス一括監査レポート
**実施日:** 2026-05-12  
**対象:** published_articles/ 全件 + note_drafts/ 全件  
**ツール:** `scripts/generate_provenance.py`  
**バッチレポート:** `review_logs/provenance_published_ALL_report.md` / `review_logs/provenance_drafts_ai_summary_report.md` / `review_logs/provenance_drafts_ai_reading_report.md`

---

## A. 全体サマリー

| カテゴリ | 対象ファイル数 | OK(LOW) | MEDIUMあり | HIGHあり |
|---|---|---|---|---|
| published_articles/ | 20 | 5 | 13 | 2 |
| note_drafts/ ai_summary | 8 | 3 | 5 | 0 |
| note_drafts/ ai_reading | 5 | 2 | 1 | 2 |
| **合計** | **33** | **10** | **19** | **4** |

> HIGH 4件のうち、**真の問題は3件**（下記B参照）。残り1件はOCRノイズ偽陽性（#013）。

---

## B. HIGH 一覧

### B-1. 真の問題（要修正）

#### ① #029 (note_drafts) d55 Syria 2016 ✅ 修正済み

| 項目 | 内容 |
|---|---|
| ファイル | `note_drafts/ai_summary_029_d55_syria_2016_note_version.md` |
| 元PDF | `dow-uap-d55-mission-report-syria-november-2016.pdf` |
| 問題クレーム1 | `contrail`（飛行雲） |
| ソース状態 | PDFに存在しない |
| 問題クレーム2 | `100,000フィート` |
| ソース状態 | PDFに存在しない |
| 分類 | AI hallucination（一般知識からの混入） |
| 対応 | **削除済み** |

---

#### ② #003 (ai_reading) Western US Event Slides ⚠️ 未修正

| 項目 | 内容 |
|---|---|
| ファイル | `note_drafts/ai_reading_003_western_us_event_slides_note_version.md` |
| 元PDF | `western_us_event_slides_5.08.2026.pdf` |
| 問題クレーム | `約45メートル先で止まった` |
| PDF原文 | `stopping about 50 yards away` |
| 分類 | **unit notation rule v1 違反**（原文値 "50 yards" が消失し換算値のみ） |
| 推奨対応 | `「スポットライトのビームが50ヤード（約45メートル）先で止まった」` に修正 |

---

#### ③ #002 (ai_reading) USPER Statement ⚠️ 未修正（2件）

| 項目 | 内容 |
|---|---|
| ファイル | `note_drafts/ai_reading_002_usper-statement_note_version.md` |
| 元PDF | `usper-statement-redacted.pdf` |
| **問題クレーム A** | `約90分間にわたり複数回の目撃が連続` |
| PDF状態 | `90` はPDFに存在しない。タイムスタンプ最終: 2320（23:20） |
| 実際の継続時間 | 主要目撃フェーズ 2227〜2320 = 約53分間 |
| 分類 | AI計算誤り（90分＝22:27+90→23:57だが終点2357はPDF不在） |
| 推奨対応 | `約90分間` → `約53分間（22時27分〜23時20分頃）` に修正。または期間表記を削除。 |
| **問題クレーム B** | `午後11時57分` （23:57） |
| PDF状態 | PDFの最終タイムスタンプは `2320`（23:20）。2357は存在しない。 |
| 分類 | AI計算誤り（90分計算の終点として生成） |
| 推奨対応 | `11時57分` → `23時20分頃` に修正（2306〜2320が最終フェーズ） |

---

### B-2. 偽陽性 HIGH（修正不要・注記済みまたは要確認）

#### ④ #013 (published) d57 Gulf of Aden — OCRノイズ偽陽性

| 項目 | 内容 |
|---|---|
| ファイル | `published_articles/ai_summary_013_d57_gulf_of_aden_sep2020_note_version.md` |
| 問題クレーム | `6.17NM` |
| PDF状態 | PDF OCR読み: `6.1 ?NM`（`7` が `?` に誤認） |
| 判定 | **値は正確。OCRノイズによる偽陽性HIGH** |
| 対応 | AI解析メモに注記追記済み ✅ |

#### ⑤ #007 (published) Apollo17 Debriefing — 画像のみPDF

| 項目 | 内容 |
|---|---|
| ファイル | `published_articles/ai_summary_007_apollo17_debriefing_note_version_revised.md` |
| PDF状態 | テキスト層1文字（実質スキャン画像のみ） |
| 問題クレーム | `MSC-07631`（NASA文書番号）・`ALFMED` など |
| 判定 | 自動検証不可。目視確認では正確と思われる（公開NASA文書番号） |
| 対応 | AI解析メモに「目視読み取り」と記載済み ✅ 人間確認推奨 |

#### ⑥ #002 (ai_reading) USPER Statement — 翻訳者注釈・数詞変換

| 問題 | 詳細 | 判定 |
|---|---|---|
| `10フィート` | PDF: "ten feet"（英語数詞）→ 記事: "10フィート"（数字） | **偽陽性**。値は正確。単語→数字変換 |
| `（US Person）` | PDF: "USPER" のみ。`US Person` は略語説明 | **翻訳者注釈**。USPER=US Person は標準DoD定義 |

---

## C. MEDIUM 一覧（確認候補・修正必須ではない）

### C-1. published_articles/

| # | ファイル | MEDIUM項目 | 判定 |
|---|---|---|---|
| 008 | d38 persian_gulf_range_fouler | `UL TN / Black Hot / Linear`（センサー設定）, `UTC` | センサー設定表記 / 標準略語。許容範囲 |
| 014 | d20 f16_middle_east | `USCENTCOM MDR` | 文書ヘッダー定型句。許容範囲 |
| 016 | d6 arabian_gulf | `MISREP`, `UTC`, `MGRS`, `USCENTCOM`（×2） | 疎テキスト(208文字)。標準軍用略語。許容範囲 |
| 018 | d58 range_fouler_na | `Range Fouler Debrief Form`, `O-3`, `USCENTCOM MDR` | 文書形式名・階級。許容範囲 |
| 019 | d4 arabian_gulf | `MISREP`, `UTC`, `MGRS`（疎テキスト) | 標準軍用略語。許容範囲 |
| 020 | d25 mediterranean_greece | `MGRS`, `NON-MANEUVERABLE` | MGRS=座標系。NON-MANEUVERABLE はPDFテキストを再確認推奨 |
| 021 | d3 arabian_gulf | `UTC` | 標準略語。許容範囲 |
| 022 | d60 persian_gulf | `MISREP`, `WAR`, `GOV` | **PDF 0文字（画像のみ）**。自動検証不可。人間確認推奨 |
| 023 | d51 pacific_email | `Intelligence Information Report` | 文書種別名。許容範囲 |
| 025 | d75 gulf_of_aden | `MGRS` | 座標系略語。許容範囲 |
| 026 | d7 arabian_gulf | `MISREP`, `USCENTCOM` | 疎テキスト(453文字)。許容範囲 |
| 027 | d5 arabian_gulf | `SECRET`, `REL TO USA`, `CSV` | 分類マーキング・メタデータ由来。許容範囲 |
| 028 | d10 iraq | `POSSIBLE MISSILE` | **要確認**。PDFで検索再確認推奨 |

### C-2. note_drafts/ ai_summary

| # | ファイル | MEDIUM項目 | 判定 |
|---|---|---|---|
| 017 | d42 japan | `O-2`, `USCENTCOM MDR` | 階級・文書ヘッダー。許容範囲 |
| 029 | d55 syria | `USCENTCOM MDR` | 文書ヘッダー。許容範囲 |
| 031 | d62 hormuz | `GENTEXT/OBSERVATION`, `ID330414`, `USCENTCOM MDR` | 文書セクション名・ID番号・ヘッダー。許容範囲 |
| 033 | d74 syria_nov2023 | `CONSISTENTLY FOR AT LEAST` | 長い句がPDFテキストと完全一致しない可能性。確認推奨 |
| 035 | d8 djibouti | `CSV` | メタデータ言及。許容範囲 |

### C-3. note_drafts/ ai_reading

| ファイル | MEDIUM項目 | 判定 |
|---|---|---|
| ai_reading_001 composite-sketch | `WAR` | PDF 0文字（画像のみ）。自動検証不可 |

---

## D. LOW 一覧（AI補助換算・翻訳者注釈）

以下は数値・単位表記ルール v1 に基づきLOW扱いとなっている項目（主なもの）。

| ファイル | LOW項目 | 内容 |
|---|---|---|
| #019 d4 | `Possible` | 限定表現の翻訳者コンテキスト |
| #032 d33 greece | `Greece` | 地名（翻訳者が地理コンテキストとして追加） |
| #035 d8 djibouti | `nautical miles per hour` | ノット単位の説明（translator補足） |

> AI補助換算（括弧内 `約N単位`）はすべてLOW扱い。#026（31,000フィート→9.4km）・#027（FL160〜170→4.9〜5.2km）など。

---

## 特記事項：画像のみPDF（自動検証不可）

| ファイル | PDF文字数 | 状況 |
|---|---|---|
| #007 Apollo17 Debriefing | 1文字 | 目視読み取りで作成。MSC-07631は公開NASA文書番号で正確と推定 |
| #022 d60 Persian Gulf | 5文字（実質0） | 全クレーム自動検証不可。**人間確認必要** |
| #001 composite-sketch | 0文字 | 画像のみ。記事内容の自動検証不可 |

---

## 公開再開条件（推奨）

### 必須（修正後に公開可）

1. **#002 (ai_reading_002)** — `90分間` → 実際の継続時間に修正（約53分 or 約1時間）
2. **#002 (ai_reading_002)** — `11時57分`（23:57）→ `23時20分頃` に修正
3. **#003 (ai_reading_003)** — `約45メートル先` → `50ヤード（約45メートル）先` に修正（原文値復活）

### 推奨確認（公開前に目視確認）

4. **#022 (published)** d60 — PDF画像のみ。記事クレームを目視確認
5. **#028 (published)** d10 Iraq — `POSSIBLE MISSILE` をPDFで確認

### 許容範囲（修正不要）

- MEDIUM警告のうち、標準軍用略語・文書種別名・疎テキストPDFのもの → 現状維持
- HIGH偽陽性（#013 OCRノイズ、#007 画像PDF）→ AI解析メモへの注記済み

---

## バッチレポートファイル一覧

| バッチ | ファイル |
|---|---|
| published_articles 全件 | `review_logs/provenance_published_ALL_report.md` |
| note_drafts ai_summary | `review_logs/provenance_drafts_ai_summary_report.md` |
| note_drafts ai_reading | `review_logs/provenance_drafts_ai_reading_report.md` |

---

*このレポートは `scripts/generate_provenance.py` の自動出力を人間がレビュー・分類したものです。*  
*generate_provenance.py バージョン: 2026-05-12 最終版*
