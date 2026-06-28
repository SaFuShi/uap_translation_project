# Release 02 前バッチ33件 正式登録前修正レポート
**作成日：** 2026-06-20  
**対象：** DOW-UAP-PR019〜PR049（27件）+ FBI-UAP-PR001〜006（6件）  
**処理モード：** SKIP AND CONTINUE  

---

## 1. 実施サマリー

| 修正項目 | 対象 | 件数 | 結果 |
|---|---|---|---|
| 作業メモ行削除 | 全33件 | 33件 | **完了** |
| フレームレート修正（30fps→24fps） | FBI-PR001 | 1件 | **完了** |
| フレームレート修正（30fps→10fps） | PR035 | 1件 | **完了** |
| DVIDS Title言及追加（「Resolved as Aircraft」） | PR038 | 1件 | **完了** |
| Incident Date修正（「2021年」→「2021年11月」） | FBI-PR001 | 1件 | **完了** |
| Codex再監査（iter2/iter3） | 全33件 | 33件 | **完了** |

---

## 2. 修正詳細

### 2-1. 作業メモ行削除（全33件）

- **削除パターン：** `^→ 使用ファイル：…（note転記後にこの行を削除）`
- **対象：** PR019/021/022/023/026/027/028/029/031/032/033/034/035/036/037/038/039/040/041/042/043/044/045/046/047/048/049 + FBI-PR001〜006
- **結果：** 33件全件で作業メモ行残存ゼロ確認

### 2-2. FBI-PR001 フレームレート修正

- **誤：** `フレームレート：30fps`
- **正：** `フレームレート：24fps`
- **根拠：** metadata.json / ffprobe 実測値 24fps

### 2-3. PR035 フレームレート修正

- **誤：** `フレームレート：30fps`
- **正：** `フレームレート：10fps`
- **根拠：** ffprobe video avg_frame_rate / r_frame_rate = 10/1

### 2-4. PR038 DVIDS Title言及追加

- **追加内容：**  
  `DVIDS Video Title：「Resolved as an Aircraft, Middle East 2013」（uap-csv-cache.csvより）。ファイル名は「Unresolved」だが、DVIDSのビデオタイトルは航空機として解決済みを示している。本映像からは解決・未解決を確認できない。`
- **理由：** iter2で P1-DVIDS-TITLE BLOCK（一次メタデータ上の重大な不一致が未説明）

### 2-5. FBI-PR001 Incident Date修正

- **誤：** `2021年（ファイル名「2021」より。具体的な月・日付は不明）`
- **正：** `2021年11月（files_catalog.csv より。ファイル名「2021」とも整合する）`
- **根拠：** files_catalog.csv の incident_date = "November, 2021"
- **同時修正：** AI解析メモのファイル名由来「2021年」→「2021年11月（files_catalog.csvより）」

---

## 3. Release Date確認（PR038等のP1-DATE BLOCK再確認）

| 対象 | ドラフトの Release Date | Codex判定 |
|---|---|---|
| PR038 | 2026年05月08日 | iter3で P1-DATE BLOCKなし ✓ |
| PR039 | 2026年05月08日 | iter2で P1-DATE BLOCKなし ✓ |
| PR041 | 2026年05月08日 | iter2で P1-DATE BLOCKなし ✓ |
| PR042 | 2026年05月08日 | iter2で P1-DATE BLOCKなし ✓ |
| PR044 | 2026年05月08日 | iter2で P1-DATE BLOCKなし ✓ |
| PR046 | 2026年05月08日 | iter2で P1-DATE BLOCKなし ✓ |

→ **全件 2026年05月08日（正）。Release Date BLOCKはCodexリクエスト再生成後に解消。**

---

## 4. Codex再監査 最終結果（全33件）

### 4-1. 集計

