# フレーム抽出間隔 VLM比較検証計画

**作成日：** 2026-06-25  
**ステータス：** DESIGN（未着手）  
**目的：** `extract_frames_adaptive.py` 実装前に、2秒・3秒・5秒の各間隔が映像内容の捕捉に十分かをローカルVLMで定量評価する

---

## 0. 前提・環境状況

### ローカル環境（確認済み）

| 項目 | 状態 |
|---|---|
| ollama | **未インストール** |
| LM Studio | **インストール済み**（`/Applications/LM Studio.app`）・サーバー未起動 |
| torch / transformers | **未インストール** |
| PIL | **インストール済み**（12.2.0） |
| MPS（Apple Silicon GPU） | 未確認（torch未インストールのため） |
| Qwen2.5-VL-7B | **未ダウンロード**（LM Studio経由で取得予定） |

### VLM実行経路（推奨順）

**経路A（推奨）：LM Studio + OpenAI互換API**
1. LM Studio を起動
2. Qwen2.5-VL-7B-Instruct をダウンロード（LM Studio のモデル検索から）
3. `Developer` タブでサーバー起動（`http://localhost:1234`）
4. OpenAI互換APIでマルチモーダルリクエスト送信

**経路B：ollama インストール**
```bash
brew install ollama
ollama pull qwen2.5vl:7b
ollama serve
```

**経路C（フォールバック）：Claude Vision（現行）**
本プロジェクトで既に使用中。比較ベースラインとして利用。

---

## 1. 検証の全体設計

### 目標

| 評価軸 | 質問 |
|---|---|
| **捕捉率** | 各間隔で映像内のUAP候補・主要対象をVLMが検出できるか |
| **False Negative率** | 間隔が粗いことで見落とすフレームはどの程度か |
| **コスト** | フレーム数・処理時間・ストレージとのトレードオフ |

### 評価フロー

```
[Step 1] PoC 5記事 × 3間隔 で試験抽出
          ↓
[Step 2] Qwen2.5-VL-7B で全フレームを評価
          ↓
[Step 3] 間隔ごとの「UAP候補検出率」を集計
          ↓
[Step 4] False Negative 発生条件を特定
          ↓
[Step 5] 本番50フレーム評価（必要に応じて）
          ↓
[Step 6] extract_frames_adaptive.py の仕様決定
```

---

## 2. PoC評価セット（5記事）

既公開記事から「30秒間隔で見落としリスクが高い」ものを優先選定。

| # | glob_key | 映像尺 | 現間隔 | 選定理由 |
|---|---|---|---|---|
| 1 | FBI-UAP-PR006 | 21s | **3s**（修正済み） | **既知の見落としケース**。4赤オーブが最初の抽出（1フレーム）で完全見落とし。PoC のベースライン（正解データあり） |
| 2 | DOW-UAP-PR042 | ~293s | 30s | 長尺・30s間隔の代表ケース。4分53秒映像 |
| 3 | DOW-UAP-PR044 | ~312s | 30s | 船舶形状が00:00に確認できた（フレーム追加で判明）。長尺の見落とし改善例 |
| 4 | FBI-UAP-PR001 | ~150s | 30s | 三角形オーブ（FBI映像）。30s間隔・6フレームのみ |
| 5 | DOW-UAP-PR038 | ~50s | 5s | 5s間隔・10フレームの良好ケース（比較ベースライン） |

---

## 3. 試験抽出設計（3間隔 × 5記事）

各記事に対して、2秒・3秒・5秒間隔でフレームを新規抽出し比較する。

### 出力先ディレクトリ構造

```
thumbnails_interval_test/
  2s/
    {glob_key}/frame_0000.png, frame_0002.png, ...
  3s/
    {glob_key}/frame_0000.png, frame_0003.png, ...
  5s/
    {glob_key}/frame_0000.png, frame_0005.png, ...
```

### 抽出コマンド例（ffmpeg）

```bash
# 2秒間隔
ffmpeg -i input.mp4 -vf fps=0.5 -q:v 2 thumbnails_interval_test/2s/{slug}/frame_%04d.png

# 3秒間隔
ffmpeg -i input.mp4 -vf fps=0.333 -q:v 2 thumbnails_interval_test/3s/{slug}/frame_%04d.png

# 5秒間隔
ffmpeg -i input.mp4 -vf fps=0.2 -q:v 2 thumbnails_interval_test/5s/{slug}/frame_%04d.png
```

### 想定フレーム数

