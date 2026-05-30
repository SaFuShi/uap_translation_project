# 作業ログ：iPad/iPhone リモート監視セットアップ

**日付：** 2026-05-30  
**担当：** fukudasatoshi（Mac Studio）+ agentai（Mac mini）  
**フェーズ：** Release 02 — ローカルワーカー環境整備

---

## 1. 本日の目的

これまでの UAP 翻訳プロジェクトは、Mac Studio の前に座っている間だけ作業状況を確認できる状態だった。今日は「外出中や移動中でも iPhone / iPad から Mac Studio・Mac mini の作業状況を確認できる」環境を整えることを目的として作業を行った。

具体的には、tmux（ターミナル多重化ツール）を使ったセッション管理と、Termius（iPad/iPhone 向け SSH アプリ）からの接続環境を整備した。これにより、OCR・Whisper・ffmpeg などの長時間バッチ処理が Mac mini で走っている間も、iPad から進捗をリアルタイムに確認できるようになった。

---

## 2. iPad/Termius でできるようになったこと

セットアップ完了後、iPad（または iPhone）から以下のことが可能になった。

- Mac mini の OCR・Whisper・ffmpeg などの**処理ログをリアルタイムで確認**できる
- Mac mini の**処理中プロセス・出力ファイルの存在**を確認できる
- Mac Studio の Claude Code 画面を**読み取り専用で監視**できる（次回 tmux 起動後から）
- **セッションを抜けてもバッチ処理は継続**される（iPhone の接続が切れても Mac mini の処理は止まらない）

---

## 3. Mac mini 側：uap-mini-worker tmux セッション

### セッション情報

| 項目 | 内容 |
|------|------|
| セッション名 | `uap-mini-worker` |
| 作成日時 | 2026-05-30 10:06 |
| 機器 | Mac mini / agentai |
| 作業ディレクトリ | `/Volumes/ACASIS_2TB/AI_Data/UAP_TRANSLATION_PROJECT/repo` |

### 用途

Mac mini では OCR・Whisper・ffmpeg などの重い処理を長時間実行する。`uap-mini-worker` セッションの中でこれらのバッチを実行しておくことで、SSH 接続が切れても処理が継続される。iPad からはこのセッションに attach（接続）して、ログをリアルタイムで確認する。

### 接続方法（iPad から）

```
① Termius で Mac mini（agentai）に SSH 接続
② $ uapmux
   → uap-mini-worker セッションに接続
③ ログや処理状況を確認
④ Ctrl+b → d でデタッチ（処理は継続したまま抜ける）
```

---

## 4. Mac Studio 側：uap-studio tmux セッション

### セッション情報

| 項目 | 内容 |
|------|------|
| セッション名 | `uap-studio` |
| 作成日時 | 2026-05-30 10:11 |
| 機器 | Mac Studio / fukudasatoshi |
| 作業ディレクトリ | `/Users/fukudasatoshi/Documents/UAP_TRANSLATION_PROJECT` |

### 用途

Mac Studio では Claude Code を使った翻訳作業・git 操作・設計書作成などを行う。次回から Claude Code を `uap-studio` セッション内で起動することで、iPad から `uapwatch` コマンドを使って Claude Code の画面を読み取り専用で確認できるようになる。

### 接続方法（iPad から・読み取り専用）

```
① Termius で Mac Studio（fukudasatoshi）に SSH 接続
② $ uapwatch
   → uap-studio セッションに読み取り専用で接続
③ Claude Code の出力・進捗を確認
④ Ctrl+b → d でデタッチ
```

---

## 5. Termius snippets（ショートカット候補）

Termius にはよく使うコマンドを「Snippet（スニペット）」として登録できる機能がある。iPad のタッチ操作で長いコマンドを打たなくて済むため、以下の登録を推奨する。

| スニペット名 | コマンド | 用途 |
|-------------|---------|------|
| mini-attach | `uapmux` | Mac mini セッション接続 |
| mini-detach | `uapdetach` | セッションを抜ける |
| mini-status | `uapstatus` | 状態確認（git/ファイル/プロセス） |
| mini-log    | `uaplog` | 最新 OCR ログ確認 |
| studio-watch | `uapwatch` | Mac Studio 読み取り専用監視 |

※ Termius スニペット登録は Settings → Snippets から行う。今回はまだ登録していない。

