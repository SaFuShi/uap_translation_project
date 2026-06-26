# Published Article Evolution Agent v1.1 — 設計書

- 作成日: 2026-06-26
- 更新日: 2026-06-26（v1.1 — Evolution Decision を4分類に変更）
- ステータス: 設計書（scripts/published_article_evolution.py は v1 実装済み）
- 関連: Media Inspector / Ground Truth / VLM Scoring / Article Revision Candidate

---

## 0. Published Article Evolution の位置付け

> **本Agentの役割は「誤り訂正」ではなく「コンテンツの進化」を管理することである。**

公開済み記事は公開時点のパイプラインによる最善整理であり、誤りではない。
Media Inspector・VLM・Ground Truth が明らかにした新しい知見を、
どの記事にどのように反映するかを分類・管理する。

### 概要版と詳細解析版の役割

| 属性 | 概要版（現公開記事） | 詳細解析版（将来公開） |
|------|--------------------|--------------------|
| 目的 | 一次ソース紹介・現時点の最善整理 | 多角的解析・考察の深化 |
| 視覚情報 | 代表フレームの目視確認結果 | 全フレーム / VLM / GT を統合 |
| VLM解析 | なし / 参照のみ | ローカルVLM全件評価結果を反映 |
| Ground Truth | 参照なし | ground_truth.csv の結果を反映 |
| 観察補完 | 元映像再確認による追記は反映可 | 全観察情報の統合 |
| 考察・解釈 | 最小限（断定禁止） | 複数フレーム変化・パターン等 |
| 更新頻度 | 観察補完時のみ（追記形式） | VLMモデル改善・再解析時 |

---

## 1. Agentの目的

公開済み記事（published_articles/）を継続的に監査し、  
Media Inspector・Ground Truth・VLM Scoring・Article Revision Candidate の結果を統合して、  
各記事について **Evolution Decision**（進化判定）を自動分類する。

### 解決する問題

| 問題 | 現状 | Agent後 |
|------|------|---------|
| 元映像再確認で見つかった観察情報の反映が手動 | Phase 3で6件手動確認 | Observation Update で自動分類 |
| VLM改善時の差分が不明 | 都度手作業 | モデル比較で差分を自動検出 |
| 詳細解析版で反映すべき知見の把握が困難 | 個別確認 | Detailed Edition で自動抽出 |
| Release前チェックが存在しない | なし | Release03から事前チェック導入 |

---

## 2. 入力

| 入力 | パス | 役割 |
|------|------|------|
| 公開済み記事 | `published_articles/*.md` | 修正対象の本文 |
| Ground Truth | `data/vlm_eval_set/20260625/ground_truth.csv` | 人間目視の正解ラベル |
| VLM results | `data/vlm_runs/<run_id>/results.csv` | モデル推論結果 |
| Article Revision Candidates | `data/vlm_runs/<run_id>/article_revision_candidates.csv` | risk_level / next_action |
| Manifest | `data/vlm_eval_set/<date>/manifest.csv` | フレームと記事の対応 |
| Source Registry | `review_logs/source_registry.csv` | 公開日・URL・published_path |

---

## 3. 出力

| 出力 | パス | 形式 |
|------|------|------|
| Evolution レポート | `review_reports/published_article_evolution_report.md` | Markdown |
| Evolution CSV | `data/vlm_runs/<run_id>/published_article_evolution.csv` | CSV |
| 人間レビュー対象リスト | `review_reports/evolution_human_review_targets.md` | Markdown |

---

## 4. ワークフロー

