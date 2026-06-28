# AI Observation Report: DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0

## メタデータ

- source_id: DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0
- article_id: R02-053
- source_video_path: raw_media/video/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0.mp4
- duration: 286s（04:46）
- run_date: 20260627
- 生成スクリプト: scripts/generate_ai_observation_report.py
- pipeline_steps:
  - adaptive_frames: data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0
  - delta_analysis: data/frame_delta_runs/20260627_v2/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0/summary.md
  - targeted_frames: data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted
  - vlm_output: 未実施

---

## 観察サマリー

Delta分析全体では DISAPPEAR 2件・OBJECT_MOVE 90件 を検出した。映像を 5 セグメントに分割して観察する。各セグメントの詳細はソース映像の確認で確定する。

---

## 重要セグメント

### セグメント A: 9s（00:09）〜18s（00:18）

**概要タグ:** DISAPPEAR×1 / OBJECT_MOVE×2

**AI観察:**
12s（00:12）→15s（00:15）で輝点の急激な減少（bc: 109,429→26,619）を検出した。

**確信度:** medium
（Delta分析で高bc値のAPPEAR/DISAPPEARを検出。ソース映像確認後に high に昇格可能）

**根拠:**
- Adaptive frame: frame_0009.png, frame_0012.png, frame_0015.png 他 4枚
- Delta result: DISAPPEAR（bc_prev=109,429→26,619@15s（00:15））; OBJECT_MOVE×2件
- Targeted frame: frame_00009.png, frame_00010.png, frame_00011.png 他 9枚 （data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted/）
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
→航空機などで上空から地上を撮影している映像。荒涼とした山脈が映るのみ。UAP対象物などはなく、輝点の急激な減少はなく、山並みの影になっている箇所とそうでない箇所がある。カラー映像と思われる
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

### セグメント B: 18s（00:18）〜102s（01:42）

**概要タグ:** OBJECT_MOVE×28

**AI観察:**
この区間で対象物の移動（OBJECT_MOVE×28件）を継続的に検出した。
輝点が継続して検出されており（平均bc≈18082）、対象物が映像内に存在し続けている可能性が高い。

**確信度:** unknown
（根拠が不十分。ソース映像確認が必要）

**根拠:**
- Adaptive frame: frame_0018.png, frame_0021.png, frame_0024.png 他 29枚
- Delta result: OBJECT_MOVE×28件
- Targeted frame: frame_00018.png, frame_00019.png, frame_00020.png 他 18枚 （data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted/）
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
→引き続き、航空機などで上空から地上を撮影している映像。荒涼とした山脈が映るのみ。UAP対象物などはなく、輝点の急激な減少はなく、山並みの影になっている箇所とそうでない箇所がある。カラー映像と思われる。影による印影が輝点の変化と誤認する影響を及ぼしている可能性がある。なお、観測機器の移動に伴い地表面の変化があるが、その中で自発的に移動している物体はない。
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

### セグメント C: 102s（01:42）〜186s（03:06）

**概要タグ:** OBJECT_MOVE×28

**AI観察:**
この区間で対象物の移動（OBJECT_MOVE×28件）を継続的に検出した。
輝点が継続して検出されており（平均bc≈23557）、対象物が映像内に存在し続けている可能性が高い。

**確信度:** unknown
（根拠が不十分。ソース映像確認が必要）

**根拠:**
- Adaptive frame: frame_0102.png, frame_0105.png, frame_0108.png 他 29枚
- Delta result: OBJECT_MOVE×28件
- Targeted frame: frame_00180.png, frame_00181.png, frame_00182.png 他 6枚 （data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted/）
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
→03:03あたりで画面右上から下に向かってほぼ一直線に進行するUAP対象物と思われるものが視認できる。それより前には対象物は見られず、移動に伴う地表面と、緑のNマーク、センター十字ターゲットマーク、フレーム枠と思われる四隅を示すマーカーが見える。これは、その前のブロック全てにおいて継続して表示されて続けている。
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

### セグメント D: 186s（03:06）〜238s（03:58）

**概要タグ:** OBJECT_MOVE×18

**AI観察:**
この区間で対象物の大きな移動（最大580px、192s（03:12）付近）をDelta分析が検出した。
輝点が継続して検出されており（平均bc≈25775）、対象物が映像内に存在し続けている可能性が高い。

**確信度:** unknown
（根拠が不十分。ソース映像確認が必要）

**根拠:**
- Adaptive frame: frame_0186.png, frame_0189.png, frame_0192.png 他 18枚
- Delta result: OBJECT_MOVE×18件
- Targeted frame: frame_00187.png, frame_00188.png, frame_00189.png 他 38枚 （data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted/）
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
→セグメントDより前から移動しているUAP対象物と思われるものが、そのまま画面下方向へ直線的に移動しており、03:09付近でフレームアウトする。撮影機器がフレームアウトした対象物を追跡するため、03:09以降で対象物を追跡するように画面下方向へカメラが移動しているように映像が遷移する。03:11付近で再度カメラがFixする・03:13頃に上部の黒いマスキング部分より再度UAP対象物と思われるものが視認できる。また、対象物は画面下部に向かって直線的に移動している。それを追跡するようにカメラがフォローしており、画面が移動している。画角は変わっておらず、カメラが対象物をフォローする動きと思われる。宇対象物の動きは当初直線的だったが、その後多少の方向転換はしているものの急激ではなく、風の影響を受けているような動きで画面下方向へ移動を続けている。撮影機器は対象物を中央に捉えようとしているが、ターゲットを示す十字マークの動きからすると対象物の直線的であるものの不規則な動きをフォローするかのように撮影機器は左右に振っているように見受けられる。
- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

