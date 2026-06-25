# ローカルVLM候補 比較実行設計

Generated: 2026-06-25

対象評価セット:

- `data/vlm_eval_set/20260625/manifest.csv`
- `data/vlm_eval_set/20260625/manifest.json`
- `data/vlm_eval_set/20260625/README.md`
- `data/vlm_eval_set/20260625/images/`

前提:

- モデル導入はまだ行わない。
- 外部APIは使わない。LM Studio / Ollama を使う場合も `localhost` のみ。
- 元画像、manifest、`note_drafts/`、`workflow.db`、`review_logs/source_registry.csv` は変更しない。
- `run_vlm_eval.py` は評価結果を新規ディレクトリに出力するだけにする。

## 結論

最初に試すべき1モデルは **Qwen2.5-VL-7B-Instruct**。

理由:

- 7B級でMac Studio上のローカル検証に載せやすい。
- 公式モデルカードで画像理解、視覚的ローカライゼーション、JSON出力能力が明示されている。
- 小さい点・発光体の確認では万能ではないが、今回の50枚PoCの基準モデルとしてバランスがよい。
- Qwen2.5-VL-32Bを試す前に、プロンプト、JSON抽出、評価CSVの形を固められる。

推奨検証順:

1. Qwen2.5-VL-7B-Instruct
2. MiniCPM-V 2.6 または MiniCPM-V 4.x 系
3. Llama 3.2 Vision 11B
4. InternVL 8B/14B級
5. Qwen2.5-VL-32B-Instruct

## モデル候補比較

| 候補 | Mac Studio実行可否 | 想定メモリ負荷 | 導入難易度 | 速度見込み | 日本語出力 | 小さい対象物検出 |
|---|---:|---:|---:|---:|---:|---|
| Qwen2.5-VL-7B | 高い | 中。4bit量子化で概ね8-16GB級、Transformers fp16/bf16ではさらに大 | 中 | 中 | 良い | 中-高。JSON/座標出力に寄せやすい |
| MiniCPM-V | 高い | 低-中。軽量系ならMac向き | 中 | 速い | 良い | 中。高解像度知覚とOCR寄りの強み |
| Llama 3.2 Vision 11B | 高い | 中。Ollama/LM Studioで扱いやすい | 低 | 中 | 良い | 中。汎用説明は強いが微小点検出は要検証 |
| Qwen2.5-VL-32B | 条件付きで可 | 高。量子化前提、ユニファイドメモリ64GB以上推奨 | 高 | 遅い | 良い | 高候補。最終比較用 |
| InternVL系 | 条件付きで可 | モデルサイズ次第。8B級は可、26B/38B級は重い | 中-高 | 中-遅 | 良い | 中-高。視覚認識は強いが環境差が出やすい |

メモリ負荷は公式値ではなく、Mac Studioローカル実行向けの実務見積もり。画像入力ではテキストLLM単体より一時メモリが増え、解像度、視覚トークン数、コンテキスト長、量子化方式で大きく変わる。

## バックエンド方針

### Ollama

用途:

- 最速でPoCを回す。
- Llama 3.2 Vision 11B を最初に動かす場合に便利。
- モデル管理、起動、localhost APIが簡単。

利点:

- 導入が比較的容易。
- CLI/APIが安定している。
- 評価スクリプトから `ollama run` または `localhost` APIを呼びやすい。

注意:

- Qwen2.5-VLやMiniCPM-Vの対応状況はモデル配布・Modelfile依存。
- 画像入力の形式がモデルごとに揺れる可能性がある。

### LM Studio local server

用途:

- GUIでモデルを切り替えながらOpenAI互換APIで評価する。
- GGUF量子化モデルの比較に向く。

利点:

- `http://localhost:1234/v1/chat/completions` のようなOpenAI互換APIに寄せられる。
- `run_vlm_eval.py` 側のbackend実装を薄くできる。

注意:

- Vision入力対応はロードするモデルとLM Studio側の対応に依存。
- JSON厳格出力はスクリプト側で再パース・失敗記録が必要。

### transformers / mlx-vlm

用途:

- Qwen2.5-VL-7B/32B、MiniCPM-V、InternVLを本来の実装に近い形で試す。
- Mac StudioではMLX系が有力。

利点:

