# ドラフト生成計画 #091-#100

**作成日:** 2026-05-14
**適用仕様:** docs/draft_type_classification_v1.md
**対象:** raw_pdf/ 未登録PDFのうちドラフト未生成10件

---

## 対象PDF一覧・タイプ分類

| article_id | pdf_file_name | source_url | 既存ドラフト | 重複 | PDFタイプ | 分類根拠 |
|---|---|---|---|---|---|---|
| #091 | fbi-photo-b23.pdf | https://www.war.gov/medialink/ufo/release_1/fbi-photo-b23.pdf | なし | なし | TYPE-A | モノクロ静止画・テキスト層なし（推定）・FBI提出AARO・2025年 |
| #092 | fbi-photo-b24.pdf | https://www.war.gov/medialink/ufo/release_1/fbi-photo-b24.pdf | なし | なし | TYPE-A | モノクロ静止画・テキスト層なし（推定）・FBI提出AARO・2025年 |
| #093 | dow-uap-d32-mission-report,-syria-october-2024.pdf | https://www.war.gov/medialink/ufo/release_1/dow-uap-d32-mission-report,-syria-october-2024.pdf | なし | なし | TYPE-D | MISREP・テキスト層あり（推定）・DoW・2024年10月・シリア |
| #094 | 65_hs1-834228961_62-hq-83894_section_3.pdf | https://www.war.gov/medialink/ufo/release_1/65_hs1-834228961_62-hq-83894_section_3.pdf | なし | なし | TYPE-G | FBI内部文書・スキャン画像PDF・62-HQ-83894シリーズ |
| #095 | 65_hs1-834228961_62-hq-83894_section_4.pdf | https://www.war.gov/medialink/ufo/release_1/65_hs1-834228961_62-hq-83894_section_4.pdf | なし | なし | TYPE-G | 同上 |
| #096 | 65_hs1-834228961_62-hq-83894_section_5.pdf | https://www.war.gov/medialink/ufo/release_1/65_hs1-834228961_62-hq-83894_section_5.pdf | なし | なし | TYPE-G | 同上 |
| #097 | 65_hs1-834228961_62-hq-83894_section_6.pdf | https://www.war.gov/medialink/ufo/release_1/65_hs1-834228961_62-hq-83894_section_6.pdf | なし | なし | TYPE-G | 同上 |
| #098 | 65_hs1-834228961_62-hq-83894_section_7.pdf | https://www.war.gov/medialink/ufo/release_1/65_hs1-834228961_62-hq-83894_section_7.pdf | なし | なし | TYPE-G | 同上 |
| #099 | 65_hs1-834228961_62-hq-83894_section_8.pdf | https://www.war.gov/medialink/ufo/release_1/65_hs1-834228961_62-hq-83894_section_8.pdf | なし | なし | TYPE-G | 同上 |
| #100 | 65_hs1-834228961_62-hq-83894_section_9.pdf | https://www.war.gov/medialink/ufo/release_1/65_hs1-834228961_62-hq-83894_section_9.pdf | なし | なし | TYPE-G | 同上 |

---

## 保留・除外

- `59_214434_sp_16_[7.18.1963].pdf` → **重複除外**: ブラケット付きファイル名版。`59_214434_sp_16_7.18.1963.pdf`（#069）と同一内容の可能性が高いため保留。
- `65_hs1-834228961_62-hq-83894_section_10.pdf` → **今回対象外**: 184ページ・テキスト層ゼロ確認済み。量が多いため#101以降で対応。
- `fbi-photo-b23.pdf` / `fbi-photo-b24.pdf` → **注意**: ファイル名がb1-b22と連続しているが、**別インシデント**（2025年・米国西部）。b1-b22（1999年12月31日IRシリーズ）との混同注意。

---

## 重要メタデータ（uap-csv-cache.csv より）

### fbi-photo-b23.pdf (#091)

- Agency: FBI
- Incident Date: Late 2025
- Location: Western United States
- 画像日時注記: "date in image is incorrect due to system date/time not being set"
- war.gov 画像説明（参考）: モノクロ・グレイン状テクスチャ・中央クロスヘア・レチクル右寄りに単一の細長い暗点

### fbi-photo-b24.pdf (#092)

- Agency: FBI
- Incident Date: Late 2025
- Location: Western United States
- 画像日時注記: "date in image is incorrect due to system date/time not being set"
- war.gov 画像説明（参考）: モノクロ・グレイン状テクスチャ・中央クロスヘア・レチクル中央やや上方に単一の不規則形状暗点

### dow-uap-d32-mission-report,-syria-october-2024.pdf (#093)

- Agency: Department of War（USCENTCOM）
- Incident Date: 2024-10-20
- Location: Syria
- 関連AARO未解決報告: DOW-UAP-PR31（5秒FMV）、DOW-UAP-PR32（6秒FMV）、DOW-UAP-PR33（5秒FMV）
- 報告者記述: "misshapen and uneven ball of white light"、"multiple glares or light from unknown origin"、"light/glare halo effect at top of FMV feed"

### 65_hs1-834228961_62-hq-83894 section 3-9 (#094-#100)

- Agency: FBI
- Incident Date: N/A（文書期間: 1947年6月〜1968年7月、war.gov説明文より）
- war.gov 説明: 捜査記録・目撃証言・UFO/空飛ぶ円盤に関する公開報告書を含む。Oak Ridge TN等の写真証拠・推進系技術提案等も含まれる（war.gov説明文より、個別セクションの内容は未確認）
- テキスト層: OCR不可（section_10の184ページ全ページが0文字のためシリーズ全体でOCR不可と推定）
- ページ数: 各セクション不明（section_1=185ページ、section_2=194ページ、section_10=184ページ）

---

## 生成ファイル一覧（予定）

- note_drafts/ai_summary_091_fbi_photo_b23_2025_note_version.md
- note_drafts/ai_summary_092_fbi_photo_b24_2025_note_version.md
- note_drafts/ai_summary_093_dow_d32_syria_oct2024_note_version.md
- note_drafts/ai_summary_094_fbi_hq_62hq83894_section3_note_version.md
- note_drafts/ai_summary_095_fbi_hq_62hq83894_section4_note_version.md
- note_drafts/ai_summary_096_fbi_hq_62hq83894_section5_note_version.md
- note_drafts/ai_summary_097_fbi_hq_62hq83894_section6_note_version.md
- note_drafts/ai_summary_098_fbi_hq_62hq83894_section7_note_version.md
- note_drafts/ai_summary_099_fbi_hq_62hq83894_section8_note_version.md
- note_drafts/ai_summary_100_fbi_hq_62hq83894_section9_note_version.md

---

*作成: 2026-05-14*
*適用仕様: docs/draft_type_classification_v1.md*
