---CODEX_AUDIT_START---
VERDICT: WARN
BLOCK: 0
WARN: 4
UNVERIFIABLE: 0
PASS: 10
MODEL: GPT-5
---ITEMS_START---
P0-1 PASS Markdown表・引用ブロック・長文英文引用・2階層以上ネスト・Codex注釈ブロックは確認されない。
P1-1 PASS ファイル名・Release Date・Incident Date・CENTCOM・DVIDS IDはローカル台帳およびメタデータと整合。対象DVIDS直接URLも記載あり。
P1-2 PASS 速度・高度・Zulu時刻など該当する数値換算項目はなく、動画時間・解像度・フレームレートはmetadata.jsonと整合。
P1-3 PASS CENTCOM、AOR、DVIDSは日本語補足があり、該当する基地名・部隊名・機密区分記述はない。
P1-4 PASS Misrep・MDR・JSIR・CSP/MRO等の番号類は本文に出ていない。
P1-5 WARN source_registry.csv に対象ファイルが未登録で、article_id未付番。本文末で未登録と明記されているが、公開前整合性としては未完了。
P2-1 WARN 構成上、「注意点」「免責」の独立セクションがなく、また「note転記後にこの行を削除」という作業メモが本文内に残っている。
P2-2 PASS 軍事略語・専門用語のうち本文に出る CENTCOM / AOR / DVIDS は概ね補足済み。
P2-3 WARN 「標準的なDOW-UAP UI」は比較・一般化の根拠が本文内で示されておらず、視覚観察と解釈の境界がやや混在する。
P2-4 PASS フィート・ノット・マイル等の日本向け換算が必要な単位は本文に出ていない。
P2-5 PASS note投稿互換上の禁止形式は確認されず、タイトルと本文主題も概ね一致。
P2-6 PASS 日本語読者向けの基本補足は概ねあり、過度に長い注釈反復もない。
P3-1 WARN source_registry.csv に対象記事が存在せず、status・draft_path・source_url・article_idの台帳整合性を完了確認できない。
IMG-1 PASS 視覚観察と解釈は概ね分離され、「IRセンサーと推定されるが確認できない」「雲とみられる」「UAP対象は確認困難」など留保表現がある。
---ITEMS_END---
---WARN_DETAILS_START---
W-01: source_registry整合性 | 「source_registry 未登録：本ドラフトは source_registry.csv への登録・article_id の付番が未実施です。」 | 公開前に source_registry.csv へ対象MP4・DVIDS URL・article_id・draft_path・statusを登録する。
W-02: 記事構成 | 「→ 使用ファイル：thumbnails/.../frame_0000.png（note転記後にこの行を削除）」 | 本文公開版では作業メモ行を削除し、必要なら画像キャプションのみ残す。
W-03: 記事構成 | 「メタデータ → 要点 → AI読解 → 出典 → source_registry 未登録」 | チェックリスト標準に合わせ、「注意点」と「免責」を独立セクションとして追加する。
W-04: 表現の客観性 | 「これはDOW-UAP映像に多く見られる標準的なUIスタイルです。」 | 「他のDOW-UAP映像にも見られるUI表示と類似します」など、比較根拠が限定的であることを示す表現に弱める。
---WARN_DETAILS_END---
---CODEX_AUDIT_END---