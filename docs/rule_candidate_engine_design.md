# Rule Candidate Engine 設計 v1.0

**作成日：** 2026-06-18
**対象プロジェクト：** UAP_TRANSLATION_PROJECT
**ステータス：** 初期運用中（候補提示フェーズ）
**スクリプト：** `scripts/rule_candidate_scan.py` v1.1.0

---

## 0. 設計の前提と制約

- **ドラフトは変更しない。** スクリプトは読み取り専用。修正は人間が行う。
- **外部APIは使わない。** 標準ライブラリのみで完結する。
- **S_CLASS ガードを維持する。** S_CLASS 疑いを検出した場合はレポートに警告を出力するのみで外部送信は行わない。
- **すべての検出は CANDIDATE として出力する。** 断定しない。
- **`docs/draft_rules_v2.md` はスクリプトから変更しない。** ルール更新は人間が行う。
- **`workflow.db` は変更しない。**

---

## 1. 目的

Rule Candidate Engine は、Codex 監査の前処理として、記事ドラフト内の以下を自動検出しレポートを生成するツールである。

- **組織名・略称の初出補足漏れ**（Codex WARN の反復原因の除去）
- **禁止表現の混入**（公開前に除去すべき断定・用語）
- **表記ゆれ候補**（日付フォーマット等、機械的に統一できる箇所）
- **note 禁止フォーマット**（投稿後の表示崩れ予防）

### なぜ Codex 前に実行するか

Codex が繰り返し WARN を出す主因（AARO 補足なし・CENTCOM 補足なし・元映像・日付ゼロ埋め）は、いずれも「ドラフト生成時点の見落とし」である。Codex 送信前にこれらを除去することで Codex のイテレーション回数を削減できる。

| タイミング | メリット | デメリット |
|-----------|---------|-----------|
| **Codex 前（推奨）** | 機械的ミスを事前除去 → WARN 削減 → Codex コスト節約 | 人間が 1 回レポートを確認する手間 |
| Codex 後 | なし | Codex が同じ内容を WARN で報告する → 二重コスト |

---

## 2. 現行ワークフローへの挿入位置

```
source_registry に登録済みか確認
  ↓
ドラフト生成（Claude Code）
  ↓
【★ここで実行】rule_candidate_scan.py --draft <draft> [--dry-run]
  ↓
  検出 0 件 → そのまま Codex 監査へ
  検出あり → review_reports/rule_candidates_YYYYMMDD_<slug>.md を生成
           → 人間が ACCEPT / REJECT 等を記入
           → ACCEPT 項目をドラフトに反映
           → Codex 監査へ
  ↓
Codex 監査（BLOCK / WARN / PASS）
  ↓
BLOCK 修正 → note インポート → プレビュー確認（人間）
  ↓
公開 → source_registry に note_url・published_date 記録
  ↓
post_publish_workflow.py → git commit → git push → Mac mini pull
```

---

## 3. 検出カテゴリ

### CAT-01：組織名・略称の初出補足候補

**目的：** 初出または近傍に日本語補足`（）`が確認できない組織名・略称を検出する。

**検出対象（主要）：**

| 略称 | 推奨補足 |
|-----|---------|
| AARO | 全領域異常解決局／米国防総省のUAP調査組織 |
| CENTCOM | 米国中央軍（中東・中央アジア周辺担当） |
| ODNI | 国家情報長官室 |
| FLIR | 前方監視赤外線カメラ |
| NVG | 暗視ゴーグル |
| AGL | 地上高度（above ground level） |
| JOC | 合同作戦センター |
| DoW | 米国防省 |
| DoD | 米国防総省 |

**対応ルール：** `docs/draft_rules_v2.md` Rule 7（略語・組織名の注釈）

**除外ロジック：**
- 文書ID・ファイル名内の略称はスキップ（例: `ODNI-UAP-D001` の `-` 直後）
- 括弧内の略称導入形式はスキップ（例: `Intelligence（ODNI / 国家情報長官室）`）
- 出典参照のみの括弧（`ファイル名より`・`csvより`）は補足なしとして検出

---

### CAT-02：禁止表現候補

**目的：** 誤解・事実誤認・公開品質に直結する表現を検出する。  
文体チェック（常体→丁寧体）は対象外。将来の **CAT-06** で管理する。

**検出対象：**

| 表現 | 対応ルール | 推奨代替 |
|-----|-----------|---------|
| 元映像・原本映像・オリジナル映像 | Rule 8-6 | → 通常表示映像 |
| 処理前映像・処理前の映像 | Rule 8-6 | → 通常表示映像 |
| 軍用赤外線（IR）カメラ映像 | Rule 4 | → IR映像とみられる映像（画像特性より） |
| 赤外線映像である | Rule 4 | → 赤外線映像とみられる（画像特性より） |
| 追跡対象物 | Rule 4 | → 暗点・追跡対象とみられる暗点 |
| IRカメラが捕捉した | Rule 4 | → 画像中央付近に確認できる |
| ローターブレードが確認できる | Rule 4 | → ローターブレード状の突起が見えるような形状 |
| AAROが確認した | Rule 3 | → AAROは（評価・推定）している |
| AAROが断定した | Rule 3 | → AAROは（評価・推定）している |

