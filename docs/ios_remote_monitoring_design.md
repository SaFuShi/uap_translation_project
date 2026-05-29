# iPhone/iPad リモート監視設計書 v1

**制定日:** 2026-05-29
**目的:** Mac Studio の前にいない時でも iPhone/iPad から作業状況を確認し、軽い Yes/No 承認・ログ確認ができる運用を設計する
**ステータス:** 設計のみ（SSH設定変更・tmuxインストール・launchd設定・実装・git commit は未実施）

---

## 0. 設計の前提

### 環境構成

| 機器 | 役割 | ホスト名 |
|------|------|---------|
| Mac Studio | git hub・Claude Code 実行環境・記事制作 | `mac-studio.local` |
| Mac mini（M4 Pro） | OCR バッチ・Whisper・ffmpeg ワーカー | `mac-mini.local` |
| iPhone / iPad | 監視端末（読み取り中心・承認操作のみ） | — |

### 基本原則

- **読み取り中心:** iPhone/iPad からの主な操作はログ確認・状況把握
- **破壊的操作は禁止:** `rm` / `mv` / `git reset` 等はモバイルから行わない
- **全件処理開始は禁止:** 長時間バッチはデスクの前で起動する
- **小画面での誤操作防止:** タップミスが致命的な操作につながらないように設計する

---

## 1. iPhone/iPad から監視したい対象

| 監視対象 | 機器 | 重要度 | 監視頻度の目安 |
|---------|------|-------|--------------|
| Claude Code 作業画面 | Mac Studio | 最高 | 作業中はリアルタイム |
| Codex 監査作業 | Mac Studio | 高 | 1時間ごとに確認 |
| Mac mini OCR ログ | Mac mini | 高 | 30分ごとに確認 |
| 夜間バッチログ（OCR / Whisper） | Mac mini | 中 | 朝に1回確認 |
| git log / コミット状況 | Mac Studio | 中 | 作業完了後に確認 |
| ディスク使用量（ACASIS_2TB） | Mac mini | 中 | バッチ前後に確認 |

---

## 2. 推奨方式

### 2-1. SSH アプリ（モバイル SSH クライアント）

**推奨アプリ:**

| アプリ名 | プラットフォーム | 特徴 |
|---------|---------------|------|
| **Blink Shell** | iOS/iPadOS | ハードウェアキーボード対応・tmux 統合・Mosh 対応 |
| **Termius** | iOS/iPadOS | GUI が直感的・接続プロファイル管理・チーム共有不要なら無料プランで可 |
| **a-Shell** | iOS/iPadOS | ローカル shell（SSH クライアントとしても使用可）|

**推奨: Blink Shell**（tmux との相性が最良・バックグラウンド接続維持が優秀）

### 2-2. tmux（ターミナルマルチプレクサ）

tmux を使う理由:

- SSH 接続が切断されてもセッションが残る（モバイルのネットワーク切断対策）
- 複数ウィンドウを1接続で管理できる（Claude Code・ログ・git 等を並列表示）
- セッション名で目的を明示できる（後述の命名規則を参照）

**基本的な使い方（読み取り専用パターン）:**

```bash
# 既存セッション一覧を確認
tmux ls

# セッションにアタッチ（読み取り専用）
tmux attach-session -t claude-code

# デタッチ（セッションを維持したまま切断）
Ctrl-b d
```

### 2-3. tail -f によるログ確認

リアルタイムログ確認コマンド（iPhone から実行可能な読み取り操作）:

```bash
# Mac mini OCR ログ（最新バッチ）
tail -f /path/to/logs/ocr/ocr_run_YYYYMMDD_HHmmss.log

# Mac mini Whisper ログ（将来）
tail -f /path/to/logs/whisper/whisper_run_YYYYMMDD_HHmmss.log

# バッチ完了確認（最終行を確認）
tail -20 /path/to/logs/ocr/ocr_run_YYYYMMDD_HHmmss.log

# ディスク使用量確認
df -h /Volumes/ACASIS_2TB
```

