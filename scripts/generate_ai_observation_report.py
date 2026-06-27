#!/usr/bin/env python3
"""
generate_ai_observation_report.py — AI Observation Report 自動生成

Media Inspector v2 (docs/media_inspector_architecture_v2.md) の
AI Observation Report 型レビューフローに基づき、Frame Delta CSV /
Adaptive Frame / Targeted Frame の分析結果から Markdown レポートを生成する。

人間はソース映像を確認し、各セグメントに OK/PARTIAL/WRONG/UNKNOWN を返すだけでよい。

参照:
  - docs/media_inspector_architecture_v2.md
  - review_reports/ai_observation_report_design_20260627.md

使い方:
  # dry-run
  python3 scripts/generate_ai_observation_report.py \\
    --source-id DOW-UAP-PR059_NAG_UAP_1_Jun_20 \\
    --article-id R02-051 \\
    --adaptive-dir data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20 \\
    --delta-csv data/frame_delta_runs/20260626/DOW-UAP-PR059_NAG_UAP_1_Jun_20/frame_delta.csv \\
    --delta-summary data/frame_delta_runs/20260626/DOW-UAP-PR059_NAG_UAP_1_Jun_20/summary.md \\
    --dry-run

  # execute
  python3 scripts/generate_ai_observation_report.py \\
    --source-id DOW-UAP-PR059_NAG_UAP_1_Jun_20 \\
    --article-id R02-051 \\
    --adaptive-dir data/adaptive_frames/20260627/DOW-UAP-PR059_NAG_UAP_1_Jun_20 \\
    --delta-csv data/frame_delta_runs/20260626/DOW-UAP-PR059_NAG_UAP_1_Jun_20/frame_delta.csv \\
    --delta-summary data/frame_delta_runs/20260626/DOW-UAP-PR059_NAG_UAP_1_Jun_20/summary.md \\
    --execute

安全制約:
  - note_drafts/ は変更しない
  - thumbnails/ は変更しない
  - workflow.db / source_registry.csv は変更しない
  - git 操作は行わない
  - 外部 API は使用しない
"""

import argparse
import csv
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


# ─────────────────────────────────────────────────────────────
# タイムコード表記ヘルパー
# ─────────────────────────────────────────────────────────────

def fmt_tc(seconds: float) -> str:
    """秒数を 'Xs（mm:ss）' 形式に変換する。"""
    s = int(round(seconds))
    mm = s // 60
    ss = s % 60
    return f"{s}s（{mm:02d}:{ss:02d}）"


def fmt_tc_range(start_s: float, end_s: float) -> str:
    """秒数範囲を 'Xs（mm:ss）〜Xs（mm:ss）' 形式に変換する。"""
    return f"{fmt_tc(start_s)}〜{fmt_tc(end_s)}"


# ─────────────────────────────────────────────────────────────
# 動画デュレーション取得
# ─────────────────────────────────────────────────────────────

def get_video_duration(video_path: str | None, fallback_s: float) -> float:
    """ffprobe で動画尺を取得する。失敗時は fallback_s を返す。"""
    if not video_path or not Path(video_path).exists():
        return fallback_s
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", video_path],
            capture_output=True, text=True, timeout=15
        )
        val = result.stdout.strip()
        if val:
            return float(val)
    except Exception:
        pass
    return fallback_s


# ─────────────────────────────────────────────────────────────
# Delta CSV 読み込み
# ─────────────────────────────────────────────────────────────

def load_delta_csv(csv_path: str) -> list[dict]:
    """Delta CSV を読み込み、数値フィールドをキャストしたリストを返す。"""
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({
                "pair_id":           int(row["pair_id"]),
                "frame_prev":        row["frame_prev"],
                "frame_curr":        row["frame_curr"],
                "ts_prev":           float(row["timestamp_prev_s"]),
                "ts_curr":           float(row["timestamp_curr_s"]),
                "mean_diff":         float(row["mean_diff"]),
                "std_diff":          float(row["std_diff"]),
                "max_diff":          int(row["max_diff"] or 0),
                "bc_prev":           int(row["bright_count_prev"] or 0),
                "bc_curr":           int(row["bright_count_curr"] or 0),
                "pos_delta":         float(row["position_delta_px"]) if row["position_delta_px"] else None,
                "event_type":        row["event_type"],
            })
    return rows


# ─────────────────────────────────────────────────────────────
# セグメントのイベント優先度スコア
# ─────────────────────────────────────────────────────────────

def row_priority(row: dict) -> int:
    """行のイベント重要度スコアを返す（セグメント分割に使用）。"""
    et  = row["event_type"]
    bc  = max(row["bc_prev"], row["bc_curr"])
    md  = row["mean_diff"]
    pos = row["pos_delta"] or 0

    if et == "APPEAR":
        if bc >= 5000:  return 12
        if bc >= 1000:  return 9
        if bc >= 500:   return 6
        return 3
    if et == "DISAPPEAR":
        bc_val = row["bc_prev"]  # DISAPPEARは消失前の輝度が重要
        if bc_val >= 5000:  return 12
        if bc_val >= 1000:  return 9
        if bc_val >= 500:   return 6
        return 3
    if et == "CUT":
        if md >= 50:  return 10
        if md >= 30:  return 7
        return 4
    if et == "OBJECT_MOVE" and pos >= 500:
        return 7
    if et == "OBJECT_MOVE" and pos >= 300:
        return 5
    if et == "REVIEW_REQUIRED":
        return 3
    if et == "STATIC":
        return 1
    return 0


# ─────────────────────────────────────────────────────────────
# セグメントクラスタリング
# ─────────────────────────────────────────────────────────────

