# UAP Translation Project — Project Asset Audit
**監査日：** 2026-06-21  
**参照ソース：** files_catalog.csv / release02_coverage_audit_20260620.md / batch_final_report_20260620_PR071-PR099.md / article_inventory_20260619.md  
**監査モード：** 読み取りのみ（workflow.db / source_registry 変更なし）

---

## 0. 全体サマリー

| 項目 | 数値 |
|---|---|
| files_catalog.csv 総ファイル数 | **294件** |
| Release 01 スコープ（CIA/ODNI/NASA/DoS/IC系） | **62件** |
| Release 02 スコープ（DOW+FBI+DOE） | **232件** |
| Release 03 管理対象（PDF・workflow.db登録済み） | **5件** ※R02素材内から分離 |
| note.com 公開済み記事（全Release合計） | **8件** |
| Release 02 VID DONE_CANDIDATE | **76件** |
| Release 02 VID 管理漏れ | **3件** |
| Release 02 PDF ドラフト未作成 | **約27件** |
| files_catalog 不整合 | **3件** |

---

## 1. Release 01 状態

Release 01はCIA / ODNI / NASA / DoS / IC Agency等の非DOW/FBI/DOE機関ファイル群。

### 1-1. agency別ファイル数（files_catalog内）

| agency | 件数 |
|---|---|
| NASA | 33件 |
| CIA（表記ゆれ含む） | 19件 |
| Department of State | 7件 |
| ODNI | 1件 |
| Intelligence Community Agency | 1件 |
| U.S. Government | 1件 |
| **合計** | **62件** |

### 1-2. 記事化状態

| 状態 | 件数 | 内容 |
|---|---|---|
| 公開済み（note.com） | 2件 | ODNI-UAP-D001（R02-s1）、CIA-UAP-D001（R02-s2） |
| Release 02 扱いで公開済み | 1件 | DOW-UAP-D017（R02-s3） |
| 未着手 | 約59件 | NASA / DoS / IC系（Release後続対応予定） |

> CIA-UAP-D001 は Release 01 機関だが workflow.db 上 R02-s2 として管理。  
> NASA / DoS / IC 系はリリース計画未策定。

---

## 2. Release 02 状態

Release 02対象：Department of War / FBI / Department of Energy の全ファイル。

### 2-1. ファイルタイプ別内訳（232件）

| file_type | DOW | FBI | DOE | 合計 |
|---|---|---|---|---|
| VID | 78件 | 6件 | 0件 | **84件** |
| PDF | 65件 | 62件 | 3件 | **130件** |
| IMG | 0件 | 18件 | 0件 | **18件** |
| AUD | 0件 | 0件 | 0件 | **0件** |
| **合計** | **143件** | **86件** | **3件** | **232件** |

---

### 2-2. VID（84件）記事化状態詳細

| 状態 | 件数 | 内訳 |
|---|---|---|
| **公開済み** | **2件** | PR050（R02-008）、PR051（R02-009） |
| **DONE_CANDIDATE** | **76件** | 下記バッチ詳細参照 |
| **HOLD** | **3件** | PR057a（R02-048）、PR057b（R02-049）、PR058（R02-050） |
| **SKIP** | **1件** | PR098（超長尺 1056秒） |
| **管理漏れ（未採番）** | **2件** | PR052（ドラフトなし）、PR070（ドラフトあり・article_id未割当） |
| **合計** | **84件** | |

**VIDカバレッジ：** 管理済み 82件 / 84件 = **97.6%**（未採番2件を除く）

#### DONE_CANDIDATE バッチ内訳（76件）

| バッチ | 件数 | 対象PR番号 |
|---|---|---|
| DOW バッチA | 27件 | PR019〜049（欠番除く） |
| FBI バッチ | 6件 | FBI-PR001〜006 |
| DOW 中間バッチ | 15件 | PR053/054/055/056/059/060/061/062/063/064/065/066/067/068/069 |
| DOW バッチ（PR071-PR099） | 28件 | PR071〜PR099（PR098=SKIP除く） |
| **合計** | **76件** | |

> 全件 Codex iter2以上 実施済み（PASS または WARN / 許容BLOCK）。  
> workflow.db への登録は未実施（source_registry のみ管理中）。

---

### 2-3. PDF（130件）記事化状態詳細

| 分類 | 件数 | 内容 |
|---|---|---|
| **R02公開済み** | **3件** | DOE-UAP-D001/D002/D003（R02-001〜003） |
| **R01管理・公開済み** | **1件** | DOW-UAP-D017（R02-s3） |
| **R03管理（別途管理中）** | **5件** | D077/D079/D080/FBI-D009/FBI-D010 |
| **R03候補（ドラフト確認要）** | **3件** | DOW-D081/D082/D083（Western US Narrative 3〜5） |
| **旧形式ドラフトあり（article_id未割当）** | **約87件** | fbi-photo-b系/FBI-HQ-62系/DOW mission report系等 |
| **未記事化（ドラフトなし）** | **約27件** | DOW D系未対応14件 + FBI-D001〜008/D011〜013 11件 + その他2件 |
| **要確認（状況不明）** | **約4件** | D086/D087/D088/composite-sketch |
| **合計** | **130件** | |

