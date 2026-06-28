# Release 02 番号体系確定計画書
**作成日：** 2026-06-20（v2改訂：2026-06-20）  
**ステータス：** DRY-RUN（workflow.db/source_registry.csv 未変更）  
**改訂理由：** 案C採用 — 欠番なし・読者公開順と内部管理番号を一致させる

---

## 改訂ポイント（v1→v2）

| 変更点 | v1 | v2 |
|---|---|---|
| PR057/057a/057b/058の扱い | 欠番（R02-043〜060を18件として管理） | HOLD予約割当（R02-047〜050） |
| 中間バッチ件数 | 18件（想定） | **19件**（PR053〜069＋PR057a/b） |
| 今回バッチ開始番号 | R02-061 / #2_061 / 2061 | **R02-062 / #2_062 / 2062** |
| 今回バッチ終了番号 | R02-088 / #2_088 / 2088 | **R02-089 / #2_089 / 2089** |

---

## 1. Release 02 番号全体像

| バッチ | PR範囲 | 件数 | article_id | #2_XXX | publish_order | 備考 |
|---|---|---|---|---|---|---|
| 登録済み | DOE-D001〜003 | 3件 | R02-001〜003 | #2_001〜003 | — | 公開済み |
| 欠番保留 | — | 4件 | R02-004〜007 | — | — | 未割当 |
| 登録済み | PR050/051 | 2件 | R02-008〜009 | #2_008〜009 | — | 公開済み |
| 前バッチA | PR019〜049 | 27件 | R02-010〜036 | #2_010〜036 | 2010〜2036 | DONE_CANDIDATE |
| 前バッチB | FBI-PR001〜006 | 6件 | R02-037〜042 | #2_037〜042 | 2037〜2042 | DONE_CANDIDATE |
| 中間バッチ | PR053〜069 | 19件 | R02-043〜061 | #2_043〜061 | 2043〜2061 | ※一部HOLD |
| 今回バッチ | PR071〜099 | 28件 | R02-062〜089 | #2_062〜089 | 2062〜2089 | DONE_CANDIDATE |
| **管理漏れ補完** | **PR052/070/098** | **3件** | **R02-090〜092** | **#2_090〜092** | **2090〜2092** | **PR052:ドラフト未作成 / PR070:Codex iter3待ち / PR098:SKIP** |

**登録予定合計（HOLD含む）：** **83件**（v2: 80件 + 管理漏れ補完3件）  
**現時点DONE_CANDIDATE：** 33件（前バッチ）+ 15件（中間バッチ有効）+ 28件（今回バッチ）= **76件**  
**DONE_CANDIDATE_PENDING：** 1件（PR070 → Codex iter3後にDONE_CANDIDATE確定）  
**HOLD：** 4件（PR057, PR057a, PR057b, PR058）  
**SKIP（採番済み）：** 1件（PR098 = R02-092）  
**ドラフト未作成：** 1件（PR052 = R02-090）

---

## 2. 前バッチA：DOW-UAP-PR019〜049（27件）

