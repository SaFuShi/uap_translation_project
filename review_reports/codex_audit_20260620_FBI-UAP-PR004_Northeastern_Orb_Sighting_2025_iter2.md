---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 3
UNVERIFIABLE: 0
PASS: 16
MODEL: gpt-5-codex
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長い英文引用・2階層以上のネスト箇条書き・Codex注釈ブロックは確認されない。
P1-1A PASS File Name・Agency・Release Date・Incident Date・Related Location・DVIDS ID は metadata/files_catalog.csv と整合している。
P1-1B BLOCK WAR.GOV URL が https://www.war.gov/UFO/ のトップページ表記のままで、対象資料の直接参照要件を満たさない。
P1-1C PASS Release Date は YYYY年MM月DD日 形式で記述され、Incident Date と本文記述の矛盾は確認されない。
P1-2A PASS 動画長49.4秒、720×1280、24fps、H.264、AAC音声あり、動画ストリームビットレート約4,090kbpsは ffprobe と整合する。
P1-2B PASS FL・速度・高度・Zulu時刻などの数値換算対象は本文中に確認されない。
P1-3 PASS FBI と DVIDS は読者向け補足があり、未説明の主要軍事略語混入は確認されない。
P1-4 PASS Misrep・MDR・JSIR・CSP/MRO等の番号類は本文に登場しない。
P1-5 WARN source_registry.csv 未登録のため、article_id 付番・status・重複管理との整合確認が未完了。
P2-1A WARN 標準構成のうち「注意点」「免責」相当の独立セクションがない。
P2-1B PASS 「この資料の要点」は3項目で、番号付き太字形式になっている。
P2-1C PASS 出典セクションに WAR.GOV、DVIDS ID、DVIDS URL、元ファイル名、代表フレームが記載されている。
P2-2 PASS DVIDS は初出で「国防映像情報配信サービス」と補足されている。
P2-3 PASS 「とされています」「確認できません」「断定しません」等の留保があり、正体・種別・行動意図の断定は避けられている。
P2-4 PASS 日本向け換算が必要なフィート・ノット等の単位記述は本文に出ていない。
P2-5A PASS OCRログ・生英文大量貼付・直訳臭・note投稿互換上の禁止形式は確認されない。
P2-5B WARN タイトル冒頭が「FBI FBI-UAP-PR004」となっており、機関名が重複している。
P2-5C PASS note転記作業用の削除指示行は確認されない。
IMG-1 PASS 視覚観察情報とファイル名・メタデータ由来情報を分ける方針が明記されている。
IMG-2 PASS 代表フレーム上の夜空、樹木シルエット、赤い水平光帯2本、ブレの記述は視覚情報と概ね整合する。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | 公開前に source_registry へ登録し、article_id・status・重複確認を完了する。
W-02: 記事構成 | 「注意点」「免責」相当の独立セクションがない | 標準順序に合わせ、注意点と免責を独立セクションとして追加する。
W-03: タイトル | 「FBI FBI-UAP-PR004」 | 機関名重複を避け、「FBI-UAP-PR004」または「FBI：UAP-PR004」に整理する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---