**PDF着手率：** 約96件 / 130件 = **約73.8%**（旧形式ドラフト含む）

#### 旧形式ドラフトあり 約87件 内訳

| グループ | 件数 |
|---|---|
| fbi-photo-b1〜b24（FBI写真PDF） | 24件 |
| FBI HQ 62-HQ-83894 section / serial系 | 18件 |
| FBI witness statement系・342_hs1系 | 5件 |
| 341系・331系・38系・18系等 | 8件 |
| DOW mission report系（D3/D8/D10〜D74等） | 25件 |
| DOW-D084/D085 | 2件 |
| western_us_event_slides等 | 2件 |
| その他 | 3件 |

> 上記は全て旧形式ドラフト。note.com公開済みのものも含む。article_id（R02-XXX）未割当。

#### 未記事化（約27件）内訳

| グループ | 件数 |
|---|---|
| DOW mission report 未対応（D4〜D7/D20/D25/D28/D38/D44/D50〜52/D56〜58/D75） | 14件 |
| FBI-UAP-D001〜D008（Colorado Springs / Northeastern US 報告書） | 8件 |
| FBI-UAP-D011〜D013（歴史的FBI文書） | 3件 |
| DOW-UAP-D078（地図・Notional Map） | 1件 |
| 2024-04-30-composite-sketch.pdf | 1件 |

---

### 2-4. IMG（18件）

| グループ | 件数 | 扱い |
|---|---|---|
| fbi-photo-a1〜a8（PNG画像） | 8件 | 単独記事化対象外（§6参照） |
| FBI-UAP-D014〜D023（Western US Eventデジタルレンダリング） | 10件 | 単独記事化対象外（D077系記事の付属素材） |
| **合計** | **18件** | **全件 単独記事化なし** |

### 2-5. AUD

Release 02素材にAUDファイルなし。AUD 11件は全てNASA系（Release 02対象外）。

---

## 3. Release 03 状態

workflow.db登録済み5件。全件 `publish_blocked = true`。

| article_id | file_id | publish_order | status | Codex |
|---|---|---|---|---|
| R03-001 | DOW-UAP-D077 | 3001 | 下書き保存（公開ブロック中） | iter2 PASS |
| R03-002 | DOW-UAP-D079 | 3002 | 公開待機中（ブロック） | iter2 PASS |
| R03-003 | DOW-UAP-D080 | 3003 | ドラフトなし | 未実施 |
| R03-004 | FBI-UAP-D009 | 3004 | ドラフトなし | 未実施 |
| R03-005 | FBI-UAP-D010 | 3005 | ドラフトなし | 未実施 |

**公開ブロック理由：** Release 02 DONE_CANDIDATE 76件が未公開のため。  
R03-003/004/005 のドラフト作成は Release 02 公開完了後に着手予定。

---

## 4. 公開済み記事（note.com 全リリース合計）

合計：**8件**

| article_id | file_id | agency | Codex | note.com |
|---|---|---|---|---|
| R02-s1 | ODNI-UAP-D001 | ODNI | iter1 BLOCK（旧仕様） | 公開済み |
| R02-s2 | CIA-UAP-D001 | CIA | iter1 BLOCK（旧仕様） | 公開済み |
| R02-s3 | DOW-UAP-D017 | DOW | iter1 WARN（旧仕様） | 公開済み |
| R02-001 | DOE-UAP-D001 | DOE | iter2 PASS | 公開済み |
| R02-002 | DOE-UAP-D002 | DOE | iter2 PASS | 公開済み |
| R02-003 | DOE-UAP-D003 | DOE | iter2 PASS | 公開済み |
| R02-008 | DOW-UAP-PR050 | DOW | iter2 PASS | 公開済み |
| R02-009 | DOW-UAP-PR051 | DOW | iter2 PASS | 公開済み |

> R02-004〜007 は欠番保留。R02-010〜089（80枠）は登録待ち。

---

## 5. DONE_CANDIDATE

VID 76件。Codex監査済み（全件 iter2以上）。

**note_drafts ディレクトリ：** _note_version ファイル 185件存在。  
（VID 76件 + 公開済み2件 + PDF旧形式ドラフト等を含む）

workflow.db 登録状況：**R02-XXX 全件未登録**（source_registry のみ管理中）。  
source_registry 登録済み R02 エントリ：5件（R02-001/002/003/008/009 = 全件 published）。

---

## 6. HOLD / SKIP

| PR番号 | article_id | 状態 | 理由 |
|---|---|---|---|
| PR057a | R02-048 | **HOLD** | 実体ファイルのドラフト未転用（既存PR057ドラフトをPR057aへ改名要） |
| PR057b | R02-049 | **HOLD** | 実体ファイルの記事化未完了 |
| PR058 | R02-050 | **HOLD** | 記事化未完了 |
| PR098 | 未採番 | **SKIP** | 超長尺（1056秒）のため通常フローでは非対応 |

---

## 7. 不整合一覧