def cluster_events_to_segments(
    rows: list[dict],
    max_segments: int = 8,
    duration: float = 0.0,
    cluster_window: float = 30.0,
    seg_buffer: float = 3.0,
    min_static_run: int = 10,
) -> list[dict]:
    """
    Delta イベントをセグメントにクラスタリングする。

    1. 重要イベント（priority >= 4）をアンカーとして収集
    2. 時系列でグルーピング（cluster_window 以内なら同一セグメント）
    3. 長期 STATIC 区間を別セグメントとして追加
    4. セグメント数が max_segments を超えたら低優先度セグメントを隣接と合併
    """
    # 1. アンカーイベントの収集
    anchor_events: list[dict] = []
    for row in rows:
        if row_priority(row) >= 4:
            anchor_events.append(row)

    # 2. 時系列グルーピング
    segments: list[dict] = []
    for row in sorted(anchor_events, key=lambda r: r["ts_prev"]):
        start = max(0.0, row["ts_prev"] - seg_buffer)
        end   = row["ts_curr"] + seg_buffer

        if segments and start <= segments[-1]["end_s"] + cluster_window:
            # 既存セグメントを拡張
            segments[-1]["end_s"]   = max(segments[-1]["end_s"], end)
            segments[-1]["max_pri"] = max(segments[-1]["max_pri"], row_priority(row))
        else:
            segments.append({
                "start_s":  start,
                "end_s":    end,
                "max_pri":  row_priority(row),
            })

    # 3. 長期 STATIC 区間の検出・追加
    static_zones = _find_static_zones(rows, min_run=min_static_run)
    for zone in static_zones:
        # 既存セグメントと重複しない独立した STATIC 区間のみ追加
        overlaps = any(
            not (zone["end_s"] <= seg["start_s"] or zone["start_s"] >= seg["end_s"])
            for seg in segments
        )
        if not overlaps:
            zone["max_pri"] = 2
            segments.append(zone)

    # 4. セグメント間の大きなギャップ（≥30s）を補完セグメントで埋める
    segments.sort(key=lambda s: s["start_s"])
    segments = _fill_coverage_gaps(segments, rows, duration, min_gap=30.0)

    # 4.5 最大長（90s）を超えるセグメントを分割する
    segments = _split_oversized_segments(segments, rows, max_duration=90.0)

    # 5. 各セグメントに含まれるイベント行を付与
    segments.sort(key=lambda s: s["start_s"])
    for seg in segments:
        seg["end_s"] = min(seg["end_s"], duration + 3.0) if duration > 0 else seg["end_s"]
        seg["events"] = [
            r for r in rows
            if r["ts_curr"] > seg["start_s"] and r["ts_prev"] < seg["end_s"]
        ]

    # 6. max_segments 超過時は隣接する低優先度セグメントを合併
    while len(segments) > max_segments:
        best_merge_idx = _find_merge_candidate(segments)
        if best_merge_idx is None:
            break
        a = segments[best_merge_idx]
        b = segments[best_merge_idx + 1]
        merged = {
            "start_s":  a["start_s"],
            "end_s":    b["end_s"],
            "max_pri":  max(a["max_pri"], b["max_pri"]),
            "events":   a["events"] + b["events"],
        }
        segments = segments[:best_merge_idx] + [merged] + segments[best_merge_idx + 2:]

    # 6. セグメントIDを付与
    seg_labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, seg in enumerate(segments):
        seg["id"] = seg_labels[i] if i < len(seg_labels) else str(i + 1)

    return segments


def _find_static_zones(rows: list[dict], min_run: int = 10) -> list[dict]:
    """STATIC が min_run ペア以上連続する区間を返す。"""
    zones = []
    run_start = None
    run_len   = 0
    for row in rows:
        if row["event_type"] == "STATIC":
            if run_start is None:
                run_start = row["ts_prev"]
            run_len += 1
        else:
            if run_len >= min_run:
                zones.append({"start_s": run_start, "end_s": row["ts_prev"],
                               "events": [], "static_count": run_len})
            run_start = None
            run_len   = 0
    if run_len >= min_run:
        zones.append({"start_s": run_start, "end_s": rows[-1]["ts_curr"],
                      "events": [], "static_count": run_len})
    return zones


def _split_oversized_segments(
    segments: list[dict],
    all_rows: list[dict],
    max_duration: float = 90.0,
) -> list[dict]:
    """
    max_duration 秒を超えるセグメントをアンカーイベントの最大ギャップ点で2分割する。
    再帰的には処理しない（1回のみ分割する）。
    """
    result: list[dict] = []
    for seg in segments:
        dur = seg["end_s"] - seg["start_s"]
        if dur <= max_duration:
            result.append(seg)
            continue

        # セグメント内のイベントをall_rowsから取得（events未付与の場合に対応）
        seg_events = seg.get("events") or [
            r for r in all_rows
            if r["ts_curr"] > seg["start_s"] and r["ts_prev"] < seg["end_s"]
        ]

        # アンカーイベントをts_currでソート
        anchors = sorted(
            [e for e in seg_events if row_priority(e) >= 4],
            key=lambda e: e["ts_curr"],
        )

        # セグメント中央 80% 内でアンカー間の最大ギャップを探す
        guard_lo = seg["start_s"] + dur * 0.10
        guard_hi = seg["end_s"]   - dur * 0.10
        best_split = None
        best_gap   = 14.0  # 最低15秒以上のギャップがなければ分割しない

        for i in range(len(anchors) - 1):
            curr_end = anchors[i]["ts_curr"]
            next_beg = anchors[i + 1]["ts_prev"]
            gap      = next_beg - curr_end
            if gap > best_gap and guard_lo <= curr_end <= guard_hi:
                best_gap   = gap
                best_split = (curr_end + next_beg) / 2

        # ギャップが見つからない場合はセグメント中央で分割
        if best_split is None:
            best_split = (seg["start_s"] + seg["end_s"]) / 2

        first = {
            "start_s": seg["start_s"],
            "end_s":   best_split,
            "max_pri": seg["max_pri"],
        }
        second = {
            "start_s": best_split,
            "end_s":   seg["end_s"],
            "max_pri": seg["max_pri"],
        }
        result.extend([first, second])

    return result


