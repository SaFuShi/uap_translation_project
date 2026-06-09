# Claude Code / Codex 連携 半自動化設計 v1.7

**作成日：** 2026-06-02  
**更新日：** 2026-06-09（v1.7：note公開後の保存版・ログ作成・commit準備表示を半自動化）
**対象プロジェクト：** UAP_TRANSLATION_PROJECT  
**ステータス：** フェーズ3移行中（Codex CLI 非対話実行 調査完了 / 2026-06-09）

---

## 0. 設計の前提と制約

- agmsg は未インストール。設計のみ。
- `curl | bash` は禁止。
- 外部スクリプト実行・設定変更・git 操作は本設計書の範囲外。
- Codex（ChatGPT）は制作者（Claude Code）と独立した外部モデルとして維持する。
  → 監査独立性の確保が本設計の核心的前提。
- 自動化はドラフト生成〜監査サイクルのみ。公開・git 操作は常に人間が判断する。

---

## 1. agmsg で Claude → Codex → Claude は成立するか

### 1-1. 技術的成立性

**成立する。ただし「リアルタイム双方向通信」ではなく「ファイル媒介の非同期ループ」として設計する。**

```
Claude Code（Bash tool）
  ↓ agmsg send コマンドを実行
agmsg
  ↓ OpenAI API（Codex / ChatGPT）へリクエスト送信
  ↓ レスポンスを受信（同期待機）
  ↓ 出力ファイルを review_reports/ に保存
Claude Code
  ↓ 出力ファイルを Read ツールで読み込む
  ↓ BLOCK / WARN / PASS を解析
  ↓ 停止条件に従って処理
```

- Claude Code は agmsg を Bash ツール経由で呼び出す（例：`agmsg send --to codex ...`）
- agmsg はレスポンスを stdout または指定ファイルに出力する
- Claude Code はそのファイルを Read ツールで読む
- 「Claude → Codex → Claude」は 1 往復で完結させる（再帰呼び出し禁止）

### 1-2. 成立しない条件

| 条件 | 理由 |
|------|------|
| agmsg が OpenAI API のみ対応で Claude 送信に非対応 | 送信元（Claude Code）は API 呼び出し側ではないので問題なし。Codex 送信のみが必要 |
| agmsg のレスポンスが構造化されていない | パースルールをプロンプトに明示することで対処（後述 §9）|
| Codex が監査プロンプトを無視して要約のみ返す | プロンプトの指定を厳密化（§8 参照）|
| ネットワーク不通・APIレート制限 | エラー時は即座に停止し、人間へ通知 |

### 1-3. agmsg の想定インターフェース

```bash
# 想定コマンド形式（設計段階・未実装）
agmsg send \
  --to codex \
  --input review_requests/codex_request_20260602_western_us.md \
  --output review_reports/codex_audit_20260602_western_us_auto.md \
  --timeout 120

# 戻り値
# 0: 正常完了（レスポンスファイル生成済み）
# 1: タイムアウト
# 2: API エラー
# 3: パース失敗
```

---

## 2. どこで停止させるべきか

### 2-1. 停止条件マトリクス

| 条件 | 停止レベル | 再開条件 |
|------|----------|---------|
| Codex 判定 = BLOCK | **完全停止** | 人間が BLOCK 内容を確認し、修正指示を与える |
| Codex 判定 = WARN | **人間確認待ち** | WARN 一覧を人間に提示。各 WARN を承認 / 却下後に再開 |
| Codex 判定 = PASS | 自動継続可 | 次のステップへ（ただし公開は人間が判断） |
| git add / commit / push | **完全停止** | 人間が明示的に指示した場合のみ |
| ファイル削除 | **完全停止** | 人間が明示的に指示した場合のみ |
| source_registry.csv 変更 | **完全停止** | 人間が明示的に指示した場合のみ |
| raw 素材・page_images 変更 | **完全停止** | 人間が明示的に指示した場合のみ |
| 公開作業（note 投稿） | **完全停止** | 人間が手動で実行 |
| agmsg タイムアウト / エラー | **完全停止** | 人間が手動で Codex 監査を実施 → ファイル保存後に再開 |
| SQLite 書き込み失敗 | **警告・継続** | ログのみ失敗。フロー自体は継続 |
| agmsg レスポンスのパース失敗 | **完全停止** | 人間がファイルを確認し、WARN 内容を手動で伝える |

### 2-2. 停止後の通知方法

- Claude Code がテキスト出力で停止理由と次の人間アクションを明示する
- SQLite の `workflow_events` テーブルに停止理由を記録する
- 再開時のコンテキスト維持のために停止時点のステートを保存する

---

## 3. AI ループ防止方法

### 3-1. 基本原則

**Codex が Claude Code に対して「再監査要求」を行う構造を禁止する。**

ループの発生経路は以下の 3 パターン：

| パターン | 対策 |
|---------|------|
| Claude Code → Codex → Claude Code → Codex ... の無限再帰 | 1 記事あたりの Codex 呼び出し回数を SQLite で制限（最大 2 回） |
| WARN 修正 → 再監査 → 新 WARN → 再修正 ... | 2 回目以降の監査は人間が明示的に承認した場合のみ実行 |
| Codex 出力が「再監査を推奨する」旨を含む | Claude Code がその指示を無視する（Codex は監査のみ。制御権は Claude Code が持つ）|

