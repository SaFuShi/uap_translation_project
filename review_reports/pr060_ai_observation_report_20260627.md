# AI Observation Report: DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2

## メタデータ

- source_id: DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2
- article_id: R02-052
- source_video_path: raw_media/video/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2.mp4
- duration: 290s（04:50）
- run_date: 20260627
- 生成スクリプト: scripts/generate_ai_observation_report.py
- pipeline_steps:
  - adaptive_frames: data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2
  - delta_analysis: data/frame_delta_runs/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/summary.md
  - targeted_frames: data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_targeted
  - vlm_output: 未実施

---

## 観察サマリー

Delta分析全体では APPEAR 1件・DISAPPEAR 3件・CUT 41件・OBJECT_MOVE 48件 を検出した。映像を 6 セグメントに分割して観察する。各セグメントの詳細はソース映像の確認で確定する。

---

## 重要セグメント

### セグメント A: 0s（00:00）〜114s（01:54）

**概要タグ:** APPEAR（bc_max=189） / DISAPPEAR×2 / CUT×31（max_diff=52.6） / OBJECT_MOVE×4

**AI観察:**
この区間で31回のシーン急変（CUT）を検出した（6s（00:06）〜105s（01:45）、mean_diff: 48.8, 47.3, 50.8）。
レンズの切り替え（FOV変更）または映像の編集点の可能性がある。
99s（01:39）付近で輝度の完全消失（bc→0）を検出しており、対象物がフレームアウトした直後にレンズが切り替わった可能性がある。
108s（01:48）付近で輝点の再出現（bc=189）を検出した。

**確信度:** medium
（Delta分析で高bc値のAPPEAR/DISAPPEARを検出。ソース映像確認後に high に昇格可能）

**根拠:**
- Adaptive frame: frame_0000.png, frame_0003.png, frame_0006.png 他 39枚
- Delta result: APPEAR（bc=189@108s（01:48））; DISAPPEAR（bc_prev=3,125→0@99s（01:39）, bc_prev=189→0@111s（01:51））; CUT（mean_diff=48.8@6s（00:06）, mean_diff=47.3@9s（00:09）, mean_diff=50.8@15s（00:15））; OBJECT_MOVE×4件
- Targeted frame: frame_00090.png, frame_00091.png, frame_00092.png 他 22枚 （data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_targeted/）
- VLM output: 未実施
- Filename metadata: ソースIDのみ参照

**リスクフラグ:**
- ui_misidentification: none
- trimming_effect: medium（31回のCUT→レンズ切り替えまたはトリミング変化の可能性）
- blowup_effect: none
- speed_change: none
- frameout_misidentification: medium（99s（01:39）のDISAPPEAR（bc→0）→フレームアウトと露出消失の区別困難）
- exposure_change: high（CUT（90s（01:30）付近）の前後にAPPEAR/DISAPPEARが発生→露出変化の可能性）
- compression_artifact: none

**人間確認:**
- [ ] OK — AIの観察は正しい
- [ ] PARTIAL — 一部修正が必要（以下に記述）
- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

### セグメント B: 114s（01:54）〜147s（02:27）

**概要タグ:** DISAPPEAR×1 / CUT×6（max_diff=63.9） / OBJECT_MOVE×4

**AI観察:**
この区間で6回のシーン急変（CUT）を検出した（126s（02:06）〜144s（02:24）、mean_diff: 44.1, 63.9, 57.2）。
レンズの切り替え（FOV変更）または映像の編集点の可能性がある。
123s（02:03）付近で輝度の完全消失（bc→0）を検出しており、対象物がフレームアウトした直後にレンズが切り替わった可能性がある。

**確信度:** medium
（CUTのmean_diff=63.9（高値）→シーン変化は確実。内容の解釈は要確認）

**根拠:**
- Adaptive frame: frame_0114.png, frame_0117.png, frame_0120.png 他 12枚
- Delta result: DISAPPEAR（bc_prev=27→0@123s（02:03））; CUT（mean_diff=44.1@126s（02:06）, mean_diff=63.9@129s（02:09）, mean_diff=57.2@132s（02:12））; OBJECT_MOVE×4件
- Targeted frame: frame_00115.png, frame_00116.png, frame_00117.png 他 14枚 （data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_targeted/）
- VLM output: 未実施
- Filename metadata: ソースIDのみ参照

**リスクフラグ:**
- ui_misidentification: none
- trimming_effect: medium（6回のCUT→レンズ切り替えまたはトリミング変化の可能性）
- blowup_effect: none
- speed_change: none
- frameout_misidentification: medium（123s（02:03）のDISAPPEAR（bc→0）→フレームアウトと露出消失の区別困難）
- exposure_change: high（CUT（126s（02:06）付近）の前後にAPPEAR/DISAPPEARが発生→露出変化の可能性）
- compression_artifact: none

**人間確認:**
- [ ] OK — AIの観察は正しい
- [ ] PARTIAL — 一部修正が必要（以下に記述）
- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

### セグメント C: 147s（02:27）〜204s（03:24）

**概要タグ:** OBJECT_MOVE×19

**AI観察:**
この区間で対象物の移動（OBJECT_MOVE×19件）を継続的に検出した。
輝点が継続して検出されており（平均bc≈30222）、対象物が映像内に存在し続けている可能性が高い。

**確信度:** unknown
（根拠が不十分。ソース映像確認が必要）

**根拠:**
- Adaptive frame: frame_0147.png, frame_0150.png, frame_0153.png 他 20枚
- Delta result: OBJECT_MOVE×19件
- Targeted frame: data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_targeted/ （範囲内フレームなし）
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