def _fill_coverage_gaps(
    segments: list[dict],
    all_rows: list[dict],
    duration: float,
    min_gap: float = 30.0,
) -> list[dict]:
    """
    セグメント間に min_gap 秒以上のギャップがある場合、
    そのギャップをカバーするコンテキストセグメントを補完する。
    """
    if not segments:
        return segments

    result: list[dict] = [segments[0]]

    for seg in segments[1:]:
        prev_end  = result[-1]["end_s"]
        gap_start = prev_end
        gap_end   = seg["start_s"]
        gap       = gap_end - gap_start

        if gap >= min_gap:
            gap_events = [
                r for r in all_rows
                if r["ts_curr"] > gap_start and r["ts_prev"] < gap_end
            ]
            gap_pri = max((row_priority(r) for r in gap_events), default=1)
            result.append({
                "start_s": gap_start,
                "end_s":   gap_end,
                "max_pri": gap_pri,
                "events":  gap_events,
            })

        result.append(seg)

    return result


def _find_merge_candidate(segments: list[dict]) -> int | None:
    """隣接する 2 セグメントの中から合併コスト最小のインデックスを返す。"""
    if len(segments) < 2:
        return None
    # 隣接ペアの「合計優先度」が最小のものを合併候補にする
    best_cost = float("inf")
    best_idx  = 0
    for i in range(len(segments) - 1):
        cost = segments[i]["max_pri"] + segments[i + 1]["max_pri"]
        if cost < best_cost:
            best_cost = cost
            best_idx  = i
    return best_idx


# ─────────────────────────────────────────────────────────────
# セグメント分類タグ
# ─────────────────────────────────────────────────────────────

def segment_tag(seg: dict) -> str:
    """セグメントの主要イベントタイプからタグ文字列を生成する。"""
    events = seg["events"]
    types  = [e["event_type"] for e in events]
    cnt    = {t: types.count(t) for t in set(types)}

    tags = []
    if cnt.get("APPEAR", 0):
        bc_max = max(e["bc_curr"] for e in events if e["event_type"] == "APPEAR")
        tags.append(f"APPEAR（bc_max={bc_max:,}）")
    if cnt.get("DISAPPEAR", 0):
        tags.append(f"DISAPPEAR×{cnt['DISAPPEAR']}")
    if cnt.get("CUT", 0):
        md_max = max(e["mean_diff"] for e in events if e["event_type"] == "CUT")
        tags.append(f"CUT×{cnt['CUT']}（max_diff={md_max:.1f}）")
    if cnt.get("OBJECT_MOVE", 0):
        tags.append(f"OBJECT_MOVE×{cnt['OBJECT_MOVE']}")
    if cnt.get("REVIEW_REQUIRED", 0):
        tags.append(f"REVIEW_REQUIRED×{cnt['REVIEW_REQUIRED']}")
    if cnt.get("STATIC", 0) and cnt.get("STATIC", 0) >= 5:
        tags.append(f"STATIC×{cnt['STATIC']}（低変化区間）")
    return " / ".join(tags) if tags else "（イベント少）"


# ─────────────────────────────────────────────────────────────
# AI 観察文生成
# ─────────────────────────────────────────────────────────────

