# ドラフト生成レポート #101-#116（最終残余分）

**作成日:** 2026-05-15
**適用仕様:** docs/draft_type_classification_v1.md
**ステータス:** 全16件生成完了

---

## 対象記事一覧・PDFタイプ

| article_id | pdf_file_name | TYPE | 生成ドラフト |
|---|---|---|---|
| #101 | 18_100754_ general 1946-7_vol_2.pdf | TYPE-E | ai_summary_101_dow_18_100754_general_1946_1947_vol2_note_version.md |
| #102 | 18_6369445_general_1948_vol_1.pdf | TYPE-E | ai_summary_102_dow_18_6369445_general_1948_vol1_note_version.md |
| #103 | 331_120752_numeric_files_1944–1945_37153_german_armament_equipment_documents.pdf | TYPE-E | ai_summary_103_dow_331_shaef_foofighters_germany_1944_1945_note_version.md |
| #104 | 341_110448_records_relating_to_the_collection_and_dissemination_of_intelligence_1948-1955-ts_cont_no.2_2-5300-2-5399.pdf | TYPE-E | ai_summary_104_dow_341_af_intel_ufo_netherlands_1948_note_version.md |
| #105 | 341_110677_numerical_file_5-2500.pdf | TYPE-E | ai_summary_105_dow_341_air_intel_ussr_aircraft_1955_note_version.md |
| #106 | 65_hs1-101634279_100-de-18221_serial_844.pdf | TYPE-G | ai_summary_106_fbi_100de18221_serial844_detroit_1958_note_version.md |
| #107 | 65_hs1-101634279_100-de-26505.pdf | TYPE-G | ai_summary_107_fbi_100de26505_krasuski_germany_1944_note_version.md |
| #108 | 65_hs1-834228961_62-hq-83894_section_10.pdf | TYPE-G | ai_summary_108_fbi_hq_62hq83894_section10_note_version.md |
| #109 | 65_hs1-834228961_62-hq-83894_serial_130.pdf | TYPE-G | ai_summary_109_fbi_hq_62hq83894_serial130_note_version.md |
| #110 | 65_hs1-834228961_62-hq-83894_serial_153.pdf | TYPE-G | ai_summary_110_fbi_hq_62hq83894_serial153_note_version.md |
| #111 | 65_hs1-834228961_62-hq-83894_serial_164.pdf | TYPE-G | ai_summary_111_fbi_hq_62hq83894_serial164_note_version.md |
| #112 | 65_hs1-834228961_62-hq-83894_serial_220.pdf | TYPE-G | ai_summary_112_fbi_hq_62hq83894_serial220_note_version.md |
| #113 | 65_hs1-834228961_62-hq-83894_serial_403.pdf | TYPE-G | ai_summary_113_fbi_hq_62hq83894_serial403_note_version.md |
| #114 | 65_hs1-834228961_62-hq-83894_serial_438.pdf | TYPE-G | ai_summary_114_fbi_hq_62hq83894_serial438_note_version.md |
| #115 | 65_hs1-834228961_62-hq-83894_serial_449.pdf | TYPE-G | ai_summary_115_fbi_hq_62hq83894_serial449_note_version.md |
| #116 | 65_hs1-834228961_62-hq-83894_sub_a.pdf | TYPE-G | ai_summary_116_fbi_hq_62hq83894_suba_note_version.md |

---

## 保留記事

なし

---

## TYPE分類詳細

### TYPE-E (#101〜#105): Department of War 歴史的文書群

分類根拠:
- OCR不可（全0文字・スキャン画像PDF）
- 歴史的情報報告・書簡集（飛行円盤・フーファイター・UFO関連）
- Department of War（米陸軍省・当時）発行
- MISREP形式でない、FBI文書でない、外交電報でない

個別注意事項:
- #101/102: 「Air Materiel Command（空材本部）」への言及はwar.gov説明文のみ。本文確認不可。
- #103: 「フーファイター」「SHAEF」はwar.gov説明文由来。「foofighters」の定義は外部知識として補足しない。
- #104/105: 「TS」（Top Secret）がファイル名に含まれるが、現在の機密指定は不明。断定しない。

### TYPE-G (#106〜#116): FBI断片資料群

**#106/107（100-DE-* シリーズ）:**
- 62-HQ-83894とは別のFBIケースファイル番号（100-DE-18221、100-DE-26505）
- war.gov説明文に具体的な目撃内容・証言者情報が記載されているため、TYPE-G固有テンプレートを使用
- #107はリダクションあり（war.gov情報より）

**#108（Section 10）:**
- 以前「184ページ・OCR不可確認済み」として保留していたもの
- 既存 #094〜#100（Section 3〜9）と同形式で生成

**#109〜#115（Serial NNN）:**
- 62-HQ-83894のシリアル番号単位のファイル
- war.gov説明文はシリーズ共通記述（個別シリアルの内容は不明）
- シリアル番号のシリーズ内位置づけは本文から確認できないため断定しない

**#116（Sub A）:**
- 62-HQ-83894のサブファイルA
- シリーズ内での役割は不明。「SUB_A」をそのまま使用。

---

## 適用したルール

- 「ファイル名以外の情報源がない」表現を使用しない → 「ファイル名およびwar.gov公開説明文から確認できる情報」を使用
- OCR不可 → 「有意なテキスト抽出が困難」と表現
- FBI 62-HQ-83894シリーズ → 「FBI本部UFO捜査ファイル」に統一
- war.gov説明文はシリーズ共通記述である旨を明記

---

## 注意点

- TYPE-E 記事には「本資料はUAP目撃事案の報告書ではありません」を付与していない（これらの文書はUAP/飛行円盤関連文書であるため）
- source_registry.csvのhashフィールドにはMD5を記録（SHA256ではない）。（MD5）注記付き
- #103ファイル名のダッシュ記号（U+2013）に注意。通常のハイフン（-）と異なる
- raw_pdf/ に残っている `png_trasformation` はディレクトリであり、PDF対象外

---

## source_registry #101-#116 登録内容

- status: draft（全16件）
- note_url: 空欄
- published_date: 空欄
- created_date: 2026-05-15

---

*作成: 2026-05-15*
*生成数: 16件（TYPE-E×5、TYPE-G×11）*
*これで raw_pdf/ 内の全PDFの記事化が完了（重複1件 #069b を除く）*