### 3-2. 実装レベルの防止策

```
MAX_CODEX_ITERATIONS = 2  # SQLite で管理
```

- 1 回目：自動実行可
- 2 回目：人間が承認した場合のみ実行
- 3 回目以降：禁止（SQLite でハードストップ）

### 3-3. Codex プロンプトに含める制約文

```
【重要】このプロンプトへの応答は、チェックリストに基づく監査レポートのみとしてください。
Claude Code への指示・再監査要求・修正案の自動適用は行わないでください。
判定は PASS / WARN / BLOCK のいずれかのみ使用してください。
```

---

## 3-A. Current Owner 制御

### 目的

Claude Code と Codex が所有権なしで勝手に処理を継続しないようにする。

### SQLite テーブル：workflow_owner

```sql
-- 記事ごとの現在オーナー管理
CREATE TABLE workflow_owner (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    article_slug  TEXT NOT NULL,
    current_owner TEXT NOT NULL,              -- CLAUDE / CODEX / HUMAN
    updated_at    TEXT DEFAULT (datetime('now','localtime'))
);
```

所有権の状態例：

| article_slug | current_owner |
|-------------|--------------|
| western_us_event_slides_20260508 | CLAUDE |
| odni_uap_d001_20260531 | CODEX |
| doe_uap_d001_pantex | HUMAN |

### 所有権ルール

- `current_owner != SELF` の場合は agmsg 送信禁止
- 所有権を持つエージェントのみ次工程へ進める
- `HUMAN` の場合は停止して人間確認待ち

### agmsg ワークフローへの組み込み

```
[STEP 2 前] 依頼パッケージ生成前
  → workflow_owner テーブルを参照
  → current_owner == CLAUDE であることを確認
  → CLAUDE 以外 → 停止（「オーナー不一致。現在のオーナー: <値>」を報告）

[STEP 3] agmsg 送信直前
  → workflow_owner を CLAUDE → CODEX に更新

[STEP 4] レスポンス受信後
  → workflow_owner を CODEX → CLAUDE に更新

[STEP 5] WARN / BLOCK の場合
  → workflow_owner を CLAUDE → HUMAN に更新
  → 人間が再開指示を出したら HUMAN → CLAUDE に更新
```

---

## 3-B. S_CLASS 資料ガードレール

### 目的

将来的な Production Memory・顧客情報・機密資料を外部エージェント（Codex）へ誤送信しないための物理的ガードレール。

### 分類定義

| 分類 | 説明 | agmsg 送信 |
|------|------|----------|
| PUBLIC | 一般公開済み資料 | 可 |
| INTERNAL | プロジェクト内部資料 | 可（監査目的のみ） |
| CONFIDENTIAL | 公開前・要注意資料 | 人間確認後のみ可 |
| S_CLASS | 顧客情報・機密・Production Memory | **禁止（ハードストップ）** |

### articles テーブルへの追加カラム（§6-2 参照）

```sql
classification TEXT DEFAULT 'PUBLIC'
-- classification: PUBLIC / INTERNAL / CONFIDENTIAL / S_CLASS
```

### ガードレールロジック（設計段階）

```python
def check_s_class_guard(article_slug):
    classification = db.query(
        "SELECT classification FROM articles WHERE slug = ?",
        (article_slug,)
    )
    if classification == 'S_CLASS':
        raise HardStop("S_CLASS 資料: agmsg 送信禁止・ワークフロー停止")
    if classification == 'CONFIDENTIAL':
        return require_human_approval("CONFIDENTIAL 資料: 人間の承認が必要")
    return True
```

### 停止条件マトリクスへの追加（§2-1 補足）

| 条件 | 停止レベル | 再開条件 |
|------|----------|---------|
| classification == S_CLASS | **完全停止（ハードストップ）** | agmsg/Codex 送信不可。人間が手動で処理 |
| classification == CONFIDENTIAL | **人間確認待ち** | 人間が明示的に送信を承認した場合のみ |

### 現プロジェクトでの適用

UAP Translation Project の現資料はすべて `PUBLIC`（公開済み政府文書）。  
S_CLASS は将来の拡張（顧客案件・未公開資料等）に向けた予防的ガードレールとして設計する。

---

## 4. バージョン変更検知方法

### 4-1. 監視対象

| 対象 | 検知方法 | 保存場所 |
|------|---------|---------|
| agmsg のバージョン | `agmsg --version` の出力を SQLite に記録 | model_versions テーブル |
| Codex モデル名 | agmsg レスポンスのメタデータから抽出（`model:` フィールド等） | model_versions テーブル |
| audit_checklist のバージョン | `audit_checklist_v1.md` の先頭行のバージョン文字列 | workflow_events テーブル |
| Claude Code モデル | 各セッション開始時に環境変数またはモデルID文字列を記録 | model_versions テーブル |

### 4-2. 検知ロジック

```
セッション開始時：
  1. agmsg --version を実行 → DB の前回値と比較
  2. audit_checklist_v1.md の更新日時を比較
  3. Codex 監査レスポンスのモデルIDを比較

変更が検出された場合：
  → 人間に通知（「モデル変更を検出しました：gpt-4o → gpt-4o-mini」等）
  → 変更内容を DB に記録
  → 今回の監査結果への影響有無を注記
  → 継続するかどうかは人間が判断
```

