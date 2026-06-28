# Release 02 管理漏れ補完計画（Gap Closure Plan）
**作成日：** 2026-06-21  
**対象：** DOW-UAP-PR052 / DOW-UAP-PR070 / DOW-UAP-PR098  
**参照：** release02_numbering_plan.md（v2+補完）/ release02_article_unit_policy_v3.md §3  
**目的：** files_catalog 登録済みだが article_id 未割当だった VID 3件を正式採番し、Release 02 VID 全84件の管理を完成させる

---

## 0. 補完後の重複確認

| チェック項目 | 結果 |
|---|---|
| article_id 重複（R02-001〜092） | **なし** |
| #2_XXX 重複（#2_001〜092） | **なし** |
| publish_order 重複（2090〜2092） | **なし** |
| R02-090〜092 既存割当 | **なし**（新規割当） |
| #2_001〜092 連続性 | **連続**（欠番は R02-004〜007 のみ・意図的保留） |
| VID 全件採番完了（84件） | **✓ 完了** |

---

## 1. 正式採番一覧

| PR番号 | article_id | #2_XXX | publish_order | status | 備考 |
|---|---|---|---|---|---|
| **PR052** | **R02-090** | **#2_090** | **2090** | **✅ DONE_CANDIDATE** | Codex iter2 PASS（2026-06-21） |
| **PR070** | **R02-091** | **#2_091** | **2091** | **✅ DONE_CANDIDATE** | Codex iter3 PASS（2026-06-21） |
| **PR098** | **R02-092** | **#2_092** | **2092** | **SKIP** | 超長尺（1056秒）・公開キュー対象外 |

---

## 2. PR052（R02-090）

### 素材情報

| 項目 | 値 |
|---|---|
| article_id | **R02-090** |
| #2_XXX | **#2_090** |
| publish_order | **2090** |
| status | **✅ DONE_CANDIDATE（Codex iter2 PASS 2026-06-21）** |
| file_name | DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission.mp4 |
| agency | Department of War |
| release_date | 2026-05-22（war.gov Release 02） |
| incident_date | 不明（files_catalog 未記録） |
| incident_location | 不明（files_catalog 未記録） |
| DVIDS ID | 1007708 |
| downloaded | true |

### 経緯・完了記録（2026-06-21）

| 項目 | 内容 |
|---|---|
| ドラフト | `note_drafts/ai_summary_DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission_note_version.md` |
| **Codex iter1（2026-06-21）** | **VERDICT: WARN（BLOCK 0 / WARN 3 / PASS 11）** |
| **Codex iter2（2026-06-21）** | **VERDICT: PASS（BLOCK 0 / WARN 0 / PASS 14）** |
| **最終ステータス** | **✅ DONE_CANDIDATE** |

### 実施した修正（2026-06-21）

| 修正 | 対応 |
|---|---|
| frame_0060キャプションにframe_0180参照を追記 | M1-VISUAL W-01 解消 |
| AARO説明文を ## AARO 公式説明（war.gov より）として独立セクション化 | M8-AARO-DESC W-02 解消 |
| AI解析メモの「IR映像」→「赤外線（IR）映像」 | W-03（IR略語統一）解消 |
| BT.709・HUD 初出注釈追加 | CAT-01 解消 |
| 2026年3月6日 → 2026年03月06日 | CAT-04 解消 |
| AARo → AARO 誤記修正 | 誤記解消 |

### Codex 履歴

| iter | 日付 | VERDICT | BLOCK | WARN | 参照ファイル |
|---|---|---|---|---|---|
| iter1 | 2026-06-21 | WARN | 0 | 3 | codex_audit_20260621_...PR052.md |
| **iter2** | **2026-06-21** | **PASS** | **0** | **0** | **codex_audit_20260621_...PR052_iter2.md** |

---

## 3. PR070（R02-091）

### 素材情報

