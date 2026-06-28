# Claude トークン削減のためのローカル処理分離設計

**作成日：** 2026-06-23  
**対象：** UAP Translation Project — Release 02 VID 公開パイプライン全体  
**目的：** Claude Code のコンテキスト消費を削減し、判断・意思決定に特化させる  
**ステータス：** 設計のみ（未実装）

---

## 0. 問題の定義

### 現在の Claude Code のトークン負荷（定量把握）

| 作業種別 | 1回あたり推定トークン | 頻度 | 主な消費源 |
|---|---|---|---|
| 78件一覧の手動照合 | ~8,000 | リリースごと | files_catalog.csv + draft一覧の同時読み込み |
| Codex audit レポート生成 | ~3,000〜6,000 | 1件あたり | ドラフト全文読み込み + 14項目評価 |
| rule_candidate_scan（手動） | ~2,000〜4,000 | 1件あたり | ドラフト全文読み込み + KNOWN_ORGS照合 |
| publish_queue dry-run 生成 | ~12,000 | リリースごと | 78件×各項目のCSV/ファイル突合 |
| 残課題確認（セッション引き継ぎ） | ~5,000〜10,000 | セッションごと | git status + 複数レポートの再読み込み |
| **合計（Release 02 1バッチ）** | **~150,000+** | — | — |

### トークン消費の構造的原因

```
Claude Code が行っていること（現状）
├── [A] 機械的チェック    ← Pythonで十分
│   ├── #TBD 残存検出
│   ├── 作業メモ行の検出
│   ├── article_id フッター形式確認
│   ├── publish_order 重複チェック
│   └── Codex audit VERDICT/BLOCK集計
│
├── [B] パターンマッチング ← ローカルLLMで可
│   ├── 略称補足漏れ（CAT-01）
│   ├── 禁止表現チェック（CAT-02）
│   ├── 日付ゼロ埋め（CAT-04）
│   ├── note禁止フォーマット（CAT-05）
│   └── 客観性・断定表現（P2-OBJECTIVITY）
│
└── [C] 意思決定・判断    ← Claudeが必要
    ├── 2ドラフト比較と正規版選択
    ├── WARN→BLOCK昇格判断
    ├── 新規ルール追加（CAT-xx）
    ├── 例外処理（ファイル名・構造異常）
    └── リリース全体設計変更
```

---

## 1. Python で置き換え可能な作業

### 判断基準

- 正規表現 / ファイル存在確認 / CSV読み込みで完結する
- 出力が「あり/なし」「件数」「ファイルパス」のいずれか
- 例外も定義可能（HOLD, SKIP, archive済みなど）

### 対象作業一覧

| ID | 作業 | 現在のClaude負担 | Python化後 |
|---|---|---|---|
| P-01 | #TBD タイトル残存検出 | ドラフト1件ずつ読み込んで grep | `grep -r '#TBD'` 相当を一括実行 |
| P-02 | 作業メモ行（→ 使用ファイル：）残存検出 | 同上 | 同上 |
| P-03 | article_id フッター形式確認 | フッター最終行のパターン目視 | `📋 \*\*article_id：` の regex マッチ |
| P-04 | publish_order 重複/欠番チェック | 78件一覧を手動照合 | set差分比較 |
| P-05 | Codex audit VERDICT 集計 | review_reports/ を逐次読み込み | VERDICT: / BLOCK: / WARN: を正規表現抽出 |
| P-06 | note_draft ↔ files_catalog 突合 | CSV + ls を交互に読み込み | pandas join |
| P-07 | thumbnail ディレクトリ存在確認 | ls で逐次確認 | `Path.is_dir()` 一括スキャン |
| P-08 | archive/ ドラフト vs 正規ドラフト 重複検出 | ls + 目視 | filename stem 比較 |
| P-09 | Codex iter 最新ファイル特定 | ls + 日付 / iter番号で判断 | glob + iter番号ソート |
| P-10 | publish queue 78件一覧の自動生成 | 毎回手動で表を作成 | CSV + glob から Markdown テーブル生成 |

---

## 2. ローカルLLM で置き換え可能な作業

### 判断基準

