# Source Registry Policy — 同一PDF二重記事化防止ルール

**制定日：** 2026-05-13  
**適用対象：** UAP Translation Project — AI概要版全ドラフト（#001以降）  
**重要度：** 公開信頼性インシデントとして扱う（軽微ミスではない）

---

## 基本方針

**同一PDFの二重記事化は、公開信頼性に関わるインシデントとして扱う。**

ドラフト生成前に必ず `source_registry.csv` で重複確認を行い、重複が検出された場合は生成を停止する。

---

## source_registry.csv

**保存先：** `review_logs/source_registry.csv`

### カラム定義

| カラム名 | 説明 |
|---|---|
| article_id | 記事番号（例: #036） |
| pdf_file_name | 元PDFのファイル名 |
| source_url | WAR.GOV等の公開URL |
| pdf_sha256 | PDFのSHA256ハッシュ（重複防止の主キー） |
| status | ステータス（下記参照） |
| note_url | 公開記事のnote URL |
| draft_path | ドラフトファイルのパス |
| published_path | 公開版ファイルのパス |
| created_date | レジストリ登録日 |
| published_date | note公開日 |
| remarks | 備考 |

### status 定義

| status | 意味 |
|---|---|
| `draft` | 作成済みだが未公開 |
| `reviewing` | Phase 1/2 レビュー中 |
| `published` | note公開済み |
| `hold` | 保留中（問題あり・後日対応） |
| `archived` | 廃止・旧版 |

---

## 重複チェック手順

### Step 1 — スクリプトによる自動チェック

ドラフト生成前に必ず以下を実行する：

```bash
python3 scripts/check_duplicate_source.py <pdf_file_name> --next-id "#037"
```

または複数PDFの一括チェック：

```bash
python3 scripts/check_duplicate_source.py --batch \
  dow-uap-d12-mission-report-iraq-may-2022.pdf \
  dow-uap-d14-mission-report-iraq-may-2022.pdf \
  dow-uap-d16-mission-report-syria-july-2022.pdf \
  --start-id 37
```

### Step 2 — チェック結果の判定

| 結果 | 意味 | アクション |
|---|---|---|
| `PASS` / `new` | 未使用PDF。新規ドラフト生成可 | 生成を進める |
| `BLOCK` / `existing` | 既登録PDF（同名またはSHA256一致）。重複 | 生成停止。人間が確認 |

### Step 3 — BLOCK 時の出力例

```
RESULT: BLOCK — 重複ソース検出

  requested_article_id : #037
  pdf_file_name        : dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.pdf

  既存エントリ:
    article_id    : #009
    status        : published
    note_url      : unknown
    match_reason  : pdf_file_name, pdf_sha256

→ 人間の明示確認なしに新規ドラフトを生成しないでください。
```

---

## 既知の二重記事化インシデント

| 件 | article_id_1 | article_id_2 | pdf_file_name | 対応 |
|---|---|---|---|---|
| 1 | #009 | #036 | dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.pdf | #036はend-to-endテスト記事として承認済み。以降同一PDF使用禁止。 |

---

## registry 更新ルール

新規ドラフトを生成・公開するたびに `source_registry.csv` を更新する。

### 更新タイミング

1. **ドラフト生成時**：status = `draft` で登録
2. **Phase 1/2 レビュー中**：status = `reviewing` へ更新
3. **note公開時**：status = `published`、`note_url`・`published_date` を追加
4. **保留決定時**：status = `hold`
5. **廃止時**：status = `archived`

---

## #037〜#050 候補選定ルール

1. `check_duplicate_source.py --batch` で全候補をチェックする
2. `BLOCK` のPDFは候補リストから除外する
3. `PASS` のPDFのみを候補として提示する
4. 候補一覧には `duplicate_check` / `registry_status` を必ず表示する

---

## 関連ファイル

| ファイル | 内容 |
|---|---|
| `review_logs/source_registry.csv` | PDF登録台帳（主ファイル） |
| `scripts/check_duplicate_source.py` | 重複チェックスクリプト |
| `docs/review_standard_v1.md` | Phase 1/2 レビュー基準 |