**対応ルール：** Rule 3（推定フォーマット）・Rule 4（画像記事表現基準）・Rule 8-6（元映像禁止）

---

### CAT-04：日付ゼロ埋め候補

**目的：** `YYYY年M月D日` 形式（月または日が 1 桁）を検出し、`YYYY年MM月DD日` 形式への統一を促す。

**検出例：**

```
2026年5月22日 → 2026年05月22日
2026年10月3日 → 2026年10月03日
```

**対応ルール：** `docs/draft_rules_v2.md` 未定義（新規ルール追加候補）  
- 複数ドラフトで 3 件以上出現した場合、Rule 7 への追記または Rule 9 として新設を検討する。

**将来の自動修正候補：** `--fix-dates` フラグ実装後は、人間確認なしで機械的修正が可能な唯一のカテゴリ。

---

### CAT-05：note 禁止フォーマット候補

**目的：** note 投稿後の表示崩れの原因となる Markdown 書式を検出する。

| 検出パターン | 問題 | 対応ルール |
|-----------|------|-----------|
| 行頭 `\| ... \|`（Markdown table） | note で空白化・欠落 | Rule 5 |
| 行頭 `>` （引用ブロック） | note で崩れ | Rule 5 |
| 行頭 ` ``` `（コードブロック） | note で崩れ | Rule 5 |

---

### 将来のカテゴリ（未実装）

| カテゴリ | 内容 | 課題 |
|---------|------|------|
| **CAT-03** | 単位換算漏れ（feet/miles/Fahrenheit 等） | Rule 7 対応済み。検出は数値文脈に依存 |
| **CAT-06** | 文体・丁寧体チェック（常体→丁寧体） | 文末判定ロジックが必要。単純な文字列マッチでは誤検知多発 |
| **CAT-07** | 内部パス公開候補（thumbnails/ 等） | `→ 使用ファイル：` 行の除外ロジックが必要 |
| **CAT-08** | uploader-defined title の断定化 | セクション単位の文脈判断が必要（regex 不向き） |

---

## 4. 人間が見るべき優先度

```
優先度 HIGH（必ず確認）
  CAT-02 禁止表現
    → 公開品質・事実誤認に直結。1件でも ACCEPT なら Codex 送信前に修正。
  CAT-01 組織名・略称補足
    → Codex WARN の主因。初出補足漏れは必ず修正。

優先度 MEDIUM（確認推奨）
  CAT-04 日付ゼロ埋め
    → フォーマット統一。修正は機械的で容易。
  CAT-05 note禁止フォーマット
    → 表示崩れリスク。Codex BLOCK になる前に除去。

優先度 LOW（まとめて確認可）
  NEW_RULE 候補
    → 複数ドラフトで繰り返し出現したもののみ rules に追加を検討。
  REJECT の理由記録
    → 誤検知パターン改善のための情報源。
```

**1 回あたりの目安所要時間：** 5〜10 分（11 件の ODNI ドラフトで確認）

---

## 5. ACCEPT / REJECT / RULE_UPDATE / NEW_RULE の処理方針

| 区分 | 処理者 | 操作内容 | 自動化可否 |
|-----|--------|---------|-----------|
| **ACCEPT** | 人間 | ドラフトを直接修正（スクリプトは修正しない） | 不可（文脈判断が必要） |
| **REJECT** | 人間 | 理由欄に記録。次回パターン改善の材料にする | 不可 |
| **RULE_UPDATE** | 人間 | `docs/draft_rules_v2.md` の該当ルールへ追記 | 不可（ルール文書は人間が管理） |
| **NEW_RULE** | 人間 | `docs/draft_rules_v2.md` に新セクション追加 | 不可 |

### 自動修正可能領域（将来）と人間承認必須領域

**自動修正可能（将来 `--fix-dates` / `--apply-approved` で対応）:**

| 項目 | 条件 |
|-----|------|
| CAT-04 日付ゼロ埋め | 純粋に機械的。文脈を問わず `YYYY年MM月DD日` に変換可能 |
| 明確な禁止語の置換候補提示 | 1対1の置換が確定しているもの（例: `元映像` → `通常表示映像`） |

**人間承認必須（自動化不可）:**

| 項目 | 理由 |
|-----|------|
| 組織名補足 | 挿入位置・文体・文脈が一定しない |
| 意味が変わる翻訳 | 文意の判断は人間にしかできない |
| 断定表現の調整 | 代替表現の選択が状況依存 |
| 新規ルール追加 | ルールの妥当性・適用範囲は人間が判断 |
| AARO 評価の断定化修正 | 文書ごとの文脈差が大きい |

---

## 6. docs/draft_rules_v2.md への反映条件

### 反映フロー

```
rule_candidates レポートで NEW_RULE / RULE_UPDATE が承認（ACCEPT）
  ↓
