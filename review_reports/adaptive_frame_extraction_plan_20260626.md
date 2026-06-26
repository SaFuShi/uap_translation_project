# Adaptive Frame Extraction PoC — 設計・dry-run レポート

- 作成日: 2026-06-26
- 更新日: 2026-06-26（v1.1 — 間隔上限を3秒に変更・10秒廃止）
- 対象: R02-043 / R02-044 / R02-045 / R02-046
- スクリプト: `scripts/extract_frames_adaptive.py`
- ステータス: dry-run 完了（修正版） / execute 未実施

---

## 0. 目的

#2_043以降の公開を停止した直接原因である「フレーム取り逃がし問題」を解消するため、
映像尺に応じた高密度・可変フレーム抽出（Adaptive Frame Extraction）を設計・検証する。

---

## 1. 既存フレーム抽出の問題点

### 使用スクリプト

`scripts/extract_frames_for_article.py`

### デフォルト設定

| パラメータ | デフォルト値 | 問題 |
|-----------|------------|------|
| `--interval` | 30秒 | 短尺映像（10〜60秒）では極端に少ないフレーム |
| `--max-frames` | 10枚 | 5分超の映像は300秒分しかカバーできない |
| 出力先 | `thumbnails/<slug>/` | 固定。再抽出すると上書きされる |

### 実際の問題事例

| 動画 | 尺 | 既存設定 | 実カバー | 問題 |
|------|-----|---------|---------|------|
| PR043 | 11.8s | 5s間隔・10枚上限 | 3枚（0/5/10s） | 全体の25%のタイムスタンプのみ |
| PR044 | 312s | 30s間隔・10枚上限 | 10枚（0〜270s） | 最後の42秒（270〜312s）が未カバー |
| PR045 | 58.8s | 5s間隔・10枚上限 | 10枚（0〜45s） | 最後の13秒（45〜58s）が未カバー |
| PR046 | 9.9s | 5s間隔・10枚上限 | 2枚（0/5s） | 全体の40%のタイムスタンプのみ |

### UAP検出観点での問題

- 光点・短時間出現・不規則な動きは「ある数秒間のみ」に発生する
- 30秒間隔では光点が現れる30秒分をまるごとスキップする可能性がある
- PR044（5分超）は10枚上限により映像後半が未解析
- VLMは渡されたフレームしか評価できず、未抽出フレームは検出不可

---

## 2. Adaptive Frame Extraction 設計

### スクリプト

`scripts/extract_frames_adaptive.py`

### Adaptive 間隔ルール（v1.1 修正）

| 動画尺 | 自動選択間隔 | 根拠 |
|--------|------------|------|
| < 15秒 | **2秒** | 超短尺。全体カバーが最優先 |
| ≥ 15秒 | **3秒** | 中〜長尺すべて。UAP取り逃がし防止 |

> **廃止**: 5秒・10秒間隔は使用しない。
> UAP候補は短時間のみ出現・不規則移動の可能性があり、10秒間隔では検出漏れリスクが高すぎる。
> 間隔の上限は3秒とする。

### 主な改善点（既存スクリプトとの差分）

| 項目 | 既存（extract_frames_for_article.py） | 新規（extract_frames_adaptive.py） |
|------|--------------------------------------|----------------------------------|
| 間隔 | 固定30秒（デフォルト） | 動画尺で自動決定 |
| 上限 | max-frames=10 | 無制限（0=unlimited） |
| 出力先 | thumbnails/<slug>/ | data/adaptive_frames/<date>/<slug>/ |
| thumbnails上書き | --force で可能 | 不可（別ディレクトリ） |
| dry-run | --dry-run フラグ | デフォルトがdry-run / --executeで実行 |
| シーン検出 | なし | --mode scene で対応（PoC） |
| 既存比較 | なし | --compare で既存thumbnailsと差分表示 |

---

## 3. PoC対象4件 — dry-run 結果

### 3-1. R02-043 / DOW-UAP-PR043（Africa 2025）

