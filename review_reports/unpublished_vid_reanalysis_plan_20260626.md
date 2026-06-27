# 未公開VIDソース 再分析計画

- 作成日: 2026-06-26
- 対象: Release 02 未公開 VID/MP4 note_draft（#2_045 以降）
- 先行事例: PR053（#2_043・公開済み）/ PR054（#2_044・再分析完了）

---

## 1. 背景と目的

### 判明した課題

PR053 / PR054 の再分析により、以下の問題が確認された：

| 問題 | PR053 | PR054 |
|------|-------|-------|
| 30秒間隔キャプチャでは UAP 対象物を見逃す | ✅ 高速横切りを5s間隔では捉えられず | ✅ 消失・再出現・フレームアウトを30s間隔では捉えられず |
| 再生速度変更・繰り返し構成の未把握 | ✅ 3段階速度の繰り返し構成を未検出 | — |
| フレームアウトと消失の区別不能 | — | ✅ 151s付近の消失原因を特定できず |
| トリミング・ブローアップの未認識 | — | ✅ 背景変化の原因が複合的 |

### 対応方針

**#2_045 以降の未公開 VID 記事はすべて、Adaptive Frame Pipeline を通してから公開する**。
30秒間隔ベースの既存 note_draft は再分析完了まで公開しない。

---

## 2. 未公開VID 一覧（43件）

※ #2_047〜#2_050 は PDF 記事（VID対象外）のため欠番

### HIGH 優先度（36件）

60秒以上・動き系キーワード含む・30秒間隔ドラフト前提のいずれかに該当。

