# Article Revision Candidates

- 生成日時: 2026-06-26 08:47:24
- モデル: `qwen2.5-vl-7b-instruct`
- run_id: `phase3_full50_20260626`
- ground_truth: `data/vlm_eval_set/20260625/ground_truth.csv`
- results: `data/vlm_runs/phase3_full50_20260626/results.csv`

> **注意**: このレポートは記事修正を自動実行しません。
> 人間・Claudeが確認し、必要な場合にのみ note_drafts を手動修正してください。

---

## サマリー

| risk_level | 件数 |
|------------|------|
| HIGH | 6 |
| MEDIUM | 17 |
| LOW | 0 |
| SKIP（VLM誤検出確定等） | 1 |
| **合計** | **24** |

### risk_level の定義

| level | 条件 |
|-------|------|
| HIGH | 人間目視確認済み（label_error）かつ記事と矛盾 |
| MEDIUM | VLM検出あり + 記事にUAP対象NEG表現、または comparison_label に品質課題 |
| LOW | VLM検出あり。NEG表現は二次的側面のみ、または NEG なし |
| SKIP | VLM誤検出確定（false_positive）または条件非該当 |

---

## HIGH — 6件

### vlm_0019 | R02-031 | #2_031

- **category**: C_no_visible_target
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0019_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_frame_0000.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央
- description: 不明瞭な形状の暗い物体、背景との明確な区別は困難。

**人間判定（ground truth）:**

- visible: True / confidence: 0.6
- human_verdict: label_error
- comparison_label: Partial Match / Description Gap

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR044 より抽出（00:00）。グレースケールの映像（IRセンサーと推定されるが確認できません）。**画面中央にタンカーとみられる暗い船舶形状が明確に確認できます**。船舶形状の周囲に拡散した明るいハロー（輝き）が確
- L38 〔二次的〕 `確認できません` : 映像開始直後（00:00付近）のフレームにて、画面中央にタンカーとみられる暗い船舶形状が明確に確認できます。船舶形状の周囲に拡散した明るいハロー（輝き）が確認でき、赤い矢印マーカーが対象を指示しています。この対象の正体は映像フレームのみから
- L41 〔対象候補〕 `確認できません` : 赤い矢印状のマーカーが左中央付近に確認できます。PR036でも類似した赤矢印マーカーが確認されており、同一または類似したシステムによる記録の可能性がありますが確認できません。
- L62 〔二次的〕 `確認できません` : - グレースケールの映像（IRセンサーと推定されるが確認できません）
- L65 〔二次的〕 `確認できません` : - 中央付近に黒い物体状の形状（正体は確認できません）
- … 他 3 件

**修正候補文:**

> 【修正候補】中央付近に対象候補が確認できます。ただし、単一または少数フレームの目視確認であり、対象の性質・移動・正体を断定することはできません。追加フレームおよび専門的分析が必要です。

- **risk_level**: HIGH
- **human_review_required**: True
- **next_action**: 人間目視確認済み。記事内NEG表現と矛盾。note_draftのNEG表現を人間が確認し、必要に応じて慎重表現で修正。

### vlm_0033 | R02-036 | #2_036

- **category**: C_no_visible_target
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0033_DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026_frame_0000.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央
- description: 白い線と点の集合、背景との明確な区別

**人間判定（ground truth）:**

- visible: True / confidence: 0.6
- human_verdict: label_error
- comparison_label: Partial Match

**記事内 NEG 表現:**

- L29 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR049 より抽出（00:10）。夜間のほぼ黒い映像（IRまたは低照度カメラと推定されるが確認できません）。ほぼ黒い背景。**画面右側付近に2つの明るい白い輝点が近接して確認できます**。各輝点の周囲にわずかなハローが
- L63 〔二次的〕 `確認できません` : - 夜間の暗い映像（IRまたは低照度カメラと推定されるが確認できません）
- L65 〔二次的〕 `確認できません` : - **白い飛行体状の物体**が中央に確認できる（翼とみられる構造を持つ形状・正体は確認できません）
- L90 〔二次的〕 `確認できません` : 本映像内でUAPとされる対象物は、映像開始直後（約5秒）に飛行体状の白い物体として、約10〜15秒付近では2つの明るい白い輝点として確認できます。対象の正体・種別は現時点で確認できません。「UAP」「Unresolved」はファイル名に付与
- L99 〔二次的〕 `確認できません` : 撮影したプラットフォーム・機材・乗員の観察記録等は本映像単体では確認できません。コールサインは黒塗りです。
- … 他 1 件

**修正候補文:**

> 【修正候補】中央付近に対象候補が確認できます。ただし、単一または少数フレームの目視確認であり、対象の性質・移動・正体を断定することはできません。追加フレームおよび専門的分析が必要です。

- **risk_level**: HIGH
- **human_review_required**: True
- **next_action**: 人間目視確認済み。記事内NEG表現と矛盾。note_draftのNEG表現を人間が確認し、必要に応じて慎重表現で修正。