### 4-3. バージョン固定方針

- agmsg：インストール時にバージョンを requirements.txt または Brewfile に固定
- Codex モデル：agmsg の設定ファイルにモデルIDを明示指定（`gpt-4o` 等）
- モデル ID が変わった場合：自動停止 → 人間確認

---

## 5. NotebookLM ログ維持方法

### 5-1. 現在の方式（手動）

```
公開後 → 人間が logs/notebooklm/YYYY-MM-DD_<slug>_published_log.md を手動作成
```

### 5-2. 半自動化後の方式

```
公開確認（人間がnote URLを伝える）
  ↓
Claude Code が SQLite から以下を取得：
  - ドラフトファイル名
  - Codex 監査サマリー（WARN 件数・修正内容）
  - モデルバージョン
  - 処理ステップのタイムスタンプ
  ↓
ログテンプレートを自動生成（logs/notebooklm/ に出力）
  ↓
人間が内容を目視確認 → 問題なければ commit 対象に追加
```

### 5-3. ログ自動生成の範囲

| 自動化 | 手動継続 |
|--------|---------|
| Codex 監査サマリー（WARN コード・件数） | note 上の手修正内容の記述 |
| ファイル名・URL・公開日 | 読者向けのコメント・所感 |
| モデルバージョン記録 | 次のアクション（文脈依存） |
| タイムスタンプ・所要時間 | 特記事項（OCR 品質等の判断） |

### 5-4. NotebookLM への影響範囲

ログファイルは「NotebookLM アップロード用」として維持するため、以下の情報は自動生成ログに含めない：

- SSH 鍵・パスワード・IP アドレス
- API キー・トークン
- agmsg の設定内容（モデル ID 以外）

---

## 6. SQLite DB 構造

### 6-1. 保存場所候補

| 候補 | パス | 特徴 |
|------|------|------|
| **推奨：Mac Studio（メイン）** | `UAP_TRANSLATION_PROJECT/workflow.db` | git 管理外（.gitignore 追加推奨）。Mac Studio で一元管理 |
| Mac mini（ワーカー側） | `/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/workflow.db` | OCR ジョブ管理との統合に有利 |
| 共有（rsync/scp で同期） | 両機に workflow.db を配置、定期 rsync | 複雑度が高い。当面は Mac Studio のみで十分 |

### 6-2. テーブル定義

```sql
-- 記事マスター
CREATE TABLE articles (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    slug        TEXT UNIQUE NOT NULL,           -- 例: western_us_event_slides_20260508
    source_pdf  TEXT,                           -- 例: western_us_event_slides_5.08.2026.pdf
    agency      TEXT,
    draft_path  TEXT,                           -- note_drafts/ 相対パス
    pub_path    TEXT,                           -- published_articles/ 相対パス
    note_url    TEXT,
    classification TEXT DEFAULT 'PUBLIC',
    -- classification: PUBLIC / INTERNAL / CONFIDENTIAL / S_CLASS
    status      TEXT DEFAULT 'draft',
    -- status: draft / in_review / warn / blocked / pass / published
    created_at  TEXT DEFAULT (datetime('now','localtime')),
    updated_at  TEXT DEFAULT (datetime('now','localtime'))
);

-- Codex 監査セッション（1記事に最大2回）
CREATE TABLE codex_sessions (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id       INTEGER REFERENCES articles(id),
    iteration        INTEGER DEFAULT 1,         -- 1 or 2（3以上は禁止）
    request_path     TEXT,                      -- review_requests/ 相対パス
    response_path    TEXT,                      -- review_reports/ 相対パス
    model_id         TEXT,                      -- 例: gpt-4o-2024-08-06
    checklist_ver    TEXT,                      -- 例: v1.11
    verdict          TEXT,                      -- PASS / WARN / BLOCK
    block_count      INTEGER DEFAULT 0,
    warn_count       INTEGER DEFAULT 0,
    pass_count       INTEGER DEFAULT 0,
    started_at       TEXT,
    completed_at     TEXT,
    auto_triggered   INTEGER DEFAULT 1          -- 1=agmsg自動, 0=人間手動
);

-- WARN 項目（修正追跡）
CREATE TABLE warn_items (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    INTEGER REFERENCES codex_sessions(id),
    warn_code     TEXT,                         -- 例: W-03
    phase         TEXT,                         -- 例: P2-4
    description   TEXT,
    fix_status    TEXT DEFAULT 'pending',
    -- fix_status: pending / applied / rejected / deferred
    human_decision TEXT,                        -- 人間がいつ判断したか
    fixed_at      TEXT
);

-- ワークフローイベントログ
CREATE TABLE workflow_events (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id      INTEGER REFERENCES articles(id),
    event_type      TEXT,
    -- draft_created / codex_requested / codex_received /
    -- warn_presented / warn_fixed / warn_rejected /
    -- published / git_committed / stopped / error
    detail          TEXT,
    human_required  INTEGER DEFAULT 0,          -- 1=人間確認が必要
    human_approved  INTEGER,                    -- 1=承認, 0=却下, NULL=未確認
    start_time      TEXT,                       -- フェーズ開始時刻
    end_time        TEXT,                       -- フェーズ終了時刻
    elapsed_minutes REAL,                       -- 所要時間（分）
    created_at      TEXT DEFAULT (datetime('now','localtime'))
);

-- モデルバージョン履歴
CREATE TABLE model_versions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    checked_at  TEXT,
    service     TEXT,                           -- claude / codex / agmsg
    model_id    TEXT,
    version_str TEXT,
    changed     INTEGER DEFAULT 0              -- 前回から変更があれば 1
);

-- 記事ごとの現在オーナー管理（§3-A 参照）
CREATE TABLE workflow_owner (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    article_slug  TEXT NOT NULL,
    current_owner TEXT NOT NULL,              -- CLAUDE / CODEX / HUMAN
    updated_at    TEXT DEFAULT (datetime('now','localtime'))
);
```