| 項目 | 値 |
|------|-----|
| 動画尺 | 11.75秒（0:11） |
| ファイルサイズ | 8.7 MB |
| 解像度 | 1920×1080 / h264 / 30fps |
| 既存間隔 | 5秒 / 3枚（frame_0000, frame_0005, frame_0010） |
| **Adaptive間隔** | **2秒（超短尺ルール）** |
| **Adaptive枚数** | **6枚**（frame_0000/0002/0004/0006/0008/0010） |
| 新規カバレッジ | +4枚（0002, 0004, 0006, 0008） |
| 既存カバー率 | 3/6枚相当 → 約50% |
| Adaptive カバー率 | 6/6枚 → **100%** |
| 出力先 | data/adaptive_frames/20260626/DOW-UAP-PR043.../ |
| **推奨方式** | ✅ **Adaptive 2秒（デフォルト）** |

**評価**: 超短尺映像のため2秒間隔で全体カバー可能。既存の5秒間隔では2・4・6・8秒が未確認。

---

### 3-2. R02-044 / DOW-UAP-PR044（Middle East 2020）

| 項目 | 値 |
|------|-----|
| 動画尺 | 312.00秒（5:12） |
| ファイルサイズ | 82.8 MB |
| 解像度 | 1920×1080 / h264 / 30fps |
| 既存間隔 | 30秒 / 10枚上限（0〜270秒、**270〜312秒未カバー**） |
| **Adaptive間隔** | **3秒（中〜長尺ルール v1.1）** |
| **Adaptive枚数** | **104枚**（frame_0000〜frame_0309） |
| 新規カバレッジ | +94枚（3/6/9/12/15/18...秒等） |
| 既存カバー率 | 10枚 / 5分超映像 → 約10時点のみ |
| Adaptive カバー率 | 104枚 → **全体を3秒精度でカバー** |
| 出力先 | data/adaptive_frames/20260626/DOW-UAP-PR044.../ |
| **推奨方式** | ✅ **Adaptive 3秒（v1.1修正後）** |

**評価**: 最も問題が大きいケース。既存30秒×10枚 → Adaptive 3秒×104枚へ。VLM処理コストは増えるが、UAP候補の取り逃がし防止が最優先。

---

### 3-3. R02-045 / DOW-UAP-PR045（Middle East 2020）

| 項目 | 値 |
|------|-----|
| 動画尺 | 58.77秒（0:58） |
| ファイルサイズ | 14.2 MB |
| 解像度 | 1920×1080 / h264 / 30fps |
| 既存間隔 | 5秒 / 10枚上限（0〜45秒、**45〜58秒未カバー**） |
| **Adaptive間隔** | **3秒（短尺ルール）** |
| **Adaptive枚数** | **20枚**（frame_0000〜frame_0057） |
| 新規カバレッジ | +16枚（3/6/9/12/18/21...秒等） |
| 既存カバー率 | 10枚（0〜45秒） → 後半13秒が空白 |
| Adaptive カバー率 | 20枚 → **全体を3秒精度でカバー** |
| 出力先 | data/adaptive_frames/20260626/DOW-UAP-PR045.../ |
| **推奨方式** | ✅ **Adaptive 3秒（デフォルト）** |

**評価**: note_draftはframe_0035（35秒付近の赤い楕円・輝点3点）を参照しているが、48〜58秒が未確認。3秒間隔で全体カバー。

---

### 3-4. R02-046 / DOW-UAP-PR046（INDOPACOM 2024）

| 項目 | 値 |
|------|-----|
| 動画尺 | 9.87秒（0:09） |
| ファイルサイズ | 2.9 MB |
| 解像度 | 1920×1080 / h264 / 30fps |
| 既存間隔 | 5秒 / 2枚（frame_0000, frame_0005） |
| **Adaptive間隔** | **2秒（超短尺ルール）** |
| **Adaptive枚数** | **5枚**（frame_0000/0002/0004/0006/0008） |
| 新規カバレッジ | +4枚（2/4/6/8秒） |
| 既存カバー率 | 2枚（0/5秒のみ） |
| Adaptive カバー率 | 5枚 → **100%カバー** |
| 出力先 | data/adaptive_frames/20260626/DOW-UAP-PR046.../ |
| **推奨方式** | ✅ **Adaptive 2秒（デフォルト）** |

**評価**: 最短動画。2枚だけでは白い翼状物体の動きを追えない。2秒間隔5枚で確認可能。

---

## 4. 全体サマリー（v1.1 修正後）