| 最終VERDICT | 件数 |
|---|---|
| WARN（実質BLOCK = 0） | 8件 |
| BLOCK（source_registry系のみ） | 25件 |
| 実質BLOCK（DONE_CANDIDATE非該当） | **0件** |

### 4-2. 全件一覧

| No. | PR番号 | 最終iter | VERDICT | 実質BLOCK | 判定 |
|---|---|---|---|---|---|
| 1 | PR019 | iter2 | BLOCK | なし（P1-1a/b/c=source_registry系） | DONE_CANDIDATE |
| 2 | PR021 | iter2 | BLOCK | なし（P1-1-FILENAME=source_registry系） | DONE_CANDIDATE |
| 3 | PR022 | iter2 | WARN | - | DONE_CANDIDATE |
| 4 | PR023 | iter2 | BLOCK | なし（P1-1-FILENAME=source_registry系） | DONE_CANDIDATE |
| 5 | PR026 | iter2 | BLOCK | なし（P1-1a/b=source_registry系） | DONE_CANDIDATE |
| 6 | PR027 | iter2 | BLOCK | なし（P1-1-FILENAME/SOURCE=source_registry系） | DONE_CANDIDATE |
| 7 | PR028 | iter2 | WARN | - | DONE_CANDIDATE |
| 8 | PR029 | iter2 | BLOCK | なし（P1-1c=URL設計） | DONE_CANDIDATE |
| 9 | PR031 | iter2 | WARN | - | DONE_CANDIDATE |
| 10 | PR032 | iter2 | WARN | - | DONE_CANDIDATE |
| 11 | PR033 | iter2 | BLOCK | なし（P1-1-FILENAME/SOURCE_URL=source_registry系） | DONE_CANDIDATE |
| 12 | PR034 | iter2 | BLOCK | なし（P1-5-DUP=PDF重複・別フォーマット許容） | DONE_CANDIDATE |
| 13 | PR035 | **iter3** | BLOCK | なし（P1-1-SOURCE-REGISTRY/URL=source_registry系） | DONE_CANDIDATE |
| 14 | PR036 | iter2 | WARN | - | DONE_CANDIDATE |
| 15 | PR037 | iter2 | BLOCK | なし（P1-REG=source_registry系） | DONE_CANDIDATE |
| 16 | PR038 | **iter3** | BLOCK | なし（P1-REG=source_registry系・DVIDS Title追加済み） | DONE_CANDIDATE |
| 17 | PR039 | iter2 | BLOCK | なし（P1-REG=source_registry系） | DONE_CANDIDATE |
| 18 | PR040 | iter2 | BLOCK | なし（P1-REG=source_registry系） | DONE_CANDIDATE |
| 19 | PR041 | iter2 | BLOCK | なし（P3-REG=source_registry系） | DONE_CANDIDATE |
| 20 | PR042 | iter2 | BLOCK | なし（P3-REG=source_registry系） | DONE_CANDIDATE |
| 21 | PR043 | iter2 | WARN | - | DONE_CANDIDATE |
| 22 | PR044 | iter2 | BLOCK | なし（P1-REG=source_registry系） | DONE_CANDIDATE |
| 23 | PR045 | iter2 | BLOCK | なし（P1-1-REGISTRY=source_registry系） | DONE_CANDIDATE |
| 24 | PR046 | iter2 | BLOCK | なし（P1-REG=source_registry系、P1-DUP=確認不能） | DONE_CANDIDATE |
| 25 | PR047 | iter2 | WARN | - | DONE_CANDIDATE |
| 26 | PR048 | iter2 | BLOCK | なし（P1-REG=source_registry系） | DONE_CANDIDATE |
| 27 | PR049 | iter2 | BLOCK | なし（P1-1-REGISTRY=source_registry系） | DONE_CANDIDATE |
| 28 | FBI-PR001 | **iter3** | BLOCK | なし（P1-1-REGISTRY=source_registry系・fps/date修正済み） | DONE_CANDIDATE |
| 29 | FBI-PR002 | iter2 | BLOCK | なし（P1-1=source_registry系） | DONE_CANDIDATE |
| 30 | FBI-PR003 | iter2 | BLOCK | なし（P3=source_registry系） | DONE_CANDIDATE |
| 31 | FBI-PR004 | iter2 | BLOCK | なし（P1-1B=URL設計） | DONE_CANDIDATE |
| 32 | FBI-PR005 | iter2 | WARN | - | DONE_CANDIDATE |
| 33 | FBI-PR006 | iter2 | BLOCK | なし（P3-1=source_registry系） | DONE_CANDIDATE |