| 項目 | 値 |
|---|---|
| article_id | **R02-091** |
| #2_XXX | **#2_091** |
| publish_order | **2091** |
| status | **✅ DONE_CANDIDATE（Codex iter3 PASS 2026-06-21）** |
| file_name | DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_Unidentified_Aerial_Phenomena_UAP_on_13_.mp4 |
| agency | Department of War |
| release_date | 2026-05-22 |
| incident_date | 2023年2月13日（ファイル名「on_13_」・uap-csv-cache.csv「13 Feb 23」） |
| incident_location | Southeastern United States（エグリン空軍基地・フロリダ州） |
| AOR | NORTHCOM |
| DVIDS ID | 1007783 |
| downloaded | true |

### 経緯・完了記録（2026-06-21）

| 項目 | 内容 |
|---|---|
| ドラフト | `note_drafts/ai_summary_DOW-UAP-PR070_..._note_version.md` |
| Codex iter2（2026-06-19） | VERDICT: BLOCK（P1-REG×1 / WARN×3） |
| **Codex iter3（2026-06-21）** | **VERDICT: PASS（BLOCK 0 / WARN 0 / PASS 14）** |
| **最終ステータス** | **✅ DONE_CANDIDATE** |

### 実施した修正（2026-06-21）

| 修正 | 対応 |
|---|---|
| タイトル `#TBD` → `#R02-091` | P1-REG 解消 |
| 作業メモ行削除（`→ 使用ファイル：...`） | W-02 解消 |
| AI解析メモを出典後へ移動 | W-01 解消 |
| 注意点に NORTHCOM AOR・chain-of-custody 追記 | W-03 解消 |
| 末尾注記を article_id R02-091 採番済み表記へ更新 | P1-REG 補完 |

### Codex 履歴

| iter | 日付 | VERDICT | BLOCK | WARN | 参照ファイル |
|---|---|---|---|---|---|
| iter1 | 2026-06-19 | BLOCK | 1 | 3 | codex_audit_20260619_...PR070.md |
| iter2 | 2026-06-19 | BLOCK | 1 | 3 | codex_audit_20260619_...PR070_iter2.md |
| **iter3** | **2026-06-21** | **PASS** | **0** | **0** | **codex_audit_20260621_...PR070_iter3.md** |

---

## 4. PR098（R02-092）

### 素材情報

| 項目 | 値 |
|---|---|
| article_id | **R02-092** |
| #2_XXX | **#2_092** |
| publish_order | **2092** |
| status | **SKIP** |
| file_name | DOW-UAP-PR098_UFOs_in_formation_over_Persian_Gulf.mp4 |
| agency | Department of War |
| release_date | 2026-05-22 |
| incident_date | 不明（files_catalog 未記録） |
| incident_location | CENTCOM（ペルシャ湾） |
| DVIDS ID | 1007737 |
| downloaded | true |

### 現状

- ドラフト **なし**
- Codex **未実施**
- **SKIP理由：** 再生時間 1056秒（17分36秒）= 通常フローの上限を超えた超長尺映像

### SKIP の定義と扱い

| 項目 | 内容 |
|---|---|
| article_id | **R02-092 / #2_092**（管理台帳への記録目的で採番） |
| publish_order | **2092**（公開キューに投入しない） |
| 公開予定 | **なし**（通常フローでは非対応） |
| files_catalog | 登録済みのまま維持（変更不要） |
| 後日対応可能性 | 超長尺対応フロー（分割処理・要人間作業）が整備された場合に再検討 |

### ファイル名から読み取れる情報

- **UFOs in formation**：複数のUFO編隊（UFO＝UAP の旧称表記）
- **Persian Gulf**：ペルシャ湾上空での観測
- 17分超の映像：VID定常記録またはオペレーションログである可能性が高い

---

## 5. 採番後の Release 02 VID 状態サマリー

