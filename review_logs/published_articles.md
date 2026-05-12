# 公開済み・作成済み記事一覧

最終更新：2026-05-12（ディレクトリ整理実施）

---

## ディレクトリ構成

```
UAP_TRANSLATION_PROJECT/
├── published_articles/   # 公開済み記事（正本 or 参考ドラフト）
├── note_drafts/          # 未公開の作業ドラフト＋テンプレート
├── archive_drafts/       # 旧版・問題あり・廃止ドラフト
└── review_logs/          # 品質チェック・管理ログ
```

---

## ステータス凡例

| ステータス | 格納先 | 説明 |
|---|---|---|
| **published（正本）** | `published_articles/` | Git版 = note公開版。正本はGit側 |
| **published（参考ドラフト）** | `published_articles/` | note公開済みだが、ChatGPT・人間の修正を経て投稿。**正本はnote側**。Git版は参考用 |
| **draft（未公開）** | `note_drafts/` | 作成済みだが未投稿の作業ドラフト |
| **archived** | `archive_drafts/` | 旧版・問題のある表現を含む廃止ドラフト |

---

## 記事一覧

### #001 — FBIが作成したUAP目撃スケッチ

| 項目 | 内容 |
|---|---|
| **タイトル** | FBIが作成したUAP目撃スケッチが公開されました【AI読解版 #001】 |
| **元PDFファイル名** | 2024-04-30-composite-sketch.pdf |
| **公開状況** | 未公開 |
| **テーマ分類** | FBI目撃証言・スケッチ |
| **ドラフトファイル** | `note_drafts/ai_reading_001_composite-sketch_20240430_note_version.md` |

**注意点**
- 旧バージョン（`ai_reading_001_composite-sketch_20240430.md`）が別途存在。公開は note_version を使用すること
- 行数超過（171行）・出典形式・免責事項・注意点セクション欠如の警告あり（review_ai_summary.py より）
- 公開前にフォーマット基準への更新を要検討

---

### #002 — 上級情報官の6時間目撃証言

| 項目 | 内容 |
|---|---|
| **タイトル** | 米国の上級情報官が6時間にわたって目撃した発光体の記録【AI概要版 #002】 |
| **元PDFファイル名** | usper-statement-redacted.pdf |
| **公開状況** | 未公開 |
| **テーマ分類** | 個人目撃証言（上級情報官） |
| **ドラフトファイル** | `note_drafts/ai_reading_002_usper-statement_note_version.md` |

**注意点**
- 黒塗り多数。場所・日付・組織名は特定不可
- チェック結果：問題なし（review_ai_summary.py より）

---

### #003 — 連邦捜査官7名の目撃（Western US Event）

| 項目 | 内容 |
|---|---|
| **タイトル** | 連邦捜査官7名が目撃した4種類の現象──「Western US Event」ブリーフィング資料【AI概要版 #003】 |
| **元PDFファイル名** | western_us_event_slides_5.08.2026.pdf |
| **公開状況** | 未公開 |
| **テーマ分類** | FBI複数目撃・ブリーフィング資料 |
| **ドラフトファイル** | `note_drafts/ai_reading_003_western_us_event_slides_note_version.md` |

**注意点**
- チェック結果：問題なし（review_ai_summary.py より）

---

### #004 — アポロ12号「星へ向かう光」

| 項目 | 内容 |
|---|---|
| **タイトル** | 1969年、月面の宇宙飛行士が報告した「星へ向かう光」──アポロ12号会話記録【AI概要版 #004】 |
| **元PDFファイル名** | nasa-uap-d1-apollo-12-transcript-1969.pdf |
| **公開状況** | 未公開 |
| **テーマ分類** | アポロ計画・宇宙目撃（NASA） |
| **ドラフトファイル** | `note_drafts/ai_reading_004_apollo12_transcript_note_version.md` |

