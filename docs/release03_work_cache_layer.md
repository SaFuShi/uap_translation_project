# Release 03 Work Cache Layer 設計書 v3

- 制定日: 2026-06-28
- 改訂日: 2026-06-28（v3: 正式運用開始確定）
- ステータス: **正式運用中**（移行完了 2026-06-28）

> **この文書が三層アーキテクチャの正式仕様書です。**
> 日常運用の参照先はこのファイルと `README.md` の2つのみです。
> `review_reports/release03_*` は移行作業の証跡であり、運用上の参照は不要です。

**恒久仕様の集約方針:**
作業環境・rsync ルール・Git 運用・日常チェックリスト・セキュリティ方針はこのファイルに追記して管理する。
新しい運用上の決定事項が生まれた場合も、まずこのファイルへの追記で対応できるか検討すること。

- 関連（証跡）: `review_reports/release03_work_cache_migration_plan_20260628.md`

---

## 0. 設計の動機

フルディスクアクセス権限問題により、外付けSSD上のリポジトリで Claude Code / Codex / Git 操作を行う現在の構成が不安定であることが判明した。外付けSSDのマウント・アクセス権制御はmacOSの外部ボリューム管理に依存しており、権限失効・再起動・SSD再接続のたびに作業が中断するリスクがある。

本設計では、**Claude Code / Codex / Git の作業を Mac Studio 内蔵SSD上の専用ディレクトリに移し**、外付けSSDを「正式保存・バックアップ・Mac mini同期元」として役割を明確に分離する。

---

## 1. 三層アーキテクチャ

```
┌────────────────────────────────────────────────────────┐
│ Layer 1: Mac Studio 内蔵SSD 作業領域（Work Cache）       │
│   ~/AI_Work/active/UAP_TRANSLATION_PROJECT/            │
│   ← Claude Code / Codex / Git 操作は全てここで          │
│   ← git-tracked ファイル + 作業中の data/ が常駐        │
│   ← raw_pdf / raw_media はシンボリックリンクで参照       │
└──────────────────────────┬─────────────────────────────┘
                           │ rsync（作業後に上書き保存）
                           ↓
┌────────────────────────────────────────────────────────┐
│ Layer 2: 外付けSSD 正式保存領域（Formal Storage）         │
│   /Volumes/ACASIS_samsung2TB/AIprj/active/             │
│   UAP_TRANSLATION_PROJECT/                             │
│   ← 全ファイルの正式保存先・バックアップ                 │
│   ← raw_pdf（3.2GB）/ raw_media（11GB）の実体           │
│   ← Git 操作は原則行わない（.git/ を保持しない）         │
└──────────────────────────┬─────────────────────────────┘
                           │ rsync（Mac mini 同期）
                           ↓
┌────────────────────────────────────────────────────────┐
│ Layer 3: Mac mini 処理ワーカー領域                       │
│   /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/ │
│   ← OCR / Whisper / ffmpeg バッチ処理                  │
│   ← git pull のみ（直接 GitHub から）                   │
│   ← 書き込みは worker_outputs/ / logs/ のみ            │
└────────────────────────────────────────────────────────┘
```

---

## 2. 各レイヤーの詳細

### 2.1 Layer 1: Mac Studio 内蔵SSD 作業領域

**ベースパス:** `~/AI_Work/active/UAP_TRANSLATION_PROJECT/`

| ディレクトリ / ファイル | 内容 | 管理方法 |
|----------------------|------|---------|
| `.git/` | Git リポジトリ本体 | Git（GitHub remote） |
| `scripts/` | 処理スクリプト | Git 管理 |
| `docs/` | 設計書・方針書 | Git 管理 |
| `note_drafts/` | note 下書き | Git 管理 |
| `published_articles/` | 公開済み保存版 | Git 管理 |
| `metadata/*.csv` | カタログ・レジストリ | Git 管理（uap-csv-cache.csv 除く）|
| `review_logs/` | Codex 監査ログ | Git 管理 |
| `review_reports/` | 設計レポート | Git 管理（一部 .gitignore）|
| `logs/notebooklm/` | 公開ログ | Git 管理 |
| `data/` | フレーム抽出・解析結果 | Git 管理外（作業中のみ）|
| `workflow.db` | SQLite 状態管理 | Git 管理外（内蔵SSD上でマスター）|
| `raw_pdf` | **シンボリックリンク** → Layer 2 | symlink（実体は外付けSSD）|
| `raw_media/` | **シンボリックリンク** → Layer 2 | symlink（実体は外付けSSD）|
| `page_images/` | シンボリックリンク → Layer 2 | symlink（実体は外付けSSD）|

