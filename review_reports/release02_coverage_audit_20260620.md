# Release 02 全素材 記事化カバレッジ監査レポート
**監査日：** 2026-06-20  
**調査対象：** metadata/files_catalog.csv / review_reports/release02_numbering_plan.md / workflow.db / source_registry.csv  
**監査モード：** 読み取りのみ（workflow.db / source_registry.csv 変更なし）

---

## 1. Release 02 素材総数（files_catalog.csv より）

| file_type | DOW | FBI | DOE | 合計 |
|---|---|---|---|---|
| VID | 78件 | 6件 | 0件 | **84件** |
| PDF | 65件 | 62件 | 3件 | **130件** |
| IMG | 0件 | 18件 | 0件 | **18件** |
| AUD | 0件 | 0件 | 0件 | **0件** |
| **合計** | **143件** | **86件** | **3件** | **232件** |

> **Release 02素材定義：** agency が `Department of War` / `FBI` / `Department of Energy` の全ファイル  
> 対象外：CIA / NASA / Department of State / ODNI / IC Agency（別リリース管理）

---

## 2. VID（84件）記事化カバレッジ詳細

### 2-1. VID カバレッジ全体

| 状態 | 件数 | PR番号 |
|---|---|---|
| **公開済み（source_registry published）** | **2件** | PR050（R02-008）、PR051（R02-009） |
| **DONE_CANDIDATE（前バッチA）** | **27件** | DOW PR019〜049（欠番除く） |
| **DONE_CANDIDATE（前バッチB）** | **6件** | FBI-PR001〜006 |
| **DONE_CANDIDATE（中間バッチ）** | **15件** | PR053/054/055/056/059/060/061/062/063/064/065/066/067/068/069 |
| **DONE_CANDIDATE（今回バッチ）** | **28件** | PR071〜099（PR098除く） |
| **HOLD（記事化未完了・予約済み）** | **3件** | PR057a（R02-048）/ PR057b（R02-049）/ PR058（R02-050） |
| **管理漏れ（未採番）** | **3件** | PR052 / PR070 / PR098 ← **要対応** |
| 合計 | 84件 | |

### 2-2. DONE_CANDIDATE 合計

| カテゴリ | 件数 |
|---|---|
| 公開済み | 2件 |
| DONE_CANDIDATE | 76件 |
| HOLD | 3件 |
| **管理済み小計** | **81件** |
| 管理漏れ | 3件 |
| **総計** | **84件** |

**VIDカバレッジ率：81/84 = 96.4%**

### 2-3. 管理漏れ3件の詳細

| PR番号 | ファイル名（概略） | release_date | ドラフト | 状態 |
|---|---|---|---|---|
| **PR052** | DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission.mp4 | 2026-05-22 | **なし** | 要新規作成 |
| **PR070** | DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_.mp4 | 2026-05-22 | **あり**（DOW-UAP-PR070ドラフト） | 要採番のみ |
| **PR098** | DOW-UAP-PR098_UFOs_in_formation_over_Persian_Gulf.mp4 | 2026-05-22 | **なし** | 要新規作成 |

**補足：** PR057そのもの（DOW-UAP-PR057_Spherical_UAP_in_clouds.mp4）は files_catalog に**存在しない**。  
ドラフト（ai_summary_DOW-UAP-PR057_...）は作成済みだが、実ファイルは PR057a / PR057b として登録されている。  
当該ドラフトはPR057a（R02-048）への転用を推奨。

---

## 3. PDF（130件）記事化カバレッジ詳細

### 3-1. PDF カバレッジ分類

| 分類 | 件数 | 内容 |
|---|---|---|
| **R02公開済み** | **3件** | DOE-UAP-D001/D002/D003（R02-001〜003） |
| **R01管理（公開済み）** | **1件** | DOW-UAP-D017（workflow.db published） |
| **R03管理（workflow.db登録済み）** | **5件** | D077（R03-001）、D079（R03-002）、D080（R03-003）、FBI-D009（R03-004）、FBI-D010（R03-005） |
| **R03候補（ドラフト確認要）** | **3件** | DoW-D081/D082/D083（Western US Narrative 3〜5） |
| **旧形式ドラフトあり（R0X番号未割当）** | **約87件** | fbi-photo-b系・FBI-HQ-62系・DOW mission report系等 ※1 |
| **未記事化（ドラフトなし）** | **約27件** | DOW-D4〜7/D20/D25/D28/D38/D44/D50〜52/D56〜58/D75、FBI-UAP-D001〜008/D011〜013 ※2 |
| **要確認（対応状況不明）** | **約4件** | D078地図、D086（USNavy）、D087/D088（USAF）、composite-sketch ※3 |
| 合計 | **130件** | |

### 3-2. 注記

**※1 旧形式ドラフトあり（約87件）の内訳：**