**注意点**
- 行数超過（108行）。公開前に圧縮を推奨
- 目撃者（アル・ビーン）本人が「水ボイラーかも」と自己解説している旨を記事に明記済み

---

### #005 — アポロ17号「遠くで規則的に点滅するもの」

| 項目 | 内容 |
|---|---|
| **タイトル** | 1972年、アポロ17号の乗組員が記録した「遠くで規則的に点滅するもの」【AI概要版 #005】 |
| **元PDFファイル名** | nasa-uap-d2-apollo-17-transcript-1972.pdf |
| **公開状況** | 未公開 |
| **テーマ分類** | アポロ計画・宇宙目撃（NASA） |
| **ドラフトファイル** | `note_drafts/ai_reading_005_apollo17_transcript_note_version.md` |

**注意点**
- 行数超過（117行）。公開前に圧縮を強く推奨

---

### #006 — アポロ11号「それは円筒形ではなかった」

| 項目 | 内容 |
|---|---|
| **タイトル** | 「それは円筒形ではなかった」──アポロ11号3名が語った不明物体の形状論争【AI概要版 #006】 |
| **元PDFファイル名** | nasa-uap-d4-apollo-11-technical-crew-debriefing-1969.pdf |
| **公開状況** | **公開済み（Git版は参考ドラフト）** |
| **テーマ分類** | アポロ計画・宇宙目撃（NASA） |
| **ドラフトファイル** | `published_articles/ai_reading_006_apollo11_debriefing_note_version.md`（参考ドラフト） |

**注意点**
- **Gitドラフトと公開版は完全一致しない。** Claude Code生成後、ChatGPTと人間が修正して投稿。正本はnote側。
- Gitドラフトは削除せず参考ドラフトとして保持
- スキャンのみPDF・Tesseract OCR使用

---

### #007 — アポロ17号「トンネルのような光」

| 項目 | 内容 |
|---|---|
| **タイトル** | アポロ17号帰還時に記録された「トンネルのような光」【AI概要版 #007】 |
| **元PDFファイル名** | nasa-uap-d6-apollo-17-technical-crew-debriefing-1973.pdf |
| **公開状況** | **公開済み（Git版は参考ドラフト）** |
| **テーマ分類** | アポロ計画・宇宙目撃（NASA） |
| **ドラフトファイル** | `published_articles/ai_summary_007_apollo17_debriefing_note_version_revised.md`（参考ドラフト・改訂版） |

**注意点**
- **Gitドラフトと公開版は完全一致しない。** Claude Code生成後、ChatGPTと人間が修正して投稿。正本はnote側。
- Gitドラフトは削除せず参考ドラフトとして保持
- 旧版（`archive_drafts/ai_reading_007_apollo17_technical_debriefing_note_version.md`）は「直接的な証拠」という強い表現を含む（archive済み）
- #005の補足記事として位置づけ

---

### #008 — ISR任務中の白い物体（ペルシャ湾）

| 項目 | 内容 |
|---|---|
| **タイトル** | ISR任務中にセンサーをよぎった白い物体──ペルシャ湾上空、2020年5月【AI概要版 #008】 |
| **元PDFファイル名** | dow-uap-d38-range-fouler-debrief-middle-east-may-2020.pdf |
| **公開状況** | **公開済み（Git版は参考ドラフト）** |
| **テーマ分類** | 軍用機ISR・Range Fouler（中東） |
| **ドラフトファイル** | `published_articles/ai_summary_008_persian_gulf_range_fouler_note_version_revised.md`（参考ドラフト・改訂版） |

**注意点**
- **Gitドラフトと公開版は完全一致しない。** Claude Code生成後、ChatGPTと人間が修正して投稿。正本はnote側。
- Gitドラフトは削除せず参考ドラフトとして保持
- 旧版（`archive_drafts/ai_reading_008_d38_middle_east_isr_note_version.md`）は「IRSセンサー」誤記・Black Hot断定表現を含む（archive済み）

