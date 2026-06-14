# Release 02 音声・映像処理パイプライン設計書 v1

**制定日:** 2026-05-29
**適用対象:** Release 02 AUD（音声）8件 / VID（動画）78件
**前提方針書:** `docs/release02_media_processing_policy_v1.md`
**ステータス:** 設計のみ（ffmpeg実行・Whisper実行・動画解析・git commit は未実施）

---

## 0. 本設計書の目的と位置づけ

`release02_media_processing_policy_v1.md` で確立した「何をすべきか」の方針に対し、本設計書は「どう実装するか」の詳細を記述する。

対象素材:

| 種別 | 件数 | 形式 | 代表的内容 |
|------|------|------|----------|
| AUD | 8件 | .mp4（音声コンテナ） | NASA Gemini/Apollo/Mercury 音声（1961–1972年） |
| VID | 78件 | .mp4 | DOW-UAP PR シリーズ（軍関連UAP映像） |
| IMG | 14件 | .png/.jpg | FBI フォト 8件・NASA Apollo 写真 6件 |

IMG（静止画）は OCR / 視覚観察のみで本設計書のスコープ外。

---

## 1. AUD 文字起こし方針

### 1-1. 方針概要

AUD 8件は全て NASA 宇宙飛行士の交信・報告音声（`audio_record` + `historical_record`）。
文字起こしの目的は「発言の事実確認」であり、「UAP目撃証言の抽出」ではない。

### 1-2. 処理単位

ファイル単位で処理する（ページ概念なし）。
出力は 1ファイル = 1 transcript ファイル。

### 1-3. 段階的実施方針

| フェーズ | 対象 | 実施内容 |
|---------|------|---------|
| Phase A | 全8件 | mlx-whisper による自動文字起こし（英文）。`transcripts/` へ保存 |
| Phase B | 人間確認 | 英文の聴き取り正確性を目視レビュー。不明瞭箇所を `[inaudible]` 記載 |
| Phase C | 翻訳・記事化 | 確認済み英文を日本語訳。note_drafts/ へ |

Phase A のみ自動化。Phase B・C は人間作業。

### 1-4. 文字起こし品質基準

- `[inaudible]` 率が 20% 以上 → Phase B 優先レビュー対象としてフラグ
- Whisper confidence スコアが平均 0.7 未満 → `low_confidence` フラグを付けて保留
- 信頼できない補完テキストは記事に使用しない（hallucination リスク）

---

## 2. Whisper / whisper.cpp / mlx-whisper 候補比較

### 2-1. 候補一覧

| 候補 | 実行環境 | Apple Silicon 最適化 | 精度 | セットアップコスト | 備考 |
|------|---------|---------------------|------|-----------------|------|
| openai/whisper (PyTorch) | CPU/GPU | なし（MPS は不完全） | 高 | 低 | M4 Pro では遅い |
| whisper.cpp | CPU/Metal | Metal GPU 対応 | 高 | 中（ビルド要） | C++ ビルド必要 |
| **mlx-whisper** | **Apple MLX** | **最大限（M4 Pro ネイティブ）** | **高** | **低（pip install）** | **推奨** |
| faster-whisper (CTranslate2) | CPU | 部分的 | 高 | 中 | Linux 最適 |

### 2-2. mlx-whisper を推奨する理由

- Apple M4 Pro の Neural Engine / GPU を MLX フレームワーク経由でフル活用
- `pip install mlx-whisper` のみでセットアップ完了（ビルド不要）
- large-v3 モデルでも Mac mini M4 Pro で実用速度（RTF ≈ 0.2 以下見込み）
- 出力形式: txt / json / srt / vtt から選択可能

### 2-3. 使用モデル選定

| モデル | VRAM相当 | 想定速度 | 精度 | 用途 |
|-------|---------|---------|------|------|
| large-v3 | ~6GB | 中 | 最高 | 本番処理（AUD 8件） |
| medium | ~3GB | 速 | 高 | --limit テスト用 |
| base | ~1GB | 最速 | 中 | 動作確認のみ |

本番処理は `large-v3` を使用。テスト実行は `medium` を使用して速度を確保する。