def generate_observation(seg: dict) -> str:
    """セグメントの Delta イベントから日本語観察文を生成する。"""
    events = seg["events"]
    appears  = [e for e in events if e["event_type"] == "APPEAR"]
    disaps   = [e for e in events if e["event_type"] == "DISAPPEAR"]
    cuts     = [e for e in events if e["event_type"] == "CUT"]
    omoves   = [e for e in events if e["event_type"] == "OBJECT_MOVE"]
    reviews  = [e for e in events if e["event_type"] == "REVIEW_REQUIRED"]
    statics  = [e for e in events if e["event_type"] == "STATIC"]

    lines: list[str] = []

    # ─ STATIC 支配区間 ─
    if len(statics) >= 5 and len(statics) >= len(appears) + len(disaps) + len(cuts):
        n = len(statics)
        dur = seg["end_s"] - seg["start_s"]
        lines.append(
            f"この区間（約{int(dur)}秒間）はDelta変化量が少ない状態が続いた（STATIC×{n}件）。"
        )
        lines.append(
            "映像が静止しているか、対象物が画面内で極めてゆっくり移動している可能性がある。"
        )
        lines.append("区間内の実際の内容はソース映像の確認まで不明。")
        return "\n".join(lines)

    # ─ CUT 支配区間 ─
    if cuts and len(cuts) >= 2:
        md_list = [f"{e['mean_diff']:.1f}" for e in sorted(cuts, key=lambda e: e["ts_curr"])[:3]]
        ts_first = fmt_tc(cuts[0]["ts_curr"])
        ts_last  = fmt_tc(cuts[-1]["ts_curr"])
        lines.append(
            f"この区間で{len(cuts)}回のシーン急変（CUT）を検出した"
            f"（{ts_first}〜{ts_last}、mean_diff: {', '.join(md_list)}）。"
        )
        lines.append(
            "レンズの切り替え（FOV変更）または映像の編集点の可能性がある。"
        )
        for d in disaps:
            if int(d["bc_curr"]) == 0:
                d_ts  = fmt_tc(d["ts_curr"])
                c_ts  = [c for c in cuts if c["ts_prev"] <= d["ts_curr"] + 9]
                if c_ts:
                    lines.append(
                        f"{d_ts}付近で輝度の完全消失（bc→0）を検出しており、"
                        "対象物がフレームアウトした直後にレンズが切り替わった可能性がある。"
                    )
                    break
        for a in appears:
            bc  = a["bc_curr"]
            ts  = fmt_tc(a["ts_curr"])
            lines.append(
                f"{ts}付近で輝点の再出現（bc={bc:,}）を検出した。"
            )
        return "\n".join(lines)

    # ─ APPEAR / DISAPPEAR 支配区間 ─
    if appears or disaps:
        for a in sorted(appears, key=lambda e: e["ts_curr"]):
            bc   = a["bc_curr"]
            t0   = fmt_tc(a["ts_prev"])
            t1   = fmt_tc(a["ts_curr"])
            if bc >= 5000:
                lines.append(
                    f"{t0}→{t1}で非常に強い輝点（bc={bc:,}）の出現をDelta分析が検出した。"
                )
            elif bc >= 1000:
                lines.append(
                    f"{t0}→{t1}で輝点（bc={bc:,}）の出現を検出した。"
                )
            else:
                lines.append(
                    f"{t0}→{t1}で中程度の輝点（bc={bc:,}）の出現を検出した。"
                )

        for d in sorted(disaps, key=lambda e: e["ts_curr"]):
            bp  = d["bc_prev"]
            bc  = d["bc_curr"]
            t0  = fmt_tc(d["ts_prev"])
            t1  = fmt_tc(d["ts_curr"])
            if bp >= 1000 and bc == 0:
                lines.append(
                    f"{t0}→{t1}で輝点の完全消失（bc: {bp:,}→0）を検出した。"
                )
            elif bp >= 500:
                lines.append(
                    f"{t0}→{t1}で輝点の急激な減少（bc: {bp:,}→{bc:,}）を検出した。"
                )
            else:
                lines.append(
                    f"{t0}→{t1}で輝点の消失を検出した（bc: {bp:,}→{bc:,}）。"
                )

        if len(appears) >= 2 or (appears and disaps):
            lines.append(
                "APPEAR と DISAPPEAR が短時間に複数回発生しており、"
                "センサーの露出変化（ホワイトアウト・露出補正）による誤検出の可能性がある。"
                "ソース映像での確認を推奨する。"
            )
        return "\n".join(lines)

    # ─ 単体 CUT ─
    if len(cuts) == 1:
        c   = cuts[0]
        ts  = fmt_tc(c["ts_curr"])
        lines.append(
            f"{ts}付近でシーン急変（CUT、mean_diff={c['mean_diff']:.1f}）を1件検出した。"
        )
        lines.append("レンズ切り替えまたは映像編集点の可能性がある。")
        return "\n".join(lines)

    # ─ 高速移動 OBJECT_MOVE ─
    if omoves:
        high = [e for e in omoves if (e["pos_delta"] or 0) >= 400]
        avg_bc = (
            sum(e["bc_curr"] for e in omoves) / len(omoves)
            if omoves else 0
        )
        if high:
            max_delta = max(e["pos_delta"] or 0 for e in high)
            ts_h = fmt_tc(high[0]["ts_curr"])
            lines.append(
                f"この区間で対象物の大きな移動（最大{max_delta:.0f}px、{ts_h}付近）をDelta分析が検出した。"
            )
        else:
            lines.append(
                f"この区間で対象物の移動（OBJECT_MOVE×{len(omoves)}件）を継続的に検出した。"
            )
        if avg_bc > 500:
            lines.append(
                f"輝点が継続して検出されており（平均bc≈{avg_bc:.0f}）、"
                "対象物が映像内に存在し続けている可能性が高い。"
            )
        return "\n".join(lines)

    # ─ REVIEW_REQUIRED 支配区間 ─
    if reviews:
        n = len(reviews)
        ts_range = fmt_tc_range(reviews[0]["ts_prev"], reviews[-1]["ts_curr"])
        lines.append(
            f"この区間（{ts_range}）でアルゴリズムが「REVIEW_REQUIRED」を{n}回判定した。"
        )
        lines.append(
            "mean_diff は低値だが輝点位置の変化が検出されており、対象物の挙動を自動判定できない。"
        )
        lines.append("ソース映像の直接確認を推奨する。")
        return "\n".join(lines)

    return "この区間の観察内容は機械的に特定できなかった。ソース映像の確認が必要。"


# ─────────────────────────────────────────────────────────────
# 確信度判定
# ─────────────────────────────────────────────────────────────

def determine_confidence(seg: dict) -> tuple[str, str]:
    """(confidence, reason) を返す。"""
    events  = seg["events"]
    appears = [e for e in events if e["event_type"] == "APPEAR"]
    disaps  = [e for e in events if e["event_type"] == "DISAPPEAR"]
    cuts    = [e for e in events if e["event_type"] == "CUT"]
    reviews = [e for e in events if e["event_type"] == "REVIEW_REQUIRED"]
    statics = [e for e in events if e["event_type"] == "STATIC"]

    high_bc_appear  = any(e["bc_curr"] >= 1000 for e in appears)
    high_bc_disap   = any(e["bc_prev"] >= 1000 for e in disaps)

    if high_bc_appear or high_bc_disap:
        return "medium", "Delta分析で高bc値のAPPEAR/DISAPPEARを検出。ソース映像確認後に high に昇格可能"

    if cuts:
        md_max = max(e["mean_diff"] for e in cuts)
        if md_max >= 50:
            return "medium", f"CUTのmean_diff={md_max:.1f}（高値）→シーン変化は確実。内容の解釈は要確認"
        return "low", f"CUTのmean_diff={md_max:.1f}（中値）→シーン変化あり。意味の解釈は不確実"

    if len(statics) >= 10:
        return "medium", f"STATIC×{len(statics)}件→変化が少ない状態は確実。内容は不明"

    if reviews:
        return "low", f"REVIEW_REQUIRED×{len(reviews)}件→自動判定困難。ソース映像確認が必要"

    return "unknown", "根拠が不十分。ソース映像確認が必要"


# ─────────────────────────────────────────────────────────────
# リスクフラグ検出
# ─────────────────────────────────────────────────────────────