| 映像 | 尺 | 2s | 3s | 5s | 現在 |
|---|---|---|---|---|---|
| FBI-PR006 | 21s | 10枚 | 7枚 | 4枚 | 8枚（3s） |
| PR042 | 293s | 146枚 | 97枚 | 58枚 | 10枚（30s） |
| PR044 | 312s | 156枚 | 104枚 | 62枚 | 10枚（30s） |
| FBI-PR001 | 150s | 75枚 | 50枚 | 30枚 | 6枚（30s） |
| PR038 | 50s | 25枚 | 16枚 | 10枚 | 10枚（5s） |
| **合計** | | **412枚** | **274枚** | **164枚** | **44枚** |

---

## 4. VLM評価プロンプト設計

### プロンプトA：UAP候補検出

```
以下の映像フレームについて、確認できる要素を列挙してください。

評価観点：
1. 白い輝点・光源（UAP候補の可能性があるもの）の有無
2. 追尾UI（シアン/赤のクロスヘア・レティクル・マーカー）の有無
3. 船舶・航空機・地上物体の有無
4. 背景の状態（空・海・地上・その他）

各項目について「確認できる / 確認できない / 不明」で回答してください。
```

### プロンプトB：アイキャッチ適性評価

```
このフレームはnote記事のアイキャッチ画像として適切ですか？

評価基準：
- 黒画面・ほぼ真っ黒ではない（5点）
- 主要な被写体が視覚的に確認できる（5点）
- 情報量がある（UAP候補・UI・地形等）（5点）

0〜15点で評価し、理由を1行で述べてください。
```

---

## 5. False Negative 測定方法

### 定義

**False Negative（FN）** = 粗い間隔では検出されなかったが、細かい間隔では検出されたUAP候補フレーム

### 測定手順

1. **正解セット（Ground Truth）作成**
   - 2秒間隔フレームのうち、VLMが「UAP候補あり」と判定したフレームセットを正解とする
   - 例：FBI-PR006の2s抽出 → 10枚中、赤オーブが映るフレームN枚 = GT

2. **各間隔のFN率計算**
   ```
   FN率 = (GTに含まれるが3s/5s間隔では抽出されなかったフレーム数) / GT総数 × 100%
   ```

3. **ケース別集計**

| 映像 | GT件数（2s） | 3s FN数 | 3s FN率 | 5s FN数 | 5s FN率 |
|---|---|---|---|---|---|
| FBI-PR006 | TBD | TBD | TBD | TBD | TBD |
| PR042 | TBD | TBD | TBD | TBD | TBD |
| PR044 | TBD | TBD | TBD | TBD | TBD |
| FBI-PR001 | TBD | TBD | TBD | TBD | TBD |
| PR038 | TBD | TBD | TBD | TBD | TBD |

### 合否判定基準（案）

| 間隔 | FN率 目標 | 判定 |
|---|---|---|
| 2s | ベースライン（0%） | 基準 |
| 3s | ≤ 10% → 採用可 | TBD |
| 5s | ≤ 20% → 短尺のみ採用 | TBD |

---

## 6. LM Studio セットアップ手順

### 6-1. Qwen2.5-VL-7B のダウンロード

1. LM Studio を起動
2. 左サイドバー「Search」タブを開く
3. 検索欄に `Qwen2.5-VL-7B-Instruct` を入力
4. GGUF版（`Q4_K_M` 推奨・約5.2GB）をダウンロード
5. 「Developer」タブ → 「Start Server」でサーバー起動
   - デフォルトポート：`http://localhost:1234`

### 6-2. 接続確認

```bash
curl -s http://localhost:1234/v1/models | python3 -m json.tool
```

### 6-3. テストリクエスト（画像あり）

```python
import base64, requests
from pathlib import Path

def encode_image(path):
    return base64.b64encode(Path(path).read_bytes()).decode()

img_b64 = encode_image("thumbnails/FBI-UAP-PR006_.../frame_0003.png")

resp = requests.post("http://localhost:1234/v1/chat/completions", json={
    "model": "qwen2.5-vl-7b-instruct",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
            {"type": "text", "text": "このフレームで確認できる光源・物体・UI要素を列挙してください。"}
        ]
    }],
    "max_tokens": 300
})
print(resp.json()["choices"][0]["message"]["content"])
```

---

## 7. 評価スクリプト構成（実装予定）

```
scripts/
  frame_interval_validator.py   # メイン評価スクリプト
  vlm_client.py                 # LM Studio API クライアント（再利用可能）

review_reports/
  frame_interval_validation_plan.md   # 本文書
  frame_interval_validation_results.md  # 評価結果（実施後）

thumbnails_interval_test/
  2s/{glob_key}/
  3s/{glob_key}/
  5s/{glob_key}/
```

