# VLM Phase 3 — 人間目視確認対象一覧

- 作成日: 2026-06-26
- 更新日: 2026-06-26（人間目視結果を記録）
- 目的: C/D カテゴリ誤検出疑い7件を人間が目視確認し、VLM誤検出か評価ラベル誤りかを判定する
- 画像変更: なし / DB変更: なし
- ground_truth保存先: `data/vlm_eval_set/20260625/ground_truth.csv`

---

## 目視確認結果サマリー

| sample_id | article_id | category | human_visible | human_verdict | comparison_label | review_required |
|-----------|------------|----------|---------------|---------------|------------------|-----------------|
| vlm_0019 | R02-031 | C | true | label_error | Partial Match / Description Gap | true |
| vlm_0021 | R02-031 | C | false | false_positive | False Positive / Acceptable | false |
| vlm_0033 | R02-036 | C | true | label_error | Partial Match | true |
| vlm_0045 | R02-040 | C | true | label_error | Match | true |
| vlm_0046 | R02-040 | C | true | label_error | Match | true |
| vlm_0047 | R02-040 | C | true | label_error | Match | true |
| vlm_0049 | R02-041 | D | true | label_error | Partial Match / Missed Secondary Objects | true |

**結果**: 7件中 label_error=6件、false_positive=1件（vlm_0021のみVLM誤検出）

---

## R02-031 — DOW-UAP-PR044（Middle East 2020）

### vlm_0019

- **image**: `data/vlm_eval_set/20260625/images/vlm_0019_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_frame_0000.png`
- **frame**: frame_0000（冒頭）
- **category（評価セット）**: C_no_visible_target
- **VLM判定**: visible=true, conf=0.7 / 「不明瞭な形状の暗い物体、背景との明確な区別は困難」
- **human_visible_candidate**: true
- **human_confidence**: 0.6
- **human_location**: 中央
- **human_objects**: 船舶形状の物体（断定せず）
- **human_description**: 画面中央に船舶形状の物体が視認できる。暗い映像内に比較的明確な形状として認識できる。
- **human_uncertainty**: 船舶と断定はしない。形状類似に基づく認識。
- **human_verdict**: `label_error`
- **comparison_label**: `Partial Match / Description Gap`
- **next_action**: 評価セットカテゴリを C→B に修正。note_drafts の NEG表現の確認（記事修正候補）。

### vlm_0021

- **image**: `data/vlm_eval_set/20260625/images/vlm_0021_DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020_frame_0060.png`
- **frame**: frame_0060（2秒付近）
- **category（評価セット）**: C_no_visible_target
- **VLM判定**: visible=true, conf=0.7 / 「不明瞭な黒い形状、背景との明確な区別は難しい」
- **human_visible_candidate**: false
- **human_confidence**: 0.9
- **human_location**: なし
- **human_objects**: Nマーク・赤三角マーカー・四隅フレーム枠マーカー（UIのみ）
- **human_description**: UIエレメントのみ確認（Nマーク・赤三角マーク・フレーム枠）。対象物と判断できる形状は確認できない。
- **human_uncertainty**: なし
- **human_verdict**: `false_positive`
- **comparison_label**: `False Positive / Acceptable`
- **next_action**: VLM誤検出確定。カテゴリCラベルは正しい。記事修正不要。

---

## R02-036 — DOW-UAP-PR049（Department of the Army 2026）

### vlm_0033

- **image**: `data/vlm_eval_set/20260625/images/vlm_0033_DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_the_Army_2026_frame_0000.png`
- **frame**: frame_0000（冒頭）
- **category（評価セット）**: C_no_visible_target
- **VLM判定**: visible=true, conf=0.7 / 「白い線と点の集合、背景との明確な区別」
- **human_visible_candidate**: true
- **human_confidence**: 0.6
- **human_location**: 中央
- **human_objects**: 白い物体（形状不明）+ UIオーバーレイ
- **human_description**: UIオーバーレイが何らかの対象を追跡している。白い物体が視認できるが形状は定かでない。UIと対象の区別が困難。
- **human_uncertainty**: 白い物体が何であるかは判別できない。UIが誘導している可能性を否定できない。
- **human_verdict**: `label_error`
- **comparison_label**: `Partial Match`
- **next_action**: 評価セットカテゴリを C→B に修正検討。note_drafts の NEG表現の確認。

---

## R02-040 — FBI-UAP-PR004（Northeastern Orb Sighting 2025）

> 同一動画の3フレーム。3件すべてで赤い光源2個が一貫して視認できた。カテゴリCラベルは誤り（→B/A相当）。

### vlm_0045