### 2-4. 言語設定

- `--language en` を明示指定（NASA 音声は英語）
- 自動検出（`--language auto`）は使用しない（誤判定リスク回避）

---

## 3. VID 代表フレーム抽出方針

### 3-1. 目的

VID 78件のうち、note 記事のサムネイル候補・視覚観察記録用のフレームを抽出する。
全フレーム解析は行わない（計算コストと保存領域の観点から）。

### 3-2. 抽出戦略

**固定間隔抽出（一次抽出）:**

- 動画長に応じて等間隔でフレームを抽出
- 基準: 30秒ごとに1フレーム（最大 10フレーム / 動画）
- 最短動画（417KB 相当）はフレーム数が少ないため最低 1フレームを保証

**追加抽出（二次抽出、オプション）:**

- シーンチェンジ検出（`ffmpeg -vf select='gt(scene,0.4)'`）
- 一次抽出で重要シーンを逃している場合のみ実施
- 二次抽出実施時は理由を `frame_extracts/` メタデータに記録

### 3-3. 抽出フォーマット

| 項目 | 設定値 |
|------|-------|
| 出力形式 | PNG（可逆圧縮） |
| 解像度 | 元動画解像度を維持（リサイズしない） |
| ファイル名 | `{pdf_stem}_frame_{timestamp_sec:06d}.png` |
| 格納先 | `frame_extracts/{video_stem}/` |

### 3-4. フレーム選定ルール

抽出されたフレームをサムネイル候補として記事化担当者が選定する。
自動選定（AI による「重要度スコアリング」）は使用しない（主観的断定のリスク）。

---

## 4. ffmpeg 利用方針

### 4-1. 用途

| 用途 | ffmpeg コマンド例 | 備考 |
|------|-----------------|------|
| AUD 音声抽出（.mp4 → .wav） | `ffmpeg -i input.mp4 -ar 16000 -ac 1 output.wav` | mlx-whisper 入力用（16kHz mono） |
| VID フレーム抽出（固定間隔） | `ffmpeg -i input.mp4 -vf fps=1/30 frame_%04d.png` | 30秒間隔 |
| VID フレーム抽出（指定時刻） | `ffmpeg -ss 00:01:00 -i input.mp4 -vframes 1 frame.png` | 特定時刻 |
| 動画メタデータ取得 | `ffprobe -v quiet -print_format json -show_format -show_streams` | duration/bitrate 取得 |

### 4-2. ffmpeg バージョン要件

- Homebrew 経由インストール (`brew install ffmpeg`)
- バージョン: 6.0 以上推奨
- Mac mini M4 Pro では VideoToolbox ハードウェアアクセラレーション利用可能

### 4-3. 安全ルール

- `--dry-run` 相当の確認（`-n` フラグで既存ファイルを上書きしない）
- 入力ファイル（`raw_media/`）は読み取り専用として扱う。ffmpeg は出力先のみ書き込む
- ファイルサイズ 490MB の大容量ファイルがある。処理前に空き容量を確認する

### 4-4. AUD → WAV 変換に関する注意

- Whisper（mlx-whisper）は直接 .mp4 を受け付けるが、安定性のため .wav 変換を推奨
- サンプリングレートは 16kHz（Whisper の学習レートと一致）
- モノラル変換（`-ac 1`）で処理速度を向上

---

## 5. 出力設計（transcripts / frame_extracts / worker_outputs）

### 5-1. ディレクトリ構成

```
UAP_TRANSLATION_PROJECT/         ← リポジトリルート
├── transcripts/                  ← 文字起こし出力（AUD）
│   ├── {audio_stem}/
│   │   ├── transcript.txt        ← プレーンテキスト（人間読用）
│   │   ├── transcript.json       ← Whisper 出力 JSON（タイムスタンプ付き）
│   │   └── transcript_meta.json  ← 処理メタデータ（モデル・時刻・conf）
│   └── ...
├── frame_extracts/               ← 代表フレーム（VID）
│   ├── {video_stem}/
│   │   ├── frame_000030.png      ← 30秒時点
│   │   ├── frame_000060.png      ← 60秒時点
│   │   └── extract_meta.json     ← 抽出設定（間隔・実施日時・元ファイル）
│   └── ...
└── worker_outputs/               ← Mac mini 処理ログ・中間ファイル
    ├── audio_transcription_run_{timestamp}.csv   ← 処理結果サマリ
    ├── frame_extraction_run_{timestamp}.csv      ← 抽出結果サマリ
    └── logs/
        ├── whisper/
        └── ffmpeg/
```