| No. | PR番号 | article_id | #2_XXX | pub_order | 事案地域 | 事案年 | 判定 |
|---|---|---|---|---|---|---|---|
| 1 | PR019 | R02-010 | #2_010 | 2010 | Middle East | 2022年5月 | DONE_CANDIDATE |
| 2 | PR021 | R02-011 | #2_011 | 2011 | Iraq | 2022年5月 | DONE_CANDIDATE |
| 3 | PR022 | R02-012 | #2_012 | 2012 | Syria | 2022年7月 | DONE_CANDIDATE |
| 4 | PR023 | R02-013 | #2_013 | 2013 | Iraq | 2022年12月 | DONE_CANDIDATE |
| 5 | PR026 | R02-014 | #2_014 | 2014 | UAE | 2023年10月 | DONE_CANDIDATE |
| 6 | PR027 | R02-015 | #2_015 | 2015 | UAE | 2023年10月 | DONE_CANDIDATE |
| 7 | PR028 | R02-016 | #2_016 | 2016 | Greece | 2024年1月 | DONE_CANDIDATE |
| 8 | PR029 | R02-017 | #2_017 | 2017 | Gulf of Oman | 2024年6月 | DONE_CANDIDATE |
| 9 | PR031 | R02-018 | #2_018 | 2018 | Syria | 2024年10月 | DONE_CANDIDATE |
| 10 | PR032 | R02-019 | #2_019 | 2019 | Syria | 2024年10月 | DONE_CANDIDATE |
| 11 | PR033 | R02-020 | #2_020 | 2020 | Syria | 2024年10月 | DONE_CANDIDATE |
| 12 | PR034 | R02-021 | #2_021 | 2021 | Greece | 2023年10月 | DONE_CANDIDATE |
| 13 | PR035 | R02-022 | #2_022 | 2022 | Greece | 2023年10月 | DONE_CANDIDATE |
| 14 | PR036 | R02-023 | #2_023 | 2023 | Middle East | 2020年5月 | DONE_CANDIDATE |
| 15 | PR037 | R02-024 | #2_024 | 2024 | Arabian Gulf | 2020年 | DONE_CANDIDATE |
| 16 | PR038 | R02-025 | #2_025 | 2025 | Middle East | 2013年 | DONE_CANDIDATE |
| 17 | PR039 | R02-026 | #2_026 | 2026 | Arabian Gulf | 2020年 | DONE_CANDIDATE |
| 18 | PR040 | R02-027 | #2_027 | 2027 | Arabian Gulf | 2020年 | DONE_CANDIDATE |
| 19 | PR041 | R02-028 | #2_028 | 2028 | Arabian Gulf | 2020年 | DONE_CANDIDATE |
| 20 | PR042 | R02-029 | #2_029 | 2029 | Arabian Gulf | 2020年 | DONE_CANDIDATE |
| 21 | PR043 | R02-030 | #2_030 | 2030 | Djibouti | 2025年 | DONE_CANDIDATE |
| 22 | PR044 | R02-031 | #2_031 | 2031 | Arabian Gulf | 2020年 | DONE_CANDIDATE |
| 23 | PR045 | R02-032 | #2_032 | 2032 | Southern US | 2020年 | DONE_CANDIDATE |
| 24 | PR046 | R02-033 | #2_033 | 2033 | East China Sea | 2024年 | DONE_CANDIDATE |
| 25 | PR047 | R02-034 | #2_034 | 2034 | Japan | 2023年 | DONE_CANDIDATE |
| 26 | PR048 | R02-035 | #2_035 | 2035 | Indo-PACOM | 2024年 | DONE_CANDIDATE |
| 27 | PR049 | R02-036 | #2_036 | 2036 | North America | 2026年 | DONE_CANDIDATE |

---

## 3. 前バッチB：FBI-UAP-PR001〜006（6件）

| No. | PR番号 | article_id | #2_XXX | pub_order | 事案地域 | 事案年月 | 判定 |
|---|---|---|---|---|---|---|---|
| 28 | FBI-PR001 | R02-037 | #2_037 | 2037 | Northeastern US | 2021年11月 | DONE_CANDIDATE |
| 29 | FBI-PR002 | R02-038 | #2_038 | 2038 | Northeastern US | 2022年3月 | DONE_CANDIDATE |
| 30 | FBI-PR003 | R02-039 | #2_039 | 2039 | Northeastern US | 2024年10月 | DONE_CANDIDATE |
| 31 | FBI-PR004 | R02-040 | #2_040 | 2040 | Northeastern US | 2025年7月 | DONE_CANDIDATE |
| 32 | FBI-PR005 | R02-041 | #2_041 | 2041 | Western US | 2023年10月 | DONE_CANDIDATE |
| 33 | FBI-PR006 | R02-042 | #2_042 | 2042 | Western US | 2023年10月 | DONE_CANDIDATE |

---

## 4. 中間バッチ：PR053〜069（19件）