### vlm_0045 | R02-040 | #2_040

- **category**: C_no_visible_target
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0045_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_frame_0000.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央上部
- description: 赤い線状の光、背景との明確な区別あり。

**人間判定（ground truth）:**

- visible: True / confidence: 0.9
- human_verdict: label_error
- comparison_label: Match

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR004 より抽出（00:00）。夜間の縦位置映像（可視光カメラ・スマートフォンと推定されるが確認できません）。暗い夜空と樹木（木）のシルエットが確認できます。右上付近に**赤い水平の光の帯**が2本確認できます（赤い
- L38 〔二次的〕 `確認できません` : frame_0000において、暗い夜空と樹木のシルエット、右上付近に赤い水平の光の帯が2本確認できます。この赤い光帯の正体（UAP・航空機の航行灯・地上の光源・その他）は映像フレームのみからは確認できません。
- L62 〔二次的〕 `確認できません` : - 夜間の縦位置映像（可視光カメラと推定されるが確認できません）
- L66 〔対象候補〕 `確認できません` : - 軍用センサーUIマーカーは確認できません
- L87 〔二次的〕 `確認できません` : 本映像内でUAPとされる対象物は、映像約10〜15秒付近のフレームにて赤いオーブ状の光体として確認できます。対象の正体・種別は現時点で確認できません。「UAP」「Unresolved」はファイル名に付与された分類名称であり、物体の性質を示す
- … 他 2 件

**修正候補文:**

> 【修正候補】中央上部付近に対象候補が確認できます。ただし、単一または少数フレームの目視確認であり、対象の性質・移動・正体を断定することはできません。追加フレームおよび専門的分析が必要です。

- **risk_level**: HIGH
- **human_review_required**: True
- **next_action**: 人間目視確認済み。記事内NEG表現と矛盾。note_draftのNEG表現を人間が確認し、必要に応じて慎重表現で修正。

### vlm_0046 | R02-040 | #2_040

- **category**: C_no_visible_target
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0046_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_frame_0005.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや左上
- description: 小さな光点、背景と明確に区別できる

**人間判定（ground truth）:**

- visible: True / confidence: 0.85
- human_verdict: label_error
- comparison_label: Match

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR004 より抽出（00:00）。夜間の縦位置映像（可視光カメラ・スマートフォンと推定されるが確認できません）。暗い夜空と樹木（木）のシルエットが確認できます。右上付近に**赤い水平の光の帯**が2本確認できます（赤い
- L38 〔二次的〕 `確認できません` : frame_0000において、暗い夜空と樹木のシルエット、右上付近に赤い水平の光の帯が2本確認できます。この赤い光帯の正体（UAP・航空機の航行灯・地上の光源・その他）は映像フレームのみからは確認できません。
- L62 〔二次的〕 `確認できません` : - 夜間の縦位置映像（可視光カメラと推定されるが確認できません）
- L66 〔対象候補〕 `確認できません` : - 軍用センサーUIマーカーは確認できません
- L87 〔二次的〕 `確認できません` : 本映像内でUAPとされる対象物は、映像約10〜15秒付近のフレームにて赤いオーブ状の光体として確認できます。対象の正体・種別は現時点で確認できません。「UAP」「Unresolved」はファイル名に付与された分類名称であり、物体の性質を示す
- … 他 2 件

**修正候補文:**

> 【修正候補】中央やや左上付近に対象候補が確認できます。ただし、単一または少数フレームの目視確認であり、対象の性質・移動・正体を断定することはできません。追加フレームおよび専門的分析が必要です。

- **risk_level**: HIGH
- **human_review_required**: True
- **next_action**: 人間目視確認済み。記事内NEG表現と矛盾。note_draftのNEG表現を人間が確認し、必要に応じて慎重表現で修正。

### vlm_0047 | R02-040 | #2_040

- **category**: C_no_visible_target
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0047_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_frame_0010.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや上部
- description: 赤い光点、周囲は暗く、背景との明確な区別

**人間判定（ground truth）:**

- visible: True / confidence: 0.8
- human_verdict: label_error
- comparison_label: Match

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR004 より抽出（00:00）。夜間の縦位置映像（可視光カメラ・スマートフォンと推定されるが確認できません）。暗い夜空と樹木（木）のシルエットが確認できます。右上付近に**赤い水平の光の帯**が2本確認できます（赤い
- L38 〔二次的〕 `確認できません` : frame_0000において、暗い夜空と樹木のシルエット、右上付近に赤い水平の光の帯が2本確認できます。この赤い光帯の正体（UAP・航空機の航行灯・地上の光源・その他）は映像フレームのみからは確認できません。
- L62 〔二次的〕 `確認できません` : - 夜間の縦位置映像（可視光カメラと推定されるが確認できません）
- L66 〔対象候補〕 `確認できません` : - 軍用センサーUIマーカーは確認できません
- L87 〔二次的〕 `確認できません` : 本映像内でUAPとされる対象物は、映像約10〜15秒付近のフレームにて赤いオーブ状の光体として確認できます。対象の正体・種別は現時点で確認できません。「UAP」「Unresolved」はファイル名に付与された分類名称であり、物体の性質を示す
- … 他 2 件

