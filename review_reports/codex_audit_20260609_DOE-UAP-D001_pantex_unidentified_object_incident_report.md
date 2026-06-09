---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK_COUNT: 2
WARN_COUNT: 2
PASS_COUNT: 10
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・複雑なネスト箇条書き・Codex注釈ブロックは検出されない。
P1-1-FILE BLOCK review_logs/source_registry.csv に DOE-UAP-D001_PANTEX_Image.pdf の該当行がなく、登録PDF名との一致を確認できない。
P1-1-SOURCE BLOCK 文書メタデータの Source URL が直接PDF URLではなく https://www.war.gov/UFO/ になっている。
P1-1-DATE WARN Release Date が YYYY年MM月DD日 形式ではなく、月がゼロ埋めされていない。
P1-1-INCIDENT PASS Incident Date / Incident Location は不明として扱われ、本文との矛盾はない。
P1-2 PASS 速度・高度・単位換算・Zulu時刻などの数値整合性リスクは該当なし。
P1-3 PASS UCNI・CNS・Sandia National Labs など主要な組織名・略語は本文内で補足されている。
P1-5 WARN source_registry に対象PDF行がないため、status・SHA256重複・公開済み重複のレジストリ照合が完了できない。
P2-1 PASS 構成、3項目の要点、限定情報記事の冒頭警告、元PDF URL・元PDFファイル名の出典記載は満たしている。
P2-2 PASS 本文で使用される専門用語は読者向け補足があり、未説明の軍事略語混入は目立たない。
P2-3 PASS 推測・解釈と確認事実は概ね分離され、画像内容の断定も避けられている。
P2-4 PASS 日本向け換算が必要な数値単位は実質的に登場しない。
P2-5 PASS OCRログや生英文の大量貼付、直訳臭、note投稿互換上の禁止形式は検出されない。
IMG-1 PASS 視覚観察と解釈は分離され、「形状・大きさ・物体の性質」を断定しない留保がある。
LIMITED-1 PASS 限定情報記事として冒頭警告があり、AI解析メモに残存テキスト文字数が記録されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | Release Date：2026年5月22日（war.gov/UFO/ にて公開） | Release Date：2026年05月22日（war.gov/UFO/ にて公開）
W-02: source_registry整合性 | review_logs/source_registry.csv に対象PDF行なし | 対象PDFの registry 登録後に status・SHA256・draft_path を照合する
---WARN_DETAILS_END---
---CODEX_AUDIT_END---
