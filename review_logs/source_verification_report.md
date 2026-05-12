# AI概要版 原文照合チェックレポート
生成日時: 2026-05-12 09:55

---

## 目的と限界

このレポートはルールベースの自動チェックです。完全な真偽判定ではなく、
**人間レビュー前の警告出し**を目的としています。

- ✅ 問題なし：自動チェックでは問題を検出しませんでした
- 💬 確認推奨：軽微な確認点があります（公開前に目を通してください）
- ⚠️ 要確認：メタデータ不一致・引用照合失敗など確認が必要です
- ❌ 要修正：重大な問題が検出されました

---

## サマリー

| ファイル | PDF照合 | ERROR | WARNING | INFO | 判定 |
|---|---|---|---|---|---|
| ai_reading_001_composite-sketch_20240430.md | 🔍0文字 | 0 | 1 | 0 | ⚠️ 要確認 |
| ai_reading_001_composite-sketch_20240430_note_version.md | 🔍0文字 | 0 | 0 | 3 | 💬 確認推奨 |
| ai_reading_002_usper-statement_note_version.md | 📄7242文字 | 0 | 0 | 2 | 💬 確認推奨 |
| ai_reading_003_western_us_event_slides_note_version.md | 📄5777文字 | 0 | 0 | 2 | 💬 確認推奨 |
| ai_reading_004_apollo12_transcript_note_version.md | 📄6173文字 | 0 | 0 | 2 | 💬 確認推奨 |
| ai_reading_005_apollo17_transcript_note_version.md | 📄22061文字 | 0 | 0 | 2 | 💬 確認推奨 |
| ai_reading_006_apollo11_debriefing_note_version.md | 🔍0文字 | 0 | 0 | 3 | 💬 確認推奨 |
| ai_reading_007_apollo17_technical_debriefing_note_version.md | 🔍0文字 | 0 | 0 | 4 | 💬 確認推奨 |
| ai_reading_008_d38_middle_east_isr_note_version.md | 📄3441文字 | 0 | 0 | 3 | 💬 確認推奨 |
| ai_reading_009_d56_arabian_sea_note_version.md | 📄3569文字 | 0 | 0 | 3 | 💬 確認推奨 |
| ai_summary_007_apollo17_debriefing_note_version_revised.md | 🔍0文字 | 0 | 0 | 4 | 💬 確認推奨 |
| ai_summary_008_persian_gulf_range_fouler_note_version_revised.md | 📄3441文字 | 0 | 0 | 3 | 💬 確認推奨 |
| **合計 (12件)** | | **0** | **1** | **31** | |

---

## 詳細レポート

### ai_reading_001_composite-sketch_20240430.md

**判定: ⚠️ 要確認**

- File Name: `(不明)`
- PDF照合方法: File Name なし

- ⚠️ **[WARNING] File Name**  
  記事にFile Nameが記載されていません

---

### ai_reading_001_composite-sketch_20240430_note_version.md

**判定: 💬 確認推奨**

- File Name: `2024-04-30-composite-sketch.pdf`
- PDF照合方法: テキスト層なし（スキャン専用PDF）

- 💬 **[INFO] 英文引用照合**  
  「2024-04-30-composite-sketch.pdf」のテキスト層が取得できないため引用照合をスキップしました
  → *スキャン専用PDFの場合は目視確認が必要です*
- 💬 **[INFO] OCRパイプライン**  
  「2024-04-30-composite-sketch.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「2024-04-30-composite-sketch.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

### ai_reading_002_usper-statement_note_version.md

**判定: 💬 確認推奨**

- File Name: `usper-statement-redacted.pdf`
- PDF照合方法: テキスト層から抽出（7242文字）

- 💬 **[INFO] OCRパイプライン**  
  「usper-statement-redacted.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「usper-statement-redacted.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

### ai_reading_003_western_us_event_slides_note_version.md

**判定: 💬 確認推奨**

- File Name: `western_us_event_slides_5.08.2026.pdf`
- PDF照合方法: テキスト層から抽出（5777文字）

- 💬 **[INFO] OCRパイプライン**  
  「western_us_event_slides_5.08.2026.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「western_us_event_slides_5.08.2026.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

### ai_reading_004_apollo12_transcript_note_version.md

**判定: 💬 確認推奨**

- File Name: `nasa-uap-d1-apollo-12-transcript-1969.pdf`
- PDF照合方法: テキスト層から抽出（6173文字）

- 💬 **[INFO] OCRパイプライン**  
  「nasa-uap-d1-apollo-12-transcript-1969.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「nasa-uap-d1-apollo-12-transcript-1969.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

### ai_reading_005_apollo17_transcript_note_version.md

**判定: 💬 確認推奨**

- File Name: `nasa-uap-d2-apollo-17-transcript-1972.pdf`
- PDF照合方法: テキスト層から抽出（22061文字）

- 💬 **[INFO] OCRパイプライン**  
  「nasa-uap-d2-apollo-17-transcript-1972.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「nasa-uap-d2-apollo-17-transcript-1972.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

### ai_reading_006_apollo11_debriefing_note_version.md

**判定: 💬 確認推奨**

- File Name: `nasa-uap-d4-apollo-11-technical-crew-debriefing-1969.pdf`
- PDF照合方法: テキスト層なし（スキャン専用PDF）

- 💬 **[INFO] 英文引用照合**  
  「nasa-uap-d4-apollo-11-technical-crew-debriefing-1969.pdf」のテキスト層が取得できないため引用照合をスキップしました
  → *スキャン専用PDFの場合は目視確認が必要です*
