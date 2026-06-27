# AI Observation Report: DOW-UAP-PR059_NAG_UAP_1_Jun_20

## メタデータ

- source_id: DOW-UAP-PR059_NAG_UAP_1_Jun_20
- article_id: R02-051
- source_video_path: raw_media/video/DOW-UAP-PR059_NAG_UAP_1_Jun_20.mp4
- duration: 291s（04:51）
- run_date: 20260627
- 生成スクリプト: scripts/generate_ai_observation_report.py
- pipeline_steps:
  - adaptive_frames: data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20
  - delta_analysis: data/frame_delta_runs/20260626/DOW-UAP-PR059_NAG_UAP_1_Jun_20/summary.md
  - targeted_frames: data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20_targeted
  - vlm_output: 未実施

---

## 観察サマリー

Delta分析全体では APPEAR 4件・DISAPPEAR 9件・CUT 8件・OBJECT_MOVE 25件・STATIC 40件（低変化区間） を検出した。映像を 5 セグメントに分割して観察する。各セグメントの詳細はソース映像の確認で確定する。

---

## 重要セグメント

### セグメント A: 0s（00:00）〜58s（00:58）

**概要タグ:** APPEAR（bc_max=4,887） / DISAPPEAR×5 / OBJECT_MOVE×6 / REVIEW_REQUIRED×5

**AI観察:**
0s（00:00）→3s（00:03）で輝点（bc=4,887）の出現を検出した。
9s（00:09）→12s（00:12）で中程度の輝点（bc=354）の出現を検出した。
3s（00:03）→6s（00:06）で輝点の急激な減少（bc: 4,887→95）を検出した。
6s（00:06）→9s（00:09）で輝点の消失を検出した（bc: 95→0）。
18s（00:18）→21s（00:21）で輝点の急激な減少（bc: 598→136）を検出した。
33s（00:33）→36s（00:36）で輝点の急激な減少（bc: 2,442→63）を検出した。
45s（00:45）→48s（00:48）で輝点の急激な減少（bc: 3,181→72）を検出した。
APPEAR と DISAPPEAR が短時間に複数回発生しており、センサーの露出変化（ホワイトアウト・露出補正）による誤検出の可能性がある。ソース映像での確認を推奨する。

**確信度:** medium
（Delta分析で高bc値のAPPEAR/DISAPPEARを検出。ソース映像確認後に high に昇格可能）

**根拠:**
- Adaptive frame: frame_0000.png, frame_0003.png, frame_0006.png 他 20枚
- Delta result: APPEAR（bc=4,887@3s（00:03）, bc=354@12s（00:12））; DISAPPEAR（bc_prev=4,887→95@6s（00:06）, bc_prev=95→0@9s（00:09）, bc_prev=598→136@21s（00:21））; OBJECT_MOVE×6件; STATIC×2件
- Targeted frame: frame_00000.png, frame_00001.png, frame_00002.png 他 53枚 （data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20_targeted/）
- VLM output: 未実施
- Filename metadata: ソースIDのみ参照

**リスクフラグ:**
- ui_misidentification: none
- trimming_effect: none
- blowup_effect: none
- speed_change: none
- frameout_misidentification: medium（9s（00:09）のDISAPPEAR（bc→0）→フレームアウトと露出消失の区別困難）
- exposure_change: medium（3s（00:03）でbc=0→4,887の急騰→ホワイトアウトの可能性）
- compression_artifact: none

**人間確認:**
- [ ] OK — AIの観察は正しい
- [ ] PARTIAL — 一部修正が必要（以下に記述）
- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

### セグメント B: 58s（00:58）〜93s（01:33）

**概要タグ:** DISAPPEAR×2 / OBJECT_MOVE×3 / REVIEW_REQUIRED×4

**AI観察:**
69s（01:09）→72s（01:12）で輝点の急激な減少（bc: 742→60）を検出した。
87s（01:27）→90s（01:30）で輝点の急激な減少（bc: 987→67）を検出した。

**確信度:** low
（REVIEW_REQUIRED×4件→自動判定困難。ソース映像確認が必要）

