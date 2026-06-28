# ルール候補レポート: CIA-UAP-D001_intelligence_information_report_ussr_1973

**生成日時:** 2026-06-18 16:01
**スクリプト:** scripts/rule_candidate_scan.py v1.1.0
**対象ドラフト:** note_drafts/ai_summary_CIA-UAP-D001_intelligence_information_report_ussr_1973_note_version.md
**参照ルールファイル:** docs/draft_rules_v2.md
**検出合計:** 2件（CAT-01: 1 / CAT-02: 0 / CAT-04: 1 / CAT-05: 0）

> ⚠️ すべての検出は **CANDIDATE（候補）** です。断定ではありません。
> 各項目を人間が確認し、承認欄に記入してください。

---

## 検出サマリー

| カテゴリ | 件数 | 既存ルール |
|---------|-----|----------|
| CAT-01 組織名・略称補足 | 1 | Rule 7 |
| CAT-02 禁止表現 | 0 | Rule 4 / Rule 8 |
| CAT-04 日付ゼロ埋め | 1 | 未定義（新規候補） |
| CAT-05 note禁止フォーマット | 0 | Rule 5 |

---

## CAT-01 組織名・略称の初出補足候補

> 初出または近傍に日本語補足（）が確認できない組織名・略称を検出します。出典参照（ファイル名より等）のみの場合も候補として出力します。

### [CANDIDATE #1] L180: `AARO`

- **カテゴリ:** CAT-01 組織名・略称の初出補足候補
- **該当箇所:** `本記事はAAROおよびwar.govが公開した米政府の公式資料を、Claude Code・ChatGPT・CodexおよびローカルAI処理環境を用いて翻訳・要約したものです。UAP（未確認異常現象）の正体・起源についての断定は含みません。A`
- **既存ルール:** Rule 7（略語・組織名の注釈）
- **推奨対応:** →「AARO（全領域異常解決局／米国防総省のUAP調査組織）」
- **補足:** 初出または近傍に日本語補足（）が確認できません。

```
承認: [ ] ACCEPT  [ ] REJECT  [ ] RULE_UPDATE  [ ] NEW_RULE
理由: 
```

---

## CAT-02 禁止表現候補

> Rule 8-6（元映像禁止）・Rule 4（画像・VID記事の断定表現）・Rule 3（AARO評価の断定化）の対象表現を検出します。文体チェック（丁寧体）は将来 CAT-06 で管理予定。

（検出なし）

---

## CAT-04 日付ゼロ埋め候補

> YYYY年M月D日形式（月または日がゼロ埋めなし）を検出します。Rule未定義・新規追加候補。

### [CANDIDATE #2] L9: `2026年5月22日`

- **カテゴリ:** CAT-04 日付ゼロ埋め候補
- **該当箇所:** `- Release Date：2026年5月22日（機密解除・war.gov/UFO にて公開）`
- **既存ルール:** Rule（未定義・新規候補）
- **推奨対応:** →「2026年05月22日」（月 5 → 05）
- **補足:** DOE-UAP-D001 B-01相当。YYYY年MM月DD日形式が推奨。

```
承認: [ ] ACCEPT  [ ] REJECT  [ ] RULE_UPDATE  [ ] NEW_RULE
理由: 
```

---

## CAT-05 note禁止フォーマット候補

> Markdown table・引用ブロック・コードブロックを検出します（Rule 5）。

（検出なし）

---

## 新規ルール追加候補（docs/draft_rules_v2.md 未定義）

- **日付ゼロ埋め強制**（1件検出）: YYYY年MM月DD日形式を Rule 7 または新 Rule 9 として追加を検討

---

## 承認後の作業フロー

1. **ACCEPT** → ドラフトを直接修正（このスクリプトは修正しない）
2. **RULE_UPDATE** → `docs/draft_rules_v2.md` の該当箇所へ人間が追記
3. **NEW_RULE** → `docs/draft_rules_v2.md` に新セクションとして人間が追加
4. **REJECT** → 誤検知理由を「理由:」欄に記録（次回パターン改善に使用）
5. 修正完了後 → Codex監査を実行