| 公開番号 | article_id | source_file | 尺(秒) | 30s前提 | 備考 |
|---------|-----------|-------------|--------|--------|------|
| #2_045 | R02-045 | DOW-UAP-PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds_23_Nov_2020 | 47.3 | No | in_and_out_of_clouds = 出現消失あり |
| #2_046 | R02-046 | DOW-UAP-PR056_Spherical_UAP_pulsing_over_water_CALLSIGN | 212.1 | **Yes** | pulsing = 輝度変動 |
| #2_051 | R02-051 | DOW-UAP-PR059_NAG_UAP_1_Jun_20 | 291.1 | **Yes** | 長尺 |
| #2_052 | R02-052 | DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2 | 290.4 | **Yes** | Spherical |
| #2_053 | R02-053 | DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0 | 286.4 | **Yes** | Spherical |
| #2_054 | R02-054 | DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1 | 289.6 | **Yes** | Spherical |
| #2_055 | R02-055 | DOW-UAP-PR063_Spherical_UAP_CALLSIGN_2021_04_12_vid_2 | 289.3 | **Yes** | Spherical |
| #2_057 | R02-057 | DOW-UAP-PR065_USCG_C-144_Tyndall_UAP_2_TIC_TAC_IR_hot_24_April_2024 | 39.6 | No | TIC_TAC |
| #2_058 | R02-058 | DOW-UAP-PR066_USCG_C-144_Tyndall_UAP_1_TIC_TAC_IR_hot_24_April_2024 | 48.6 | No | TIC_TAC |
| #2_059 | R02-059 | DOW-UAP-PR067_Multiple_Spherical_UAP_USO_near_Sub_CALLSIGN_2022_03_25_in_and_out_of_water | 290.4 | **Yes** | Multiple + USO + in_and_out |
| #2_060 | R02-060 | DOW-UAP-PR068_IIR_1_666_S0151_23_Video_Footage_of_UAP | 63.1 | No | FLIR/IIR |
| #2_061 | R02-061 | DOW-UAP-PR069_F_A-18_FLIR_UAP | 29.8 | No | F/A-18 FLIR |
| #2_062 | R02-062 | DOW-UAP-PR071_USAF_ANG_F-16C_Shoots_Down_UAP_Lake_Huron | 46.8 | **Yes** | 撃墜映像 |
| #2_064 | R02-064 | DOW-UAP-PR073_IIR_1_655_S0053_23_Several_UAP_Midwestern_United_States | 88.6 | No | Several UAP |
| #2_065 | R02-065 | DOW-UAP-PR074_CALLSIGN_Mission_HD_20220613 | 285.7 | **Yes** | 長尺 |
| #2_067 | R02-067 | DOW-UAP-PR076_03_January_2021_CALLSIGN_Mission_observes_UAP | 297.4 | **Yes** | observes |
| #2_068 | R02-068 | DOW-UAP-PR077_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_1_of_2 | 298.9 | **Yes** | tracks (1of2) |
| #2_069 | R02-069 | DOW-UAP-PR078_2_November_2020_CALLSIGN_Observes_and_tracks_UAP_2_of_2 | 298.6 | **Yes** | tracks (2of2) |
| #2_070 | R02-070 | DOW-UAP-PR079_29_October_2020_CALLSIGN_Mission_observes_3_fast_moving_UAPs | 240.6 | **Yes** | **3_fast_moving** |
| #2_071 | R02-071 | DOW-UAP-PR080_20_October_2020_CALLSIGN_CALLSIGN_Observes_UAP | 294.4 | **Yes** | |
| #2_072 | R02-072 | DOW-UAP-PR081_18_Oct_2020_CALLSIGN_observes_UAP_AFRICOM | 299.3 | **Yes** | |
| #2_073 | R02-073 | DOW-UAP-PR082_16_OCT_2020_CALLSIGN_views_UAP_AFRICOM | 297.1 | **Yes** | |
| #2_074 | R02-074 | DOW-UAP-PR083_7_October_2020_CALLSIGN_observes_UAP | 274.1 | **Yes** | |
| #2_075 | R02-075 | DOW-UAP-PR084（詳細確認要） | 253.8 | **Yes** | |
| #2_076 | R02-076 | DOW-UAP-PR085（詳細確認要） | 284.2 | **Yes** | |
| #2_078 | R02-078 | DOW-UAP-PR087（詳細確認要） | 294.0 | **Yes** | |
| #2_079 | R02-079 | DOW-UAP-PR088（詳細確認要） | 298.8 | **Yes** | |
| #2_080 | R02-080 | DOW-UAP-PR089（詳細確認要） | 298.5 | **Yes** | |
| #2_081 | R02-081 | DOW-UAP-PR090（詳細確認要） | 298.0 | **Yes** | |
| #2_082 | R02-082 | DOW-UAP-PR091（詳細確認要） | 288.7 | **Yes** | |
| #2_083 | R02-083 | DOW-UAP-PR092（詳細確認要） | 292.8 | **Yes** | |
| #2_085 | R02-085 | DOW-UAP-PR094（詳細確認要） | 299.8 | **Yes** | |
| #2_087 | R02-087 | DOW-UAP-PR096（詳細確認要） | 79.1 | No | |
| #2_088 | R02-088 | DOW-UAP-PR097（詳細確認要） | 299.4 | **Yes** | |
| #2_089 | R02-089 | DOW-UAP-PR099（詳細確認要） | 291.4 | **Yes** | |
| #2_090 | R02-090 | DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission | **495.5** | No | **超長尺8分超・USO Formation** |

### MEDIUM 優先度（2件）

短尺だが動き系キーワードあり、または情報不足の可能性。

| 公開番号 | article_id | source_file | 尺(秒) | 30s前提 |
|---------|-----------|-------------|--------|--------|
| #2_077 | R02-077 | DOW-UAP-PR086（詳細確認要） | 34.0 | No |
| #2_091 | R02-091 | DOW-UAP-PR070_IIR_1_655_S0301_23_Eglin_AFB_Aircrew_Observed_UAP | 30.1 | No |

### LOW 優先度（5件）

短尺（≤25秒）かつ動き系キーワード非該当。ただし内容確認後に再分類の可能性あり。

| 公開番号 | article_id | source_file | 尺(秒) | 備考 |
|---------|-----------|-------------|--------|------|
| #2_056 | R02-056 | DOW-UAP-PR064_AFSOC_Kabul_UAP_Jul_2017 | 17.7 | 17秒・Adaptive で全区間カバー可能 |
| #2_063 | R02-063 | DOW-UAP-PR072_ADMINISTRATIVE_REVISION_... | 17.3 | ADMINISTRATIVE REVISION（文書改訂）|
| #2_066 | R02-066 | DOW-UAP-PR075_09JUN2021_Platform_observed_UAP | 23.6 | 23秒 |
| #2_084 | R02-084 | DOW-UAP-PR093（尺未取得） | 不明 | ffprobe再取得要 |
| #2_086 | R02-086 | DOW-UAP-PR095（尺未取得） | 不明 | ffprobe再取得要 |

