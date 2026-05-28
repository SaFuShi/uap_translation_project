# Mac mini UAP データ移行前チェックリスト v1

**制定日:** 2026-05-28
**参照設計書:** `docs/macmini_uap_local_worker_design.md`
**目的:** Mac Studio → Mac mini / agentai / 外付けSSD への安全なデータ移行のため、事前確認項目と作業順序を明確にする

> **重要:** このチェックリストは確認・準備フェーズのみを対象とする。実際のコピー・SSH接続・rsync・ディレクトリ作成・git操作はチェック完了後に別工程として実施する。

---

## 1. 前提

| 項目 | 内容 |
|------|------|
| Mac Studio | 現在の作業・編集・Git管理拠点。`fukudasatoshi` アカウント |
| Mac mini | ローカル処理拠点化予定。`agentai` アカウントで処理を担当 |
| 外付けSSD | ACASIS 2TB。マウントポイント: `/Volumes/ACASIS_2TB/` |
| 移行先ベースパス | `/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/` |

---

## 2. 移行対象

以下のディレクトリ・ファイルを Mac mini 側へコピーする。

| 対象 | 優先度 | 理由 |
|------|--------|------|
| `raw_pdf/` | 最優先 | OCR処理の入力素材（122件・約2.4GB）|
| `raw_media/audio/` | 最優先 | 音声文字起こし処理の入力素材（8件）|
| `raw_media/image/` | 最優先 | 画像処理の入力素材（14件）|
| `raw_media/video/` | 最優先 | 動画フレーム抽出の入力素材（78件）|
| `metadata/files_catalog.csv` | 最優先 | 処理状態管理の基準となるカタログ |
| `page_images/` | 必要に応じて | PDF画像変換済みファイルがある場合 |
| `extracted_text/` | 必要に応じて | OCR抽出済みテキストがある場合 |

---

## 3. 移行対象外

以下はコピーしない。

| 対象外 | 理由 |
|--------|------|
| `.git/` | Git管理はMac Studio側で行う。Mac miniはclone別工程で実施 |
| `metadata/uap-csv-cache.csv` | war.gov生キャッシュ。再取得可能・頻繁に変化 |
| `metadata/text_layer_report.csv` | スクリプト生成物。Mac mini側で再生成可能 |
| `*.tmp` / `*.log` の一時ファイル | 移行不要 |
| `logs/` 配下の巨大ログ | 移行不要（Mac mini側で新規生成する）|
| `note_drafts/` | 編集はMac Studio側で行う。後回し |
| `published_articles/` | 公開済み記事管理はMac Studio側で行う |

---

## 4. 事前確認コマンド

### 4-1. Mac Studio 側で実行する確認コマンド

以下を **この順番で** 実行し、結果を記録してから Mac mini 側の確認へ進む。

```bash
# 1. 作業ディレクトリの確認
pwd

# 2. Git 作業ツリーの状態確認（未コミット変更がないか）
git status --short

# 3. 主要ディレクトリの容量確認
du -sh raw_pdf raw_media metadata

# 4. PDF ファイル数確認
find raw_pdf -type f | wc -l

# 5. raw_media 全ファイル数確認
find raw_media -type f | wc -l

# 6. メディアタイプ別ファイル数確認
find raw_media/audio -type f | wc -l
find raw_media/image -type f | wc -l
find raw_media/video -type f | wc -l
```

**期待値（現時点）:**

| コマンド | 期待値 |
|---------|--------|
| `find raw_pdf -type f \| wc -l` | 122 |
| `find raw_media -type f \| wc -l` | 100 |
| `find raw_media/audio -type f \| wc -l` | 8 |
| `find raw_media/image -type f \| wc -l` | 14 |
| `find raw_media/video -type f \| wc -l` | 78 |
| `du -sh raw_pdf` | 約 2.4 GB |
| `du -sh raw_media` | 約 6.6 GB |

> 期待値と一致しない場合は、移行前に原因を確認する。

### 4-2. Mac mini / agentai 側で実行する確認コマンド

Mac mini にログインし、以下を実行して環境を確認する。

```bash
# 1. ログインユーザーの確認（agentai であること）
whoami

# 2. ホスト名の確認
hostname

# 3. 外付けSSDのマウント確認
ls /Volumes/ACASIS_2TB/AI_Data

# 4. 空き容量の確認（raw_pdf 2.4GB + raw_media 6.6GB = 約9GB以上必要）
df -h /Volumes/ACASIS_2TB

# 5. 現在いるディレクトリの確認
pwd
```

**確認ポイント:**

| 確認項目 | 合格基準 |
|---------|---------|
| `whoami` | `agentai` であること（root でないこと）|
| `ls /Volumes/ACASIS_2TB/AI_Data` | ディレクトリが存在すること |
| `df -h /Volumes/ACASIS_2TB` | 空き容量が **20GB 以上** あること（余裕を持たせる）|

---

## 5. 推奨ディレクトリ構成（作成候補）

Mac mini 側の移行先に以下のディレクトリを作成する方針。**実際の作成は別工程**。