```
published_articles/
        │
        ▼
┌─────────────────────────────┐
│  Step 1: Media Inspector    │  VLM全フレーム評価
│  scripts/run_vlm_eval.py    │  → data/vlm_runs/<run_id>/results.csv
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  Step 2: Ground Truth比較   │  人間目視確認との突合
│  scripts/score_vlm_vs_      │  → score_summary.csv
│  ground_truth.py            │  → Gold F1 / Proxy F1
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  Step 3: Article Revision   │  記事本文とVLM/GTの差分検出
│  Candidate                  │  → article_revision_candidates.csv
│  scripts/article_revision_  │  → risk_level: HIGH/MEDIUM/LOW/SKIP
│  candidate.py               │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  Step 4: Evolution Decision │  ← 本Agentの中核
│  scripts/published_article_ │
│  evolution.py               │
│                             │
│  判定ルール適用              │
│  → decision: A/B/C/D        │
│  → priority: High/Mid/Low   │
│  → human_review_required    │
└─────────────────────────────┘
        │
   ┌────┼──────────────┬─────────────┐
   ▼    ▼              ▼             ▼
A.即時  B.観察補完     C.詳細解析版  D.修正不要
Imme-   Observation    Detailed      No Change
diate   Update         Edition
Fix       │              │             │
  │       ▼              ▼             ▼
  │   概要版に         詳細解析版     記録のみ
  │   追記形式で       草稿作成時     = no_change
  │   反映可能         に反映
  ▼
人間レビュー
→ note_draft修正
→ note.com再公開
```

---

## 5. Evolution Decision — 4分類と判定ルール

### 5.1 Immediate Fix（即時修正）

公開済み記事に **事実誤認または読者に誤解を与える内容** がある場合。速やかな修正が必要。

「観察情報の欠落」ではなく「記述の誤り」が対象。

| 条件 | 詳細 | 例 |
|------|------|-----|
| IF-1 | 記事が「確認できない」と記述しているが、VLM・人間ともに確認できた | NEG表現が実際の観察と矛盾 |
| IF-2 | 時刻・フレーム番号の記述が事実と著しく異なる | 「10秒から可視」だが実際は0秒から |
| IF-3 | 物体の存在を否定しているが人間・VLM両方で確認できた | 主対象にNEG + GT陽性 |

**判定条件**:
- `risk_level = HIGH` かつ `has_uap_object_neg = true`（UAP主対象へのNEG）
- かつ `human_visible = true` かつ `human_confidence >= 0.8`
- かつ 記事の主観察に誤りがある（単なる未記載ではなく誤記述）

### 5.2 Observation Update（観察補完）★ v1.1 新設

公開済み記事に事実誤認はないが、**元映像再確認・VLM評価により確認された視覚情報が未記載** の場合。
新しい解析ではなく「観察情報の補完」であり、概要版でも追記形式で反映可能。

| 条件 | 詳細 | 例 |
|------|------|-----|
| OU-1 | 人間が元映像再確認で副次対象物を確認したが記事に未記載 | 赤い光点2個（R02-041） |
| OU-2 | VLMが検出した副次対象物を人間が高信頼度で確認し、記事に未記載 | Missed Secondary Objects + confidence≥0.8 |
| OU-3 | 主対象物の色・位置表現が目視確認と異なる（誤りではなく精度不足） | 「オレンジ色」→「黄色〜オレンジ色」 |

**判定条件**:
- `comparison_label` に `"Missed Secondary Objects"` を含む
- かつ `human_confidence >= 0.8`
- かつ `human_visible = true`
- かつ 副次対象物の記述が記事本文に存在しない
- かつ 主観察（主対象物の存在）には誤りがない

**概要版への反映方針**:
- 追記形式（【YYYY-MM-DD 追記】）で記述を補完する
- 断定表現は使用しない。「〜とみられる」「〜の可能性は断定できない」を維持する
- 圧縮アーティファクト等の留保を明示する

### 5.3 Detailed Edition（詳細解析版へ反映）

記事本文は概ね正確だが、**Media Inspector / VLM / Ground Truth / 人間再解析 により得られた新しい解析・考察・知見** を反映できる場合。概要版では扱わず、詳細解析版で反映する。

詳細解析版で反映する内容:
- Media Inspector 全フレーム評価の統合
- VLM複数モデル比較（Qwen2.5-VL-7B vs 32B 等）の結果
- Ground Truth との詳細突合（信頼度・位置・形状の変化）
- 複数フレーム間の対象物の変化・パターン
- AIパイプライン改善履歴（NEG分類精度向上等）
- 時刻・カバレッジの補完（概要版では記述できなかった細部）