### 5-2. transcript_meta.json フォーマット

```json
{
  "source_file": "NASA-AUD-D001_....mp4",
  "source_path": "raw_media/audio/NASA-AUD-D001_....mp4",
  "model": "mlx-whisper/large-v3",
  "language": "en",
  "processed_at": "2026-xx-xx HH:MM:SS",
  "duration_sec": 123.4,
  "avg_confidence": 0.87,
  "low_confidence_segments": 2,
  "inaudible_count": 3,
  "notes": ""
}
```

### 5-3. audio_transcription_run CSV カラム

```
source_file, duration_sec, model, avg_confidence, inaudible_count,
low_confidence_flag, processed_at, output_path, status, error_message
```

### 5-4. frame_extraction_run CSV カラム

```
source_file, duration_sec, total_frames_extracted, extraction_interval_sec,
scene_change_used, processed_at, output_dir, status, error_message
```

### 5-5. リポジトリ管理方針

| ディレクトリ | git 管理 | 理由 |
|------------|---------|------|
| `transcripts/` 内 .txt / .json（全文） | **管理しない**（.gitignore） | AUD 8件でも数MB〜数十MB、大量 JSON は差分管理に不向き |
| `transcripts/` 内 `*_meta.json` | **管理しない**（.gitignore） | 処理ログは worker_outputs の CSV に集約する |
| `frame_extracts/` 内 .png | 管理しない（.gitignore） | バイナリ・容量大 |
| `frame_extracts/` 内 `extract_meta.json` | 管理しない（.gitignore） | フレーム抽出設定は worker_outputs の CSV に集約する |
| `worker_outputs/` 内 処理結果サマリ CSV | **管理する** | 軽量・差分が読める・処理記録として資産 |
| `worker_outputs/material_cards/` 内 素材カード JSON | **管理する（候補）** | 人間レビュー済みの確認済みカードのみ。全自動出力カードは対象外 |
| `worker_outputs/logs/` | 管理しない（.gitignore） | 大量のログファイル |

**方針の背景:** 全文 transcript や大量 JSON は git の差分管理と相性が悪く、リポジトリを肥大化させる。git には「何を処理したか・品質がどうだったか」の軽量なサマリ CSV のみ残す。全文テキストは Mac mini の ACASIS_2TB（ローカルストレージ）に保持し、必要に応じてバックアップで管理する。

---

## 6. --limit テスト方針

### 6-1. テスト設計原則

PDF パイプラインと同様に、本番全件実行前に `--limit N` テストを必ず実施する。

### 6-2. AUD 文字起こしテスト計画

| ステップ | --limit | 対象 | 確認項目 |
|---------|---------|------|---------|
| ① 動作確認 | 1 | AUD 先頭1件 | mlx-whisper が正常動作、出力ファイルが生成される |
| ② 品質確認 | 3 | AUD 先頭3件 | avg_confidence・inaudible率・出力フォーマットを確認 |
| ③ 全件実行 | なし（全8件） | AUD 全件 | エラーなし・全件出力確認 |

### 6-3. VID フレーム抽出テスト計画

| ステップ | --limit | 対象 | 確認項目 |
|---------|---------|------|----------|
| ① 動作確認 | 1 | VID 先頭1件（小ファイル） | ffmpeg 正常動作、PNG 生成確認 |
| ② 境界確認 | 1 | VID 最大ファイル（490MB） | 大容量ファイルの処理時間・空き容量確認 |
| ③ 全件実行 | なし（全78件） | VID 全件 | エラーなし・全件出力確認 |

### 6-4. スクリプト設計要件（実装時）

