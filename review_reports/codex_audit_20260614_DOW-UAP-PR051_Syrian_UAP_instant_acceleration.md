---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK_COUNT: 0
WARN_COUNT: 3
PASS_COUNT: 16
MODEL: GPT-5
---ITEMS_START---
P0-1 WARN 長い英文引用が1か所あり、note投稿互換上の本文崩れリスクが残る。Markdown table・引用ブロック・複雑なネスト箇条書き・Codex注釈ブロックはなし。
P1-1 PASS VID記事として、ファイル名・公開日・Incident Date・Locationの由来留保は本文内で明示されている。
P1-2 PASS 数値・単位は動画メタデータ中心で、原値と換算の矛盾は確認されない。
P1-3 PASS 固有名詞・略語のうち、動画記事で必要な範囲の説明は概ね補足されている。
P2-1 PASS 構成はメタデータ、要点、AI読解、注意点、出典、免責の順で概ね整っている。
P2-2 WARN AAROの初出時に「全領域異常解決局／米国防総省のUAP調査組織」の補足がない。
P2-3 PASS 視覚確認事実、ファイル名・メタデータ由来情報、AARO説明文由来情報が分離され、物体の正体・速度・加速度は断定されていない。
P2-5 PASS note投稿互換上の禁止要素（Markdown表、引用ブロック、Codex注釈ブロック、複雑なネスト箇条書き）は確認されない。
VID-1 PASS 映像から視覚的に確認できる情報と、ファイル名・メタデータ由来情報がセクション分離されている。
VID-2 PASS タイトル・本文・メタデータ欄・画像キャプションの「赤外線映像」「IR映像」は推定表現として扱われ、タイトルでの断定はない。
VID-3 PASS 「空中にある」「飛行している」等の空中物体断定は確認されない。
VID-4 PASS 「Syrian」「UAP」「instant acceleration」「シリア地区」「2021年」はファイル名、files_catalog.csv、アップロード者タイトル等の由来が明示されている。
VID-5 PASS AAC音声トラックの技術情報のみで、会話・音響など音声内容への言及はない。
VID-6 PASS タイトルと本文の断定レベルは概ね一致し、本文より強い断定は確認されない。
VID-7 PASS AAROの評価とVideo Description由来のタイムコード付き説明は区別され、「情報提供のみを目的とする」旨も反映されている。
VID-8 PASS 冒頭でデジタル改変済みを独立明示し、速度変更・白縁強調・白黒反転・ズームが改変者による処理であること、画像②が処理版・加工済み抽出であることも明示されている。
VID-9 PASS chain-of-custody不足は冒頭および注意点で明示されている。
VID-10 PASS 「instant acceleration」はuploader-defined titleとして扱われ、AAROの分析判断や実速度・実加速度の断定にはなっていない。
VID-11 WARN AARO説明文の英文が200字を超える形で直接引用されており、P0-1上の長い英文引用リスクがある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: AI読解 / AAROは「This video description is provided for informational purposes only. Readers should not interpret any part of this description as reflecting an analytical judgment, investigative conclusion, or factual determination regarding the described event's validity, nature, or significance.（本映像説明は情報提供のみを目的としており、記述のいかなる部分も、当該事象の妥当性・性質・重要性に関する分析的判断・調査結論・事実認定を反映するものとして解釈してはならない）」と付記しています。 / 英文原文は短く要約し、日本語側で「AAROは、説明文を分析判断・調査結論・事実認定として解釈しないよう付記している」と整理する。
W-02: 冒頭・この資料の要点 / AAROの説明文は / 初出を「AARO（全領域異常解決局／米国防総省のUAP調査組織）の説明文は」に修正する。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---