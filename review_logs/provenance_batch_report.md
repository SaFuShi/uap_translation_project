# プロベナンス一括検証レポート
生成日時: 2026-05-13 20:29

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
| `ai_summary_041_d23_uae_oct2023_note_version.md` | `dow-uap-d23-mission-report-united-arab-emirates-oc` | 🟡 MEDIUM | 0 | 5 | 1 | 🟡 MEDIUM |
| `ai_summary_042_d27_uae_oct2023_note_version.md` | `dow-uap-d27-mission-report-united-arab-emirates-oc` | 🟡 MEDIUM | 0 | 4 | 0 | 🟡 MEDIUM |
| `ai_summary_043_d32_syria_oct2024_note_version.md` | `dow-uap-d32-mission-report,-syria-october-2024.pdf` | 🟡 MEDIUM | 0 | 2 | 0 | 🟡 MEDIUM |
| `ai_summary_044_d35_greece_oct2023_note_version.md` | `dow-uap-d35-mission-report-greece-october-2023.pdf` | 🟡 MEDIUM | 0 | 4 | 0 | 🟡 MEDIUM |
| `ai_summary_045_d54_mediterranean_na_note_version.md` | `dow-uap-d54-mission-report-mediterranean-sea-na.pd` | 🟡 MEDIUM | 0 | 2 | 0 | 🟡 MEDIUM |
| `ai_summary_046_d63_hormuz_oct2020_note_version.md` | `dow-uap-d63-mission-report-strait-of-hormuz-octobe` | 🔴 HIGH | 1 | 2 | 0 | 🔴 HIGH |
| `ai_summary_047_d64_iran_nov2020_note_version.md` | `dow-uap-d64-mission-report-iran-november-2020.pdf` | 🔴 HIGH | 2 | 12 | 0 | 🔴 HIGH |
| `ai_summary_048_d65_persian_gulf_jul2020_note_version.md` | `dow-uap-d65-mission-report-persian-gulf-july-2020.` | 🔴 HIGH | 1 | 2 | 0 | 🔴 HIGH |
| `ai_summary_049_d48_rocket_failure_1996_note_version.md` | `dow-uap-d48-report-september-1996.pdf` | 🟡 MEDIUM | 0 | 2 | 0 | 🟡 MEDIUM |
| `ai_summary_050_d49_vandenberg_launch_2000_note_version.md` | `dow-uap-d49-launch-summary-february-2000.pdf` | 🟡 MEDIUM | 0 | 1 | 0 | 🟡 MEDIUM |

**合計 10 件**: 🔴 HIGH=3  🟡 MEDIUM=7  🟢 LOW=0

---

## 🔴 HIGH リスク記事 詳細（要修正）

### ai_summary_046_d63_hormuz_oct2020_note_version.md

- **元PDF**: `dow-uap-d63-mission-report-strait-of-hormuz-october-2020.pdf`
- **PDF文字数**: 7

| 検索語 | 種別 | 記事での出現 | コンテキスト（前後） |
|---|---|---|---|
| `Strait of Hormuz` | paren_english | `（Strait of Hormuz）` | `...種別**：ミッションレポート（MISREP） - **推定地域**：ホルムズ海峡（Strait of Hormuz） -...` |

→ 個別レポート: `provenance/dow-uap-d63-mission-report-strait-of-hormuz-october-2020_check.md`

### ai_summary_047_d64_iran_nov2020_note_version.md

- **元PDF**: `dow-uap-d64-mission-report-iran-november-2020.pdf`
- **PDF文字数**: 8,534

| 検索語 | 種別 | 記事での出現 | コンテキスト（前後） |
|---|---|---|---|
| `For Official Use Only` | paren_english | `（For Official Use Only）` | `...O（米国防総省のUAP調査組織）への公開が承認されました。なお本文書にはFOUO（For Official Use On...` |
| `STANDARD RESPONSE 1` | paren_english | `（STANDARD RESPONSE 1）` | `...イラン防空軍による GUARD 周波数での呼びかけ - 乗員の応答：標準的な応答（STANDARD RESPONSE 1...` |

→ 個別レポート: `provenance/dow-uap-d64-mission-report-iran-november-2020_check.md`

### ai_summary_048_d65_persian_gulf_jul2020_note_version.md

- **元PDF**: `dow-uap-d65-mission-report-persian-gulf-july-2020.pdf`
- **PDF文字数**: 7

| 検索語 | 種別 | 記事での出現 | コンテキスト（前後） |
|---|---|---|---|
| `Persian Gulf` | paren_english | `（Persian Gulf）` | `...務種別**：ミッションレポート（MISREP） - **推定地域**：ペルシャ湾（Persian Gulf） - **推...` |

→ 個別レポート: `provenance/dow-uap-d65-mission-report-persian-gulf-july-2020_check.md`

## 🟡 MEDIUM リスク記事（OCR誤読等・確認推奨）

- **ai_summary_041_d23_uae_oct2023_note_version.md**: `UAE`, `MGRS`, `MDR`, `SECRET`, `USCENTCOM MDR`
- **ai_summary_042_d27_uae_oct2023_note_version.md**: `UAE`, `INHERENT RESOLVE`, `FOREIGN NATIONALS`, `REL TO FVEY`
- **ai_summary_043_d32_syria_oct2024_note_version.md**: `MGRS`, `FLASHED ACROSS FMV CAMERA`
- **ai_summary_044_d35_greece_oct2023_note_version.md**: `FLEW STRAIGHT ABOVE THE OCEAN TOWARDS LAND`, `MGRS`, `FLEW STRAIGHT ABOVE THE`, `SPOTTED`
- **ai_summary_045_d54_mediterranean_na_note_version.md**: `TRIANGULAR AND METALLIC`, `TRIANGULAR AND METALLIC`
- **ai_summary_049_d48_rocket_failure_1996_note_version.md**: `F04703-91-C-0112`, `AARO`
- **ai_summary_050_d49_vandenberg_launch_2000_note_version.md**: `GOV`

---

*このレポートは `scripts/generate_provenance.py` によって自動生成されました。*
*HIGH リスクは「PDF に見当たらない」事実を示します。公開前に元 PDF を目視確認してください。*