| 条件 | 詳細 | 例 |
|------|------|-----|
| DE-1 | 評価セットラベル誤りで記事は正確だが、カバレッジ補完候補あり | R02-040（注意点の時刻補完） |
| DE-2 | 人間が低信頼度（<0.8）で対象を確認 | R02-036（frame_0000の白い物体） |
| DE-3 | GT未確認（MEDIUM候補）の記事 | R02-025/032/033等 |
| DE-4 | 複数フレームで Match が確認され、詳細解析版で統合価値がある | R02-040（3フレームでMatch） |
| DE-5 | 次世代VLMモデルで再評価後に差分が生じた | Qwen2.5-VL-32B比較 |

**判定条件（OR）**:
- `label_error + Match in comparison_label` → タイミング/カバレッジ補完候補
- `label_error + Partial Match + confidence < 0.8` → 低信頼度確認
- GT未確認 + `risk_level = MEDIUM` → 人間確認未実施

### 5.4 No Change（現状維持）

記事本文は正確。Evolution Decision による変更なし。記録のみ。

| 条件 | 詳細 | 例 |
|------|------|-----|
| NC-1 | 評価セットラベル誤り + 記事は既に正確 | R02-031（船舶形状が既に記述済み） |
| NC-2 | VLM False Positive（人間も対象なしを確認） | vlm_0021（UIマーカーのみ） |
| NC-3 | Description Gap のみ（語彙差異・意味は一致） | VLM語彙と記事語彙の表現差 |
| NC-4 | risk_level=SKIP | 低優先度 |

---

## 6. Evolution Decision 判定フローチャート（v1.1）

```
[GT（人間ground truth）あり？]
     │ No  → risk_level で判定
     │         MEDIUM → Detailed Edition
     │         SKIP   → No Change
     │ Yes
     ▼
[human_verdict = false_positive ?]
     │ Yes → No Change (NC-2)
     │ No
     ▼
[comparison_label に Missed Secondary Objects ?]
     │ Yes かつ confidence≥0.8
     │    ↓
     │ [記事に副次対象物の記述あり？]
     │    Yes → Detailed Edition (DE-4 補完候補)
     │    No  → Observation Update (OU-1/2)  ← v1.1 新設
     │
     │ No（Missed Secondary Objects なし）
     ▼
[Description Gap かつ confidence<0.8 ?]
     │ Yes → No Change (NC-3)
     │ No
     ▼
[comparison_label = Match ?]
     │ Yes → Detailed Edition (DE-1/4)
     │ No
     ▼
[confidence < 0.8 ?]
     │ Yes → Detailed Edition (DE-2)
     │ No  (confidence≥0.8)
     ▼
[has_uap_object_neg かつ 主観察に誤り？]
     │ Yes → Immediate Fix (IF-1/3)
     │ No
     ▼
[記事に記述あり？]
     │ Yes → No Change (NC-1)
     │ No  → Observation Update (OU-1)
```

---

## 7. 人間確認ポイント

### 必須（Immediate Fix）
| ポイント | 内容 |
|---------|------|
| HC-1 | 記事の誤記述箇所を人間が特定・承認 |
| HC-2 | 修正候補文を人間が査読 |
| HC-3 | note_draft最終確認後にnote再公開 |

### 必須（Observation Update）
| ポイント | 内容 |
|---------|------|
| HC-4 | 元映像の該当フレームを人間が目視確認 |
| HC-5 | 追記文案を人間が承認 |
| HC-6 | 【追記】セクションをnoteに挿入・再公開 |

### 任意（Detailed Edition）
| ポイント | 内容 |
|---------|------|
| HC-7 | VLM再評価結果の目視確認 |
| HC-8 | 詳細解析版草稿の最終承認 |

### 不要（No Change）
記録のみ。人間確認不要。

---

### note修正とdraft表現の完全一致について

**ポリシー: 内容同等であれば `done` とする。完全一致は不要。**