---

## 3. 再分析 Pipeline 定義（標準）

**方針更新（2026-06-27 v2）：AI Observation Report型レビューへ変更**
Human Q&A型（人間に多数の確認質問を投げる方式）を廃止。
AIが先に映像観察レポート（AI Observation Report）を生成し、
人間はソース映像を見ながら「OK / PARTIAL / WRONG / UNKNOWN」を返すだけでよい。
人間を「回答者」ではなく「査読者・編集長」として扱う。
→ 詳細は「3d. AI Observation Report 方針」および以下を参照：
  - docs/media_inspector_architecture_v2.md
  - review_reports/ai_observation_report_design_20260627.md

```
[Step 1] Adaptive Frame Extraction
  - スクリプト: scripts/extract_frames_adaptive.py --execute
  - 間隔規則: 映像尺 < 15s → 2秒間隔 / ≥ 15s → 3秒間隔
  - 出力先: data/adaptive_frames/<run_date>/<slug>/
  - thumbnails/ は変更しない

[Step 2] Frame Delta Analysis
  - スクリプト: scripts/frame_delta_analyzer.py --execute
  - 出力: data/frame_delta_runs/<run_date>/<slug>/frame_delta.csv + summary.md
  - ⚠️ ts_mode: --ts-mode seconds を必ず指定
    （フレームが秒数命名の場合、デフォルトの index では3倍ズレが発生する。
      PR056以降は --ts-mode seconds を標準とする。2026-06-27確認済み）

[Step 3] Targeted Frame Extraction（Delta 結果によりトリガー）
  - スクリプト: scripts/extract_frames_targeted.py --execute
  - トリガー: DISAPPEAR / APPEAR / REVIEW_REQUIRED / CUT(連続区間)
  - 間隔: 1.0s（--interval 1.0）
  - 出力先: data/adaptive_frames/<run_date>/<slug>_targeted/
  - 既存フレームと重複する秒はスキップ
  - ※ Targeted フレームは「人間が映像確認する際のタイムコードガイド」として使用

[Step 4] 映像確認ガイド作成（AI）
  - 出力: review_reports/<slug>_source_video_review_guide_<date>.md
  - 含める内容:
    - ソース映像ファイル名・総尺
    - 確認すべきタイムコード区間と理由
    - AI が検出した仮説（構造・構成・物体特性）
    - 人間が映像で確認すべき問い（Yes / No / 不明 で答えられる形式）
    - 代表フレーム候補（タイムスタンプ・選定理由）

[Step 5] 人間によるソース映像確認（source-video-first）
  - ソース映像を raw_media/video/ から直接再生して確認
  - ガイドのタイムコードを参照しながら映像を確認
  - AI仮説に対して「正しい／不正確／不明」を返す
  - 映像構造・センサーUI・物体特性を記述
  - 確認結果は Ground Truth として記録

[Step 6] note_draft 更新
  - 人間確認結果を反映して note_draft を更新
  - 視覚確認セクションを更新（フレーム番号ではなくタイムコード表記を推奨）
  - 代表フレームをアイキャッチに設定
  - AI解析メモ・注意点を更新
  - 断定しない表現を維持

[Step 7] VLM 解析（オプション・LM Studio 起動時）
  - スクリプト: scripts/run_vlm_on_adaptive.py --execute
  - モデル: Qwen2.5-VL-7B（ローカル）
  - 注意: 軍事UI（十字マーク・N方位マーカー等）を過検出する傾向あり
  - 人間確認完了後のオプション工程として位置づける
```

---

## 3d. AI Observation Report 方針（2026-06-27制定）

### 旧フロー（廃止）

Human Q&A型 Source Video Review Guide。PR059で14問以上の確認質問が発生し、運用負荷が高いと判断。

### 新フロー