- Qwen2.5-VLの公式モデルカードはTransformers利用を案内している。
- `mlx-vlm` はMac上のVLM推論用パッケージで、CLI/Python/Serverが使える。

注意:

- Python環境、モデルキャッシュ、量子化モデル選定が必要。
- 32B級は速度・メモリとも重い。PoC初回には向かない。

### 任意コマンド呼び出し

用途:

- モデル固有CLIをそのまま評価に組み込む。
- 例: `mlx_vlm.generate --model ... --image {image} --prompt {prompt}`

利点:

- バックエンド追加が最小で済む。
- 研究用/暫定モデルに対応しやすい。

注意:

- stdoutからJSONを抽出する堅牢性が必要。
- タイムアウト、終了コード、stderr保存が必須。

## `scripts/run_vlm_eval.py` 仕様案

### 入力

必須:

- `--manifest data/vlm_eval_set/20260625/manifest.csv`
- `--images-dir data/vlm_eval_set/20260625/images`
- `--model <model_name>`
- `--backend <ollama|lmstudio|mlx-vlm|transformers|command>`

推奨オプション:

- `--output-dir review_reports/vlm_eval_runs/YYYYMMDD_<backend>_<model_slug>/`
- `--limit N`
- `--sample-id vlm_0001` 複数指定可
- `--category E_known_miss_case` 複数指定可
- `--temperature 0`
- `--max-tokens 512`
- `--timeout-sec 180`
- `--prompt-file prompts/vlm_eval_prompt_ja_json.txt`
- `--command-template 'mlx_vlm.generate --model ... --image {image} --prompt {prompt}'`
- `--dry-run`
- `--execute`

### 出力

評価実行ごとに新規ディレクトリを作る。

- `results.csv`
- `results.jsonl`
- `raw_outputs/<sample_id>.txt`
- `errors.csv`
- `run_config.json`
- `summary.md`

既存の `manifest.csv` や画像は変更しない。

### 処理フロー

1. manifestを読み込む。
2. `sample_id` / `category` / `limit` で対象を絞る。
3. `copied_image_path` の存在を確認する。
4. プロンプトを生成する。
5. backend別にローカル実行する。
6. stdout/API応答からJSONを抽出する。
7. JSON parse失敗時は `parse_ok=false` としてrawを保存する。
8. `results.csv` / `results.jsonl` に追記する。
9. 最後にカテゴリ別成功率、平均時間、JSON成功率を `summary.md` に書く。

### Backend I/F案

内部では共通関数に寄せる。

```python
class VlmBackend:
    def run(self, image_path: Path, prompt: str, sample: dict) -> dict:
        ...
```

戻り値:

```json
{
  "raw_text": "...",
  "parsed_json": {},
  "latency_sec": 12.3,
  "return_code": 0,
  "error": ""
}
```

## 評価プロンプト案

モデルには以下を1画像ごとに渡す。

```text
あなたはUAP動画フレームの視覚確認補助です。
画像だけから確認できることと、推測を必ず分けてください。

確認タスク:
1. 画像内にUAP候補らしき点・物体・発光体が見えるか。
2. 見える場合、位置、形状、明るさ、背景との違いを説明してください。
3. 見えない場合、見えないと明記してください。
4. センサーUI、黒塗り、クロスヘア、地形、建物、雲、海面などと対象物候補を混同しないでください。
5. 判断できない場合は「判断不能」としてください。断定しないでください。

必ず次のJSONだけを返してください。Markdownや説明文をJSON外に出さないでください。

{
  "visible_candidate": true,
  "confidence": "low|medium|high",
  "candidate_type": "point|bright_spot|dark_spot|object|light_orb|none|unknown",
  "location": {
    "relative_position": "例: center-left, lower-left, near crosshair, not visible",
    "x_percent_estimate": null,
    "y_percent_estimate": null
  },
  "visual_evidence": {
    "shape": "",
    "brightness": "",
    "contrast_with_background": "",
    "motion_inference": "single frame only; no motion can be confirmed"
  },
  "background_or_ui": {
    "sensor_ui_present": true,
    "black_redactions_present": true,
    "likely_background": ""
  },
  "uncertainty": "",
  "visual_confirmation_only": "",
  "speculation": ""
}
```

`visible_candidate` は、対象候補が視覚的に見える場合のみ `true`。ファイル名や記事メタデータからの推測だけなら `false` にする。