| ケース | evolution_status | 根拠 |
|--------|----------------|------|
| note修正内容がdraftと完全一致 | done | 理想的な状態 |
| note修正内容がdraftと表現は異なるが内容同等 | **done** | 内容同等なら `done` として記録 |
| note修正内容がdraftと意味・事実が異なる | confirmed（再確認要） | 内容差異を記録し再確認 |
| note修正がまだ行われていない | pending / confirmed | 再公開待ち |

**「内容同等」の判断基準**:
- 主要な事実（色・位置・対象物の存在）が反映されているか
- CGI/圧縮アーティファクト等の留保が明示されているか
- 断定表現が混入していないか

**記録方針**:
- note上の表現がdraftと異なる場合でも、内容同等なら `done` として記録する
- notes列に「note上の表現はdraftと完全一致ではないが内容同等」と記録し、反映内容の要点を明示する
- 人間が実際にnoteで修正した場合は `human_review_done: true` / `note_update_done: true` を記録する

---

## 8. published_article_evolution.py — スクリプト仕様（v1.1 更新対象）

### 8.1 入出力

```
入力:
  --published-dir     published_articles/ ディレクトリ
  --ground-truth      data/vlm_eval_set/<date>/ground_truth.csv
  --candidates        data/vlm_runs/<run_id>/article_revision_candidates.csv
  --source-registry   review_logs/source_registry.csv
  --run-id            実行識別子（例: phase3_full50_20260626）
  --model             モデル名（例: qwen2.5-vl-7b-instruct）
  --output            review_reports/published_article_evolution_report.md
  --csv               data/vlm_runs/<run_id>/published_article_evolution.csv

出力:
  Markdownレポート + CSV
```

### 8.2 主要関数（v1.1 で更新）

```python
def classify_single_gt(gt, article_text) -> str:
    """
    Returns:
      'immediate_fix'      ← 事実誤認・誤記述
      'observation_update' ← 観察情報の補完（v1.1 新設）
      'detailed'           ← 詳細解析版で反映
      'no_change'          ← 変更不要
    """

def decide_evolution(candidates, gt_map, article_text) -> tuple:
    """
    decision: Immediate Fix / Observation Update / Detailed Edition / No Change
    """
```

### 8.3 処理フロー

```python
# 1. 入力読み込み
candidates = load_candidates(args.candidates)
gt = load_ground_truth(args.ground_truth)
articles = load_published_articles(args.published_dir)
registry = load_source_registry(args.source_registry)

# 2. 判定（4分類）
records = build_evolution_records(candidates, articles, gt, registry)

# 3. 出力
write_evolution_csv(records, args.csv)
write_evolution_report(records, args.model, args.run_id, args.output)
```

---

## 9. published_article_evolution.csv — 項目設計（v1.1）

```csv
article_id,h2_number,sample_ids,published_date,published_url,
evolution_status,decision,priority,
human_review_required,human_review_done,human_review_date,
vlm_visible,human_visible,human_confidence,comparison_label,
has_uap_object_neg,risk_level,
modification_target_section,modification_draft,
next_action,notes
```

### decision 列（v1.1 更新）

| 値 | 意味 | 対応アクション |
|----|------|--------------|
| `Immediate Fix` | 事実誤認・誤記述 | 速やかにnote_draft修正・再公開 |
| `Observation Update` | 観察情報の補完 ★v1.1新設 | 元映像再確認後に【追記】形式で概要版へ反映 |
| `Detailed Edition` | 新知見・解析 | 詳細解析版草稿作成時に反映 |
| `No Change` | 変更不要 | 記録のみ |

### evolution_status 遷移（v1.1）

```
pending
  ├→ confirmed（人間レビュー完了）
  │     └→ done（note再公開完了）
  └→ no_change（修正不要確認）
```

---

## 10. Markdownレポート構成（v1.1）

```markdown
# Published Article Evolution Report

## サマリー

| decision | 件数 | 優先度 |
|----------|------|--------|
| Immediate Fix | N | High |
| Observation Update | N | High |   ← v1.1 新設
| Detailed Edition | N | Medium/Low |
| No Change | N | — |

## A. Immediate Fix（即時修正）
...

## B. Observation Update（観察補完）  ← v1.1 新設
...

## C. Detailed Edition（詳細解析版へ反映）
...

## D. No Change（修正不要）
...
```