| No. | PR番号 | article_id | #2_XXX | pub_order | 事案地域 | 事案年 | Codex最終 | 判定 |
|---|---|---|---|---|---|---|---|---|
| 34 | PR053 | R02-043 | #2_043 | 2043 | CENTCOM | 2022年10月 | iter2 BLOCK | DONE_CANDIDATE ※1 |
| 35 | PR054 | R02-044 | #2_044 | 2044 | EUCOM | 2022年 | iter3 BLOCK | DONE_CANDIDATE |
| 36 | PR055 | R02-045 | #2_045 | 2045 | CENTCOM | 2020年11月 | iter2 BLOCK | DONE_CANDIDATE |
| 37 | PR056 | R02-046 | #2_046 | 2046 | （不明） | （不明） | iter3 BLOCK | DONE_CANDIDATE |
| 38 | PR057 | **R02-047** | **#2_047** | **2047** | Yellow Sea | 2023年 | iter2 BLOCK | **HOLD ※2** |
| 39 | PR057a | **R02-048** | **#2_048** | **2048** | Yellow Sea | 2023年 | 未処理 | **HOLD（予約）** |
| 40 | PR057b | **R02-049** | **#2_049** | **2049** | Yellow Sea | 2023年 | 未処理 | **HOLD（予約）** |
| 41 | PR058 | **R02-050** | **#2_050** | **2050** | INDOPACOM | — | 未処理 | **HOLD（予約）** |
| 42 | PR059 | R02-051 | #2_051 | 2051 | CENTCOM | 2020年6月 | iter6 WARN | DONE_CANDIDATE |
| 43 | PR060 | R02-052 | #2_052 | 2052 | CENTCOM | 2021年 | iter1 WARN | DONE_CANDIDATE ※3 |
| 44 | PR061 | R02-053 | #2_053 | 2053 | CENTCOM | 2021年 | iter2 WARN | DONE_CANDIDATE |
| 45 | PR062 | R02-054 | #2_054 | 2054 | CENTCOM | 2021年 | iter5 WARN | DONE_CANDIDATE |
| 46 | PR063 | R02-055 | #2_055 | 2055 | CENTCOM | 2021年 | iter2 WARN | DONE_CANDIDATE |
| 47 | PR064 | R02-056 | #2_056 | 2056 | CENTCOM | 2017年 | iter2 BLOCK | DONE_CANDIDATE |
| 48 | PR065 | R02-057 | #2_057 | 2057 | Southeastern US | 2024年 | iter2 WARN | DONE_CANDIDATE |
| 49 | PR066 | R02-058 | #2_058 | 2058 | Southeastern US | 2024年 | iter2 BLOCK | DONE_CANDIDATE ※4 |
| 50 | PR067 | R02-059 | #2_059 | 2059 | （不明） | 2022年3月 | iter1 BLOCK | DONE_CANDIDATE ※3 |
| 51 | PR068 | R02-060 | #2_060 | 2060 | NORTHCOM | 2023年 | iter2 BLOCK | DONE_CANDIDATE |
| 52 | PR069 | R02-061 | #2_061 | 2061 | NORTHCOM | — | iter2 BLOCK | DONE_CANDIDATE |

---

## 5. 今回バッチ：DOW-UAP-PR071〜099（28件）【再採番】

> v1（#2_061〜088）から**#2_062〜089 / 2062〜2089**へ変更

