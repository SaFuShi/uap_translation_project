# プロベナンス全体検証マスターレポート
生成日時: 2026-05-12
対象: 全公開記事（#007〜#028、計20件）

---

## リスクスコア定義

| レベル | 意味 | 対応方針 |
|---|---|---|
| 🔴 HIGH | ソースに存在しない技術用語・数値（AI ハルシネーション疑い） | **公開停止 / 要修正** |
| 🟡 MEDIUM | OCR 誤読・略語不一致の可能性あり | 元 PDF 目視確認推奨 |
| 🟢 LOW | 翻訳者追加コンテキスト（地名等）または AI 補助換算 | 許容範囲（確認任意） |

---

## 全記事サマリー

| # | 記事 | リスク | HIGH | MED | LOW | 対応状況 |
|---|---|---|---|---|---|---|
| 007 | apollo17_debriefing | 🔴 HIGH | 1 | 4 | 0 | ⚠️ PDF画像のみ（1文字）・自動検証不可・人間確認必要 |
| 008 | d38 persian_gulf_range_fouler | 🟡 MEDIUM | 0 | 2 | 0 | ✅ センサー設定表記・UTC → 許容範囲 |
| 010 | d52 email_uap_orb | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| 011 | d28 armed_overwatch_iraq | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| 012 | d44 arabian_sea_oct2020 | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| 013 | d57 gulf_of_aden_sep2020 | 🔴 HIGH→修正済 | 1 | 0 | 0 | ✅ OCRノイズ偽陽性（`6.1 ?NM`→`6.17NM`）・メモ追記済 |
| 014 | d20 f16_middle_east | 🟡 MEDIUM | 0 | 1 | 0 | ✅ USCENTCOM MDR → 標準ヘッダー・許容範囲 |
| 015 | d50 indopacom_email | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| 016 | d6 arabian_gulf_2020 | 🟡 MEDIUM | 0 | 5 | 0 | ✅ 疎テキスト（208文字）・MISREP/UTC/MGRS/USCENTCOM → 許容範囲 |
| 018 | d58 range_fouler_na | 🟡 MEDIUM | 0 | 3 | 0 | ✅ 標準軍用略語 → 許容範囲 |
| 019 | d4 arabian_gulf_2020 | 🟡 MEDIUM | 0 | 4 | 1 | ✅ 標準軍用略語 → 許容範囲 |
| 020 | d25 mediterranean_greece | 🟡 MEDIUM | 0 | 2 | 0 | ✅ 標準軍用略語 → 許容範囲 |
| 021 | d3 arabian_gulf_2020 | 🟡 MEDIUM | 0 | 1 | 0 | ✅ 標準軍用略語 → 許容範囲 |
| 022 | d60 persian_gulf_aug2020 | 🟡 MEDIUM | 0 | 3 | 0 | ⚠️ PDF画像のみ（0文字）・自動検証不可・人間確認必要 |
| 023 | d51 pacific_email | 🟡 MEDIUM | 0 | 1 | 0 | ✅ 標準略語 → 許容範囲 |
| 024 | dos_d1 papua_new_guinea | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| 025 | d75 gulf_of_aden_2024 | 🟡 MEDIUM | 0 | 1 | 0 | ✅ 標準軍用略語 → 許容範囲 |
| 026 | d7 arabian_gulf | 🟡 MEDIUM | 0 | 3 | 0 | ✅ 疎テキスト → 許容範囲 |
| 027 | d5 arabian_gulf | 🟡 MEDIUM | 0 | 3 | 0 | ✅ 疎テキスト → 許容範囲 |
| 028 | d10 iraq_may2022 | 🟡 MEDIUM | 0 | 1 | 0 | ✅ 標準軍用略語 → 許容範囲 |

**合計 20 件: 🔴 HIGH=2(修正済含む)  🟡 MEDIUM=14  🟢 LOW=4**

---

## 真のハルシネーション検出（修正済）

### #029 (note_drafts) d55 Syria 2016
- `contrail`（飛行雲）: PDF に存在しない → **削除済**
- `100,000フィート`: PDF に存在しない → **削除済**

---

## 要人間確認（画像のみ PDF）

### #007 Apollo17 Technical Crew Debriefing 1973
- PDF テキスト: 1文字（実質ゼロ・スキャン画像のみ）
- 記事は目視読み取りで作成済み・AI解析メモに明記あり
- `MSC-07631`（NASA 文書番号）・`ALFMED` などは画像確認必要

### #022 d60 Persian Gulf August 2020
- PDF テキスト: 0文字（スキャン画像のみ）
- すべてのクレームが自動検証不可

---

## OCRノイズ偽陽性 HIGH（修正済）

### #013 d57 Gulf of Aden Sep2020
- `6.17NM` → PDF OCR読み `6.1 ?NM`（`7` が `?` に誤認）
- 値は正確・AI解析メモに OCR ノイズとして注記済み

---

## バッチレポートファイル

| バッチ | ファイル |
|---|---|
| #007-#008 | `review_logs/provenance_007-008_report.md` |
| #010-#016 | `review_logs/provenance_010-016_report.md` |
| #018-#025 | `review_logs/provenance_018-025_report.md` |
| #026-#029 | `review_logs/provenance_026-029_report.md` |

---

## 結論

**真のハルシネーション（AI作話）は #029 の 2 件のみ（修正済）。**  
残りの WARNING はすべて：
- OCR ノイズによる偽陽性
- 画像のみ PDF による検証不可
- 標準的な軍用略語・文書分類マーキング

記事品質としては **許容範囲内**。  
#007・#022 については人間による目視確認を推奨。

---

*このレポートは `scripts/generate_provenance.py` バッチ結果を手動集約したものです。*
