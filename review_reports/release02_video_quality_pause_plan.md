# Release 02 動画記事 品質監査・公開停止計画書

**作成日：** 2026-06-25  
**ステータス：** ACTIVE（公開停止中）

---

## 1. 公開停止理由

### 直接のトリガー
FBI-UAP-PR006（#2_042）において、当初ドラフトがフレーム抽出不足により映像の実際の内容（4つの赤い光源が夜空を右から左へ移動するCG映像）を完全に見落とし、「冒頭は黒い画面・内容確認困難」という誤った記述になっていた。

ユーザーが実映像を確認し、記述の不正確さを発見。ドラフトを全面書き直しの上、note公開後に判明。

### 構造的な問題

1. **フレーム抽出間隔が粗すぎる**  
   長尺映像（約5分）に対して30秒間隔・10フレームのみ。映像内でUAP対象が5〜10秒しか映らない場合に完全見落としが発生しうる。

2. **frame_0000依存のリスク**  
   デフォルトのアイキャッチ推奨が `frame_0005` または `frame_0000` に集中しており、映像開始直後がフェードイン・黒画面の場合にアイキャッチとして不適切。

3. **一括修正による記述不整合**  
   過去セッションで約26記事を一括修正した際、代表フレーム変更・キャプション変更・要点・注意点・掲載画像出典の間に部分的な不整合が残存している可能性がある。

4. **短尺・長尺でフレーム間隔が不統一**  
   短尺（< 60s）は5秒間隔、長尺（270〜300s）は30秒間隔と設計が混在。品質基準が存在しない。

---

## 2. 公開済み範囲（停止時点）

| カテゴリ | 内容 |
|---|---|
| 公開済み件数 | **38件** |
| publish_order範囲 | 2000〜2042（intro + 3文書記事 + 34動画記事） |
| 動画記事範囲 | #2_010〜#2_042（po=2010〜2042、計33件） |
| 最終公開記事 | #2_042 / FBI-UAP-PR006（2026-06-25） |

### 公開済み記事一覧

| # | publish_order | slug（先頭50文字） |
|---|---|---|
| 1 | 2000 | release02_intro |
| 2 | 2001 | ODNI-UAP-D001_usper_narrative_senior_usic |
| 3 | 2002 | CIA-UAP-D001_intelligence_information_report_ussr |
| 4 | 2003 | DOW-UAP-D017_general_correspondence_sandia |
| 5 | 2010 | DOW-UAP-PR019_Unresolved_UAP_Report_Middle_East_Ma |
| 6 | 2011 | DOW-UAP-PR021_Unresolved_UAP_Report_Iraq_May_2022 |
| 7 | 2012 | DOW-UAP-PR022_Unresolved_UAP_Report_Syria_July_202 |
| 8 | 2013 | DOW-UAP-PR023_Unresolved_UAP_Report_Iraq_December |
| 9 | 2014 | DOW-UAP-PR026_Unresolved_UAP_Report_United_Arab_Em |
| 10 | 2015 | DOW-UAP-PR027_Unresolved_UAP_Report_United_Arab_Em |
| 11 | 2016 | DOW-UAP-PR028_Unresolved_UAP_Report_Greece_January |
| 12 | 2017 | DOW-UAP-PR029_Unresolved_UAP_Report_United_Arab_Em |
| 13 | 2018 | DOW-UAP-PR031_Unresolved_UAP_Report_Syria_October |
| 14 | 2019 | DOW-UAP-PR032_Unresolved_UAP_Report_Syria_October |
| 15 | 2020 | DOW-UAP-PR033_Unresolved_UAP_Report_Syria_October |
| 16 | 2021 | DOW-UAP-PR034_Unresolved_UAP_Report_Greece_October |
| 17 | 2022 | DOW-UAP-PR035_Unresolved_UAP_Report_Greece_October |
| 18 | 2023 | DOW-UAP-PR036_Unresolved_UAP_Report_Middle_East_Ma |
| 19 | 2024 | DOW-UAP-PR037_Unresolved_UAP_Report_Middle_East_20 |
| 20 | 2025 | DOW-UAP-PR038_Unresolved_UAP_Report_Middle_East_20 |
| 21 | 2026 | DOW-UAP-PR039_Unresolved_UAP_Report_Middle_East_20 |
| 22 | 2027 | DOW-UAP-PR040_Unresolved_UAP_Report_Middle_East_20 |
| 23 | 2028 | DOW-UAP-PR041_Unresolved_UAP_Report_Middle_East_20 |
| 24 | 2029 | DOW-UAP-PR042_Unresolved_UAP_Report_Middle_East_20 |
| 25 | 2030 | DOW-UAP-PR043_Unresolved_UAP_Report_Africa_2025 |
| 26 | 2031 | DOW-UAP-PR044_Unresolved_UAP_Report_Middle_East_20 |
| 27 | 2032 | DOW-UAP-PR045_Unresolved_UAP_Report_Middle_East_20 |
| 28 | 2033 | DOW-UAP-PR046_Unresolved_UAP_Report_INDOPACOM_2024 |
| 29 | 2034 | DOW-UAP-PR047_Unresolved_UAP_Report_INDOPACOM_2023 |
| 30 | 2035 | DOW-UAP-PR048_Unresolved_UAP_Report_INDOPACOM_2024 |
| 31 | 2036 | DOW-UAP-PR049_Unresolved_UAP_Report_Department_of_ |
| 32 | 2037 | FBI-UAP-PR001_Triangle_Orbs_Northeastern_United_St |
| 33 | 2038 | FBI-UAP-PR002_Red_Orb_Rotation_Northeastern_United |
| 34 | 2039 | FBI-UAP-PR003_Orbs_Over_the_Pond_2024 |
| 35 | 2040 | FBI-UAP-PR004_Northeastern_Orb_Sighting_2025 |
| 36 | 2041 | FBI-UAP-PR005_Digital_Recreation_Narrative_Stateme |
| 37 | 2042 | FBI-UAP-PR006_Digital_Recreation_Narrative_Stateme |