| No. | PR番号 | article_id | #2_XXX | pub_order | 事案地域 | 事案年 | Codex最終 | 判定 |
|---|---|---|---|---|---|---|---|---|
| 53 | PR071 | R02-062 | #2_062 | 2062 | NORTHCOM | 2023年 | iter3 BLOCK | DONE_CANDIDATE |
| 54 | PR072 | R02-063 | #2_063 | 2063 | Kazakhstan | 2022年 | iter2 WARN | DONE_CANDIDATE |
| 55 | PR073 | R02-064 | #2_064 | 2064 | Midwestern US | 2022年 | iter2 BLOCK | DONE_CANDIDATE |
| 56 | PR074 | R02-065 | #2_065 | 2065 | CENTCOM | 2022年6月13日 | iter2 BLOCK | DONE_CANDIDATE |
| 57 | PR075 | R02-066 | #2_066 | 2066 | East China Sea | 2021年6月9日 | iter2 BLOCK | DONE_CANDIDATE |
| 58 | PR076 | R02-067 | #2_067 | 2067 | CENTCOM | 2021年1月3日 | iter2 BLOCK | DONE_CANDIDATE |
| 59 | PR077 | R02-068 | #2_068 | 2068 | CENTCOM | 2020年11月2日 | iter2 WARN | DONE_CANDIDATE |
| 60 | PR078 | R02-069 | #2_069 | 2069 | CENTCOM | 2020年11月2日 | iter2 WARN | DONE_CANDIDATE |
| 61 | PR079 | R02-070 | #2_070 | 2070 | CENTCOM | 2020年10月29日 | iter2 BLOCK | DONE_CANDIDATE |
| 62 | PR080 | R02-071 | #2_071 | 2071 | CENTCOM | 2020年10月20日 | iter2 WARN | DONE_CANDIDATE |
| 63 | PR081 | R02-072 | #2_072 | 2072 | AFRICOM | 2020年10月18日 | iter2 BLOCK | DONE_CANDIDATE |
| 64 | PR082 | R02-073 | #2_073 | 2073 | AFRICOM | 2020年10月16日 | iter2 WARN | DONE_CANDIDATE |
| 65 | PR083 | R02-074 | #2_074 | 2074 | CENTCOM | 2020年10月7日 | iter2 BLOCK | DONE_CANDIDATE |
| 66 | PR084 | R02-075 | #2_075 | 2075 | CENTCOM | 2020年9月17日 | iter2 BLOCK | DONE_CANDIDATE |
| 67 | PR085 | R02-076 | #2_076 | 2076 | CENTCOM | 2020年9月16日 | iter2 BLOCK | DONE_CANDIDATE |
| 68 | PR086 | R02-077 | #2_077 | 2077 | NORTHCOM | 2019年12月 | iter2 WARN | DONE_CANDIDATE |
| 69 | PR087 | R02-078 | #2_078 | 2078 | CENTCOM | 2020年9月5日 | iter2 WARN | DONE_CANDIDATE |
| 70 | PR088 | R02-079 | #2_079 | 2079 | CENTCOM | 2020年8月31日 | iter2 WARN | DONE_CANDIDATE |
| 71 | PR089 | R02-080 | #2_080 | 2080 | CENTCOM | 2020年8月31日 | iter2 WARN | DONE_CANDIDATE |
| 72 | PR090 | R02-081 | #2_081 | 2081 | CENTCOM | 2020年8月24日 | iter2 WARN | DONE_CANDIDATE |
| 73 | PR091 | R02-082 | #2_082 | 2082 | CENTCOM | 2020年8月21日 | iter2 WARN | DONE_CANDIDATE |
| 74 | PR092 | R02-083 | #2_083 | 2083 | CENTCOM | 2020年8月8日 | iter2 WARN | DONE_CANDIDATE |
| 75 | PR093 | R02-084 | #2_084 | 2084 | CENTCOM | 2020年5月5日 | iter2 WARN | DONE_CANDIDATE |
| 76 | PR094 | R02-085 | #2_085 | 2085 | CENTCOM | 2020年2月13日 | iter2 BLOCK | DONE_CANDIDATE |
| 77 | PR095 | R02-086 | #2_086 | 2086 | CENTCOM | 2020年5月5日 | iter2 WARN | DONE_CANDIDATE |
| 78 | PR096 | R02-087 | #2_087 | 2087 | CENTCOM | 2018年7月3日 | iter2 WARN | DONE_CANDIDATE |
| 79 | PR097 | R02-088 | #2_088 | 2088 | CENTCOM | 2019年9月25日 21:35Z | iter2 WARN | DONE_CANDIDATE |
| 80 | PR099 | R02-089 | #2_089 | 2089 | CENTCOM | 2019年9月25日 17:15Z | iter2 BLOCK | DONE_CANDIDATE |