### 6-3. 主要クエリ例

```sql
-- 未完了記事の確認
SELECT slug, status, updated_at FROM articles WHERE status NOT IN ('published');

-- 特定記事の WARN 残件確認
SELECT w.warn_code, w.description, w.fix_status
FROM warn_items w
JOIN codex_sessions s ON w.session_id = s.id
JOIN articles a ON s.article_id = a.id
WHERE a.slug = 'western_us_event_slides_20260508'
  AND w.fix_status = 'pending';

-- モデル変更検知
SELECT service, model_id, checked_at
FROM model_versions
WHERE changed = 1
ORDER BY checked_at DESC LIMIT 5;
```

---

## 7. 最小 PoC 構成

### 7-1. スコープ

1 記事・1 回の Codex 往復のみ。  
agmsg のインストール確認から review_reports/ 保存まで。公開・git 操作は含まない。

### 7-2. 必要コンポーネント

| コンポーネント | 役割 | 実装状態 |
|-------------|------|---------|
| agmsg | Codex への送信・受信 | 未インストール（PoC 前提条件）|
| `review_requests/` ディレクトリ | 監査依頼パッケージの置き場 | 未作成 |
| `scripts/codex_request_gen.py` | 依頼ファイル自動生成スクリプト | 未作成 |
| `workflow.db` | SQLite 状態管理 | 未作成 |
| Codex 監査プロンプトテンプレート | 構造化プロンプト | 設計済み（§8 参照） |

### 7-3. PoC フロー（最小）

```
[STEP 1] Claude Code がドラフト生成
  → note_drafts/<slug>_note_version.md を保存

[STEP 2] Claude Code が依頼パッケージを生成
  → review_requests/codex_request_YYYYMMDD_<slug>.md を作成
  → 内容：ドラフト全文 + 監査プロンプト + チェックリスト参照

[STEP 3] agmsg でCodexへ送信（Claude Code が Bash tool 経由で実行）
  $ agmsg send \
      --to codex \
      --input review_requests/codex_request_YYYYMMDD_<slug>.md \
      --output review_reports/codex_audit_YYYYMMDD_<slug>_auto.md

[STEP 4] agmsg が完了したら Claude Code が review_reports/ を読み込む
  → BLOCK / WARN / PASS を解析
  → SQLite に結果を記録

[STEP 5] 判定別の処理
  BLOCK  → 停止。人間に BLOCK 内容を提示
  WARN   → WARN 一覧を提示。各項目を人間に確認
  PASS   → 人間に報告。note_drafts の Finder 表示コマンドを自動出力。git / 公開は人間が判断

[停止点]
  → STEP 5 のすべてのケースで人間に報告して停止
  → git / 公開 / ファイル削除は PoC スコープ外
```

### 7-4. PoC 成功基準

#### 機能基準

- [x] agmsg が `review_reports/` にファイルを生成できる（Fallback：手動ペーストで実施）
- [x] 生成されたファイルを Claude Code が正常に解析できる
- [x] BLOCK / WARN / PASS を正確に抽出できる（BLOCK:3 WARN:4 PASS:6 を確認）
- [x] SQLite に 1 件のセッション記録が保存できる
- [N/A] agmsg タイムアウト時に Claude Code が停止できる（agmsg 未インストール・Fallback 使用）
- [x] workflow_owner チェックが送信前に動作する（Current Owner 制御）
- [N/A] S_CLASS 判定時にハードストップが発動する（test_article は PUBLIC 分類のため未発動）

#### 時短基準（追加）

| 測定指標 | 従来（手動） | 目標（半自動） |
|---------|-----------|------------|
| 1 記事あたり総処理時間 | 約 90 分 | **45 分以内** |
| Codex 監査往復時間 | 人間手動：15〜30 分 | agmsg 自動：5 分以内 |

**測定方法：** `workflow_events` テーブルの `start_time` / `end_time` / `elapsed_minutes` で記録する。

計測対象フェーズ：

| フェーズ | event_type | 計測内容 |
|---------|-----------|---------|
| ドラフト作成 | `draft_created` | テキスト抽出〜note_drafts/ 保存まで |
| Codex 監査 | `codex_requested` → `codex_received` | agmsg 送信〜レスポンス受信まで |
| 修正作業 | `warn_fixed` | WARN 提示〜最終修正完了まで |
| 公開確認 | `published` | 人間による note 公開〜URL 確認まで |

**NotebookLM ログへの集計：** §5 の自動生成ログに `elapsed_minutes` の合計・フェーズ別内訳を含める（§5-3 参照）。