```
Adaptive → Delta → Targeted → AI Observation Report → 人間査読（OK/PARTIAL/WRONG/UNKNOWN）→ Ground Truth → note_draft
```

### AI Observation Report の生成

- 出力先: `review_reports/<source_id>_ai_observation_report_<YYYYMMDD>.md`
- 生成タイミング: Targeted Frame Extraction 完了直後・人間確認前
- 生成方法: `scripts/generate_ai_observation_report.py`（実装中）または AI が手動で生成
- セグメント数: 1映像あたり 5〜8 セグメント（確認負荷を低く保つ）

### 人間の確認作業

1. AI Observation Report を読む（ソース映像確認前に）
2. QuickTime 等でソース映像を再生・タイムコードを確認
3. 各セグメントに「OK / PARTIAL / WRONG / UNKNOWN」を返す
4. PARTIAL / WRONG の場合は差分を簡潔に記述

→ 詳細仕様: `review_reports/ai_observation_report_design_20260627.md`

---

## 3c. タイムコード表記ルール（2026-06-27制定）

### 目的

QuickTime Player等でソース映像を確認する際、秒数だけでは確認しづらいため、
すべての映像確認用レポートで「秒数」と「分:秒」を併記する。

### 表記形式

```
【正しい形式】
7s（00:07）
95s（01:35）
219s（03:39）
273〜276s（04:33〜04:36）

【禁止形式】
7s             ← 分:秒なし
00:07          ← 秒数なし
約7秒          ← 両方なし
```

- 秒数を先に書き、括弧内に分:秒を添える
- 区間は `開始s（mm:ss）〜終了s（mm:ss）` の形式
- 1時間を超える映像は `hh:mm:ss` 形式
- 小数点以下の秒は通常省略（例：291.1s → 291s（04:51））

### 適用対象

| ドキュメント | 適用 |
|-------------|------|
| Source Video Review Guide | ✅ 必須 |
| AI Observation Report | ✅ 必須 |
| note_draft 内の重要タイムコード | ✅ 必須 |
| Frame Delta summary（機械生成） | ⬜ 将来対応（現在は秒数のみ） |
| 人間確認質問 | ✅ 必須 |
| Ground Truth 記録 | ✅ 必須 |

### 適用開始

PR059（2026-06-27）以降の新規生成レポートから適用。既存ファイルの一括修正は不要。

---

## 3b. 人間確認フロー（source-video-first）

**変更背景（2026-06-27）**

PR056・PR059の処理を通じて、静止画フレームのみによる確認の限界が明らかになった：
- UAP対象物の不規則な動き・速度変化はフレーム間隔に依存するため静止画では判断不能
- フレームイン/アウト・ブローアップ・反復再生構成は映像を通しで見ないと認識できない
- センサーUIの種別・挙動も映像の流れで確認する必要がある

**新しい役割分担**

| 要素 | 役割 |
|------|------|
| Adaptive Frame | 映像内の注目区間を発見するための索引 |
| Frame Delta Analysis | 変化の大きい区間・カット・フレームイン/アウト候補を機械的に抽出 |
| Targeted Frame | 人間が映像確認する際のタイムコードガイド |
| **ソース映像** | **人間が最終確認する本体** |
| 代表フレーム | 記事掲載用に映像確認後に選定するもの |

**確認ガイドの形式**

各PRごとに `review_reports/<slug>_source_video_review_guide_<date>.md` を作成する。
ガイドには以下を含める：
1. ソース映像ファイル名・総尺・保存パス
2. 確認すべきタイムコード区間（Delta分析で検出した重要区間）
3. AI が検出した仮説（構造・物体特性・センサーUI）
4. 人間が映像で確認すべき問い（「正しい／不正確／不明」で答えられる形式）
5. 代表フレーム候補（タイムスタンプ・選定理由）

**人間確認の出力**

確認後、ガイドファイルに直接返答を記入するか、AIとの会話で返答する。
返答は Ground Truth として `data/ground_truth/` に記録する（将来のVLM改善用）。

---

### 超長尺映像（>300秒）の追加考慮

PR052（495秒）のような超長尺は以下を追加する：