### セグメント D: 204s（03:24）〜216s（03:36）

**概要タグ:** CUT×2（max_diff=42.2） / OBJECT_MOVE×2

**AI観察:**
この区間で2回のシーン急変（CUT）を検出した（210s（03:30）〜213s（03:33）、mean_diff: 42.2, 37.7）。
レンズの切り替え（FOV変更）または映像の編集点の可能性がある。

**確信度:** low
（CUTのmean_diff=42.2（中値）→シーン変化あり。意味の解釈は不確実）

**根拠:**
- Adaptive frame: frame_0204.png, frame_0207.png, frame_0210.png 他 5枚
- Delta result: CUT（mean_diff=42.2@210s（03:30）, mean_diff=37.7@213s（03:33））; OBJECT_MOVE×2件
- Targeted frame: data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_targeted/ （範囲内フレームなし）
- VLM output: 未実施
- Filename metadata: ソースIDのみ参照

**リスクフラグ:**
- ui_misidentification: none
- trimming_effect: medium（2回のCUT→レンズ切り替えまたはトリミング変化の可能性）
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

### セグメント E: 216s（03:36）〜267s（04:27）

**概要タグ:** OBJECT_MOVE×17

**AI観察:**
この区間で対象物の移動（OBJECT_MOVE×17件）を継続的に検出した。
輝点が継続して検出されており（平均bc≈28438）、対象物が映像内に存在し続けている可能性が高い。

**確信度:** unknown
（根拠が不十分。ソース映像確認が必要）

**根拠:**
- Adaptive frame: frame_0216.png, frame_0219.png, frame_0222.png 他 18枚
- Delta result: OBJECT_MOVE×17件
- Targeted frame: data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_targeted/ （範囲内フレームなし）
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

### セグメント F: 267s（04:27）〜279s（04:39）

**概要タグ:** CUT×2（max_diff=48.5） / OBJECT_MOVE×2

**AI観察:**
この区間で2回のシーン急変（CUT）を検出した（273s（04:33）〜276s（04:36）、mean_diff: 48.5, 35.2）。
レンズの切り替え（FOV変更）または映像の編集点の可能性がある。

**確信度:** low
（CUTのmean_diff=48.5（中値）→シーン変化あり。意味の解釈は不確実）

**根拠:**
- Adaptive frame: frame_0267.png, frame_0270.png, frame_0273.png 他 5枚
- Delta result: CUT（mean_diff=48.5@273s（04:33）, mean_diff=35.2@276s（04:36））; OBJECT_MOVE×2件
- Targeted frame: data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_targeted/ （範囲内フレームなし）
- VLM output: 未実施
- Filename metadata: ソースIDのみ参照

**リスクフラグ:**
- ui_misidentification: none
- trimming_effect: medium（2回のCUT→レンズ切り替えまたはトリミング変化の可能性）
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

## note_draft 反映候補

| セグメント | note_draft 反映案 | 確信度 | 人間確認後に反映 |
|-----------|-----------------|--------|----------------|
| A | 「99s（01:39）付近で対象物の消失またはフレームアウトが検出された」 | medium | （人間確認待ち） |
| B | 「123s（02:03）付近で対象物の消失またはフレームアウトが検出された」 | medium | （人間確認待ち） |
| C | 「この区間（約57秒）で対象物の緩やかな移動を継続検出（OBJECT_MOVE×19件）」 | unknown | （人間確認待ち） |
| D | 「210s（03:30）前後でレンズ切り替えと思われるシーン変化が2回検出された」 | low | （人間確認待ち） |
| E | 「この区間（約51秒）で対象物の緩やかな移動を継続検出（OBJECT_MOVE×17件）」 | unknown | （人間確認待ち） |
| F | 「273s（04:33）前後でレンズ切り替えと思われるシーン変化が2回検出された」 | low | （人間確認待ち） |

---

## 代表フレーム候補

| セグメント | フレーム | タイムスタンプ | 選定理由 | 優先度 |
|-----------|---------|-------------|---------|--------|
| A | data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/frame_0033.png | 33s（00:33） | CUT mean_diff=52.6（セグメントAで最大変化） | 中 |
| B | data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2_targeted/frame_00129.png | 129s（02:09） | CUT mean_diff=63.9（セグメントBで最大変化） | 中 |
| C | data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/frame_0177.png | 176s（02:56） | 区間中央フレーム（顕著なイベントなし） | 低 |
| D | data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/frame_0210.png | 210s（03:30） | CUT mean_diff=42.2（セグメントDで最大変化） | 中 |
| E | data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/frame_0243.png | 242s（04:02） | 区間中央フレーム（顕著なイベントなし） | 低 |
| F | data/adaptive_frames/20260627/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2/frame_0273.png | 273s（04:33） | CUT mean_diff=48.5（セグメントFで最大変化） | 中 |

**→ 代表フレーム確定:** （人間確認後に記入）

---

## 人間確認フロー

1. このレポートを通読する
2. QuickTime（または任意のプレイヤー）でソース映像を開く
   `raw_media/video/DOW-UAP-PR060_Spherical_UAP_CALLSIGN_2021_04_12_obj_2.mp4`
3. 各セグメントのタイムコードを参照しながら該当箇所を再生する
4. 各セグメントの「人間確認」欄に OK / PARTIAL / WRONG / UNKNOWN を記入する
5. PARTIAL / WRONG の場合は「人間メモ」欄に差分を記述する
6. 保存して AI に返す（AI が note_draft を修正する）
