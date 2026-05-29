# Mac mini ローカル処理拠点 設計書 v1

**制定日:** 2026-05-28
**対象環境:** Mac mini / agentai アカウント / 外付けSSD（ACASIS 2TB）
**関連方針書:** `docs/release02_media_processing_policy_v1.md`

---

## 0. 設計の目的

現在 Mac Studio 側で行っている重い下処理（OCR・動画フレーム抽出・音声文字起こし）を Mac mini の `agentai` アカウントで実行できるようにする。Claude Code / Codex / ChatGPT の API コストと処理時間を削減し、Mac Studio 側を司令塔・編集・公開専用に特化させる。

**Mac mini を選ぶ理由:**
- 電力効率が高く夜間連続稼働に適している
- ローカル処理のため、機密性の高い政府公開資料を外部 API に送らずに処理できる
- `agentai` アカウントで権限を分離し、誤操作リスクを低減できる

---

## 1. Mac Studio と Mac mini の役割分担

### 1-1. Mac Studio（司令塔・編集・公開）

| 役割 | 内容 |
|------|------|
| 司令塔 | 全体の処理方針決定・ジョブ指示 |
| Git 管理 | commit / push / PR はすべて Mac Studio 側で行う |
| 記事編集 | note_drafts/ の最終編集・Codex レビュー指示 |
| note 投稿 | published_articles/ 管理・note 公開 |
| 最終判断 | 公開可否・source_registry.csv 本番更新 |
| Claude Code / Codex 連携 | API 呼び出し・レビュー依頼 |

### 1-2. Mac mini / agentai（素材処理ワーカー）

| 役割 | 内容 |
|------|------|
| 素材保管 | raw_pdf / raw_media / page_images の一次保管 |
| OCR | テキスト層検出 → OCR 実行 → extracted_text 出力 |
| 動画フレーム抽出 | 代表フレームの抽出 → frame_extracts/ 保存 |
| 音声文字起こし | Whisper 等によるローカル文字起こし → transcripts/ 保存 |
| 素材カード生成 | worker_outputs/ に JSON 素材カードを出力 |
| 夜間バッチ | 手動→小規模自動→拡張の段階的移行 |

**Mac mini では行わない作業:**
- note 本文の最終生成
- UFO/UAP の断定的解釈
- 公開可否判断
- source_registry.csv の本番更新
- published_articles/ の操作
- note 投稿

---

## 2. Mac mini 側ディレクトリ構成

ベースパス: `/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/`

```
/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/
├── repo/                        # Git リポジトリ（Mac Studio からの clone）
│   ├── docs/
│   ├── scripts/
│   └── metadata/                # 軽量 CSV のみ（後述）
│
├── raw_pdf/                     # PDF 本体（Git 管理外）
├── raw_media/
│   ├── audio/                   # AUD ファイル実体（.mp4 コンテナ）
│   ├── image/                   # IMG ファイル（.png / .jpg）
│   └── video/                   # VID ファイル（.mp4）
│
├── page_images/                 # PDF → 画像変換後の中間ファイル
├── extracted_text/              # OCR・テキスト抽出結果（.txt / .json）
├── frame_extracts/              # 動画代表フレーム画像
├── transcripts/                 # 音声文字起こし結果（.txt / .json）
├── ocr_outputs/                 # OCR 処理中間ファイル
├── worker_outputs/              # 素材カード JSON・要約 CSV
│
├── logs/
│   ├── worker/                  # 汎用ワーカーログ
│   ├── ocr/                     # OCR 実行ログ
│   ├── transcript/              # 文字起こしログ
│   └── nightly/                 # 夜間バッチ実行ログ
│
└── jobs/                        # 実行待ちジョブファイル（JSON）
```

**注意:**
- `raw_video/` / `raw_image/` / `raw_audio/` は**作らない**
- Mac Studio 側の `raw_media/audio/` / `raw_media/image/` / `raw_media/video/` の構成をそのまま踏襲する

---

## 3. Git 管理するもの・しないもの