```
[Step 1a] ffprobe で章・シーン構成を確認
[Step 1b] 全体を3秒間隔で抽出後、Delta分析でシーン変化点を特定
[Step 1c] 変化点前後のみ Targeted 抽出（1秒間隔）
→ ストレージ節約のため一括抽出は避ける
```

---

## 4. 先行事例（PR053 / PR054）

### PR053 — #2_043（公開済み）

| 項目 | 内容 |
|------|------|
| 映像尺 | 21.9秒 |
| Adaptive 抽出 | 1秒間隔・22枚 |
| Delta 結果 | OBJECT_MOVE 3件（2-5s・13-14s）/ CUT 0件 |
| 発見 | 3段階速度の繰り返し構成（0-8s / 9-14s / 15-21s）/ 葉巻型暗色物体の横切り |
| 既存draftの問題 | 5秒間隔ではUAP横切りフレームを完全に見逃していた |
| 対応 | 1秒間隔22枚 → アイキャッチ7連続フレーム（16-22s）に差し替え済み |
| 公開済み URL | https://note.com/deft_ibis3303/n/n91198ae60ede |
| 残課題 | Published Article Evolution（区間境界の定量確認）|

### PR054 — #2_044（再分析完了・公開準備中）

| 項目 | 内容 |
|------|------|
| 映像尺 | 237.2秒（3分57秒）|
| Adaptive 抽出 | 3秒間隔・79枚 |
| Delta 結果 | CUT 53件 / OBJECT_MOVE 21件 / DISAPPEAR 3件 / APPEAR 1件 |
| Targeted 抽出 | 1秒間隔・62枚（4区間：60-87s / 135-168s / 177-195s / 210-225s）|
| 発見 | 輝点が151s付近で完全消失→154s再出現（フレームアウト可能性）/ 最大1014px移動 / 急激な方向転換 |
| 既存draftの問題 | 30秒間隔8フレームでは消失・再出現・不規則移動をまったく捉えられていなかった |
| 対応 | アイキャッチ差し替え（frame_00067）/ 視覚確認セクション全面更新 / 注意点追加 |
| 状態 | note_draft 更新完了・公開承認待ち |

---

## 5. 処理推奨順（公開番号順 × 優先度）

### Wave A — 即時処理対象（#2_045〜#2_055）

次の公開バッチ。11件中9件が HIGH。

| 順 | 公開番号 | source_file | 尺(秒) | 優先度 | 特記 |
|----|---------|-------------|--------|--------|------|
| 1 | **#2_044** | PR054 | 237s | — | 再分析完了・**公開可能** |
| 2 | #2_045 | PR055_Spherical_UAP_over_AFG_in_and_out_of_clouds | 47s | HIGH | 次の公開候補 |
| 3 | #2_046 | PR056_Spherical_UAP_pulsing_over_water | 212s | HIGH | pulsing = 輝度変化要確認 |
| 4 | #2_051 | PR059_NAG_UAP | 291s | HIGH | 長尺 |
| 5 | #2_052 | PR060_Spherical_UAP..._obj_2 | 290s | HIGH | 同日同機材4本連続 |
| 6 | #2_053 | PR061_Spherical_UAP..._vid_0 | 286s | HIGH | 同上 |
| 7 | #2_054 | PR062_Spherical_UAP..._vid_1 | 290s | HIGH | 同上 |
| 8 | #2_055 | PR063_Spherical_UAP..._vid_2 | 289s | HIGH | 同上 |
| 9 | #2_056 | PR064_AFSOC_Kabul_UAP | 17.7s | LOW | 短尺・簡易確認で可 |
| 10 | #2_057 | PR065_USCG_TIC_TAC_2 | 39.6s | HIGH | TIC TAC / IR |
| 11 | #2_058 | PR066_USCG_TIC_TAC_1 | 48.6s | HIGH | TIC TAC / IR |

### Wave B — 続行対象（#2_059〜#2_070）