**修正候補文:**

> 【修正候補】中央やや上部付近に対象候補が確認できます。ただし、単一または少数フレームの目視確認であり、対象の性質・移動・正体を断定することはできません。追加フレームおよび専門的分析が必要です。

- **risk_level**: HIGH
- **human_review_required**: True
- **next_action**: 人間目視確認済み。記事内NEG表現と矛盾。note_draftのNEG表現を人間が確認し、必要に応じて慎重表現で修正。

### vlm_0049 | R02-041 | #2_041

- **category**: D_sensor_ui_background
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0049_FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023_frame_0030.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.8
- location: 右上
- description: 黄色い球体、背景に星が見える

**人間判定（ground truth）:**

- visible: True / confidence: 0.9
- human_verdict: label_error
- comparison_label: Partial Match / Missed Secondary Objects

**記事内 NEG 表現:**

- L31 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR005 より抽出（00:30）。カラーのCGIとみられる映像（デジタル再現）。砂漠の景色（岩山・サボテン・低木）と青紫の夜空・星が確認できます。右中央付近の空中に**大きなオレンジ色の球体**が確認できます。米国西部
- L38 〔対象候補〕 `確認できません` : ファイル名「Digital_Recreation_Narrative_Statement_3-1」から、本映像は目撃者のナレーティブステートメント（陳述書）に基づくデジタル再現（CGI・3Dレンダリング等）と推定されます。実際の記録映像では
- L44 〔対象候補〕 `確認できません` : frame_0000（00:00）は完全に黒い画面です。映像はfade-in（徐々に明るくなる）で始まる可能性がありますが確認できません。
- L75 〔対象候補〕 `確認できません` : - 軍用センサーUIマーカーは確認できません
- L114 〔二次的〕 `確認できません` : 映像内容の判断には不確実性が含まれます。センサー種別・物体の性質・撮影状況の詳細は本映像単体では確認できません。

**修正候補文:**

> 【修正候補】右上付近に対象候補が確認できます。ただし、単一または少数フレームの目視確認であり、対象の性質・移動・正体を断定することはできません。追加フレームおよび専門的分析が必要です。

- **risk_level**: HIGH
- **human_review_required**: True
- **next_action**: 人間目視確認済み。記事内NEG表現と矛盾。note_draftのNEG表現を人間が確認し、必要に応じて慎重表現で修正。


## MEDIUM — 17件

### vlm_0001 | R02-025 | #2_025