- 自然言語テキストの内容評価が必要
- ただし「PASS/WARN/BLOCK」の3択出力に収束できる
- 誤判定のコストが低い（Claude が最終確認する）
- 外部API送信禁止のため、ollama等のローカル推論を使用

### 推奨モデル環境

```
Ollama + llama3.2 / qwen2.5 / gemma3 のいずれか
  → Mac Studio（M2 Ultra）または Mac mini でローカル推論
  → 外部送信なし・オフライン動作
  → 応答 JSON 形式で受け取り、Pythonで後処理
```

### 対象作業一覧

| ID | 作業 | Codex チェック項目 | ローカルLLMへの指示難度 |
|---|---|---|---|
| L-01 | 略称補足漏れ検出（CAT-01） | P2-ABBR | 低：KNOWN_ORGS辞書 + 本文比較 |
| L-02 | 禁止表現チェック（CAT-02） | P2-OBJECTIVITY | 低：禁止リスト + regex + LLM判定 |
| L-03 | 日付ゼロ埋めチェック（CAT-04） | P1-DATE | 最低：正規表現で十分（L-03はPython化推奨） |
| L-04 | 要点3項目の構造確認（P2-KEYPOINT） | P2-KEYPOINT | 中：番号付き太字3項目の形式+内容確認 |
| L-05 | 客観性チェック（P2-OBJECTIVITY） | P2-OBJECTIVITY | 中：断定表現リスト + LLM文脈判断 |
| L-06 | AI解析メモ位置確認（P2-STRUCT） | P2-STRUCT | 低：セクション順序を正規表現で確認 |
| L-07 | 免責文・警告文の存在確認 | P2-WARNING | 最低：固定文字列の存在確認（Python化推奨） |
| L-08 | 初回Codex audit（iter1） | 全14項目 | 高：ローカルLLMの品質次第 |

### ローカルLLM導入方針

```
Claude Code の役割：
  ┌─────────────────────────────────────┐
  │ 設計・判断・例外処理 のみ           │
  │ ローカルLLM出力の最終レビュー       │
  └─────────────────────────────────────┘
          ↑ 疑問/BLOCK のみ上申
  ┌─────────────────────────────────────┐
  │ ローカルLLM（Ollama）               │
  │ iter1 Codex audit の初回スキャン    │
  │ CAT-01/02/04/05 rule scan           │
  │ 出力: JSON {check_id, verdict, note}│
  └─────────────────────────────────────┘
          ↑ ファイル読み込み・整形
  ┌─────────────────────────────────────┐
  │ Python スクリプト群                 │
  │ ファイル一覧・CSV突合・機械的チェック│
  └─────────────────────────────────────┘
```

---

## 3. Claude に残すべき判断作業

以下はローカル処理に移管しない。Claude Code のコンテキストで処理する。

| 判断種別 | 理由 |
|---|---|
| 2ドラフト比較と正規版選択 | 内容の質・充実度の価値判断が必要 |
| WARN → BLOCK 昇格判断 | ルール解釈・文脈依存の判断 |
| 新規ルール提案（CAT-xx） | プロジェクト方針と整合が必要 |
| ファイル構造異常の原因特定 | 例外的状況の因果推論 |
| release 設計変更（article_id体系等） | 全体影響の評価が必要 |
| ローカルLLM出力のエスカレーション確認 | BLOCK判定・WARN内容の最終レビュー |
| git操作・公開操作の判断 | 不可逆操作のため人間承認ループ必須 |

---

## 4. 最小実装案

### フェーズ1：Python 機械チェック（実装優先度：高）

**対象スクリプト：**

#### `scripts/local_ops/release_inventory_check.py`

```
目的: files_catalog.csv × note_drafts/ × codex_audit/ の3点突合
入力: --release R02 （または --all）
出力: review_reports/inventory_check_YYYYMMDD.md

チェック項目:
  - [P-01] #TBD タイトル残存
  - [P-02] 作業メモ行残存
  - [P-03] article_id フッター形式
  - [P-04] publish_order 重複/欠番
  - [P-05] Codex audit 最新VERDICT集計
  - [P-06] note_draft ↔ files_catalog 突合（欠落/余剰）
  - [P-07] thumbnail ディレクトリ存在確認
  - [P-08] archive/ ↔ 正規ドラフト 重複チェック
  - [P-09] Codex iter 最新ファイル特定

出力フォーマット（Markdown）:
  ## サマリー
  | 項目 | 件数 | 詳細 |
  |---|---|---|
  | ✅ 問題なし | N | |
  | ⚠️ 確認推奨 | N | ファイル名一覧 |
  | ❌ 要修正 | N | ファイル名一覧 |
  
  ## 詳細（⚠️/❌ のみ）
  ...
```

