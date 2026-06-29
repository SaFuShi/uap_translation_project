# Media Inspector v4 設計記録

- 作成日: 2026-06-28
- 設計起点: PR062 再検証で判明したv3の限界
- 恒久仕様: `docs/media_inspector_v4_architecture.md`
- ステータス: 設計完了・実装未着手

---

## 1. 設計の起点：PR062 で判明した問題

PR062（DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1）に対してMedia Inspector v3フローを適用したところ、以下の問題が人間査読により発見された。

### 1.1 背景の誤識別（最大の問題）

| AI v3 判断 | Human確認結果 |
|-----------|--------------|
| 全セグメントを「雲面（雲層）」と記述 | 実際は**荒涼とした山脈地帯の地表面** |

**根本原因**: Motion Intelligence v3 はピクセル差分を計算するが、フレームの背景が「何であるか」を判定する機能を持たない。AIがフレームを目視確認した際、低解像度の山脈テクスチャを雲と誤認した。

### 1.2 移動方向の誤推定

| セグメント | AI v3 判断 | Human確認 |
|-----------|-----------|---------|
| Seg-2（track_2）| RIGHT方向 | 実際は左方向へ位置変化 |
| Seg-5（track_6）| RIGHT方向 | 実際は左方向へ位置変化 |

**根本原因**: Motion Intelligence v3 の LEFT/RIGHT 判定は「フレーム内の候補クラスタの絶対座標」に基づく。カメラのパン追尾（観測機器が対象物を追いかける動き）が補正されていないため、対象物の画面上の見かけ移動方向と実際の移動方向が逆転する場合がある。

### 1.3 ERRATIC_MOTION の誤評価

| 判断 | 詳細 |
|------|------|
| track_3（72-135s）: ERRATIC_MOTION | カメラのパン追尾で相対座標が不規則に変動したため |
| track_4（147-174s）: ERRATIC_MOTION | 同上 |

**Human確認**: 実際には対象物候補は直線的な移動を継続していた。カメラが対象物をフォロー追跡していたため、フレーム内の相対座標が乱れた。

### 1.4 カメラ事象の未検出

Human確認により以下が発見されたが、v3 では一切検出できなかった：

| タイムコード | 事象 |
|------------|------|
| 25s（00:25）| ワイド画角への切替 |
| 52s（00:52）| Zoom画角への切替 |
| 124s（02:04）| Zoom画角への切替 |
| 249s（04:09）| 望遠→ワイドへの切替 |
| 256s（04:16）| ブラックアウト→ホワイトアウト→ワイド化 |

### 1.5 陰影変化の誤分類

| AI v3 判断 | Human確認 |
|-----------|---------|
| 69-72s: 「背景急変（CUT相当）」 | 地表面の陰から日向への陰影変化（CUTではない）|

### 1.6 物体捕捉精度の問題

- `object_detection_quality: low`（Ground Truth 記録）
- 8トラックを別々の物体候補として検出したが、実際は**同一物体を映像全体で継続追跡**していた
- MASKED_ENTRY（マスキング外への移動）を「新規物体出現」と誤判定

---

## 2. v4 設計の方針決定

### 2.1 分業化の根拠

v3 の単一エンジン設計では、「何が映っているか」「カメラはどう動いているか」「対象物はどこにいるか」「陰影はどう変化しているか」を同一アルゴリズムが同時に処理しようとして失敗した。

v4 では各問題を専門 Agent に分担させる。

| v3 での失敗 | v4 での対応 Agent |
|------------|----------------|
| 背景誤識別 | Scene Analyzer |
| 方向誤推定 | Camera Analyzer → MI v4 補正 |
| カメラ事象未検出 | Camera Analyzer |
| 陰影変化誤分類 | Shadow/Illumination Analyzer |
| ERRATIC誤評価 | Camera Analyzer 補正 + MI v4 |
| 不適切な断定表現 | Observation Generator（表現ルール）|

### 2.2 実装しない理由（現時点）

- 実装は v4 設計確定後に別途着手
- PR062 の note_draft 修正は AI Observation Report v3 修正版を使用し、v4 実装を待たない
- v4 は次の未処理VIDから適用開始を目標とする

---

## 3. 各 Agent の設計判断記録

### Scene Analyzer 設計判断

**なぜルールベースか**: ローカルVLM（Qwen2.5-VL-7B）は画像分類でも利用可能だが、軍事センサー映像の低解像度・独特な色調では汎用VLMの誤判定が懸念される。まずルールベース（色ヒストグラム・テクスチャ周波数特性）で実装し、VLM補強は Phase 2 とする。

**クラウドとの混同防止**: 雲（cloud）と地表面（ground_surface）の混同はPR062の主因。以下の特徴量で区別する：
- 空間周波数: 雲は低域優位、地表岩肌は高域優位
- エッジ強度: 地表は稜線・谷のエッジが強い
- 輝度分布: 雲は比較的均一、地表は陰影による偏りがある

### Camera Analyzer 設計判断