## 評価結果CSV形式案

`results.csv`:

| column | description |
|---|---|
| run_id | 実行ID |
| sample_id | manifestのsample_id |
| category | manifestのcategory |
| article_id | manifestのarticle_id |
| h2_number | manifestのh2_number |
| slug | manifestのslug |
| image_path | copied_image_path |
| model | モデル名 |
| backend | backend名 |
| prompt_version | プロンプト識別子 |
| started_at | ISO日時 |
| latency_sec | 推論時間 |
| parse_ok | JSON parse可否 |
| visible_candidate | JSON値 |
| confidence | JSON値 |
| candidate_type | JSON値 |
| relative_position | JSON値 |
| x_percent_estimate | JSON値 |
| y_percent_estimate | JSON値 |
| shape | JSON値 |
| brightness | JSON値 |
| contrast_with_background | JSON値 |
| sensor_ui_present | JSON値 |
| black_redactions_present | JSON値 |
| uncertainty | JSON値 |
| expected_human_label | manifestの人間ラベル |
| raw_output_path | raw出力保存先 |
| error | エラー内容 |

`results.jsonl` は同じ情報に加えて、モデル出力JSON全体とmanifest行全体を保持する。

## 最初のPoC手順

1. 実行スクリプトはまだ作らず、まずバックエンドを1つ決める。
2. 最初は `Qwen2.5-VL-7B-Instruct` を `mlx-vlm` またはTransformersで候補にする。
3. ただし環境構築を最小化したい場合は、Ollamaで `llama3.2-vision:11b` を先に1-3枚だけ動かし、評価CSV設計を検証する。
4. 最初の評価対象は `E_known_miss_case` の `vlm_0001` と、A/B/C/Dから各1枚の合計5枚。
5. JSON parse率、`visible_candidate` の妥当性、見えない場合に見えないと言えるかを確認する。
6. 問題なければ50枚全件に拡張する。

## 必要なインストール候補

導入はまだ行わない。候補のみ。

### MLX系

```bash
python3 -m venv .venv-vlm
source .venv-vlm/bin/activate
pip install -U mlx-vlm
```

想定:

```bash
mlx_vlm.generate \
  --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit \
  --image data/vlm_eval_set/20260625/images/vlm_0001_DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_2013_frame_0030.png \
  --prompt "$PROMPT" \
  --max-tokens 512 \
  --temperature 0
```

### Transformers系

```bash
python3 -m venv .venv-vlm
source .venv-vlm/bin/activate
pip install torch pillow accelerate qwen-vl-utils
pip install git+https://github.com/huggingface/transformers
```

Qwen2.5-VL公式モデルカードでは、`qwen2_5_vl` 対応のため最新Transformers、必要に応じて `qwen-vl-utils` が案内されている。

### Ollama

```bash
ollama pull llama3.2-vision:11b
```

Qwen2.5-VL系をOllamaで使う場合は、対応済み量子化モデル/Modelfileを別途確認する。

### LM Studio

LM Studio側でVision対応モデルをロードし、local serverを有効化する。評価スクリプトはOpenAI互換APIとして `localhost` にだけ投げる。

## 判断基準

最初の5枚PoCで見るべき指標:

- JSON成功率: 100%に近いこと
- `E_known_miss_case` の `frame_0030` で候補を見落とさないこと
- C/Dカテゴリで無理に対象ありとしないこと
- 推測と視覚確認を分けられること
- 日本語で短く安定して出力できること
- 1枚あたりの推論時間が運用可能な範囲に収まること

50枚全件比較の採点案:

- JSON parse成功: 1点
- 人間ラベルとの候補有無一致: 2点
- 位置説明の妥当性: 2点
- 不確実性表現の妥当性: 1点
- 過剰断定なし: 1点
- 小さい対象/既知見落とし検出: 3点
- False Negative抑制: 3点

False Negative評価では、特に以下を重く見る。

- 既知見落としケースを検出できたか。
- 見えている対象を `visible_candidate=false` として見落としていないか。
- `confidence=low` でも、人間確認に回すべき視覚的手がかりを `uncertainty` に残せているか。
- 小さい点、輝点、黒点、背景に埋もれた対象を、センサーUIや黒塗りと混同して消していないか。