def detect_risks(seg: dict, all_rows: list[dict]) -> dict[str, tuple[str, str]]:
    """リスクフラグ辞書 {flag: (level, reason)} を返す。"""
    events  = seg["events"]
    appears = [e for e in events if e["event_type"] == "APPEAR"]
    disaps  = [e for e in events if e["event_type"] == "DISAPPEAR"]
    cuts    = [e for e in events if e["event_type"] == "CUT"]
    statics = [e for e in events if e["event_type"] == "STATIC"]

    flags: dict[str, tuple[str, str]] = {
        "ui_misidentification":      ("none", ""),
        "trimming_effect":           ("none", ""),
        "blowup_effect":             ("none", ""),
        "speed_change":              ("none", ""),
        "frameout_misidentification":("none", ""),
        "exposure_change":           ("none", ""),
        "compression_artifact":      ("none", ""),
    }

    # exposure_change: CUT 近傍（±9s）に APPEAR/DISAPPEAR が発生
    for c in cuts:
        c_ts = c["ts_curr"]
        nearby = [e for e in appears + disaps
                  if abs(e["ts_curr"] - c_ts) <= 9]
        if nearby:
            flags["exposure_change"] = (
                "high",
                f"CUT（{fmt_tc(c_ts)}付近）の前後にAPPEAR/DISAPPEARが発生→露出変化の可能性"
            )
            break

    # APPEAR の bc 急騰が CUT なしの場合は medium
    if flags["exposure_change"][0] == "none":
        high_appears = [e for e in appears if e["bc_curr"] >= 3000 and e["bc_prev"] == 0]
        if high_appears and not cuts:
            a = high_appears[0]
            flags["exposure_change"] = (
                "medium",
                f"{fmt_tc(a['ts_curr'])}でbc=0→{a['bc_curr']:,}の急騰→ホワイトアウトの可能性"
            )

    # frameout_misidentification: bc→0 の DISAPPEAR があり CUT が前後 9s 以内
    for d in disaps:
        if d["bc_curr"] == 0:
            d_ts = d["ts_curr"]
            nearby_cut = [r for r in all_rows
                          if r["event_type"] == "CUT"
                          and abs(r["ts_prev"] - d_ts) <= 9]
            if nearby_cut:
                flags["frameout_misidentification"] = (
                    "high",
                    f"{fmt_tc(d_ts)}付近のDISAPPEAR（bc→0）直後にCUT→フレームアウトかレンズ切替か不明"
                )
            else:
                cur = flags["frameout_misidentification"]
                if cur[0] == "none":
                    flags["frameout_misidentification"] = (
                        "medium",
                        f"{fmt_tc(d_ts)}のDISAPPEAR（bc→0）→フレームアウトと露出消失の区別困難"
                    )

    # trimming_effect: CUT が複数
    if len(cuts) >= 2:
        flags["trimming_effect"] = (
            "medium",
            f"{len(cuts)}回のCUT→レンズ切り替えまたはトリミング変化の可能性"
        )
    elif len(cuts) == 1:
        flags["trimming_effect"] = (
            "low",
            "CUT 1件→単発のレンズ切り替えの可能性"
        )

    # blowup_effect: 長期 STATIC 区間
    if len(statics) >= 8:
        flags["blowup_effect"] = (
            "low",
            f"STATIC×{len(statics)}件の長期区間→ブローアップによる解像度低下の可能性"
        )

    return flags


# ─────────────────────────────────────────────────────────────
# 根拠テキスト生成
# ─────────────────────────────────────────────────────────────

def generate_basis(
    seg: dict,
    adaptive_dir: str,
    targeted_dir: str | None,
    delta_summary_path: str,
) -> str:
    """根拠フィールドのリスト形式テキストを生成する。"""
    events  = seg["events"]
    appears = [e for e in events if e["event_type"] == "APPEAR"]
    disaps  = [e for e in events if e["event_type"] == "DISAPPEAR"]
    cuts    = [e for e in events if e["event_type"] == "CUT"]
    omoves  = [e for e in events if e["event_type"] == "OBJECT_MOVE"]
    statics = [e for e in events if e["event_type"] == "STATIC"]

    lines: list[str] = []

    # Adaptive frame
    adp_frames = _list_adaptive_frames_in_range(adaptive_dir, seg["start_s"], seg["end_s"])
    if adp_frames:
        sample = adp_frames[:3]
        lines.append(f"- Adaptive frame: {', '.join(sample)} 他 {len(adp_frames)}枚")
    else:
        lines.append("- Adaptive frame: 該当なし")

    # Delta result summary
    delta_parts: list[str] = []
    if appears:
        bc_vals = [f"bc={e['bc_curr']:,}@{fmt_tc(e['ts_curr'])}" for e in appears]
        delta_parts.append(f"APPEAR（{', '.join(bc_vals)}）")
    if disaps:
        bc_vals = [f"bc_prev={e['bc_prev']:,}→{e['bc_curr']:,}@{fmt_tc(e['ts_curr'])}" for e in disaps[:3]]
        delta_parts.append(f"DISAPPEAR（{', '.join(bc_vals)}）")
    if cuts:
        md_vals = [f"mean_diff={e['mean_diff']:.1f}@{fmt_tc(e['ts_curr'])}" for e in cuts[:3]]
        delta_parts.append(f"CUT（{', '.join(md_vals)}）")
    if omoves:
        delta_parts.append(f"OBJECT_MOVE×{len(omoves)}件")
    if statics:
        delta_parts.append(f"STATIC×{len(statics)}件")
    lines.append(f"- Delta result: {'; '.join(delta_parts) if delta_parts else '（なし）'}")

    # Targeted frame
    if targeted_dir:
        tgt_frames = _list_targeted_frames_in_range(targeted_dir, seg["start_s"], seg["end_s"])
        if tgt_frames:
            sample = tgt_frames[:3]
            lines.append(
                f"- Targeted frame: {', '.join(sample)} 他 {len(tgt_frames)}枚 "
                f"（{targeted_dir}/）"
            )
        else:
            lines.append(f"- Targeted frame: {targeted_dir}/ （範囲内フレームなし）")
    else:
        lines.append("- Targeted frame: （--targeted-dir 未指定）")

    lines.append("- VLM output: 未実施")
    lines.append("- Filename metadata: ソースIDのみ参照")

    return "\n".join(lines)


def _list_adaptive_frames_in_range(
    adaptive_dir: str, start_s: float, end_s: float
) -> list[str]:
    """Adaptive フレームの中で time range 内のファイル名リストを返す。"""
    frames: list[str] = []
    if not Path(adaptive_dir).is_dir():
        return frames
    pattern = re.compile(r"^frame_(\d+)\.png$")
    for fname in sorted(os.listdir(adaptive_dir)):
        m = pattern.match(fname)
        if m:
            ts = float(m.group(1))
            if start_s <= ts <= end_s:
                frames.append(fname)
    return frames