---

## 3. Mac Studio / Mac mini の使い分け

### 3-1. 接続先の選択基準

| 確認したい内容 | 接続先 |
|-------------|-------|
| Claude Code の作業・プロンプト入力 | Mac Studio |
| Codex 監査・記事ドラフトレビュー | Mac Studio |
| git log / コミット確認 | Mac Studio |
| OCR バッチ進捗・ログ | Mac mini |
| Whisper 文字起こし進捗・ログ（将来） | Mac mini |
| ffmpeg フレーム抽出進捗・ログ（将来） | Mac mini |
| ディスク使用量（ACASIS_2TB） | Mac mini |

### 3-2. 同時接続の考え方

- iPhone の画面は小さいため、1接続・1ウィンドウを基本とする
- iPad では Blink Shell の分割表示を使い、Mac Studio + Mac mini を同時表示も可
- どちらに接続するかを tmux セッション名で判断できるように命名する（後述）

---

## 4. セッション命名規則

### 4-1. Mac Studio 上の tmux セッション名

| セッション名 | 用途 |
|------------|------|
| `claude-code` | Claude Code のメイン作業画面 |
| `codex-audit` | Codex 監査・レビュー作業 |
| `git-watch` | git log / git status 監視 |
| `article-draft` | note 記事ドラフト編集 |

### 4-2. Mac mini 上の tmux セッション名

| セッション名 | 用途 |
|------------|------|
| `ocr-batch` | OCR バッチ処理（run_ocr.py） |
| `whisper-batch` | Whisper 文字起こしバッチ（将来） |
| `ffmpeg-batch` | ffmpeg フレーム抽出バッチ（将来） |
| `log-tail` | 各種ログの tail -f 専用セッション |

### 4-3. 命名ルール

- 全て小文字・ハイフン区切り
- 役割が一目でわかる名前（`batch1` / `session2` 等の連番禁止）
- バッチセッションは処理完了後も残す（`tmux ls` で完了確認できるように）

---

## 5. 読み取り中心の安全運用

### 5-1. 読み取り専用モードでの tmux アタッチ

```bash
# 読み取り専用でアタッチ（キー入力がセッションに影響しない）
tmux attach-session -r -t ocr-batch
```

`-r` フラグにより、タップ・スワイプによる誤入力がセッションに送信されない。
**iPhone から既存バッチセッションを監視する際は常に `-r` を付ける。**

### 5-2. ログファイルの直接参照

バッチセッションにアタッチせず、ログファイルを `tail -f` で確認する方式の方が安全:

```bash
# 専用の log-tail セッションを作り、ログ確認はそこで行う
tmux new-session -d -s log-tail
tmux send-keys -t log-tail "tail -f /path/to/logs/ocr/latest.log" Enter
```

これにより、バッチセッション本体への誤操作リスクを排除する。

### 5-4. Claude Code は実行主体ではなく監視役

長時間処理（OCR・Whisper・ffmpeg）は **tmux または nohup で Mac mini 側が自律実行する**。Claude Code は起動指示・進捗確認・結果確認のみを担当し、処理そのものを制御しない。

| Claude Code の役割 | 内容 |
|------------------|------|
| 起動指示 | tmux 起動コマンドを生成・説明する |
| 進捗確認 | SSH 経由でログ・プロセスを読み取る（読み取り専用） |
| 結果確認 | 処理完了後に CSV 行数・エラー件数・conf 統計を集計する |
| 成否判定 | exit code だけでなく複数指標で確認する（後述）|

**Claude Code バックグラウンドタスクの `failed` は SSH 断を示すのみ。Mac mini 側プロセスの成否とは無関係の場合がある。**

### 5-5. iPhone/iPad から成否を確認する手順

Claude Code のタスクが `failed` を返した場合、iPhone から SSH してプロセス実態を確認する。

