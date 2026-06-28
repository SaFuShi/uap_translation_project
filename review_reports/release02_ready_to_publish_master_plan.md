# Release 02 正式在庫化 統合 dry-run マスタープラン
**作成日：** 2026-06-20  
**ステータス：** DRY-RUN（source_registry.csv / workflow.db 未変更）  
**対象：** DONE_CANDIDATE 61件  

---

## 1. 全体サマリー

| 区分 | 件数 |
|---|---|
| 前バッチA（DOW-UAP-PR019〜049） | 27件 |
| 前バッチB（FBI-UAP-PR001〜006） | 6件 |
| **前バッチ合計** | **33件** |
| 今回バッチ（DOW-UAP-PR071〜099） | 28件 |
| **登録予定合計** | **61件** |
| HOLD | **0件** |
| SKIP | **0件**（PR098は別管理） |

| チェック項目 | 結果 |
|---|---|
| note_draft 全件存在 | OK（61/61） |
| Codex監査実施済み | OK（61/61 / iter2〜3） |
| 実質BLOCK | 0件（全件DONE_CANDIDATE） |
| article_id重複 | **なし** |
| publish_order重複 | **なし** |
| 概要版#2_XXX重複 | **なし** |

---

## 2. 番号体系（確定）

| バッチ | 件数 | article_id範囲 | #2_XXX範囲 | publish_order範囲 |
|---|---|---|---|---|
| 前バッチA（PR019〜049） | 27件 | R02-010〜R02-036 | #2_010〜#2_036 | 2010〜2036 |
| 前バッチB（FBI-PR001〜006） | 6件 | R02-037〜R02-042 | #2_037〜#2_042 | 2037〜2042 |
| 中間バッチ（PR053〜069）※保留 | 18件 | R02-043〜R02-060 | #2_043〜#2_060 | 2043〜2060 |
| 今回バッチ（PR071〜099） | 28件 | R02-061〜R02-088 | #2_061〜#2_088 | 2061〜2088 |

> 中間バッチ（PR053〜069）は未処理・番号枠のみ確保。今回登録対象外。

---

## 3. 前バッチA：DOW-UAP-PR019〜049（27件）