**ポイント:**
- `raw_pdf` / `raw_media` / `page_images` はシンボリックリンクにより外付けSSDの実体を参照する。スクリプト内の相対パス記述は変更不要。
- `data/` ディレクトリは作業中に生成される。作業セッション終了後に Layer 2 へ rsync する。
- Git 操作（add / commit / push / pull）はすべてここで実行する。

### 2.2 Layer 2: 外付けSSD 正式保存領域

**ベースパス:** `/Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/`

| ディレクトリ / ファイル | 内容 | 管理方法 |
|----------------------|------|---------|
| `raw_pdf/`（3.2GB）| PDF 本体（読み取り専用） | rsync のみ（Layer 1 から参照）|
| `raw_media/`（11GB）| 動画・音声・画像（読み取り専用）| rsync のみ（Layer 1 から参照）|
| `page_images/` | PDF→画像変換中間ファイル | rsync のみ |
| `data/` | フレーム抽出・解析結果 | rsync で Layer 1 から保存 |
| `workflow.db` | SQLite バックアップ | rsync で Layer 1 から保存 |
| `scripts/` `docs/` 等 | Layer 1 作業後の rsync コピー | rsync |
| `.git/` | **保持しない** | ← 原則 Git 操作禁止 |

**ポイント:**
- 外付けSSDは「正式保存先」であり「作業場所」ではない。
- `.git/` ディレクトリは移行後に削除するか、保持する場合でも一切の Git 操作を行わない。
- Mac mini はこのレイヤーから `rsync` で素材を受け取り、GitHub remote から `git pull` でスクリプト・設計書を更新する。

### 2.3 Layer 3: Mac mini 処理ワーカー

**ベースパス:** `/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/`（変更なし）

| 変更点 | 内容 |
|--------|------|
| git 操作 | GitHub remote から直接 `git pull`（Layer 2 経由は廃止）|
| 素材同期 | Layer 2 から rsync で受け取る（変更なし）|
| repo/ ディレクトリ | `repo/` 内に Git clone を保持（変更なし）|

---

## 3. rsync 同期方針

### 3.1 Sync A: Layer 1 → Layer 2（作業後保存）

**タイミング:** 作業セッション終了時、または git push の前後

```bash
# 必ず --dry-run で差分を確認してから実行する
rsync -av --dry-run \
  --exclude='.git/' \
  --exclude='raw_pdf' \
  --exclude='raw_media/' \
  --exclude='page_images/' \
  --exclude='workflow.db' \
  --exclude='.DS_Store' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='*.tmp' \
  ~/AI_Work/active/UAP_TRANSLATION_PROJECT/ \
  /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/

# 確認後に --dry-run を外して実行
```

**除外理由:**
| 除外対象 | 理由 |
|---------|------|
| `.git/` | Git はリモート（GitHub）経由で管理。外付けSSDは非 Git |
| `raw_pdf` | symlink（実体は外付けSSD上に既にある）|
| `raw_media/` | symlink（同上）|
| `page_images/` | symlink（同上）|
| `workflow.db` | バイナリ・作業状態依存。必要時は別途手動コピー |

**data/ ディレクトリの扱い:**
- `data/` は除外しない → 作業後に Layer 2 へ保存される
- Layer 2 の `data/` が Mac mini 同期元になる

### 3.2 Sync B: Layer 2 → Mac mini（ワーカー同期）