| 記事 | 尺 | 既存枚数 | Adaptive枚数 | 増加 | 推奨間隔 |
|------|-----|---------|-------------|------|---------|
| R02-043 | 11.8s | 3枚（5s） | **6枚（2s）** | +3枚 | 2秒 |
| R02-044 | 312s | 10枚（30s/上限） | **104枚（3s）** | +94枚 | 3秒 ★変更 |
| R02-045 | 58.8s | 10枚（5s/上限） | **20枚（3s）** | +10枚 | 3秒 |
| R02-046 | 9.9s | 2枚（5s） | **5枚（2s）** | +3枚 | 2秒 |
| **合計** | | **25枚** | **135枚** | **+110枚** | |

---

## 5. ストレージ負荷（v1.1 修正後）

| 項目 | 見積もり |
|------|---------|
| 1フレームあたり（1920x1080 PNG） | 約0.5〜2 MB |
| 135枚合計 | 約70〜270 MB |
| 既存 thumbnails/ への影響 | **なし**（別ディレクトリ） |
| 出力先 | `data/adaptive_frames/20260626/` |

> PR044 単体で 104枚 ≈ 50〜200 MB。`raw_media/video/` の空き容量確認を推奨。

---

## 6. VLM処理時間見込み（Qwen2.5-VL-7B @ LM Studio）（v1.1 修正後）

| 記事 | フレーム数 | 処理時間見込み（@約10秒/枚） |
|------|----------|---------------------------|
| R02-043 | 6枚 | 約1分 |
| R02-044 | **104枚** | **約17〜18分** |
| R02-045 | 20枚 | 約3〜4分 |
| R02-046 | 5枚 | 約1分 |
| **合計** | **135枚** | **約22〜24分** |

---

## 7. 推奨抽出方式（v1.1）

**全件: Adaptive固定間隔（--mode fixed）を推奨。間隔上限 3秒。**

| 方式 | 推奨度 | 理由 |
|------|--------|------|
| Adaptive固定間隔（--mode fixed, ≤3s） | ✅ 推奨 | 再現性が高い。UAP取り逃がし防止。thumbnails/ を汚染しない |
| シーン変化検出（--mode scene） | 参考 | PoC用途。再現性が低く、閾値チューニングが必要 |
| 既存10秒固定 | ❌ 廃止 | 長尺でもUAP候補を取り逃がす |
| 既存30秒固定 | ❌ 非推奨 | 短尺・長尺ともに問題あり |

---

## 8. #2_043以降 公開再開条件

| 条件 | 必須/推奨 | ステータス |
|------|---------|----------|
| Adaptive Frame Extraction dry-run 確認 | 必須 | ✅ 完了（本レポート） |
| execute 実施・フレーム生成 | 必須 | ⬜ 未実施 |
| VLM評価（Media Inspector）実施 | 必須 | ⬜ 未実施 |
| Article Revision Candidate 確認 | 必須 | ⬜ 未実施 |
| 人間目視確認（代表フレーム） | 必須 | ⬜ 未実施 |
| note_draft更新（必要な場合） | 必須 | ⬜ 未実施 |
| Published Article Evolution 記録 | 推奨 | ⬜ 未実施 |

---

## 9. execute コマンド（承認後に実行）

```bash
# R02-043
python3 scripts/extract_frames_adaptive.py \
  --input "raw_media/video/DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025.mp4" \
  --slug DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025 \
  --run-date 20260626 --execute

# R02-044
python3 scripts/extract_frames_adaptive.py \
  --input "raw_media/video/DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020.mp4" \
  --slug DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_2020 \
  --run-date 20260626 --execute

# R02-045
python3 scripts/extract_frames_adaptive.py \
  --input "raw_media/video/DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020.mp4" \
  --slug DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_2020 \
  --run-date 20260626 --execute

# R02-046
python3 scripts/extract_frames_adaptive.py \
  --input "raw_media/video/DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024.mp4" \
  --slug DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024 \
  --run-date 20260626 --execute
```

---

## 関連ファイル

| ファイル | 役割 |
|---------|------|
| `scripts/extract_frames_for_article.py` | 既存の30秒間隔抽出スクリプト |
| `scripts/extract_frames_adaptive.py` | 今回実装（Adaptive版） |
| `scripts/media_inspector.py` | VLM評価スクリプト |
| `docs/published_article_evolution_agent_v1.md` | Evolution設計書 |
| `thumbnails/DOW-UAP-PR04{3-6}_*/` | 既存フレーム（上書きしない） |
| `data/adaptive_frames/20260626/` | Adaptive抽出先（execute後に生成） |