def _list_targeted_frames_in_range(
    targeted_dir: str, start_s: float, end_s: float
) -> list[str]:
    """Targeted フレームの中で time range 内のファイル名リストを返す。"""
    frames: list[str] = []
    if not targeted_dir or not Path(targeted_dir).is_dir():
        return frames
    pattern = re.compile(r"^frame_(\d{5})\.png$")
    for fname in sorted(os.listdir(targeted_dir)):
        m = pattern.match(fname)
        if m:
            ts = int(m.group(1))
            if start_s <= ts <= end_s:
                frames.append(fname)
    return frames


# ─────────────────────────────────────────────────────────────
# 代表フレーム候補選定
# ─────────────────────────────────────────────────────────────

def select_representative_frames(
    segments: list[dict],
    adaptive_dir: str,
    targeted_dir: str | None,
) -> list[dict]:
    """
    各セグメントから代表フレーム候補を選定する。
    優先度: 高bc APPEAR > CUT high mean_diff > OBJECT_MOVE high pos_delta > STATIC中央
    """
    candidates: list[dict] = []

    for seg in segments:
        events  = seg["events"]
        appears = sorted(
            [e for e in events if e["event_type"] == "APPEAR" and e["bc_curr"] >= 500],
            key=lambda e: -e["bc_curr"]
        )
        cuts    = sorted(
            [e for e in events if e["event_type"] == "CUT"],
            key=lambda e: -e["mean_diff"]
        )
        omoves  = sorted(
            [e for e in events if e["event_type"] == "OBJECT_MOVE" and (e["pos_delta"] or 0) >= 300],
            key=lambda e: -(e["pos_delta"] or 0)
        )

        if appears:
            e  = appears[0]
            ts = e["ts_curr"]
            candidates.append({
                "segment": seg["id"],
                "frame":   _find_best_frame(ts, adaptive_dir, targeted_dir),
                "ts":      fmt_tc(ts),
                "reason":  f"APPEAR bc={e['bc_curr']:,}（セグメント{seg['id']}で最大輝度）",
                "priority":"高",
            })
        elif cuts:
            e  = cuts[0]
            ts = e["ts_curr"]
            candidates.append({
                "segment": seg["id"],
                "frame":   _find_best_frame(ts, adaptive_dir, targeted_dir),
                "ts":      fmt_tc(ts),
                "reason":  f"CUT mean_diff={e['mean_diff']:.1f}（セグメント{seg['id']}で最大変化）",
                "priority":"中",
            })
        elif omoves:
            e  = omoves[0]
            ts = e["ts_curr"]
            candidates.append({
                "segment": seg["id"],
                "frame":   _find_best_frame(ts, adaptive_dir, targeted_dir),
                "ts":      fmt_tc(ts),
                "reason":  f"OBJECT_MOVE pos_delta={e['pos_delta']:.0f}px",
                "priority":"中",
            })
        else:
            mid_s = (seg["start_s"] + seg["end_s"]) / 2
            candidates.append({
                "segment": seg["id"],
                "frame":   _find_best_frame(mid_s, adaptive_dir, targeted_dir),
                "ts":      fmt_tc(mid_s),
                "reason":  "区間中央フレーム（顕著なイベントなし）",
                "priority":"低",
            })

    return candidates


def _find_best_frame(ts: float, adaptive_dir: str, targeted_dir: str | None) -> str:
    """指定タイムスタンプに最も近いフレームファイル名を返す。"""
    ts_int = int(round(ts))

    # targeted frame が存在すれば優先
    if targeted_dir:
        tgt = Path(targeted_dir) / f"frame_{ts_int:05d}.png"
        if tgt.exists():
            return str(tgt)

    # adaptive frame
    if Path(adaptive_dir).is_dir():
        adp = Path(adaptive_dir) / f"frame_{ts_int:04d}.png"
        if adp.exists():
            return str(adp)
        # 最近傍探索
        pattern = re.compile(r"^frame_(\d+)\.png$")
        best_fname, best_diff = None, float("inf")
        for fname in os.listdir(adaptive_dir):
            m = pattern.match(fname)
            if m:
                diff = abs(int(m.group(1)) - ts_int)
                if diff < best_diff:
                    best_diff = diff
                    best_fname = str(Path(adaptive_dir) / fname)
        if best_fname:
            return best_fname

    return f"（{ts_int}s フレーム未発見）"


# ─────────────────────────────────────────────────────────────
# note_draft 反映候補
# ─────────────────────────────────────────────────────────────

def generate_draft_candidates(segments: list[dict]) -> list[dict]:
    """各セグメントの note_draft 反映候補を生成する（プレースホルダ込み）。"""
    candidates: list[dict] = []
    for seg in segments:
        events  = seg["events"]
        appears = [e for e in events if e["event_type"] == "APPEAR"]
        disaps  = [e for e in events if e["event_type"] == "DISAPPEAR"]
        cuts    = [e for e in events if e["event_type"] == "CUT"]
        omoves  = [e for e in events if e["event_type"] == "OBJECT_MOVE"]
        statics = [e for e in events if e["event_type"] == "STATIC"]

        if appears and max(e["bc_curr"] for e in appears) >= 1000:
            bc_max = max(e["bc_curr"] for e in appears)
            ts = fmt_tc(max(appears, key=lambda e: e["bc_curr"])["ts_curr"])
            draft = f"「{ts}付近で強い輝点（推定bc≈{bc_max:,}）が検出された」"
        elif disaps and any(e["bc_curr"] == 0 for e in disaps):
            d = next(e for e in disaps if e["bc_curr"] == 0)
            ts = fmt_tc(d["ts_curr"])
            draft = f"「{ts}付近で対象物の消失またはフレームアウトが検出された」"
        elif len(cuts) >= 2:
            ts_first = fmt_tc(cuts[0]["ts_curr"])
            draft = f"「{ts_first}前後でレンズ切り替えと思われるシーン変化が{len(cuts)}回検出された」"
        elif omoves:
            high = [m for m in omoves if (m["pos_delta"] or 0) >= 300]
            if high:
                ts  = fmt_tc(high[0]["ts_curr"])
                mpd = max(m["pos_delta"] or 0 for m in high)
                draft = f"「この区間で対象物の継続的な移動を検出（最大{mpd:.0f}px、{ts}付近）」"
            else:
                dur = int(seg["end_s"] - seg["start_s"])
                draft = (
                    f"「この区間（約{dur}秒）で対象物の緩やかな移動を継続検出"
                    f"（OBJECT_MOVE×{len(omoves)}件）」"
                )
        elif len(statics) >= 8:
            draft = f"「この区間（約{int(seg['end_s'] - seg['start_s'])}秒）は対象物の大きな動きなし（STATIC）」"
        else:
            draft = "（人間確認後に記述）"

        conf, _ = determine_confidence(seg)
        candidates.append({
            "segment": seg["id"],
            "draft":   draft,
            "conf":    conf,
        })

    return candidates