```bash
# raw_pdf / raw_media は通常ここで Mac mini へ転送
rsync -av --dry-run \
  --exclude='.git/' \
  --exclude='workflow.db' \
  --exclude='note_drafts/' \
  --exclude='published_articles/' \
  --exclude='review_requests/' \
  --exclude='.DS_Store' \
  --exclude='__pycache__/' \
  /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/ \
  agentai@safinoMac-mini.local:/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/
```

**除外理由:**
| 除外対象 | 理由 |
|---------|------|
| `workflow.db` | Mac Studio マスター。Mac mini は独立管理 |
| `note_drafts/` | 編集は Mac Studio のみ |
| `published_articles/` | 公開管理は Mac Studio のみ |
| `review_requests/` | .gitignore 対象・機密含む |

### 3.3 rsync 実行の絶対ルール

| ルール | 内容 |
|--------|------|
| `--dry-run` 必須 | 必ず先に dry-run で差分確認してから本実行 |
| `--delete` 禁止 | 誤削除リスクのため付けない |
| root / sudo 禁止 | すべての操作は `fukudasatoshi` / `agentai` ユーザーで実行 |
| 実行ログ保存 | 本実行時は `2>&1 | tee logs/rsync/rsync_YYYYMMDD.log` でログ保存 |

---

## 4. Git 運用方針

| 操作 | 実行場所 | 禁止場所 |
|------|---------|---------|
| `git add` | `~/AI_Work/active/UAP_TRANSLATION_PROJECT/` のみ | 外付けSSD / Mac mini |
| `git commit` | `~/AI_Work/` のみ | 外付けSSD / Mac mini |
| `git push` | `~/AI_Work/` のみ | 外付けSSD / Mac mini |
| `git pull` | `~/AI_Work/`（Mac Studio）または Mac mini repo/ | — |
| `git status` / `git log` | すべての場所で OK | — |

**Mac mini の git 操作:**
```bash
# Mac mini 側: GitHub remote から直接 pull（Layer 2 を経由しない）
cd /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/repo
git pull
```

**外付けSSD の Git 廃止方針:**
- 移行後、外付けSSD の `.git/` ディレクトリは削除するか、残す場合でも操作禁止とする
- Claude Code の作業ディレクトリが `~/AI_Work/` になれば、外付けSSD への git 誤操作は自然に防がれる

---

## 5. 大容量ファイルの取り扱い

| ファイル種別 | 実体の場所 | Layer 1 での参照方法 |
|------------|---------|-------------------|
| raw_pdf/（3.2GB）| Layer 2（外付けSSD）| symlink |
| raw_media/（11GB）| Layer 2（外付けSSD）| symlink |
| page_images/ | Layer 2（外付けSSD）| symlink |
| data/（フレーム等）| Layer 1（内蔵SSD、作業中）| 実ファイル → 作業後に Sync A |
| thumbnails/ | Layer 2（外付けSSD）| symlink（必要に応じて）|

**シンボリックリンク作成コマンド（移行時に実行）:**
```bash
# 移行作業時に一度だけ実行（まだ実行しない）
ln -s /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/raw_pdf \
       ~/AI_Work/active/UAP_TRANSLATION_PROJECT/raw_pdf
ln -s /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/raw_media \
       ~/AI_Work/active/UAP_TRANSLATION_PROJECT/raw_media
ln -s /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/page_images \
       ~/AI_Work/active/UAP_TRANSLATION_PROJECT/page_images
```

---

## 6. Claude Code 設定の変更点

| 変更項目 | 現在 | 移行後 |
|---------|------|--------|
| Primary working directory | `/Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT` | `~/AI_Work/active/UAP_TRANSLATION_PROJECT` |
| dangerouslyDisableSandbox | 禁止（変更なし）| 禁止（変更なし）|
| Git リモート | GitHub（変更なし）| GitHub（変更なし）|

Claude Code の設定ファイル（`.claude/settings.json` 等）はプロジェクトに紐づくため、新しい作業ディレクトリで Claude Code を開き直すことで自動的に更新される。

---

## 7. 移行後の日常運用フロー

