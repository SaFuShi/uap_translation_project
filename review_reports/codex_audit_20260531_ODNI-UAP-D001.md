# Codex 監査レポート 20260531 — ODNI-UAP-D001

**監査日**: 2026-05-31  
**監査者**: Codex  
**監査対象**: `note_drafts/ai_summary_ODNI-UAP-D001_usper_narrative_senior_usic_note_version.md`  
**対象資料**: `raw_pdf/ODNI-UAP-D001_USPER_Narrative_Senior_USIC.pdf`  
**出力先**: `review_reports/codex_audit_20260531_ODNI-UAP-D001.md`

**参照資料**:
- `docs/codex_audit_role.md`
- `docs/audit_checklist_v1.md`
- `docs/release02_pdf_visual_policy.md`
- `docs/release02_media_processing_policy_v1.md`
- `docs/release02_audio_video_pipeline_design.md`
- `review_logs/codex_feedback_log.md`
- `metadata/files_catalog.csv`
- `worker_outputs/ocr_review_summary_20260529.csv`

---

## 総合判定

**BLOCK**

本文の中心的な要約は概ね原文に沿っているが、関連文書セクションで `usper-statement-redacted.pdf` を「別事案・別の報告者」と断定している点は公開前修正が必要。ローカルの既存ドラフトおよび原文抽出結果では、同ファイルは本ODNI文書と同一または強く重なるヘリコプター事案を扱っている可能性が高く、現状の記述は読者に誤った関係性を伝える。

---

## サマリー

- PASS: 8
- WARN: 4
- BLOCK: 1
- UNVERIFIABLE: 0

---

## BLOCK

### B-01: 関連文書 `usper-statement-redacted.pdf` を「別事案・別の報告者」と断定している

**該当箇所**
- 191行目: `関連文書について（別事案・参考）`
- 193行目: `それぞれは独立した別の事案・別の報告者によるものです`
- 195行目: `usper-statement-redacted.pdf（Release 01・FBI/DoW・Late 2025・別の報告者）`
- 198行目: `上記2件とは異なる事案・異なる証言者による記録です`

**問題**  
`usper-statement-redacted.pdf` は、既存ドラフト `note_drafts/ai_reading_002_usper-statement_note_version.md` および原文抽出結果上、以下の点でODNI-UAP-D001と強く重なる。

- 上級米国情報官を含むヘリコプター事案
- 山岳地帯での轟音・デブリ調査
- FLIR / NVG / 肉眼の組み合わせ
- ヘリコプターへの10フィート接近
- オーブの分裂、T字状出現、戦闘機付近での出現

したがって、少なくとも `usper-statement-redacted.pdf` については「別事案・別の報告者」とは断定できない。むしろ、Release 01の黒塗り運用報告とRelease 02の一人称ナラティブが同一または重複事案を別形式で示している可能性がある。

**公開前に必ず修正すべき理由**  
関連文書の関係性は、読者が資料群をたどる際の provenance に直結する。ここで同一・重複可能性のある資料を「別事案」と断定すると、資料体系の理解を誤らせる。

**修正案**

```
## 関連文書について（同一・重複可能性のある資料と別事案）

war.gov/UFO では、同時期または同地域に関連する文書が複数公開されています。

- usper-statement-redacted.pdf（Release 01・FBI・Late 2025）
  黒塗りの多い運用報告形式の文書。本記事のODNI-UAP-D001と同一または強く重なるヘリコプター事案を扱っている可能性があります。

- western_us_event_slides_5.08.2026.pdf（Release 01・DoW・2023年）
  法執行官USPER1-7による別事案のブリーフィング資料です。

この記事の本文要約はODNI-UAP-D001のみを対象とし、上記資料とは混同しないよう区別しています。
```

---

## WARN

### W-01: タイトルが地上チーム報告を事実断定に見せている

**該当箇所**
- 1行目: `ヘリコプターに10フィートまで接近した光の球体`

**判定**: WARN

**理由**  
10フィート接近は原文上、地上チームが無線で報告した内容を証言者が記録したもの。本文119行目では適切に補足されているが、タイトルだけを見ると「記事が接近を確定事実として断定している」ように読める。

**修正案**

```
# 「ヘリに10フィートまで接近」と報告された光の球体──西部米国・上級情報官のUAP目撃証言【AI概要版】
```

または

```
# ヘリコプター至近に現れた光の球体──西部米国・上級情報官のUAP目撃証言【AI概要版】
```

---

### W-02: `超高温（super-hot）` が実測温度のように読める箇所がある

**該当箇所**
- 37行目: `FLIRで「超高温（super-hot）」と描写されたオーブ`
- 64行目: `FLIR映像で「超高温（super-hot）」の物体を確認`

**判定**: WARN

**理由**  
原文の `super-hot` は地上チームがFLIR上でそう描写した表現。実際の温度測定値ではない。`docs/release02_media_processing_policy_v1.md` では、IR / FLIR 表示を熱源・高温実体として断定しない方針が明記されている。

**修正案**

37行目:

```
最初の接触では、FLIR上で「super-hot」と表現された物体が地面から上昇し...
```

64行目:

```
地上チームから、FLIR上で「super-hot」と見える物体を確認したとの無線が届きました。
```

必要なら注意事項に以下を追加。

```
- 「super-hot」はFLIR上の見え方を表す証言内の表現であり、実測温度を示すものではありません
```

---

### W-03: セクション見出しの「追跡」が断定的