### 3-1. Git 管理する（repo/ 以下に含める）

| 対象 | 理由 |
|------|------|
| `docs/` | 方針書・設計書の共有 |
| `scripts/` | 処理スクリプトのバージョン管理 |
| `metadata/files_catalog.csv` | カタログの状態管理（軽量） |
| `metadata/manual_download_required.csv` | 手動DLリスト（軽量） |
| `review_reports/` | Codex 監査結果の共有 |
| `worker_outputs/` の要約 CSV / JSON（軽量のもの） | 素材カードのサマリー共有 |

### 3-2. Git 管理しない（.gitignore で除外）

| 対象 | 理由 |
|------|------|
| `raw_pdf/` | 大容量（合計 2.4 GB 超）|
| `raw_media/` | 大容量（合計 6.6 GB 超）|
| `page_images/` | OCR 中間生成物・再生成可能 |
| `frame_extracts/` | 動画中間生成物・再生成可能 |
| `transcripts/` の大容量ファイル | Whisper 出力は再実行可能 |
| `ocr_outputs/` | OCR 中間生成物 |
| `logs/` の巨大ログ | 運用ログは Git 管理不要 |
| `metadata/uap-csv-cache.csv` | war.gov 生キャッシュ（頻繁に変化）|
| `metadata/text_layer_report.csv` | スクリプト生成物・再生成可能 |

---

## 4. Mac Studio から Mac mini へのデータ移行方針

### 4-1. 基本方針

- **一気に全自動化しない。段階的に移行する**
- 各ステップで件数・容量・ファイル名一致を人間が確認してから次へ進む
- Git commit は原則 Mac Studio 側で行う。Mac mini は repo の pull のみ

### 4-2. 移行ステップ

```
Step 1: metadata のみ移行・確認
   Mac Studio → Mac mini
   対象: metadata/files_catalog.csv
   確認: 行数・列数・Release 01/02 件数の一致

Step 2: raw_pdf/ 移行・確認
   対象: raw_pdf/ 以下の全 PDF（122 件・約 2.4 GB）
   手段: rsync --checksum（チェックサム検証付き）
   確認: ファイル数・合計サイズ・ランダム 5 件のファイル名照合

Step 3: raw_media/ 移行・確認
   対象: raw_media/audio/ / raw_media/image/ / raw_media/video/
   手段: rsync --checksum
   確認: audio 8 件 / image 14 件 / video 78 件・合計 100 件

Step 4: scripts/ / docs/ の clone または pull
   手段: git clone（repo/ に）
   確認: git log --oneline で最新 commit が一致するか

Step 5: Mac mini 側での動作確認
   対象スクリプト: detect_text_layer.py（PDF 1 件で試験実行）
   確認: output が extracted_text/ に正常出力されるか
```

### 4-3. rsync オプション指針

```bash
# 基本形（実行前に --dry-run で確認必須）
rsync -av --checksum --dry-run \
  /path/to/mac_studio/raw_pdf/ \
  agentai@mac-mini.local:/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/raw_pdf/
```

- `--dry-run` を必ず先に実行し、差分を確認してから本実行する
- `--delete` は慎重に使用する（誤削除リスクあり）

---

## 5. ローカル LLM に任せる作業・任せない作業

### 5-1. 任せる（Mac mini ローカル LLM）

| 作業 | 出力先 |
|------|--------|
| OCR 結果整形（誤認字補正候補の提示） | ocr_outputs/ |
| OCR 不可理由分類（ocr_failure_reason 判定） | worker_outputs/ |
| PDF ページごとの素材カード作成 | worker_outputs/ |
| 動画代表フレームの視覚観察メモ候補 | worker_outputs/ |
| 音声文字起こし後の要点抽出候補 | worker_outputs/ |

### 5-2. 任せない（必ず Mac Studio / 人間が担当）