---

## 3. 未公開・再監査対象（45件）

| # | publish_order | glob_key | 現フレーム数 | 現間隔 | 映像尺（推定） |
|---|---|---|---|---|---|
| 1 | 2043 | DOW-UAP-PR053 | 5 | 5s | ~25s |
| 2 | 2044 | DOW-UAP-PR054 | 8 | 30s | ~210s |
| 3 | 2045 | DOW-UAP-PR055 | 10 | 5s | ~45s |
| 4 | 2046 | DOW-UAP-PR056 | 8 | 30s | ~210s |
| 5 | 2051 | DOW-UAP-PR059 | 10 | 30s | ~270s |
| 6 | 2052 | DOW-UAP-PR060 | 10 | 30s | ~270s |
| 7 | 2053 | DOW-UAP-PR061 | 10 | 30s | ~270s |
| 8 | 2054 | DOW-UAP-PR062 | 10 | 30s | ~270s |
| 9 | 2055 | DOW-UAP-PR063 | 10 | 30s | ~270s |
| 10 | 2056 | DOW-UAP-PR064 | 4 | 5s | ~15s |
| 11 | 2057 | DOW-UAP-PR065 | 8 | 5s | ~35s |
| 12 | 2058 | DOW-UAP-PR066 | 10 | 5s | ~45s |
| 13 | 2059 | DOW-UAP-PR067 | 10 | 30s | ~270s |
| 14 | 2060 | DOW-UAP-PR068 | 10 | 5s | ~45s |
| 15 | 2061 | DOW-UAP-PR069 | 6 | 5s | ~25s |
| 16 | 2062 | DOW-UAP-PR071 | 10 | 5s | ~45s |
| 17 | 2063 | DOW-UAP-PR072 | 4 | 5s | ~15s |
| 18 | 2064 | DOW-UAP-PR073 | 3 | 30s | ~60s |
| 19 | 2065 | DOW-UAP-PR074 | 10 | 30s | ~270s |
| 20 | 2066 | DOW-UAP-PR075 | 5 | 5s | ~20s |
| 21 | 2067 | DOW-UAP-PR076 | 10 | 30s | ~270s |
| 22 | 2068 | DOW-UAP-PR077 | 10 | 30s | ~270s |
| 23 | 2069 | DOW-UAP-PR078 | 10 | 30s | ~270s |
| 24 | 2070 | DOW-UAP-PR079 | 9 | 30s | ~240s |
| 25 | 2071 | DOW-UAP-PR080 | 10 | 30s | ~270s |
| 26 | 2072 | DOW-UAP-PR081 | 10 | 30s | ~270s |
| 27 | 2073 | DOW-UAP-PR082 | 10 | 30s | ~270s |
| 28 | 2074 | DOW-UAP-PR083 | 10 | 30s | ~270s |
| 29 | 2075 | DOW-UAP-PR084 | 9 | 30s | ~240s |
| 30 | 2076 | DOW-UAP-PR085 | 10 | 30s | ~270s |
| 31 | 2077 | DOW-UAP-PR086 | 7 | 5s | ~30s |
| 32 | 2078 | DOW-UAP-PR087 | 10 | 30s | ~270s |
| 33 | 2079 | DOW-UAP-PR088 | 10 | 30s | ~270s |
| 34 | 2080 | DOW-UAP-PR089 | 10 | 30s | ~270s |
| 35 | 2081 | DOW-UAP-PR090 | 10 | 30s | ~270s |
| 36 | 2082 | DOW-UAP-PR091 | 10 | 30s | ~270s |
| 37 | 2083 | DOW-UAP-PR092 | 10 | 30s | ~270s |
| 38 | 2084 | DOW-UAP-PR093 | 7 | 5s | ~30s |
| 39 | 2085 | DOW-UAP-PR094 | 10 | 30s | ~270s |
| 40 | 2086 | DOW-UAP-PR095 | 10 | 30s | ~270s |
| 41 | 2087 | DOW-UAP-PR096 | 3 | 30s | ~60s |
| 42 | 2088 | DOW-UAP-PR097 | 10 | 30s | ~270s |
| 43 | 2089 | DOW-UAP-PR099 | 10 | 30s | ~270s |
| 44 | 2090 | DOW-UAP-PR052 | 9 | 60s | ~480s |
| 45 | 2091 | DOW-UAP-PR070 | 7 | 5s | ~30s |

