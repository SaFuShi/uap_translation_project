# Release 03 Work Cache 移行計画

- 作成日: 2026-06-28
- 設計書: `docs/release03_work_cache_layer.md`
- ステータス: 計画策定済み・実移行未実施
- 制約: ファイル移動・rsync・git 操作・note_drafts 変更・source_registry.csv 変更は一切行わない

---

## 1. 現状分析

### 1.1 現在の構成（移行前）

```
Claude Code 作業場所: /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/
Git リポジトリ:        同上（外付けSSD上に .git/ あり）
raw_pdf:               同上/raw_pdf/（3.2GB）
raw_media:             同上/raw_media/（11GB）
data/:                 同上/data/（604MB）
内蔵SSD:               ~/（作業利用なし）
Mac mini repo:         /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/repo/
```

### 1.2 問題点

| 問題 | 影響 |
|------|------|
| フルディスクアクセス権限が外付けSSDで失効する | Claude Code / Codex / スクリプトが突然アクセス不能になる |
| 外付けSSD再接続のたびに作業が中断する | 非再現性の高い権限問題が繰り返す |
| git 操作も外付けSSD依存 | commit / push ができなくなる |

### 1.3 移行後の構成（目標）

```
Claude Code 作業場所: ~/AI_Work/UAP_TRANSLATION_PROJECT/（内蔵SSD）
Git リポジトリ:        同上（内蔵SSDに .git/ を移動）
raw_pdf:               シンボリックリンク → 外付けSSD（実体は移動しない）
raw_media:             シンボリックリンク → 外付けSSD（実体は移動しない）
外付けSSD:             正式保存・バックアップ・Mac mini 同期元
Mac mini git:          GitHub remote から直接 git pull
```

---

## 2. 外付けSSDパスを参照している既存ドキュメント

### 2.1 更新が必要なドキュメント一覧

| ファイル | 現在の外付けSSD参照箇所 | 必要な更新内容 |
|---------|---------------------|------------|
| `docs/macmini_uap_local_worker_design.md` | Section 1-1: Mac Studio 役割、Section 4: 移行方針、Section 9-3: ファイルアクセス権限表 | Mac Studio 作業パスを `~/AI_Work/` に変更。Mac mini pull を GitHub remote から行うよう変更 |
| `docs/macmini_uap_migration_checklist.md` | Section 1: 前提（外付けSSD上が移行元）、Section 6: rsync コマンド | 三層構成（内蔵SSD→外付けSSD→Mac mini）に改訂 |
| `docs/claude_codex_semiauto_workflow_design.md` | Section 6-1: workflow.db 保存場所、Section 12-3/12-4: SQLite パス、Mac mini pull コマンド（Section 12-6）| workflow.db パス更新、Mac mini pull コマンド更新 |
| `docs/ios_remote_monitoring_design.md` | Section 2: 環境構成（Mac Studio パス）、Section 1 監視対象（ACASIS_2TB）| Mac Studio 監視対象を ~/AI_Work/ に変更 |
| `docs/release02_audio_video_pipeline_design.md` | Mac mini / Mac Studio 間パス参照 | パス記載があれば更新（低優先度）|

### 2.2 更新不要なドキュメント

| ファイル | 理由 |
|---------|------|
| `docs/release03_work_cache_layer.md` | 本設計書。移行後状態が記載済み |
| `docs/motion_intelligence_engine_v*.md` | 相対パスのみ使用。影響なし |
| `docs/macmini_uap_local_worker_design.md` の Mac mini 側パス | Mac mini 側は `/Volumes/ACASIS_2TB/...` のまま変更なし |

---

## 3. 推奨ディレクトリ構成（移行後）