```
【作業開始】
  1. Mac Studio で ~/AI_Work/active/UAP_TRANSLATION_PROJECT/ を開く
  2. Claude Code を ~/AI_Work/ で起動
  3. 外付けSSDがマウントされていることを確認（symlink が機能するため）
  4. git pull で最新状態を取得

【作業中】
  - Claude Code / Codex / Git はすべて ~/AI_Work/ で実行
  - raw_pdf / raw_media へのアクセスは symlink 経由で透明に動作
  - data/ 配下の生成物は内蔵SSD上に蓄積

【作業終了】
  1. git add / commit / push（~/AI_Work/ で実行）
  2. Sync A を実行（~/AI_Work/ → 外付けSSD）
     ※ workflow.db も必要に応じて手動コピー

【Mac mini 同期が必要な場合】
  1. Sync B を実行（外付けSSD → Mac mini）
  2. Mac mini 側で git pull（GitHub から）
```

---

## 8. セキュリティ・安全方針

| ルール | 内容 |
|--------|------|
| root 実行禁止 | すべての操作は `fukudasatoshi` で実行 |
| chmod 777 禁止 | 必要最小権限のみ |
| dangerouslyDisableSandbox 禁止 | 外部ボリューム権限を失う（[feedback参照]）|
| 外付けSSD への git 操作禁止 | 移行後は Layer 2 で git コマンドを実行しない |
| `--delete` 禁止 | rsync の誤削除リスク回避 |

---

## 9. 既存設計書との整合性

本設計により更新が必要な既存ドキュメント一覧（詳細は migration plan 参照）:

| ドキュメント | 更新内容 |
|------------|---------|
| `docs/macmini_uap_local_worker_design.md` | Mac Studio の作業パス・Mac mini pullコマンド |
| `docs/macmini_uap_migration_checklist.md` | 三層構成への改訂 |
| `docs/claude_codex_semiauto_workflow_design.md` | workflow.db パス・Mac mini pullコマンド |
| `docs/ios_remote_monitoring_design.md` | Mac Studio 監視パス |

---

## 10. 正式運用確認済み項目（2026-06-28）

| 確認項目 | 結果 |
|---------|------|
| git clone → 内蔵SSD | ✅ 完了（HEAD: a51a63c）|
| symlink（raw_pdf / raw_media / page_images）| ✅ 動作確認済み |
| .gitignore 修正（symlink除外）| ✅ 完了 |
| data/ rsync（adaptive_frames 除く）| ✅ 30MB / 185件 |
| workflow.db コピー | ✅ 124KB |
| source_registry.csv 同期（R02-010〜043）| ✅ commit/push 済み |
| Python スクリプト動作確認 | ✅ py_compile PASS |
| raw_media/video/ アクセス（symlink経由）| ✅ MP4一覧取得成功 |
| **Claude Code 再起動** | ⏳ Phase 7（次回セッションで実施）|

---

## 11. 日常運用チェックリスト

作業開始時:
- [ ] 外付けSSD マウント確認（`ls /Volumes/ACASIS_samsung2TB/`）
- [ ] `~/AI_Work/active/UAP_TRANSLATION_PROJECT/` で Claude Code を開く
- [ ] `git pull` で最新状態を取得

作業終了時:
- [ ] `git add / commit / push` 実行
- [ ] Sync A: `rsync` で内蔵SSD → 外付けSSD（workflow.db は別途 cp）

---

## 12. 次のステップ

1. **Phase 7**: Claude Code を `~/AI_Work/active/UAP_TRANSLATION_PROJECT/` で開き直す（次回セッション）
2. **既存ドキュメント更新**: macmini_uap_local_worker_design.md 等のパス記載を更新
3. **note_drafts 別途 commit**: untracked 70件超を別コミットで整理

---

## 改訂履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| v1 | 2026-06-28 | 初版制定（フルディスクアクセス権限問題対応）|
| v2 | 2026-06-28 | ~/AI_Work/active/ サブディレクトリ構成に変更 |
| v3 | 2026-06-28 | 正式運用開始確定・移行完了記録追加 |
