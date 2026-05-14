# プロベナンス一括検証レポート
生成日時: 2026-05-12 21:16
対象範囲: 007-008

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
| `ai_summary_007_apollo17_debriefing_note_version_revised.md` | `nasa-uap-d6-apollo-17-technical-crew-debriefing-19` | 🔴 HIGH | 1 | 4 | 0 | 🔴 HIGH |
| `ai_summary_008_persian_gulf_range_fouler_note_version_revised.md` | `dow-uap-d38-range-fouler-debrief-middle-east-may-2` | 🟡 MEDIUM | 0 | 2 | 0 | 🟡 MEDIUM |

**合計 2 件**: 🔴 HIGH=1  🟡 MEDIUM=1  🟢 LOW=0

---

## 🔴 HIGH リスク記事 詳細（要修正）

### ai_summary_007_apollo17_debriefing_note_version_revised.md

- **元PDF**: `nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf`
- **PDF文字数**: 1

| 検索語 | 種別 | 記事での出現 | コンテキスト（前後） |
|---|---|---|---|
| `MSC-07631` | paren_english | `（MSC-07631）` | `...ract OCR出力0文字のため目視読み取りで内容把握・CONFIDENTIAL（MSC-07631）・Training...` |

→ 個別レポート: `provenance/nasa-uap-d6-apollo-17-technical-crew-debriefing-1973_check.md`

## 🟡 MEDIUM リスク記事（OCR誤読等・確認推奨）

- **ai_summary_008_persian_gulf_range_fouler_note_version_revised.md**: `UL TN / Black Hot / Linear`, `UTC`

---

*このレポートは `scripts/generate_provenance.py` によって自動生成されました。*
*HIGH リスクは「PDF に見当たらない」事実を示します。公開前に元 PDF を目視確認してください。*