### 7-1. VID 管理漏れ（files_catalog登録済み・article_id未割当）

| PR番号 | ドラフト | 推奨対応 |
|---|---|---|
| **PR052** | なし | article_id 割当 → ドラフト作成 → Codex監査 |
| **PR070** | あり | article_id 割当のみ（ドラフト転用可能） |

> PR098 は SKIP 確定（超長尺1056秒）だが article_id 未割当。  
> 管理台帳への記録（SKIP扱い）は要実施。

### 7-2. PR057 実体不在

`DOW-UAP-PR057` のドラフトが存在するが、files_catalog に PR057 のファイルが登録されていない。  
実体は `PR057a`（R02-048）と `PR057b`（R02-049）の2ファイル。  
**推奨対応：** 既存PR057ドラフト → `PR057a`（R02-048）の記事として転用・改名。

### 7-3. PDF 要確認4件

| ファイル | 状況 |
|---|---|
| DOW-UAP-D086 | 対応ドラフト不明（USNavy Report of Flying Discs 1948） |
| DOW-UAP-D087 | ai_summary_057との同一性要確認 |
| DOW-UAP-D088 | ai_summary_058との同一性要確認 |
| 2024-04-30-composite-sketch.pdf | Western US Event参考素材と思われるが対応方針未定 |

---

## 8. fbi-photo-a1 の扱い

**方針：単独記事化しない。**

`fbi-photo-a1〜a8`（PNG画像 8件）は以下の理由で独立した note 記事を作成しない：

1. 対応するPDF（`fbi-photo-b1〜b24`）の旧形式ドラフトにすでに挿入済み
2. IMG単独では文書的文脈（説明文・背景情報）が成立しない
3. 現行のR02番号体系（R02-010〜089）はVID専用であり、IMGに割り当てる枠がない

記事内での扱い：fbi-photo-b系PDF記事の本文中に画像として埋め込む（付属素材扱い）。

---

## 9. ファイル管理単位と公開コンテンツ単位の分離方針

```
ファイル管理単位 ≠ 公開コンテンツ単位
```

| 概念 | 定義 | 管理場所 |
|---|---|---|
| ファイル管理単位 | files_catalog.csv の1行 = 1政府公開ファイル | files_catalog.csv |
| 公開コンテンツ単位 | 1記事 = 1 article_id = note.com 1投稿 | source_registry / workflow.db |
| VID記事 | 1 VIDファイル → 1記事（原則1:1） | R02-010〜089番号体系 |
| PDF記事 | 1ファイル → 1記事、または複数PDFを1記事に集約も可 | 番号体系未設計（R02-090以降候補） |
| IMG | 記事本文挿入素材（単独article_id付与しない） | 対応PDF記事内で管理 |
| AUD | Release 02対象外（NASA系 = 別Release） | 別途管理 |

**重要な分離原則：**
- VIDの管理漏れ（PR052/PR070）は「ファイル管理側の不整合」。article_id割当で解消。
- PDFの旧形式ドラフト87件は「コンテンツ側の未整理」。article_id割当体系の設計が先決。
- IMGの単独記事化は行わない。常にPDF/VID記事の付属素材として扱う。

---

## 10. 修正優先順位

| 優先度 | 分類 | 対象 | 作業内容 |
|---|---|---|---|
| **P1** | VID不整合解消 | PR052 | article_id割当 → ドラフト作成 → Codex監査 |
| **P1** | VID不整合解消 | PR070 | article_id割当（ドラフトは転用可） |
| **P1** | VID不整合解消 | PR098 | article_id割当（SKIP）→ 管理台帳へ記録 |
| **P2** | ドラフト転用 | PR057 | 既存PR057ドラフト → PR057a（R02-048）に改名・転用 |
| **P3** | 品質修正 | PR066 | ドラフト残存作業メモ行削除 → Codex iter3実施 |
| **P4** | 体系設計 | PDF article_id | R02-090以降またはPDF専用番号体系の設計 |
| **P5** | DB登録 | R02 DONE_CANDIDATE | 76件のworkflow.db登録（現在source_registryのみ） |
| **P6** | 公開実行 | Release 02 VID | DONE_CANDIDATE 76件 → note.com 一括公開 |
| **P7** | R03 着手 | D080/FBI-D009/010 | Release 02公開完了後にドラフト作成開始 |

---

## 付録：Release 02 numbering体系

```
R02-s1〜s3 : 特別採番（旧Codex時代・R02準備作業）
R02-001〜003 : DOE PDF 3件（公開済み）
R02-004〜007 : 欠番（保留）
R02-008 : DOW-UAP-PR050（公開済み）
R02-009 : DOW-UAP-PR051（公開済み）
R02-010〜089 : DOW/FBI VID 80件枠（DONE_CANDIDATE 76件 + HOLD 3件 + 未割当 1件）
R02-090〜   : 未設計（PDF記事化 / VID残3件用）
```

---

**出力ファイル：** `review_reports/project_asset_audit.md`  
**監査実施：** 2026-06-21  
**次回推奨アクション：** P1（PR052/PR070/PR098 管理漏れ解消）
