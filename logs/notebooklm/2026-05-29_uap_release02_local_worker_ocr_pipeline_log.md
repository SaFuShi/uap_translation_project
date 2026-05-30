# UAP翻訳プロジェクト 作業ログ
## 2026-05-29〜30 ｜ Release 02 対応・Mac mini ローカルワーカー化・OCR全件処理完了

---

## 1. 本日の目的

米国政府が公開している UAP（未確認空中現象）関連の機密解除文書を日本語に翻訳・要約し、note に公開するプロジェクトの「Release 02」対応として、以下を完結させることが目標だった。

- **Mac mini を PDF・動画・音声の一次処理専用マシン（ローカルワーカー）として整備する**
- **全 PDF ファイル（124本・4,289ページ）のテキスト抽出（OCR）を完了する**
- **OCR 結果を分析し、次の記事化作業に向けた下準備（分類・レビュー）を整える**

Release 01 では PDF だけを扱っていたが、Release 02 からは動画（78本）・音声（8本）・画像（14本）が加わるため、処理量が大幅に増える。この増加に対応するため、Mac Studio（記事制作・Git 管理の司令塔）と Mac mini（重い処理を担う作業者）に役割を分けた。

---

## 2. 現在の整理

### Mac Studio の役割（司令塔・編集・公開）

| 役割 | 内容 |
|------|------|
| 全体の指揮 | どの処理を行うか・記事をどう構成するかを決める |
| Git 管理 | ファイルの変更履歴の管理・GitHub への保存は Mac Studio だけで行う |
| 記事の最終編集 | 翻訳・要約・note 記事の仕上げ |
| note 投稿 | 公開作業は Mac Studio（または人間）が行う |
| Claude Code 連携 | AI（Claude）への指示・レビュー依頼 |

### Mac mini / agentai アカウントの役割（素材処理ワーカー）

| 役割 | 内容 |
|------|------|
| OCR（テキスト化） | PDF をスキャンして文字を取り出す処理 |
| 画像変換 | PDF の各ページを画像ファイルに変換する |
| 動画フレーム抽出 | 動画から代表的な静止画を取り出す（将来実装予定） |
| 音声文字起こし | 音声ファイルをテキスト化する（将来実装予定） |
| 夜間バッチ処理 | 人間が寝ている間に重い処理を実行する |

**Mac mini では行わないこと：** note 本文の生成・記事の公開判断・Git へのコミット・push

### 外付けSSD（ACASIS 2TB）の保存場所

Mac mini には 2TB の外付けSSD（ACASIS 2TB）が接続されており、大容量の素材ファイルを保存している。

```
/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/
├── repo/          ← Git リポジトリ（GitHub と同期）
├── raw_pdf/       ← PDF 本体（124本・約2.4GB）
├── raw_media/     ← 動画・音声・画像（100本）
├── page_images/   ← PDF → 画像変換後のファイル（4,289枚・15.65GB）
├── extracted_text/ ← OCR 結果
└── logs/          ← 処理ログ
```

### リポジトリ（Git で管理するファイルの場所）

- **GitHub（クラウド）:** `https://github.com/SaFuShi/uap_translation_project`
- **Mac Studio 上:** `/Users/fukudasatoshi/Documents/UAP_TRANSLATION_PROJECT/`
- **Mac mini 上:** `/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/repo/`

### raw素材の保存場所

| 種別 | 場所 | 件数 |
|------|------|------|
| PDF | Mac mini の外付けSSD `raw_pdf/` | 124本（約2.4GB） |
| 動画 | Mac mini の外付けSSD `raw_media/video/` | 78本（DOW-UAP PR シリーズ） |
| 音声 | Mac mini の外付けSSD `raw_media/audio/` | 8本（NASA Apollo・Mercury等） |
| 画像 | Mac mini の外付けSSD `raw_media/image/` | 14本（FBI フォト・NASA写真） |

**raw素材は Git 管理しない。**（容量が大きすぎるため・war.gov の公開資料なので紛失しても再取得可能）

---

## 3. 実施した作業

### 3-1. Mac mini ローカルワーカー化