| 状態 | 件数 | PR番号 |
|---|---|---|
| 公開済み（note.com） | 2件 | PR050（R02-008）、PR051（R02-009） |
| **✅ DONE_CANDIDATE** | **78件** | 前バッチA(27)+前バッチB(6)+中間バッチ有効(15)+今回バッチ(28)+**PR070(1)**+**PR052(1)** |
| DRAFT_NEEDED | 0件 | — |
| HOLD | 3件 | PR057a（R02-048）、PR057b（R02-049）、PR058（R02-050） |
| SKIP | 1件 | PR098（R02-092） |
| **合計** | **84件** | **VID 全件採番完了 ✓** |

### 公開キュー投入可能件数（2026-06-21時点）

| 区分 | 件数 | 内訳 |
|---|---|---|
| **即時公開可能（DONE_CANDIDATE）** | **78件** | PR052（R02-090）・PR070（R02-091）の追加でDONE_CANDIDATE 78件 |
| **公開キュー見込み合計** | **78件** | |
| 公開対象外（HOLD/SKIP） | 4件 | PR057a/b, PR058（HOLD） + PR098（SKIP） |

---

## 6. Release 02 番号体系の完成確認

### VID 番号体系（R02-008〜092）

```
R02-008 / #2_008 / —    : PR050（公開済み）
R02-009 / #2_009 / —    : PR051（公開済み）
R02-010 / #2_010 / 2010 : PR019  ← 前バッチA 先頭
...
R02-036 / #2_036 / 2036 : PR049  ← 前バッチA 末尾
R02-037 / #2_037 / 2037 : FBI-PR001  ← 前バッチB 先頭
...
R02-042 / #2_042 / 2042 : FBI-PR006  ← 前バッチB 末尾
R02-043 / #2_043 / 2043 : PR053  ← 中間バッチ 先頭
...
R02-061 / #2_061 / 2061 : PR069  ← 中間バッチ 末尾
R02-062 / #2_062 / 2062 : PR071  ← 今回バッチ 先頭
...
R02-089 / #2_089 / 2089 : PR099  ← 今回バッチ 末尾
R02-090 / #2_090 / 2090 : PR052  ← 管理漏れ補完 [NEW]
R02-091 / #2_091 / 2091 : PR070  ← 管理漏れ補完 [NEW]
R02-092 / #2_092 / 2092 : PR098  ← 管理漏れ補完 SKIP [NEW]
```

### PDF/IMG 番号体系（R02-093〜）

article_unit_policy_v3.md §3〜7 に基づき別途設計済み（#2_093〜124）。

### Release 02 番号体系 完成判定

| 判定対象 | 結果 |
|---|---|
| VID 全84件の article_id 割当 | **✓ 完了**（本補完で完成） |
| #2_001〜092 の連続性 | **✓ 連続**（欠番は R02-004〜007 のみ・意図的） |
| publish_order 2090〜2092 の重複 | **✓ なし** |
| DONE_CANDIDATE 公開可能件数 | **78件（PR052・PR070追加後 78件）** |
| PDF/IMG 体系 | **設計済み（#2_093〜124、policy v3参照）** |

---

## 7. 次回作業推奨順

| 優先度 | 作業 | 対象 | 状態 |
|---|---|---|---|
| **P1-a** | PR070 ドラフト修正 → Codex iter3 | R02-091 | **✅ 完了（2026-06-21）** |
| **P1-b** | PR052 ドラフト新規作成 → Codex iter1/iter2 | R02-090 | **✅ 完了（2026-06-21）** |
| **P2** | PR098 管理台帳記録（source_registry 登録時 SKIP 明記） | R02-092 | ⬜ 未着手（採番のみ済み） |
| **P3** | Release 02 VID 78件の公開キュー一括投入 | R02-008〜091 | ⬜ 別途計画 |

---

**出力ファイル：** `review_reports/release02_gap_closure_plan.md`  
**作成：** 2026-06-21  
**更新対象：** `review_reports/release02_numbering_plan.md`（v2 → v2+補完：セクション1/7/8/9を更新済み）