- `--limit N`: 先頭 N 件で停止（スキップ済みファイルはカウントしない）
- `--file-name`: 特定ファイル名を指定して単体テスト
- `--dry-run`: 処理対象ファイル一覧を表示するのみ（実際の処理なし）
- 既存出力があるファイルはスキップ（PDF パイプラインと同じ resume 方式）

### 6-5. 長時間処理の実行方式（Whisper / ffmpeg）

AUD 文字起こし（Whisper）や VID フレーム抽出（ffmpeg）は処理時間が長くなる可能性がある。**Claude Code のバックグラウンドタスクに依存せず、Mac mini 側で tmux を使って独立実行する。**

#### 推奨実行方式

| 方式 | 適用 | コマンドパターン |
|------|------|----------------|
| **tmux（推奨）** | 全件 Whisper / 全件 ffmpeg | `tmux new-session -d -s whisper-batch 'python3 scripts/run_whisper.py ... 2>&1 \| tee logs/whisper/run_YYYYMMDD_HHmmss.log'` |
| **nohup（代替）** | tmux 不使用時 | `nohup python3 scripts/run_whisper.py ... > logs/whisper/run_YYYYMMDD_HHmmss.log 2>&1 &` |
| **Claude Code background** | `--limit 1〜3` の動作確認のみ | 5分以内に収まる小規模テストに限定 |

#### 成否判定（exit code だけで判断しない）

Claude Code のバックグラウンドタスクが `failed` を返した場合も、以下の順で実態を確認する:

1. `ps aux | grep run_whisper` → プロセス有無（終了済み or 稼働中）
2. `ls -lh transcripts/` → 出力ファイルの存在・サイズ
3. `tail -20 logs/whisper/run_YYYYMMDD_HHmmss.log` → 完了メッセージ or エラー
4. `wc -l worker_outputs/audio_transcription_run_YYYYMMDD_HHmmss.csv` → 処理件数
5. ログ内のエラー件数: `grep -c -i error logs/whisper/run_YYYYMMDD_HHmmss.log`

**exit code 255 は SSH クライアント断のみを示す。Mac mini 上のプロセス成否とは無関係。**

---

## 7. 視覚観察と解釈の分離

本節は `release02_media_processing_policy_v1.md` Section 6-2 の実装ガイドライン。
フレーム抽出スクリプトおよび素材カード生成スクリプトに組み込む判定ルール。

### 7-1. 記述可能な「視覚観察」の定義

| カテゴリ | 具体例 | 判定基準 |
|---------|-------|---------|
| 位置記述 | 「画面左上に白い点が確認できる」 | 画面座標の相対記述 ✅ |
| 形状記述 | 「楕円形の明るい物体が確認できる」 | 幾何形状の記述 ✅ |
| 動き記述 | 「光点が左から右へ移動している」 | 位置の変化の記述 ✅ |
| センサー表示 | 「画面右下に 'IR' の表示がある」 | 画面内テキストの引用 ✅ |
| 色・輝度 | 「白く明るい点として映っている」 | 色・明暗の記述 ✅ |

### 7-2. 禁止される「解釈・断定」の定義

| 禁止カテゴリ | 禁止表現 | 代替表現 |
|------------|---------|---------|
| 速度断定 | 「急加速した」「高速で飛行した」 | 「光点の位置が急激に変化した」 |
| 意図断定 | 「回避行動を取った」「追跡を回避した」 | 「物体の軌跡が変化した」 |
| 対象断定 | 「UAP が映っている」「UFO である」 | 「物体が確認できる」 |
| センサー動作断定 | 「センサーがロックした」「捕捉した」 | 「センサーが物体を中心付近に維持している」 |
| 熱源断定 | 「IR 映像で高温を示している」 | 「IR 映像で白く映っている（熱源の可能性は除外しない）」 |
| 物体性質断定 | 「金属製の飛行体」「円盤型 UFO」 | 「円形または楕円形の物体」 |

### 7-3. 素材カード生成スクリプトへの組み込み方針

- 素材カードに「視覚観察欄」と「補足・推定欄」を別フィールドとして設ける
- 視覚観察欄はフリーテキストで、人間が記述する（AI 自動生成しない）
- 「補足・推定欄」への記入は provenance（`ファイル名より推定` 等）を必須記載

