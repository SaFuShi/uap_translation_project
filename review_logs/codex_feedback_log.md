# Codex Feedback Log

**制定日**: 2026-05-13  
**管理**: `review_logs/codex_feedback_log.md`

---

## 記録目的

Codexが出したWARN/BLOCK/UNVERIFIABLEに対し、人間＋ChatGPTがどう判断したかを記録する。  
このログは、今後のCodex監査精度改善・`docs/review_standard_v1.md` 更新・`docs/audit_checklist_v1.md` 更新に使う。

---

## 記録フォーマット

```
### [YYYYMMDD-NNN] Article ID: #XXX — [Finding の短い見出し]

#### Article ID
#XXX

#### Codex Finding
Codexが指摘した内容を具体的に記述する

#### Codex Severity
WARN / BLOCK / UNVERIFIABLE

#### Human Decision
Accepted / Rejected / Partially Accepted / Deferred

#### Reason
採用・却下・保留の理由。なぜその判断をしたかを残す。

#### Rule Update Needed
Yes / No

#### Suggested Rule Update
（Rule Update Needed が Yes の場合）audit_checklist または review_standard に反映する文案

#### Follow-up Owner
Claude Code / Codex / Human / ChatGPT

#### Status
Open / Reflected / Closed
```

---

## ログ一覧（最新順）

---

### [20260514-007] Article ID: #091以降 — 軽量レビュー方式へ移行

#### Article ID
#091以降

#### Codex Finding
（該当なし。人間からのレビュー出力方式更新として記録）

#### Codex Severity
N/A（レビュー運用ルール）

#### Human Decision
Accepted

#### Reason
#071〜#090までの画像連番記事レビューで、同種指摘の長文反復が増えた。#091以降は人間レビュー負荷を下げるため、PASSは1行、WARNは記事番号・問題種別・一言、BLOCKのみ詳細出力とする。既知ルール違反はコード単位で集約し、全文レビューや修正不要箇所説明は行わない。

#### Rule Update Needed
Yes

#### Suggested Rule Update
`docs/review_standard_v1.md` と `docs/audit_checklist_v1.md` に「#091以降：軽量レビュー方式」を追加。OCR不可記事はファイル名外情報・Record Group断定・歴史背景混入・系列構成断定を重点確認。画像記事は EO/IR断定・追跡対象・捕捉・ロック・軍用IR を重点確認する。

#### Follow-up Owner
Codex（#091以降のレビューで軽量レビュー方式を適用）

#### Status
Reflected

---

### [20260514-006] Article ID: 今後の Codexレビュー全体 — OCR不可・画像記事・note投稿互換・反復違反の監査強化

#### Article ID
今後の Codexレビュー全体

#### Codex Finding
（該当なし。人間からのレビュー方針更新として記録）

#### Codex Severity
N/A（新規レビュー運用ルール）

#### Human Decision
Accepted

#### Reason
OCR不可記事でファイル名以外の事実・外部背景・シリーズ推定が混入しやすい。画像記事では、画面上の視覚観察と、機器動作・物体種別・同一性などの解釈が混ざりやすい。また note投稿時のレイアウト崩れ対策として、Markdown表・引用ブロックに加えて長い英文引用も避ける必要がある。既に標準化済みの違反は、通常の新規指摘ではなく反復違反として明示する。

#### Rule Update Needed
Yes

#### Suggested Rule Update
`docs/review_standard_v1.md` に「Codex監査方針：重点チェック」を追加。OCR不可記事ではファイル名以外の事実・背景・シリーズ推定を重点チェックし、`Record Group`、`FBI番号体系`、`NARA`、`Project Sign`、`JFK政権期` などの外部背景混入を WARN / BLOCK 候補にする。画像記事では視覚観察と機器・物体解釈を分離して評価する。`docs/audit_checklist_v1.md` に長い英文引用、画像記事チェック、短い修正指摘、反復違反明示を追加する。

#### Follow-up Owner
Codex（次回監査から、該当時はセクション名・該当文・修正案を短く出し、既出ルール違反は「反復違反」と明示する）

#### Status
Reflected

---

### [20260514-005] Article ID: 今後の note_drafts 全記事 — note投稿互換フォーマット制約（表・引用ブロック禁止）

#### Article ID
今後の note_drafts 全記事

#### Codex Finding
（該当なし。note投稿時に発生したフォーマット問題として記録）

#### Codex Severity
N/A（Codex未検出→新規フォーマットルールとして記録）

#### Human Decision
Accepted

#### Reason
noteブラウザ投稿画面へのコピペで、Markdown table・引用ブロック（`>`）・複雑なネスト箇条書き・Codex注釈ブロックが本文欠落、空白化、レイアウト崩れを引き起こす可能性がある。ドラフト生成段階で note 投稿互換の単純な本文構造に統一する。