- 💬 **[INFO] OCRパイプライン**  
  「nasa-uap-d4-apollo-11-technical-crew-debriefing-1969.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「nasa-uap-d4-apollo-11-technical-crew-debriefing-1969.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

### ai_reading_007_apollo17_technical_debriefing_note_version.md

**判定: 💬 確認推奨**

- File Name: `nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf`
- PDF照合方法: テキスト層なし（スキャン専用PDF）

- 💬 **[INFO] Incident Date**  
  年が一致しません（記事: 1972 / カタログ: 1973）（記事原文: 「1972年（アポロ17号ミッション）」 / カタログ原文: 「1973」）
  → *インシデント日と文書作成日が異なる場合があります。意図的なら注記を*
- 💬 **[INFO] 英文引用照合**  
  「nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf」のテキスト層が取得できないため引用照合をスキップしました
  → *スキャン専用PDFの場合は目視確認が必要です*
- 💬 **[INFO] OCRパイプライン**  
  「nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

### ai_reading_008_d38_middle_east_isr_note_version.md

**判定: 💬 確認推奨**

- File Name: `dow-uap-d38-range-fouler-debrief-middle-east-may-2020.pdf`
- PDF照合方法: テキスト層から抽出（3441文字）

- 💬 **[INFO] Incident Location**  
  カタログ「Middle East」と記事「北緯28°31′・東経49°52′付近（ペルシャ湾上）」に共通語なし
  → *翻訳・詳細化は問題ありませんが、矛盾がないか確認してください*
- 💬 **[INFO] OCRパイプライン**  
  「dow-uap-d38-range-fouler-debrief-middle-east-may-2020.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「dow-uap-d38-range-fouler-debrief-middle-east-may-2020.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

### ai_reading_009_d56_arabian_sea_note_version.md

**判定: 💬 確認推奨**

- File Name: `dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.pdf`
- PDF照合方法: テキスト層から抽出（3569文字）

- 💬 **[INFO] Incident Location**  
  カタログ「Arabian Sea」と記事「アラビア海北部（北緯21°44′付近）」に共通語なし
  → *翻訳・詳細化は問題ありませんが、矛盾がないか確認してください*
- 💬 **[INFO] OCRパイプライン**  
  「dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

### ai_summary_007_apollo17_debriefing_note_version_revised.md

**判定: 💬 確認推奨**

- File Name: `nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf`
- PDF照合方法: テキスト層なし（スキャン専用PDF）

- 💬 **[INFO] Incident Date**  
  年が一致しません（記事: 1972 / カタログ: 1973）（記事原文: 「1972年（アポロ17号ミッション）」 / カタログ原文: 「1973」）
  → *インシデント日と文書作成日が異なる場合があります。意図的なら注記を*
- 💬 **[INFO] 英文引用照合**  
  「nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf」のテキスト層が取得できないため引用照合をスキップしました
  → *スキャン専用PDFの場合は目視確認が必要です*
- 💬 **[INFO] OCRパイプライン**  
  「nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

### ai_summary_008_persian_gulf_range_fouler_note_version_revised.md

**判定: 💬 確認推奨**

- File Name: `dow-uap-d38-range-fouler-debrief-middle-east-may-2020.pdf`
- PDF照合方法: テキスト層から抽出（3441文字）

- 💬 **[INFO] Incident Location**  
  カタログ「Middle East」と記事「北緯28°31′・東経49°52′付近（ペルシャ湾上）」に共通語なし
  → *翻訳・詳細化は問題ありませんが、矛盾がないか確認してください*
- 💬 **[INFO] OCRパイプライン**  
  「dow-uap-d38-range-fouler-debrief-middle-east-may-2020.pdf」の OCR パイプライン実行記録が ocr_results.csv にありません
  → *個別処理（手動OCR）で対応した場合はこの警告を無視してください*
- 💬 **[INFO] テキスト層レポート**  
  「dow-uap-d38-range-fouler-debrief-middle-east-may-2020.pdf」の text_layer_report.csv エントリがありません
  → *個別処理の場合はこの警告を無視してください*

---

## チェック項目の説明

| チェック | 内容 | 判定レベル |
|---|---|---|
| File Name照合 | files_catalog.csv にファイル名が存在するか | WARNING |
| Agency | 記事とカタログのエージェンシーが一致するか | WARNING |
| Release Date | リリース日が一致するか（正規化比較） | WARNING |
| Incident Date | インシデント日が一致するか（年レベル比較） | INFO |
| Incident Location | カタログの場所が記事に含まれるか | INFO |
| URL整合性 | Source URL が war.gov/UFO か・元PDF URL にファイル名が含まれるか | WARNING |
| 英文引用照合 | 引用の冒頭部分がPDFテキストに存在するか（テキスト層のみ） | WARNING/INFO |
| 黒塗り開示 | 黒塗りの多いPDFで記事が黒塗りに言及しているか | WARNING |
| 黒塗り推測 | 黒塗り箇所の内容を推測していないか | INFO |
| 推測断定 | 引用外の本文で「〜に違いない」等の断定表現がないか | WARNING |
| OCRパイプライン | ocr_results.csv / text_layer_report.csv に記録があるか | INFO |

---

*このレポートは `scripts/verify_article_against_sources.py` によって自動生成されました。*
*完全な真偽判定ではなく、人間レビュー前の参考情報です。*