| 作業 | 理由 |
|------|------|
| note 本文の最終生成 | 品質・provenance 保証が必要 |
| UFO/UAP の断定的解釈 | 編集方針違反リスク |
| 公開可否判断 | 人間の最終判断が必要 |
| source_registry.csv の本番更新 | データ整合性リスク |
| published_articles/ 操作 | 公開済みコンテンツへの影響 |
| note 投稿 | 対外発信は人間が行う |

---

## 6. OCR Challenge Pipeline

通常 PDF 処理ラインと分岐し、OCR 不可ファイルを別管理する。

### 6-1. 通常ライン

```
PDF
 └─ ocr_status: not_needed / partial（テキスト抽出済み）
      ↓
    detect_text_layer.py → extracted_text/
      ↓
    run_ocr.py（必要なページのみ）
      ↓
    extracted_text/ に .txt / .json 出力
      ↓
    素材カード生成 → worker_outputs/
      ↓
    Mac Studio 側で translation / summary / note draft へ
```

### 6-2. OCR Challenge Pipeline

```
PDF
 └─ ocr_status: needed（OCR 失敗・テキスト取得不可）
      ↓
    ocr_failure_reason 分類
    ├─ handwriting          : 手書き文字が多い
    ├─ low_resolution       : 解像度不足・文字潰れ
    ├─ poor_contrast        : コントラスト不足
    ├─ skew_or_rotation     : 傾き・回転・スキャン歪み
    ├─ redacted_or_cropped  : 黒塗り・欠損・切れ
    ├─ image_only_non_text  : 写真・図版中心（文字なし）
    ├─ unknown_file_structure: 構造不明・解析方法未確定
    └─ corrupted_or_unreadable: ファイル破損・読み込み不能
      ↓
    画像品質診断
    （image_quality: poor / fair / good）
    （text_visibility: none / partial / most / full）
      ↓
    補正候補判定（recommended_next_step）
    ┌─ retry_ocr_high_resolution
    ├─ retry_ocr_after_contrast_adjustment
    ├─ retry_ocr_after_deskew
    ├─ ai_vision_review
    ├─ human_visual_review
    └─ hold_no_article
      ↓
    実施
    ├─ retry_ocr_*: 補正後に run_ocr.py 再実行
    ├─ ai_vision_review: ローカル Vision モデルで画像読み取り
    └─ human_visual_review: Mac Studio 側で人間確認依頼
      ↓
    記事化可否判断
    ├─ 可: 通常ラインの素材カード生成以降へ合流
    └─ 不可: hold_no_article → ocr_challenge_log.csv に記録
              logs/ocr/ に停止理由を記録して停止
```

### 6-3. OCR Challenge 結果の記録フォーマット（ocr_challenge_log.csv）

```
file_name, page_number, ocr_failure_reason, image_quality,
text_visibility, recommended_next_step, result_status,
human_review_needed, reviewed_by, reviewed_at, notes
```

**重要:** OCR Challenge 経由の結果は通常 OCR と同等扱いしない。記事内で情報源種別（OCR / AI Vision / 目視）を必ず明記する。

---

## 7. 夜間バッチ方針

### 7-1. 段階的移行

```
Phase 1: 手動実行
  - スクリプトを手動で 1 件ずつ実行
  - 出力・ログを目視確認
  - 問題なければ Phase 2 へ

Phase 2: 小規模夜間実行
  - 対象: 1〜5 件の PDF / VID / AUD
  - jobs/ に実行ジョブファイルを置き、スクリプトが読む方式
  - 翌朝 logs/nightly/ を確認してから次のジョブを投入

Phase 3: 複数ファイルへ拡張
  - Phase 2 で問題が出なければ対象を拡大
  - launchd による自動起動は Phase 2 完了後に設計する
```

### 7-3. 長時間処理の実行方式

#### 原則

**Claude Code のバックグラウンドタスクハーネスに長時間処理を依存させない。**

Claude Code の背景実行（Background Task）は SSH 経由の接続を保持するが、Claude Code セッション側のコンテキスト切れ・ネットワーク断・ハーネス終了により、Mac mini 側プロセスが途中終了することがある。また SSH クライアントが切断されると tee パイプが SIGPIPE を受け、Python スクリプト自体も強制終了するリスクがある。

