# プロベナンス一括検証レポート
生成日時: 2026-05-12 21:16
対象範囲: 010-016

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
| `ai_summary_010_d52_email_uap_orb_note_version.md` | `dow-uap-d52-email-correspondance-na-august-2024.pd` | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| `ai_summary_011_d28_armed_overwatch_iraq_note_version.md` | `dow-uap-d28-mission-report-east-china-sea-2024.pdf` | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| `ai_summary_012_d44_arabian_sea_oct2020_note_version.md` | `dow-uap-d44-range-fouler-arabian-sea-october-2020.` | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| `ai_summary_013_d57_gulf_of_aden_sep2020_note_version.md` | `dow-uap-d57-mission-report-gulf-of-aden-september-` | 🔴 HIGH | 1 | 0 | 0 | 🔴 HIGH |
| `ai_summary_014_d20_f16_middle_east_note_version.md` | `dow-uap-d20-mission-report-southern-united-states-` | 🟡 MEDIUM | 0 | 1 | 0 | 🟡 MEDIUM |
| `ai_summary_015_d50_indopacom_email_note_version.md` | `dow-uap-d50-email-correspondence-indopacom-april-2` | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| `ai_summary_016_d6_arabian_gulf_2020_note_version.md` | `dow-uap-d6-mission-report-arabian-gulf-2020.pdf` | 🟡 MEDIUM | 0 | 5 | 0 | 🟡 MEDIUM |

**合計 7 件**: 🔴 HIGH=1  🟡 MEDIUM=2  🟢 LOW=4

---

## 🔴 HIGH リスク記事 詳細（要修正）

### ai_summary_013_d57_gulf_of_aden_sep2020_note_version.md

- **元PDF**: `dow-uap-d57-mission-report-gulf-of-aden-september-2020.pdf`
- **PDF文字数**: 3,175

| 検索語 | 種別 | 記事での出現 | コンテキスト（前後） |
|---|---|---|---|
| `6.17` | distance | `6.17NM` | `...触中に数回の急激な方向転換を行った。センサーはスラントレンジ6.17NM、グラウンドレンジ8.81KMに照準していた。I...` |

→ 個別レポート: `provenance/dow-uap-d57-mission-report-gulf-of-aden-september-2020_check.md`

## 🟡 MEDIUM リスク記事（OCR誤読等・確認推奨）

- **ai_summary_014_d20_f16_middle_east_note_version.md**: `USCENTCOM MDR`
- **ai_summary_016_d6_arabian_gulf_2020_note_version.md**: `MISREP`, `UTC`, `MGRS`, `USCENTCOM`, `MISREP`

---

*このレポートは `scripts/generate_provenance.py` によって自動生成されました。*
*HIGH リスクは「PDF に見当たらない」事実を示します。公開前に元 PDF を目視確認してください。*