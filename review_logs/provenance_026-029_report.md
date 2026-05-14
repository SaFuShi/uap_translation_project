# プロベナンス一括検証レポート
生成日時: 2026-05-12 21:12
対象範囲: #026-#029

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
| `ai_summary_026_d7_arabian_gulf_note_version.md` | `dow-uap-d7-mission-report-arabian-gulf-2020.pdf` | 🟡 MEDIUM | 0 | 3 | 0 | 🟡 MEDIUM |
| `ai_summary_027_d5_arabian_gulf_note_version.md` | `dow-uap-d5-mission-report-arabian-gulf-2020.pdf` | 🟡 MEDIUM | 0 | 3 | 0 | 🟡 MEDIUM |
| `ai_summary_028_d10_iraq_may2022_note_version.md` | `dow-uap-d10-mission-report-middle-east-may-2022.pd` | 🟡 MEDIUM | 0 | 1 | 0 | 🟡 MEDIUM |
| `ai_summary_029_d55_syria_2016_note_version.md` | `dow-uap-d55-mission-report-syria-november-2016.pdf` | 🟡 MEDIUM | 0 | 1 | 0 | 🟡 MEDIUM |

**合計 4 件**: 🔴 HIGH=0  🟡 MEDIUM=4  🟢 LOW=0

---

## ✅ HIGH リスク記事なし

このバッチの全記事で HIGH リスクの候補は検出されませんでした。

## 🟡 MEDIUM リスク記事（OCR誤読等・確認推奨）

- **ai_summary_026_d7_arabian_gulf_note_version.md**: `MISREP`, `MISREP`, `USCENTCOM`
- **ai_summary_027_d5_arabian_gulf_note_version.md**: `SECRET`, `REL TO USA`, `CSV`
- **ai_summary_028_d10_iraq_may2022_note_version.md**: `POSSIBLE MISSILE`
- **ai_summary_029_d55_syria_2016_note_version.md**: `USCENTCOM MDR`

---

*このレポートは `scripts/generate_provenance.py` によって自動生成されました。*
*HIGH リスクは「PDF に見当たらない」事実を示します。公開前に元 PDF を目視確認してください。*