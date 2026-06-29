#!/usr/bin/env python3
"""
micro_frame_analyzer.py — Frame-Level Micro Pass (Media Inspector v4)

設計書: docs/media_inspector_v4_architecture.md  §3.5 サンプリング戦略

【役割】
  Precision Sampler (0.25秒) でも取り逃がす瞬間的な映像変化を、
  候補区間だけ全フレーム（30fps）で解析する。

【パイプライン上の位置】
  粗パス (3s)          : Scene Analyzer / Camera Analyzer
  精密パス (0.25s)     : Precision Sampler + Camera Analyzer
  超精密パス (全frames): Micro Frame Analyzer ← このスクリプト

【検出対象イベント】
  BLACKOUT / WHITEOUT / FLASH / BLOOM
  HARD_CUT / FRAME_DROP / SENSOR_SWITCH / FOV_SWITCH / ZOOM_IN / ZOOM_OUT

【利用例】
  # 手動区間指定
  python3 scripts/micro_frame_analyzer.py \\
    --video raw_media/video/DOW-UAP-PR062_....mp4 \\
    --manual-windows "255:257" \\
    --source-id DOW-UAP-PR062_... --article-id R02-054 \\
    --execute

  # Camera Analyzer 出力からトリガー自動検出
  python3 scripts/micro_frame_analyzer.py \\
    --video raw_media/video/DOW-UAP-PR062_....mp4 \\
    --camera-events-csv .../camera_events.csv \\
    --camera-trigger-events EDGE_SURGE,COMBINED \\
    --window 1.0 \\
    --source-id DOW-UAP-PR062_... --article-id R02-054 \\
    --execute

【出力ファイル】
  data/micro_frame_runs/<date>/<source_id>/<start>s_<end>s/
    micro_frame_events.csv     : per-frame メトリクス + 検出イベント
    micro_frame_summary.md     : 人間可読サマリー
    event_candidates.jsonl     : 1行1候補 (MI v4 / OT 前段入力)
    [frames/]                  : --keep-frames 指定時のみ抽出フレーム画像
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile
import shutil
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from pathlib import Path

import numpy as np
from PIL import Image

VERSION = "micro_frame_analyzer_v1"

# ── デフォルト閾値（すべて CLI 引数で上書き可能）────────────────

@dataclass
class Thresholds:
    # BLACKOUT / WHITEOUT
    blackout_thresh:    float = 15.0   # 平均輝度 < この値
    whiteout_thresh:    float = 240.0  # 平均輝度 > この値
    # FLASH: 単フレーム輝度スパイク（前後フレームより +delta 以上）
    flash_delta:        float = 60.0
    # HARD_CUT: フレーム間差分 + 空間周波数変化
    hard_cut_diff:      float = 50.0   # frame_diff_mean > この値
    hard_cut_hf:        float = 2.0    # hf_ratio_vs_prev > この値 または < 1/この値
    # FRAME_DROP: 前フレームとほぼ同一（コマ落ち）
    frame_drop_diff:    float = 1.0    # frame_diff_mean < この値
    # SENSOR_SWITCH: 彩度急変
    sensor_sat_delta:   float = 30.0   # 彩度差 > この値
    # FOV_SWITCH: 空間周波数の急激変化（1フレーム間）
    fov_switch_hf_high: float = 3.0    # hf_ratio_vs_prev > この値
    fov_switch_hf_low:  float = 0.33   # hf_ratio_vs_prev < この値
    # ZOOM_IN / ZOOM_OUT: 移動平均との比較
    zoom_in_hf:         float = 2.0    # curr_hf / rolling_avg > この値
    zoom_out_hf:        float = 0.50   # curr_hf / rolling_avg < この値
    zoom_rolling_n:     int   = 5      # rolling avg のフレーム数
    # BLOOM: 輝度が N フレーム以内でピークを迎える
    bloom_window:       int   = 10     # ピーク検出窓 (フレーム数)
    bloom_ratio:        float = 1.30   # ピーク値 / 周辺平均 > この倍率


CSV_FIELDS = [
    "frame_no", "timestamp_s",
    "brightness_mean", "brightness_max", "brightness_min",
    "edge_density", "hf_ratio_self", "hf_ratio_vs_prev",
    "color_saturation",
    "frame_diff_mean", "frame_diff_max",
    "blackout_flag", "whiteout_flag",
    "micro_event", "event_confidence", "event_notes",
]

JSONL_FIELDS = [
    "timestamp_s", "event", "confidence", "frame_no",
    "brightness_mean", "frame_diff_mean", "hf_ratio_vs_prev",
    "color_saturation", "notes",
]


# ── ffmpeg / ffprobe ─────────────────────────────────────────────

def get_video_fps(video_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "quiet",
        "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    raw = result.stdout.strip()
    if "/" in raw:
        n, d = raw.split("/")
        return float(n) / float(d)
    try:
        return float(raw)
    except ValueError:
        return 30.0


def get_video_duration(video_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 9999.0


def extract_micro_frames(
    video_path: Path,
    start: float,
    end: float,
    out_dir: Path,
    fps: float,
) -> list:
    """
    [start, end] 区間を元の fps で全フレーム抽出。
    Returns list of (Path, timestamp_s) sorted by timestamp.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    duration = end - start
    cmd = [
        "ffmpeg",
        "-ss", f"{start:.3f}",
        "-t",  f"{duration:.3f}",
        "-i",  str(video_path),
        "-vsync", "0",
        "-q:v", "2",
        "-y",
        str(out_dir / "frame_%05d.png"),
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"  [WARN] ffmpeg 失敗: {result.stderr.decode()[-200:]}", file=sys.stderr)

    paths = sorted(out_dir.glob("frame_*.png"))
    # timestamp 計算: start + (idx/fps)
    entries = []
    for i, p in enumerate(paths):
        ts = round(start + i / fps, 4)
        entries.append((p, ts))
    return entries