| No. | PR番号 | article_id | #2_XXX | pub_order | 事案地域 | 事案年 | DVIDS ID | Codex最終 | draft | frames | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PR019 | R02-010 | #2_010 | 2010 | Middle East | 2022年5月 | 1006056 | iter2 BLOCK | OK | 2 | DONE_CANDIDATE |
| 2 | PR021 | R02-011 | #2_011 | 2011 | Iraq | 2022年5月 | 1006059 | iter2 BLOCK | OK | 3 | DONE_CANDIDATE |
| 3 | PR022 | R02-012 | #2_012 | 2012 | Syria | 2022年7月 | 1006060 | iter2 WARN | OK | 3 | DONE_CANDIDATE |
| 4 | PR023 | R02-013 | #2_013 | 2013 | Iraq | 2022年12月 | 1006062 | iter2 BLOCK | OK | 3 | DONE_CANDIDATE |
| 5 | PR026 | R02-014 | #2_014 | 2014 | UAE | 2023年10月 | 1006063 | iter2 BLOCK | OK | 9 | DONE_CANDIDATE |
| 6 | PR027 | R02-015 | #2_015 | 2015 | UAE | 2023年10月 | 1006067 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 7 | PR028 | R02-016 | #2_016 | 2016 | Greece | 2024年1月 | 1006073 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 8 | PR029 | R02-017 | #2_017 | 2017 | Gulf of Oman | 2024年6月 | 1006074 | iter2 BLOCK | OK | 5 | DONE_CANDIDATE |
| 9 | PR031 | R02-018 | #2_018 | 2018 | Syria | 2024年10月 | 1006076 | iter2 WARN | OK | 2 | DONE_CANDIDATE |
| 10 | PR032 | R02-019 | #2_019 | 2019 | Syria | 2024年10月 | 1006078 | iter2 WARN | OK | 2 | DONE_CANDIDATE |
| 11 | PR033 | R02-020 | #2_020 | 2020 | Syria | 2024年10月 | 1006079 | iter2 BLOCK | OK | 2 | DONE_CANDIDATE |
| 12 | PR034 | R02-021 | #2_021 | 2021 | Greece | 2023年10月 | 1006080 | iter2 BLOCK | OK | 6 | DONE_CANDIDATE ※1 |
| 13 | PR035 | R02-022 | #2_022 | 2022 | Greece | 2023年10月 | 1006082 | iter3 BLOCK | OK | 5 | DONE_CANDIDATE |
| 14 | PR036 | R02-023 | #2_023 | 2023 | Middle East | 2020年5月 | 1006083 | iter2 WARN | OK | 5 | DONE_CANDIDATE |
| 15 | PR037 | R02-024 | #2_024 | 2024 | Arabian Gulf | 2020年 | 1006087 | iter2 BLOCK | OK | 2 | DONE_CANDIDATE |
| 16 | PR038 | R02-025 | #2_025 | 2025 | Middle East | 2013年 | 1006088 | iter3 BLOCK | OK | 10 | DONE_CANDIDATE ※2 |
| 17 | PR039 | R02-026 | #2_026 | 2026 | Arabian Gulf | 2020年 | 1006089 | iter2 BLOCK | OK | 2 | DONE_CANDIDATE |
| 18 | PR040 | R02-027 | #2_027 | 2027 | Arabian Gulf | 2020年 | 1006093 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 19 | PR041 | R02-028 | #2_028 | 2028 | Arabian Gulf | 2020年 | 1006094 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 20 | PR042 | R02-029 | #2_029 | 2029 | Arabian Gulf | 2020年 | 1006097 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 21 | PR043 | R02-030 | #2_030 | 2030 | Djibouti | 2025年 | 1006159 | iter2 WARN | OK | 3 | DONE_CANDIDATE |
| 22 | PR044 | R02-031 | #2_031 | 2031 | Arabian Gulf | 2020年 | 1006104 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 23 | PR045 | R02-032 | #2_032 | 2032 | Southern US | 2020年 | 1006105 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 24 | PR046 | R02-033 | #2_033 | 2033 | East China Sea | 2024年 | 1006106 | iter2 BLOCK | OK | 2 | DONE_CANDIDATE |
| 25 | PR047 | R02-034 | #2_034 | 2034 | Japan | 2023年 | 1006107 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 26 | PR048 | R02-035 | #2_035 | 2035 | Indo-PACOM | 2024年 | 1006110 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 27 | PR049 | R02-036 | #2_036 | 2036 | North America | 2026年 | 1006111 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |

---

## 4. 前バッチB：FBI-UAP-PR001〜006（6件）

| No. | PR番号 | article_id | #2_XXX | pub_order | 事案地域 | 事案年月 | DVIDS ID | Codex最終 | draft | frames | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 28 | FBI-PR001 | R02-037 | #2_037 | 2037 | Northeastern US | 2021年11月 | 1010263 | iter3 BLOCK | OK | 6 | DONE_CANDIDATE |
| 29 | FBI-PR002 | R02-038 | #2_038 | 2038 | Northeastern US | 2022年3月 | 1010264 | iter2 BLOCK | OK | 6 | DONE_CANDIDATE |
| 30 | FBI-PR003 | R02-039 | #2_039 | 2039 | Northeastern US | 2024年10月 | 1010267 | iter2 BLOCK | OK | 9 | DONE_CANDIDATE |
| 31 | FBI-PR004 | R02-040 | #2_040 | 2040 | Northeastern US | 2025年7月 | 1010269 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 32 | FBI-PR005 | R02-041 | #2_041 | 2041 | Western US | 2023年10月 | 1010272 | iter2 WARN | OK | 2 | DONE_CANDIDATE |
| 33 | FBI-PR006 | R02-042 | #2_042 | 2042 | Western US | 2023年10月 | 1010276 | iter2 BLOCK | OK | 1 | DONE_CANDIDATE |