---

## 11. 将来の自動化方針

### Phase 1（現在）: 手動運用
- Media Inspector → 人間がground_truth.csvを作成
- evolution.py (v1) → 3分類で判定
- note_draft修正 → Claude + 人間確認

### Phase 2（v1.1実装後）: 4分類対応
- evolution.py (v1.1) → Observation Update を自動分類
- Observation Update の追記文案を自動生成
- Detailed Edition の詳細解析版草稿を自動生成

### Phase 3（将来）: 継続監査
- 新モデル公開時に同一ground_truth.csvで自動再評価
- モデル比較レポートの自動生成（Qwen2.5-VL-32B 等）
- 詳細解析版の自動マージ・再公開

---

## 12. Release 03 への適用方針

### 公開前チェック（Pre-Publication Gate）

Release 03 からは **公開前に Media Inspector を通す** 設計を導入する。

```
[Release 03 公開フロー]

note_draft 完成
        │
        ▼
┌──────────────────────────────────┐
│  Pre-Publication Media Inspector │  ← Release 03 新設
│  - VLM全代表フレーム評価          │
│  - NEG表現チェック               │
│  - evolution_status=pre_check    │
└──────────────────────────────────┘
        │
        ▼
[Pre-check レポート出力]
  → review_reports/precheck_R03-XXX.md
        │
   ┌────┼──────────────────┐
   ▼    ▼                  ▼
  OK  Observation        公開保留
      Update候補          (要修正)
   │    │                  │
   ▼    ▼                  ▼
 公開  人間確認後          draft修正
      に公開              → 再チェック
```

### Pre-check 判定基準（v1.1）

| 判定 | 条件 | アクション |
|------|------|-----------|
| OK | risk_level=LOW以下 / No Change | そのまま公開 |
| Observation Update候補 | Missed Secondary Objects + confidence≥0.8 | 元映像確認後に【追記】付きで公開 |
| 要確認 | risk_level=MEDIUM / 副次NEG | 人間確認後に公開 |
| 公開保留 | risk_level=HIGH / UAP-object NEG + VLM陽性 | draft修正後に再チェック |

---

## 13. 既知の制約・注意事項

| 制約 | 内容 |
|------|------|
| S_CLASS | 言及禁止 |
| 外部API | 使用禁止（LM Studio ローカルのみ） |
| published_articles | 直接変更禁止（note_draft経由） |
| 断定表現 | 物体の正体・種別の断定表現への変更禁止 |
| 圧縮アーティファクト | Observation Update では必ず留保を記述 |
| ground_truth | 現在7件（2026-06-25）。次フェーズで拡張 |
| VLMモデル依存 | Qwen2.5-VL-7B基準。32B比較で判定変化の可能性あり |

---

## 関連ファイル

| ファイル | 役割 |
|---------|------|
| `docs/media_inspector_ground_truth_v1.md` | Ground Truth 仕様 |
| `review_reports/published_article_evolution_plan_20260626.md` | 現在の運用方針 |
| `review_reports/article_revision_high6_confirmed_20260626.md` | HIGH 6件確定分析 |
| `review_reports/article_revision_candidates_20260626.md` | 全24件候補リスト |
| `data/vlm_eval_set/20260625/ground_truth.csv` | 人間目視 Ground Truth |
| `scripts/score_vlm_vs_ground_truth.py` | VLMスコアリング |
| `scripts/article_revision_candidate.py` | 修正候補生成 |
| `scripts/published_article_evolution.py` | 本Agent v1（3分類実装済み） |

## 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| v1.0 | 2026-06-26 | 初版。3分類（Immediate Fix / Detailed Edition / No Change） |
| v1.1 | 2026-06-26 | Observation Update（観察補完）を4つ目の分類として追加。概要版/詳細解析版の役割を明文化。R02-041を Observation Update に再分類。 |