```bash
# Step 1: プロセスが終了しているか確認
ps aux | grep run_ocr | grep -v grep
# → 出力なし = 終了済み、出力あり = 稼働中

# Step 2: 出力ファイルが存在するか確認
ls -lh extracted_text/ocr_results_full_*.csv

# Step 3: ログ末尾を確認（完了 or エラー）
tail -20 logs/ocr/ocr_run_YYYYMMDD_HHmmss.log

# Step 4: 出力 CSV の行数を確認
python3 -c "import csv; f=open('extracted_text/ocr_results_full_YYYYMMDD_HHmmss.csv'); print(sum(1 for _ in csv.DictReader(f)), 'rows')"
```

これら 4 ステップ全てを確認してから成否を判断する。**exit code 255 のみで失敗と判断しない。**

---

### 5-3. SSH 接続確立後の最初の操作

iPhone から SSH 接続した直後は必ず以下を確認してから操作する:

1. `tmux ls` でセッション一覧を確認
2. 目的のセッションが動作中か確認
3. 読み取り専用が必要なら `-r` でアタッチ
4. ログ確認のみなら `log-tail` セッションを使用

---

## 6. iPhone/iPad で許可する操作

### 6-1. 状況確認操作（常時許可）

```bash
tmux ls                          # セッション一覧
tail -f logs/ocr/latest.log      # ログのリアルタイム確認
tail -20 logs/ocr/latest.log     # ログの末尾確認
df -h /Volumes/ACASIS_2TB        # ディスク使用量確認
ps aux | grep python             # プロセス稼働確認
git log --oneline -10            # 最新コミット確認
git status                       # 作業ツリー状態確認
```

### 6-2. Yes/No 承認操作（慎重に許可）

Claude Code が承認待ちになった場合にのみ:

- `y` + Enter（承認）
- `n` + Enter（拒否）

**条件:** 画面を読んで内容を理解した上でのみ。内容が読めない・不明な場合は拒否 (`n`) を選ぶ。

### 6-3. 軽い停止指示（許可・ただし慎重に）

```bash
Ctrl-c     # 実行中プロセスの停止（tmux ウィンドウ内で）
```

**バッチ処理を停止する場合は resume 可能かを事前確認する。**
run_ocr.py は resume 対応しているため停止後の再実行で途中から再開できる。

---

## 7. iPhone/iPad で避ける操作

### 7-1. 絶対に行わない操作

| 操作 | 理由 |
|------|------|
| `rm -rf` / `rm` | 誤タップで素材・ログを削除するリスク |
| `mv` / `cp` で本番ファイルを操作 | パス入力ミスで意図しない場所へ移動 |
| `git reset --hard` | コミット済み内容の消失リスク |
| `git push --force` | リモートへの強制上書き |
| `chmod` / `chown` | 権限設定の誤変更 |
| `sudo` を含む操作 | システム設定の誤変更 |

### 7-2. 作業開始操作は行わない

| 操作 | 理由 |
|------|------|
| 全件バッチの開始（OCR / Whisper / ffmpeg） | 長時間・大容量処理はデスクの前で開始する |
| note 記事の投稿 | 最終確認が必要・モバイルでの投稿ミスリスク |
| 新しい Python スクリプトの実行 | 想定外の出力・エラーへの対応ができない |
| Claude Code への長文プロンプト入力 | 誤字・指示ミスのリスクが高い |
| git commit / git add | コミットメッセージの品質維持のため |

### 7-3. 小画面特有の注意

- 補完候補の誤タップ（`rm logs/*` を `rm raw_media/*` と誤入力等）
- SSH セッション名の混同（Mac Studio / Mac mini の接続先確認を必ず行う）
- tmux のキーバインド誤操作（`Ctrl-b :kill-session` 等の誤実行）

---

## 8. 誤操作防止ルール

### 8-1. ターミナル設定（Mac 側の設定 / 実装時に対応）