**該当箇所**
- 82行目: `戦闘機への追跡と三角フォーメーション`

**判定**: WARN

**理由**  
本文84行目・151行目・153行目では、戦闘機を追っていたという表現を証言者の主観として整理できている。一方、見出しだけは「追跡」を事実化しているように見える。Release 02 メディア処理方針でも「追跡」は断定注意語。

**修正案**

```
### 戦闘機上方に現れたオーブと三角フォーメーション
```

または

```
### 「追いかけているように見えた」戦闘機付近のオーブ
```

---

### W-04: 使用画像のローカルパスが現存しない

**該当箇所**
- 210行目: `page_images/ODNI-UAP-D001_USPER_Narrative_Senior_USIC/page_0001.png・page_0002.png`

**判定**: WARN

**理由**  
監査時点で `page_images/ODNI-UAP-D001_USPER_Narrative_Senior_USIC/` は存在しない。記事内の画像キャプション自体は、出典・視覚的参考・非断定方針に沿っているが、出典情報に存在しないローカル素材パスを記載すると運用上の混乱が出る。

**修正案**

画像素材を生成してから掲載する場合:

```
- 使用画像：ODNI-UAP-D001_USPER_Narrative_Senior_USIC.pdf p.1・p.2
```

ローカルパスは記事本文ではなく制作管理側に残す。画像をまだ使わない場合は、19行目・94行目の画像プレースホルダーと210行目の使用画像行を公開前に削除または保留表示にする。

---

## 観点別チェック

### 1. 公式資料・証言者主観・記事側推論の分離

**判定**: WARN

本文の大部分は「記録されています」「述べています」「報告された」と書き分けられている。119行目と153行目の補足は特に有効。  
ただし、タイトルと82行目見出しが本文の留保より強く、断定寄りに見える。

### 2. メタデータ整合性

**判定**: PASS

`metadata/files_catalog.csv` と照合した結果、以下は整合。

- file_name: `ODNI-UAP-D001_USPER_Narrative_Senior_USIC.pdf`
- agency: `Office of the Director of National Intelligence`
- release_date: `2026-05-22`
- incident_date: `2025`
- incident_location: `Western United States`
- file_type: `PDF`
- ocr_status: `not_needed`

2026年5月26日の脚注訂正もPDF本文の脚注と整合。

### 3. 主要描写の出所区別

**判定**: PASS

- 10フィート接近: 地上チーム報告として整理あり
- `super-hot`: 地上チームのFLIR上の描写。ただし温度断定回避の修正推奨あり
- 分裂: 地上チーム報告およびパイロットのNVG観察として記述
- T字フォーメーション: 証言者・パイロット観察として記述
- 戦闘機を追いかけた: 証言者の主観表現として明記

### 4. 「光の球体」「オーブ」「UAP」の表現

**判定**: PASS

原文に `orb` / `orbs` が繰り返し出るため、「オーブ」の使用自体は妥当。本文28行目、184行目、187行目、216行目で正体・起源を断定しない旨も明記されている。  
より安全にするなら初出付近で「オーブは原文 `orb` の訳語であり、正体を示すものではない」と補足するとよい。

### 5. タイトル妥当性

**判定**: WARN

読者の関心を引く範囲には収まっているが、10フィート接近が地上チーム報告である点をタイトル上でも留保した方がよい。

### 6. `super-hot` の扱い

**判定**: WARN

FLIR上の表現であることは前後から分かるが、実測温度ではない旨を明示すると方針により合う。

### 7. 「無数のオーブ」の妥当性

**判定**: PASS

原文に `countless orange orbs` があり、「無数のオレンジ色のオーブ」は根拠あり。煽り表現とは判断しない。

### 8. 画像キャプション

**判定**: PASS / WARN

キャプション本文は、資料名・ページ・視覚的参考・非断定を含み、`docs/release02_pdf_visual_policy.md` と整合。  
ただし、画像素材パスが現存しないため W-04 を付けた。

### 9. 関連文書セクション

**判定**: BLOCK

`western_us_event_slides_5.08.2026.pdf` を別事案とする点は妥当。  
`usper-statement-redacted.pdf` を別事案・別報告者とする点は不適切。B-01参照。

### 10. note投稿互換性

**判定**: PASS

以下は検出されなかった。

- Markdown table
- 引用ブロック
- コードブロック
- Codex注釈ブロック
- 2階層以上のネスト箇条書き

### 11. AI利用上の留保・ディスクレイマー

**判定**: PASS

28行目、184〜187行目、216行目で、UAPの正体・起源を断定しないこと、AI処理に誤変換・誤訳の可能性があること、公式見解は原文資料を参照すべきことが明記されている。

### 12. OCR / テキスト品質

**判定**: PASS

`worker_outputs/ocr_review_summary_20260529.csv` にはODNI-UAP-D001の行はないが、`metadata/files_catalog.csv` の `ocr_status=not_needed`、`metadata/text_layer_report.csv` の2ページとも `text layer present, OCR not needed`、およびPyMuPDF抽出で2ページ合計5,692文字を確認した。本文169行目の数字と整合。

---

## 最終判定

**BLOCK**

公開前に最低限 B-01 を修正すること。  
B-01修正後は、W-01〜W-04を反映すれば PASS 相当に近い。特にタイトル、`super-hot`、追跡見出しは、本文の慎重な留保と表現レベルを揃えるだけで解消できる。
