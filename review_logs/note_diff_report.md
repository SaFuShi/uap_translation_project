# note公開版 差分レポート

このファイルは `scripts/fetch_published_note_article.py` によって自動更新されます。

## 差分カテゴリの説明

| カテゴリ | 説明 |
|---|---|
| UIアーティファクト | note.com の著者ヘッダー・ハッシュタグ・いいね/チップUI等 |
| Markdownフォーマット差異 | 空行・URLリンク化・リスト整形等（内容は同一） |
| **実質的な内容差異** | **実際の本文変更（Git版に反映が必要な可能性あり）** |


---

## 2026-05-12 13:14 — 記事 #015

| 項目 | 内容 |
|---|---|
| URL | https://note.com/deft_ibis3303/n/nd447cee0001c |
| ステータス | **SUCCESS** |
| 取得タイトル | INDOPACOM域内で報告された12秒・23秒のUAP観測──2025年4月【AI概要版 #015】 |
| 抽出方式 | article_tag + v2 post-process |
| 文字数（クリーン後） | 2255 文字 |
| 行数（クリーン後） | 95 行 |
| 保存先 | `published_articles/from_note/015.md` |
| Git版 | `published_articles/ai_summary_015_d50_indopacom_email_note_version.md` |

### 差分サマリー

| カテゴリ | +行 / -行 | 備考 |
|---|---|---|
| 全体差分（生） | +29 / -11 | note取得(クリーン後) vs Git版 |
| 全体差分（正規化後） | +9 / -1 | フォーマット差異除去後 |
| UIアーティファクト | 0 行 | 著者ヘッダー・ハッシュタグ等 |
| Markdownフォーマット差異 | 8 行 | 空行・URLリンク化等 |
| **実質的な内容差異** | **2 行** | Git版との本文差分 |

> ⚠️ **判定: 実質的な内容差異あり（要確認: 2行）**

#### 実質的な内容差異

```diff
-# INDOPACOM域内で2日連続して確認された短時間UAP観測──2025年4月【AI概要版 #015】
+# INDOPACOM域内で報告された12秒・23秒のUAP観測──2025年4月【AI概要版 #015】
```

<details><summary>Markdownフォーマット差異（8行）</summary>

```diff
+
+
+
+
+
+
+
+
```
</details>

<details><summary>全差分 unified diff（デバッグ用）</summary>

```diff
--- git:ai_summary_015_d50_indopacom_email_note_version.md
+++ note:015.md
@@ -1,4 +1,4 @@
-# INDOPACOM域内で2日連続して確認された短時間UAP観測──2025年4月【AI概要版 #015】
+# INDOPACOM域内で報告された12秒・23秒のUAP観測──2025年4月【AI概要版 #015】
 
 この文書は、機密解除されたメールのやり取りです。UAP目撃情報の非機密ティアライン（公開可能サマリー）の記述が「UNCLASSIFIED（非機密）」レベルであることを確認した手続き記録です。目撃の詳細報告書そのものではありません。
 
@@ -6,13 +6,26 @@
 
 ## 文書メタデータ
 
-- **File Name：** dow-uap-d50-email-correspondence-indopacom-april-2025.pdf
-- **Agency：** Department of War（米国防総省系公開資料）
-- **Release Date：** 2026年5月8日
-- **Incident Date：** 2025年4月10〜11日
-- **Incident Location：** INDOPACOM AOR（インド太平洋軍担当地域）
-- **File Type：** PDF 2ページ・内部メール（SECRET//NOFORN、機密解除済み）
-- **Source URL：** https://www.war.gov/UFO/
+-
+**File Name：** dow-uap-d50-email-correspondence-indopacom-april-2025.pdf
+
+-
+**Agency：** Department of War（米国防総省系公開資料）
+
+-
+**Release Date：** 2026年5月8日
+
+-
+**Incident Date：** 2025年4月10〜11日
+
+-
+**Incident Location：** INDOPACOM AOR（インド太平洋軍担当地域）
+
+-
+**File Type：** PDF 2ページ・内部メール（SECRET//NOFORN、機密解除済み）
+
+-
+**Source URL：** [https://www.war.gov/UFO/](https://www.war.gov/UFO/)
 
 ---
 
@@ -61,9 +74,14 @@
 
 ## 出典
 
-- WAR.GOV：https://www.war.gov/UFO/
-- 元PDF：https://www.war.gov/medialink/ufo/release_1/dow-uap-d50-email-correspondence-indopacom-april-2025.pdf
-- 元PDFファイル名：dow-uap-d50-email-correspondence-indopacom-april-2025.pdf
+-
+[WAR.GOV](http://WAR.GOV)：[https://www.war.gov/UFO/](https://www.war.gov/UFO/)
+
+-
+元PDF：[https://www.war.gov/medialink/ufo/release_1/dow-uap-d50-email-correspondence-indopacom-april-2025.pdf](https://www.war.gov/medialink/ufo/release_1/dow-uap-d50-email-correspondence-indopacom-april-2025.pdf)
+
+-
+元PDFファイル名：dow-uap-d50-email-correspondence-indopacom-april-2025.pdf
 
 ---
 

```
</details>