```bash
# .zshrc または .bashrc に追加（Mac Studio / Mac mini 両方）
# 破壊的コマンドの確認プロンプト
alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'
```

**注意: これらの alias は対話用シェル（`.zshrc` / `.bashrc`）にのみ追加すること。**

- `alias rm='rm -i'` を `.zshrc` に書いた場合、シェルスクリプト（`#!/bin/bash` や `#!/usr/bin/env python` 内の `os.remove` 等）には**影響しない**。alias はインタラクティブシェルセッション内でのみ有効。
- Python スクリプト・バッチ処理スクリプト（`run_ocr.py` 等）が内部で `subprocess.run(["rm", ...])` を呼ぶ場合も alias は適用されない。スクリプト側の安全設計（出力先の明示・上書き防止フラグ等）と混同しないこと。
- `BASH_ENV` や `ENV` 変数でスクリプト実行環境に `.bashrc` を読み込ませる設定がある場合、alias が意図せず適用されることがあるため注意する。

### 8-2. 誤った成否判定を防ぐ運用ルール

Claude Code のバックグラウンドタスクが `failed` を返した場合でも、**Mac mini 側プロセスが正常完了している可能性がある**（exit code 255 = SSH 断のみを示す）。

iPhone からの確認手順:

1. `ps aux | grep python` → プロセスなし = 終了済み
2. `ls -lh extracted_text/*.csv` → 出力ファイルの存在・サイズを確認
3. `tail -20 logs/ocr/最新ログ.log` → エラーか完了かを確認
4. 全て正常 → **実質成功**。Claude Code の `failed` は SSH 断による誤報

**iPhone から絶対にやってはいけない確認方法:**
- 「failed だから再実行する」という即断 → resume 方式でも意図しない重複が発生しうる
- 再実行前に必ず 1〜3 の確認を完了すること

---

### 8-3. tmux 設定（実装時に対応）

```
# ~/.tmux.conf
# マウス操作を制限（誤スクロールによるコマンド入力防止）
set -g mouse off

# セッション確認プロンプト（kill 操作前に確認）
bind-key x confirm-before -p "kill-pane #P? (y/n)" kill-pane
bind-key X confirm-before -p "kill-session #S? (y/n)" kill-session
```

### 8-4. 接続確認プロンプト（SSH 接続先の明示）

```bash
# Mac Studio .zshrc: ホスト名をプロンプトに表示
PS1='[MAC-STUDIO] %n@%m %~$ '

# Mac mini .zshrc: ホスト名をプロンプトに表示
PS1='[MAC-MINI] %n@%m %~$ '
```

接続後すぐにどちらのマシンに接続しているか視覚的に確認できる。

### 8-5. 操作前の確認チェックリスト

iPhone/iPad から操作する前に:

1. **接続先確認:** プロンプトの `[MAC-STUDIO]` / `[MAC-MINI]` を確認
2. **セッション確認:** `tmux ls` で目的のセッションを確認
3. **バッチ稼働中確認:** バッチが稼働中の場合、そのセッションへの入力は避ける
4. **操作内容確認:** 実行するコマンドを入力前にもう一度読む

---

## 9. SSH 鍵・認証まわりの注意

### 9-1. 推奨認証方式

| 方式 | 推奨度 | 理由 |
|------|-------|------|
| SSH 公開鍵認証 | 最推奨 | パスワード不要・セキュリティ高 |
| パスワード認証 | 非推奨 | 覗き見リスク・入力ミスリスク |
| パスワード + TOTP | 許容 | 追加レイヤーだが iPhone 入力は煩雑 |

### 9-2. iPhone/iPad 専用の SSH 鍵の作成

iPhone/iPad 専用の鍵ペアを作成し、デスクトップ環境の鍵と分離する。