---

### #009 — 1機が3機になっていた（アラビア海）

| 項目 | 内容 |
|---|---|
| **タイトル** | 1機が雲の後ろに消えたら3機になっていた──アラビア海北部、2020年8月【AI概要版 #009】 |
| **元PDFファイル名** | dow-uap-d56-range-fouler-debrief-arabian-sea-august-2020.pdf |
| **公開状況** | **公開済み（Git版は参考ドラフト）** |
| **テーマ分類** | 軍用機ISR・Range Fouler（アラビア海） |
| **ドラフトファイル** | `published_articles/ai_reading_009_d56_arabian_sea_note_version.md`（参考ドラフト） |

**注意点**
- **Gitドラフトと公開版は完全一致しない。** Claude Code生成後、ChatGPTと人間が修正して投稿。正本はnote側。
- Gitドラフトは削除せず参考ドラフトとして保持

---

### #010 — 楕円形・オーブ状のUAPを2時間以上追跡

| 項目 | 内容 |
|---|---|
| **タイトル** | 楕円形・オーブ状の未確認飛行体を2時間以上追跡──場所不明、2024年10月【AI概要版 #010】 |
| **元PDFファイル名** | dow-uap-d52-email-correspondance-na-august-2024.pdf |
| **公開状況** | **公開済み** |
| **テーマ分類** | 機密解除メール・ティアライン承認手続き |
| **ドラフトファイル** | `published_articles/ai_summary_010_d52_email_uap_orb_note_version.md` |

**注意点**
- ファイル名「august-2024」だがインシデントは2024年10月31日（記事内で明記済み）
- 目撃の詳細（場所・センサー）は別文書のため含まれていない旨を記事内で明記済み

---

### #011 — 精密誘導爆撃中にセンサーを高速通過した未確認物体

| 項目 | 内容 |
|---|---|
| **タイトル** | 精密誘導爆撃中にセンサーを高速通過した未確認物体──イラク上空、2024年9月【AI概要版 #011】 |
| **元PDFファイル名** | dow-uap-d28-mission-report-east-china-sea-2024.pdf |
| **公開状況** | **公開済み** |
| **テーマ分類** | 軍用機MISREP・武器運用中（イラク・USCENTCOM） |
| **ドラフトファイル** | `published_articles/ai_summary_011_d28_armed_overwatch_iraq_note_version.md` |

**注意点**
- ファイル名「east-china-sea」だが実際はイラク（Ayn al-Asad）（記事内で明記済み）
- IRレンズフレア・熱源として検出。乗員評価「BENIGN」

---

### #012 — ISR任務中に1分間追跡した丸い物体（アデン湾、2020年10月）

| 項目 | 内容 |
|---|---|
| **タイトル** | ISR任務中に1分間追跡した丸い未識別物体──アデン湾上空、2020年10月【AI概要版 #012】 |
| **元PDFファイル名** | dow-uap-d44-range-fouler-arabian-sea-october-2020.pdf |
| **公開状況** | **公開済み** |
| **テーマ分類** | 軍用機ISR・Range Fouler（アデン湾） |
| **ドラフトファイル** | `published_articles/ai_summary_012_d44_arabian_sea_oct2020_note_version.md` |

**注意点**
- ファイル名「Arabian Sea」だが本文はアデン湾（記事内で明記済み）
- #009・#013と同飛行隊（1172 ATKS）、同地域・同時期の複数報告

---

### #013 — 夜間ISR任務中に8分間追跡した丸い物体（アデン湾、2020年9月）

| 項目 | 内容 |
|---|---|
| **タイトル** | 夜間ISR任務中に8分間追跡した丸い未識別物体──アデン湾上空、2020年9月【AI概要版 #013】 |
| **元PDFファイル名** | dow-uap-d57-mission-report-gulf-of-aden-september-2020.pdf |
| **公開状況** | **公開済み** |
| **テーマ分類** | 軍用機ISR・Range Fouler（アデン湾） |
| **ドラフトファイル** | `published_articles/ai_summary_013_d57_gulf_of_aden_sep2020_note_version.md` |

