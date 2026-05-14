# プロベナンス一括検証レポート
生成日時: 2026-05-12 21:13
対象範囲: #018-#025

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
| `ai_summary_018_d58_range_fouler_na_oct2020_note_version.md` | `dow-uap-d58-range-fouler-debrief-na-october-2020.p` | 🟡 MEDIUM | 0 | 3 | 0 | 🟡 MEDIUM |
| `ai_summary_019_d4_arabian_gulf_2020_note_version.md` | `dow-uap-d4-mission-report-arabian-gulf-2020.pdf` | 🟡 MEDIUM | 0 | 4 | 1 | 🟡 MEDIUM |
| `ai_summary_020_d25_mediterranean_greece_2024_note_version.md` | `dow-uap-d25-mission-report-greece-january-2024.pdf` | 🟡 MEDIUM | 0 | 2 | 0 | 🟡 MEDIUM |
| `ai_summary_021_d3_arabian_gulf_2020_note_version.md` | `dow-uap-d3-mission-report-arabian-gulf-2020.pdf` | 🟡 MEDIUM | 0 | 1 | 0 | 🟡 MEDIUM |
| `ai_summary_022_d60_persian_gulf_aug2020_note_version.md` | `dow-uap-d60-mission-report-persian-gulf-august-202` | 🟡 MEDIUM | 0 | 3 | 0 | 🟡 MEDIUM |
| `ai_summary_023_d51_pacific_email_2023_note_version.md` | `dow-uap-d51-email-correspondence-pacific-time-zone` | 🟡 MEDIUM | 0 | 1 | 0 | 🟡 MEDIUM |
| `ai_summary_024_dos_d1_papua_new_guinea_1985_note_version.md` | `dos-uap-d1-cable-1-papua-new-guinea-january-1985.p` | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| `ai_summary_025_d75_gulf_of_aden_2024_note_version.md` | `dow-uap-d75-mission-report-gulf-of-aden-july-2024.` | 🟡 MEDIUM | 0 | 1 | 0 | 🟡 MEDIUM |

**合計 8 件**: 🔴 HIGH=0  🟡 MEDIUM=7  🟢 LOW=1

---

## ✅ HIGH リスク記事なし

このバッチの全記事で HIGH リスクの候補は検出されませんでした。

## 🟡 MEDIUM リスク記事（OCR誤読等・確認推奨）

- **ai_summary_018_d58_range_fouler_na_oct2020_note_version.md**: `Range Fouler Debrief Form`, `O-3`, `USCENTCOM MDR`
- **ai_summary_019_d4_arabian_gulf_2020_note_version.md**: `MISREP`, `UTC`, `MGRS`, `MISREP`
- **ai_summary_020_d25_mediterranean_greece_2024_note_version.md**: `MGRS`, `NON-MANEUVERABLE`
- **ai_summary_021_d3_arabian_gulf_2020_note_version.md**: `UTC`
- **ai_summary_022_d60_persian_gulf_aug2020_note_version.md**: `MISREP`, `WAR`, `GOV`
- **ai_summary_023_d51_pacific_email_2023_note_version.md**: `Intelligence Information Report`
- **ai_summary_025_d75_gulf_of_aden_2024_note_version.md**: `MGRS`

---

*このレポートは `scripts/generate_provenance.py` によって自動生成されました。*
*HIGH リスクは「PDF に見当たらない」事実を示します。公開前に元 PDF を目視確認してください。*