```
~/AI_Work/UAP_TRANSLATION_PROJECT/
├── .git/                        ← Git リポジトリ（内蔵SSDへ移動）
├── .gitignore
├── CLAUDE.md
├── PROJECT_SPEC.md
│
├── scripts/                     ← Git 管理
├── docs/                        ← Git 管理
├── note_drafts/                 ← Git 管理
├── published_articles/          ← Git 管理
├── metadata/                    ← Git 管理（uap-csv-cache.csv 除く）
├── review_logs/                 ← Git 管理
├── review_reports/              ← Git 管理（一部 .gitignore）
├── logs/notebooklm/             ← Git 管理
│
├── data/                        ← Git 管理外（作業中生成物）
│   ├── adaptive_frames/
│   ├── frame_delta_runs/
│   ├── motion_intelligence_runs/
│   └── vlm_runs/
│
├── workflow.db                  ← Git 管理外（内蔵SSD上でマスター）
│
├── raw_pdf  → [symlink]        ← /Volumes/ACASIS_samsung2TB/.../raw_pdf
├── raw_media/ → [symlink]      ← /Volumes/ACASIS_samsung2TB/.../raw_media
└── page_images/ → [symlink]    ← /Volumes/ACASIS_samsung2TB/.../page_images
```

---

## 4. 初回移行手順（実行順序）

> **重要:** 以下は計画のみ。実行前に設計承認を取得すること。

### Phase 0: 事前確認（実行可能）

```bash
# 内蔵SSD 空き容量確認（302GB 以上あることを確認）
df -h /

# 外付けSSD マウント確認
ls /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/

# git status 確認（未コミット変更がないことを確認）
git -C /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT status --short

# 内蔵SSD 上の ~/AI_Work/ 存在確認
ls ~/AI_Work/ 2>/dev/null || echo "NOT EXISTS"
```

### Phase 1: ~/AI_Work ディレクトリ作成（実行する）

```bash
# 移行先ベースディレクトリを作成
mkdir -p ~/AI_Work
```

### Phase 2: git clone を内蔵SSDに作成（実行する）

```bash
# 現在のリモート URL を確認
git -C /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT remote -v

# GitHub remote から内蔵SSDへ clone
# （remote URL は上記コマンドで確認した値を使用）
git clone <remote-url> ~/AI_Work/UAP_TRANSLATION_PROJECT
```

### Phase 3: 大容量ファイルへのシンボリックリンク作成（実行する）

```bash
# raw_pdf（外付けSSD → 内蔵SSD作業領域）
ln -s /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/raw_pdf \
      ~/AI_Work/UAP_TRANSLATION_PROJECT/raw_pdf

# raw_media
ln -s /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/raw_media \
      ~/AI_Work/UAP_TRANSLATION_PROJECT/raw_media

# page_images
ln -s /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/page_images \
      ~/AI_Work/UAP_TRANSLATION_PROJECT/page_images

# シンボリックリンク確認
ls -la ~/AI_Work/UAP_TRANSLATION_PROJECT/ | grep "^l"
```

### Phase 4: data/ ディレクトリの移行（実行する）

```bash
# data/ は git 管理外のため rsync でコピー（dry-run 先行）
rsync -av --dry-run \
  /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/data/ \
  ~/AI_Work/UAP_TRANSLATION_PROJECT/data/

# 確認後に実行
rsync -av \
  /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/data/ \
  ~/AI_Work/UAP_TRANSLATION_PROJECT/data/
```

### Phase 5: workflow.db の移行（実行する）

```bash
# workflow.db は git 管理外のため手動コピー
cp /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/workflow.db \
   ~/AI_Work/UAP_TRANSLATION_PROJECT/workflow.db

# 確認
ls -lh ~/AI_Work/UAP_TRANSLATION_PROJECT/workflow.db
```

### Phase 6: 動作確認（実行する）

```bash
# 新しい作業領域でのスクリプト動作確認
cd ~/AI_Work/UAP_TRANSLATION_PROJECT

# git 状態確認
git status

# シンボリックリンク先確認
ls raw_pdf/ | head -5
ls raw_media/video/ | head -3

# Python スクリプト動作確認（dry-run のみ）
python3 scripts/publish_done.py --help 2>/dev/null || echo "スクリプト確認"
```

### Phase 7: Claude Code 再起動（手動操作）

- Claude Code を `~/AI_Work/UAP_TRANSLATION_PROJECT/` で開き直す
- 新セッションで `git status` が正常動作することを確認

---

## 5. rsync 除外ルール（詳細）

### 5.1 Sync A: 内蔵SSD → 外付けSSD

