# Codex Review #091-#100

総合: WARN

PASS: #091 #092

BLOCK: なし

WARN:

W-TERM:
#093
軍事略語補足: MISREP/GENTEXT/FMV の補足表現を標準表記に寄せる。

W-OCR-SRC:
#094 #095 #096 #097 #098 #099 #100
OCR不可: 「ファイル名以外の情報源がない」としつつ war.gov説明文を使っており、表現が矛盾する。

UNVERIFIABLE:

U-PDF:
#093
PDF本文OCR未実施・フォームフィールド未検証のため、GENTEXT以外は限定記事として扱う。

source_registry整合性:
PASS: #091-#100 は draft、Source URLあり、Draft Pathあり、published扱いなし。

note投稿形式リスク:
PASS: Markdown table / 引用ブロック / Codex注釈ブロック / コードフェンス / 複雑ネストなし。

最優先修正:
- #094-#100: 「ファイル名以外の情報源がない」を「ファイル名およびwar.gov説明文以外では確認できない」等に修正。
- #093: MISREPを「軍の任務報告書」、GENTEXTを「自由記述欄」など標準補足へ統一。
- #093: PDF全体を確認できていない限定性を維持。