| グループ | 件数 | ドラフト対応 |
|---|---|---|
| fbi-photo-b1〜24（FBI写真PDF） | 24件 | ai_summary_067〜092系 |
| FBI HQ 62-HQ-83894 section1〜10 | 10件 | ai_summary_065/094〜100/108系 |
| FBI HQ 62-HQ-83894 serial系 | 8件 | ai_summary_109〜116系 |
| FBI 65_hs1-101634279系 | 2件 | ai_summary_106/107系 |
| FBI witness statement系 | 4件 | ai_summary_060/061/062/070系 |
| 342_hs1（flying-discs-1949） | 1件 | ai_summary_063系 |
| 341系・331系・38系・18系 | 8件 | ai_summary_101〜105系 |
| DOW-D084/D085 | 2件 | ai_summary_063/064系 |
| DOW mission report系（D3/D8/D10〜D74等） | 25件 | ai_summary_017〜050系 |
| western_us_event_slides + dow-uap-pr20 | 2件 | ai_summary_056/western系 |
| その他 | 1件 | |
| **小計** | **約87件** | |

> 上記は全て旧形式（article_id = R0X未割当）。note公開済みのものも含む。

**※2 未記事化（約27件）：**

| グループ | 件数 |
|---|---|
| DOW mission report 未対応（D4〜D7、D20、D25、D28、D38、D44、D50〜52、D56〜58、D75） | 14件 |
| FBI-UAP-D001〜D008（Colorado Springs / Northeastern US 報告書） | 8件 |
| FBI-UAP-D011〜D013（歴史的FBI文書） | 3件 |
| 2024-04-30-composite-sketch.pdf | 1件 |
| DOW-UAP-D078（地図・Notional Map） | 1件 |
| **小計** | **約27件** |

**※3 要確認（約4件）：**
- DOW-UAP-D086（USNavy Report of Flying Discs 1948）：対応ドラフト不明
- DOW-UAP-D087/D088（US Air Force Analysis 1-172）：ai_summary_057/058との同一性要確認

---

## 4. IMG（18件）記事化カバレッジ詳細

| グループ | 件数 | 状態 |
|---|---|---|
| fbi-photo-a1〜a8（PNG画像） | 8件 | 単独記事なし（fbi-photo-b系PDFの関連画像） |
| FBI-UAP-D014〜D023（Western US Eventデジタルレンダリング） | 10件 | 単独記事なし（D077等の付属素材） |
| **合計** | **18件** | **全件：単独記事化なし** |

> IMGは現行R02番号体系（R02-010〜089がVID専用）の**対象外**。  
> D014〜D023はD077系R03記事の挿入素材として参照される想定。  
> fbi-photo-a系は対応するPDF（fbi-photo-b系）の記事内に挿入済み（旧形式ドラフト）。

---

## 5. AUD（0件）

Release 02素材にAUDファイルは含まれない（AUD 11件は全てNASA系 = Release 02対象外）。

---

## 6. 記事化カバレッジ算出

### 6-1. VID（本番号体系の中核管理対象）

| 区分 | 件数 | カバー率 |
|---|---|---|
| 公開済み | 2件 | |
| DONE_CANDIDATE | 76件 | |
| HOLD | 3件 | |
| **記事化対象（管理済み）** | **81件 / 84件** | **96.4%** |
| 管理漏れ（未採番） | 3件 | 3.6% |

### 6-2. PDF（広義のカバレッジ）

| 区分 | 件数 | カバー率 |
|---|---|---|
| 公開済み（R02/R01/R03） | 9件 | |
| ドラフト作成済み（旧形式・R0X未割当） | 約87件 | |
| **広義の記事化着手済み** | **約96件 / 130件** | **約74%** |
| 未記事化（ドラフトなし） | 約27件 | |
| 要確認 | 約4件 | |
| R03候補（ドラフト確認要） | 3件 | |

### 6-3. IMG

| 区分 | 件数 | カバー率 |
|---|---|---|
| 単独記事化対象外 | 18件 / 18件 | 除外（他記事の付属素材） |

### 6-4. 合計サマリー

```
Release 02 カバレッジ監査 最終結果（2026-06-20）

素材総数：232件
  VID :  84件  →  公開済:2 / DONE_CANDIDATE:76 / HOLD:3 / 未採番:3
  PDF : 130件  →  公開済:9 / ドラフトあり:約87 / 未記事化:約27 / 要確認:約7
  IMG :  18件  →  単独記事化対象外:18（他記事付属素材）
  AUD :   0件  →  Release 02に該当なし

VIDカバレッジ  :  81 / 84 = 96.4%（管理漏れ3件）
PDF着手率      :  96 / 130 = 73.8%（article_id未割当が多数）
IMG記事化率    :   0 / 18 = 対象外

完全カバレッジ達成可否：未達成（VID 3件管理漏れのため）
```