Mac mini の `agentai` アカウントに、処理に必要なソフトウェアを整備した。

- **Homebrew（パッケージ管理ツール）:** `/opt/homebrew/` にインストール済み
- **Python 仮想環境（venv）:** プロジェクト専用の Python 環境を `/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/.venv/` に構築
- **Tesseract OCR:** 画像から文字を読み取るエンジン。Homebrew でインストール・英語データ確認済み
- **symlink（ショートカット）設定:** repo 内から外付けSSD の `raw_pdf/` を参照できるよう symlink を設定

### 3-2. raw_pdf / raw_media の移行

Mac Studio から Mac mini へ、PDF・動画・音声・画像ファイルを転送した。

- 転送方法: `rsync`（ファイルのコピーツール。差分のみ転送・チェックサムで一致確認）
- PDF 124本、raw_media 100本を転送・件数・サイズを確認して完了

### 3-3. テキスト層検出（detect_text_layer.py）

PDF には2種類ある。「はじめからテキストとして読める PDF」と「紙をスキャンした画像だけの PDF」だ。OCR（光学的文字認識）が必要なのは後者のみ。

- `detect_text_layer.py` を全件実行し、各 PDF・各ページが OCR 必要か不要かを自動判定
- 結果を `metadata/text_layer_report.csv` に保存（4,289ページ分）
- has_text_layer=false（OCR 必要）: 3,596ページ（83.8%）
- has_text_layer=true（テキスト抽出で OK）: 642ページ（15.0%）

### 3-4. page_classification.csv の生成

OCR をどのように実行するかを管理するための分類ファイルを、4,289ページ全件分作成した。

- `build_page_classification.py` を新規作成・実行
- テキスト層検出結果をもとに、各ページの「OCR 推奨・スキップ・要レビュー」を自動判定
- 既存の手動分類 184行を保持しつつ、4,105行を自動追加
- 結果: `classification/page_classification.csv`（4,289行）

### 3-5. pdf_to_images.py 全件実行

OCR エンジン（Tesseract）は画像ファイルを入力として受け取るため、PDF の各ページを PNG 画像に変換する作業が必要だった。

- `pdf_to_images.py` に `--limit`（テスト用上限）などのオプションを追加し安全性を高めてから全件実行
- 結果: 4,289枚の PNG 画像ファイルを生成（15.65GB・エラー 0件）
- 保存先: Mac mini 外付けSSD `page_images/{PDF名}/page_{番号}.png`

### 3-6. run_ocr.py 全件 OCR 実行

4,289ページのうち、OCR が必要な 3,615ページに対して Tesseract OCR を実行した。

- 事前に `--limit 20` で 20ページのテスト実行を行い、動作・出力品質を確認してから全件実行
- 処理時間: 約98分（21:52 開始 → 23:30 完了）
- 処理速度: 約 30.7ページ/分
- エラー件数: 0件
- 出力: `extracted_text/ocr_results_full_20260529_215201.csv`（3.4MB・3,615行）

### 3-7. OCR 結果レビュー

全件 OCR 結果を Python で集計・分析した。

- 信頼度（confidence）平均: **79.6**（中央値 86.9）
- 信頼度 80 以上のページ: 2,377件（66%）→ 大半は高品質
- 信頼度 50 未満のページ: 411件（11%）→ 要確認
- 0文字ページ: 581件（白紙・図版・手書き等でテキストなし）
- OCR Challenge Pipeline（再処理検討）候補: 849件

### 3-8. worker_outputs 生成

OCR レビューの結果を、Git 管理できる軽量 CSV ファイルにまとめた。

- `worker_outputs/ocr_review_summary_20260529.csv`: PDF 単位のサマリ（77行・7.5KB）
- `worker_outputs/ocr_challenge_candidates_20260529.csv`: 再処理候補ページ一覧（849行・78KB）

### 3-9. 設計書整備

作業を通じて得た知見をもとに、以下の設計書を新規作成・更新した。

- `docs/macmini_uap_local_worker_design.md`（更新）: 長時間処理は tmux で Mac mini 自走・成否判定方法を追記
- `docs/ios_remote_monitoring_design.md`（新規）: iPhone/iPad からの作業状況監視の設計
- `docs/release02_audio_video_pipeline_design.md`（新規）: 音声・映像処理パイプラインの設計

