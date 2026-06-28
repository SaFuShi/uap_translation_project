---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 5
WARN: 3
UNVERIFIABLE: 0
PASS: 6
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-1 BLOCK Release Date / Release 表記が metadata/files_catalog.csv と不一致。ドラフトは「2026年05月22日・Release 02」だが、カタログは release_date=6/12/26 の Release 03 相当。
P1-1B BLOCK Incident Date が metadata/files_catalog.csv と不一致。ドラフトは「2025年・具体的な月不明」だが、カタログは「July, 2025」。
P1-1C BLOCK Source URL が WAR.GOV トップページのまま。チェックリスト上、対象資料の直接URLではなくトップページURLは BLOCK。
P1-2 BLOCK 映像メタデータのフレームレートが不一致。ドラフトは「30fps」だが、metadata.json / ffprobe は 24fps。
P1-5 WARN source_registry.csv 未登録のため article_id 付番・status・重複管理との整合確認が未完了。
P2-1 WARN 記事構成に「注意点」「免責」相当の独立セクションがなく、標準順序「メタデータ → 要点 → AI読解 → 注意点 → 出典 → 免責」から外れている。
P2-1B WARN note転記作業用の削除指示行が本文内に残っている。
P2-1C PASS 要点は3項目で、番号付き太字形式になっている。
P2-2 PASS DVIDS は初出で「国防映像情報配信サービス」と補足されている。
P2-3 PASS 「オーブ目撃」「赤い光帯の正体」等は「とされる」「確認できません」等の留保付きで、正体断定は避けられている。
P2-4 PASS 換算対象となる高度・速度・距離などの原文単位は本文中に確認されない。
P2-5 PASS OCRログ・生英文の大量貼り付けは確認されない。
IMG-1 PASS 視覚観察情報とファイル名・メタデータ由来情報を分ける方針が明記されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | 公開前に source_registry へ登録し、article_id・status・重複確認を完了する。
W-02: 記事構成 | 「注意点」「免責」相当の独立セクションがない | 標準順序に合わせ、注意点と免責を独立セクションとして追加する。
W-03: 転記用メモ | 「→ 使用ファイル：...（note転記後にこの行を削除）」 | note公開本文から削除する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---