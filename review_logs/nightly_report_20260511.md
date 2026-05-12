# 夜間作業レポート 2026-05-11

---

## 今夜実施した作業

1. **Apollo 11 技術ブリーフィング（d4）の処理完了**
   - Tesseract OCR でページ5〜11を全文抽出
   - `note_drafts/ai_reading_006_apollo11_debriefing_note_version.md` を新規作成（101行）

2. **残存 breaking 候補 3件のテキスト層・コンテンツ調査**
   - `nasa-uap-d5-apollo-17-crew-debriefing-for-science-1973.pdf`：テキスト層あり（garbled）、コンテンツ確認 → UV天文学の科学ブリーフィングであり、UAP観察記録ではないと判明
   - `nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf`：スキャンのみ、Tesseract完全空振り（低解像度）→ 80dpiプレビュー画像で目視確認し内容を把握
   - `dow-uap-d6-mission-report-arabian-gulf-2020.pdf`：テキスト層あり（計202文字）→ 7ページのほぼ全てが 1.4(a) 黒塗り、実質コンテンツは1文のみ

3. **上位 detailed 候補のコンテンツサンプリング（8件）**
   - d28（東シナ海）、d38（中東）、d42（アラビア湾）、d44（アラビア海）、d50（INDOPACOM）、d52（不明）、d56（アラビア海）、d57（アデン湾）を確認
   - 各ファイルのテキスト品質・記事化可能性を評価

4. **集計・分析**
   - article_candidates.csv の全119件を集計
   - 未ドラフト候補の優先度評価
   - `metadata/next_article_candidates.csv` を新規作成
   - `review_logs/draft_inventory.md` を新規作成

---

## 生成・更新したファイル

| ファイル | 操作 |
|---|---|
| `note_drafts/ai_reading_006_apollo11_debriefing_note_version.md` | 新規作成 |
| `review_logs/nightly_report_20260511.md` | 新規作成（本ファイル） |
| `metadata/next_article_candidates.csv` | 新規作成 |
| `review_logs/draft_inventory.md` | 新規作成 |

---

## 重要な発見（要確認）

### 1. nasa-uap-d5 は UAP 資料ではない可能性が高い

`nasa-uap-d5-apollo-17-crew-debriefing-for-science-1973.pdf`
- breaking スコア60で、次の記事化候補として優先度が高かった
- 実際の内容：UV天文学の科学ブリーフィング。「HENRY（科学者）」が銀河のLyman-alpha水素放射線・コマ銀河団・銀河面外のUV放射について発表している
- UAP観察の記述は発見されなかった
- **推奨処置**：`recommended_lane` を `hold` に変更を検討。article_candidates.csv の再評価が必要

### 2. nasa-uap-d6 の OCR が Tesseract で完全失敗

`nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf`
- Tesseract PSM 3 / PSM 6 の両方で出力0文字
- 画像は正常（1700×2200px、明瞭）
- 目視では読める内容：
  - EVANS：「（月からの）帰還時の火球が弱まったあと、ランデブー窓から覗くと、トンネルの中にいるようで奥に火球が見えた」
  - CERNAN：「着水時に最も珍しかった光景は、CMPが窓から空母の上部構造を見て『ブリキ缶と一緒だ』と言ったこと」
  - SCHMITT：「暗順応中はほぼ常に光フラッシュが見えた。ALFMED実験でアイマスクをしている間だけ見えなかった」
- **推奨処置**：画像直読（Claude Vision）またはより高精度なOCR設定の試行（DPI向上・前処理）

### 3. dow-uap-d6 はほぼ全文黒塗り

`dow-uap-d6-mission-report-arabian-gulf-2020.pdf`
- 7ページ中、実質コンテンツは最終ページの1文のみ
- 内容：「AT 1246Z, [REDACTED] OBSERVED 1X PROB UAP IVO [coordinates]. NO MISSION IMPACT, CONTINUED ORIGINAL TASKING.」
- 単独記事としては情報量不足。他の Arabian Gulf 系文書と束ねる必要あり

---

## 記事化候補トップ10（次のアクション向け）

