# UAP Translation Project

UAP（未確認航空現象）関連の機密解除文書・映像を日本語訳し、note で公開するプロジェクト。

---

## まず見るファイル（日常運用）

| ファイル | 用途 |
|---------|------|
| **このファイル（README.md）** | 作業環境・ルール・ナビゲーションの起点 |
| **`docs/release03_work_cache_layer.md`** | 三層アーキテクチャの正式仕様・日常運用チェックリスト |

> `review_reports/` は作業ログ・移行証跡であり、**日常運用では参照不要**。
> `review_reports/commit_plan_*.md` は commit 作業用一時メモであり、commit 後は参照不要。

---

## 作業環境（Release 03 Work Cache Layer）

| レイヤー | 場所 | 役割 |
|---------|------|------|
| **Layer 1（作業）** | `~/AI_Work/active/UAP_TRANSLATION_PROJECT/` | Claude Code / Git / スクリプト実行 |
| **Layer 2（正式保存）** | `/Volumes/ACASIS_samsung2TB/AIprj/active/UAP_TRANSLATION_PROJECT/` | 外付けSSD・バックアップ・Mac mini 同期元 |
| **Layer 3（ワーカー）** | Mac mini `/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/` | OCR / ffmpeg / GitHub pull |

> **Claude Code は必ず `~/AI_Work/active/UAP_TRANSLATION_PROJECT/` で開くこと。**
> 外付けSSD（Layer 2）での git 操作は禁止。

詳細: `docs/release03_work_cache_layer.md`

---

## ディレクトリ構成

```
~/AI_Work/active/UAP_TRANSLATION_PROJECT/
├── scripts/          # 処理スクリプト（Git管理）
├── docs/             # 設計書・方針書（Git管理）
├── note_drafts/      # note下書き（Git管理）
├── published_articles/ # 公開済み保存版（Git管理）
├── metadata/         # カタログ・CSV（Git管理）
├── review_logs/      # 監査ログ・source_registry（Git管理）
├── review_reports/   # 設計レポート（Git管理）
├── logs/             # 各種ログ（Git管理）
├── data/             # 解析結果（Git管理外・rsync）
├── workflow.db       # SQLite状態管理（Git管理外）
├── raw_pdf  -> [symlink] /Volumes/ACASIS_samsung2TB/.../raw_pdf
├── raw_media/ -> [symlink] /Volumes/ACASIS_samsung2TB/.../raw_media
└── page_images/ -> [symlink] /Volumes/ACASIS_samsung2TB/.../page_images
```

---

## Git 運用ルール

- `git add / commit / push` は `~/AI_Work/active/` でのみ実行
- `git add .` / `git add -A` 禁止（対象を明示して add）
- `--delete` 付き rsync 禁止
- `dangerouslyDisableSandbox` 使用禁止
- `chmod 777` / root 実行禁止

---

## 公開先

note: https://note.com/deft_ibis3303

---

## 主要ドキュメント

| ドキュメント | 内容 |
|------------|------|
| `docs/release03_work_cache_layer.md` | 三層アーキテクチャ設計（**正式仕様**） |
| `docs/claude_codex_semiauto_workflow_design.md` | Claude/Codex 半自動ワークフロー |
| `docs/macmini_uap_local_worker_design.md` | Mac mini ワーカー設計 |
| `review_logs/source_registry.csv` | 公開済み記事レジストリ |

---

## ドキュメント運用ルール

### 原則

1. **恒久 md を安易に増やさない。**
   新しい設計・方針が生まれた場合は、まず既存の `docs/` ファイルへの追記で対応できるか検討する。

2. **日常運用の入口は `README.md` のみ。**
   何かを探すときはまずここから始める。

3. **詳細仕様は `docs/release03_work_cache_layer.md` に集約する。**
   作業環境・三層構成・rsync ルール・Git 運用・日常チェックリストはここに書く。

4. **`review_reports/` は作業ログ・証跡・一時判断の置き場とする。**
   日常運用での参照は不要。Claude Code セッション内の判断記録・移行証跡はここに置く。

5. **`review_reports/commit_plan_*.md` は commit 完了後に参照不要。**
   commit のたびに作成・使い捨てする一時メモ。恒久ドキュメントではない。

### 新規 md を作る場合のルール

- `docs/` への新規ファイル追加は、既存 docs への追記で対応できない場合のみ許可する。
- 新規 docs を作成したら、**必ず README.md の「主要ドキュメント」テーブルに追記する**。
- `review_reports/` への追加は自由（作業ログ・一時判断・証跡）。ただし日常参照ファイルとは扱わない。
- セッションをまたいで参照される恒久情報を `review_reports/` に書かない。