**高リスク（30秒以上間隔）：30件**  
**超長尺（PR052・480s以上、60s間隔）：1件**  
**フレーム数3以下：2件（PR073・PR096）**

---

## 4. 現在の問題点まとめ

### 4-1. フレーム抽出の問題

| 問題 | 詳細 |
|---|---|
| 30秒間隔・長尺映像 | 5分映像でフレーム10枚。10秒以内の出来事は完全見落とし |
| frame_0000の黒画面リスク | フェードイン・黒画面フレームがアイキャッチになるケースあり（PR006で発生） |
| 最大間隔が統一されていない | 5s・30s・60sが混在。品質基準なし |
| 短尺映像への過剰抽出 | 15秒の映像に5秒間隔×3フレームは妥当だが、基準として明文化されていない |

### 4-2. ドラフト記述の不整合リスク

| リスク箇所 | 内容 |
|---|---|
| 代表フレーム変更時の掲載画像出典 | フレーム番号・タイムスタンプが旧フレームのまま残存する可能性 |
| 要点と代表フレームの乖離 | 要点がframe_0030を説明しているが代表フレームがframe_0060に変更されたケース等 |
| 注意点の旧記述残存 | 一括修正で注意点のみ更新漏れのケース |
| キャプションのタイムスタンプ不一致 | `▲ (MM:SS)` のタイムスタンプがファイル名のframe番号と不一致 |

---

## 5. フレーム抽出改善案

### 案A：映像尺に応じた可変間隔（推奨）

| 映像尺 | 抽出間隔 | フレーム数（目安） |
|---|---|---|
| ≤ 30s | 2s | 最大15枚 |
| 31s〜90s | 3s | 10〜30枚 |
| 91s〜180s | 5s | 18〜36枚 |
| 181s〜360s | 10s | 18〜36枚 |
| > 360s | 15s | 最大32枚 |

**メリット：** UAP出現期間が短くても捕捉率が大幅向上  
**デメリット：** ディスク使用量・処理時間が増加（最大3〜4倍）

### 案B：固定2秒間隔（全映像統一）

全映像を2秒間隔で抽出。

**メリット：** 設計シンプル・最高の捕捉率  
**デメリット：** 300秒映像で150枚。ストレージ負荷大。VLM処理コスト増

### 案C：シーン変化検出（ffmpeg scene detect）

ffmpegの `-vf select='gt(scene,0.3)'` を使用しシーン変化フレームのみ抽出。

**メリット：** 内容変化点を自動検出・効率的  
**デメリット：** 閾値チューニングが必要。IR映像（低コントラスト・緩やかな変化）ではシーン変化が検出されにくい可能性が高い。

### 案D：案Aの可変間隔 ＋ 案Cのシーン変化検出の併用（推奨）