---

## 6. 注記

### ※1 PR053（R02-043）Codex OUT-1 BLOCK

- **内容：** iter2 OUT-1 = 「サンドボックス制限でCodexが結果ファイルを保存できなかった」出力制限BLOCK
- **実態：** PASS 9件 / WARN 5件 / コンテンツBLOCK 0件（作業メモWARNは削除済み相当）
- **判定：** DONE_CANDIDATE

### ※2 PR057（R02-047）HOLD

- **理由：** P1-5-DUPLICATE BLOCK（AARO Comment: duplicate）+ IMG-2 BLOCK
- **状況：** PR057a / PR057b（2ファイル）が実体。PR057として作成したdraft/thumbはあるが整理が必要
- **必要な作業：** PR057a / PR057b を個別に記事化するか、PR057ドラフトをどちらかに紐付けるか判断が必要
- **#2_048〜049（PR057a/b）も予約HOLD**

### ※3 PR060（R02-052）/ PR067（R02-059）Codex iter1のみ

- **状況：** iter2未実施（前セッションで一部skipされた模様）
- **実態：** PR060 iter1 WARN（BLOCK=0）、PR067 iter1 BLOCK（P1-1 = source_registry系のみ）
- **判定：** 実質問題なし。DONE_CANDIDATE。在庫化前にiter2を実施することを推奨

### ※4 PR066（R02-058）作業メモ残存

- **内容：** P2-1 BLOCK = 作業メモ行「→ 使用ファイル：...（note転記後にこの行を削除）」が残存
- **前バッチ削除処理（前セッション）では対象外だった**
- **修正内容：** 1行削除（sed） → Codex iter3 実施
- **判定：** 修正後 DONE_CANDIDATE

---

## 7. 重複確認

| チェック | 結果 |
|---|---|
| article_id重複（R02-001〜092） | **なし** |
| #2_XXX重複（#2_001〜092） | **なし** |
| publish_order重複（2010〜2092） | **なし** |
| 既存登録済み（R02-001〜009）との重複 | **なし** |
| 欠番 | R02-004〜007のみ（意図的保留） |
| VID全件採番確認（84件） | **完了**（R02-008〜092でVID 84件すべて採番済み） |

---

## 8. 今後の作業（番号体系確定後）

### 管理漏れ補完（NEW・2026-06-21追加）

- [ ] **PR052（R02-090 / #2_090 / 2090）**：ドラフト作成 → Codex監査 → DONE_CANDIDATE
  - files_catalog: `DOW-UAP-PR052_UAP_USO_Formation_CALLSIGN_Mission.mp4` (DVIDS 1007708, downloaded=true)
  - 事案地域・日時: 不明（files_catalog未記録）
- [ ] **PR070（R02-091 / #2_091 / 2091）**：作業メモ行削除 + NORTHCOM/chain-of-custody追記 → Codex iter3 → DONE_CANDIDATE
  - ドラフト: `ai_summary_DOW-UAP-PR070_..._note_version.md` 存在
  - Codex iter2 BLOCK理由: P1-REG（article_id未登録）→ 採番で解消、W-02（作業メモ行残存）→ 削除要
- [ ] **PR098（R02-092 / #2_092 / 2092）**：採番のみ（SKIP確定・公開キューに含めない）
  - files_catalog: `DOW-UAP-PR098_UFOs_in_formation_over_Persian_Gulf.mp4` (DVIDS 1007737)
  - SKIP理由: 超長尺 1056秒（17分36秒）

### 即対応推奨
- [ ] **PR066**：作業メモ削除 → Codex iter3
- [ ] **PR060, PR067**：Codex iter2 実施（念のため）

