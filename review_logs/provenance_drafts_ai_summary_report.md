# プロベナンス一括検証レポート
生成日時: 2026-05-12 21:20
対象範囲: drafts_ai_summary

---

## リスクスコア定義

| レベル | 意味 | 対応方針 |
|---|---|---|
| 🔴 HIGH | ソースに存在しない技術用語・数値（AI ハルシネーションの疑い） | **公開停止 / 要修正** |
| 🟡 MEDIUM | OCR 誤読・略語不一致の可能性あり | 元 PDF 目視確認推奨 |
| 🟢 LOW | 翻訳者追加コンテキスト（地名等）または軽微な不一致 | 許容範囲（確認任意） |

---

## 全記事サマリー

| 記事ファイル | 元PDF | リスク | HIGH | MED | LOW | 判定 |
|---|---|---|---|---|---|---|
| `ai_summary_017_d42_range_fouler_japan_note_version.md` | `dow-uap-d42-range-fouler-debrief-japan-2023.pdf` | 🟡 MEDIUM | 0 | 2 | 0 | 🟡 MEDIUM |
| `ai_summary_029_d55_syria_2016_note_version.md` | `dow-uap-d55-mission-report-syria-november-2016.pdf` | 🟡 MEDIUM | 0 | 1 | 0 | 🟡 MEDIUM |
| `ai_summary_030_d61_persian_gulf_aug2020_note_version.md` | `dow-uap-d61-mission-report-persian-gulf-august-202` | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| `ai_summary_031_d62_hormuz_sep2020_note_version.md` | `dow-uap-d62-mission-report-strait-of-hormuz-septem` | 🟡 MEDIUM | 0 | 3 | 0 | 🟡 MEDIUM |
| `ai_summary_032_d33_greece_oct2023_note_version.md` | `dow-uap-d33-mission-report-greece-october-2023.pdf` | 🟢 LOW | 0 | 0 | 1 | ✅ OK |
| `ai_summary_033_d74_syria_nov2023_note_version.md` | `dow-uap-d74-mission-report-syria-november-2023.pdf` | 🟡 MEDIUM | 0 | 1 | 0 | 🟡 MEDIUM |
| `ai_summary_034_dos_d2_kazakhstan_1994_note_version.md` | `dos-uap-d2-cable-2-kazakhstan-january-1994.pdf` | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| `ai_summary_035_d8_djibouti_2025_note_version.md` | `dow-uap-d8-mission-report-djibouti-2025.pdf` | 🟡 MEDIUM | 0 | 1 | 1 | 🟡 MEDIUM |

**合計 8 件**: 🔴 HIGH=0  🟡 MEDIUM=5  🟢 LOW=3

---

## ✅ HIGH リスク記事なし

このバッチの全記事で HIGH リスクの候補は検出されませんでした。

## 🟡 MEDIUM リスク記事（OCR誤読等・確認推奨）

- **ai_summary_017_d42_range_fouler_japan_note_version.md**: `O-2`, `USCENTCOM MDR`
- **ai_summary_029_d55_syria_2016_note_version.md**: `USCENTCOM MDR`
- **ai_summary_031_d62_hormuz_sep2020_note_version.md**: `GENTEXT/OBSERVATION`, `ID330414`, `USCENTCOM MDR`
- **ai_summary_033_d74_syria_nov2023_note_version.md**: `CONSISTENTLY FOR AT LEAST`
- **ai_summary_035_d8_djibouti_2025_note_version.md**: `CSV`

---

*このレポートは `scripts/generate_provenance.py` によって自動生成されました。*
*HIGH リスクは「PDF に見当たらない」事実を示します。公開前に元 PDF を目視確認してください。*