---

## 4. 重要な判断

### Claude Code は長時間処理を「握らない」

Claude Code（AI アシスタント）のバックグラウンドタスク機能を使って Mac mini に処理させる方法を試みたが、処理途中で SSH 接続が切断されて「失敗」と報告されることがあった（後述）。

**方針転換:** OCR・Whisper（音声文字起こし）・ffmpeg（動画処理）などの長時間処理は、Mac mini 上で `tmux`（セッション管理ツール）を使い、SSH が切断されても処理が続くように実行する。Claude Code は「起動の指示・進捗確認・結果確認」のみを担う。

### OCR 結果の全文 CSV は Git 管理しない

OCR 結果の本体（`ocr_results_full_20260529_215201.csv`・3.4MB）は Git に含めない。

**理由:**
- Git は差分（変更された部分）を管理するツールだが、大きなテキストファイルは差分管理と相性が悪い
- 再実行すれば同じ結果が得られる（再現可能）
- リポジトリが肥大化するとクローン・プル操作が遅くなる

**代わりに:** PDF 単位のサマリ CSV と再処理候補 CSV（合計 86KB）だけを Git 管理する。

### raw素材は Git 管理しない

PDF・動画・音声・画像ファイルは Git で管理しない。

**理由:** 合計 9GB 超の素材を Git に入れるとリポジトリが使い物にならなくなる。war.gov の公開資料なので、必要な場合は再ダウンロードできる。

### 軽量サマリのみ Git 管理候補

Git に入れるのは「軽量・テキスト形式・人間が読める・差分が意味を持つ」ファイルのみ。具体的には:
- 分類 CSV（`page_classification.csv` 等）
- 処理サマリ CSV（`worker_outputs/` 内）
- 設計書・ドキュメント（`docs/` 内）
- スクリプト（`scripts/` 内）

---

## 5. 発生した問題と対応

### 問題: Claude Code バックグラウンドタスクが「failed」と報告した

OCR 全件処理をバックグラウンドで実行中、Claude Code のハーネス（タスク管理機能）が SSH 接続切断を検知して「exit code 255 / failed」と報告した。

**実際の状況:** Mac mini 上の Python スクリプトは SSH 切断後も継続して動作しており、約98分後に正常に全件処理を完了し、CSV ファイルを出力していた。

**判定方法:** exit code（終了コード）だけで成否を判断するのは危険。以下の複数指標で確認する。
1. `ps aux | grep run_ocr` → プロセスが終了しているか
2. 出力 CSV ファイルが存在するか・サイズは正常か
3. ログの末尾にエラーがないか
4. Python でデータ行数をカウントして期待値と一致するか
5. MD5（ファイルの指紋）を転送元と転送先で比較する

**今後の対策:** 長時間処理は tmux セッション内で実行し、SSH 切断の影響を受けないようにする。

### 問題: Mac mini が GitHub に push できなかった

Mac mini からは GitHub への認証情報が設定されておらず、コード変更を直接 push できなかった。

**対応:** Mac mini でスクリプト変更 → Mac Studio に scp（ファイル転送）→ Mac Studio から commit/push → Mac mini で git pull という流れに統一。この運用を設計書に明記した。

---

## 6. 成果物

| ファイル | 内容 | 場所 |
|---------|------|------|
| `metadata/text_layer_report.csv` | 4,289ページのテキスト層有無の検出結果 | Git 管理（Mac Studio / Mac mini 共通）|
| `classification/page_classification.csv` | 4,289ページの OCR 処理方針分類 | Git 管理 |
| `page_images/`（4,289枚・15.65GB） | PDF → PNG 変換済み画像 | Mac mini 外付けSSD のみ |
| `extracted_text/ocr_results_full_20260529_215201.csv` | OCR 全件結果（3,615ページ・3.4MB） | Mac mini 外付けSSD＋Mac Studio local（Git 管理外）|
| `worker_outputs/ocr_review_summary_20260529.csv` | PDF 単位 OCR サマリ（77行・7.5KB） | Git 管理 |
| `worker_outputs/ocr_challenge_candidates_20260529.csv` | 再処理候補ページ一覧（849行・78KB） | Git 管理 |
| `docs/macmini_uap_local_worker_design.md` | Mac mini ワーカー設計書（更新） | Git 管理 |
| `docs/ios_remote_monitoring_design.md` | iPhone/iPad 監視設計書（新規） | Git 管理 |
| `docs/release02_audio_video_pipeline_design.md` | 音声・映像パイプライン設計書（新規） | Git 管理 |