## Article Revision Candidate 設計

目的:

ローカルVLMの出力JSONを、記事本文の自動修正ではなく、Claudeまたは人間が判断するための「記事修正候補レポート」に変換する。対象は、`note_drafts/` 内の既存記述とVLM結果が矛盾する可能性がある箇所に限る。

接続フロー:

```text
画像解析結果
  ↓
results.csv / results.jsonl
  ↓
article_revision_candidate.py
  ↓
Claude / 人間レビュー
  ↓
採用する修正だけ記事へ反映
```

この段階では記事本文を書き換えない。修正候補文、根拠、リスク、人間確認要否だけを出力する。

### 入力

想定入力:

- VLM `results.csv`
- VLM `results.jsonl`
- `note_drafts/*.md`
- `manifest.csv`
- `review_logs/source_registry.csv`

必須情報:

- `sample_id`
- `article_id`
- `h2_number`
- `slug`
- `image_path` または `copied_image_path`
- `draft_path`
- `visible_candidate`
- `confidence`
- `candidate_type`
- `relative_position`
- `x_percent_estimate`
- `y_percent_estimate`
- `shape`
- `brightness`
- `contrast_with_background`
- `uncertainty`
- `visual_confirmation_only`
- `speculation`

`results.jsonl` がある場合は、CSVで平坦化されていない `visual_evidence` 全体を優先して参照する。

### 出力

出力先:

```text
review_reports/article_revision_candidates_YYYYMMDD.md
```

またはrun_id単位:

```text
review_reports/article_revision_candidates_<run_id>.md
```

出力内容:

- `article_id`
- `#2番号`
- `slug`
- `draft_path`
- `sample_id`
- `frame_path`
- VLM `visible_candidate`
- VLM `confidence`
- `candidate_type`
- `location`
- `visual_evidence`
- 現在の記事中の該当文
- 修正候補文
- 修正理由
- `risk_level`
- `human_review_required`

レポート形式案:

```markdown
## R02-025 / #2_025 / DOW-UAP-PR038...

- sample_id: vlm_0001
- frame_path: data/vlm_eval_set/20260625/images/...
- VLM: visible_candidate=true / confidence=medium / candidate_type=bright_spot
- location: center-left / x=42 / y=65
- visual_evidence: small bright/dark contrast around a compact point; background is sensor imagery
- current sentence: 「映像からUAP対象物は確認できません。」
- revision candidate: 「当該フレームでは、画面中央左寄りに小さな点状の対象が確認できます。ただし、単一フレームの目視確認であり、対象の性質や移動は断定できません。」
- reason: current wording may overstate non-visibility relative to VLM visual evidence.
- risk_level: high
- human_review_required: true
```

### 判定ルール

Rule A:

- 記事が「確認できません」「明確に識別できません」「判別できません」と書いている
- かつ VLM `visible_candidate=true`
- かつ `confidence=medium` または `confidence=high`

結果:

- 修正候補を生成する。
- `risk_level=high`
- `human_review_required=true`

Rule B:

- 記事が「対象物は確認困難」「UAP対象物は確認できません」「直接確認できません」と書いている
- かつ VLM `visible_candidate=true`

結果:

- より慎重な表現への修正候補を生成する。
- `confidence=medium/high` は `risk_level=high`
- `confidence=low` は `risk_level=medium`
- `human_review_required=true`

Rule C:

- VLM `visible_candidate=false`
- かつ 記事が「確認できます」「対象が確認できます」「発光体が確認できます」など肯定的に書いている

結果:

- 人間確認候補にする。
- 自動修正候補文は弱く出す。
- `risk_level=medium`
- `human_review_required=true`

Rule D:

- VLM `confidence=low`

結果:

- 自動修正候補ではなく、確認候補にする。
- `risk_level=low` または `medium`
- `human_review_required=true`
- 修正候補文には「可能性」「判別不能」「追加確認が必要」を含める。

Rule E:

- `category=E_known_miss_case`
- かつ VLM `visible_candidate=false`

結果:

- False Negative重要候補として記録する。
- `risk_level=high`
- `human_review_required=true`
- モデル評価上は見落としとして扱う。

Rule F:

- VLM出力がJSON parse失敗、または必須フィールド欠落

結果:

- 記事修正候補は生成しない。
- VLM実行品質の問題として `parse_error` セクションへ送る。

