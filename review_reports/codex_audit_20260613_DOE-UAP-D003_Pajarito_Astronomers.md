---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK_COUNT: 0
WARN_COUNT: 5
PASS_COUNT: 15
MODEL: GPT-5 Codex
---ITEMS_START---
P0-1 PASS Markdown table、引用ブロック、Codex注釈ブロック、複雑なネスト箇条書きは確認されない。英文抜粋は通常テキストで記載されている。
P1-1 WARN File Name と Download URL は対象PDFを指しており主要メタデータも画像と整合するが、文書メタデータに WAR.GOV 公開ページURLが併記されているため、Source URL直接URL化ルール上は誤用リスクが残る。
P1-2 PASS 日付・時刻は本文、OCR補正全文、画像の範囲で一貫しており、単位換算対象の高度・速度等はない。
P1-3 PASS DOE、LANL、AT-6、MS等は記事文脈上必要な範囲で説明され、PDF外の推定は外部背景情報として分離されている。
P1-4 PASS Misrep、MDR、JSIR、CSP/MRO等の番号類は本記事に該当しない。
P1-5 WARN source_registry.csv内の対象エントリをローカル検索で確認できず、重複状態・登録状態の完全検証はできなかった。
P2-1 PASS 構成はメタデータ、要点、AI読解、注意点、出典、免責の順で、要点3項目、冒頭警告、元PDF URL、ファイル名を備えている。
P2-2 PASS 軍事略語中心の記事ではなく、AT-6、MS、LANL等は本文または外部背景情報で説明されている。
P2-3-FACT PASS PDF本文・画像から確認できる講演日時、場所、講演者名、タイトルと、LANL・Club 1663・Fuller Lodge・MSコード等の外部背景情報は「【外部背景情報（PDF外）】」で明確に分離されている。
P2-3-UFO WARN タイトルと要訳に原文タイトル由来の「UFO」は含まれるが、本文全体では講演案内の位置付けを維持しており、UFO研究・研究者等の煽り見出しはない。
P2-3-MISLEAD PASS 「ロスアラモスの科学者がUFO研究を行った」「LANLがUFOを研究した」と読める断定は残っておらず、注意点で研究活動を示す文書ではないと明記している。
P2-3-LIMIT PASS 講演が実際に行われたか、内容・結論が不明である旨は冒頭警告、要点2、注意点で反復明示されている。
P2-4 PASS 換算対象となる数値・単位はなく、日時・住所・メールストップ等は原文に沿って記載されている。
P2-5 WARN OCR補正全文として英文本文をほぼ全文掲載しており、1ページ短文のため可読性崩壊は小さいが、チェックリストの「長い英文引用（目安200字超）」に抵触する可能性がある。
P2-6 PASS 日本語読者向けにDOE、LANL、Fuller Lodge、Club 1663、AT-6、MSの意味や限定性が補足されている。
DOC-SPEC-1 PASS 本記事は一貫して「1ページの講演案内文書」として扱われ、講演内容や組織的研究活動へ踏み込んでいない。
DOC-SPEC-2 PASS OCR補正の主要箇所である「Pajarito Astronomers」、日時、場所、講演者、AT-6、講演タイトルはページ画像と矛盾しない。
DOC-SPEC-3 PASS 右上手書きアノテーションは「文書管理番号風」「等」「みられる」と留保され、内部的意味は不明と明記されている。
DOC-SPEC-4 PASS タイトルは「講演案内」を中心に据えており、「UFO研究」「研究者」など研究実施を示唆する見出し語は含まれていない。
P3 WARN source_registry.csv内の対象エントリを確認できず、article_id、status、重複状態、raw_pdf実在性のCSV整合性を完全には検証できなかった。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 文書メタデータ | WAR.GOV（公開ページ）：https://www.war.gov/UFO/ | Source URL欄として扱われる可能性を避けるため、「公開ページ（参考）」などに限定し、主要ソースはDownload URLの直接PDFに一本化する
W-02: source_registry整合性 | source_registry.csv内の対象エントリを確認できず | source_registry.csvへ対象PDFの登録状態、status、SHA256、重複有無が記録されているか確認する
W-03: タイトル・要訳 | ロスアラモス天文クラブへの講演案内──「科学者はなぜUFOを気にすべきか？」／講演タイトルは「科学者はなぜUFOを気にすべきなのか？」です。 | 原文タイトルの引用であることをさらに明示し、必要なら日本語タイトル側は「原題にUFOを含む講演案内」程度に留める
W-04: AI読解 | Our next meeting will be Thursday... See you there. までのOCR補正済み英文全文 | note投稿互換を優先する場合は全文掲載をやめ、画像で確認できる主要項目と短い原文抜粋のみに圧縮する
W-05: Phase 3 | source_registry.csv内の対象エントリを確認できず、article_id、status、重複状態、raw_pdf実在性のCSV整合性を完全には検証できなかった。 | レジストリ側でDOE-UAP-D003_Pajarito_Astronomers.pdfの登録とハッシュ照合結果を確認する
---WARN_DETAILS_END---
---CODEX_AUDIT_END---