- **category**: E_known_miss_case
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0001_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_frame_0030.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.75
- location: 中央
- description: 不明瞭な輝点、周囲に放射状のパターン

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR038 より抽出（00:30）。グレースケール映像（IRセンサーと推定されるが確認できません）。画面中央やや左に、強い輝点とみられる対象が確認できます。対象の周囲にハロー状の放射パターンが確認できます。グレー色のクロ
- L38 〔対象候補〕 `確認できません` : 他のRelease 02映像で多用されるシアン/マゼンタ色のマーカーとは異なり、本映像のUIマーカーはグレー色です。また映像周囲に明確なビネット（周辺減光）が確認でき、非常に多くの黒塗り矩形が確認できます。これらの特徴から、2013年当時の
- L41 〔二次的〕 `確認できません` : 映像の約25〜35秒付近のフレームでは、強い輝点とみられる対象がハロー状の放射パターンを伴って確認できます。対象は複数フレームにわたり画面内の異なる位置に確認され、映像内を移動しているとみられます。対象の正体・種別は現時点で確認できません。
- L62 〔二次的〕 `確認できません` : - 映像（IRセンサーと推定されるが確認できません）
- L79 〔対象候補〕 `確認できません` : - DVIDS Video Title：「Resolved as an Aircraft, Middle East 2013」（uap-csv-cache.csvより）。ファイル名は「Unresolved」だが、DVIDSのビデオタイトルは
- … 他 3 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央付近に不明瞭な輝点、周囲に放射状のパターンが確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0002 | R02-025 | #2_025

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0002_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_frame_0000.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや右上
- description: 小さな光点、背景より明るく、円形に近い。

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR038 より抽出（00:30）。グレースケール映像（IRセンサーと推定されるが確認できません）。画面中央やや左に、強い輝点とみられる対象が確認できます。対象の周囲にハロー状の放射パターンが確認できます。グレー色のクロ
- L38 〔対象候補〕 `確認できません` : 他のRelease 02映像で多用されるシアン/マゼンタ色のマーカーとは異なり、本映像のUIマーカーはグレー色です。また映像周囲に明確なビネット（周辺減光）が確認でき、非常に多くの黒塗り矩形が確認できます。これらの特徴から、2013年当時の
- L41 〔二次的〕 `確認できません` : 映像の約25〜35秒付近のフレームでは、強い輝点とみられる対象がハロー状の放射パターンを伴って確認できます。対象は複数フレームにわたり画面内の異なる位置に確認され、映像内を移動しているとみられます。対象の正体・種別は現時点で確認できません。
- L62 〔二次的〕 `確認できません` : - 映像（IRセンサーと推定されるが確認できません）
- L79 〔対象候補〕 `確認できません` : - DVIDS Video Title：「Resolved as an Aircraft, Middle East 2013」（uap-csv-cache.csvより）。ファイル名は「Unresolved」だが、DVIDSのビデオタイトルは
- … 他 3 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや右上付近に小さな光点、背景より明るく、円形に近い。が確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0003 | R02-025 | #2_025

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0003_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_frame_0005.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや下
- description: 不明瞭な光点、背景との明確な区別が難しい

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR038 より抽出（00:30）。グレースケール映像（IRセンサーと推定されるが確認できません）。画面中央やや左に、強い輝点とみられる対象が確認できます。対象の周囲にハロー状の放射パターンが確認できます。グレー色のクロ
- L38 〔対象候補〕 `確認できません` : 他のRelease 02映像で多用されるシアン/マゼンタ色のマーカーとは異なり、本映像のUIマーカーはグレー色です。また映像周囲に明確なビネット（周辺減光）が確認でき、非常に多くの黒塗り矩形が確認できます。これらの特徴から、2013年当時の
- L41 〔二次的〕 `確認できません` : 映像の約25〜35秒付近のフレームでは、強い輝点とみられる対象がハロー状の放射パターンを伴って確認できます。対象は複数フレームにわたり画面内の異なる位置に確認され、映像内を移動しているとみられます。対象の正体・種別は現時点で確認できません。
- L62 〔二次的〕 `確認できません` : - 映像（IRセンサーと推定されるが確認できません）
- L79 〔対象候補〕 `確認できません` : - DVIDS Video Title：「Resolved as an Aircraft, Middle East 2013」（uap-csv-cache.csvより）。ファイル名は「Unresolved」だが、DVIDSのビデオタイトルは
- … 他 3 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや下付近に不明瞭な光点、背景との明確な区別が難しいが確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0004 | R02-025 | #2_025

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0004_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_frame_0010.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや下
- description: 小さな光点、背景より明るく、形状は不明瞭。

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR038 より抽出（00:30）。グレースケール映像（IRセンサーと推定されるが確認できません）。画面中央やや左に、強い輝点とみられる対象が確認できます。対象の周囲にハロー状の放射パターンが確認できます。グレー色のクロ
- L38 〔対象候補〕 `確認できません` : 他のRelease 02映像で多用されるシアン/マゼンタ色のマーカーとは異なり、本映像のUIマーカーはグレー色です。また映像周囲に明確なビネット（周辺減光）が確認でき、非常に多くの黒塗り矩形が確認できます。これらの特徴から、2013年当時の
- L41 〔二次的〕 `確認できません` : 映像の約25〜35秒付近のフレームでは、強い輝点とみられる対象がハロー状の放射パターンを伴って確認できます。対象は複数フレームにわたり画面内の異なる位置に確認され、映像内を移動しているとみられます。対象の正体・種別は現時点で確認できません。
- L62 〔二次的〕 `確認できません` : - 映像（IRセンサーと推定されるが確認できません）
- L79 〔対象候補〕 `確認できません` : - DVIDS Video Title：「Resolved as an Aircraft, Middle East 2013」（uap-csv-cache.csvより）。ファイル名は「Unresolved」だが、DVIDSのビデオタイトルは
- … 他 3 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや下付近に小さな光点、背景より明るく、形状は不明瞭。が確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0022 | R02-032 | #2_032

- **category**: B_small_unclear
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0022_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_frame_0000.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.75
- location: 中央上部
- description: 紫色の楕円形で、背景より明るい。

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR045 より抽出（00:35）。グレースケールの映像（IRセンサーと推定されるが確認できません）。映像外縁にグリーン色のフレーム（縁取り）が確認できます。中央に大きな楕円形のマゼンタ色の輪郭線（追尾マーカーとみられま
- L35 〔対象候補〕 `確認できません` : ファイル名「Unresolved_UAP_Report_Middle_East_2020」ですが、files_catalog.csvの担当AOR（Area of Responsibility：担当作戦地域）は「Southern United
- L41 〔二次的〕 `確認できません` : 映像約35秒付近のフレームにて、赤い楕円形の追尾レティクル（トラッキングマーカー）の内部に**2つの白い輝点**が確認できます。さらに上部中央のマゼンタ色の小さな点を加えると計3点の光源とみられます。各点の関係・正体は映像フレームのみからは
- L63 〔二次的〕 `確認できません` : - グレースケールの映像（IRセンサーと推定されるが確認できません）
- L91 〔対象候補〕 `確認できません` : ファイル名は「Middle_East_2020」ですが、files_catalog.csvの担当AOR（Area of Responsibility：担当作戦地域）は「Southern United States」（南部米国）です。同じファ
- … 他 1 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央上部付近に紫色の楕円形で、背景より明るい。が確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0023 | R02-032 | #2_032

