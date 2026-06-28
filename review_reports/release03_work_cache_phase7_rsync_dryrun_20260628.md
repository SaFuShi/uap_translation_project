# Release 03 Work Cache — Phase 7 rsync レポート

- 実施日: 2026-06-28
- 対象: 内蔵SSD → 外付けSSD 同期確認
- ステータス: **✅ 実 rsync 完了（2026-06-28）**

> **証跡ファイル**: 日常運用では参照不要。正式仕様は `docs/release03_work_cache_layer.md` を参照。

---

## 1. 実行コマンド

```bash
rsync -av --dry-run \
  --exclude='.git/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='.DS_Store' \
  --exclude='adaptive_frames/' \
  --exclude='targeted_frames/' \
  --exclude='frame_delta_runs/' \
  --exclude='motion_intelligence_runs/' \
  --exclude='tmp/' \
  --exclude='temp/' \
  --exclude='scratchpad/' \
  --exclude='workflow.db' \
  --exclude='raw_pdf' \
  --exclude='raw_media' \
  --exclude='page_images' \
  --exclude='thumbnails/' \
  --exclude='*.bak' \
  ~/AI_Work/active/UAP_TRANSLATION_PROJECT/ \
  /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/
```

---

## 2. dry-run 結果サマリー

| 項目 | 値 |
|------|---|
| 対象ファイル総数 | **904件** |
| ソース総サイズ | **約 39MB**（39,105,224 bytes）|
| 実転送推定量 | **約 110KB**（speedup: 346.86）|
| git pull 実施 | ✅（a51a63c → 4d9cd1f）|

> speedup 346.86 = 外付けSSD側にほぼ全ファイルが存在済み。実際に転送されるのは差分のみ（~110KB）。

---

## 3. カテゴリ別ファイル数

| カテゴリ | ファイル数 | 備考 |
|---------|---------|------|
| `docs/` | 25 | release03_work_cache_layer.md 含む ✅ |
| `scripts/` | 60 | |
| `review_reports/` | 357 | 証跡ファイル群 |
| `review_logs/` | 18 | source_registry.csv 含む |
| `note_drafts/` | 135 | .md のみ（.bak は除外済み）⚠️ 要判断 |
| `published_articles/` | 75 | |
| `logs/` | 49 | |
| `data/` | 0 | Phase 4 で同期済み（差分なし）|
| `archive_drafts/` | 5 | |
| `classification/` | 2 | |
| `extracted_text/` | 2 | |
| `metadata/` | 6 | |
| ルート直下 | 4 | README.md / .gitignore / PROJECT_SPEC.md / requirements_macmini_phase1.txt |

---

## 4. 除外確認（全て正常）

| 除外対象 | 確認結果 |
|---------|---------|
| `workflow.db` | ✅ 含まれていない |
| `raw_pdf` / `raw_media` / `page_images` | ✅ 含まれていない（symlink）|
| `*.bak` | ✅ 含まれていない |
| `frame_delta_runs/` | ✅ 含まれていない |
| `motion_intelligence_runs/` | ✅ 含まれていない |
| `adaptive_frames/` | ✅ 含まれていない |
| `.git/` | ✅ 含まれていない |

---

## 5. 新規・更新ファイル（外付けSSDに存在しないか古い）

| ファイル | 状況 |
|---------|------|
| `README.md` | 新規（Phase 7 で初めて外付けSSDへ同期）|
| `docs/release03_work_cache_layer.md` | 更新（v3: 正式運用記録追加）|

---

## 6. note_drafts/ 方針（確定）

`note_drafts/` 135件の .md ファイルは **A: 含める** で確定。
- 理由: .bak 除外済み・実転送量少量・公開作業に必要な作業資産・保存領域への同期が自然

---

## 7. 実 rsync 結果（2026-06-28 完了）

```
sent 101,760 bytes  received 54 bytes  2,208,546 bytes/sec
total size is 39,105,224  speedup is 384.08
```

| 項目 | 値 |
|------|---|
| 処理ファイル数 | 1,060件 |
| 実転送 | `logs/rsync/` ディレクトリ + ログファイル 3件のみ |
| 送信量 | 約 99KB |
| speedup | **384x**（全ファイル同期済みを確認）|
| ログ保存先 | `logs/rsync/rsync_phase7_20260628.log` |

> 1回目の rsync 実行時（tee エラー発生）に 904ファイルの差分転送が完了。
> 2回目は logs/rsync/ の新規ディレクトリとログファイルのみ追加。

---

## 8. Phase 7 完了確認

| チェック項目 | 結果 |
|------------|------|
| 除外対象（workflow.db / raw系 / .bak / frame_delta_runs）| ✅ 全て除外確認済み |
| 外付けSSD マウント状態 | ✅ |
| 内蔵SSD git pull 完了（HEAD = 4d9cd1f）| ✅ |
| note_drafts 方針確定（A: 含める）| ✅ |
| 実 rsync 完了 | ✅ |
| ログ保存 | ✅ `logs/rsync/rsync_phase7_20260628.log` |

**→ Phase 7（Sync A 初回）完了。Release 03 Work Cache Layer 全フェーズ完了。**