```
/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/
├── repo/                   # Git clone先（別工程）
├── raw_pdf/                # ← Mac Studio からコピー
├── raw_media/
│   ├── audio/              # ← Mac Studio からコピー
│   ├── image/              # ← Mac Studio からコピー
│   └── video/              # ← Mac Studio からコピー
├── metadata/               # files_catalog.csv のみコピー
├── page_images/            # 空で作成（処理後に生成される）
├── extracted_text/         # 空で作成（処理後に生成される）
├── frame_extracts/         # 空で作成（処理後に生成される）
├── transcripts/            # 空で作成（処理後に生成される）
├── ocr_outputs/            # 空で作成（処理後に生成される）
├── worker_outputs/         # 空で作成（処理後に生成される）
├── logs/
│   ├── worker/
│   ├── ocr/
│   ├── transcript/
│   └── nightly/
└── jobs/                   # 空で作成（ジョブファイル配置先）
```

> **注意:** `raw_video/` / `raw_image/` / `raw_audio/` は作成しない。Mac Studio 側の `raw_media/audio/` / `raw_media/image/` / `raw_media/video/` 構成を踏襲する。

---

## 6. コピー方針と実行順序

実際のコピーは別工程だが、順序と方針を以下に定める。

### 6-1. コピー実行順序

```
Step A: Mac mini 側でディレクトリ構成を作成
         （別工程。このチェックリストの確認完了後）

Step B: metadata/files_catalog.csv のみ先行コピー
         rsync --dry-run で差分確認 → 実行 → 行数照合

Step C: raw_pdf/ のコピー
         rsync --checksum --dry-run → 差分確認 → 実行
         コピー後: find raw_pdf -type f | wc -l で件数一致確認

Step D: raw_media/audio/ のコピー
         rsync --checksum --dry-run → 差分確認 → 実行
         コピー後: find raw_media/audio -type f | wc -l で件数一致確認

Step E: raw_media/image/ のコピー
         rsync --checksum --dry-run → 差分確認 → 実行
         コピー後: find raw_media/image -type f | wc -l で件数一致確認

Step F: raw_media/video/ のコピー
         rsync --checksum --dry-run → 差分確認 → 実行
         コピー後: find raw_media/video -type f | wc -l で件数一致確認

Step G: Git repo の clone（別工程）
         Mac mini 側で git clone を実行
```

### 6-2. rsync 基本オプション

```bash
# 必ず --dry-run を先に実行して差分を確認する
rsync -av --checksum --dry-run \
  /path/mac_studio/raw_pdf/ \
  agentai@mac-mini.local:/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/raw_pdf/

# 差分に問題がなければ --dry-run を外して実行
rsync -av --checksum \
  /path/mac_studio/raw_pdf/ \
  agentai@mac-mini.local:/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/raw_pdf/
```

### 6-3. コピー後の照合確認コマンド

コピー完了後、Mac Studio 側と Mac mini 側で以下を比較する。

```bash
# Mac Studio 側
find raw_pdf -type f | sort | wc -l
du -sh raw_pdf

# Mac mini 側（比較用）
find /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/raw_pdf -type f | sort | wc -l
du -sh /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/raw_pdf
```

---

## 7. 安全ルール

移行作業全体を通じて、以下のルールを厳守する。

| ルール | 内容 |
|--------|------|
| root 実行禁止 | すべての操作は `agentai` ユーザーで行う |
| chmod 777 禁止 | 必要最小権限のみ付与する |
| 削除系コマンド禁止 | `rm` / `rmdir` / `git clean` は使用しない |
| `rsync --delete` 禁止 | 誤削除リスクのため付けない |
| Git commit / push 禁止 | 移行作業中は Git 操作を行わない |
| 不明なエラー時は停止 | エラー内容を記録して報告。自動で次へ進まない |
| `--dry-run` 必須 | rsync は必ず dry-run で差分を確認してから実行する |

---

## 8. 完了条件

### 8-1. このチェックリストの完了条件（準備フェーズ）

- [ ] `docs/macmini_uap_migration_checklist.md` が作成されている
- [ ] 実際の移行作業はまだ行っていない
- [ ] Mac Studio 側の確認コマンドが明確になっている
- [ ] Mac mini 側の確認コマンドが明確になっている
- [ ] 移行対象・移行対象外が整理されている

### 8-2. 移行作業の完了条件（実施フェーズ）

- [ ] Mac Studio 側の事前確認コマンドが全て実行され、期待値と一致している
- [ ] Mac mini 側で `whoami` = `agentai` であることを確認している
- [ ] Mac mini 側で空き容量 20GB 以上を確認している
- [ ] Mac mini 側のディレクトリ構成が作成されている
- [ ] `metadata/files_catalog.csv` がコピーされ、行数が一致している
- [ ] `raw_pdf/` がコピーされ、ファイル数（122件）が一致している
- [ ] `raw_media/audio/`（8件）・`raw_media/image/`（14件）・`raw_media/video/`（78件）がコピーされ、件数が一致している
- [ ] コピー後に Mac mini 側で `detect_text_layer.py` が PDF 1件に対して正常実行できる

---

## 9. 次に人間が実行すべきコマンド一覧

### Mac Studio 側（今すぐ実行可能）

```bash
pwd
git status --short
du -sh raw_pdf raw_media metadata
find raw_pdf -type f | wc -l
find raw_media -type f | wc -l
find raw_media/audio -type f | wc -l
find raw_media/image -type f | wc -l
find raw_media/video -type f | wc -l
```

### Mac mini / agentai 側（Mac mini にログイン後に実行）

```bash
whoami
hostname
ls /Volumes/ACASIS_2TB/AI_Data
df -h /Volumes/ACASIS_2TB
pwd
```

上記の結果を確認し、期待値と一致していればディレクトリ作成・rsync 工程へ進む。

---

## 改訂履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| v1 | 2026-05-28 | 初版制定 |