---

## 8. Codex 監査プロンプトテンプレート設計

依頼ファイル（`review_requests/codex_request_YYYYMMDD_<slug>.md`）の構成：

```markdown
# Codex 監査依頼

## 依頼メタデータ
- 記事スラッグ：<slug>
- ドラフトファイル：<path>
- チェックリスト：docs/audit_checklist_v1.md（v1.11）
- 依頼日時：YYYY-MM-DD HH:MM

## 監査指示
以下の UAP 翻訳記事ドラフトを、docs/audit_checklist_v1.md に従って監査してください。

【重要な制約】
- 応答は監査レポートのみとしてください
- Claude Code への指示・再監査要求は行わないでください
- 修正を自動的に適用しないでください
- 判定は PASS / WARN / BLOCK のいずれかのみ使用してください
- 出力フォーマットは以下の構造に従ってください：

## 出力フォーマット（必須）
---CODEX_AUDIT_START---
VERDICT: [PASS|WARN|BLOCK]
BLOCK_COUNT: [数値]
WARN_COUNT: [数値]
PASS_COUNT: [数値]
MODEL: [使用モデルID]
---ITEMS_START---
[P0-1] [PASS|WARN|BLOCK] [説明]
...
---ITEMS_END---
---WARN_DETAILS_START---
W-01: [セクション名] | [該当文] | [修正案]
...
---WARN_DETAILS_END---
---CODEX_AUDIT_END---

## ドラフト本文
<ここにドラフト全文を挿入>
```

### 8-1. パース方法（Claude Code 側）

```python
# 想定パースロジック（設計段階）
import re

def parse_codex_response(file_path):
    with open(file_path) as f:
        content = f.read()
    
    verdict = re.search(r'VERDICT: (PASS|WARN|BLOCK)', content).group(1)
    warn_count = int(re.search(r'WARN_COUNT: (\d+)', content).group(1))
    block_count = int(re.search(r'BLOCK_COUNT: (\d+)', content).group(1))
    model_id = re.search(r'MODEL: (.+)', content).group(1).strip()
    
    warn_details = re.findall(
        r'(W-\d+): (.+?) \| (.+?) \| (.+)',
        content[content.find('---WARN_DETAILS_START---'):]
    )
    
    return {
        'verdict': verdict,
        'warn_count': warn_count,
        'block_count': block_count,
        'model_id': model_id,
        'warn_details': warn_details
    }
```

---

## 9. Fallback Plan：review_requests / review_reports ファイル受け渡し（agmsg 不使用時）

agmsg が利用できない場合に即座に切り替えられるフェイルセーフ運用。  
代替「案」ではなく、**常に維持する本番フォールバック**として位置付ける。

### フォールバック発動条件

以下のいずれかが発生した場合、即座にこの手順に切り替える：

| 発動条件 | 対処 |
|---------|------|
| agmsg 故障・インストール不可 | STEP 3 のみ手動に切り替え |
| SQLite 破損 | DB を再作成し、手動で状態を補完 |
| Codex 仕様変更（API 互換性破壊） | プロンプトテンプレートを更新するまで手動継続 |
| Claude Code 仕様変更 | 設計書を更新するまで手動継続 |

**変更点：** STEP 3 のみ手動に切り替え。他は同一。

### 9-A. 手動 Fallback フロー（Codex Terminal ペースト）

`codex_request_gen.py` 実行後、以下の手順が自動表示される：

```
【手順 1】Finder でファイルを確認：
  open -R review_requests/codex_request_YYYYMMDD_<slug>.md

【手順 2】依頼文をクリップボードへコピー：
  pbcopy < review_requests/codex_request_YYYYMMDD_<slug>.md

【手順 3-A】Codex Terminal に貼り付け（手動 Fallback）
  ペースト後、Codex が出力した監査結果を以下のファイルへ保存：
  review_reports/codex_audit_YYYYMMDD_<slug>.md

【手順 4】監査結果の解析（Codex 完了後）：
  python3 scripts/codex_flow.py \
    --slug <slug> \
    --fallback \
    --response-path review_reports/codex_audit_YYYYMMDD_<slug>.md

【PASS時・codex_flow.py が自動表示するnote投稿前Finder確認コマンド】
  1. ドラフトFinder表示コマンド：
    open -R note_drafts/ai_summary_<slug>_note_version.md

  2. 使用画像Finder表示コマンド：
    open -R page_images/<画像フォルダ>/page_0001.png
    open -R page_images/<画像フォルダ>/page_0002.png

  3. 画像フォルダFinder表示コマンド：
    open page_images/<画像フォルダ>/

  4. 注意：
     Mac Studio側に画像がない場合は、Mac Studio側Finderでは直接表示できない旨と、
     Mac mini側の画像配置確認を促すメッセージを表示する。
```

### 9-B. Codex CLI 非対話実行（STEP 3 自動化候補）

**調査結果（2026-06-09）：Codex CLI v0.137.0 で非対話実行が可能。**

```bash
# インストール確認
which codex   # → /opt/homebrew/bin/codex
codex --version  # → codex-cli 0.137.0
```

有効な非対話オプション（`codex exec --help` で確認済み）：

