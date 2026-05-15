# ドラフト生成レポート #091-#100

**作成日:** 2026-05-14
**適用仕様:** docs/draft_type_classification_v1.md
**ステータス:** 全10件生成完了

---

## 対象記事一覧・PDFタイプ

| article_id | pdf_file_name | TYPE | 生成ドラフト |
|---|---|---|---|
| #091 | fbi-photo-b23.pdf | TYPE-A | ai_summary_091_fbi_photo_b23_2025_note_version.md |
| #092 | fbi-photo-b24.pdf | TYPE-A | ai_summary_092_fbi_photo_b24_2025_note_version.md |
| #093 | dow-uap-d32-mission-report,-syria-october-2024.pdf | TYPE-D | ai_summary_093_dow_d32_syria_oct2024_note_version.md |
| #094 | 65_hs1-834228961_62-hq-83894_section_3.pdf | TYPE-G | ai_summary_094_fbi_hq_62hq83894_section3_note_version.md |
| #095 | 65_hs1-834228961_62-hq-83894_section_4.pdf | TYPE-G | ai_summary_095_fbi_hq_62hq83894_section4_note_version.md |
| #096 | 65_hs1-834228961_62-hq-83894_section_5.pdf | TYPE-G | ai_summary_096_fbi_hq_62hq83894_section5_note_version.md |
| #097 | 65_hs1-834228961_62-hq-83894_section_6.pdf | TYPE-G | ai_summary_097_fbi_hq_62hq83894_section6_note_version.md |
| #098 | 65_hs1-834228961_62-hq-83894_section_7.pdf | TYPE-G | ai_summary_098_fbi_hq_62hq83894_section7_note_version.md |
| #099 | 65_hs1-834228961_62-hq-83894_section_8.pdf | TYPE-G | ai_summary_099_fbi_hq_62hq83894_section8_note_version.md |
| #100 | 65_hs1-834228961_62-hq-83894_section_9.pdf | TYPE-G | ai_summary_100_fbi_hq_62hq83894_section9_note_version.md |

---

## 保留記事

- `59_214434_sp_16_[7.18.1963].pdf` → 重複疑い（#069と同一内容の可能性）。要人間確認。
- `65_hs1-834228961_62-hq-83894_section_10.pdf` → 184ページ・OCR不可確認済み。量が多いため#101以降。

---

## TYPE分類詳細

### TYPE-A (#091, #092): fbi-photo-b23/b24

分類根拠：
- FBIがAARO提出した静止画（war.gov説明文より）
- テキスト層なし推定
- OCR不可（スキャン画像PDF）
- モノクロ静止画・クロスヘア・暗点確認

重要注意：
- fbi-photo-b23/b24 は fbi-photo-b1〜b22（1999年12月31日IRシリーズ）とは別インシデント
- インシデント日時: 2025年後半（b1-b22: 1999年）
- 場所: 米国西部（b1-b22: 不明）
- 画像内日時不正確（system date/time not set）

### TYPE-D (#093): dow-uap-d32

分類根拠：
- MISREP（軍事インシデント報告書）
- Agency: USCENTCOM（米国中央軍）
- Incident Date: 2024年10月20日
- テキスト層あり推定

注意：
- 同PDFがAAROの3件の未解決UAP報告（PR31/PR32/PR33）の参照元
- GENTEXTの報告者記述のみ確認（PDF本文直接OCR未実施）
- 報告者記述は主観的解釈（war.gov注記より）

### TYPE-G (#094-#100): 62-HQ-83894 section 3-9

分類根拠：
- FBI内部文書断片シリーズ
- テキスト層なし推定（section_10の184ページ全ページ0文字から類推）
- ファイル名のみから識別可能

注意：
- 各セクションのページ数は不明
- war.gov説明文はシリーズ全体の記述（個別セクション内容は未確認）
- 既存の#065（section_1）・#066（section_2）との継続記事

---

## 適用した短文化ルール

- TYPE-A: 本文2〜4文・視覚観察はwar.gov説明文に限定・AI解析メモ1行
- TYPE-D: GENTEXTの報告者記述のみ・座標等フォームフィールドの直接確認は省略
- TYPE-G: ファイル名＋war.gov説明文のみ・ページ数不明と明示・シリーズ構成断定なし

---

## 外部背景を削除・抑制した箇所

- TYPE-G: 既存#065/066ドラフトにあった「62は国内安全保障調査分類」のような外部FBI番号体系説明を排除
- TYPE-G: 「Record Group 65（FBI記録）」への言及はファイル名由来として保持（外部断定なし）
- TYPE-A (#091/092): b23/b24を1999年IRシリーズと混同しないよう明示的に分離
- TYPE-D: USCENTCOM・シリア等の背景説明を排除、報告者記述のみに限定

---

## 注意点

- b23/b24 (#091/092): 画像内日時が不正確（war.gov公式確認）。timestamp利用不可。
- d32 (#093): PDF本文のOCR未実施のため、フォームフィールド値（座標・高度・速度等）は未確認。
- sections 3-9 (#094-#100): ページ数不明。テキスト層なし推定。war.gov説明文が個別セクション内容を示さない点を明記。
- source_registry.csv: #091-#100 を status=draft で追加済み。published_date・note_url は空欄。

---

## source_registry #091-#100 登録内容

- status: draft（全10件）
- note_url: 空欄
- published_date: 空欄
- created_date: 2026-05-14

---

*作成: 2026-05-14*
*生成数: 10件（TYPE-A×2、TYPE-D×1、TYPE-G×7）*
