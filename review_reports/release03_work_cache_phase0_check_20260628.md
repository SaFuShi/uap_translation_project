# Release 03 Work Cache Layer — Phase 0 確認レポート

- 実施日: 2026-06-28
- 設計書: `docs/release03_work_cache_layer.md`
- 移行計画: `review_reports/release03_work_cache_migration_plan_20260628.md`
- ステータス: Phase 0 完了 / **Phase 1 ブロック条件あり（下記参照）**

---

## 1. 現在地確認

```
pwd: /Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT
```

→ 現在は**外付けSSD上**で作業中（移行前の状態）

---

## 2. Git 状態

### 2.1 最新コミット（HEAD）

```
521d221 Add Media Inspector v2 observation reporting pipeline
73b00cb feat: adopt adaptive frame extraction for Release02 VID pipeline (PR043-046)
6d403f9 Add Media Inspector scoring and article evolution pipeline
```

### 2.2 Git リモート

```
origin  https://github.com/SaFuShi/uap_translation_project.git (fetch)
origin  https://github.com/SaFuShi/uap_translation_project.git (push)
```

→ GitHub リモート確認済み ✓

### 2.3 未コミット状態（⚠️ Phase 1 ブロック要因）

#### 修正済みトラックファイル（M）: 6件

| ファイル | 種別 | 備考 |
|---------|------|------|
| `metadata/files_catalog.csv` | カタログ更新 | commit 対象候補 |
| `metadata/uap-csv-cache.csv` | war.gov キャッシュ | .gitignore 対象のため commit 不要 |
| `note_drafts/ai_summary_DOW-UAP-PR059_NAG_UAP_1_Jun_20_note_version.md` | note 下書き | commit 対象候補 |
| `note_drafts/release02_intro_note_version.md` | note 下書き | commit 対象候補 |
| `review_logs/source_registry.csv` | ソースレジストリ | commit 対象候補 |
| `scripts/publish_done.py` | スクリプト更新 | commit 対象候補 |

> ⚠️ `metadata/uap-csv-cache.csv` は `.gitignore` 対象だが `git add -u` で追跡されている可能性あり。commit 時は対象から除く。

#### 未追跡ファイル（??）: 442件

大分類別の内訳：

| カテゴリ | 代表ファイル・ディレクトリ | 種別 |
|---------|------------------------|------|
| `data/adaptive_frames/` | フレーム抽出結果 | git 管理外（移行時にコピー）|
| `data/frame_delta_runs/` | フレームデルタ解析結果 | git 管理外（移行時にコピー）|
| `data/motion_intelligence_runs/` | モーション解析結果 | git 管理外（移行時にコピー）|
| `data/vlm_runs/` | VLM 評価結果 | git 管理外（移行時にコピー）|
| `docs/motion_intelligence_engine_v*.md` | 設計書 3 件 | **git 管理対象 → commit 必要** |
| `docs/release03_work_cache_layer.md` | 本移行設計書 | **git 管理対象 → commit 必要** |
| `docs/release02_article_template_v1.md` | テンプレート | **git 管理対象 → commit 必要** |
| `logs/notebooklm/` | 公開ログ多数 | **git 管理対象 → commit 必要** |
| `review_reports/motion_intelligence_v3_*.md` | v3 設計レポート | git 管理対象 → commit 必要 |
| `review_reports/release03_work_cache_*.md` | 本移行計画 | git 管理対象 → commit 必要 |

**Phase 1 ブロック理由:**
`git clone` は GitHub 上の最新 commit（521d221）のみを取得する。上記の未コミット変更・未追跡ファイルは clone 先に引き継がれない。**Phase 1 実行前に git commit / push が必要。**

---

## 3. ディスク容量

### 3.1 Mac Studio 内蔵SSD（移行先）

```
Filesystem: /dev/disk3s5 (~/が属するボリューム)
Size:     926GB
Used:     603GB
Avail:    302GB
Capacity: 67%
```

→ 302GB 空き。移行に必要な容量（data/ 604MB + workflow.db 124KB）は十分 ✓

### 3.2 外付けSSD（現在の作業場所 / 移行後の正式保存先）