```
# .rsync-filter または --exclude オプション
- .git/
- raw_pdf          # symlink（外付けSSDに実体あり）
- raw_media/       # symlink（外付けSSDに実体あり）
- page_images/     # symlink（外付けSSDに実体あり）
- .DS_Store
- __pycache__/
- *.pyc
- *.tmp
- *~
- review_tmp/
```

### 5.2 Sync B: 外付けSSD → Mac mini

```
- .git/
- workflow.db
- workflow.db.*.bak
- note_drafts/
- published_articles/
- review_requests/
- archive_drafts/
- note_import_tests/
- .DS_Store
- __pycache__/
- *.pyc
- *.tmp
- *~
```

---

## 6. 移行後の検証チェックリスト

### Phase 0 完了条件

- [ ] 内蔵SSD 空き容量 > 20GB（現在 302GB）
- [ ] 外付けSSDがマウントされている
- [ ] `git status` がクリーン（未コミット変更なし）

### Phase 1-3 完了条件

- [ ] `~/AI_Work/UAP_TRANSLATION_PROJECT/` が存在する
- [ ] `git log --oneline -5` で最新 commit が外付けSSD のものと一致する
- [ ] `ls -la ~/AI_Work/UAP_TRANSLATION_PROJECT/` で `raw_pdf`, `raw_media`, `page_images` が symlink として表示される
- [ ] `ls ~/AI_Work/UAP_TRANSLATION_PROJECT/raw_pdf/ | wc -l` が外付けSSD の件数と一致する

### Phase 4-5 完了条件

- [ ] `~/AI_Work/UAP_TRANSLATION_PROJECT/data/` が存在し、ファイル数が一致する
- [ ] `~/AI_Work/UAP_TRANSLATION_PROJECT/workflow.db` が存在する

### Phase 6 完了条件

- [ ] `git status` が `~/AI_Work/` から正常動作する
- [ ] Python スクリプトが `~/AI_Work/` から起動できる
- [ ] symlink 経由で `raw_pdf/` 内のファイルにアクセスできる

---

## 7. ロールバック手順

移行後に問題が発生した場合：

```bash
# 外付けSSD の元の作業領域はそのまま残っているため、
# Claude Code を外付けSSDのパスで開き直すだけで元の状態に戻る

# 確認コマンド（外付けSSD 側）
git -C /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT status
```

**外付けSSD側のファイルは移行フェーズ中は削除しない。**
内蔵SSD側が正常動作することを確認してから、外付けSSD側の.git/削除を検討する。

---

## 8. リスクと対策

| リスク | 影響 | 対策 |
|--------|------|------|
| git clone 失敗（ネットワーク）| Phase 2 でブロック | remote URL 確認後に実行。失敗したら --local clone（外付けSSD から clone）|
| symlink 先が見つからない（外付けSSD未マウント）| raw_pdf 等にアクセス不可 | 外付けSSDマウント確認を作業開始手順に組み込む |
| data/ rsync でディスク容量不足 | 604MB 必要 → 内蔵SSD 302GB 空きで問題なし | 移行前に df -h で確認済み |
| workflow.db の不整合 | SQLite の状態が古い | 移行直後はテスト用記事で動作確認してから本番利用 |
| 既存 Claude Code セッションが外付けSSD を参照し続ける | 新旧パスが混在 | 移行後は必ず Claude Code を再起動し ~/AI_Work/ で開き直す |

---

## 9. 次に実コピーへ進めるか（判断基準）

以下の条件が全て揃えば移行実行を推奨する：

| 条件 | 現在の状態 |
|------|-----------|
| 設計承認 | **未承認（本ドキュメントのレビュー待ち）**|
| 外付けSSD マウント済み | 確認済み |
| 未コミット変更なし | 要確認（git status）|
| 内蔵SSD 空き容量 ≥ 20GB | 確認済み（302GB 空き）|
| Remote URL 確認済み | 未確認（Phase 2 前に確認）|
| workflow.db バックアップ | 外付けSSD 上に元ファイルが残るため移行後でもロールバック可能 |

**現時点では設計承認待ち。承認後に Phase 0 から順に実施する。**