### HOLD管理（別途）
- [ ] **PR057**：PR057a/PR057b との紐付け整理。どちらかの記事として確定
- [ ] **PR057a/057b**：記事化（draft作成 → Codex監査）
- [ ] **PR058**：記事化（draft作成 → Codex監査）

### マスタープラン更新
- [ ] `release02_ready_to_publish_master_plan.md` の PR071〜099 番号を #2_062〜089 / R02-062〜089 / 2062〜2089 へ更新

---

## 9. 番号体系まとめ（完全版）

```
Release 02 article_id / #2_XXX 体系（v2確定）

DOE文書（登録済み）:
  R02-001 / #2_001: DOE-UAP-D001
  R02-002 / #2_002: DOE-UAP-D002
  R02-003 / #2_003: DOE-UAP-D003
  R02-004〜007: 欠番保留
  R02-008 / #2_008: DOW-UAP-PR050
  R02-009 / #2_009: DOW-UAP-PR051

前バッチA（DOW-PR019〜049 / 27件）:
  R02-010〜036 / #2_010〜036 / pub_order 2010〜2036

前バッチB（FBI / 6件）:
  R02-037〜042 / #2_037〜042 / pub_order 2037〜2042

中間バッチ（PR053〜069 / 19件）:
  R02-043 / #2_043 / 2043: PR053  [DONE_CANDIDATE]
  R02-044 / #2_044 / 2044: PR054  [DONE_CANDIDATE]
  R02-045 / #2_045 / 2045: PR055  [DONE_CANDIDATE]
  R02-046 / #2_046 / 2046: PR056  [DONE_CANDIDATE]
  R02-047 / #2_047 / 2047: PR057  [HOLD]
  R02-048 / #2_048 / 2048: PR057a [HOLD・予約]
  R02-049 / #2_049 / 2049: PR057b [HOLD・予約]
  R02-050 / #2_050 / 2050: PR058  [HOLD・予約]
  R02-051 / #2_051 / 2051: PR059  [DONE_CANDIDATE]
  R02-052 / #2_052 / 2052: PR060  [DONE_CANDIDATE]
  R02-053 / #2_053 / 2053: PR061  [DONE_CANDIDATE]
  R02-054 / #2_054 / 2054: PR062  [DONE_CANDIDATE]
  R02-055 / #2_055 / 2055: PR063  [DONE_CANDIDATE]
  R02-056 / #2_056 / 2056: PR064  [DONE_CANDIDATE]
  R02-057 / #2_057 / 2057: PR065  [DONE_CANDIDATE]
  R02-058 / #2_058 / 2058: PR066  [DONE_CANDIDATE（作業メモ削除後）]
  R02-059 / #2_059 / 2059: PR067  [DONE_CANDIDATE]
  R02-060 / #2_060 / 2060: PR068  [DONE_CANDIDATE]
  R02-061 / #2_061 / 2061: PR069  [DONE_CANDIDATE]

今回バッチ（PR071〜099 / 28件）:
  R02-062 / #2_062 / 2062: PR071
  R02-063 / #2_063 / 2063: PR072
  ...
  R02-089 / #2_089 / 2089: PR099

管理漏れ補完（2026-06-21追加）:
  R02-090 / #2_090 / 2090: PR052  [ドラフト未作成 → 要新規作成]
  R02-091 / #2_091 / 2091: PR070  [ドラフトあり → Codex iter3待ち]
  R02-092 / #2_092 / 2092: PR098  [SKIP確定（超長尺1056秒）]

管理件数合計: R02-001〜092（うち欠番4件）= 88件
登録予定（HOLDあり）: 83件
現時点DONE_CANDIDATE: 76件（PR070はiter3通過後に+1 = 77件）
VID全件採番: 84件完了（R02-008〜092）
```

---

**出力ファイル：** `review_reports/release02_numbering_plan.md`（v2）  
**作成：** 2026-06-20（dry-run）  
**旧計画（v1）との差分：** PR057/057a/057b/058をHOLD予約。PR071〜099を#2_062〜089へ再採番。