- **image**: `data/vlm_eval_set/20260625/images/vlm_0045_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_frame_0000.png`
- **frame**: frame_0000（冒頭）
- **category（評価セット）**: C_no_visible_target
- **VLM判定**: visible=true, conf=0.7 / 「赤い線状の光、背景との明確な区別あり」
- **human_visible_candidate**: true
- **human_confidence**: 0.9
- **human_location**: 全体（線状に延伸）
- **human_objects**: 赤い光源2個（カメラブレで線状に延伸）
- **human_description**: 赤い2つの光源が視認できる。カメラのブレにより光源が線状に横方向へ延伸している。
- **human_uncertainty**: 光源2個の判定はブレの形状から推定。静止状態では点状の可能性あり。
- **human_verdict**: `label_error`
- **comparison_label**: `Match`
- **next_action**: VLMの「赤い線状の光」記述は正確。カテゴリをC→Bに修正。記事修正候補（高優先）。

### vlm_0046

- **image**: `data/vlm_eval_set/20260625/images/vlm_0046_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_frame_0005.png`
- **frame**: frame_0005
- **category（評価セット）**: C_no_visible_target
- **VLM判定**: visible=true, conf=0.7 / 「小さな光点、背景と明確に区別できる」
- **human_visible_candidate**: true
- **human_confidence**: 0.85
- **human_location**: 中央
- **human_objects**: 赤い光源2個
- **human_description**: 画像中央付近に赤い2つの光源が視認できる。
- **human_uncertainty**: なし
- **human_verdict**: `label_error`
- **comparison_label**: `Match`
- **next_action**: カテゴリC→B修正。vlm_0045と同一動画連続フレーム。

### vlm_0047

- **image**: `data/vlm_eval_set/20260625/images/vlm_0047_FBI-UAP-PR004_Northeastern_Orb_Sighting_2025_frame_0010.png`
- **frame**: frame_0010
- **category（評価セット）**: C_no_visible_target
- **VLM判定**: visible=true, conf=0.7 / 「赤い光点、周囲は暗く、背景との明確な区別」
- **human_visible_candidate**: true
- **human_confidence**: 0.8
- **human_location**: 中央左上
- **human_objects**: 赤い光源2個（低解像度）
- **human_description**: 画像中央左上側に赤い2つの光源が視認できる。ズームによる解像度低下あり。
- **human_uncertainty**: 低解像度のため位置・個数の精度は限定的。
- **human_verdict**: `label_error`
- **comparison_label**: `Match`
- **next_action**: カテゴリC→B修正。vlm_0045/0046と同一動画連続フレーム。

---

## R02-041 — FBI-UAP-PR005（Digital Recreation 2023）

### vlm_0049

- **image**: `data/vlm_eval_set/20260625/images/vlm_0049_FBI-UAP-PR005_Digital_Recreation_Narrative_Statement_3-1_Western_United_States_Event_2023_frame_0030.png`
- **frame**: frame_0030（1秒付近）
- **category（評価セット）**: D_sensor_ui_background
- **VLM判定**: visible=true, conf=0.8 / 「黄色い球体、背景に星が見える」
- **human_visible_candidate**: true
- **human_confidence**: 0.9
- **human_location**: 中央左（球体）、右側（赤い光源）
- **human_objects**: オレンジ/黄色球体・赤い光源2個・星空背景
- **human_description**: 星空のような空に黄色/オレンジ色の球体と赤い2つの光源が浮かんでいる。球体右側に赤い光源2個が確認できる。
- **human_uncertainty**: Digital Recreation映像のため描画オブジェクトである可能性が高い。実際の撮影映像との区別要確認。
- **human_verdict**: `label_error`
- **comparison_label**: `Partial Match / Missed Secondary Objects`
- **next_action**: VLMは主対象（黄色球体+星空）は正しく検出したが赤い光源2個を見落とし。Dカテゴリの定義見直しが必要（CGオブジェクトを「背景」と扱うかどうか）。記事修正候補。

---

## 確認結果まとめ

### label_error 確定（6件）→ カテゴリ修正候補

| sample_id | 現カテゴリ | 推奨変更先 | 理由 |
|-----------|------------|------------|------|
| vlm_0019 | C | B | 船舶形状の物体が視認できる |
| vlm_0033 | C | B | 白い物体が視認できる（形状不明） |
| vlm_0045 | C | B | 赤い光源2個、明確に視認 |
| vlm_0046 | C | B | 同上 |
| vlm_0047 | C | B | 同上（低解像度） |
| vlm_0049 | D | A | CGオブジェクト（球体+光源）が明確に視認できる |

### false_positive 確定（1件）→ カテゴリ変更不要

| sample_id | 現カテゴリ | VLM誤りの内容 |
|-----------|------------|---------------|
| vlm_0021 | C（正しい） | UIマーカーを対象物と誤認 |

### 次手順

1. `ground_truth.csv` に全件記録済み（`data/vlm_eval_set/20260625/ground_truth.csv`）
2. 評価セット v2 向けに manifest.csv の category を修正（別タスク）
3. R02-031 / R02-036 / R02-040 / R02-041 の note_drafts を記事修正候補として確認
4. 次VLMモデル（Qwen2.5-VL-32B等）比較時に ground_truth.csv を基準として使用