#### `scripts/local_ops/draft_quality_scan.py`

```
目的: 1件のドラフトに対してPython機械チェックを実行
入力: --draft <path> [--slug <slug>]
出力: stdout（PASS/WARN/FAIL + 項目一覧）

チェック項目:
  - [P-01] タイトル行の #TBD / #2_TBD 残存
  - [P-02] 作業メモ行 "→ 使用ファイル：" 残存
  - [P-03] フッター "📋 **article_id：" 形式
  - [P-03b] フッター publish_order: の数値形式
  - [P-04] 日付ゼロ埋め（月・日が1桁表記）
  - [P-05] DVIDS URL 形式確認（dvidshub.net/video/\d+）
  - [P-06] セクション順序（## 見出し の出現順）
  - [P-07] 免責文 "AI映像解析" / "AI概要版" の存在
  - [P-08] AARO 公式説明セクションの位置（文書メタデータ直後かどうか）

既存の rule_candidate_scan.py との関係:
  本スクリプトは "機械的形式チェック" のみ担当。
  CAT-01（略称）/ CAT-02（禁止表現）は rule_candidate_scan.py が担当（変更なし）。
  両スクリプトを順に実行して結果をマージする。

戻り値:
  0 = PASS（問題なし）
  1 = WARN（確認推奨）
  2 = FAIL（必須修正あり）
```

#### `scripts/local_ops/publish_queue_builder.py`

```
目的: DONE_CANDIDATE 一覧から publish_queue dry-run レポートを自動生成
入力: --release R02 [--output review_reports/...]

処理:
  1. files_catalog.csv から対象リリースの全ファイルを抽出
  2. release02_numbering_plan.md（またはDB）からarticle_id/publish_order を取得
  3. note_drafts/ に対応ドラフトが存在するか確認
  4. review_reports/codex_audit_*_{slug}*.md から最新VERDICTを抽出
  5. thumbnails/ ディレクトリの存在・重複を確認
  6. HOLD/SKIP/DONE_CANDIDATE/PENDING を分類
  7. Markdown テーブルを生成（publish_order 昇順）

出力:
  ## 1. サマリー
  ## 2. 警告一覧（⚠️ のみ）
  ## 3. 78件一覧（publish_order 昇順）
  ## 4. チェックリスト（残課題）

Claude Code への上申条件:
  - ⚠️ が1件以上ある場合のみ「確認が必要です」と出力
  - ⚠️ 0件の場合「投入可能です」と出力して終了
```

#### `scripts/local_ops/review_report_summarizer.py`

```
目的: 複数の Codex audit ファイルから VERDICT/BLOCK/WARN を集計
入力: --glob "review_reports/codex_audit_*_{slug}*.md"
      または --dir review_reports/ --release R02

処理:
  1. glob でファイル一覧取得
  2. 各ファイルから VERDICT: / BLOCK: / WARN: / PASS: を regex 抽出
  3. slug × iter番号 × VERDICT のマトリクスを生成
  4. 最新 iter の VERDICT を "current" として識別

出力（stdout または --output ファイル）:
  | slug | iter1 | iter2 | iter3 | current | BLOCK | WARN |
  |---|---|---|---|---|---|---|
  | PR060 | WARN | PASS | — | PASS | 0 | 0 |
  | PR066 | BLOCK | BLOCK | PASS | PASS | 0 | 1 |
  ...
  
  DONE_CANDIDATE: N件
  要確認（current=BLOCK）: N件 → ファイル名一覧
```

---

### フェーズ2：ローカルLLM（実装優先度：中）

#### `scripts/local_ops/local_llm_codex_iter1.py`