| 順 | 公開番号 | source_file | 尺(秒) | 優先度 | 特記 |
|----|---------|-------------|--------|--------|------|
| 12 | #2_059 | PR067_Multiple_Spherical_UAP_USO | 290s | HIGH | **Multiple + USO + in_and_out_of_water** |
| 13 | #2_060 | PR068_IIR_UAP_Video | 63s | HIGH | FLIR/IIR |
| 14 | #2_061 | PR069_F/A-18_FLIR_UAP | 30s | HIGH | F/A-18 |
| 15 | #2_062 | PR071_F-16C_Shoots_Down_UAP | 47s | HIGH | **撃墜映像** |
| 16 | #2_063 | PR072_ADMINISTRATIVE_REVISION | 17s | LOW | 文書改訂系 |
| 17 | #2_064 | PR073_Several_UAP_Midwestern | 89s | HIGH | Several UAP |
| 18 | #2_065 | PR074_CALLSIGN_Mission_HD | 286s | HIGH | 長尺 |
| 19 | #2_066 | PR075_Platform_observed_UAP | 24s | LOW | 短尺 |
| 20 | #2_067 | PR076_CALLSIGN_observes_UAP | 297s | HIGH | |
| 21 | #2_068 | PR077_Observes_and_tracks_1of2 | 299s | HIGH | tracks |
| 22 | #2_069 | PR078_Observes_and_tracks_2of2 | 299s | HIGH | tracks |

### Wave C — 残件（#2_070〜#2_091）

| 公開番号 | source_file | 尺(秒) | 優先度 |
|---------|-------------|--------|--------|
| #2_070 | PR079_3_fast_moving_UAPs | 241s | HIGH / **3_fast_moving** |
| #2_071〜#2_076 | PR080-085 | 253-299s | HIGH（長尺・30s前提） |
| #2_077 | PR086 | 34s | MEDIUM |
| #2_078〜#2_083 | PR087-092 | 288-299s | HIGH（長尺・30s前提） |
| #2_084 | PR093 | 不明 | LOW（尺未取得）|
| #2_085 | PR094 | 300s | HIGH |
| #2_086 | PR095 | 不明 | LOW（尺未取得）|
| #2_087 | PR096 | 79s | HIGH |
| #2_088〜#2_089 | PR097/099 | 291-299s | HIGH |
| **#2_090** | **PR052_USO_Formation** | **495s（8分超）** | HIGH / 超長尺・別途計画 |
| #2_091 | PR070_Eglin_AFB_UAP | 30s | MEDIUM |

---

## 6. 公開再開条件

### 即時公開可能

| 記事 | 条件 |
|------|------|
| **#2_044（PR054）** | note_draft 更新済み・人間確認完了 → **即時公開可能** |

### 簡易確認で公開可能（LOW 優先度・短尺）

以下は Adaptive Frame Extraction（2秒間隔）+ 簡易目視で公開可能と判断できる可能性がある。
Delta 分析で CUT / DISAPPEAR / OBJECT_MOVE が出なければ即公開。

| 記事 | 尺 | 条件 |
|------|-----|------|
| #2_056（PR064・AFSOC Kabul）| 17.7s | Adaptive 8枚 + 目視 |
| #2_063（PR072・ADMIN REVISION）| 17.3s | Adaptive 8枚 + 目視 |
| #2_066（PR075・Platform observed）| 23.6s | Adaptive 11枚 + 目視 |

### 再分析完了後に公開（標準 Pipeline 適用）

- HIGH: Wave A → Wave B → Wave C の順で処理
- 各記事で Step 1〜5 完了後に公開
- 30秒間隔ベースの note_draft は必ず Step 6（更新）を経ること

### PR052（#2_090・495秒）

- 超長尺のため専用計画が必要
- 通常 Pipeline では処理時間・ストレージが過大になる
- 別途 `review_reports/pr052_superlong_analysis_plan.md` で計画を立てること

---

## 7. 既存 note_draft のリスク評価

### 30秒間隔前提ドラフトに共通するリスク

| リスク種別 | 説明 | 該当件数 |
|-----------|------|---------|
| 高速通過物体の見逃し | 3秒以内の通過は30秒間隔ではほぼ検出不可 | 30件以上 |
| フレームイン/アウトの未記録 | 消失と フレームアウトを区別できない | 30件以上 |
| 繰り返し再生構成の未認識 | PR053型の速度変更・反復を捉えられない | 不明（要確認）|
| トリミング/ブローアップの未記録 | 背景変化の原因が「カメラ追跡」に誤帰属される | 不明 |
| アイキャッチが不適切 | 対象物が写っていないフレームが選ばれている可能性 | 複数確認済み |