#### 推奨実行方式

| 方式 | 適用場面 | コマンド例 |
|------|---------|----------|
| **tmux（推奨）** | 全長時間バッチ（OCR / Whisper / ffmpeg） | `tmux new-session -d -s ocr-batch 'python3 scripts/run_ocr.py ... 2>&1 \| tee logs/ocr/ocr_run_YYYYMMDD.log'` |
| **nohup（代替）** | tmux が使えない環境 | `nohup python3 scripts/run_ocr.py ... > logs/ocr/ocr_run_YYYYMMDD.log 2>&1 &` |
| **Claude Code background** | 短時間処理のみ（5分以内を目安） | Claude Code の Task 機能。長時間は使わない |

#### tmux を使った起動手順（標準パターン）

```bash
# 1. Mac mini に SSH ログイン
ssh agentai

# 2. 既存セッション確認
tmux ls

# 3. セッション作成して起動（Mac mini 上で実行）
eval "$(/opt/homebrew/bin/brew shellenv)"
cd /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/repo
source /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/.venv/bin/activate
TS=$(date +%Y%m%d_%H%M%S)
tmux new-session -d -s ocr-batch \
  "python3 scripts/run_ocr.py \
    --input-root /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/page_images/ \
    --output-file extracted_text/ocr_results_full_${TS}.csv \
    2>&1 | tee logs/ocr/ocr_run_${TS}.log"

# 4. SSH を切断（tmux セッションは Mac mini 上で継続）
exit
```

#### Claude Code の役割（長時間処理時）

| 役割 | 内容 |
|------|------|
| 起動指示 | tmux セッション起動コマンドを生成・説明する |
| 進捗確認 | SSH 経由で `tail -f` / `tmux attach -r` / `ps aux` で確認 |
| 結果確認 | 処理完了後に出力 CSV・ログ末尾・行数を確認 |
| **実行主体にならない** | tmux セッション内の処理を直接制御しない |

#### 出力ファイルの命名規則

- ログ: `logs/{処理種別}/run_YYYYMMDD_HHmmss.log`（timestamp 必須）
- 出力 CSV: `extracted_text/{種別}_YYYYMMDD_HHmmss.csv`（timestamp 必須）
- timestamp は処理開始時に一度だけ生成し、ログ・CSV で同じ値を使う

---

### 7-2. 失敗時の停止ルール

以下のいずれかが発生した場合、**自動で次工程へ進まず** `logs/nightly/YYYYMMDD.log` に停止理由を記録して停止する。

| 停止トリガー | 記録内容 |
|------------|---------|
| OCR 失敗 | 対象ファイル名・エラーメッセージ・ocr_failure_reason 候補 |
| 動画フレーム抽出失敗 | 対象ファイル名・エラーメッセージ・対象タイムスタンプ |
| 音声文字起こし失敗 | 対象ファイル名・エラーメッセージ・音声長 |
| ファイル欠損 | 期待ファイル名・実在確認結果 |
| metadata 不一致 | files_catalog.csv の期待値・実ファイルの差分 |
| 容量不足 | 残容量・必要容量・対象ディレクトリ |
| 権限不足 | 対象パス・実行ユーザー・必要権限 |

---

## 8. 素材カード設計

### 8-1. 出力先と命名規則

```
worker_outputs/
└── {file_name_without_ext}_card.json
    例: CIA-UAP-D001_Intelligence_Information_Report_USSR_1973_card.json
```

### 8-2. 素材カード JSON スキーマ

