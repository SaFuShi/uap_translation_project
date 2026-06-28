# ルール候補レポート: DOW-UAP-D077_Unresolved-Case-Analysis-Update_Western-United-States-Event

**生成日時:** 2026-06-18 20:11
**スクリプト:** scripts/rule_candidate_scan.py v1.2.0
**対象ドラフト:** note_drafts/ai_summary_DOW-UAP-D077_Unresolved-Case-Analysis-Update_Western-United-States-Event_note_version.md
**参照ルールファイル:** docs/draft_rules_v2.md
**検出合計:** 1件（CAT-01: 1 / CAT-02: 0 / CAT-04: 0 / CAT-05: 0）

> ⚠️ すべての検出は **CANDIDATE（候補）** です。断定ではありません。
> 各項目を人間が確認し、承認欄に記入してください。

---

## 検出サマリー

| カテゴリ | 件数 | 既存ルール |
|---------|-----|----------|
| CAT-01 組織名・略称補足 | 1 | Rule 7 |
| CAT-02 禁止表現 | 0 | Rule 4 / Rule 8 |
| CAT-04 日付ゼロ埋め | 0 | 未定義（新規候補） |
| CAT-05 note禁止フォーマット | 0 | Rule 5 |

---

## CAT-01 組織名・略称の初出補足候補

> 初出または近傍に日本語補足（）が確認できない組織名・略称を検出します。出典参照（ファイル名より等）のみの場合も候補として出力します。

### [CANDIDATE #1] L1: `AARO`

- **カテゴリ:** CAT-01 組織名・略称の初出補足候補
- **該当箇所:** `# 「40%が未解決のまま」──AAROが2023年米国西部UAP事案の分析を更新、「未認識技術」仮説を保留に【AI概要版・DOW-UAP-D077】`
- **既存ルール:** Rule 7（略語・組織名の注釈）
- **推奨対応:** →「AARO（全領域異常解決局／米国防総省のUAP調査組織）」
- **補足:** 初出または近傍に日本語補足（）が確認できません。

```
承認: [ ] ACCEPT  [x] REJECT  [ ] RULE_UPDATE  [ ] NEW_RULE
理由: タイトル行（H1）のAAROは補足不要。note公開時タイトルに括弧補足は入れない慣習。
      本文初出（L37）に「AARO（全領域異常解決局／米国防総省のUAP調査組織）」の補足済み。
      → rule_candidate_scan の CAT-01 はタイトル行を除外するよう将来改善候補。
```

---

## CAT-02 禁止表現候補

> Rule 8-6（元映像禁止）・Rule 4（画像・VID記事の断定表現）・Rule 3（AARO評価の断定化）の対象表現を検出します。文体チェック（丁寧体）は将来 CAT-06 で管理予定。

（検出なし）

---

## CAT-04 日付ゼロ埋め候補

> YYYY年M月D日形式（月または日がゼロ埋めなし）を検出します。Rule未定義・新規追加候補。

（検出なし）

---

## CAT-05 note禁止フォーマット候補

> Markdown table・引用ブロック・コードブロックを検出します（Rule 5）。

（検出なし）

---

## 新規ルール追加候補（docs/draft_rules_v2.md 未定義）

（今回のドラフトでは新規候補なし）

---

## 承認後の作業フロー

1. **ACCEPT** → ドラフトを直接修正（このスクリプトは修正しない）
2. **RULE_UPDATE** → `docs/draft_rules_v2.md` の該当箇所へ人間が追記
3. **NEW_RULE** → `docs/draft_rules_v2.md` に新セクションとして人間が追加
4. **REJECT** → 誤検知理由を「理由:」欄に記録（次回パターン改善に使用）
5. 修正完了後 → Codex監査を実行