- **category**: B_small_unclear
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0023_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_frame_0005.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.8
- location: 中央上部
- description: 紫色の光と黒い矩形の組み合わせ

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR045 より抽出（00:35）。グレースケールの映像（IRセンサーと推定されるが確認できません）。映像外縁にグリーン色のフレーム（縁取り）が確認できます。中央に大きな楕円形のマゼンタ色の輪郭線（追尾マーカーとみられま
- L35 〔対象候補〕 `確認できません` : ファイル名「Unresolved_UAP_Report_Middle_East_2020」ですが、files_catalog.csvの担当AOR（Area of Responsibility：担当作戦地域）は「Southern United
- L41 〔二次的〕 `確認できません` : 映像約35秒付近のフレームにて、赤い楕円形の追尾レティクル（トラッキングマーカー）の内部に**2つの白い輝点**が確認できます。さらに上部中央のマゼンタ色の小さな点を加えると計3点の光源とみられます。各点の関係・正体は映像フレームのみからは
- L63 〔二次的〕 `確認できません` : - グレースケールの映像（IRセンサーと推定されるが確認できません）
- L91 〔対象候補〕 `確認できません` : ファイル名は「Middle_East_2020」ですが、files_catalog.csvの担当AOR（Area of Responsibility：担当作戦地域）は「Southern United States」（南部米国）です。同じファ
- … 他 1 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央上部付近に紫色の光と黒い矩形の組み合わせが確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0024 | R02-032 | #2_032

- **category**: B_small_unclear
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0024_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_frame_0010.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.8
- location: 中央上部
- description: ピンク色の光と周囲の黒い矩形

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR045 より抽出（00:35）。グレースケールの映像（IRセンサーと推定されるが確認できません）。映像外縁にグリーン色のフレーム（縁取り）が確認できます。中央に大きな楕円形のマゼンタ色の輪郭線（追尾マーカーとみられま
- L35 〔対象候補〕 `確認できません` : ファイル名「Unresolved_UAP_Report_Middle_East_2020」ですが、files_catalog.csvの担当AOR（Area of Responsibility：担当作戦地域）は「Southern United
- L41 〔二次的〕 `確認できません` : 映像約35秒付近のフレームにて、赤い楕円形の追尾レティクル（トラッキングマーカー）の内部に**2つの白い輝点**が確認できます。さらに上部中央のマゼンタ色の小さな点を加えると計3点の光源とみられます。各点の関係・正体は映像フレームのみからは
- L63 〔二次的〕 `確認できません` : - グレースケールの映像（IRセンサーと推定されるが確認できません）
- L91 〔対象候補〕 `確認できません` : ファイル名は「Middle_East_2020」ですが、files_catalog.csvの担当AOR（Area of Responsibility：担当作戦地域）は「Southern United States」（南部米国）です。同じファ
- … 他 1 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央上部付近にピンク色の光と周囲の黒い矩形が確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0025 | R02-033 | #2_033

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0025_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_frame_0000.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや右上
- description: 不明瞭な形状、暗い背景に浮かび上がる

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR046 より抽出（00:00）。グレースケールの映像（IRセンサーと推定されるが確認できません）。均一なグレーの背景（海面または空とみられますが確認できません）。**画面中央に白い翼状または飛行体状の物体が明確に確認
- L38 〔二次的〕 `確認できません` : frame_0000において、均一なグレーの背景（海面または空とみられる）に対して、白い翼状または飛行体状の物体が中央に明確に確認できます。物体は翼とみられる構造を持つ形状（ただし確認できません）で、Release 02のVID映像の中では
- L41 〔対象候補〕 `確認できません` : 物体の周囲（上下左右）に黒い矩形コーナーマーカーが確認できます。これらがトラッキングシステムのUIかセンサーのフレームマーカーかは映像フレームのみからは確認できません。
- L64 〔二次的〕 `確認できません` : - グレースケールの映像（IRセンサーと推定されるが確認できません）
- L65 〔二次的〕 `確認できません` : - 均一なグレーの背景（海面または空とみられるが確認できません）
- … 他 3 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや右上付近に不明瞭な形状、暗い背景に浮かび上がるが確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0026 | R02-033 | #2_033

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0026_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_frame_0005.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや上部
- description: 不明瞭な形状、暗い背景に浮かび上がる

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR046 より抽出（00:00）。グレースケールの映像（IRセンサーと推定されるが確認できません）。均一なグレーの背景（海面または空とみられますが確認できません）。**画面中央に白い翼状または飛行体状の物体が明確に確認
- L38 〔二次的〕 `確認できません` : frame_0000において、均一なグレーの背景（海面または空とみられる）に対して、白い翼状または飛行体状の物体が中央に明確に確認できます。物体は翼とみられる構造を持つ形状（ただし確認できません）で、Release 02のVID映像の中では
- L41 〔対象候補〕 `確認できません` : 物体の周囲（上下左右）に黒い矩形コーナーマーカーが確認できます。これらがトラッキングシステムのUIかセンサーのフレームマーカーかは映像フレームのみからは確認できません。
- L64 〔二次的〕 `確認できません` : - グレースケールの映像（IRセンサーと推定されるが確認できません）
- L65 〔二次的〕 `確認できません` : - 均一なグレーの背景（海面または空とみられるが確認できません）
- … 他 3 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや上部付近に不明瞭な形状、暗い背景に浮かび上がるが確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0029 | R02-034 | #2_034