---

## 7. Git commit 一覧

| commit hash | メッセージ | 内容 |
|------------|-----------|------|
| `220f1d5` | feat: add safe test options to PDF image converter | `pdf_to_images.py` に `--limit` 等のテスト用オプションを追加 |
| `9ca025c` | feat: add generated page classification workflow | `page_classification.csv` を全4,289ページ分に拡充・`build_page_classification.py` 追加 |
| `f42314f` | docs: update local worker and media pipeline operations | 設計書3本追加・`run_ocr.py` に `--limit` オプション追加 |
| `db85e03` | chore: ignore raw_pdf symlink | `.gitignore` の `raw_pdf/` を `raw_pdf`（symlink 対応）に修正 |
| `9b478c7` | chore: ignore full OCR result CSVs | `.gitignore` に `ocr_results_full_*.csv` を追加 |
| `14562df` | chore: add OCR review worker outputs | OCR レビューサマリ・Challenge 候補 CSV を `worker_outputs/` に追加 |

---

## 8. 次にやること

### 短期（次回作業）

- **OCR Challenge Pipeline 候補のレビュー**
  - `worker_outputs/ocr_challenge_candidates_20260529.csv` の 849件を確認
  - 特に `65_hs1-834228961_62-hq-83894_section_*`（FBI 系文書）の再処理方針を決める
  - 0文字ページ 581件のうち「白紙・図版」と「本当に読めない」を仕分ける

- **PDF 記事化候補の選定**
  - OCR 品質が高く（conf 平均 ≥ 80）、ページ数が少ない PDF から記事化を開始
  - 有力候補: NASA Skylab・Apollo 11 デブリーフィング、DOW-UAP ミッションレポートシリーズ

### 中期

- **AUD 音声文字起こし PoC（小規模テスト）**
  - mlx-whisper（Apple Silicon 最適化の音声認識）を Mac mini にインストール
  - NASA 音声 1〜3件で動作確認
  - 設計書（`docs/release02_audio_video_pipeline_design.md`）の手順に従う

- **VID 代表フレーム抽出 PoC**
  - ffmpeg（動画処理ツール）で DOW-UAP 動画 1件から代表フレームを抽出
  - 視覚観察記録のフォーマットを確認

- **iPhone/iPad 監視環境の実装検討**
  - `docs/ios_remote_monitoring_design.md` の設計に基づき、tmux・SSH アプリの設定を実装
  - Blink Shell または Termius の導入・SSH 鍵の生成

---

## 9. 注意点

### このログを NotebookLM に入れる際の注意

- **API キー・パスワード・認証情報は記載していない**（記載禁止）
- **raw素材（PDF 本体・動画・音声）の内容はこのログに含まれていない**（素材はあくまで war.gov 公開資料だが、未処理の生データを NotebookLM に入れるのは避ける）
- **大容量 OCR 全文 CSV は NotebookLM への転記対象にしない**（3.4MB のテキスト全量を入れると有用な要約が得られにくい。サマリ CSV を使うこと）

### 事実と推測の区別

- **事実:** OCR を 3,615ページ処理した・エラー 0件・confidence 平均 79.6 など数値で確認できるもの
- **推測:** `65_hs1-834228961` が「FBI 系文書」であること（ファイル名からの推定。war.gov の公開ページで確認が必要）
- **判断:** 「Git 管理しない」「tmux を使う」などの運用判断（根拠を上記に記述済み）

---

## 改訂履歴

| バージョン | 日付 | 内容 |
|----------|------|------|
| v1 | 2026-05-30 | 初版作成 |