```json
{
  "file_name": "CIA-UAP-D001_Intelligence_Information_Report_USSR_1973.pdf",
  "file_type": "PDF",
  "confirmed_metadata": {
    "agency": "Central Intelligence Agency",
    "release_date": "2026-05-22",
    "incident_date": "1973-12-20",
    "incident_location": "USSR",
    "source_url": "https://www.war.gov/UFO/"
  },
  "processing_status": "completed",
  "ocr_status": "not_needed",
  "ocr_failure_reason": [],
  "readable_elements": [
    "page 1: ヘッダー・分類表示・文書番号",
    "page 2: 本文テキスト抽出済み"
  ],
  "visual_observations": [],
  "uncertain_points": [
    "page 1: 固有名詞の読み取りに誤認の可能性あり"
  ],
  "risk_flags": [
    "SENSITIVE INTELLIGENCE SOURCES AND METHODS の記載あり"
  ],
  "human_review_needed": false,
  "generated_by": "mac_mini_agentai",
  "generated_at": "2026-05-29T02:00:00+09:00",
  "worker_version": "v1"
}
```

### 8-3. フィールド定義

| フィールド | 型 | 説明 |
|-----------|----|----|
| `file_name` | string | files_catalog.csv の file_name と一致させる |
| `file_type` | string | PDF / VID / AUD / IMG |
| `confirmed_metadata` | object | files_catalog.csv の値をそのままコピー（改変しない）|
| `processing_status` | string | pending / in_progress / completed / failed / hold |
| `ocr_status` | string | not_needed / partial / needed / failed |
| `ocr_failure_reason` | array | 空配列または ocr_failure_reason 分類値のリスト |
| `readable_elements` | array | 実際に読み取れた要素（ページ番号付き）|
| `visual_observations` | array | VID/IMG の視覚観察メモ候補（断定禁止）|
| `uncertain_points` | array | 読み取り・解釈が不確かな点 |
| `risk_flags` | array | 記事化リスク・センシティブ記述の注記 |
| `human_review_needed` | boolean | Mac Studio 側での人間確認が必要か |
| `generated_by` | string | 生成元の識別子 |
| `generated_at` | string | ISO 8601 形式 |
| `worker_version` | string | 素材カードスキーマのバージョン |

---

## 9. セキュリティ方針

### 9-1. 実行権限

| ルール | 内容 |
|--------|------|
| root 実行禁止 | すべての処理は `agentai` ユーザーで実行する |
| chmod 777 禁止 | 必要最小限の権限のみ付与する |
| sudo 禁止 | スクリプト内に sudo を書かない |
| 必要最小権限の原則 | ディレクトリごとに read / write を最小化する |

### 9-2. 外部 API・ネットワーク

| ルール | 内容 |
|--------|------|
| 外部 API 前提にしない | Mac mini の処理は原則ローカル完結 |
| 機密情報の外部送信禁止 | 米政府公開資料（war.gov）のコンテンツを外部 API に送らない |
| war.gov ダウンロードのみ許可 | スクリプトからの外部 HTTP アクセスは war.gov / DVIDS に限定する |

**Mac mini でローカル処理する主な理由:**
- 米政府公開資料は公開情報だが、未公開の中間生成物（OCR テキスト・文字起こし等）を外部 LLM API に送るリスクを回避する
- Claude API / OpenAI API のトークンコストを削減する
- ネットワーク障害・API 障害に依存しない夜間バッチを実現する

### 9-3. ファイルアクセス

| ディレクトリ | agentai 権限 | Mac Studio 権限 |
|------------|-------------|----------------|
| raw_pdf/ | read / write | read only（参照のみ）|
| raw_media/ | read / write | read only（参照のみ）|
| worker_outputs/ | read / write | read only（結果参照）|
| repo/（Git）| read only（pull のみ）| read / write |
| logs/ | read / write | read only（確認のみ）|

---

## 10. 失敗時の停止ルール（詳細）

### 10-1. ログ出力フォーマット

```
[STOP] 2026-05-29T02:13:45+09:00
FILE   : CIA-UAP-D001_Intelligence_Information_Report_USSR_1973.pdf
STAGE  : ocr_execution
REASON : OCRプロセスが非ゼロで終了した (exit code: 1)
DETAIL : tesseract: error while loading shared libraries
ACTION : 手動確認が必要。次工程へは進まない。
LOG    : logs/ocr/20260529_CIA-UAP-D001.log
```