---

## 5. 今回バッチ：DOW-UAP-PR071〜099（28件）

| No. | PR番号 | article_id | #2_XXX | pub_order | 事案地域 | 事案年 | DVIDS ID | Codex最終 | draft | frames | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 34 | PR071 | R02-061 | #2_061 | 2061 | NORTHCOM | 2023年 | 1007784 | iter3 BLOCK | OK | 10 | DONE_CANDIDATE ※3 |
| 35 | PR072 | R02-062 | #2_062 | 2062 | Kazakhstan | 2022年 | 1007788 | iter2 WARN | OK | 4 | DONE_CANDIDATE |
| 36 | PR073 | R02-063 | #2_063 | 2063 | Midwestern US | 2022年 | 1007790 | iter2 BLOCK | OK | 3 | DONE_CANDIDATE |
| 37 | PR074 | R02-064 | #2_064 | 2064 | CENTCOM | 2022年6月13日 | 1007791 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 38 | PR075 | R02-065 | #2_065 | 2065 | East China Sea | 2021年6月9日 | 1007795 | iter2 BLOCK | OK | 5 | DONE_CANDIDATE ※4 |
| 39 | PR076 | R02-066 | #2_066 | 2066 | CENTCOM | 2021年1月3日 | 1007804 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 40 | PR077 | R02-067 | #2_067 | 2067 | CENTCOM | 2020年11月2日 | 1007809 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 41 | PR078 | R02-068 | #2_068 | 2068 | CENTCOM | 2020年11月2日 | 1007812 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 42 | PR079 | R02-069 | #2_069 | 2069 | CENTCOM | 2020年10月29日 | 1007816 | iter2 BLOCK | OK | 9 | DONE_CANDIDATE |
| 43 | PR080 | R02-070 | #2_070 | 2070 | CENTCOM | 2020年10月20日 | 1007803 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 44 | PR081 | R02-071 | #2_071 | 2071 | AFRICOM | 2020年10月18日 | 1007805 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 45 | PR082 | R02-072 | #2_072 | 2072 | AFRICOM | 2020年10月16日 | 1007807 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 46 | PR083 | R02-073 | #2_073 | 2073 | CENTCOM | 2020年10月7日 | 1007808 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 47 | PR084 | R02-074 | #2_074 | 2074 | CENTCOM | 2020年9月17日 | 1007810 | iter2 BLOCK | OK | 9 | DONE_CANDIDATE |
| 48 | PR085 | R02-075 | #2_075 | 2075 | CENTCOM | 2020年9月16日 | 1007796 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 49 | PR086 | R02-076 | #2_076 | 2076 | NORTHCOM | 2019年12月 | 1007797 | iter2 WARN | OK | 7 | DONE_CANDIDATE |
| 50 | PR087 | R02-077 | #2_077 | 2077 | CENTCOM | 2020年9月5日 | 1007799 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 51 | PR088 | R02-078 | #2_078 | 2078 | CENTCOM | 2020年8月31日 | 1007800 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 52 | PR089 | R02-079 | #2_079 | 2079 | CENTCOM | 2020年8月31日 | 1007712 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 53 | PR090 | R02-080 | #2_080 | 2080 | CENTCOM | 2020年8月24日 | 1007719 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 54 | PR091 | R02-081 | #2_081 | 2081 | CENTCOM | 2020年8月21日 | 1007716 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 55 | PR092 | R02-082 | #2_082 | 2082 | CENTCOM | 2020年8月8日 | 1007715 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 56 | PR093 | R02-083 | #2_083 | 2083 | CENTCOM | 2020年5月5日 | 1007721 | iter2 WARN | OK | 7 | DONE_CANDIDATE |
| 57 | PR094 | R02-084 | #2_084 | 2084 | CENTCOM | 2020年2月13日 | 1007722 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |
| 58 | PR095 | R02-085 | #2_085 | 2085 | CENTCOM | 2020年5月5日 | 1007725 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 59 | PR096 | R02-086 | #2_086 | 2086 | CENTCOM | 2018年7月3日 | 1007726 | iter2 WARN | OK | 3 | DONE_CANDIDATE |
| 60 | PR097 | R02-087 | #2_087 | 2087 | CENTCOM | 2019年9月25日 21:35Z | 1007728 | iter2 WARN | OK | 10 | DONE_CANDIDATE |
| 61 | PR099 | R02-088 | #2_088 | 2088 | CENTCOM | 2023年 | 1007738 | iter2 BLOCK | OK | 10 | DONE_CANDIDATE |