- **category**: B_small_unclear
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0029_DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023_frame_0010.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央
- description: 小さな光点、背景より明るい。

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR047 より抽出（00:15）。グレースケールの映像（IRセンサーと推定されるが確認できません）。均一なグレーの背景。画面中央上部付近に**複数の明るい白い輝点がクラスター状に集まった対象**が確認できます。対象はマ
- L38 〔対象候補〕 `確認できません` : PR045（Southern United States 2020）と類似した特殊なUIスタイルが確認できます。グリーン色のフレーム（外縁縁取り）と赤い円形のクロスヘアマーカーが特徴です。PR045とは異なる用途・機器による可能性があります
- L62 〔二次的〕 `確認できません` : - グレースケールの映像（IRセンサーと推定されるが確認できません）
- L69 〔二次的〕 `確認できません` : - 映像右付近に白い小さな点（UAP候補の可能性があるが確認できません）
- L89 〔二次的〕 `確認できません` : 本映像内でUAPとされる対象物は、映像約15〜25秒付近のフレームにて複数の明るい白い輝点がクラスター状に集まった形状として確認できます。対象の正体・種別は現時点で確認できません。「UAP」「Unresolved」はファイル名に付与された分
- … 他 2 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央付近に小さな光点、背景より明るい。が確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0037 | R02-037 | #2_037

- **category**: B_small_unclear
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0037_FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021_frame_0030.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_States_2021_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや下
- description: 小さな白い光、背景との明確な区別あり

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR001 より抽出（00:00）。夜間のほぼ黒い映像（可視光カメラと推定されるが確認できません）。星空とみられる背景（多数の小さな点が確認できます）。中央付近に小さな点（光源とみられます）が1つ確認できます。軍用センサ
- L37 〔二次的〕 `確認できません` : **2. 可視光カメラと推定される夜間の映像。軍用センサーUIマーカーは確認できません**
- L38 〔対象候補〕 `確認できません` : 本映像は軍用センサー映像（DOW-UAP系）と異なり、シアン/マゼンタのUIマーカーは確認できません。可視光カメラによる夜間撮影と推定されますが確認できません。frame_0000では星空とみられる背景に中央付近の小さな点（光源）が1つ確認
- L41 〔対象候補〕 `確認できません` : ファイル名の「Triangle Orbs」（三角形のオーブ）について、frame_0000では確認できませんでした。「三角形」の配置に関しては映像を通じた確認が必要ですが、抽出フレームでは1点の小さな光源のみ確認できます。
- L62 〔二次的〕 `確認できません` : - 夜間のほぼ黒い映像（可視光カメラと推定されるが確認できません）
- … 他 3 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや下付近に小さな白い光、背景との明確な区別ありが確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0039 | R02-038 | #2_038

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0039_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_frame_0000.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや上
- description: 赤い光点、周囲は完全に暗闇

**記事内 NEG 表現:**

- L29 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR002 より抽出（00:00）。夜間の暗い映像（可視光カメラと推定されるが確認できません）。ほぼ黒い背景（夜空または暗い環境）。**中央左付近に明確な赤い光球**（小さい丸い赤い点）が確認できます。軍用センサーUIマ
- L38 〔対象候補〕 `確認できません` : **2. 夜間の可視光映像で、ほぼ黒い背景に赤い光球が確認できる。軍用センサーUIは確認できません**
- L39 〔対象候補〕 `確認できません` : 夜間のほぼ黒い背景に対して、中央左付近に明確な赤い光球が確認できます。DOW-UAP映像で多く見られるシアン/マゼンタのUIマーカーは本映像では確認できません。
- L42 〔対象候補〕 `確認できません` : ファイル名の「Rotation」（回転）について、frame_0000では確認できません。回転の動きは映像を通じた確認が必要です。
- L64 〔二次的〕 `確認できません` : - 夜間の暗い映像（可視光カメラと推定されるが確認できません）
- … 他 4 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや上付近に赤い光点、周囲は完全に暗闇が確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0040 | R02-038 | #2_038

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0040_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_frame_0030.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや右上
- description: 赤い光の球体、背景との明確な区別あり