---

## 7. 主要発見事項

### 7-1. VID管理漏れ3件（要対応）

現行の `release02_numbering_plan.md` に含まれていない VIDが3件確認された：

| PR番号 | 状況 | 推奨対応 |
|---|---|---|
| **PR052** | files_catalog登録済み・downloaded=true・ドラフトなし | article_id割当 → ドラフト作成 → Codex監査 |
| **PR070** | files_catalog登録済み・downloaded=true・**ドラフトあり** | article_id割当のみで対応可能 |
| **PR098** | files_catalog登録済み・downloaded=true・ドラフトなし | article_id割当 → ドラフト作成 → Codex監査 |

### 7-2. PR057実体不在

`DOW-UAP-PR057` のドラフトは存在するが、files_catalog には PR057 のファイルが登録されていない。  
実体は `PR057a` / `PR057b` の2ファイル。  
既存のPR057ドラフトをPR057a（R02-048）に転用する方向が推奨される。

### 7-3. workflow.db R02エントリ 0件

現時点でworkflow.dbには R02-XXX の article_id エントリが存在しない。  
source_registry に `#R02-001〜003 / #R02-008〜009`（5件、published）のみ登録済み。  
R02-010〜089（80件）はworkflow.db登録待ち状態。

### 7-4. PDF（旧形式ドラフト87件）のarticle_id未割当

旧形式ドラフト（ai_summary_017〜116系）約87件はRelease 02 PDF素材に対応するドラフトだが、  
article_id（R02-XXX）が割り当てられていない。  
現行の R02番号体系（R02-010〜089）はVID専用であり、PDF記事化の番号体系（R02-090以降等）は未設計。

### 7-5. 未記事化PDF 27件の性格

未記事化PDF 27件の内訳：
- **FBI-UAP-D001〜D008/D011〜D013（11件）**: 6/12/26公開。R03候補（FBI証拠資料）
- **DOW mission report 未対応（14件）**: 5/8/26公開。対応VID記事の「関連PDF」として注記する方式の可能性
- **composite-sketch.pdf（1件）**: 4/30/24付。Western US Eventの参考素材と思われる

---

## 8. 推奨アクション（優先順位付き）

### 【P1】VID管理漏れ3件への対応

```
PR052 → 番号割当（R02-090候補?） → ドラフト作成 → Codex監査
PR070 → 番号割当（R02-091候補?） → ドラフト確認のみ
PR098 → 番号割当（R02-092候補?） → ドラフト作成 → Codex監査
```

> ※ 現行numbering_planは R02-062〜089（今回バッチ28件）まで。  
> PR052/070/098をR02-090〜092として追加、または別途検討が必要。

### 【P2】PR057ドラフトの転用

既存の `ai_summary_DOW-UAP-PR057_Spherical_UAP_in_clouds_note_version.md` を  
`ai_summary_DOW-UAP-PR057a_...note_version.md` に改名・転用することを推奨。  
（PR057aのドラフトが現時点で存在しないため）

### 【P3】PR066 作業メモ削除

PR066ドラフトに残存する作業メモ行 `→ 使用ファイル：...` を削除後、Codex iter3実施。

### 【P4】PDF記事化番号体系設計

現行R02体系はVIDのみ（R02-010〜089）。  
PDF記事化をR02の延長で管理する場合、R02-090以降の割当が必要。  
または別シリーズ（PDF専用番号体系）の設計を検討。

---

## 9. source_registry 登録済みR02エントリ

| article_id | 対象ファイル | status |
|---|---|---|
| #R02-001 | DOE-UAP-D001_PANTEX_Image.pdf | published |
| #R02-002 | DOE-UAP-D002_JamesTuck_Correspondence.pdf | published |
| #R02-003 | DOE-UAP-D003_Pajarito_Astronomers.pdf | published |
| #R02-008 | DOW-UAP-PR050_4_UAP_Formation_Iran.mp4 | published |
| #R02-009 | DOW-UAP-PR051_Syrian_UAP_instant_acceleration.mp4 | published |

（#R02-004〜007: 欠番保留、#R02-010〜089: 登録待ち）

---

## 10. workflow.db 管理状況

| article_id | 状態 |
|---|---|
| R02-XXX（全件） | **未登録（0件）** |
| R03-001〜005 | ready_to_publish / preprocessed |
| R01系（CIA/ODNI/D017/PR050等） | published |

R02記事はworkflow.dbへの投入が未実施（source_registry のみ管理中）。

---

**出力ファイル：** `review_reports/release02_coverage_audit_20260620.md`  
**監査実施：** 2026-06-20  
**次回アクション：** P1（VID 3件管理漏れ対応）を優先確認