---

## 8. note 記事化に使う素材カード設計

### 8-1. 素材カードの目的

文字起こし結果・代表フレーム・メタデータを集約し、note 記事ドラフトを生成するための入力フォーマット。
記事生成前に人間が素材カードをレビューすることで、事実・推測・解釈の混在を防ぐ。

### 8-2. AUD 素材カード（JSON 形式）

```json
{
  "card_type": "audio",
  "source_file": "NASA-AUD-D001_....mp4",
  "catalog_id": "NASA-AUD-D001",
  "dvids_video_id": "XXXXXXX",
  "incident_date": "1965-12-04",
  "incident_location": "（ファイル名より推定）",
  "content_category": "audio_record",
  "note_series": "NASA音声記録",
  "transcript_status": "confirmed",
  "transcript_txt_path": "transcripts/NASA-AUD-D001_.../transcript.txt",
  "avg_confidence": 0.87,
  "low_confidence_flag": false,
  "inaudible_count": 2,
  "confirmed_quotes": [
    {
      "timestamp_sec": 45,
      "text": "I can see something out there",
      "confidence": "high",
      "human_verified": true
    }
  ],
  "visual_observations": [],
  "supplementary_notes": "Gemini 7ミッション中の交信音声（ファイル名より推定）",
  "article_ready": false,
  "review_required_reason": "引用箇所の聴き取り確認待ち"
}
```

### 8-3. VID 素材カード（JSON 形式）

```json
{
  "card_type": "video",
  "source_file": "DOW-UAP-PR050_....mp4",
  "catalog_id": "DOW-UAP-PR050",
  "dvids_video_id": "XXXXXXX",
  "incident_date": "（DVIDS ページで確認要）",
  "incident_location": "（DVIDS ページで確認要）",
  "content_category": "video_evidence",
  "note_series": "DOW-UAP PR",
  "duration_sec": 123,
  "representative_frames": [
    {
      "timestamp_sec": 30,
      "file": "frame_extracts/DOW-UAP-PR050_.../frame_000030.png",
      "visual_observation": "（人間が記入）"
    }
  ],
  "sensor_type": "（画面表示より確認: IR / FMV / 不明）",
  "visual_observations": [],
  "supplementary_notes": "",
  "article_ready": false,
  "review_required_reason": "視覚観察記録の人間入力待ち"
}
```

### 8-4. 素材カードの格納先

```
worker_outputs/material_cards/
├── audio/
│   └── NASA-AUD-D001_card.json
└── video/
    └── DOW-UAP-PR050_card.json
```

### 8-5. 素材カードから記事ドラフトへの変換ルール

- `article_ready: true` かつ `review_required_reason: ""` のカードのみ記事化対象
- `confirmed_quotes` 内の `human_verified: true` の引用のみ記事に使用
- `visual_observations` は人間が記入した内容のみ（AI 自動生成は補足候補として別フィールドへ）

---

## 9. ローカル LLM で処理する部分と人間確認が必要な部分

### 9-1. 自動化可能（ローカル LLM・スクリプト）

| 処理 | ツール | 信頼度 |
|------|-------|--------|
| 音声ファイルの文字起こし（英文） | mlx-whisper | 高（人間確認前提） |
| 動画メタデータ取得（duration・bitrate・codec） | ffprobe | 高 |
| 代表フレーム抽出（固定間隔） | ffmpeg | 高 |
| 素材カード JSON の雛形生成 | Python スクリプト | 高 |
| 文字起こし信頼度スコアの集計・フラグ付け | Python スクリプト | 高 |
| files_catalog.csv との照合・カタログ情報の素材カードへの転記 | Python スクリプト | 高 |

### 9-2. 人間確認が必須