```bash
# iPhone 専用鍵の生成（Mac 上で実行・鍵は iPhone の SSH アプリに取り込む）
ssh-keygen -t ed25519 -C "iphone-monitoring-key" -f ~/.ssh/id_iphone_monitoring
```

- iPhone 専用鍵の `authorized_keys` への追加は Mac Studio / Mac mini 両方に行う
- iPhone を紛失した場合は即座にその鍵を `authorized_keys` から削除する

### 9-3. authorized_keys の管理

```bash
# authorized_keys に iPhone 鍵を追加
cat ~/.ssh/id_iphone_monitoring.pub >> ~/.ssh/authorized_keys

# コメントを明示的に記載（どの鍵か識別できるように）
# ssh-ed25519 AAAA... iphone-monitoring-key
```

### 9-4. ネットワーク条件

| 接続先 | ローカル（自宅 Wi-Fi）| 外出先（4G/5G） |
|--------|---------------------|----------------|
| Mac Studio | SSH（ポート 22）| Tailscale / ZeroTier 等の VPN 経由を推奨 |
| Mac mini | SSH（ポート 22）| Tailscale / ZeroTier 等の VPN 経由を推奨 |

**外出先からの接続には VPN を使用する（直接ポート開放はしない）。**

### 9-5. Mosh の活用（推奨）

Mosh（mobile shell）は不安定なモバイル回線での SSH の代替として優秀:

- 接続が切れてもセッションが維持される（tmux との二重保護）
- 4G/5G の IP アドレス変化に対応
- Blink Shell は Mosh に対応

Mac Studio / Mac mini 側に `mosh-server` をインストールする必要あり（実装時に対応）。

---

## 10. 将来的な Web ダッシュボード化候補

### 10-1. 軽量ダッシュボード案

SSH + tmux による監視は強力だが、技術的ハードルが高い。将来的には以下のような Web UI を検討する。

| ツール | 概要 | メリット |
|-------|------|---------|
| **ttyd** | ターミナルを Web ブラウザで表示 | Safari から URL アクセスするだけ |
| **uptime-kuma** | サービス死活監視ダッシュボード | プロセス稼働状況を可視化 |
| **Grafana** | ログ・メトリクス可視化 | OCR 進捗・ログをグラフで表示 |
| **カスタム Flask アプリ** | Mac Studio 上で起動する簡易 Web UI | プロジェクト特化の承認フロー実装可能 |

### 10-2. ttyd による最小ダッシュボード（最も実装コストが低い）

```bash
# ttyd のインストール（Homebrew）
brew install ttyd

# 特定 tmux セッションを Web で公開（読み取り専用）
ttyd --readonly tmux attach-session -t log-tail
```

Safari で `http://mac-studio.local:7681` にアクセスするだけで tmux セッションを確認できる。
読み取り専用オプション（`--readonly`）により、誤入力が排除される。

**セキュリティ注意:** ttyd はパスワード認証なしでポートを開けるため、自宅 LAN 内のみの利用を前提とする。外部公開する場合は認証設定または VPN 経由が必須。

### 10-3. 将来の承認フロー自動化候補

| 機能 | 実現方法 | 優先度 |
|------|---------|-------|
| バッチ完了通知 | `terminal-notifier` / Mac 通知 → Shortcuts 経由で iPhone 通知 | 中 |
| Yes/No 承認 Web UI | Flask + Claude Code カスタムフック | 低（現状 SSH で十分） |
| ログ検索・フィルタ | Grafana Loki + モバイルアプリ | 低（過剰実装） |
| 自動エラー通知 | バッチスクリプトのエラー時に notify-send | 中 |

---

## 改訂履歴

| バージョン | 日付 | 変更内容 |
|----------|------|---------|
| v1 | 2026-05-29 | 初版制定（iPhone/iPad リモート監視設計）|
| v1.1 | 2026-05-30 | Section 5-4「Claude Code は監視役」・Section 5-5「成否確認手順」・Section 8-2「誤判定防止ルール」追加 |