**根拠:**
- Adaptive frame: frame_0060.png, frame_0063.png, frame_0066.png 他 12枚
- Delta result: DISAPPEAR（bc_prev=742→60@72s（01:12）, bc_prev=987→67@90s（01:30））; OBJECT_MOVE×3件; STATIC×3件
- Targeted frame: frame_00059.png, frame_00061.png, frame_00062.png 他 31枚 （data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20_targeted/）
- VLM output: 未実施
- Filename metadata: ソースIDのみ参照

**リスクフラグ:**
- ui_misidentification: none
- trimming_effect: none
- blowup_effect: none
- speed_change: none
- frameout_misidentification: none
- exposure_change: none
- compression_artifact: none

**人間確認:**
- [ ] OK — AIの観察は正しい
- [ ] PARTIAL — 一部修正が必要（以下に記述）
- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

### セグメント C: 99s（01:39）〜138s（02:18）

**概要タグ:** STATIC×13（低変化区間）

**AI観察:**
この区間（約39秒間）はDelta変化量が少ない状態が続いた（STATIC×13件）。
映像が静止しているか、対象物が画面内で極めてゆっくり移動している可能性がある。
区間内の実際の内容はソース映像の確認まで不明。

**確信度:** medium
（STATIC×13件→変化が少ない状態は確実。内容は不明）

**根拠:**
- Adaptive frame: frame_0099.png, frame_0102.png, frame_0105.png 他 14枚
- Delta result: STATIC×13件
- Targeted frame: data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20_targeted/ （範囲内フレームなし）
- VLM output: 未実施
- Filename metadata: ソースIDのみ参照

**リスクフラグ:**
- ui_misidentification: none
- trimming_effect: none
- blowup_effect: low（STATIC×13件の長期区間→ブローアップによる解像度低下の可能性）
- speed_change: none
- frameout_misidentification: none
- exposure_change: none
- compression_artifact: none

**人間確認:**
- [ ] OK — AIの観察は正しい
- [ ] PARTIAL — 一部修正が必要（以下に記述）
- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

### セグメント D: 138s（02:18）〜213s（03:33）

**概要タグ:** OBJECT_MOVE×9 / REVIEW_REQUIRED×1 / STATIC×15（低変化区間）

**AI観察:**
この区間（約75秒間）はDelta変化量が少ない状態が続いた（STATIC×15件）。
映像が静止しているか、対象物が画面内で極めてゆっくり移動している可能性がある。
区間内の実際の内容はソース映像の確認まで不明。

**確信度:** medium
（STATIC×15件→変化が少ない状態は確実。内容は不明）

**根拠:**
- Adaptive frame: frame_0138.png, frame_0141.png, frame_0144.png 他 26枚
- Delta result: OBJECT_MOVE×9件; STATIC×15件
- Targeted frame: frame_00162.png, frame_00163.png, frame_00164.png 他 17枚 （data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20_targeted/）
- VLM output: 未実施
- Filename metadata: ソースIDのみ参照

**リスクフラグ:**
- ui_misidentification: none
- trimming_effect: none
- blowup_effect: low（STATIC×15件の長期区間→ブローアップによる解像度低下の可能性）
- speed_change: none
- frameout_misidentification: none
- exposure_change: none
- compression_artifact: none

**人間確認:**
- [ ] OK — AIの観察は正しい
- [ ] PARTIAL — 一部修正が必要（以下に記述）
- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

### セグメント E: 213s（03:33）〜294s（04:54）

**概要タグ:** APPEAR（bc_max=9,937） / DISAPPEAR×2 / CUT×8（max_diff=105.7） / OBJECT_MOVE×7 / STATIC×7（低変化区間）

**AI観察:**
この区間で8回のシーン急変（CUT）を検出した（222s（03:42）〜288s（04:48）、mean_diff: 54.5, 105.7, 36.8）。
レンズの切り替え（FOV変更）または映像の編集点の可能性がある。
219s（03:39）付近で輝度の完全消失（bc→0）を検出しており、対象物がフレームアウトした直後にレンズが切り替わった可能性がある。
234s（03:54）付近で輝点の再出現（bc=9,937）を検出した。
291s（04:51）付近で輝点の再出現（bc=7,643）を検出した。