### 特に注意が必要な記事

| 記事 | リスク |
|------|--------|
| PR079（#2_070）**3_fast_moving_UAPs** | 「高速移動する3物体」→ 30秒間隔では全て見逃す可能性大 |
| PR067（#2_059）**in_and_out_of_water** | USO（水中出入り）→ 水面接触点を30秒では捉えられない可能性 |
| PR056（#2_046）**pulsing** | 輝度の点滅・脈動 → 30秒間隔では周期を捉えられない |
| PR065/PR066（#2_057/058）**TIC TAC** | TIC TAC型UAP → 特徴的な動きが30秒間隔では捉えられない |
| PR052（#2_090）**USO Formation** | 超長尺 + Formation → 多物体の位置関係が全て未把握 |

---

## 8. Ground Truth 蓄積方針

### 目的

VLM の過検出（軍事UI要素を UAP として誤検出）を補正するための人間確認コストを削減する。

### 蓄積データ構造

```
data/ground_truth/
├── ui_elements/          ← 誤検出対象（Military UI）
│   ├── n_marker.csv      ← 「N」北方位マーカーのサンプル
│   ├── crosshair.csv     ← センター十字ターゲットマーク
│   ├── black_mask.csv    ← 黒マスキング領域
│   └── corner_marker.csv ← L字コーナーマーカー
├── uap_candidates/       ← 真の UAP 候補サンプル
│   ├── confirmed_spherical.csv  ← 球形確認済み（PR054等）
│   ├── confirmed_cigar.csv      ← 葉巻型確認済み（PR053）
│   └── confirmed_frameout.csv   ← フレームアウト確認済み
└── negative/             ← UAP 候補なし確認済みフレーム
    └── confirmed_negative.csv
```

### 蓄積タイミング

| タイミング | 記録内容 |
|-----------|---------|
| 人間確認完了時 | 確認済みフレームパス・判定結果・根拠 |
| VLM 過検出を発見した時 | 誤検出フレーム・誤検出要素名 |
| 新規 UI 要素を発見した時 | 要素名・代表フレームパス・特徴 |

### 目標

- **10件以上の確認済みサンプル蓄積**後に VLM プロンプト改善を実施
- PR043〜054 の確認結果を即時登録（N方位マーカー・十字ターゲット・黒マスキングは既に複数確認済み）
- 誤検出率が 50% 以下に低下した時点で VLM 単独での一次フィルタリングを試験導入

---

## 9. 処理フロー自動化の方向性

現状は記事ごとに手動実行。以下を段階的に自動化する。

### Phase 1（現在）
- 記事ごとに手動で Step 1〜5 を実行
- summary.md を確認して人間確認対象を特定

### Phase 2（10件処理後）
- `scripts/run_vid_pipeline.py` を作成
- 1コマンドで Adaptive → Delta → Targeted まで実行
- `review_ready` フラグを設定し、人間確認待ちキューに追加

### Phase 3（Ground Truth 10件以上）
- VLM 結果と Ground Truth を突合して自動フィルタリング
- 人間確認の必要件数を削減

---

## 10. まとめ

| 指標 | 値 |
|------|-----|
| 未公開 VID note_draft 総件数 | **43件** |
| HIGH 優先度 | **36件** |
| MEDIUM 優先度 | **2件** |
| LOW 優先度 | **5件** |
| 即時公開可能 | **1件**（#2_044 / PR054）|
| 簡易確認で公開可能な候補 | **3件**（#2_056/063/066・短尺 LOW） |
| 標準 Pipeline 適用必要 | **39件** |
| 超長尺別途計画必要 | **1件**（#2_090 / PR052・495秒）|
| 欠番（PDF記事・VID対象外）| #2_047〜050（4件）|

### 次に処理すべき記事

1. **#2_044（PR054）を公開**（準備完了）
2. **#2_045（PR055・Spherical UAP over AFG・47秒）** を最初に処理
   - `in_and_out_of_clouds` = 雲への出入り → フレームアウトの可能性
   - 47秒・2秒間隔で約23枚 → 処理軽量
