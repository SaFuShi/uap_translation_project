---CODEX_AUDIT_START---
VERDICT: BLOCK
BLOCK: 1
WARN: 5
UNVERIFIABLE: 1
PASS: 7
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown table・引用ブロック・長文英文引用・2階層以上ネスト箇条書き・Codex注釈ブロックは確認されない。
P1-1 BLOCK files_catalog.csv では release_date が 6/12/26、incident_date が March, 2022 だが、本文は Release Date を 2026年05月22日、Incident Date を 2022年・月日不明としており一次メタデータと矛盾する。
P1-2 WARN ffprobe/metadata.json ではフレームレート 24fps、ビットレート約7,044kbpsだが、本文は30fps、6,944kbpsとしており技術メタデータに不一致がある。
P1-3 PASS FBI、DVIDS等の組織・略語は初出付近で読者向け補足がある。
P1-5 UNVERIFIABLE source_registry.csv に対象ファイルの登録が確認できず、BLOCK状態・重複・article_id整合性を検証できない。
P2-1 WARN 構成上、独立した「注意点」および「免責」セクションがなく、AI解析メモも出典前に置かれている。
P2-2 PASS 軍事略語・専門用語の未補足による重大な読解阻害は確認されない。
P2-3 WARN 「Release 02の中で最も明確な単一光源の一つ」は比較根拠が本文中で確認できず、評価表現として強い。
P2-4 PASS 換算対象となる速度・高度・距離等の単位は本文中に確認されない。
P2-5 WARN タイトル冒頭の「FBI FBI-UAP-PR002」は重複表記で、本文中に「note転記後にこの行を削除」という作業メモが残っている。
P2-6 PASS 日本語読者向けの組織名・地域名補足は概ね維持されている。
IMG-1 WARN 代表フレーム上の赤い光点は画面中央付近からやや右寄りに見え、「中央左付近」という位置表現は視覚確認とずれる可能性がある。
IMG-2 PASS 回転・移動・追跡・消失等の動きは確定事実として断定されていない。
SRC-1 PASS DVIDS ID 1010264 と DVIDS直接URLは本文・出典に記載されている。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: 映像メタデータ | 「フレームレート：30fps」「ビットレート：6,944 kbps」 | ffprobe/metadata.json に合わせて「フレームレート：24fps」「ビットレート：約7,044 kbps」に修正する。
W-02: 記事構成 | 独立した「注意点」「免責」セクションがない | 注意点と免責を出典前後の所定位置に分け、AI解析メモの位置も所定構成に合わせる。
W-03: 客観性 | 「Release 02の中で最も明確な単一光源の一つ」 | 比較根拠がなければ「明確な単一光源が確認できる」に弱める。
W-04: 読みやすさ | 「FBI FBI-UAP-PR002」「note転記後にこの行を削除」 | タイトル重複を解消し、作業メモ行は公開本文から削除する。
W-05: 視覚観察 | 「中央左付近に明確な赤い光球」 | 代表フレームに合わせて「画面中央付近からやや右寄り」などに修正する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---