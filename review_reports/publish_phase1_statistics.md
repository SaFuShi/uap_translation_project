# UAP翻訳プロジェクト Phase 1 公開統計
## 集計日：2026-05-15 ｜ #001〜#116 全記事化完了時点

---

## 1. ファイル・登録数サマリー

| 項目 | 件数 |
|---|---|
| raw_pdf/ 総PDF数 | 116件 |
| source_registry.csv 総登録件数 | 119件（重複エントリ含む） |
| うち通常記事（#001〜#116） | 116件 |
| うち重複エントリ（#069b） | 1件 |
| うち取り下げ重複（#036） | 1件 |
| raw_pdf/ 内 動画ファイル | 0件 |
| raw_pdf/ 内 その他ファイル | 0件（PNGサムネイル変換先ディレクトリのみ） |

---

## 2. 公開ステータス別件数

| ステータス | 件数 | 内容 |
|---|---|---|
| published | 108件 | note公開済み |
| draft | 7件 | 未公開保留中 |
| hold | 1件 | 公開保留（#017） |
| withdrawn_duplicate | 1件 | 重複取り下げ（#036） |
| duplicate_of_069 | 1件 | war.gov起因の重複（#069b） |
| **合計** | **118件** | （#069bを含む全エントリ） |

### 保留記事一覧（draft / hold）

| article_id | ファイル名 | ステータス |
|---|---|---|
| #001 | 2024-04-30-composite-sketch.pdf | draft |
| #002 | usper-statement-redacted.pdf | draft |
| #003 | western_us_event_slides_5.08.2026.pdf | draft |
| #004 | nasa-uap-d1-apollo-12-transcript-1969.pdf | draft |
| #005 | nasa-uap-d2-apollo-17-transcript-1972.pdf | draft |
| #017 | dow-uap-d42-range-fouler-debrief-japan-2023.pdf | hold |
| #041 | dow-uap-d23-mission-report-united-arab-emirates-october-2023.pdf | draft |
| #044 | dow-uap-d35-mission-report-greece-october-2023.pdf | draft |

---

## 3. 重複PDF詳細

### ケース1：#036（取り下げ済み重複）

- **ファイル名：** `dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.pdf`
- **status：** withdrawn_duplicate
- **SHA256：** `9127fb5a81efacf030df4dc6290d02bcdf4c8512cf1809b6eccfe6cf16a77f31`
- **状況：** #009 と同一PDF（SHA256一致）。#009 が正式記事として公開済み。#036 は取り下げ。

### ケース2：#069b（war.gov起因の重複）

- **ファイル名：** `59_214434_sp_16_[7.18.1963].pdf`
- **status：** duplicate_of_069
- **MD5：** `6039f96c52e566b69f3a3d774b7653fa`（MD5）
- **状況：** war.gov がファイル名を変えて同一PDFを別URLで公開していた事例。`59_214434_sp_16_7.18.1963.pdf`（#069, published）と同一内容。ブラケットの有無のみ異なる。

---

## 4. PDFタイプ別件数

ファイル名・remarks・ドラフトパスから分類（#001〜#116、重複除く116件）

| タイプ | 定義 | 件数 |
|---|---|---|
| TYPE-A | IRカメラ映像の静止フレーム | 2件 |
| TYPE-B | 一部リダクション（黒塗り）あり | 8件 |
| TYPE-C | 画像・スライド資料 | 1件 |
| TYPE-D | MISREP（任務報告書）形式 | 37件 |
| TYPE-E | 歴史的背景文書・書簡集・報告書 | 20件 |
| TYPE-F | 外交電報・email通信文 | 5件 |
| TYPE-G | FBI断片資料（写真・捜査ファイル） | 43件 |
| **合計** | | **116件** |

**注記：** TYPE分類は2026-05-15時点で `draft_type_classification_v1.md` として正式化。それ以前の記事（#001〜#090前後）はファイル名からの推定を含む。

---

## 5. 発行機関系統別件数

| 系統 | 代表ファイル接頭辞 | 件数 |
|---|---|---|
| FBI系 | `65_*`, `fbi-photo-*`, `59_*`, `serial-*` | 43件 |
| DoW / DoD 任務報告書系 | `dow-uap-d*`, `38_*`, `342_*`, `255_*` | 51件 |
| NASA系 | `nasa-uap-d*` | 6件 |
| 国務省（DoS）系 | `dos-uap-d*` | 2件 |
| AARO関連 | `059uap*` | 3件 |
| その他 | — | 11件 |
| **合計** | | **116件** |

---

## 6. OCR処理状況（テキスト抽出可否）

| 区分 | 件数 | 主な対象 |
|---|---|---|
| OCR困難（スキャン画像PDF・0文字） | 約55件以上 | #101〜#116（全16件）、FBI捜査ファイル 62-HQ-83894 シリーズ、FBI写真分析シリーズ等 |
| テキスト層あり（OCR可能） | 約40件以上 | DoW MISREP（dow-uap-d* 多数）、NASA転写録 |
| 未確認 | 残余 | 初期登録時に記録なし |

**注記：** remarks に「OCR不可」「スキャン画像PDF」「有意なテキスト抽出が困難」の記載がある記事は少なくとも37件。これは主として後期追加分（#094以降）。早期登録分は個別確認が必要。

---

## 7. 時系列 記事追加推移

| 追加バッチ | 対象 | 主な内容 |
|---|---|---|
| 初期〜#070 | 70件 | DoW MISREP、NASA転写録、FBI写真初期、DoS電報 |
| #071〜#090 | 20件 | FBI写真分析シリーズ b3〜b22（IRカメラ・FMV） |
| #091〜#100 | 10件 | FBI写真 b23/b24、DoW MISREP d32（シリア）、FBI 62-HQ-83894 Section 3〜9 |
| #101〜#105 | 5件 | DoW 歴史的文書（飛行円盤・フーファイター・1944〜1955年） |
| #106〜#116 | 11件 | FBI 62-HQ-83894 Section 10 / Serial / Sub A |

---

## 8. まとめ記事用 統計サマリー（短縮版）

```
【UAP翻訳プロジェクト Phase 1 完了統計】

公開済み記事：108本
記事化対象PDF：116件（war.gov公開の機密解除文書）
発行機関：FBI / 国防総省（DoD/DoW） / NASA / 国務省（DoS）/ AARO

記事タイプ内訳：
  任務報告書（MISREP）系：37件
  FBI捜査・写真資料系：43件
  歴史的文書・書簡集：20件
  外交電報・通信文：5件
  その他（リダクション文書・スライド等）：11件

スキャン画像PDF（テキスト抽出不可）：55件以上
対象年代：1944年〜2026年

重複PDF：2件検出・処理済み
  - war.gov内部の別URL重複（#069b）
  - 登録ミスによる取り下げ（#036）

プロジェクト期間：2026年初頭〜2026-05-15
```

---

## 9. 参照ファイル

| ファイル | 内容 |
|---|---|
| `review_logs/source_registry.csv` | 全記事の登録・公開管理台帳 |
| `docs/draft_type_classification_v1.md` | PDFタイプ分類仕様 |
| `docs/audit_checklist_v1.md` | レビューチェックリスト v1.9 |
| `docs/review_standard_v1.md` | レビュー基準・用語標準補足一覧 |
| `logs/notebooklm/2026-05-15_uap_articles_071_116_publish_log.md` | 今回作業の詳細ログ |

---

*集計日：2026-05-15*
*対象commit：2cb1e1f（記事公開完了）/ 7628693（NotebookLMログ追加）*