```
目的: Ollama を使って Codex iter1 相当のスキャンを実行
入力: --draft <path> --model llama3.2 [--ollama-url http://localhost:11434]

処理:
  1. ドラフト本文を読み込む
  2. Codex audit プロンプト（P2-OBJECTIVITY / P2-ABBR / P2-KEYPOINT のみ）を生成
  3. Ollama API（ローカル）へ POST
  4. JSON レスポンスを VERDICT/項目別結果に変換
  5. Markdown レポートを生成（`codex_audit_YYYYMMDD_{slug}_local_iter1.md`）

プロンプト構造（簡略版）:
  """
  あなたはUAP文書の日本語翻訳記事品質監査AIです。
  以下の記事ドラフトについて、以下3項目を確認し
  {"check_id": "P2-OBJECTIVITY", "verdict": "PASS|WARN|BLOCK", "note": "..."}
  の形式でJSON配列を返してください。
  チェック項目: P2-OBJECTIVITY, P2-ABBR, P2-KEYPOINT
  ---
  {draft_content}
  """

制約:
  - 外部API使用禁止（Ollama はローカルのみ）
  - 全14項目のうちP2系3項目のみ（最小化）
  - 出力は review_reports/ に保存、Claude の最終確認用

Claude への上申条件:
  - BLOCK が1件以上 → Claude に全文と結果を渡す
  - WARN のみ → サマリーのみ Claude に渡す
  - PASS → ログのみ（Claude への通知不要）
```

---

## 5. Claude Code への効果試算

### 現状 vs 導入後のトークン比較

| タスク | 現状（Claude） | 導入後（Claude） | 削減率 |
|---|---|---|---|
| 78件 publish_queue dry-run | ~12,000 tok | ~500 tok（結果確認のみ） | **96%** |
| 1件 draft quality check | ~3,000 tok | ~200 tok（WARN/FAIL 箇所のみ） | **93%** |
| Codex iter1（P2系3項目） | ~4,000 tok | ~500 tok（BLOCK箇所のみ） | **88%** |
| 残課題確認（セッション引き継ぎ） | ~8,000 tok | ~1,000 tok（スクリプト結果を渡す） | **88%** |
| リリース全体インベントリ | ~10,000 tok | ~1,000 tok（差分のみ） | **90%** |
| **合計（1リリース）** | **~150,000 tok** | **~15,000 tok** | **~90%** |

---

## 6. 実装順序（推奨）

```
優先度1（即効性・リスク低）:
  release_inventory_check.py   → 78件一覧の手動確認を自動化
  draft_quality_scan.py        → 作業メモ/#TBD の機械チェック

優先度2（Release 03 前に）:
  publish_queue_builder.py     → dry-run レポートの自動生成
  review_report_summarizer.py  → Codex audit 結果の集計自動化

優先度3（安定後）:
  local_llm_codex_iter1.py     → Ollama 導入後に検討
  （Ollama 未インストールの場合は後回し）
```

---

## 7. 実装時の制約・前提

- `workflow.db` は変更しない（読み取りのみ許可）
- `source_registry.csv` は変更しない（読み取りのみ許可）
- `files_catalog.csv` は変更しない（読み取りのみ許可）
- 外部API禁止（Ollama はローカルのみ）
- git操作禁止（スクリプト内から `git add/commit` しない）
- note 公開禁止（スクリプト内から note.com へのアクセスしない）
- Mac mini 側は触らない（ファイル書き込み先はローカルのみ）
- スクリプトは `scripts/local_ops/` に配置（既存 `scripts/` と分離）
- 出力レポートは `review_reports/` に保存（既存の命名規則に準拠）
- Python 標準ライブラリ + pandas + pathlib のみ（追加 pip 禁止）
  ※ ローカルLLM連携スクリプトのみ `httpx` / `requests` を許可（Ollama ローカルアクセス用）

---

## 8. 次のアクション（実装フェーズ開始時）

1. `scripts/local_ops/` ディレクトリ作成
2. `draft_quality_scan.py` から実装開始（最小・単一ファイル対象・依存なし）
3. 既存の `rule_candidate_scan.py` との I/F を確認（重複チェック回避）
4. `release_inventory_check.py` 実装
5. Release 03 開始前に `publish_queue_builder.py` 実装
6. Ollama 環境確認後に `local_llm_codex_iter1.py` を検討