# ─────────────────────────────────────────────────────────────
# Markdown レンダリング
# ─────────────────────────────────────────────────────────────

def render_markdown(
    source_id:   str,
    article_id:  str,
    video_path:  str | None,
    duration:    float,
    run_date:    str,
    adaptive_dir: str,
    delta_csv:   str,
    delta_summary: str,
    targeted_dir: str | None,
    segments:    list[dict],
    draft_cands: list[dict],
    rep_frames:  list[dict],
) -> str:
    """AI Observation Report の Markdown 文字列を生成する。"""

    lines: list[str] = []

    # ── ヘッダー ──
    lines += [
        f"# AI Observation Report: {source_id}",
        "",
        "## メタデータ",
        "",
        f"- source_id: {source_id}",
        f"- article_id: {article_id}",
        f"- source_video_path: {video_path or '（--video 未指定）'}",
        f"- duration: {fmt_tc(duration)}",
        f"- run_date: {run_date}",
        f"- 生成スクリプト: scripts/generate_ai_observation_report.py",
        "- pipeline_steps:",
        f"  - adaptive_frames: {adaptive_dir}",
        f"  - delta_analysis: {delta_summary}",
        f"  - targeted_frames: {targeted_dir or '（未指定）'}",
        "  - vlm_output: 未実施",
        "",
        "---",
        "",
        "## 観察サマリー",
        "",
    ]

    # ── 観察サマリー（全セグメントのタグを集約して生成）──
    dominant_events = _summarize_all_events(segments)
    lines += [
        dominant_events,
        "",
        "---",
        "",
        "## 重要セグメント",
        "",
    ]

    # ── セグメント詳細 ──
    for seg in segments:
        start_tc = fmt_tc(seg["start_s"])
        end_tc   = fmt_tc(seg["end_s"])
        seg_id   = seg["id"]
        conf, conf_reason = determine_confidence(seg)
        risks    = detect_risks(seg, [])  # all_rows 参照なし（セグメント内のみ）
        obs      = generate_observation(seg)
        basis    = generate_basis(seg, adaptive_dir, targeted_dir, delta_summary)
        tag      = segment_tag(seg)

        lines += [
            f"### セグメント {seg_id}: {start_tc}〜{end_tc}",
            "",
            f"**概要タグ:** {tag}",
            "",
            "**AI観察:**",
            obs,
            "",
            f"**確信度:** {conf}",
            f"（{conf_reason}）",
            "",
            "**根拠:**",
            basis,
            "",
            "**リスクフラグ:**",
        ]

        for flag, (level, reason) in risks.items():
            reason_str = f"（{reason}）" if reason else ""
            lines.append(f"- {flag}: {level}{reason_str}")

        lines += [
            "",
            "**人間確認:**",
            "- [ ] OK — AIの観察は正しい",
            "- [ ] PARTIAL — 一部修正が必要（以下に記述）",
            "- [ ] WRONG — AIの観察は誤っている（以下に正しい観察を記述）",
            "- [ ] UNKNOWN — 映像からは判断できない",
            "",
            "**人間メモ:**",
            "（確認後にここに記入。PARTIAL/WRONGの場合は差分を記述）",
            "",
            "---",
            "",
        ]

    # ── note_draft 反映候補 ──
    lines += [
        "## note_draft 反映候補",
        "",
        "| セグメント | note_draft 反映案 | 確信度 | 人間確認後に反映 |",
        "|-----------|-----------------|--------|----------------|",
    ]
    for dc in draft_cands:
        lines.append(
            f"| {dc['segment']} | {dc['draft']} | {dc['conf']} | "
            "（人間確認待ち） |"
        )

    lines += [
        "",
        "---",
        "",
        "## 代表フレーム候補",
        "",
        "| セグメント | フレーム | タイムスタンプ | 選定理由 | 優先度 |",
        "|-----------|---------|-------------|---------|--------|",
    ]
    for rf in rep_frames:
        lines.append(
            f"| {rf['segment']} | {rf['frame']} | {rf['ts']} | {rf['reason']} | {rf['priority']} |"
        )

    lines += [
        "",
        "**→ 代表フレーム確定:** （人間確認後に記入）",
        "",
        "---",
        "",
        "## 人間確認フロー",
        "",
        "1. このレポートを通読する",
        "2. QuickTime（または任意のプレイヤー）でソース映像を開く",
        f"   `{video_path or '（ソース映像パスを確認）'}`",
        "3. 各セグメントのタイムコードを参照しながら該当箇所を再生する",
        "4. 各セグメントの「人間確認」欄に OK / PARTIAL / WRONG / UNKNOWN を記入する",
        "5. PARTIAL / WRONG の場合は「人間メモ」欄に差分を記述する",
        "6. 保存して AI に返す（AI が note_draft を修正する）",
        "",
    ]

    return "\n".join(lines)