#### Rule Update Needed
Yes

#### Suggested Rule Update
`docs/review_standard_v1.md` に「note投稿互換フォーマット」セクションを追加。`docs/audit_checklist_v1.md` P2-5 に note投稿互換チェックを追加（Markdown table → 🔴 BLOCK、引用ブロック → 🔴 BLOCK、複雑なネスト箇条書き → 🔴 BLOCK、Codex注釈ブロック in note_drafts → 🔴 BLOCK）。代替フォーマット：表は「【項目名】＋箇条書き」、英文引用は「【原文抜粋】」通常テキスト、和訳は「【要訳】」通常テキスト。

#### Follow-up Owner
Claude Code / Codex（今後の note_drafts 生成・監査時に適用）

#### Status
Reflected

---

### [20260514-004] Article ID: #048〜 — Source URL 直接URL化・MGRS初出補足を標準ルール化

#### Article ID
#048〜（全記事共通）

#### Codex Finding
（該当なし。人間レビューで毎回発生していた定型修正として記録）

#### Codex Severity
N/A（Codex未検出→標準フォーマットルール化として記録）

#### Human Decision
Accepted

#### Reason
①Source URL がトップページ（https://www.war.gov/UFO/）のまま出力される問題が毎回発生しており、人間側で直接 PDF URL へ修正していた。②Incident Location の MGRS 初出補足漏れも同様に毎回発生していた。どちらもドラフト生成段階で事前修正することで、人間レビュー工数を削減できる。

#### Rule Update Needed
Yes

#### Suggested Rule Update
`docs/review_standard_v1.md` に「AI概要版メタデータ定型ルール」セクションを新設。Source URL は直接 PDF URL 必須、Incident Location の MGRS は `MGRS〔軍用地図座標系〕` 初出補足必須とする。`docs/audit_checklist_v1.md` P1-1 に両チェック項目を追加（Source URL → 🔴 BLOCK、MGRS補足 → ⚠️ WARN）。#048〜#060 のドラフト Source URL を一括修正済み。

#### Follow-up Owner
Codex（次回監査から、Source URL がトップページの場合 BLOCK、MGRS初出補足なしは WARN を出す）

#### Status
Reflected

---

### [20260513-003] Article ID: #042 — 記事単独理解性の対象語を強化

#### Article ID
#042

#### Codex Finding
（該当なし。人間レビューで新たに発見されたフィードバック）

#### Codex Severity
N/A（Codex未検出→新規ルール追加として記録）

#### Human Decision
Accepted

#### Reason
一般読者はどの記事から読み始めるか分からず、シリーズ前提の省略は可読性低下につながる。ISR、MISREP、FVEY、1.4(a)、RTB、MGRS などの基本軍事・管理用語は、記事単独で読んでも理解できるよう初出時に毎回補足する必要がある。

#### Rule Update Needed
Yes

#### Suggested Rule Update
基本軍事略語・管理用語は、「過去記事で説明済み」を理由に省略しない。RTB は `RTB（Return To Base：基地へ帰投）`、MISREP は `MISREP（軍の任務報告書）`、FVEY は `FVEY（Five Eyes共有）`、1.4(a) は `国家安全保障上の理由（1.4(a)区分）` と補足する。

#### Follow-up Owner
Codex（次回監査から、RTB・MISREP・FVEY・1.4(a) の初出補足不足にWARNを出す）

#### Status
Reflected

---

### [20260515-001] Article ID: General — 軍事略語・専門語の標準補足を更新

#### Article ID
General

#### Codex Finding
（該当なし。人間指示による標準補足更新）

#### Codex Severity
N/A

#### Human Decision
Accepted

#### Reason
一般向けUAP記事では、軍事略語・専門語の直訳よりも意味が伝わる補足が必要。初出時に短い標準補足を入れ、2回目以降は略語のみとする。ただし、資料から確認できない具体化は避ける。

#### Rule Update Needed
Yes

#### Suggested Rule Update
AARO は `AARO（全領域異常解決局／米国防総省のUAP調査組織）`、USCENTCOM は `USCENTCOM（米国中央軍。中東・中央アジア周辺を担当する米軍の統合軍）`、MISREP は `MISREP（軍の任務報告書）`、GENTEXT は `GENTEXT（報告書内の自由記述欄）`、FMV は `FMV（フルモーション映像。静止画ではなく短い動画クリップとして記録された映像）`、positive identification は `対象を明確に識別すること` と補足する。`platform` は、具体的な機種・車両・装置が未確認の場合 `米軍側の機材・システム` と訳し、航空機・車両・ドローン等に断定しない。

#### Follow-up Owner
Codex（今後のドラフト生成・レビューで初出補足不足、意味不足、platformの根拠なき具体化にWARN/BLOCKを出す）