```
Filesystem: /dev/disk7s1
Size:     1.8TB
Used:     69GB
Avail:    1.8TB (約 1.75TB)
Capacity: 4%
Mount:    /Volumes/ACASIS_samsung2TB
```

→ マウント済み ✓ / 空き容量に問題なし ✓

---

## 4. 移行先ディレクトリ確認

```
~/AI_Work                        : NOT EXISTS
~/AI_Work/UAP_TRANSLATION_PROJECT: NOT EXISTS
```

→ Phase 1（`mkdir -p ~/AI_Work`）は未実施。設計通り ✓

---

## 5. raw 系ディレクトリの型確認

```
drwxr-xr-x  raw_pdf     （通常ディレクトリ / 外付けSSD上 / 3.2GB）
drwxr-xr-x  raw_media/  （通常ディレクトリ / 外付けSSD上 / 11GB）
drwxr-xr-x  page_images/ （通常ディレクトリ / 外付けSSD上）
```

→ 3件とも現時点では**通常ディレクトリ（symlink ではない）**。Phase 3 でシンボリックリンクに切り替える ✓

---

## 6. workflow.db 確認

```
-rw-r--r--  workflow.db  124KB  最終更新: 6月26日 16:23
```

→ 存在確認済み ✓。Phase 5 で内蔵SSDへコピー予定。

---

## 7. Phase 0 判定サマリー

| チェック項目 | 結果 | 判定 |
|------------|------|------|
| 外付けSSDマウント | `/Volumes/ACASIS_samsung2TB` マウント済み | ✓ |
| GitHub remote 確認 | `https://github.com/SaFuShi/uap_translation_project.git` | ✓ |
| 内蔵SSD 空き容量 ≥ 20GB | 302GB 空き | ✓ |
| ~/AI_Work 未存在（予定通り）| NOT EXISTS | ✓ |
| raw_pdf / raw_media が symlink でない | 通常ディレクトリ（Phase 3 で symlink 化）| ✓ |
| workflow.db 確認 | 124KB 存在 | ✓ |
| **git status クリーン** | **M: 6件 / ??: 442件 ← 未解決** | **⚠️ BLOCK** |

---

## 8. Phase 1 への進め方（推奨手順）

Phase 0 でブロック条件が発覚したため、Phase 1 の前に以下を完了する必要がある。

### 必要な前処理

**Step A（優先）: git commit / push**

commit 対象候補（未コミット M ファイル + 未追跡の docs / review_reports / logs）:

```
M  metadata/files_catalog.csv
M  note_drafts/ai_summary_DOW-UAP-PR059_NAG_UAP_1_Jun_20_note_version.md
M  note_drafts/release02_intro_note_version.md
M  review_logs/source_registry.csv
M  scripts/publish_done.py
?? docs/motion_intelligence_engine_v1.md
?? docs/motion_intelligence_engine_v2.md
?? docs/motion_intelligence_engine_v3.md
?? docs/release02_article_template_v1.md
?? docs/release03_work_cache_layer.md
?? logs/notebooklm/ （多数）
?? review_reports/motion_intelligence_v3_design_20260627.md
?? review_reports/release03_work_cache_migration_plan_20260628.md
?? review_reports/release03_work_cache_phase0_check_20260628.md（本ファイル）
```

commit 除外対象（git clone 後に別途コピー / git 管理外）:
```
?? data/（adaptive_frames / frame_delta_runs / motion_intelligence_runs / vlm_runs）
 M metadata/uap-csv-cache.csv（.gitignore 対象のためステージング不要）
```

**Step B（オプション）: data/ の git clone 後コピー計画確認**

data/ 配下は git 管理外のため clone 後に別途 rsync でコピーする（移行計画 Phase 4）。

---

## 9. 結論

| 項目 | 状態 |
|------|------|
| Phase 0 完了 | ✓ |
| Phase 1 即時着手可否 | **❌ 不可（git commit / push が先決）** |
| Phase 1 への前提条件 | 未コミットファイルの commit & push を完了してから |
| 移行可否判断 | 環境・容量・マウント・remote URL は全て準備完了。git 状態解消のみ残る |