| 優先 | ファイル名 | ページ数 | テキスト層 | 推奨理由 |
|---|---|---|---|---|
| 1 | nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf | 2 | なし（スキャン） | Apollo 17シリーズ連続性、Evans火球記述、Schmitt ALFMED補足 |
| 2 | dow-uap-d28-mission-report-east-china-sea-2024.pdf | 6 | あり | AC-130がPGM投下中にUAPをセンサーで検出。「物体分離の可能性」言及あり |
| 3 | dow-uap-d38-range-fouler-debrief-middle-east-may-2020.pdf | 1 | あり | 白い物体が海面上で不規則運動、4倍ズームで追跡 |
| 4 | dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.pdf | 1 | あり | 3機の未確認飛行体（1機→3機）、アラビア海北部 |
| 5 | dow-uap-d52-email-correspondance-na-august-2024.pdf | 2 | あり | 楕円/オーブ型、2時間以上追跡、UNCLASS tearline |
| 6 | dow-uap-d20-mission-report-southern-united-states-2023.pdf | 6 | あり | F-16が「複数の可能性あるUAP」を観察、2023年 |
| 7 | dow-uap-d42-range-fouler-debrief-japan-2023.pdf | 1 | あり（要OCR改善） | ファイル名に「japan」含むが実際はアラビア湾の事案（注意書き必須） |
| 8 | dow-uap-d44-range-fouler-arabian-sea-october-2020.pdf | 1 | あり（要OCR改善） | Range Fouler形式、アラビア海 2020年10月 |
| 9 | dow-uap-d50-email-correspondence-indopacom-april-2025.pdf | 2 | あり | INDOPACOMエリア、分類レベル確認の内部通信 |
| 10 | nasa-uap-d5-apollo-17-crew-debriefing-for-science-1973.pdf | 3 | あり（garbled） | 注意：UAP記述なし・UV天文学記録。記事化前に内容再確認必須 |

---

## OCR失敗・注意ページの概要

| ファイル | 問題 | 詳細 |
|---|---|---|
| nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf | Tesseract完全空振り（0文字） | 1700×2200pxで画像は正常。理由不明。DPI調整・前処理が必要 |
| nasa-uap-d5-apollo-17-crew-debriefing-for-science-1973.pdf | テキスト層あるが文字化け | 元PDFのスキャン由来テキスト層が点・記号列に化けている。p.2-3は読めるが内容がUAP無関係 |
| dow-uap-d42-range-fouler-debrief-japan-2023.pdf | OCR文字化け多数 | テキスト層があるが特殊文字混入多数。内容の把握には影響なし（読めるレベル） |
| dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.pdf | テキスト層があるが一部崩れ | 本文フリーコメント部分は読めた。判断に影響なし |

---

## 全体統計サマリー

| 項目 | 値 |
|---|---|
| article_candidates.csv 総件数 | 119件 |
| breaking レーン | 9件 |
| detailed レーン | 74件 |
| hold レーン | 36件 |
| ドラフト作成済み（#001〜#006） | 6件 |
| 残存 breaking 未ドラフト | 3件（うち1件はUAP内容なしの可能性） |
| 1ページ候補（最短） | 34件 |
| 5〜10ページ候補 | 41件 |
| 21ページ以上（大型） | 23件 |
| raw_pdf 合計容量 | 2.3GB |

---

## 明日確認すべきこと

1. **`nasa-uap-d5` を `hold` に変更するか判断してほしい**
   本当にUAP記述がないかを人間が確認後、`article_candidates.csv` の `recommended_lane` を修正

2. **`nasa-uap-d6` のOCR失敗を解決するか決めてほしい**
   内容は目視で把握済み（2ページのみ）。OCR修正に時間をかけるか、画像読みで記事を書くか方針を決めてほしい

3. **記事#007 は `nasa-uap-d6` か `dow-uap-d28` か選んでほしい**
   - d6（NASA Apollo 17 技術ブリーフィング）：アポロシリーズ連続性あり、短くまとめやすい
   - d28（東シナ海ミッションレポート）：最も現代的・軍事的内容。読者層によって優先度が変わる

4. **note 連番のルールを固めてほしい**
   #001〜#006 まで進んだが、今後 detailed レーンの記事を出す場合、同じ連番を使うか別シリーズにするか

---

*生成日時：2026-05-11 夜間バッチ（Claude自動作業）*
*commit なし・削除なし・既存ドラフト変更なし*