**注意点**
- 速度277 mph（時速約446km）・夜間8分間追跡
- 1172 ATKSからの3件目の記録（#009・#012・本件）として記事内で言及済み

---

### #014 — F-16部隊が高高度で確認した複数の発光物体

| 項目 | 内容 |
|---|---|
| **タイトル** | F-16部隊が高高度で確認した複数の発光物体──中東上空、2023年3月【AI概要版 #014】 |
| **元PDFファイル名** | dow-uap-d20-mission-report-southern-united-states-2023.pdf |
| **公開状況** | **公開済み** |
| **テーマ分類** | 軍用機MISREP・DCA任務中（中東・USCENTCOM） |
| **ドラフトファイル** | `published_articles/ai_summary_014_d20_f16_middle_east_note_version.md` |

**注意点**
- ファイル名「southern-united-states」だが実際はプリンス・スルタン空軍基地（サウジアラビア）（記事内で明記済み）
- 推定10〜20機、高度FL600+。ターゲティングポッドで星と比較→「結果が異なった」

---

### #015 — INDOPACOM域内での短時間UAP観測2件

| 項目 | 内容 |
|---|---|
| **タイトル** | INDOPACOM域内で2日連続して確認された短時間UAP観測──2025年4月【AI概要版 #015】 |
| **元PDFファイル名** | dow-uap-d50-email-correspondence-indopacom-april-2025.pdf |
| **公開状況** | **公開済み** |
| **テーマ分類** | 機密解除メール・ティアライン承認手続き（INDOPACOM） |
| **ドラフトファイル** | `published_articles/ai_summary_015_d50_indopacom_email_note_version.md` |

**注意点**
- 12秒・23秒の短時間観測2件のみ
- #010と同様の承認手続きメール形式。PAROCの役割として言及済み

---

### #016 — 高高度で目視された不明航空現象（アラビア湾・2020年）

| 項目 | 内容 |
|---|---|
| **タイトル** | 高高度で目視された不明航空現象──アラビア湾・2020年【AI概要版 #016】 |
| **元PDFファイル名** | dow-uap-d6-mission-report-arabian-gulf-2020.pdf |
| **公開状況** | **公開済み** |
| **note URL** | https://note.com/deft_ibis3303/n/n267aa9e43143 |
| **テーマ分類** | 軍用機MISREP（アラビア湾・2020年） |
| **ドラフトファイル** | `published_articles/ai_summary_016_d6_arabian_gulf_2020_note_version.md` |

**注意点**
- 7ページ大部分黒塗り（1.4(a)区分）・有効テキスト約225文字
- カタログ表記「Pacific Ocean」だがMGRS 3SKTはアラビア湾域。記事内注意点に記載済み

---

### #018 — レーダー捕捉・赤点滅・妨害電波受信（場所不明・2020年10月）

| 項目 | 内容 |
|---|---|
| **タイトル** | レーダー捕捉・赤点滅・妨害電波受信──場所不明・2020年10月【AI概要版 #018】 |
| **元PDFファイル名** | dow-uap-d58-range-fouler-debrief-na-october-2020.pdf |
| **公開状況** | **公開済み** |
| **note URL** | https://note.com/deft_ibis3303/n/n9c1a2459694f |
| **テーマ分類** | 軍用機ISR・Range Fouler（場所不明・2020年10月） |
| **ドラフトファイル** | `published_articles/ai_summary_018_d58_range_fouler_na_oct2020_note_version.md` |

**注意点**
- 発生場所「N/A」。センサーFOV内で1機がもう1機を1/30秒で周回して消えたとの記述あり
- 赤色点滅ストローブ目視・ノイズジャミング（2本シェブロン）受信を記録

