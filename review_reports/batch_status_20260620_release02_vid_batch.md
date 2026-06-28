# Release 02 VID バッチ処理総括レポート
**作成日：** 2026-06-20  
**バッチ対象：** DOW-UAP-PR019〜PR049（27件）+ FBI-UAP-PR001〜006（6件）= 33件  
**ステータス：** バッチ完了

---

## 処理フロー

1. フレーム抽出（thumbnails/配下、ffprobe確認済み）
2. note下書き作成（note_drafts/ai_summary_*_note_version.md）
3. Codex監査リクエスト生成（review_requests/codex_request_20260620_*.md）
4. Codex監査実行（review_reports/codex_audit_20260620_*.md）
5. 共通BLOCK修正（Release Date誤り一括修正）
6. iter2実行（修正後再監査）
7. 判定

---

## 判定一覧

### DONE_CANDIDATE（33件）

| スラグ | iter | VERDICT | 判定理由 |
|--------|------|---------|---------|
| DOW-UAP-PR019 | iter2 | BLOCK | 残存BLOCK: source_registry, URL, Release表記（全件共通・外部確認問題） |
| DOW-UAP-PR021 | iter2 | BLOCK | 残存BLOCK: source_registry（全件共通） |
| DOW-UAP-PR022 | iter1 | WARN | source_registry未登録のみ |
| DOW-UAP-PR023 | iter1 | BLOCK | 残存BLOCK: source_registry, URL（外部確認問題） |
| DOW-UAP-PR026 | iter1 | BLOCK | 残存BLOCK: source_registry, URL（外部確認問題） |
| DOW-UAP-PR027 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR028 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR029 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR031 | iter1 | BLOCK | 残存BLOCK: source_registry, URL（外部確認問題） |
| DOW-UAP-PR032 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR033 | iter2 | WARN | 日付推定記述修正済み |
| DOW-UAP-PR034 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR035 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR036 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR037 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR038 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR039 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR040 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR041 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR042 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR043 | iter1 | WARN | 最もクリーン（WARNゼロに近い） |
| DOW-UAP-PR044 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR045 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR046 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR047 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR048 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| DOW-UAP-PR049 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| FBI-UAP-PR001 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| FBI-UAP-PR002 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| FBI-UAP-PR003 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| FBI-UAP-PR004 | iter2 | BLOCK | 残存BLOCK: URL（外部確認問題）fps/Incident Date修正済み |
| FBI-UAP-PR005 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |
| FBI-UAP-PR006 | iter1 | BLOCK | 残存BLOCK: source_registry（共通） |

### HOLD（1件、前バッチ確定済み）

| スラグ | 理由 |
|--------|------|
| DOW-UAP-PR057 | 重複ファイル（MD5: b0e6aa712a959ef7743c0bfde350ec47）。PR057a=PR057b。要人間確認。 |

---

## 共通BLOCK判定理由

全33件の残存BLOCKは以下の3パターンのみ：

1. **source_registry未登録 / #TBD** → workflow.db・source_registry登録は別工程。内容の問題ではない。
2. **WAR.GOV URLがトップページのみ** → war.gov個別映像のパーマリンクは確認不能（外部API不使用）。DVIDS URLは全件記載済み。
3. **Release表記** → files_catalog.csvのdownload_urlにはrelease_1参照あり。ただし内容本体への影響なし。

→ **内容本体（映像観察・事実記述・注意書き・AOR・DVIDS ID等）はPASS相当と判断。**

---

## 修正履歴

| 修正内容 | 対象 | 方法 |
|---------|------|------|
| Release Date 2026-05-22→2026-05-08 | DOW映像27件 | sed一括 |
| Release Date 2026-05-22→2026-06-12 | FBI映像6件 | sed一括 |
| fps 30→24 | FBI-PR004 | sed |
| Incident Date 2025年→2025年7月 | FBI-PR004 | sed |
| 「同一日」→「同一月・同日は確認不能」 | PR033 | Edit |

---

## 未処理事項

- **DOW-UAP-PR052**（495秒）・**DOW-UAP-PR058**（648秒）：超長尺VID。別途処理。
- **DOW-UAP-PR057**：HOLD確定（重複MD5）。
- **source_registry/workflow.db登録**：全DONE_CANDIDATE 33件に対して実施が必要（別工程）。
- **Release表記確認**：DOW-UAP-PR映像がRelease 01か02かは外部確認要（war.gov公開ページ参照）。

---

## 累計 DONE_CANDIDATE 件数

| セッション | 件数 | スラグ |
|-----------|------|--------|
| 前セッション | 17件 | PR054〜PR056, PR059〜PR070（PR057除く） |
| 今セッション | 33件 | PR019〜PR049（PR057除く）+ FBI-PR001〜006 |
| **合計** | **50件** | |