- まず案Aの可変間隔でフレームを抽出
- 追加で `scene>0.4` のフレームを補完抽出
- 重複フレームを除去

**結論：案Dを推奨。ただしまず案Aを実装し、シーン検出は後続フェーズで追加。**

---

## 6. Media Inspector Agent 改善案

### 現状の問題
- フレームが粗い段階でVLM解析を行っているため、見落としが発生
- アイキャッチ推奨ロジックが「最初のフレームに近いもの」に偏っている

### 改善項目

| 項目 | 内容 |
|---|---|
| フレーム抽出前の尺チェック | `ffprobe` で尺を取得し案Aの間隔を自動選択 |
| アイキャッチ候補スコアリング | UAP候補（輝点・追尾レティクル・船舶形状）が含まれるフレームを優先 |
| black frame 除外 | 平均輝度が閾値以下のフレームをアイキャッチ候補から除外 |
| 複数フレーム比較出力 | 最良候補3〜5枚を提示し人間が選択する形式に |
| タイムスタンプ自動計算 | `frame_NNNN` のNNNNを秒に変換してキャプション用タイムスタンプを生成 |

---

## 7. ローカルVLM比較の次手順

### 目的
Claude Vision の解析結果をローカルVLM（LLaVA / Qwen-VL 等）と比較し、UAP候補の検出精度を検証する。

### 手順案

1. **環境確認**：`ollama list` でローカルVLMの利用可能モデルを確認
2. **比較対象選定**：既公開記事の代表フレーム10件を選定
3. **プロンプト統一**：「この映像フレームに確認できる物体・UI要素を列挙してください」
4. **結果比較**：Claude解析結果 vs ローカルVLM結果のdiffを作成
5. **精度評価**：UAP候補（輝点・追尾レティクル・船舶等）の検出精度を評価
6. **次フェーズ決定**：精度差が大きい場合はローカルVLMをセカンドオピニオンとして活用

---

## 8. Article Revision Candidate 実装計画

### 目的
既公開記事（#2_010〜#2_042）のドラフトと published_articles を対象に、記述不整合を自動検出・修正候補を生成するスクリプト。

### 実装順

**Phase 1（優先）：不整合検出**
- `scripts/article_revision_checker.py` の実装
- チェック項目：
  - `▼ 代表フレーム` のファイル名 vs `掲載画像：` のファイル名が一致するか
  - `▲ (MM:SS)` のタイムスタンプ vs ファイル名の秒数が一致するか
  - `掲載画像出典` のタイムスタンプ vs 代表フレームのファイル名が一致するか
  - `要点` 内のフレーム番号言及 vs 代表フレームが一致するか

**Phase 2：修正候補生成**
- 不整合箇所を `revision_candidates/` に出力
- 人間がレビューして承認後に適用

**Phase 3：未公開記事への事前適用**
- #2_043以降のドラフトを公開前に自動チェック
- 不整合があれば公開ブロック

---

## 9. 公開再開条件

以下をすべて満たした時点で公開再開可能とする。

| 条件 | ステータス |
|---|---|
| **C1** フレーム抽出改善（案A実装）完了 | ⬜ 未着手 |
| **C2** #2_043〜#2_046（次の4記事）を改善フレームで再抽出・ドラフト確認 | ⬜ 未着手 |
| **C3** Article Revision Checker Phase 1 実装 | ⬜ 未着手 |
| **C4** 未公開45件のドラフト不整合チェック完了（自動または目視） | ⬜ 未着手 |
| **C5** ユーザーによる公開再開承認 | ⬜ 未着手 |

---

## 10. 次の作業順（推奨）

```
STEP 1：フレーム抽出改善スクリプト実装（案A・可変間隔）
  → scripts/extract_frames_adaptive.py

STEP 2：高リスク未公開記事（30s間隔・長尺30件）の再抽出
  → 優先：#2_043（PR053）〜#2_046（PR056）の4件を試験的に再抽出・比較

STEP 3：Article Revision Checker Phase 1 実装
  → scripts/article_revision_checker.py

STEP 4：未公開45件のドラフト自動チェック → 不整合リスト作成

STEP 5：ユーザーによるレビュー・承認

STEP 6：公開再開（#2_043から順次）
```

---

*本文書は設計・停止判断の記録のみ。workflow.db / source_registry.csv / note公開への変更なし。*