---

### #019 — 速度321ノット・東方向へ加速した不明航空現象（アラビア湾・2020年）

| 項目 | 内容 |
|---|---|
| **タイトル** | 速度321ノット・東方向へ加速した不明航空現象──アラビア湾・2020年【AI概要版 #019】 |
| **元PDFファイル名** | dow-uap-d4-mission-report-arabian-gulf-2020.pdf |
| **公開状況** | **公開済み** |
| **note URL** | https://note.com/deft_ibis3303/n/nd705d6119670 |
| **テーマ分類** | 軍用機MISREP（アラビア湾・2020年） |
| **ドラフトファイル** | `published_articles/ai_summary_019_d4_arabian_gulf_2020_note_version.md` |

**注意点**
- 5ページ大部分黒塗り（SECRET//REL TO USA, FVEY）・有効テキスト約338文字
- インシデント日付「N/A」・MGRS 34SDG（アラビア湾域）
- 速度推定321ノットの後、東方向へ加速。短時間観測のため高度推定不可

---

### #020 — SWIRカメラのみに映ったダイヤモンド形UAPと非稼働の「突起物」（地中海・2024年1月）

| 項目 | 内容 |
|---|---|
| **タイトル** | SWIRカメラのみに映ったダイヤモンド形UAPと非稼働の「突起物」──地中海・2024年1月【AI概要版 #020】 |
| **元PDFファイル名** | dow-uap-d25-mission-report-greece-january-2024.pdf |
| **公開状況** | **公開済み** |
| **note URL** | https://note.com/deft_ibis3303/n/na3cf23f3cf06 |
| **テーマ分類** | 軍用機MISREP（地中海・2024年1月） |
| **ドラフトファイル** | `published_articles/ai_summary_020_d25_mediterranean_greece_2024_note_version.md` |

**注意点**
- SWIRカメラのみ捕捉・EO/IRでは確認されず
- ダイヤモンド形・非稼働の突起物・約434ノット・2分間
- ギリシャLGLR（ラリサ空軍基地）付近・observer評価はBenign

---

### #021 — 雲の間に4機のUAPを目視（アラビア湾・2020年）

| 項目 | 内容 |
|---|---|
| **タイトル** | 雲の間に4機のUAPを目視──アラビア湾・2020年【AI概要版 #021】 |
| **元PDFファイル名** | dow-uap-d3-mission-report-arabian-gulf-2020.pdf |
| **公開状況** | **公開済み** |
| **note URL** | https://note.com/deft_ibis3303/n/na6119fe94348 |
| **テーマ分類** | 軍用機MISREP（アラビア湾・2020年） |
| **ドラフトファイル** | `published_articles/ai_summary_021_d3_arabian_gulf_2020_note_version.md` |

**注意点**
- 7ページ大部分黒塗り（1.4(a)/1.4(c)区分）
- 3タイムコードで4機を観測・クラウドカバーで追跡困難
- Advanced Capabilities欄: NO

---

### #022 — テキスト抽出不可（ペルシャ湾・2020年8月）

| 項目 | 内容 |
|---|---|
| **タイトル** | テキスト抽出不可──ペルシャ湾・2020年8月【AI概要版 #022】 |
| **元PDFファイル名** | dow-uap-d60-mission-report-persian-gulf-august-2020.pdf |
| **公開状況** | **公開済み** |
| **note URL** | https://note.com/deft_ibis3303/n/n66824c3adede |
| **テーマ分類** | 軍用機MISREP（ペルシャ湾・2020年8月）※OCR不可 |
| **ドラフトファイル** | `published_articles/ai_summary_022_d60_persian_gulf_aug2020_note_version.md` |

**注意点**
- 6ページ・テキスト層なし（抽出文字数約5文字）・スキャン画像のみ
- OCR不可のため内容解析不可として記事化

---