| 処理 | 理由 | 優先度 |
|------|------|-------|
| 文字起こし英文の正確性確認 | hallucination リスク・`[inaudible]` 判断 | 最高 |
| 代表フレームの選定（サムネイル候補） | 主観的判断・センセーショナル化防止 | 高 |
| 視覚観察の記述（VID フレーム） | 断定禁止ルール適用に人間判断が必要 | 高 |
| 素材カードの `article_ready` フラグの確定 | 品質ゲート | 高 |
| 日本語翻訳・要訳 | 文脈理解・ニュアンス・敬語 | 高 |
| `[inaudible]` 箇所の補完可否判断 | 文脈依存の難問 | 高 |
| DVIDS ページによる出典確認 | 外部サイト参照・機械化困難 | 中 |
| センサー種別（IR/FMV）の確定 | 映像目視が必要な場合あり | 中 |

### 9-3. AI 補助は可（ただし人間最終承認）

| 処理 | AI 活用方法 | 最終承認者 |
|------|-----------|----------|
| note 記事ドラフト生成 | 素材カードから Claude が下書き | 人間 |
| 難読な文字起こし箇所の補完候補提示 | AI が複数候補を提示（選択は人間） | 人間 |
| 視覚観察の文章化補助 | 人間の観察メモを AI が文章化 | 人間 |

---

## 10. 失敗時の停止ルール

### 10-1. 即時停止条件（STOP）

以下のいずれかが発生した場合、処理を即時停止し、エラーログを記録する。

| 条件 | 理由 |
|------|------|
| 入力ファイル（raw_media/）への書き込みが発生 | 素材保護 |
| 出力先ディスクの空き容量が 20GB 未満 | /Volumes/ACASIS_2TB の容量枯渇防止 |
| 連続 5件以上のエラー | スクリプトまたは環境の根本的な問題の可能性 |
| mlx-whisper が途中でクラッシュ（exit code != 0） | プロセス異常 |
| ffmpeg が出力ファイルを生成しない（0バイト出力） | 動画ファイル破損の可能性 |
| transcript.json の avg_confidence が 0.3 未満 | 音声品質が極端に低い |

### 10-2. スキップして継続可能な条件（WARN & SKIP）

| 条件 | 対応 |
|------|------|
| 特定ファイルのみ処理失敗（他は成功） | エラーログに記録し、そのファイルをスキップして継続 |
| avg_confidence が 0.5 以上 0.7 未満 | `low_confidence_flag: true` を付けて継続 |
| `inaudible_count` が多い（20% 超） | `review_required: true` を付けて継続 |
| フレーム抽出で特定フレームが破損 | そのフレームをスキップし、前後フレームで代替 |

### 10-3. 再実行時の resume 方針

- 処理済みファイルは output CSV の `source_file` 列で管理
- 再実行時は出力 CSV を読み込み、処理済みファイルをスキップ（PDF パイプラインと同方式）
- `--force` オプションで再処理強制（デフォルトはスキップ）

### 10-4. ロールバック方針

| 影響範囲 | ロールバック方法 |
|---------|----------------|
| transcripts/ 内のファイル | git で管理。不正ファイルは `git checkout` で復元可 |
| frame_extracts/ 内の .png | git 管理外。ディレクトリごと削除して再抽出 |
| worker_outputs/ 内の CSV | git で管理。不正 CSV は `git checkout` で復元可 |
| raw_media/ | 変更しない原則。変更された場合は即停止・報告 |

### 10-5. 人間への報告フォーマット（処理完了時）

```
=== [処理名] 完了レポート ===
処理件数   : XX / YY 件
スキップ   : ZZ 件（処理済み）
エラー     : NN 件
処理時間   : HH:MM:SS
出力先     : worker_outputs/[run_csv_path]
WARN 件数  : NN 件（内訳: low_confidence=X, review_required=Y）
STOP 発生  : なし / あり（理由: ...）
次のアクション: [Phase B 人間レビュー 等]
```

---

## 11. VID 記事レビュー用フレーム抽出ルール（Claude Code 単記事作業）

本節は Section 3「VID 代表フレーム抽出方針」（バッチパイプライン）とは別の、**Claude Code が個別記事作成時に実施するフレーム抽出**の運用ルールである。

### 11-1. 二つのフレーム抽出ワークフローの区別