---

## 6. 注記（※番号参照）

### ※1 PR034 — PDF既公開記事との関連

- **状況：** 同一DVIDS ID 1006080 の PDF「dow-uap-d33-mission-report-greece-october-2023.pdf」が source_registry #032 として公開済み
- **対応推奨：** 記事内に「関連文書：DOW-UAP-D33（source_registry #032）」を追記
- **判定：** 別フォーマット（VID vs PDF）の独立記事として登録可能。DONE_CANDIDATE

### ※2 PR038 — DVIDS Title「Resolved as an Aircraft」

- **状況：** DVIDSビデオタイトル「Resolved as an Aircraft, Middle East 2013」への言及をドラフトに追記済み（iter3で確認）
- **対応済み：** ファイル名「Unresolved」との不一致を記事内で説明
- **確認ポイント：** 本映像では「Resolved（解決済み）」の根拠は確認できない旨の記述が適切か最終確認推奨
- **判定：** DONE_CANDIDATE

### ※3 PR071 — F-16C・ヒューロン湖UAP撃墜事案

- **状況：** Release 02で最も重要度の高い公的記録の可能性がある事案。iter3まで実施済み
- **確認ポイント：** 映像フレームの記述（00:15からIR映像）・代表フレーム frame_0040 の内容
- **判定：** DONE_CANDIDATE

### ※4 PR075 — 東シナ海・プラットフォーム表現

- **状況：** iter2で P2-2 BLOCK（platform表現に不確実性が必要）が検出されたが、最終ドラフトでは修正済み（PASS）
- **判定：** DONE_CANDIDATE

---

## 7. BLOCK/WARN 種別集計（全61件）

### 残留BLOCKの種別

| BLOCK種別 | 件数 | 判定 |
|---|---|---|
| source_registry未登録（P1-REG/P1-1a等） | 全61件共通 | 在庫化で解消。許容 |
| WAR.GOV URLトップページ（P1-1c等） | 複数件 | 設計共通。許容 |
| 実質BLOCK（DONE_CANDIDATE非該当） | **0件** | - |

### Codex最終VERDICT集計

| VERDICT | 前バッチA | 前バッチB | 今回バッチ | 合計 |
|---|---|---|---|---|
| WARN | 8件 | 1件 | 14件 | **23件** |
| BLOCK（source_registry系のみ） | 19件 | 5件 | 14件 | **38件** |
| **合計** | **27件** | **6件** | **28件** | **61件** |

---

## 8. 重複確認マトリクス

### source_registry既存（登録済み）との重複なし

| 既存 | 番号 | 今回割当 |
|---|---|---|
| DOE-UAP-D001〜003 | R02-001〜003 | 重複なし（R02-010〜） |
| 欠番 | R02-004〜007 | 未割当（保留） |
| DOW-UAP-PR050/051 | R02-008〜009 | 重複なし（R02-010〜） |

### 連番チェック