### #023 — 安保施設上空で8分間目視された大型青色三角形（太平洋時間帯・2023年3月）

| 項目 | 内容 |
|---|---|
| **タイトル** | 安保施設上空で8分間目視された大型青色三角形──太平洋時間帯・2023年3月【AI概要版 #023】 |
| **元PDFファイル名** | dow-uap-d51-email-correspondence-pacific-time-zone-march-2023.pdf |
| **公開状況** | **公開済み** |
| **note URL** | https://note.com/deft_ibis3303/n/n84094afa1a51 |
| **テーマ分類** | 機密解除メール・民間目撃・AFOSI関与（太平洋時間帯・2023年3月） |
| **ドラフトファイル** | `published_articles/ai_summary_023_d51_pacific_email_2023_note_version.md` |

**注意点**
- 民間人による安保施設上空目撃・後退するジャンプ動作の記述
- AFOSI派生分類審査済み・SECRET//NOFORNから非機密への分類変更承認

---

### #024 — 高高度・高速で複数の不明飛行物体（パプアニューギニア・1985年1月）

| 項目 | 内容 |
|---|---|
| **タイトル** | 高高度・高速で複数の不明飛行物体──パプアニューギニア・1985年1月【AI概要版 #024】 |
| **元PDFファイル名** | dos-uap-d1-cable-1-papua-new-guinea-january-1985.pdf |
| **公開状況** | **公開済み** |
| **note URL** | https://note.com/deft_ibis3303/n/n9dc6f10e4146 |
| **テーマ分類** | 国務省外交電報（パプアニューギニア・1985年） |
| **ドラフトファイル** | `published_articles/ai_summary_024_dos_d1_papua_new_guinea_1985_note_version.md` |

**注意点**
- 初の国務省（DoS）外交電報記事
- Air Niuginiパイロットがレーダー確認・米大使館は該当機なしと回答
- MRN 85 PORT MORESBY 199・CSP-2025-00040

---

### #025 — 機体より速く飛行したUAP（アデン湾・2024年7月）

| 項目 | 内容 |
|---|---|
| **タイトル** | 機体より速く飛行したUAP──アデン湾・2024年7月【AI概要版 #025】 |
| **元PDFファイル名** | dow-uap-d75-mission-report-gulf-of-aden-july-2024.pdf |
| **公開状況** | **公開済み** |
| **note URL** | https://note.com/deft_ibis3303/n/n381bc0b8487a |
| **テーマ分類** | 軍用機MISREP（アデン湾・2024年7月） |
| **ドラフトファイル** | `published_articles/ai_summary_025_d75_gulf_of_aden_2024_note_version.md` |

**注意点**
- 「観測機より速い」UAP・124 ATKS / 132 Wing・低高度NW飛行
- USCENTCOM MDR 25-0072・2025年6月2日 AARO承認
- observer評価はBenign・装備影響なし

---

## 統計サマリー

| 項目 | 値 |
|---|---|
| 総記事数 | 24件（#001〜#025、#017除く） |
| **公開済み（Git版一致）** | **15件（#010〜#016・#018〜#025）** |
| **公開済み（Git版は参考ドラフト）** | **4件（#006〜#009）** |
| 未公開 | 5件（#001〜#005） |
| テーマ: アポロ計画 | 4件（#004〜#007） |
| テーマ: FBI/目撃証言 | 3件（#001〜#003） |
| テーマ: 軍用機ISR/Range Fouler | 6件（#008・#009・#012・#013・#018） |
| テーマ: 軍用機MISREP | 4件（#011・#014・#016・#019） |
| テーマ: ティアライン承認メール | 2件（#010・#015） |

---

## archive_drafts/ に格納された旧版ドラフト

以下のドラフトは問題のある表現を含むため `archive_drafts/` へ移動済み。参照のみ可。