# ── 画像メトリクス ───────────────────────────────────────────────

def spatial_freq_ratio(gray: np.ndarray) -> float:
    """
    画像の空間周波数比（高周波成分の割合）。
    camera_analyzer.py と同一実装。
    """
    h, w = gray.shape
    total = np.sum(np.abs(np.fft.rfft2(gray.astype(float))))
    if total < 1.0:
        return 0.0
    col_hf = np.array([
        np.sum(np.abs(np.fft.rfft(gray[:, c].astype(float))[h // 4:]))
        for c in range(0, w, 4)
    ])
    row_hf = np.array([
        np.sum(np.abs(np.fft.rfft(gray[r, :].astype(float))[w // 4:]))
        for r in range(0, h, 4)
    ])
    return float((col_hf.sum() + row_hf.sum()) / (2.0 * total))


def compute_color_saturation(arr: np.ndarray) -> float:
    """RGB → HSV 変換なし簡易彩度: (max - min) / max の平均 × 100"""
    r = arr[:, :, 0].astype(float)
    g = arr[:, :, 1].astype(float)
    b = arr[:, :, 2].astype(float)
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    with np.errstate(invalid="ignore", divide="ignore"):
        sat = np.where(maxc > 0, (maxc - minc) / maxc, 0.0)
    return float(np.nan_to_num(sat).mean() * 100.0)


def compute_edge_density(gray: np.ndarray) -> float:
    """Sobel 近似による正規化エッジ密度 (0〜1)"""
    gy = np.diff(gray.astype(float), axis=0)
    gx = np.diff(gray.astype(float), axis=1)
    h = min(gy.shape[0], gx.shape[0])
    w = min(gy.shape[1], gx.shape[1])
    mag = np.sqrt(gy[:h, :w] ** 2 + gx[:h, :w] ** 2)
    return float(mag.mean() / 255.0)


def analyze_single_frame(path: Path) -> dict:
    """1 フレームの全メトリクスを計算（前フレームとの比較なし）"""
    img = Image.open(path).convert("RGB")
    arr = np.array(img)
    gray = arr.mean(axis=2)

    hf = spatial_freq_ratio(gray)
    ed = compute_edge_density(gray)
    sat = compute_color_saturation(arr)
    bm = float(gray.mean())

    return {
        "arr":              arr,
        "gray":             gray,
        "hf_ratio_self":    round(hf, 4),
        "edge_density":     round(ed, 4),
        "brightness_mean":  round(bm, 2),
        "brightness_max":   float(gray.max()),
        "brightness_min":   float(gray.min()),
        "color_saturation": round(sat, 2),
        "blackout_flag":    bm < 15.0,   # 後で閾値で上書き
        "whiteout_flag":    bm > 240.0,
    }


# ── 全フレーム解析 ───────────────────────────────────────────────

def analyze_all_frames(
    frame_entries: list,
    thresholds: Thresholds,
    verbose: bool = False,
) -> list:
    """
    全フレームのメトリクスを計算してリストで返す。
    Returns: [{"frame_no", "timestamp_s", "brightness_mean", ..., "hf_ratio_vs_prev", ...}]
    """
    results = []
    prev = None

    for idx, (path, ts) in enumerate(frame_entries):
        m = analyze_single_frame(path)

        # 閾値適用（CLI 引数で変更可能なため）
        m["blackout_flag"] = m["brightness_mean"] < thresholds.blackout_thresh
        m["whiteout_flag"] = m["brightness_mean"] > thresholds.whiteout_thresh

        # 前フレームとの差分
        if prev is not None:
            diff = np.abs(m["arr"].astype(float) - prev["arr"].astype(float)).mean(axis=2)
            diff_mean = float(diff.mean())
            diff_max  = float(diff.max())

            prev_hf = prev["hf_ratio_self"]
            curr_hf = m["hf_ratio_self"]
            if prev_hf >= 0.010 and curr_hf >= 0.010:
                hf_vs_prev = round(curr_hf / prev_hf, 4)
            else:
                hf_vs_prev = 0.0
        else:
            diff_mean  = 0.0
            diff_max   = 0.0
            hf_vs_prev = 0.0

        row = {
            "frame_no":         idx + 1,
            "timestamp_s":      ts,
            "brightness_mean":  m["brightness_mean"],
            "brightness_max":   m["brightness_max"],
            "brightness_min":   m["brightness_min"],
            "edge_density":     m["edge_density"],
            "hf_ratio_self":    m["hf_ratio_self"],
            "hf_ratio_vs_prev": hf_vs_prev,
            "color_saturation": m["color_saturation"],
            "frame_diff_mean":  round(diff_mean, 3),
            "frame_diff_max":   round(diff_max, 1),
            "blackout_flag":    m["blackout_flag"],
            "whiteout_flag":    m["whiteout_flag"],
            # 内部用（イベント検出に使う）
            "_arr":             m["arr"],
            "_hf_self":         m["hf_ratio_self"],
        }
        results.append(row)
        prev = m

        if verbose and (idx % 10 == 0 or m["blackout_flag"] or m["whiteout_flag"]):
            bo = "BO" if m["blackout_flag"] else "  "
            wo = "WO" if m["whiteout_flag"] else "  "
            print(
                f"  f{idx+1:04d} {ts:.3f}s"
                f"  br={m['brightness_mean']:5.1f}"
                f"  ed={m['edge_density']:.4f}"
                f"  hf={m['hf_ratio_self']:.4f}"
                f"  diff={diff_mean:5.1f}"
                f"  {bo}{wo}"
            )

    return results


# ── イベント検出 ─────────────────────────────────────────────────

def detect_events(frames: list, thresholds: Thresholds) -> list:
    """
    フレームメトリクスのリストからイベント候補を検出。
    Returns: list of event-candidate dicts (JSONL 形式)
    """
    n = len(frames)
    events = []

    def _emit(frame_idx: int, event: str, confidence: float, notes: str, extra: dict = None):
        m = frames[frame_idx]
        ev = {
            "timestamp_s":      m["timestamp_s"],
            "event":            event,
            "confidence":       round(confidence, 3),
            "frame_no":         m["frame_no"],
            "brightness_mean":  m["brightness_mean"],
            "frame_diff_mean":  m["frame_diff_mean"],
            "hf_ratio_vs_prev": m["hf_ratio_vs_prev"],
            "color_saturation": m["color_saturation"],
            "notes":            notes,
        }
        if extra:
            ev.update(extra)
        events.append(ev)

    # rolling avg of hf_ratio_self
    hf_self = [f["_hf_self"] for f in frames]

    for i, m in enumerate(frames):
        ts = m["timestamp_s"]
        bm = m["brightness_mean"]
        ed = m["edge_density"]
        hf_vs = m["hf_ratio_vs_prev"]
        diff_m = m["frame_diff_mean"]
        sat = m["color_saturation"]

        # ① BLACKOUT
        if m["blackout_flag"]:
            _emit(i, "BLACKOUT", 0.95, f"平均輝度={bm:.1f} (閾値={thresholds.blackout_thresh})")

        # ② WHITEOUT
        elif m["whiteout_flag"]:
            _emit(i, "WHITEOUT", 0.95, f"平均輝度={bm:.1f} (閾値={thresholds.whiteout_thresh})")

        # ③ FLASH: 前後フレームより +flash_delta 以上の単フレームスパイク
        elif 0 < i < n - 1:
            prev_b = frames[i - 1]["brightness_mean"]
            next_b = frames[i + 1]["brightness_mean"]
            delta_prev = bm - prev_b
            delta_next = bm - next_b
            if delta_prev > thresholds.flash_delta and delta_next > thresholds.flash_delta:
                conf = min(0.95, (delta_prev + delta_next) / (thresholds.flash_delta * 4))
                _emit(i, "FLASH", conf,
                      f"輝度スパイク: +{delta_prev:.1f}(前) +{delta_next:.1f}(後)",
                      {"brightness_delta_prev": round(delta_prev, 1),
                       "brightness_delta_next": round(delta_next, 1)})

        # ④ FRAME_DROP: 前フレームとほぼ同一
        if i > 0 and diff_m < thresholds.frame_drop_diff:
            _emit(i, "FRAME_DROP", 0.90,
                  f"フレーム差分={diff_m:.3f} (閾値={thresholds.frame_drop_diff})",
                  {"frame_diff_mean": diff_m})

        # ⑤ HARD_CUT: 大きなフレーム差分 + 空間周波数急変
        if i > 0 and diff_m > thresholds.hard_cut_diff:
            hf_ok = (hf_vs > thresholds.hard_cut_hf or
                     (hf_vs > 0 and hf_vs < 1.0 / thresholds.hard_cut_hf))
            if hf_ok:
                conf = min(0.90, diff_m / 100.0)
                _emit(i, "HARD_CUT", conf,
                      f"差分={diff_m:.1f} hf_ratio={hf_vs:.2f}",
                      {"frame_diff_mean": diff_m, "hf_ratio_vs_prev": hf_vs})

        # ⑥ SENSOR_SWITCH: 彩度急変
        if i > 0:
            prev_sat = frames[i - 1]["color_saturation"]
            sat_delta = abs(sat - prev_sat)
            if sat_delta > thresholds.sensor_sat_delta:
                conf = min(0.75, sat_delta / (thresholds.sensor_sat_delta * 2))
                _emit(i, "SENSOR_SWITCH", conf,
                      f"彩度変化={sat_delta:.1f} ({prev_sat:.1f}→{sat:.1f})",
                      {"sat_delta": round(sat_delta, 1)})

        # ⑦ FOV_SWITCH: 1フレーム間での空間周波数急変
        if i > 0 and hf_vs > 0:
            if hf_vs > thresholds.fov_switch_hf_high:
                _emit(i, "FOV_SWITCH", 0.45,
                      f"hf_ratio急増 ×{hf_vs:.2f} (閾値={thresholds.fov_switch_hf_high})",
                      {"hf_ratio_vs_prev": hf_vs})
            elif hf_vs < thresholds.fov_switch_hf_low:
                _emit(i, "FOV_SWITCH", 0.45,
                      f"hf_ratio急減 ×{hf_vs:.2f} (閾値={thresholds.fov_switch_hf_low})",
                      {"hf_ratio_vs_prev": hf_vs})

        # ⑧ ZOOM_IN / ZOOM_OUT: rolling avg との比較
        roll_n = thresholds.zoom_rolling_n
        if i >= roll_n and hf_vs > 0:
            rolling_avg = float(np.mean([
                frames[j]["_hf_self"] for j in range(i - roll_n, i)
            ]))
            curr_hf_self = m["_hf_self"]
            if rolling_avg > 0.010:
                ratio_vs_avg = curr_hf_self / rolling_avg
                if ratio_vs_avg > thresholds.zoom_in_hf:
                    _emit(i, "ZOOM_IN", 0.45,
                          f"hf_self/rolling_avg={ratio_vs_avg:.2f} (avg={rolling_avg:.4f})",
                          {"hf_ratio_vs_rolling": round(ratio_vs_avg, 3)})
                elif ratio_vs_avg < thresholds.zoom_out_hf:
                    _emit(i, "ZOOM_OUT", 0.45,
                          f"hf_self/rolling_avg={ratio_vs_avg:.2f} (avg={rolling_avg:.4f})",
                          {"hf_ratio_vs_rolling": round(ratio_vs_avg, 3)})

        # ⑨ BLOOM: 輝度が局所ピークを迎える（前後 bloom_window フレームで最大）
        bw = thresholds.bloom_window
        if bw <= i < n - bw:
            window_b = [frames[j]["brightness_mean"] for j in range(i - bw, i + bw + 1)]
            peak_val = window_b[bw]  # 現在フレーム
            surround = [window_b[j] for j in range(len(window_b)) if j != bw]
            surround_avg = float(np.mean(surround))
            if peak_val == max(window_b) and surround_avg > 0 and peak_val > surround_avg * thresholds.bloom_ratio:
                conf = min(0.70, (peak_val / surround_avg - 1.0) / thresholds.bloom_ratio)
                _emit(i, "BLOOM", conf,
                      f"輝度ピーク={peak_val:.1f} (周辺平均={surround_avg:.1f} 比{peak_val/surround_avg:.2f}倍)",
                      {"brightness_peak": peak_val, "surround_avg": round(surround_avg, 1)})

    return events


# ── per-frame CSV に micro_event を付与 ─────────────────────────

def attach_events_to_frames(frame_metrics: list, events: list) -> list:
    """
    events リストを使って frame_metrics の各行に micro_event を付与。
    1フレームに複数イベントがある場合は | 区切り。
    """
    from collections import defaultdict
    ev_map = defaultdict(list)
    for ev in events:
        ev_map[ev["frame_no"]].append(ev)

    out = []
    for m in frame_metrics:
        row = {k: v for k, v in m.items() if not k.startswith("_")}
        fn = m["frame_no"]
        if fn in ev_map:
            evs = ev_map[fn]
            row["micro_event"]      = "|".join(e["event"] for e in evs)
            row["event_confidence"] = round(max(e["confidence"] for e in evs), 3)
            row["event_notes"]      = " / ".join(e["notes"] for e in evs)[:200]
        else:
            row["micro_event"]      = "NONE"
            row["event_confidence"] = 0.0
            row["event_notes"]      = ""
        out.append(row)
    return out


# ── サマリー生成 ─────────────────────────────────────────────────

def build_summary(
    window_spec: str,
    frame_metrics: list,
    events: list,
    source_id: str,
    article_id: str,
    thresholds: Thresholds,
    fps: float,
) -> str:
    from collections import Counter
    n_frames = len(frame_metrics)
    event_counts = Counter(e["event"] for e in events)

    lines = [
        "# Micro Frame Analyzer Summary",
        "",
        f"- 実行日時   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- article_id : {article_id}",
        f"- source_id  : {source_id}",
        f"- 区間       : {window_spec}",
        f"- フレーム数 : {n_frames} (@ {fps:.1f} fps)",
        f"- 分類器     : {VERSION}",
        "",
        "---",
        "",
        "## 使用閾値",
        "",
        "| パラメータ | 値 |",
        "|-----------|-----|",
    ]
    for k, v in asdict(thresholds).items():
        lines.append(f"| {k} | {v} |")

    lines += [
        "",
        "---",
        "",
        "## イベント候補 集計",
        "",
        "| event | 件数 |",
        "|-------|------|",
    ]
    if event_counts:
        for ev, cnt in event_counts.most_common():
            lines.append(f"| {ev} | {cnt} |")
    else:
        lines.append("| （検出なし） | 0 |")

    lines += ["", "---", "", "## 検出イベント 詳細", ""]

    if not events:
        lines.append("（イベント候補なし）")
    else:
        lines += [
            "| 時刻 (s) | フレーム# | イベント | 信頼度 | notes |",
            "|---------|---------|---------|--------|-------|",
        ]
        for e in sorted(events, key=lambda x: x["timestamp_s"]):
            note_short = e["notes"][:80] + ("…" if len(e["notes"]) > 80 else "")
            lines.append(
                f"| {e['timestamp_s']:.3f} | {e['frame_no']} "
                f"| {e['event']} | {e['confidence']:.2f} | {note_short} |"
            )

    lines += [
        "",
        "---",
        "",
        "## 輝度推移（概要）",
        "",
        "| 時刻 (s) | brightness_mean | frame_diff_mean | micro_event |",
        "|---------|-----------------|-----------------|-------------|",
    ]
    step = max(1, n_frames // 20)
    ev_ts_set = {e["timestamp_s"] for e in events}
    for m in frame_metrics[::step]:
        ts = m["timestamp_s"]
        marker = "← ⚠️" if ts in ev_ts_set else ""
        lines.append(
            f"| {ts:.3f} "
            f"| {m['brightness_mean']:>10.1f} "
            f"| {m['frame_diff_mean']:>10.3f} "
            f"| {m.get('micro_event', 'NONE')} {marker} |"
        )

    return "\n".join(lines)


# ── ファイル出力 ─────────────────────────────────────────────────

def write_outputs(
    frame_metrics_with_events: list,
    events: list,
    out_dir: Path,
    summary: str,
):
    # micro_frame_events.csv
    csv_path = out_dir / "micro_frame_events.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in frame_metrics_with_events:
            writer.writerow({k: row.get(k, "") for k in CSV_FIELDS})

    # micro_frame_summary.md
    md_path = out_dir / "micro_frame_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(summary)

    # event_candidates.jsonl
    jsonl_path = out_dir / "event_candidates.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for ev in sorted(events, key=lambda x: x["timestamp_s"]):
            record = {k: ev.get(k) for k in JSONL_FIELDS if k in ev or k in ["notes"]}
            # 追加メトリクス（任意キー）
            extra_keys = [k for k in ev if k not in JSONL_FIELDS]
            for k in extra_keys:
                record[k] = ev[k]
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return csv_path, md_path, jsonl_path


# ── トリガーソース読み込み ─────────────────────────────────────

def load_manual_windows(windows_str: str, video_duration: float) -> list:
    """"255:257,22:24" → [(255.0, 257.0), ...]"""
    result = []
    for token in windows_str.split(","):
        token = token.strip()
        if not token:
            continue
        parts = token.split(":")
        if len(parts) != 2:
            print(f"  [WARN] フォーマット誤り: '{token}' スキップ", file=sys.stderr)
            continue
        try:
            s, e = float(parts[0]), float(parts[1])
        except ValueError:
            continue
        if s >= e:
            print(f"  [WARN] start >= end: '{token}' スキップ", file=sys.stderr)
            continue
        s = max(0.0, min(s, video_duration))
        e = max(0.0, min(e, video_duration))
        result.append((s, e))
    return result


def load_camera_event_windows(
    csv_path: Path,
    target_events: set,
    window: float,
    video_duration: float,
) -> list:
    """camera_events.csv の指定イベントの前後 ±window 秒区間を返す"""
    import csv as csv_mod
    windows = []
    if not csv_path.exists():
        print(f"  [ERROR] camera-events-csv が見つかりません: {csv_path}", file=sys.stderr)
        return []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv_mod.DictReader(f):
            ev = row.get("camera_event", "").strip()
            if ev not in target_events:
                continue
            try:
                ts = float(row["timestamp_s"])
            except (KeyError, ValueError):
                continue
            s = max(0.0, ts - window)
            e = min(video_duration, ts + window)
            windows.append((s, e))
    return windows


# ── CLI ─────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description=f"{VERSION}: 候補区間を全フレーム解析する Micro Pass",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 動画・識別子
    p.add_argument("--video", required=True, type=Path, help="元動画ファイルパス")
    p.add_argument("--source-id", default="", help="source_id (例: DOW-UAP-PR062_...)")
    p.add_argument("--article-id", default="", help="article_id (例: R02-054)")

    # トリガーソース
    trig = p.add_argument_group("トリガーソース（1つ以上必須）")
    trig.add_argument("--manual-windows", default="",
                      help='手動区間 "START:END,START:END,..." (秒指定)')
    trig.add_argument("--camera-events-csv", type=Path,
                      help="Camera Analyzer 出力 (camera_events.csv)")
    trig.add_argument("--camera-trigger-events",
                      default="EDGE_SURGE,COMBINED,BLACKOUT,WHITEOUT,FOV_SWITCH",
                      help="Camera Analyzer のトリガーイベント（カンマ区切り）")
    trig.add_argument("--window", type=float, default=1.0,
                      help="CSV トリガー前後の解析幅 (秒, デフォルト 1.0)")

    # 出力
    p.add_argument("--output-dir", type=Path,
                   help="出力先（省略時: data/micro_frame_runs/<date>/<source_id>/）")
    p.add_argument("--keep-frames", action="store_true",
                   help="抽出フレーム画像を frames/ サブディレクトリに保存する")

    # 閾値（全て調整可能）
    th = p.add_argument_group("検出閾値（デフォルト値で実行可; PR062 検証後に調整推奨）")
    th.add_argument("--blackout-thresh", type=float, default=15.0,
                    help="BLACKOUT: 平均輝度 < この値 (default 15.0)")
    th.add_argument("--whiteout-thresh", type=float, default=240.0,
                    help="WHITEOUT: 平均輝度 > この値 (default 240.0)")
    th.add_argument("--flash-delta", type=float, default=60.0,
                    help="FLASH: 輝度スパイク幅 (前後フレーム差 > この値, default 60.0)")
    th.add_argument("--hard-cut-diff", type=float, default=50.0,
                    help="HARD_CUT: frame_diff_mean > この値 (default 50.0)")
    th.add_argument("--hard-cut-hf", type=float, default=2.0,
                    help="HARD_CUT: hf_ratio_vs_prev の倍率閾値 (default 2.0)")
    th.add_argument("--frame-drop-diff", type=float, default=1.0,
                    help="FRAME_DROP: frame_diff_mean < この値 (default 1.0)")
    th.add_argument("--sensor-sat-delta", type=float, default=30.0,
                    help="SENSOR_SWITCH: 彩度変化 > この値 (default 30.0)")
    th.add_argument("--fov-switch-hf-high", type=float, default=3.0,
                    help="FOV_SWITCH: hf_ratio_vs_prev > この値 (default 3.0)")
    th.add_argument("--fov-switch-hf-low", type=float, default=0.33,
                    help="FOV_SWITCH: hf_ratio_vs_prev < この値 (default 0.33)")
    th.add_argument("--zoom-in-hf", type=float, default=2.0,
                    help="ZOOM_IN: hf_self / rolling_avg > この値 (default 2.0)")
    th.add_argument("--zoom-out-hf", type=float, default=0.50,
                    help="ZOOM_OUT: hf_self / rolling_avg < この値 (default 0.50)")
    th.add_argument("--zoom-rolling-n", type=int, default=5,
                    help="ZOOM: rolling avg のフレーム数 (default 5)")
    th.add_argument("--bloom-window", type=int, default=10,
                    help="BLOOM: ピーク検出窓 (フレーム数, default 10)")
    th.add_argument("--bloom-ratio", type=float, default=1.30,
                    help="BLOOM: peak / surround_avg > この倍率 (default 1.30)")

    # 実行制御
    p.add_argument("--execute", action="store_true",
                   help="実行モード（省略時は dry-run）")
    p.add_argument("--verbose", action="store_true",
                   help="フレームごとの詳細ログを表示")

    return p.parse_args()


def main():
    args = parse_args()

    # 閾値オブジェクトを構築
    thr = Thresholds(
        blackout_thresh    = args.blackout_thresh,
        whiteout_thresh    = args.whiteout_thresh,
        flash_delta        = args.flash_delta,
        hard_cut_diff      = args.hard_cut_diff,
        hard_cut_hf        = args.hard_cut_hf,
        frame_drop_diff    = args.frame_drop_diff,
        sensor_sat_delta   = args.sensor_sat_delta,
        fov_switch_hf_high = args.fov_switch_hf_high,
        fov_switch_hf_low  = args.fov_switch_hf_low,
        zoom_in_hf         = args.zoom_in_hf,
        zoom_out_hf        = args.zoom_out_hf,
        zoom_rolling_n     = args.zoom_rolling_n,
        bloom_window       = args.bloom_window,
        bloom_ratio        = args.bloom_ratio,
    )

    video_path = args.video
    if not video_path.exists():
        sys.exit(f"[ERROR] --video が見つかりません: {video_path}")

    has_trigger = args.manual_windows.strip() or args.camera_events_csv
    if not has_trigger:
        sys.exit(
            "[ERROR] トリガーソースが指定されていません。\n"
            "  --manual-windows または --camera-events-csv を指定してください。"
        )

    mode = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"[{VERSION}] mode={mode}")
    print(f"  video      : {video_path}")
    print(f"  source_id  : {args.source_id}")

    fps = get_video_fps(video_path)
    dur = get_video_duration(video_path)
    print(f"  fps        : {fps:.1f}")
    print(f"  duration   : {dur:.1f}s")
    print()

    # ── トリガーソース収集 ──────────────────────────────────────
    windows = []

    if args.manual_windows.strip():
        mw = load_manual_windows(args.manual_windows, dur)
        print(f"[手動区間] {len(mw)} 区間")
        for s, e in mw:
            n_est = int((e - s) * fps)
            print(f"  {s:.1f}〜{e:.1f}s → 約 {n_est} フレーム")
        windows.extend(mw)
        print()

    if args.camera_events_csv:
        cam_events = set(e.strip() for e in args.camera_trigger_events.split(","))
        cw = load_camera_event_windows(args.camera_events_csv, cam_events, args.window, dur)
        print(f"[Camera Events] {len(cw)} 区間 (events={sorted(cam_events)})")
        for s, e in cw:
            print(f"  {s:.1f}〜{e:.1f}s")
        windows.extend(cw)
        print()

    if not windows:
        print("[結果] 有効な区間が0件のため終了します。")
        return

    if not args.execute:
        total_frames = sum(int((e - s) * fps) for s, e in windows)
        print(
            f"[DRY-RUN 完了] --execute を付けると {len(windows)} 区間 / "
            f"約 {total_frames} フレームを解析します。"
        )
        return

    # ── EXECUTE ──────────────────────────────────────────────────
    run_date = date.today().isoformat().replace("-", "")
    source_slug = args.source_id or video_path.stem

    for win_idx, (start, end) in enumerate(windows):
        win_label = f"{start:.1f}s_{end:.1f}s"
        print(f"=== 区間 {win_idx+1}/{len(windows)}: {win_label} ===")

        # 出力ディレクトリ
        if args.output_dir:
            out_dir = args.output_dir / win_label
        else:
            out_dir = (
                Path("data/micro_frame_runs")
                / run_date
                / source_slug
                / win_label
            )
        out_dir.mkdir(parents=True, exist_ok=True)

        # フレーム抽出先
        frames_tmp = out_dir / "frames" if args.keep_frames else Path(
            tempfile.mkdtemp(prefix="micro_frames_")
        )
        frames_tmp.mkdir(parents=True, exist_ok=True)

        print(f"  フレーム抽出中 ({start:.1f}〜{end:.1f}s @ {fps:.1f}fps)...")
        frame_entries = extract_micro_frames(video_path, start, end, frames_tmp, fps)
        n_frames = len(frame_entries)
        print(f"  抽出完了: {n_frames} フレーム → {frames_tmp}/")

        if n_frames < 2:
            print("  [WARN] フレームが2枚未満のためスキップ。")
            if not args.keep_frames:
                shutil.rmtree(frames_tmp, ignore_errors=True)
            continue

        # per-frame 解析
        print(f"  フレーム解析中 ({n_frames} frames)...")
        frame_metrics = analyze_all_frames(frame_entries, thr, verbose=args.verbose)

        # イベント検出
        events = detect_events(frame_metrics, thr)

        # CSV 用にイベントを付与
        frame_metrics_ev = attach_events_to_frames(frame_metrics, events)

        # サマリー生成
        summary = build_summary(
            win_label, frame_metrics_ev, events,
            args.source_id, args.article_id, thr, fps
        )

        # ファイル出力
        csv_p, md_p, jsonl_p = write_outputs(frame_metrics_ev, events, out_dir, summary)

        # 一時フレーム削除
        if not args.keep_frames:
            shutil.rmtree(frames_tmp, ignore_errors=True)

        # 結果表示
        from collections import Counter
        ev_counts = Counter(e["event"] for e in events)
        print(f"  検出イベント: {dict(ev_counts.most_common())}")
        print(f"  CSV   : {csv_p}")
        print(f"  MD    : {md_p}")
        print(f"  JSONL : {jsonl_p}")
        if args.keep_frames:
            print(f"  フレーム: {frames_tmp}/")
        print()

    print("[完了]")


if __name__ == "__main__":
    main()
