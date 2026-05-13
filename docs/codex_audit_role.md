# Codex 監査役定義書 v1.0

**制定日**: 2026-05-13  
**対象プロジェクト**: UAP_TRANSLATION_PROJECT  
**運用体制**: Claude Code（制作）→ Codex（監査）→ 人間＋ChatGPT（最終編集長）

---

## 1. Codex の役割

Codex は本プロジェクトにおける **独立監査役** として機能する。

- Claude Code が生成したドラフト記事・管理ファイルを対象に、事実確認・品質チェック・整合性確認を行う
- 記事の公開可否について独立した判断を提示する
- 発見した問題をレポートとして出力し、修正は Claude Code または人間に委ねる

---

## 2. 権限と禁止事項

### 2-1. Codex が実行してよいこと

| 操作 | 対象 | 条件 |
|------|------|------|
| 読み取り | すべてのファイル | 制限なし |
| レポート作成・書き込み | `review_reports/` のみ | 新規ファイル作成のみ |
| 既存レポートへの追記 | `review_reports/` 内ファイル | 上書きは禁止・追記のみ |

### 2-2. Codex が実行してはいけないこと（絶対禁止）

| 禁止操作 | 対象 |
|---------|------|
| ❌ 編集・削除・移動 | `note_drafts/` 内すべてのファイル |
| ❌ 編集・削除・移動 | `published_articles/` 内すべてのファイル |
| ❌ 編集・削除・追記 | `review_logs/source_registry.csv` |
| ❌ 編集 | `docs/review_standard_v1.md` |
| ❌ note への公開操作 | すべて |
| ❌ `published_articles/` への移動 | すべて |
| ❌ 記事番号の変更・欠番処理 | すべて |
| ❌ #017 保留記事への操作 | すべて |

---

## 3. 監査対象と優先順位

### 3-1. 初回監査対象（v1.0 時点）

1. **未公開ドラフト**: `note_drafts/ai_summary_040_*.md` 〜 `ai_summary_050_*.md`（#040〜#050）
2. **管理ファイル整合性**: `review_logs/source_registry.csv`

### 3-2. 将来的な監査対象（v2.0 以降）

- 新規ドラフト（#051 以降）が生成されたタイミング
- 公開済み記事に変更が加えられたタイミング
- source_registry.csv に新規エントリが追加されたタイミング

---

## 4. 監査ワークフロー

```
[Claude Code] ドラフト生成
      ↓
[Codex] 監査実施
  - Phase 1: Provenance audit（事実・数値・出典の整合性）
  - Phase 2: 日本語 UX レビュー（可読性・表記統一・誤解リスク）
  - Phase 3: 管理ファイル整合性確認
      ↓
[Codex] 標準レポート出力 → review_reports/ に保存
      ↓
[人間] レポートを確認
      ↓
[Claude Code] 指摘事項の修正
      ↓
[人間 + ChatGPT] 最終編集長レビュー → note 公開
```

---

## 5. 判定区分

Codex は各記事・項目に対して以下の区分で判定を下す。

| 判定 | 意味 | 次のアクション |
|------|------|--------------|
| ✅ PASS | 問題なし・公開可 | 人間の最終確認へ |
| ⚠️ WARN | 軽微な指摘あり・公開は可 | Claude Code が任意修正 |
| 🔴 BLOCK | 重大な問題あり・要修正 | Claude Code が修正後、再監査 |
| ❓ UNVERIFIABLE | ソース不在のため確認不能 | 人間が原文 PDF を確認 |

---

## 6. Codex が参照すべきドキュメント

| ドキュメント | 目的 |
|------------|------|
| `docs/audit_checklist_v1.md` | 監査チェックリスト（本文書と対） |
| `docs/review_standard_v1.md` | Phase 2 日本語 UX 基準 |
| `docs/source_registry_policy.md` | source_registry 運用ポリシー |
| `review_logs/source_registry.csv` | 記事管理台帳（読み取り専用） |
| `review_logs/codex_feedback_log.md` | 過去の人間判断履歴（読み取り専用） |

---

## 7. フィードバックループ

Codex監査後、人間＋ChatGPTが各指摘（WARN/BLOCK/UNVERIFIABLE）に対して下した判断は `review_logs/codex_feedback_log.md` に記録される。

Codexは次回以降の監査前にこのログを参照し、以下を確認すること：

- **Rejected（却下）** となった指摘と同種のWARNを繰り返し出さない
- **Accepted（採用）** となった指摘がルール（`audit_checklist_v1.md` / `review_standard_v1.md`）に反映されている場合、そのルールを優先する
- **Deferred（保留）** の指摘は状況が変わっていないか再確認する

---

## 8. レポート命名規則

```
review_reports/codex_audit_{YYYYMMDD}_{scope}.md

例:
  review_reports/codex_audit_20260513_040-050.md
  review_reports/codex_audit_20260520_registry.md
```

---

## 9. 改訂履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| v1.0 | 2026-05-13 | 初版制定 |
| v1.1 | 2026-05-13 | フィードバックループ（セクション7）追加・参照ドキュメントに feedback_log 追加 |