### 修正候補生成ルール

修正候補文は必ず慎重表現にする。

禁止:

- 「UAPである」と断定する。
- ファイル名やメタデータから対象の性質を補う。
- 単一フレームから移動、速度、意図、機種を断定する。
- VLMの推測だけを本文事実として扱う。

基本テンプレート:

```text
当該フレームでは、{location}に{shape}の対象候補が確認できます。
ただし、単一フレームの視覚確認であり、対象の性質、距離、速度、移動は断定できません。
```

低信頼テンプレート:

```text
当該フレームでは、{location}に対象候補の可能性がある視覚的手がかりがあります。
ただし、背景やセンサーUIとの区別は困難であり、人間による追加確認が必要です。
```

見えない方向の確認候補テンプレート:

```text
当該フレームでは、記事中で述べている対象がVLM結果では確認されていません。
ただし、VLMの見落としの可能性があるため、元フレームの人間確認が必要です。
```

例:

変更前:

```text
映像からUAP対象物は確認できません。
```

修正候補:

```text
当該フレームでは、画面中央左寄りに小さな点状の対象が確認できます。ただし、単一フレームの目視確認であり、対象の性質や移動は断定できません。
```

### 安全制約

- 記事本文は変更しない。
- 修正候補だけ出す。
- `visible_candidate=true` でも断定しない。
- ファイル名やメタデータから推測しない。
- 視覚確認と推測を分離する。
- `confidence=low` は人間確認に回す。
- 外部APIは禁止。
- `S_CLASS` ガードを維持する。
- `note_drafts/`、`workflow.db`、`review_logs/source_registry.csv` は読み取りのみ。
- `git add` / `commit` / `push` は行わない。

### 将来実装スクリプト案

スクリプト:

```text
scripts/article_revision_candidate.py
```

想定コマンド:

```bash
python3 scripts/article_revision_candidate.py \
  --vlm-results data/vlm_runs/<run_id>/results.csv \
  --manifest data/vlm_eval_set/20260625/manifest.csv \
  --output review_reports/article_revision_candidates_<run_id>.md
```

追加オプション案:

- `--vlm-jsonl data/vlm_runs/<run_id>/results.jsonl`
- `--source-registry review_logs/source_registry.csv`
- `--draft-root note_drafts`
- `--confidence-threshold medium`
- `--include-low-confidence`
- `--sample-id vlm_0001`
- `--article-id R02-025`
- `--dry-run`
- `--execute`

`--execute` はレポート生成のみを意味する。記事本文の上書き機能は持たせない。

内部処理案:

1. `results.csv` と `manifest.csv` を `sample_id` で結合する。
2. `results.jsonl` があれば、ネストされたVLM JSONを補完する。
3. `source_registry.csv` と `workflow.db` 相当の情報で `S_CLASS` や公開状態をガードする。
4. `draft_path` の本文を読み、否定表現・肯定表現を行単位で抽出する。
5. VLM結果と本文表現を判定ルールA-Fにかける。
6. 修正候補文をテンプレート生成する。
7. `risk_level` と `human_review_required` を付与する。
8. Markdownレポートを書き出す。

`run_vlm_eval.py` との接続:

```text
scripts/run_vlm_eval.py
  -> review_reports/vlm_eval_runs/<run_id>/results.csv
  -> review_reports/vlm_eval_runs/<run_id>/results.jsonl
  -> scripts/article_revision_candidate.py
  -> review_reports/article_revision_candidates_<run_id>.md
  -> Claude / 人間レビュー
  -> 採用する修正だけ手動または別工程で記事へ反映
```

## 参考情報

- Qwen2.5-VL-7B-Instruct model card: https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct
- Qwen2.5-VL-32B-Instruct model card: https://huggingface.co/Qwen/Qwen2.5-VL-32B-Instruct
- MiniCPM-V 2.6 model card: https://huggingface.co/openbmb/MiniCPM-V-2_6
- Llama 3.2 Vision on Ollama: https://ollama.com/library/llama3.2-vision
- InternVL repository: https://github.com/OpenGVLab/InternVL
- MLX-VLM repository: https://github.com/Blaizzy/mlx-vlm
- LM Studio OpenAI compatibility docs: https://lmstudio.ai/docs/developer/openai-compat