| ファイル | 問題点 | 代替ファイル |
|---|---|---|
| `archive_drafts/ai_reading_001_composite-sketch_20240430.md` | #001旧速報版。フォーマット基準未適用 | `note_drafts/ai_reading_001_composite-sketch_20240430_note_version.md` |
| `archive_drafts/ai_reading_007_apollo17_technical_debriefing_note_version.md` | 「直接的な証拠」という強い表現あり | `published_articles/ai_summary_007_apollo17_debriefing_note_version_revised.md` |
| `archive_drafts/ai_reading_008_d38_middle_east_isr_note_version.md` | 「IRSセンサー」誤記・Black Hot断定表現 | `published_articles/ai_summary_008_persian_gulf_range_fouler_note_version_revised.md` |

---

## #016〜#020 候補（次バッチ）

article_candidates.csvより、未使用かつスコア上位のものを選定。

| 優先順 | ファイル名 | スコア | ページ数 | 推奨理由 | リスクメモ |
|---|---|---|---|---|---|
| **#016** | `dow-uap-d6-mission-report-arabian-gulf-2020.pdf` | 55 | 7 | MISREPとして処理実績あり。アラビア湾2020。テキスト層あり | カタログ上の場所が「Pacific Ocean」だがファイル名はArabian Gulf。要確認 |
| **#017** | `dow-uap-d42-range-fouler-debrief-japan-2023.pdf` | 45 | 1 | ファイル名に「japan」含む誤認記録。実際はアラビア湾（MGRS 39RWL）。誤解解消の記事として価値高い | OCR文字化け多数。ファイル名と発生場所の乖離に関する注意書き必須 |
| **#018** | `dow-uap-d58-range-fouler-debrief-na-october-2020.pdf` | 45 | 1 | Range Foulerフォーム1ページ。処理が速い。2020年10月 | 場所「N/A」。内容確認が必要 |
| **#019** | `dow-uap-d4-mission-report-arabian-gulf-2020.pdf` | 40 | 5 | 5ページMISREP。アラビア湾2020。テキスト層あり | インシデント日付「N/A」。内容確認が必要 |
| **#020** | `dow-uap-d25-mission-report-greece-january-2024.pdf` | 35 | 7 | 地中海・ギリシャ周辺（既存記事と異なる地域）。2024年1月 | 7ページ。内容確認が必要 |

> **除外理由**
> - `nasa-uap-d5`：UAP記録ではなくUV天文学（Lyman-alpha）。記事化不適（nightly_reportで確認済み）
> - `nasa-uap-d6`：#007で使用済み
> - `dow-uap-d38/d44/d52/d56/d57/d28/d20/d50`：#008〜#015で使用済み

---

---

## 運用ルール：公開後のGit同期について

### 基本方針

記事公開後、可能な範囲でnote公開版の内容をGitドラフトへ反映することを推奨します。

### 同期の優先度

| 優先度 | 状況 | 対応 |
|---|---|---|
| **高** | 公開版でERROR・WARNINGに相当する修正が行われた場合 | Gitドラフトを公開版に合わせて更新し、再コミット |
| **中** | 文章の改善・表現変更など軽微な修正が行われた場合 | 余裕があれば反映。難しければ本ファイルの注意点欄に変更概要を記録 |
| **低** | 体裁調整・誤字修正のみの場合 | 対応不要。正本はnote側と明記するにとどめる |

### 同期できない場合の記録方法

Gitドラフトをnote公開版に合わせられない場合は、本ファイルの該当記事の「注意点」欄に以下を記録してください。

```
- 公開版との主な差分：[変更の概要を1〜2文で記述]
```

### 正本の所在

- **Git未同期の公開記事（#006〜#009）**：正本はnote側
- **Git同期済みの公開記事（#010〜）**：Git版・note版が一致

---

*このファイルは `review_logs/published_articles.md` として管理します。*
*記事公開のたびに「公開状況」欄を手動で更新してください。*