複数ドラフトで同じ候補が繰り返し出現（目安: 3 件以上）
  ↓
人間が docs/draft_rules_v2.md を直接編集
  ↓
同じドラフトに対して rule_candidate_scan.py を再実行
  → 新ルールに対応した検出パターンで REJECT / スキップになれば反映成功
  ↓
Codex 監査チェックリストとの整合確認
```

### ルール追加のトリガー条件

| トリガー | 対応 |
|---------|------|
| CAT-04 日付ゼロ埋めが 3 ドラフト以上で出現 | Rule 7 に「Release Date は YYYY年MM月DD日形式」を追記 |
| CAT-01 で同一組織が 2 ドラフト以上で初出未補足 | Rule 7 の対象例に追記 |
| CAT-02 の REJECT 率が高い | `FORBIDDEN_EXPRESSIONS` のパターンを精査・除去 |
| NEW_RULE が 3 回以上 ACCEPT される | Rule 9 以降として新規追加を検討 |

---

## 7. git_publish_helper.py との疎結合連携方針

### 基本方針：ソフトチェック（注記のみ）

`rule_candidate_scan.py` の実行有無は **commit の必須条件にしない**。

- `git_publish_helper.py --report` 実行時、対象スラッグの `rule_candidates_*.md` が存在しない場合は commit 候補セクションに注記を追加する（将来実装）
- scan 未実施 = commit 不可 には**しない**（運用の硬直化を防ぐ）
- 両ツールは単独でも使える独立性を維持する

### 将来の連携実装案（未実装）

```python
# git_publish_helper.py の build_report() に追加する想定コード（参考）
scan_done = any(
    slug in p.name
    for p in Path("review_reports").glob("rule_candidates_*.md")
)
if not scan_done and tier == "review":
    # commit 候補セクションに注記を追加
    # ⚠️ rule_candidate_scan.py 未実行（推奨: Codex 前に実行）
```

---

## 8. S_CLASS ガード

`scripts/rule_candidate_scan.py` は S_CLASS 疑いの文字列を検出した場合、レポートの冒頭に警告セクションを出力する。

```
## ⚠️ S_CLASS疑い文字列（外部送信前に確認必須）

> この文書を外部AI・APIへ送信する前に内容確認が必要です。

- L42: `...S_CLASS に該当する可能性のある記述...`
```

**検出パターン：** `S_CLASS` / `S-CLASS` / `SCLASS`（大文字小文字を問わない）

**外部送信は絶対に行わない。** レポート生成・標準出力への警告表示のみ。

---

## 9. 将来の拡張設計

### フラグ拡張

| フラグ | 機能 | 実装条件 |
|-------|------|---------|
| `--fix-dates` | CAT-04 の日付ゼロ埋めをドラフトに自動適用 | 人間がオプション付き実行で明示的に承認する |
| `--apply-approved` | rule_candidates レポートの ACCEPT 項目を一括適用 | レポートパーサーの実装が必要 |
| `--since <date>` | 指定日以降に生成されたドラフトをバッチスキャン | リリース前の一括チェックに有用 |

### workflow.db との連携（将来）

現時点では `workflow.db` との連携はない。将来的には以下の統合を検討する。

- `codex_sessions` テーブルにスキャン実行ログを追加（`scan_path` 列）
- `articles` テーブルの `status` 遷移に `scan_pending` を追加
- `workflow_events` テーブルにスキャン結果サマリーを記録

**ただし：** workflow.db への書き込みは実装前に `claude_codex_semiauto_workflow_design.md` § 6 の設計との整合確認が必要。

---

## 10. 実行コマンドリファレンス

```bash
# 基本実行（レポート生成）
python3 scripts/rule_candidate_scan.py \
    --draft note_drafts/ai_summary_<slug>_note_version.md

# dry-run（ファイル未生成・標準出力のみ）
python3 scripts/rule_candidate_scan.py \
    --draft note_drafts/ai_summary_<slug>_note_version.md \
    --dry-run

# スラッグ明示（ファイル名から推定できない場合）
python3 scripts/rule_candidate_scan.py \
    --draft note_drafts/ai_summary_<slug>_note_version.md \
    --slug DOW-UAP-PR051

# 出力先を明示
python3 scripts/rule_candidate_scan.py \
    --draft note_drafts/ai_summary_<slug>_note_version.md \
    --output review_reports/rule_candidates_custom_<slug>.md
```

**出力先：** `review_reports/rule_candidates_YYYYMMDD_<slug>.md`  
**Git 管理：** `review_reports/` は Git 管理外（`.gitignore` 推奨 or COMMIT_EXCLUDE_PATTERNS で除外済み）

---

## 11. バージョン履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| v1.0 | 2026-06-18 | 初版。CAT-01/02/04/05 実装。文書化。 |