**確信度:** medium
（Delta分析で高bc値のAPPEAR/DISAPPEARを検出。ソース映像確認後に high に昇格可能）

**根拠:**
- Adaptive frame: frame_0213.png, frame_0216.png, frame_0219.png 他 27枚
- Delta result: APPEAR（bc=9,937@234s（03:54）, bc=7,643@291s（04:51））; DISAPPEAR（bc_prev=4,930→0@219s（03:39）, bc_prev=5,307→0@276s（04:36））; CUT（mean_diff=54.5@222s（03:42）, mean_diff=105.7@225s（03:45）, mean_diff=36.8@228s（03:48））; OBJECT_MOVE×7件; STATIC×7件
- Targeted frame: frame_00214.png, frame_00215.png, frame_00216.png 他 49枚 （data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20_targeted/）
- VLM output: 未実施
- Filename metadata: ソースIDのみ参照

**リスクフラグ:**
- ui_misidentification: none
- trimming_effect: medium（8回のCUT→レンズ切り替えまたはトリミング変化の可能性）
- blowup_effect: none
- speed_change: none
- frameout_misidentification: medium（219s（03:39）のDISAPPEAR（bc→0）→フレームアウトと露出消失の区別困難）
- exposure_change: high（CUT（222s（03:42）付近）の前後にAPPEAR/DISAPPEARが発生→露出変化の可能性）
- compression_artifact: none

**人間確認:**
- [ ] OK — AIの観察は正しい
- [ ] PARTIAL — 一部修正が必要（以下に記述）
- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

## note_draft 反映候補

| セグメント | note_draft 反映案 | 確信度 | 人間確認後に反映 |
|-----------|-----------------|--------|----------------|
| A | 「3s（00:03）付近で強い輝点（推定bc≈4,887）が検出された」 | medium | （人間確認待ち） |
| B | 「この区間で対象物の継続的な移動を検出（最大352px、75s（01:15）付近）」 | low | （人間確認待ち） |
| C | 「この区間（約39秒）は対象物の大きな動きなし（STATIC）」 | medium | （人間確認待ち） |
| D | 「この区間（約75秒）で対象物の緩やかな移動を継続検出（OBJECT_MOVE×9件）」 | medium | （人間確認待ち） |
| E | 「234s（03:54）付近で強い輝点（推定bc≈9,937）が検出された」 | medium | （人間確認待ち） |

---

## 代表フレーム候補

| セグメント | フレーム | タイムスタンプ | 選定理由 | 優先度 |
|-----------|---------|-------------|---------|--------|
| A | data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20_targeted/frame_00003.png | 3s（00:03） | APPEAR bc=4,887（セグメントAで最大輝度） | 高 |
| B | data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20_targeted/frame_00075.png | 75s（01:15） | OBJECT_MOVE pos_delta=352px | 中 |
| C | data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20/frame_0117.png | 118s（01:58） | 区間中央フレーム（顕著なイベントなし） | 低 |
| D | data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20_targeted/frame_00176.png | 176s（02:56） | 区間中央フレーム（顕著なイベントなし） | 低 |
| E | data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20_targeted/frame_00234.png | 234s（03:54） | APPEAR bc=9,937（セグメントEで最大輝度） | 高 |

**→ 代表フレーム確定:** （人間確認後に記入）

---

## 人間確認フロー

1. このレポートを通読する
2. QuickTime（または任意のプレイヤー）でソース映像を開く
   `raw_media/video/DOW-UAP-PR059_NAG_UAP_1_Jun_20.mp4`
3. 各セグメントのタイムコードを参照しながら該当箇所を再生する
4. 各セグメントの「人間確認」欄に OK / PARTIAL / WRONG / UNKNOWN を記入する
5. PARTIAL / WRONG の場合は「人間メモ」欄に差分を記述する
6. 保存して AI に返す（AI が note_draft を修正する）