### セグメント E: 238s（03:58）〜282s（04:42）

**概要タグ:** DISAPPEAR×1 / OBJECT_MOVE×14

**AI観察:**
276s（04:36）→279s（04:39）で輝点の急激な減少（bc: 124,059→13,577）を検出した。

**確信度:** medium
（Delta分析で高bc値のAPPEAR/DISAPPEARを検出。ソース映像確認後に high に昇格可能）

**根拠:**
- Adaptive frame: frame_0240.png, frame_0243.png, frame_0246.png 他 15枚
- Delta result: DISAPPEAR（bc_prev=124,059→13,577@279s（04:39））; OBJECT_MOVE×14件
- Targeted frame: frame_00243.png, frame_00244.png, frame_00245.png 他 31枚 （data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted/）
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
→04:00付近で対象物の影が地表面に出ていることを視認。04:01付近で撮影機器が対象物を見失う。撮影機器が対象物より行き過ぎてしまい、撮影機器が消失したと思われる地点に04:02頃に戻るものの、対象物は消失しているようで目視では確認できず。しばらく消失地点付近を撮影機器が探すように映像が動くものの、見つからず。04:12付近で撮影機器のモードを変更したかのように地表面の見え方が変わる。その時点で今まで緑で視認できていたNマーク、十字ターゲットマーク、フレーム枠と思われる四隅を示すマーカーがシアンに変化する。なお、映像の中心点は対象物と思われるものの消失点にほぼfixしている。04:17で一度ホワイトアウト（おそらく露出オーバー）し、Zoom画像に切り替わる。おそらく撮影機器のレンズのミリ数が代わり、望遠に変わっている。対象物と思われるものの消失点がより大きく映る。04:31で露出オーバーになったかのように画面全体が明るくなるが、地表面の見え方のディテールがより明確になり、影が落ちていた部分も明るくなり、対象物と思われるものの消失点付近も若干ではあるものの明るく視認しやすくなる。だが、対象物と思われるものは見つからず。04:37でまた映像が少し暗くなり、撮影機器の何らかのモード変更が行われた可能性がある。04:12以降の十字ターゲットマークなどのUIの色はシアンのままで、撮影機器のレンズのミリ数やモードが切り替わっていると推測される
- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）
- [ ] UNKNOWN — 映像からは判断できない

**人間メモ:**
（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）

---

## note_draft 反映候補

| セグメント | note_draft 反映案 | 確信度 | 人間確認後に反映 |
|-----------|-----------------|--------|----------------|
| A | 「この区間（約9秒）で対象物の緩やかな移動を継続検出（OBJECT_MOVE×2件）」 | medium | （人間確認待ち） |
| B | 「この区間（約84秒）で対象物の緩やかな移動を継続検出（OBJECT_MOVE×28件）」 | unknown | （人間確認待ち） |
| C | 「この区間（約84秒）で対象物の緩やかな移動を継続検出（OBJECT_MOVE×28件）」 | unknown | （人間確認待ち） |
| D | 「この区間で対象物の継続的な移動を検出（最大580px、192s（03:12）付近）」 | unknown | （人間確認待ち） |
| E | 「この区間で対象物の継続的な移動を検出（最大842px、252s（04:12）付近）」 | medium | （人間確認待ち） |

---

## 代表フレーム候補

| セグメント | フレーム | タイムスタンプ | 選定理由 | 優先度 |
|-----------|---------|-------------|---------|--------|
| A | data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted/frame_00014.png | 14s（00:14） | 区間中央フレーム（顕著なイベントなし） | 低 |
| B | data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0/frame_0060.png | 60s（01:00） | 区間中央フレーム（顕著なイベントなし） | 低 |
| C | data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0/frame_0144.png | 144s（02:24） | 区間中央フレーム（顕著なイベントなし） | 低 |
| D | data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted/frame_00192.png | 192s（03:12） | OBJECT_MOVE pos_delta=580px | 中 |
| E | data/adaptive_frames/20260627/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0_targeted/frame_00273.png | 273s（04:33） | OBJECT_MOVE pos_delta=842px | 中 |

**→ 代表フレーム確定:** （人間確認後に記入）

---

## 人間確認フロー

1. このレポートを通読する
2. QuickTime（または任意のプレイヤー）でソース映像を開く
   `raw_media/video/DOW-UAP-PR061_Spherical_UAP_CALLSIGN_2021_04_12_vid_0.mp4`
3. 各セグメントのタイムコードを参照しながら該当箇所を再生する
4. 各セグメントの「人間確認」欄に OK / PARTIAL / WRONG / UNKNOWN を記入する
5. PARTIAL / WRONG の場合は「人間メモ」欄に差分を記述する
6. 保存して AI に返す（AI が note_draft を修正する）