### `frame_interval_validator.py` の主な処理

```python
# 擬似コード
for interval in [2, 3, 5]:
    for article in POC_ARTICLES:
        extract_frames(article.video, interval, output_dir)
        for frame in frames:
            result = vlm_evaluate(frame, PROMPT_A)
            results.append({interval, article, frame, result})

# GT作成（2s間隔を正解とする）
gt = {a: [f for f in results[2][a] if f.uap_detected] for a in POC_ARTICLES}

# FN率計算
for interval in [3, 5]:
    for article in POC_ARTICLES:
        detected = {f for f in results[interval][article] if f.uap_detected}
        fn = gt[article] - detected  # GTにあるが検出されなかったフレーム
        fn_rate = len(fn) / len(gt[article]) if gt[article] else 0
        print(f"{interval}s / {article}: FN率={fn_rate:.1%}")
```

---

## 8. extract_frames_adaptive.py 仕様への反映

VLM比較結果をもとに以下の仕様を決定する。

### 決定項目

| 項目 | 決定方法 |
|---|---|
| 短尺（< 30s）の間隔 | 3sのFN率 ≤ 5% → 3s採用、超過 → 2s採用 |
| 中尺（30s〜90s）の間隔 | 5sのFN率 ≤ 10% → 5s採用、超過 → 3s採用 |
| 長尺（90s〜360s）の間隔 | FN率の傾向から10s or 5s を決定 |
| 超長尺（> 360s）の間隔 | 長尺の結果を外挿して決定 |
| 最大フレーム数上限 | ストレージ・処理時間制約から別途決定 |
| black frame 除外閾値 | VLM評価時の輝度統計から決定 |

### 仕様書テンプレート（実施後に記入）

```python
# extract_frames_adaptive.py の間隔マッピング（TBD）
INTERVAL_MAP = {
    # (尺の下限秒, 尺の上限秒): 抽出間隔秒
    (0,    30):  X,   # TBD: 2 or 3
    (30,   90):  X,   # TBD: 3 or 5
    (90,  180):  X,   # TBD: 5 or 10
    (180, 360):  X,   # TBD: 10 or 15
    (360, 9999): X,   # TBD: 15 or 20
}
MAX_FRAMES = 50       # TBD
BLACK_THRESHOLD = 10  # TBD: 平均輝度がこの値以下なら除外
```

---

## 9. 実施手順チェックリスト

```
Phase 0: 環境準備
  ⬜ LM Studio 起動・Qwen2.5-VL-7B-Instruct (Q4_K_M) ダウンロード
  ⬜ http://localhost:1234 サーバー起動確認
  ⬜ テストリクエスト1件送信・動作確認

Phase 1: PoC 5記事 試験抽出
  ⬜ thumbnails_interval_test/ ディレクトリ作成
  ⬜ 5記事 × 3間隔 = 15ディレクトリ分を ffmpeg で抽出
  ⬜ フレーム数確認

Phase 2: VLM評価実行
  ⬜ frame_interval_validator.py 実装
  ⬜ 5記事 × 2s間隔フレーム全件評価（GT作成）
  ⬜ 5記事 × 3s/5s間隔フレーム評価
  ⬜ FN率計算・結果CSV出力

Phase 3: 結果分析・仕様決定
  ⬜ FN率テーブル作成
  ⬜ 間隔別・尺別の傾向分析
  ⬜ INTERVAL_MAP の数値決定
  ⬜ frame_interval_validation_results.md に記録

Phase 4: extract_frames_adaptive.py 仕様書確定
  ⬜ 仕様書ドラフト作成
  ⬜ ユーザーレビュー・承認
  ⬜ 実装フェーズへ移行
```

---

## 10. 留意事項

- **本計画書は設計のみ。** extract_frames_adaptive.py 実装・thumbnails/ 変更・workflow.db 変更は行わない
- **thumbnails_interval_test/ は既存の thumbnails/ とは別ディレクトリ**。既存フレームを上書きしない
- Qwen2.5-VL-7BのGGUF版はApple SiliconのMPS加速が有効。LM Studio Q4_K_M でも十分な速度が期待できる
- VLM評価の「正解」は確率的であるため、同一フレームを複数回評価して安定性を確認することが望ましい
- FBI-UAP-PR006 は正解データ（3s間隔・8フレーム・4赤オーブ確認済み）が存在するため、VLM評価精度のキャリブレーションにも活用できる

---

*関連文書：`review_reports/release02_video_quality_pause_plan.md`*