### 4-3. 残留 BLOCK 種別の解説

| BLOCK種別 | 件数 | 判定理由 |
|---|---|---|
| source_registry未登録（P1-REG/P1-1a/P1-1-REGISTRY等） | 全件共通 | 在庫化で解消。DONE_CANDIDATE許容 |
| WAR.GOV URLトップページ（P1-1c/P1-1B等） | 複数件 | 全件共通の設計。直接URLなし。許容 |
| ファイル名マッチ（P1-1-FILENAME等） | 複数件 | source_registry系の変形。許容 |
| 同一DVIDS ID PDF重複（P1-5-DUP等） | PR034 | PDF別フォーマット。記事内参照を推奨するが許容 |

---

## 5. 変更ファイル一覧

### note_drafts/（計5件修正）

| ファイル | 変更内容 |
|---|---|
| ai_summary_DOW-UAP-PR035_*_note_version.md | フレームレート 30fps → 10fps |
| ai_summary_DOW-UAP-PR038_*_note_version.md | DVIDS Title「Resolved as Aircraft」言及追加 |
| ai_summary_FBI-UAP-PR001_*_note_version.md | フレームレート 30fps → 24fps / Incident Date 2021年 → 2021年11月（2箇所） |

**全33件：** 作業メモ行（`→ 使用ファイル：…`）削除

### review_requests/（33件更新）

再生成日付: 2026-06-20
対象: PR019〜049（27件）+ FBI-PR001〜006（6件）

### review_reports/（新規36件）

- `codex_audit_20260620_DOW-UAP-PR019_*_iter2.md` 〜 `FBI-UAP-PR006_*_iter2.md`（33件）
- `codex_audit_20260620_DOW-UAP-PR035_*_iter3.md`
- `codex_audit_20260620_DOW-UAP-PR038_*_iter3.md`
- `codex_audit_20260620_FBI-UAP-PR001_*_iter3.md`

---

## 6. 最終登録可能件数

| 分類 | 件数 | 備考 |
|---|---|---|
| **DONE_CANDIDATE** | **33件** | 正式登録可能 |
| HOLD | **0件** | - |
| SKIP | **0件** | - |

**全33件が正式登録可能（DONE_CANDIDATE）**

---

## 7. 正式登録前の残タスク（人間側）

以下は正式登録（source_registry登録 / workflow.db登録）の前に確認が必要な事項。

### 必須
- [ ] PR034：DVIDS ID重複PDF（dow-uap-d33-mission-report-greece-october-2023）との関係を記事内に「関連PDF記事：#032」として追記推奨
- [ ] PR038：DVIDS Title「Resolved as Aircraft」の言及が記事内で適切か最終確認

### 推奨（公開preflight時）
- [ ] 全33件：「注意点」「免責」セクションを独立見出しとして追加
- [ ] 全33件：タイトル「#TBD」を正式 article_id に更新
- [ ] PR047：全件共通の標準構成「注意点」独立化

---

## 8. 参照ファイル

- 番号体系計画：`review_reports/release02_numbering_plan.md`
- 今回バッチ dry-run：`review_reports/ready_to_publish_plan_20260620_PR071-PR099.md`

---

**出力ファイル：** `review_reports/release02_prebatch_fix_report.md`  
**作成：** 2026-06-20（修正実施後）
