# Media Inspector Ground Truth 仕様 v1

- 作成日: 2026-06-26
- バージョン: v1
- 対象評価セット: `data/vlm_eval_set/20260625/`
- 対象モデル: Qwen2.5-VL-7B-Instruct（Phase 3 基準）

---

## 1. 目的

VLM（ローカル画像言語モデル）によるUAPフレーム評価を人間の目視確認で検証し、
モデル比較・精度改善・記事修正候補抽出に再利用できる評価資産を構築する。

---

## 2. Ground Truth の役割

| 役割 | 説明 |
|------|------|
| VLM評価の正解ラベル | モデル間比較の基準（Qwen/InternVL/MiniCPM 等） |
| 誤検出／見落とし判定 | False Positive / False Negative の確定 |
| 記事修正候補の根拠 | note_drafts のNEG表現を修正すべき対象を特定 |
| 評価セット改善 | カテゴリラベル誤りを修正し、次世代評価セットへ継承 |

---

## 3. human_visible_candidate の定義

| 値 | 条件 |
|----|------|
| `true` | 人間が画像内に対象物候補（光源・形状・不明物体）を視認できる |
| `false` | 人間が画像内に対象物候補を視認できない（背景・UIのみ） |
| `uncertain` | 視認可否が判断できない（低解像度・全体が不鮮明等） |

**注意**:
- UIオーバーレイ（クロスヘア・方位マーカー・枠線）のみ見える場合は `false`
- UIが何かを「追跡している」場合は、その対象が視認できれば `true`
- 断定できなくても、形状の存在が確認できれば `true`（不確実性は `human_uncertainty` に記録）

---

## 4. human_description の書き方

- 視覚的に観察できる事実のみを記述する
- 推測・解釈は `human_uncertainty` に分離して記述する
- 物体の種別断定は避ける（「船舶」でなく「船舶形状の物体」）
- 複数対象がある場合はそれぞれ記述する（例: 「オレンジ球体 + 赤い光源2個」）
- UIエレメントは括弧で区別する（例: 「（Nマーカー、赤三角マーカー）」）

---

## 5. human_confidence の定義

| 値 | 意味 |
|----|------|
| 0.9〜1.0 | 明確に視認できる。判定に迷いなし |
| 0.7〜0.89 | 視認できるが、低解像度・ブレ等の制約あり |
| 0.5〜0.69 | 存在の可能性はあるが、確信を持てない |
| 0.3〜0.49 | 非常に曖昧。画像品質または対象自体の問題 |
| 0.0〜0.29 | ほぼ判断不能 |

---

## 6. VLM評価との対応関係

| Ground Truth フィールド | VLM評価フィールド | 対応関係 |
|------------------------|------------------|---------|
| `human_visible_candidate` | `visible_candidate` | 一致／不一致が comparison_label の基礎 |
| `human_confidence` | `confidence` | 信頼度の人間基準 vs モデル基準 |
| `human_location` | `location` | 位置記述の精度比較 |
| `human_description` | `description` | 記述内容の質的比較 |

---

## 7. comparison_label の定義

| ラベル | 条件 |
|--------|------|
| `Match` | visible 一致 + description が実質的に合致 |
| `Partial Match` | visible 一致 + description に重要な差異あり |
| `Description Gap` | visible 一致 + description の内容が大きく乖離 |
| `Missed Secondary Objects` | 主対象は一致 + 人間が認識した副次対象をVLMが見落とし |
| `False Positive` | VLM: visible=true / Human: visible=false |
| `False Negative` | VLM: visible=false / Human: visible=true |
| `Acceptable` | VLM判定がUIや背景要素を検出したが、文脈上許容範囲 |
| `Label Error` | 評価セットのカテゴリラベル自体が誤りと判明 |

複数ラベルの組み合わせは `/` で区切る（例: `Partial Match / Missed Secondary Objects`）

---

## 8. human_verdict の定義

| 値 | 意味 |
|----|------|
| `false_positive` | VLMの誤検出。評価セットラベルは正しい |
| `label_error` | 評価セットのカテゴリラベルが誤り。対象物は実際に存在する |
| `ambiguous` | 人間も判断できない |
| `true_positive` | VLMの正検出。対象物あり |
| `true_negative` | VLMの正非検出。対象物なし |

---

## 9. review_required の条件

`review_required = true` となる条件:

1. `human_verdict = label_error` — カテゴリ修正が必要
2. `comparison_label` に `False Negative` が含まれる — VLMが見落とし
3. `human_visible_candidate = true` かつ note_drafts に NEG表現がある — 記事修正候補

---

## 10. 公開記事修正候補への接続方法

`review_required = true` のサンプルを特定 → `article_id` / `h2_number` で note_drafts を特定 →
note_drafts 内の NEG表現（「確認できません」等）が不正確かどうかを確認 →
修正が必要な場合は Article Revision Candidate として別途管理する。

接続ファイル:
- `data/vlm_eval_set/20260625/ground_truth.csv` → `article_id`, `h2_number`
- `note_drafts/ai_summary_{slug}_note_version.md`
- `review_logs/source_registry.csv` の `status` 確認

---

## 11. 安全制約

| 制約 | 内容 |
|------|------|
| S_CLASS 除外 | S_CLASS 分類のレコードは ground truth 対象外 |
| 外部API禁止 | VLM評価はローカルLM Studio のみ。Anthropic/OpenAI 等の外部API不使用 |
| note_drafts 変更禁止 | ground truth は評価資産であり、記事本文の変更権限を持たない |
| workflow.db 変更禁止 | ground truth は独立した評価データ。workflow管理とは分離 |
| source_registry 変更禁止 | 同上 |
| dangerouslyDisableSandbox 禁止 | いかなる状況でも使用しない |

---

## 12. ファイル構成

```
data/vlm_eval_set/20260625/
├── manifest.csv          # 評価セット定義（変更しない）
├── ground_truth.csv      # 人間目視結果 + VLM比較（このドキュメントの対象）
└── images/               # 評価画像（変更しない）

data/vlm_runs/
└── phase3_full50_20260626/
    ├── results.csv       # VLM評価結果
    └── results.jsonl

review_reports/
├── vlm_phase3_full50_report.md
└── vlm_phase3_human_review_targets.md
```

---

## 13. 次フェーズでの利用

| フェーズ | 利用方法 |
|----------|---------|
| VLMモデル比較 | Qwen2.5-VL-32B / MiniCPM-V / InternVL を同一セットで評価し、ground_truth.csv と比較 |
| 精度スコア計算 | Precision / Recall / F1 を category 別・モデル別に算出 |
| Article Revision | review_required=true + article_id で note_drafts の NEG表現を修正候補化 |
| 評価セット v2 | label_error 判明分のカテゴリを修正し、次世代評価セットを構築 |