**記事内 NEG 表現:**

- L29 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR002 より抽出（00:00）。夜間の暗い映像（可視光カメラと推定されるが確認できません）。ほぼ黒い背景（夜空または暗い環境）。**中央左付近に明確な赤い光球**（小さい丸い赤い点）が確認できます。軍用センサーUIマ
- L38 〔対象候補〕 `確認できません` : **2. 夜間の可視光映像で、ほぼ黒い背景に赤い光球が確認できる。軍用センサーUIは確認できません**
- L39 〔対象候補〕 `確認できません` : 夜間のほぼ黒い背景に対して、中央左付近に明確な赤い光球が確認できます。DOW-UAP映像で多く見られるシアン/マゼンタのUIマーカーは本映像では確認できません。
- L42 〔対象候補〕 `確認できません` : ファイル名の「Rotation」（回転）について、frame_0000では確認できません。回転の動きは映像を通じた確認が必要です。
- L64 〔二次的〕 `確認できません` : - 夜間の暗い映像（可視光カメラと推定されるが確認できません）
- … 他 4 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや右上付近に赤い光の球体、背景との明確な区別ありが確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0041 | R02-038 | #2_038

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0041_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_frame_0060.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United_States_2022_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや左上
- description: 赤い円形の光、周囲は暗く背景との对比が強い

**記事内 NEG 表現:**

- L29 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR002 より抽出（00:00）。夜間の暗い映像（可視光カメラと推定されるが確認できません）。ほぼ黒い背景（夜空または暗い環境）。**中央左付近に明確な赤い光球**（小さい丸い赤い点）が確認できます。軍用センサーUIマ
- L38 〔対象候補〕 `確認できません` : **2. 夜間の可視光映像で、ほぼ黒い背景に赤い光球が確認できる。軍用センサーUIは確認できません**
- L39 〔対象候補〕 `確認できません` : 夜間のほぼ黒い背景に対して、中央左付近に明確な赤い光球が確認できます。DOW-UAP映像で多く見られるシアン/マゼンタのUIマーカーは本映像では確認できません。
- L42 〔対象候補〕 `確認できません` : ファイル名の「Rotation」（回転）について、frame_0000では確認できません。回転の動きは映像を通じた確認が必要です。
- L64 〔二次的〕 `確認できません` : - 夜間の暗い映像（可視光カメラと推定されるが確認できません）
- … 他 4 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや左上付近に赤い円形の光、周囲は暗く背景との对比が強いが確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0042 | R02-039 | #2_039

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0042_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_frame_0000.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央上部
- description: 白い光点、周囲は暗く、背景との明確な区別がある。

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR003 より抽出（00:00）。夜間の縦位置映像（可視光カメラ・スマートフォンまたは民間カメラと推定されるが確認できません）。暗い雲・空の背景。中央付近に**明確な白い丸い光球（オーブ）**が確認できます。軍用センサ
- L38 〔対象候補〕 `確認できません` : frame_0000において、暗い雲と空の背景に対して、白い丸い光球（オーブ）が中央付近に確認できます。DOW-UAP映像で多く見られる軍用センサーUIは確認できません。
- L61 〔二次的〕 `確認できません` : - 夜間の縦位置映像（可視光カメラと推定されるが確認できません）
- L64 〔対象候補〕 `確認できません` : - 軍用センサーUIマーカーは確認できません
- L85 〔二次的〕 `確認できません` : 本映像内でUAPとされる対象物は、全フレームを通じて明確な白い光球（オーブ）として確認できます。対象は映像全体を通じて一定の明るさを保ちながら位置が変化し、移動しているとみられます。対象の正体・種別は現時点で確認できません。「UAP」「Un
- … 他 2 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央上部付近に白い光点、周囲は暗く、背景との明確な区別がある。が確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0043 | R02-039 | #2_039

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0043_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_frame_0030.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや上部
- description: 白い光点、周囲は暗く、背景との明確な区別あり。

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR003 より抽出（00:00）。夜間の縦位置映像（可視光カメラ・スマートフォンまたは民間カメラと推定されるが確認できません）。暗い雲・空の背景。中央付近に**明確な白い丸い光球（オーブ）**が確認できます。軍用センサ
- L38 〔対象候補〕 `確認できません` : frame_0000において、暗い雲と空の背景に対して、白い丸い光球（オーブ）が中央付近に確認できます。DOW-UAP映像で多く見られる軍用センサーUIは確認できません。
- L61 〔二次的〕 `確認できません` : - 夜間の縦位置映像（可視光カメラと推定されるが確認できません）
- L64 〔対象候補〕 `確認できません` : - 軍用センサーUIマーカーは確認できません
- L85 〔二次的〕 `確認できません` : 本映像内でUAPとされる対象物は、全フレームを通じて明確な白い光球（オーブ）として確認できます。対象は映像全体を通じて一定の明るさを保ちながら位置が変化し、移動しているとみられます。対象の正体・種別は現時点で確認できません。「UAP」「Un
- … 他 2 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや上部付近に白い光点、周囲は暗く、背景との明確な区別あり。が確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。