| 範囲 | 件数 | 想定 | 過不足 |
|---|---|---|---|
| R02-010〜036 | 27件 | 27件 | **0** |
| R02-037〜042 | 6件 | 6件 | **0** |
| R02-043〜060 | 18件 | 18件（中間バッチ・未登録枠） | — |
| R02-061〜088 | 28件 | 28件 | **0** |

### publish_order チェック

| 範囲 | 既存 |
|---|---|
| 2000〜2003 | release02_intro / ODNI / CIA / DOW-D017（公開済み） |
| 2004〜2009 | DOE-D001〜003, PR050, PR051（未登録・保留） |
| 2010〜2088 | 今回割当 61件（重複なし） |

---

## 9. 人間確認リスト

### [必須確認]

| 対象 | 理由 | アクション |
|---|---|---|
| PR071 | Release 02最重要事案（F-16C UAP撃墜）。内容の正確性が公的影響を持つ | 映像フレーム記述・frame_0040内容の最終確認 |
| PR038 | DVIDS Title「Resolved as Aircraft」との不一致表現 | 記事内表現の適切さを最終確認 |

### [推奨確認]

| 対象 | 理由 | アクション |
|---|---|---|
| PR034 | PDF既公開記事（#032）との関連参照未追記 | 関連記事参照の追記 |
| FBI-PR006 | frames=1（フレーム1枚のみ） | サムネイル少数が記事として適切か確認 |
| PR046 | East China Sea・白い翼状物体 | 翼状表現の適切さ確認（断定回避） |
| PR099 | files_catalogのincident_dateが「2023年」だが記事は「2019年9月25日」 | ※補足参照 |

> **PR099補足：** DVIDS番号 1007738 とffiles_catalogのincident_dateの「2023年」はおそらくfiles_catalog側の記録誤り。ドラフトのファイル名「25SEP19_at_1715Z」から2019年9月25日が正しい。要確認。

---

## 10. 公開前 共通タスク（全61件）

正式在庫化後、公開前に全件で実施が必要な作業：

| タスク | 内容 | タイミング |
|---|---|---|
| タイトル更新 | 「#TBD」→ 正式 article_id（例：「R02-010」） | source_registry登録後 |
| 注意点セクション追加 | 独立見出し「## 注意点」を全件追加 | 公開preflight時 |
| 免責セクション整理 | 末尾注記を「## 免責」見出しに移動 | 公開preflight時 |
| source_registry未登録注記削除 | 末尾の未登録メモを削除（登録後） | source_registry登録後 |

---

## 11. 正式在庫化 実行ステップ（今後）

1. **人間側確認**（必須確認リスト対応）
2. **前バッチA（27件）を先行登録**
   - source_registry.csv へ R02-010〜036 追加
   - workflow.db へ 27件登録（status=preprocessed）
3. **前バッチB（6件）登録**
   - source_registry.csv へ R02-037〜042 追加
   - workflow.db へ 6件登録
4. **今回バッチ（28件）登録**
   - source_registry.csv へ R02-061〜088 追加
   - workflow.db へ 28件登録
5. **全61件タイトル更新**（#TBD → article_id）
6. **Review Package生成**（優先10件）
7. **中間バッチ（PR053〜069 18件）は別途処理**

---

## 12. SKIP / 対象外記事

| 記事 | 理由 | 今後の扱い |
|---|---|---|
| DOW-UAP-PR098 | 超長尺（1056秒・17分36秒）| SKIP継続。別途処理方針検討 |
| PR053〜069（18件）| 中間バッチ未処理 | 別途バッチ処理 |

---

**出力ファイル：** `review_reports/release02_ready_to_publish_master_plan.md`  
**作成：** 2026-06-20（dry-run）  
**参照元：**
- `review_reports/release02_prebatch_fix_report.md`
- `review_reports/ready_to_publish_plan_20260620_PR071-PR099.md`
- `review_reports/release02_numbering_plan.md`