| オプション | 内容 |
|---|---|
| `codex exec -` | stdin からプロンプトを読み込む（非対話） |
| `-o <FILE>` | エージェント最終メッセージを指定ファイルへ保存 |
| `-s read-only` | シェルコマンドを read-only サンドボックスで制限 |
| `-m <MODEL>` | 使用モデルを指定（例: `o4-mini`） |

安全な実行コマンド例（`codex_request_gen.py` 生成時に自動表示）：

```bash
【手順 3-B】Codex CLI 非対話実行（自動）：
  codex exec - \
    -s read-only \
    -m o4-mini \
    -o review_reports/codex_audit_YYYYMMDD_<slug>.md \
    < review_requests/codex_request_YYYYMMDD_<slug>.md
```

**注意：** `-s read-only` はエージェントのツール呼び出しを制限するが、`-o` による出力ファイル保存は CLI 自身が行うため矛盾しない。実際の保存動作は次のテスト記事で確認予定（§13-5 参照）。

この方式でも STEP 2（依頼パッケージ生成）と STEP 4〜5（結果解析・SQLite 記録）は自動化済みのため、往復コピペの負担は大幅に軽減される。

---

## 10. 導入ロードマップ

| フェーズ | 内容 | 状態 |
|---------|------|------|
| フェーズ 0 ✓ | 設計のみ。手動フロー継続 | 完了 |
| フェーズ 1 ✓ | SQLite DB 作成・review_requests/ 整備・プロンプトテンプレート確定 | 完了 |
| フェーズ 2 ✓ | Fallback で 1 記事動作確認（2026-06-05）。agmsg 本番導入は保留 | 完了（Fallback）|
| **フェーズ 3（現在）** | 依頼生成後の手順自動表示・Codex CLI 非対話実行調査・本番記事への適用 | **進行中（2026-06-09）**|
| フェーズ 4 | `codex exec` 非対話実行の PoC（テスト記事で保存動作確認） | 待機中 |
| フェーズ 5 | agmsg または Codex CLI による STEP 3 完全自動化 | 待機中 |

---

## 11. 未解決事項・要判断

- agmsg の具体的なインストール方法・対応プロバイダー（公式ドキュメント確認が必要）
- agmsg が OpenAI モデルを直接指定できるか（`--model gpt-4o` 等）
- SQLite を git 管理外にするか（推奨：.gitignore に追加）
- `review_requests/` ディレクトリを git 管理するか（依頼ファイルは含むべきか）
- PoC の実施タイミング（次の記事制作時か、独立テストとして実施か）

---

---

## 12. 実装ファイル一覧（PoC 最小実装）

### 12-1. スクリプト一覧

| ファイル | 役割 | 動作環境 |
|---------|------|---------|
| `scripts/init_db.py` | SQLite DB 初期化（全テーブル作成） | Mac Studio / Mac mini |
| `scripts/codex_request_gen.py` | 依頼パッケージ生成（STEP 2） | Mac Studio |
| `scripts/codex_flow.py` | agmsg 送信〜結果解析（STEP 3〜5）+ フォールバック | Mac Studio |
| `scripts/version_monitor.py` | agmsg/Python/SQLite/bash/スキーマ バージョン監視 | Mac Studio / Mac mini |
| `scripts/notebooklm_log_gen.py` | 公開後 NotebookLM ログ自動生成 | Mac Studio |
| `scripts/post_publish_workflow.py` | note公開後の保存版・公開ログ作成とcommit準備表示 | Mac Studio |

### 12-2. 標準フロー（通常モード）

```bash
# セッション開始時（バージョン確認）
python3 scripts/version_monitor.py

# 初回のみ: DB 初期化
python3 scripts/init_db.py

# STEP 2: 依頼パッケージ生成
python3 scripts/codex_request_gen.py --slug <スラッグ>

# STEP 3〜5: agmsg 経由で送信・結果解析
python3 scripts/codex_flow.py --slug <スラッグ> \
    --request-path review_requests/codex_request_YYYYMMDD_<スラッグ>.md

# 公開後: NotebookLM ログ生成
python3 scripts/notebooklm_log_gen.py --slug <スラッグ> --note-url <URL>

# 公開後: 保存版・ログ作成・commit準備表示（git操作は表示のみ）
python3 scripts/post_publish_workflow.py \
    --slug <スラッグ> \
    --draft note_drafts/ai_summary_<スラッグ>_note_version.md \
    --note-url <URL> \
    --audit review_reports/codex_audit_YYYYMMDD_<スラッグ>.md
```

### 12-3. フォールバックフロー（§9 Fallback Plan）

agmsg 故障・未インストール時は STEP 3 のみ手動に切り替え：

```bash
# STEP 2 は同じ（依頼パッケージを生成）
python3 scripts/codex_request_gen.py --slug <スラッグ>

# STEP 3（手動）: review_requests/<スラッグ>.md を Codex にペースト
# → 出力を review_reports/codex_audit_YYYYMMDD_<スラッグ>_manual.md に保存

# STEP 4〜5: 保存済みファイルを解析
python3 scripts/codex_flow.py --slug <スラッグ> \
    --fallback \
    --response-path review_reports/codex_audit_YYYYMMDD_<スラッグ>_manual.md
```

### 12-4. SQLite 確認クエリ例