---

## 6. alias 一覧

両機の `~/.zshrc` に追記した alias の一覧。新しいターミナルを開いた時点で自動的に使えるようになる。

### Mac mini（agentai）

| alias | 実行内容 |
|-------|---------|
| `uap` | UAP 作業ディレクトリ（repo）へ移動 |
| `uapmux` | `uap-mini-worker` セッションに接続（なければ新規作成） |
| `uapdetach` | tmux セッションをデタッチして抜ける |
| `uapstatus` | git 状態・出力ファイル一覧・実行中プロセスを一括表示 |
| `uaplog` | 最新の OCR ログ末尾 50 行を表示 |

### Mac Studio（fukudasatoshi）

| alias | 実行内容 |
|-------|---------|
| `uap` | UAP 作業ディレクトリへ移動 |
| `uapmux` | `uap-studio` セッションに接続（なければ新規作成） |
| `uapdetach` | tmux セッションをデタッチして抜ける |
| `uapstatus` | git 状態・最新コミット 5 件を表示 |
| `uapwatch` | `uap-studio` セッションに**読み取り専用**で接続（iPad 監視用） |

---

## 7. 現在の通常 Terminal の Claude Code は直接監視不可

**重要な制約：** 本日時点では、現在動いている Claude Code は通常の Terminal（tmux 外）で起動している。このため、iPad から SSH 接続しても Claude Code の画面を見ることはできない。

tmux セッションの中で起動しているプロセスだけが、`tmux attach` で別の端末から画面共有できる仕組みになっている。今の通常 Terminal は Mac Studio の画面上にしか表示されない。

---

## 8. 次回からの方針：Claude Code を uap-studio tmux 内で起動する

次回以降の作業は、以下の手順で始める。

```
① Mac Studio の Terminal を開く
② $ uapmux               → uap-studio セッションにアタッチ
③ $ uap                  → UAP 作業ディレクトリへ移動
④ $ claude               → Claude Code 起動
⑤ 作業中に iPad から確認したい場合：
   Termius → ssh → $ uapwatch（読み取り専用でアタッチ）
⑥ 作業完了後：Claude Code を /exit または Ctrl+C で終了
⑦ $ uapdetach または Ctrl+b d でセッションをデタッチ
   （セッション自体は残る）
```

この手順を定着させることで、外出中・就寝中でも iPad から作業進捗を確認できるようになる。

---

## 9. iPad で許可する操作・避ける操作

### 許可する操作（安全）

- `uapmux` / `uapwatch` でのセッション接続・監視
- `uapstatus` / `uaplog` での状態確認（読み取り専用）
- `uapdetach`（Ctrl+b d）でのデタッチ

### 慎重に行う操作

- Claude Code へのプロンプト入力（`uap-studio` に attach 中）  
  → タッチ誤入力で意図しない処理が走るリスクあり。`uapwatch`（読み取り専用）を使うこと。

### 避ける操作（iPad からは行わない）

| 操作 | 理由 |
|------|------|
| `git commit / push` | タッチ誤操作で意図しない commit が発生するリスク |
| `rm` 系コマンド | 誤削除のリスク |
| Python スクリプトの直接実行 | 引数ミスで誤動作するリスク |
| `tmux kill-session` | Claude Code ごとセッションが終了してしまう |
| 設定ファイルの編集 | 誤編集のリスク |

---

## 10. 今後の課題

### 短期（次の作業セッションで実施）

- [ ] 次回 Claude Code を `uap-studio` セッション内で起動し、iPad の Termius から `uapwatch` で監視できることを実際にテストする
- [ ] iPhone の Termius（または Blink Shell）からも同様に接続できるか確認する

### 中期

- [ ] Termius にスニペット（mini-attach / mini-log / studio-watch 等）を登録し、タッチ操作だけで監視できるようにする
- [ ] Mac mini で Whisper バッチ処理が始まった際に、iPad から `uaplog` 相当のコマンドで Whisper ログを確認できるよう `uapwhisperlog` alias を追加する
- [ ] 長時間処理の完了通知を何らかの形で受け取れる仕組みを検討する（例：処理完了時にファイルを書き出す、Slack 通知など）

---

*このログは NotebookLM へのアップロード用です。SSH 鍵・パスワード・IP アドレスなどの機密情報は含まれていません。*