def _summarize_all_events(segments: list[dict]) -> str:
    """全セグメントを横断した観察サマリー文を生成する。"""
    total_cuts    = sum(len([e for e in s["events"] if e["event_type"] == "CUT"])    for s in segments)
    total_appears = sum(len([e for e in s["events"] if e["event_type"] == "APPEAR"]) for s in segments)
    total_disaps  = sum(len([e for e in s["events"] if e["event_type"] == "DISAPPEAR"]) for s in segments)
    total_omoves  = sum(len([e for e in s["events"] if e["event_type"] == "OBJECT_MOVE"]) for s in segments)
    total_statics = sum(len([e for e in s["events"] if e["event_type"] == "STATIC"]) for s in segments)

    parts: list[str] = []
    if total_appears:
        parts.append(f"APPEAR {total_appears}件")
    if total_disaps:
        parts.append(f"DISAPPEAR {total_disaps}件")
    if total_cuts:
        parts.append(f"CUT {total_cuts}件")
    if total_omoves:
        parts.append(f"OBJECT_MOVE {total_omoves}件")
    if total_statics:
        parts.append(f"STATIC {total_statics}件（低変化区間）")

    event_str = "・".join(parts) if parts else "イベントなし"
    n_seg = len(segments)

    return (
        f"Delta分析全体では {event_str} を検出した。"
        f"映像を {n_seg} セグメントに分割して観察する。"
        "各セグメントの詳細はソース映像の確認で確定する。"
    )


# ─────────────────────────────────────────────────────────────
# メインエントリ
# ─────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI Observation Report 自動生成（Media Inspector v2）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--source-id",      required=True,
                        help="ソースID（例: DOW-UAP-PR059_NAG_UAP_1_Jun_20）")
    parser.add_argument("--article-id",     required=True,
                        help="記事ID（例: R02-051）")
    parser.add_argument("--video",          default=None,
                        help="ソース映像ファイルパス（省略可）")
    parser.add_argument("--adaptive-dir",   required=True,
                        help="Adaptive フレームディレクトリ")
    parser.add_argument("--delta-csv",      required=True,
                        help="Frame Delta CSV ファイルパス")
    parser.add_argument("--delta-summary",  required=True,
                        help="Frame Delta summary.md パス")
    parser.add_argument("--targeted-dir",   default=None,
                        help="Targeted フレームディレクトリ（省略可）")
    parser.add_argument("--output",         default=None,
                        help="出力ファイルパス（省略時は review_reports/<source_id>_ai_observation_report_<date>.md）")
    parser.add_argument("--max-segments",   type=int, default=8,
                        help="最大セグメント数（デフォルト: 8）")
    parser.add_argument("--dry-run",        action="store_true", default=False,
                        help="計画のみ表示・ファイル生成しない（--execute がない場合はデフォルト）")
    parser.add_argument("--execute",        action="store_true", default=False,
                        help="実際にファイルを生成する（明示的指定が必要）")

    args = parser.parse_args()

    # --execute なければ dry-run 強制
    if not args.execute:
        args.dry_run = True

    # 出力先
    run_date = date.today().strftime("%Y%m%d")
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = (
            Path("review_reports") /
            f"{args.source_id}_ai_observation_report_{run_date}.md"
        )

    print("=" * 64)
    print(f"  {'[DRY-RUN]' if args.dry_run else '[EXECUTE]'} generate_ai_observation_report")
    print(f"  source_id    : {args.source_id}")
    print(f"  article_id   : {args.article_id}")
    print(f"  delta_csv    : {args.delta_csv}")
    print(f"  adaptive_dir : {args.adaptive_dir}")
    print(f"  targeted_dir : {args.targeted_dir or '（未指定）'}")
    print(f"  max_segments : {args.max_segments}")
    print(f"  output       : {output_path}")
    print("=" * 64)

    # ── 1. Delta CSV 読み込み ──
    if not Path(args.delta_csv).exists():
        print(f"[ERROR] delta-csv が見つかりません: {args.delta_csv}", file=sys.stderr)
        sys.exit(1)

    rows = load_delta_csv(args.delta_csv)
    print(f"  Delta rows loaded: {len(rows)}")

    # ── 2. 動画尺取得 ──
    fallback_dur = rows[-1]["ts_curr"] if rows else 0.0
    duration = get_video_duration(args.video, fallback_dur)
    print(f"  Duration: {fmt_tc(duration)}")

    # ── 3. セグメント生成 ──
    segments = cluster_events_to_segments(
        rows,
        max_segments=args.max_segments,
        duration=duration,
    )
    print(f"  Segments generated: {len(segments)}")
    for seg in segments:
        n_events = len(seg["events"])
        print(
            f"    [{seg['id']}] {fmt_tc(seg['start_s'])}〜{fmt_tc(seg['end_s'])}"
            f"  ({n_events}events, pri={seg['max_pri']})"
        )

    # ── 4. note_draft 反映候補 ──
    draft_cands = generate_draft_candidates(segments)

    # ── 5. 代表フレーム候補 ──
    rep_frames = select_representative_frames(segments, args.adaptive_dir, args.targeted_dir)

    # ── 6. Markdown 生成 ──
    md = render_markdown(
        source_id     = args.source_id,
        article_id    = args.article_id,
        video_path    = args.video,
        duration      = duration,
        run_date      = run_date,
        adaptive_dir  = args.adaptive_dir,
        delta_csv     = args.delta_csv,
        delta_summary = args.delta_summary,
        targeted_dir  = args.targeted_dir,
        segments      = segments,
        draft_cands   = draft_cands,
        rep_frames    = rep_frames,
    )

    # ── 7. 出力 ──
    if args.dry_run:
        print("\n[DRY-RUN] 生成されるレポートのプレビュー（先頭80行）:")
        print("-" * 64)
        for line in md.splitlines()[:80]:
            print(line)
        print("-" * 64)
        print(f"\n[DRY-RUN] ファイルは生成されていません。--execute を付けて再実行してください。")
        print(f"  出力先（予定）: {output_path}")
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(md, encoding="utf-8")
        print(f"\n[EXECUTE] レポートを生成しました: {output_path}")
        print(f"  文字数: {len(md):,}")
        print(f"  セグメント数: {len(segments)}")


if __name__ == "__main__":
    main()