**位相相関との違い**: v3 の位相相関は「背景全体の移動ベクトル」を算出するが、カメラ事象の種別（ズームか、パンか、FOV切替か）は判定できない。Camera Analyzer は事象種別を明示的に出力する。

**ブラックアウト/ホワイトアウト検出**: フレーム全体の平均輝度を前後フレームと比較する。閾値は `brightness < 10`（ブラックアウト）/ `brightness > 245`（ホワイトアウト）を暫定値とする。

**FOV変化の検出方法**: 連続する2フレーム間で、背景テクスチャのスケール変化をパッチマッチングで推定する。ズームイン時はテクスチャが拡大（スケール > 1.0）、ズームアウト時は縮小（スケール < 1.0）。

### Motion Intelligence v4 設計判断

**v3 との後方互換**: 出力フィールドは v3 の `motion_events.csv` を拡張する形で設計する（`camera_compensated`, `cam_dx`, `cam_dy`, `corrected_cx`, `corrected_cy` を追加）。

**地表面時の閾値調整**: Scene Analyzer が `scene_type: ground_surface` を返した場合、`SEED_RES_THRESH` を現在の35.0から45.0に引き上げる。地表テクスチャの高周波成分が誤seed を生成しやすいため。

### Object Tracker 設計判断

**MASKED_ENTRY / MASKED_EXIT の意義**: PR062の225-235sで、黒マスキング（黒塗り矩形）から対象物候補が「現れた」ように見えたケースを `MASKED_ENTRY` として記録することで、「新規出現」との混同を防ぐ。フレームの端にある黒塗り矩形の範囲を事前に検出し、対象物候補がその矩形内から出てきた場合に `MASKED_ENTRY` を付与する。

### Shadow/Illumination Analyzer 設計判断

**実装を後回しにした理由**: 陰影解析は有用だが、PR062での即時的な誤認識の主因ではない。Scene Analyzer と Camera Analyzer を先に実装することで、v3 の主要な問題の大半が解決できる。Shadow Analyzer は Phase 2 での実装とする。

**地表陰影と雲影の区別**: Scene Analyzer で地表面と確定した場合にのみ terrain_shadow_transition を判定する。雲背景（cloud）では地表陰影は存在しないため。

### Observation Generator 設計判断

**表現ルールを独立層として設ける理由**: 過去のバージョンでは分析エンジンが「確認できる」「右方向へ移動」等の断定表現を直接出力していた。表現の制御を分析から分離することで、分析精度が向上しなくても表現の適切さを個別に改善できる。

**セグメント数の維持**: 5〜8セグメントの原則はv4でも継続。各Agentの出力が多量であっても、Observation Generator がセグメント単位に集約する。

---

## 4. 未解決の課題（v4 設計時点）

| 課題 | 詳細 | 対応方針 |
|------|------|---------|
| カメラパン量の定量的補正精度 | パン量の推定誤差が大きい場合、MI v4 の補正が逆効果になる可能性 | Camera Analyzer の出力にconfidence を付与し、低confidence 時は補正を適用しない |
| VLMなしでのScene分類精度 | ルールベースでは「砂漠」と「山岳」の区別が困難な場合がある | `unknown` を適切に返す。分類の誤りより `unknown` の方がマシ |
| 複数対象物のトラッキング | PR062では単一物体だったが、PR067（Multiple Spherical UAP）等では複数同時追跡が必要 | Object Tracker の multi-track 設計は Phase 2 |
| 音声トラックの未活用 | PR062には音声トラック（AAC）があるが未解析 | 音声解析は別途 Audio Analyzer として設計（v5以降）|

---

## 5. 実装ロードマップ

```
Phase 1（v4.0）: 最優先2 Agent
  ├── scripts/scene_analyzer.py        ← Scene Analyzer 実装
  └── scripts/camera_analyzer.py       ← Camera Analyzer 実装

Phase 1.5（v4.1）: MI v4 + Observation Generator 更新
  ├── scripts/motion_intelligence_v4.py   ← Camera補正統合
  └── scripts/generate_observation_report_v4.py

Phase 2（v4.2）: Tracker + Shadow
  ├── scripts/object_tracker.py           ← Object Tracker 独立化
  └── scripts/shadow_illumination_analyzer.py

Phase 3（v5 以降）:
  ├── Audio Analyzer
  ├── VLM補強（Scene Analyzer Phase 2）
  └── Multi-track 対応（Object Tracker）
```

---

## 6. PR062 再検証 チェックリスト（v4実装後）

```
□ Scene Analyzer: 全フレームが ground_surface を返すことを確認
□ Camera Analyzer: 5つの画角変化事象が検出されることを確認
□ MI v4: track_2 の方向がカメラ補正後に適切に変更されることを確認
□ Object Tracker: FRAMEOUT・MASKED_ENTRY 事象の記録を確認
□ Shadow Analyzer: 69-72s の terrain_shadow_transition=true を確認
□ Observation Report v4: 背景「地表面」・方向「位置変化」表現であることを確認
□ v3 レポートとの diff を作成し、改善箇所を文書化
```