### 10-2. 停止後の対応フロー

```
停止ログ検出（Mac Studio 側で logs/nightly/ を朝確認）
    ↓
原因特定（ログの REASON / DETAIL を確認）
    ↓
修正または手動実行
    ↓
jobs/ に再実行ジョブを投入
    ↓
再実行・確認
```

### 10-3. 自動リトライの禁止

- **失敗したジョブを自動リトライしない**（無限ループ・ストレージ枯渇リスク）
- リトライは人間が内容を確認してから手動で行う

### 10-4. 成否判定の手順（exit code だけで判断しない）

Claude Code のバックグラウンドタスクが `failed` を返しても、Mac mini 上の処理が成功している場合がある（SSH 断による exit code 255 等）。**成否判定は以下の複数指標で行う。**

#### 確認コマンド一覧

```bash
# 1. プロセス有無（まだ動いているか / 終了したか）
ps aux | grep run_ocr | grep -v grep

# 2. ログ末尾（正常完了 or エラーメッセージ）
tail -30 logs/ocr/ocr_run_YYYYMMDD_HHmmss.log

# 3. 出力ファイルの存在確認
ls -lh extracted_text/ocr_results_full_YYYYMMDD_HHmmss.csv

# 4. 出力ファイルの行数（Python でカウント・埋め込み改行対応）
python3 -c "
import csv
with open('extracted_text/ocr_results_full_YYYYMMDD_HHmmss.csv') as f:
    print(sum(1 for _ in csv.DictReader(f)), 'rows')
"

# 5. エラー件数
grep -c -i 'error\|exception\|traceback' logs/ocr/ocr_run_YYYYMMDD_HHmmss.log || echo '0'

# 6. 完了メッセージ確認
grep '完了\|完成\|finished\|done' logs/ocr/ocr_run_YYYYMMDD_HHmmss.log | tail -5
```

#### 成否判定マトリクス

| プロセス有無 | ログ末尾 | 出力CSV | 判定 |
|------------|---------|--------|------|
| 終了（なし） | 完了メッセージあり | 存在・行数一致 | **成功** |
| 終了（なし） | エラーあり | 存在しない or 0行 | **失敗** → ログで原因確認 |
| 終了（なし） | 途中で途切れ | 存在・行数一致 | **実質成功**（ログは tee 断の可能性）|
| 終了（なし） | 途中で途切れ | 存在しない | **不明** → 再実行（resume 方式で重複回避）|
| 稼働中 | 進捗あり | 未生成（処理中） | **正常処理中** → 待機 |
| 稼働中 | 更新なし（10分以上） | — | **ハング疑い** → 確認後に Ctrl-C |

**exit code 255 は SSH クライアント断を示すのみ。Mac mini 側プロセスの成否は表さない。**

---

## 11. 将来的な単体サービス化可能性

本設計は UAP_TRANSLATION_PROJECT 専用として作るが、以下の汎用化可能性を持つ。

| サービス候補 | 概要 |
|------------|------|
| OCR 不可 PDF 原因診断ツール | スキャン PDF の品質診断 → 再解析方針の自動提案 |
| 古い行政文書・スキャン文書の再解析ワーカー | 政府公開文書・公文書館資料の OCR Challenge Pipeline |
| 動画・画像・音声を含む公開資料の素材カード化 | マルチメディア対応の文書処理ワーカー |
| 一人事業者向けローカル AI 文書処理ワーカー | API 不要・電力効率重視の小規模文書処理基盤 |

**汎用化する場合の前提:**
- 機密情報は扱わない（パブリックドメイン・公開資料のみ）
- ローカル完結（外部 API 送信なし）
- 失敗停止ルールを維持する

---

## 改訂履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| v1 | 2026-05-28 | 初版制定 |
| v1.1 | 2026-05-30 | Section 7-3「長時間処理の実行方式」追加・Section 10-4「成否判定マトリクス」追加 |