#### Status
Reflected

---

### [20260513-002] Article ID: #041 — 基本軍事略語は記事ごとに初出補足が必要

#### Article ID
#041

#### Codex Finding
（該当なし。人間レビューで新たに発見されたフィードバック）

#### Codex Severity
N/A（Codex未検出→新規ルール追加として記録）

#### Human Decision
Accepted

#### Reason
ISR は軍事分野では基本用語だが、一般読者には意味が伝わりにくい。AI概要版は読者が #001 から順番に読むとは限らず、どの記事から読み始めても意味が分かる「記事単独理解性」を担保する必要がある。「過去記事で説明済み」を理由に省略しない。

#### Rule Update Needed
Yes

#### Suggested Rule Update
`docs/review_standard_v1.md` に「Phase 2 追加基準：記事単独理解性（#041以降適用）」を追加。ISR・SIGINT・IMINT・FMV・MGRS・MDR・MRN・JSIR・HVI・POI・FVEY・NOFORN 等の略語は記事ごとの初出時に毎回補足する。

ISR は記事ごとの初出で `ISR（情報収集・監視・偵察）` と補足する。#041では `UAE・アル・ダフラ空軍基地（OMAM）発のISR任務中` を `UAE・アル・ダフラ空軍基地（OMAM）発のISR（情報収集・監視・偵察）任務中`、`ISRミッションレポートです` を `ISR（情報収集・監視・偵察）ミッションの報告書です` に修正する。

#### Follow-up Owner
Codex（次回監査から、初出補足なしの対象略語にWARNを出す）

#### Status
Reflected

---

### [20260513-001] Article ID: #040 — 単位換算だけでなくスケール感翻訳が必要

#### Article ID
#040

#### Codex Finding
（該当なし。Codexがこの項目を指摘していたわけではなく、人間＋ChatGPTレビューで新たに発見されたフィードバック）

#### Codex Severity
N/A（Codex未検出→新規ルール追加として記録）

#### Human Decision
Accepted

#### Reason
「81,500ポンド」は単位換算をしても「36,967kg」では一般読者に規模感が伝わらない。「約37トン」のように丸めたスケール感のある表現が必要。単位の正確な変換ではなく、読者が数値の規模・異常性を感覚的にイメージできることが目的。

#### Rule Update Needed
Yes

#### Suggested Rule Update
`docs/review_standard_v1.md` に「Phase 2 追加基準：スケール感翻訳（#040以降適用）」を追加。対象は重量・燃料量・大きな距離・高度など。推奨は「約37トン」「約30.5km」のような丸めた表現。NG は「36,967kg」のような過度な精密換算値。

#### Follow-up Owner
Codex（次回監査から、スケール感のない大きな数値にWARNを出す）

#### Status
Reflected

---

## ステータス定義

| Status | 意味 |
|--------|------|
| Open | 判断済みだが、ルール反映・修正がまだ |
| Reflected | audit_checklist または review_standard にルールを反映済み |
| Closed | 対応完了（反映不要の場合も含む） |

---

## Human Decision 定義

| Decision | 意味 |
|---------|------|
| Accepted | Codexの指摘を正当と判断し、修正または今後のルールに採用する |
| Rejected | Codexの指摘を不当と判断し、対応しない（同種のWARNは今後出さないよう指示） |
| Partially Accepted | 指摘の一部のみ採用 |
| Deferred | 今回は保留。将来の改訂時に検討 |

---

## 改訂履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| v1.0 | 2026-05-13 | 初版制定 |
| v1.1 | 2026-05-13 | #040フィードバックとしてスケール感翻訳を記録 |
| v1.2 | 2026-05-13 | #041フィードバックとして記事単独理解性（略語初出補足必須）を記録 |
| v1.3 | 2026-05-13 | #042フィードバックとしてRTB・MISREP・FVEY・1.4(a)の初出補足必須を記録 |
| v1.4 | 2026-05-14 | Source URL直接URL化・MGRS初出補足を標準フォーマットルールとして記録（#048〜一括修正済み） |
| v1.5 | 2026-05-14 | 今後の note_drafts 全記事に note投稿互換フォーマット制約（Markdown table・引用ブロック・Codex注釈ブロック・複雑なネスト箇条書き禁止）を記録 |
| v1.6 | 2026-05-14 | OCR不可記事・画像記事・長い英文引用・短い修正指摘・反復違反明示のレビュー方針を記録 |
| v1.7 | 2026-05-14 | #091以降の軽量レビュー方式（PASS一行、WARN集約、BLOCKのみ詳細）を記録 |
| v1.8 | 2026-05-15 | AARO・USCENTCOM・MISREP・GENTEXT・FMV・positive identification・platform の標準補足を更新 |
