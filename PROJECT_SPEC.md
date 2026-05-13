# UAP公開文書 翻訳・要約プロジェクト 仕様書

## 目的

米政府・国防総省などが公式公開したUAP関連資料を、
AIを使って効率よく日本語化・要約し、
note等へ転記可能な形に整える。

## 基本方針

- 対象はまずPDFのみ
- 動画・画像単体・音声は後回し
- raw_pdf 内の元PDFファイル名は変更しない
- 処理単位は「PDF単位」ではなく「ページ単位」
- 判読不能なページは無理に翻訳せず、判読不能として記録する
- 事実・推測・補足解説を分ける
- 出典URLを必ず残す
- 最終公開判断は人間が行う

## 処理フロー

1. WAR.GOV/UFO から一覧メタデータを取得
2. PDFファイルだけを抽出
3. PDFを raw_pdf に保存
4. PDFをページ画像化
5. ページごとに分類
6. 読めるページをOCR
7. 英文テキストを日本語訳
8. 翻訳をダブルチェック
9. 補足注釈を作成
10. 要約を作成
11. note等へ転記可能な形式に整形

## ページ分類

- typed_report: タイプされた報告書
- handwritten_note: 手書きメモ
- newspaper_clipping: 新聞・雑誌切り抜き
- mixed_annotation: タイプ文書＋手書き注釈・スタンプ
- receipt_or_misc: レシート等の雑多資料
- cover_or_admin_sheet: 表紙・管理票
- photo_or_visual: 写真・図版中心
- unreadable: 判読不能

## フォルダ構成

UAP_TRANSLATION_PROJECT/
├── raw_pdf/
├── page_images/
├── thumbnails/
├── extracted_text/
├── translated/
├── summaries/
├── note_drafts/
├── review_logs/
├── metadata/
├── classification/
└── prompts/

## 人間が担当すること

- 公開判断
- 翻訳結果の最終確認
- 補足解説の妥当性確認
- note等への投稿
- 陰謀論的表現になっていないかの確認

## AIに任せたいこと

- PDF一覧整理
- ページ画像化
- ページ分類
- OCR
- 一次翻訳
- 翻訳チェック
- 要約作成
- note下書き生成

## 三層運用体制（2026-05-13 以降）

### 役割分担

| 役割 | 担当 | 主な責務 |
|------|------|---------|
| **制作** | Claude Code | ドラフト生成・Phase 1/2 自己レビュー・修正 |
| **監査** | Codex | 独立監査・レポート出力（`review_reports/` に保存） |
| **編集長** | 人間 ＋ ChatGPT | 最終確認・note 公開判断 |

### Codex の操作権限

- ✅ 読み取り: すべてのファイル
- ✅ 書き込み: `review_reports/` のみ
- ❌ 編集禁止: `note_drafts/`, `published_articles/`, `review_logs/source_registry.csv`

詳細は `docs/codex_audit_role.md` および `docs/audit_checklist_v1.md` を参照。

### 公開フロー（三層）

```
[Claude Code] ドラフト生成 → Phase 1/2 自己レビュー
      ↓
[Codex] 独立監査 → review_reports/ にレポート出力
      ↓
[人間 + ChatGPT] レポート確認 → 各指摘を Accepted/Rejected/Deferred で判断
      ↓
[人間] 判断結果を review_logs/codex_feedback_log.md に記録
      ↓
[人間 + ChatGPT] 最終編集長レビュー → note 公開
```

Codex監査結果に対する人間判断は `review_logs/codex_feedback_log.md` に蓄積し、同じWARNが繰り返されないよう監査精度のチューニングに利用する。詳細は `docs/codex_audit_role.md` セクション7を参照。

---

## 次の実装候補

最初に自動化する対象は以下。

1. PDFをページ画像へ変換
2. ページ画像を分類
3. OCRテキストを生成
4. translation.md の下書きを自動生成
