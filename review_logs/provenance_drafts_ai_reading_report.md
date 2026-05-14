# プロベナンス一括検証レポート
生成日時: 2026-05-12 21:20
対象範囲: drafts_ai_reading

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
| `ai_reading_001_composite-sketch_20240430_note_version.md` | `2024-04-30-composite-sketch.pdf` | 🟡 MEDIUM | 0 | 1 | 0 | 🟡 MEDIUM |
| `ai_reading_002_usper-statement_note_version.md` | `usper-statement-redacted.pdf` | 🔴 HIGH | 3 | 1 | 0 | 🔴 HIGH |
| `ai_reading_003_western_us_event_slides_note_version.md` | `western_us_event_slides_5.08.2026.pdf` | 🔴 HIGH | 1 | 0 | 0 | 🔴 HIGH |
| `ai_reading_004_apollo12_transcript_note_version.md` | `nasa-uap-d1-apollo-12-transcript-1969.pdf` | 🟢 LOW | 0 | 0 | 0 | ✅ OK |
| `ai_reading_005_apollo17_transcript_note_version.md` | `nasa-uap-d2-apollo-17-transcript-1972.pdf` | 🟢 LOW | 0 | 0 | 0 | ✅ OK |

**合計 5 件**: 🔴 HIGH=2  🟡 MEDIUM=1  🟢 LOW=2

---

## 🔴 HIGH リスク記事 詳細（要修正）

### ai_reading_002_usper-statement_note_version.md

- **元PDF**: `usper-statement-redacted.pdf`
- **PDF文字数**: 7,242

| 検索語 | 種別 | 記事での出現 | コンテキスト（前後） |
|---|---|---|---|
| `10` | altitude | `10フィート` | `...上に接近** 文書の記述によれば、発光体がヘリコプターから「10フィート以内（約3メートル）」まで接近した、とLP/OP...` |
| `90` | duration | `90分間` | `...返す現象（午後10時27分〜11時57分）**  その後、約90分間にわたり複数回の目撃が連続して記録されています。  ...` |
| `US Person` | paren_english | `（US Person）` | `...と明記されています。ヘリコプターに同乗し、肉眼で直接目撃しています。「USPER（US Person）」とは米国政府が自...` |

→ 個別レポート: `provenance/usper-statement-redacted_check.md`

### ai_reading_003_western_us_event_slides_note_version.md

- **元PDF**: `western_us_event_slides_5.08.2026.pdf`
- **PDF文字数**: 5,777

| 検索語 | 種別 | 記事での出現 | コンテキスト（前後） |
|---|---|---|---|
| `45` | altitude | `45メートル` | `...トで物体を再探索した際、「ある地点でビームが遠くまで届かず約45メートル先で止まったが、その後は再び遠くまで届いた」との...` |

→ 個別レポート: `provenance/western_us_event_slides_5.08.2026_check.md`

## 🟡 MEDIUM リスク記事（OCR誤読等・確認推奨）

- **ai_reading_001_composite-sketch_20240430_note_version.md**: `WAR`

---

*このレポートは `scripts/generate_provenance.py` によって自動生成されました。*
*HIGH リスクは「PDF に見当たらない」事実を示します。公開前に元 PDF を目視確認してください。*