| 区分 | 対象 | 実施者 | 保存先 | 命名規則 |
|------|------|-------|-------|---------|
| バッチパイプライン（Section 3） | 全78件一括 | Mac mini スクリプト | `frame_extracts/{video_stem}/` | `frame_{timestamp_sec:06d}.png`（6桁） |
| **記事レビュー用（本節）** | **1記事ごと** | **Claude Code** | **`thumbnails/{media_slug}/`** | **`frame_{seconds:04d}.png`（4桁）** |

### 11-2. 保存先・命名規則（記事レビュー用）

```
thumbnails/
└── {media_slug}/           ← catalog_id と一致させる（例: DOW-UAP-PR051）
    ├── frame_0005.png      ← 00:05 時点のフレーム（PNG, 元解像度）
    ├── frame_0015.png      ← 00:15 時点
    └── frame_0270.png      ← 04:30 時点（270秒）
```

- **ディレクトリ:** `thumbnails/{media_slug}/`（リポジトリルート直下）
- **形式:** PNG（可逆圧縮・元解像度維持）
- **命名:** `frame_{秒数:04d}.png`（4桁ゼロ埋め。例：5秒 → `frame_0005.png`、270秒 → `frame_0270.png`）
- **/tmp 使用禁止:** `/tmp` を最終保存先にしてはならない。Claude Code セッション外からアクセス不可能になるため。

### 11-3. ffmpeg コマンドテンプレート

```bash
# 特定時刻のフレームを抽出（指定秒数）
MEDIA_SLUG="DOW-UAP-PR051"
VIDEO="raw_media/video/${MEDIA_SLUG}_*.mp4"
mkdir -p "thumbnails/${MEDIA_SLUG}"

# 例：5秒時点と270秒時点を抽出
ffmpeg -ss 00:00:05 -i $VIDEO -vframes 1 -y "thumbnails/${MEDIA_SLUG}/frame_0005.png"
ffmpeg -ss 00:04:30 -i $VIDEO -vframes 1 -y "thumbnails/${MEDIA_SLUG}/frame_0270.png"
```

### 11-4. フレーム選定の考え方

記事レビュー用フレームは以下の目的で抽出する。

| 目的 | 説明 |
|------|------|
| 視覚観察記録 | 記事化前の事実確認（物体の位置・形状・映像構成の把握） |
| note 記事添付画像候補 | 記事に埋め込む画像①②の素材。note に直接アップロードする |
| Codex 審査用の参考 | 視覚断定の根拠確認（Codex 自体は画像を受け取らないが、記述の根拠となる） |

選定は人間が行う。AI による自動選定は使用しない。

### 11-5. 記事内での参照方法

note 記事ドラフト（`note_drafts/`）内で画像を参照する際は以下の形式を使用する。

```
【画像①】thumbnails/DOW-UAP-PR051/frame_0005.png
```

note 投稿時は `thumbnails/{media_slug}/frame_{秒数:04d}.png` をアップロードし、
記事内に埋め込む（note の画像管理機能を使用）。

### 11-6. 遵守チェック（記事作成開始前に確認）

- [ ] `thumbnails/{media_slug}/` ディレクトリが存在するか確認
- [ ] フレームが `/tmp` 以下に保存されていないことを確認
- [ ] ファイル名が `frame_{秒数:04d}.png` 形式であることを確認
- [ ] PNG 形式であることを確認（JPEG / WebP は使用しない）

### 11-7. 参照実績

| 記事 | media_slug | 抽出フレーム数 | 記事使用フレーム |
|------|-----------|-------------|--------------|
| #R02-008 DOW-UAP-PR050 | DOW-UAP-PR050 | 4 | frame_0000.png, frame_0009.png |
| #R02-009 DOW-UAP-PR051 | DOW-UAP-PR051 | 6 | frame_0005.png, frame_0270.png |

---

## 改訂履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| v1 | 2026-05-29 | 初版制定（Release 02 音声・映像パイプライン設計）|
| v1.1 | 2026-05-30 | Section 6-5「長時間処理の実行方式」追加（tmux推奨・exit code 255 誤報対策）|
| v1.2 | 2026-06-14 | Section 11「VID 記事レビュー用フレーム抽出ルール」追加（/tmp 禁止・thumbnails/ 正式保存先・4桁命名規則）|