```bash
sqlite3 workflow.db "SELECT slug, current_owner FROM articles a
  JOIN workflow_owner w ON a.slug = w.article_slug
  ORDER BY w.updated_at DESC LIMIT 5;"

sqlite3 workflow.db "SELECT slug, SUM(elapsed_minutes) AS total_min
  FROM workflow_events e JOIN articles a ON e.article_id = a.id
  GROUP BY slug ORDER BY total_min DESC;"
```

### 12-5. .gitignore 推奨追加（別途対応）

```
workflow.db
review_requests/
```

### 12-6. note公開後フロー（post_publish_workflow.py）

`post_publish_workflow.py` は、note記事公開後の定型作業を半自動化する統合支援スクリプトである。

実行例：

```bash
python3 scripts/post_publish_workflow.py \
  --slug DOE-UAP-D001_pantex_unidentified_object_incident_report \
  --draft note_drafts/ai_summary_DOE-UAP-D001_pantex_unidentified_object_incident_report_note_version.md \
  --note-url https://note.com/deft_ibis3303/n/xxxx \
  --audit review_reports/codex_audit_20260609_DOE-UAP-D001_pantex_unidentified_object_incident_report_iter2.md
```

自動作成するファイル：

- `published_articles/ai_summary_<slug>_published_YYYYMMDD.md`
- `logs/notebooklm/YYYY-MM-DD_<slug>_published_log.md`

表示する情報：

- 作成ファイル一覧
- `git diff` 対象ファイル一覧
- commit対象候補
- commit対象外候補
- source_registry変更候補（表示のみ）
- 実行すべきgitコマンド案（表示のみ）
- Mac mini pullコマンド案（表示のみ）

安全条件：

- `git add` / `git commit` / `git push` は自動実行しない
- Mac mini pull は自動実行しない
- `review_logs/source_registry.csv` は自動変更しない
- `metadata/uap-csv-cache.csv` は触らない
- `raw_pdf/` / `page_images/` は触らない
- `workflow.db` は読まない・書かない

Mac mini pullコマンド案：

```bash
ssh agentai@safinoMac-mini.local 'cd /Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/repo && git pull'
```

---

---

## 13. PoC 実施記録（2026-06-05）

### 13-1. 実施概要

| 項目 | 内容 |
|------|------|
| 実施日 | 2026-06-05 |
| 実施環境 | Mac Studio（メイン）/ Mac mini（ワーカー）|
| agmsg 状態 | 両環境とも NOT_INSTALLED → §9 Fallback Plan で実施 |
| 実施スラッグ | test_article_semiauto_poc |

### 13-2. 環境別確認結果

| 確認項目 | Mac Studio | Mac mini |
|---------|-----------|---------|
| workflow.db 作成 | ✓ | ✓ |
| version_monitor.py | ✓ | ✓ |
| Codex 依頼パッケージ生成 | ✓ | — |
| 監査結果解析（BLOCK/WARN/PASS）| ✓ | — |
| NotebookLM ログ生成 | ✓ | — |
| git pull / git status クリーン | ✓ | ✓ |

### 13-3. PoC 成功基準の達成状況

agmsg に依存しない項目はすべて Fallback 経由で確認済み。

| 基準 | 状態 | 備考 |
|------|------|------|
| review_reports/ にファイル生成 | ✓ Fallback | 手動ペーストで実施（agmsg 未使用）|
| 生成ファイルの正常解析 | ✓ | |
| BLOCK / WARN / PASS 抽出 | ✓ | BLOCK:3 WARN:4 PASS:6 を確認 |
| SQLite セッション記録 | ✓ | |
| agmsg タイムアウト時の停止 | N/A | agmsg 未インストールのため未検証 |
| workflow_owner チェック | ✓ | |
| S_CLASS ハードストップ | N/A | test_article は PUBLIC のため未発動 |

### 13-4. 確定した運用方針

- agmsg は現時点で本番導入を保留。§9 Fallback Plan を常時フォールバックとして維持する。
- workflow.db は Mac Studio のみでマスター管理。Mac mini 側は独立テスト用。両者は同期しない。
- Python バージョン差異（Mac Studio 3.12.4 / Mac mini 3.9.6）は暫定運用注意として扱い、3.10+ 構文禁止を継続する。
- フェーズ 3（本番適用）の実施タイミングは agmsg の実装可能性が確認できた時点で判断する。

---

---

## 13-5. フェーズ 3 実施記録（2026-06-09）

### 実施内容

| 項目 | 内容 |
|------|------|
| 実施日 | 2026-06-09 |
| 対象記事 | DOE-UAP-D001_pantex_unidentified_object_incident_report |
| 変更ファイル | scripts/codex_request_gen.py / docs/claude_codex_semiauto_workflow_design.md |

### Codex CLI 調査結果

- `codex` CLI が `/opt/homebrew/bin/codex`（v0.137.0）にインストール済みであることを確認
- `codex exec` サブコマンドで非対話実行が可能であることを確認（`--help` 参照）
- stdin 読み込み（`-`）・出力ファイル保存（`-o`）・read-only サンドボックス（`-s read-only`）の組み合わせが使用可能
- 実際の保存動作（`-o` でファイルが正しく生成されるか）はフェーズ 4 のテスト記事で確認予定

### `codex_request_gen.py` への変更