### vlm_0044 | R02-039 | #2_039

- **category**: A_clear_candidate
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0044_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_frame_0060.png`
- **draft**: `note_drafts/ai_summary_FBI-UAP-PR003_Orbs_Over_the_Pond_2024_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央やや左上
- description: 白い光点、背景と明確に区別できる

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ FBI-UAP-PR003 より抽出（00:00）。夜間の縦位置映像（可視光カメラ・スマートフォンまたは民間カメラと推定されるが確認できません）。暗い雲・空の背景。中央付近に**明確な白い丸い光球（オーブ）**が確認できます。軍用センサ
- L38 〔対象候補〕 `確認できません` : frame_0000において、暗い雲と空の背景に対して、白い丸い光球（オーブ）が中央付近に確認できます。DOW-UAP映像で多く見られる軍用センサーUIは確認できません。
- L61 〔二次的〕 `確認できません` : - 夜間の縦位置映像（可視光カメラと推定されるが確認できません）
- L64 〔対象候補〕 `確認できません` : - 軍用センサーUIマーカーは確認できません
- L85 〔二次的〕 `確認できません` : 本映像内でUAPとされる対象物は、全フレームを通じて明確な白い光球（オーブ）として確認できます。対象は映像全体を通じて一定の明るさを保ちながら位置が変化し、移動しているとみられます。対象の正体・種別は現時点で確認できません。「UAP」「Un
- … 他 2 件

**修正候補文:**

> 【修正候補（VLMのみ）】中央やや左上付近に白い光点、背景と明確に区別できるが確認される可能性があります。ただし、本候補はローカルVLM（Qwen2.5-VL-7B）による自動解析であり、人間による目視確認が必要です。断定的な記述は避けてください。

- **risk_level**: MEDIUM
- **human_review_required**: True
- **next_action**: VLM検出あり + 記事にUAP対象NEG表現。人間目視確認後、矛盾があれば慎重表現で修正候補を検討。


## SKIP — 1件

### vlm_0021 | R02-031 | #2_031

- **category**: C_no_visible_target
- **frame**: `data/vlm_eval_set/20260625/images/vlm_0021_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_frame_0060.png`
- **draft**: `note_drafts/ai_summary_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_note_version.md`

**VLM判定:**

- visible: True / confidence: 0.7
- location: 中央
- description: 不明瞭な黒い形状、背景との明確な区別は難しい。

**人間判定（ground truth）:**

- visible: False / confidence: 0.9
- human_verdict: false_positive
- comparison_label: False Positive / Acceptable

**記事内 NEG 表現:**

- L28 〔二次的〕 `確認できません` : ▲ DOW-UAP-PR044 より抽出（00:00）。グレースケールの映像（IRセンサーと推定されるが確認できません）。**画面中央にタンカーとみられる暗い船舶形状が明確に確認できます**。船舶形状の周囲に拡散した明るいハロー（輝き）が確
- L38 〔二次的〕 `確認できません` : 映像開始直後（00:00付近）のフレームにて、画面中央にタンカーとみられる暗い船舶形状が明確に確認できます。船舶形状の周囲に拡散した明るいハロー（輝き）が確認でき、赤い矢印マーカーが対象を指示しています。この対象の正体は映像フレームのみから
- L41 〔対象候補〕 `確認できません` : 赤い矢印状のマーカーが左中央付近に確認できます。PR036でも類似した赤矢印マーカーが確認されており、同一または類似したシステムによる記録の可能性がありますが確認できません。
- L62 〔二次的〕 `確認できません` : - グレースケールの映像（IRセンサーと推定されるが確認できません）
- L65 〔二次的〕 `確認できません` : - 中央付近に黒い物体状の形状（正体は確認できません）
- … 他 3 件

**修正候補文:**

> （VLM誤検出確定のため修正不要）

- **risk_level**: SKIP
- **human_review_required**: False
- **next_action**: VLM誤検出確定。記事修正不要。評価セットのカテゴリラベルは正しい。

---

## 修正手順（human_review_required=true の場合）

1. `frame_path` の画像を目視確認
2. `draft` の該当行を確認
3. VLM・人間判定と記事記述が矛盾している場合、`修正候補文` を参考に慎重表現で修正
4. 修正後に `ground_truth.csv` の `notes` に修正内容を記録
5. 記事公開フロー（publish workflow）は別途実施