- PROMPT_TEMPLATE に「出力先ファイル・note_drafts 編集禁止・マーカー必須」を明記
- 依頼生成後に人間向け手順（`open -R` / `pbcopy` / 3-A 手動 / 3-B CLI / 4 解析）を自動表示する `_print_next_steps()` 関数を追加
- `response_path` を `generate_request()` 内で確定し、テンプレートと手順表示の両方で一貫して参照するよう変更

### 確定した運用（フェーズ 3）

```
人間の操作（最小）：
  1. python3 scripts/codex_request_gen.py --slug <slug>
     → 手順が自動表示される
  2. pbcopy < review_requests/<file>.md  （表示されたコマンドをコピペ）
  3. Codex Terminal に貼り付け → 監査結果を review_reports/ に保存

Claude Code：
  python3 scripts/codex_flow.py --fallback ...  （自動解析）
```

---

## 13-6. 半自動化PoC 本番適用第1弾（DOE-UAP-D001）記録（2026-06-09）

### 概要

| 項目 | 内容 |
|------|------|
| 実施日 | 2026-06-09 |
| 対象記事スラッグ | DOE-UAP-D001_pantex_unidentified_object_incident_report |
| 記事種別 | 限定情報記事 × 画像記事（UCNI指定・2ページのみ公開） |
| note 公開URL | https://note.com/deft_ibis3303/n/nec7810337531 |
| 設計書バージョン | v1.3〜v1.4 |

### Codex 監査フロー実績

| iteration | 判定 | BLOCK | WARN | 備考 |
|-----------|------|-------|------|------|
| iter1 | BLOCK | 2 | 2 | B-01:source_registry未登録 / B-02:Source URL表記 / W-01:日付ゼロ埋め / W-02:registry照合不完全 |
| iter2 | PASS | 0 | 0 | B-01/B-02/W-01修正後 / W-02は自動解消 |

### 修正記録

- **B-01:** review_logs/source_registry.csv に #R02-001 エントリを新規追加
- **B-02:** メタデータの `Source URL` ラベルを `WAR.GOV（公開ページ）` に変更し `Download URL`（直接PDF URL）と分離
- **W-01:** `Release Date：2026年5月22日` → `2026年05月22日`（月ゼロ埋め）

### 確認できた PoC 効果

- codex_request_gen.py による依頼ファイル生成・next steps 自動表示が本番で機能
- codex_flow.py --fallback による BLOCK 判定解析・修正提示が本番で機能
- iter2 PASS 判定後の Finder 表示コマンド出力（v1.4 追加機能）が機能
- source_registry への #R02-001 登録が Codex 照合チェック（P1-1-FILE）に有効であることを確認

### 関連ファイル

- 依頼（iter1/iter2共通）: review_requests/codex_request_20260609_DOE-UAP-D001_pantex_unidentified_object_incident_report.md
- 監査レポート iter1: review_reports/codex_audit_20260609_DOE-UAP-D001_pantex_unidentified_object_incident_report.md
- 監査レポート iter2: review_reports/codex_audit_20260609_DOE-UAP-D001_pantex_unidentified_object_incident_report_iter2.md
- 公開記事保存版: published_articles/ai_summary_DOE-UAP-D001_pantex_unidentified_object_incident_report_published_20260609.md
- 公開ログ: logs/notebooklm/2026-06-09_DOE-UAP-D001_pantex_unidentified_object_incident_report_published_log.md

---

*v1.3 更新（2026-06-09）：§9 に Codex CLI 調査結果と手順自動表示を追加。§10 ロードマップをフェーズ 3〜5 に更新。§13-5 実施記録を追加。*

*v1.4 更新（2026-06-09）：`codex_flow.py` の PASS 判定時に、ドラフト Finder 表示コマンド（`open -R` / `open`）を自動出力するよう変更。`--draft-path` 引数を追加（省略時はスラッグから自動推定）。§9-A にコマンド例を追記。§13-6 に半自動化PoC本番適用第1弾（DOE-UAP-D001）記録を追加。*

*v1.5 更新（2026-06-09）：`codex_flow.py` PASS 判定時と `codex_request_gen.py` 手順5に、ドラフト内 `page_images/` 参照を自動抽出して Finder 表示コマンドを出力する `_get_image_info()` / `_print_image_steps()` を追加。Mac Studio 側に画像がない場合は Mac mini 参照メッセージを表示。§9-A に表示例を追記。*

*v1.6 更新（2026-06-09）：`codex_flow.py` PASS 判定時と `codex_request_gen.py` 手順5の表示を、1. ドラフトFinder表示、2. 使用画像Finder表示、3. 画像フォルダFinder表示、4. Mac Studio側に画像がない場合の注意、の4項目に整理。画像が1枚のみでも画像フォルダFinder表示コマンドを出力し、Finderコマンド用のパスをshell quoteするよう更新。*

*v1.7 更新（2026-06-09）：`scripts/post_publish_workflow.py` を追加。note公開後に `published_articles/` 保存版と `logs/notebooklm/` 公開ログを作成し、git diff対象・commit対象候補・commit対象外候補・gitコマンド案・Mac mini pullコマンド案を表示する。git操作、Mac mini pull、source_registry変更、metadata/raw/page_images/workflow.db変更は自動実行しない。*
