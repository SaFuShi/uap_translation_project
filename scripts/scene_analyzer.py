#!/usr/bin/env python3
"""
scene_analyzer.py — Scene Analyzer (Media Inspector v4 Agent 1)

役割: フレームの背景・環境・センサー種別を分類する。

設計書: docs/media_inspector_v4_architecture.md (Agent 1: Scene Analyzer)

v4 での位置づけ:
  全 Agent の最初に実行する。背景種別・センサーモードを確定し、
  Camera Analyzer / Motion Intelligence v4 / Shadow Analyzer の前提情報を提供する。

PR062 で判明した問題への対応:
  地表面（山脈）を雲面と誤認した根本原因は背景分類 Agent が存在しなかったこと。
  本 Agent はエッジ密度・高周波比率・テクスチャ分散を用いて雲と地表面を区別する。

使い方:
  # dry-run（先頭 5 フレームをプレビュー）
  python3 scripts/scene_analyzer.py \\
    --frames-dir data/adaptive_frames/20260628/DOW-UAP-PR062_.../ \\
    --source-id DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1 \\
    --article-id R02-054

  # 実行
  python3 scripts/scene_analyzer.py \\
    --frames-dir data/adaptive_frames/20260628/DOW-UAP-PR062_.../ \\
    --source-id DOW-UAP-PR062_Spherical_UAP_CALLSIGN_2021_04_12_vid_1 \\
    --article-id R02-054 \\
    --output-dir data/media_inspector_runs/20260628/DOW-UAP-PR062_.../scene_analysis/ \\
    --execute
"""

import argparse
import csv
import json
import math
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

import numpy as np
from PIL import Image

VERSION = "scene_analyzer_v1"

# ── 黒塗り・UI マスク ───────────────────────────────────────────────────────
BLACK_THRESH       = 15     # この値以下の輝度ピクセルを黒塗り（除外）とみなす
BRIGHT_THRESH      = 245    # ホワイトアウト検出用（平均輝度がこれ以上）

# ── 夜間・昼間 判定 ─────────────────────────────────────────────────────────
NIGHT_BRIGHTNESS   = 30     # 夜間の平均輝度上限

# ── センサーモード判定 ──────────────────────────────────────────────────────
GRAYSCALE_DIFF_MAX = 8.0    # RGB 差がこれ以下ならグレースケール/IR とみなす

# ── Scene 分類 閾値 ─────────────────────────────────────────────────────────
#
# 設計方針:
#   PR062 で判明した通り、高高度航空映像では山岳地形も雲面と同等の
#   滑らかなテクスチャを持つ。テクスチャ単体では区別不能。
#   可視光カラー映像では【輝度】が最良の識別子:
#     - 可視光の雲（上面）: 白/明るいグレー（180-255）
#     - 地表面: 中輝度グレー/褐色（40-140）
#   輝度 + FFT高周波比率 + テクスチャで多段判定する。

# エッジ密度（Sobel正規化値）
# 高高度映像では地表面でも edge < 0.020 になるため、地表面の「証拠」としては
# 使わず、非常に強いエッジ（稜線など）があれば地表面とする。
EDGE_GROUND_STRONG  = 0.040  # 稜線・山脈エッジが明確なら地表面（強）
EDGE_GROUND_WEAK    = 0.020  # やや強いエッジなら地表面寄り
EDGE_CLOUD_MAX      = 0.008  # これ以下なら雲寄り（+1）。エッジはあまり使わない

# 高周波比率（FFT、DC除去後の hi / (hi+lo)）
HIFREQ_GROUND_STRONG = 0.150
HIFREQ_GROUND_WEAK   = 0.100
HIFREQ_CLOUD_STRONG  = 0.060
HIFREQ_CLOUD_WEAK    = 0.080

# テクスチャ分散（8×8 パッチの輝度標準偏差の平均）
TEXTURE_GROUND_MIN   = 15.0
TEXTURE_CLOUD_MAX    = 1.0   # 極めて均一（std≈0）なら雲証拠。PR062(2-4)はここに入らない

# 可視光カラー映像の輝度（最重要識別子）
# 上空から見た雲の頂部は明るい白。地表面は中輝度グレー/褐色。
COLOR_CLOUD_BRIGHT   = 155   # 輝度 > 155 → 雲（+2）
COLOR_GROUND_BRIGHT  = 125   # 輝度 < 125 → 地表面（+2）

# 最低信頼度（unknown 判定のボーダー）
CONF_UNKNOWN_MAX = 2   # スコア差がこれ以下なら unknown

# ── センサーモード別 前提・信頼度制御 ────────────────────────────────────────
#
# color 映像: 輝度による地表/雲識別が有効（本スクリプトの主設計対象）
# grayscale:  可視光モノクロ/IR/センサー処理済みの可能性あり。輝度識別を無効化
# ir:         熱映像。輝度＝熱分布。白い領域＝雲・黒い領域＝地表とは限らない
# night_vision: 暗視増感映像。輝度は増感処理の影響を受ける
# unknown:    センサー不明。手動指定 (--sensor-mode) を推奨
#
# 自動検出ではグレースケールと IR / 暗視の区別が困難。
# それらの映像を使う場合は --sensor-mode フラグで手動指定すること。

SENSOR_MODE_NOTES: dict = {
    "color": (
        "可視光カラー映像。輝度による地表/雲識別が有効（可視光の雲は白い）。"
        "現在の分類ロジックを最大信頼度で使用する。"
    ),
    "grayscale": (
        "グレースケール映像（可視光モノクロ/IR/センサー処理済みの可能性あり）。"
        "輝度の意味が可視光と異なる可能性があるため、輝度識別を無効化する。"
        "地表/雲/海の断定信頼度を低下させる（×0.75）。"
        "IR や暗視系と確認できた場合は --sensor-mode ir/night_vision で再実行を推奨。"
    ),
    "ir": (
        "赤外線（IR）映像。輝度は熱・センサー処理を反映し、可視光の明るさではない。"
        "白い領域＝雲・黒い領域＝地表とは限らない（センサー設定により逆転する場合あり）。"
        "地表/雲/海の分類は暫定扱い。信頼度を低下させる（×0.55）。"
        "Human review による最終確認が必須。"
    ),
    "night_vision": (
        "暗視カメラ系映像（増感処理・NVG等）。輝度は増感処理の影響を受ける。"
        "可視光の明るさではないため輝度識別は無効。"
        "地表/雲/海の分類は暫定扱い。信頼度を低下させる（×0.55）。"
        "Human review による最終確認が必須。"
    ),
    "unknown": (
        "センサー種別不明。自動検出に失敗した可能性がある。"
        "--sensor-mode フラグで手動指定を推奨。"
        "分類は暫定扱い（×0.65）。"
    ),
}

# センサー種別ごとの confidence スケーリング係数
SENSOR_CONFIDENCE_FACTOR: dict = {
    "color":        1.00,  # フルスコア（輝度識別有効）
    "grayscale":    0.75,  # 輝度意味不明のため低下
    "ir":           0.55,  # 輝度の意味が逆転する可能性
    "night_vision": 0.55,  # 増感処理の影響
    "unknown":      0.65,
}

# センサー種別ごとに「地表・雲の断定が暫定」かどうか
SENSOR_CLASSIFICATION_PROVISIONAL: dict = {
    "color":        False,
    "grayscale":    True,
    "ir":           True,
    "night_vision": True,
    "unknown":      True,
}

# ── CSV フィールド ──────────────────────────────────────────────────────────
CSV_FIELDS = [
    "frame_name", "timestamp_s",
    "scene_type", "ground_subtype", "lighting_type", "sensor_mode",
    "scene_confidence",
    "mean_brightness", "texture_variance", "edge_density", "spatial_freq_ratio",
    "masked_pixel_ratio",
    "scene_notes",
]

# ── scene_type 日本語説明 ──────────────────────────────────────────────────
SCENE_DESC = {
    "ground_surface": "地表面",
    "cloud":          "雲面",
    "sky":            "空（上空）",
    "sea":            "海面",
    "night_sky":      "夜空",
    "mixed":          "混在（地表+雲等）",
    "unknown":        "判定不能",
}


# ════════════════════════════════════════════════════════════════════════════
# 画像ロード
# ════════════════════════════════════════════════════════════════════════════

def load_rgb(path: Path):
    """RGB ndarray (H, W, 3) をロード"""
    return np.array(Image.open(path).convert("RGB"), dtype=np.uint8)


def to_gray(rgb: np.ndarray) -> np.ndarray:
    """RGB → グレースケール（輝度式）"""
    return (
        0.299 * rgb[:, :, 0].astype(np.float32)
        + 0.587 * rgb[:, :, 1].astype(np.float32)
        + 0.114 * rgb[:, :, 2].astype(np.float32)
    ).astype(np.float32)


# ════════════════════════════════════════════════════════════════════════════
# マスク生成（黒塗り除外）
# ════════════════════════════════════════════════════════════════════════════

def build_valid_mask(gray: np.ndarray) -> np.ndarray:
    """
    黒塗り矩形（純黒ピクセル）を除外したブール mask を返す。
    True = 有効ピクセル。
    """
    return gray > BLACK_THRESH


# ════════════════════════════════════════════════════════════════════════════
# 特徴量計算
# ════════════════════════════════════════════════════════════════════════════

def mean_brightness(gray: np.ndarray, mask: np.ndarray) -> float:
    valid = gray[mask]
    return float(np.mean(valid)) if valid.size > 0 else 0.0


def texture_variance(gray: np.ndarray, mask: np.ndarray,
                     patch_size: int = 8) -> float:
    """ローカルパッチ (patch_size×patch_size) ごとの輝度標準偏差の平均。"""
    h, w = gray.shape
    stds = []
    for y in range(0, h - patch_size, patch_size):
        for x in range(0, w - patch_size, patch_size):
            patch_gray = gray[y:y + patch_size, x:x + patch_size]
            patch_mask = mask[y:y + patch_size, x:x + patch_size]
            valid = patch_gray[patch_mask]
            if valid.size < patch_size * patch_size // 2:
                continue
            stds.append(float(np.std(valid)))
    return float(np.mean(stds)) if stds else 0.0


def sobel_edge_density(gray: np.ndarray, mask: np.ndarray) -> float:
    """
    Sobel フィルタによるエッジ密度（0〜1 に正規化）。

    黒塗り境界のアーティファクトを避けるため、全 8 近傍が有効なピクセルのみを
    評価対象とする（マスク侵食）。ゼロ埋めをしないことで境界での人工エッジを防ぐ。
    """
    img = gray.astype(np.float32)  # 元の値をそのまま使用（ゼロ埋めしない）

    # Sobel Gx / Gy
    gx = (
        -img[:-2, :-2] + img[:-2, 2:]
        - 2 * img[1:-1, :-2] + 2 * img[1:-1, 2:]
        - img[2:, :-2] + img[2:, 2:]
    )
    gy = (
        -img[:-2, :-2] - 2 * img[:-2, 1:-1] - img[:-2, 2:]
        + img[2:, :-2] + 2 * img[2:, 1:-1] + img[2:, 2:]
    )
    magnitude = np.sqrt(gx ** 2 + gy ** 2)

    # 全 9 近傍が有効なピクセルのみ評価（黒塗り境界排除）
    m = mask.astype(np.float32)
    neigh = (
        m[:-2, :-2] + m[:-2, 1:-1] + m[:-2, 2:]
        + m[1:-1, :-2] + m[1:-1, 1:-1] + m[1:-1, 2:]
        + m[2:, :-2] + m[2:, 1:-1] + m[2:, 2:]
    )
    safe = neigh == 9  # 全近傍が有効

    valid_mag = magnitude[safe]
    if valid_mag.size == 0:
        return 0.0

    # 最大理論値: 4 * 255 * sqrt(2) ≈ 1442
    return float(np.mean(valid_mag) / 1442.0)


def spatial_freq_ratio(gray: np.ndarray, mask: np.ndarray,
                       crop_size: int = 256) -> float:
    """
    FFT による高周波 vs 低周波の比率（hi / (hi + lo)）。

    DCバイアス排除:
      - 黒塗り領域をシーン平均値で補填してから平均を引く（DC → 0）
      - DC を除いた状態で hi / lo を計算するため、輝度均一性の影響を受けない

    高周波 = 周波数半径の外側 35%、低周波 = 内側 20%（DC除く）
    """
    h, w = gray.shape
    cy, cx = h // 2, w // 2
    half = crop_size // 2
    y0 = max(cy - half, 0)
    x0 = max(cx - half, 0)
    crop = gray[y0:y0 + crop_size, x0:x0 + crop_size].astype(np.float32)
    crop_mask = mask[y0:y0 + crop_size, x0:x0 + crop_size]
    ch, cw = crop.shape

    valid = crop[crop_mask]
    if valid.size < ch * cw * 0.20:  # 有効ピクセルが 20% 未満なら信頼不能
        return 0.0

    # 黒塗り領域をシーン平均値で補填（DC バイアスを防ぐ）
    fill_val = float(np.mean(valid))
    crop_filled = crop.copy()
    crop_filled[~crop_mask] = fill_val

    # DC 除去（平均を引く）→ DC 成分がゼロになる
    crop_detrended = crop_filled - crop_filled.mean()

    fft_shifted = np.fft.fftshift(np.fft.fft2(crop_detrended))
    power = np.abs(fft_shifted) ** 2

    y_idx, x_idx = np.mgrid[0:ch, 0:cw]
    max_dist = min(ch, cw) / 2.0
    dist = np.sqrt((y_idx - ch / 2.0) ** 2 + (x_idx - cw / 2.0) ** 2)

    lo_mask = (dist > 1) & (dist <= max_dist * 0.20)
    hi_mask = dist > max_dist * 0.35

    lo_power = np.sum(power[lo_mask])
    hi_power = np.sum(power[hi_mask])
    total = lo_power + hi_power

    if total < 1e-10:
        return 0.0

    return float(hi_power / total)


def uniformity(gray: np.ndarray, mask: np.ndarray, delta: float = 10.0) -> float:
    """
    有効ピクセルのうち、平均輝度 ± delta 以内の割合。
    雲は均一なので高い値を示す。
    """
    valid = gray[mask]
    if valid.size == 0:
        return 0.0
    m = np.mean(valid)
    near = np.sum(np.abs(valid - m) <= delta)
    return float(near / valid.size)


# ════════════════════════════════════════════════════════════════════════════
# センサーモード判定
# ════════════════════════════════════════════════════════════════════════════

def detect_sensor_mode(rgb: np.ndarray, mask: np.ndarray) -> str:
    """
    RGB チャンネルの差分とUI要素の有無からセンサーモードを推定する。

    検出方法:
      1. 高彩度ピクセル（chroma > 60）が 0.05% 以上 → カラーセンサー確定
         根拠: カラー映像のUIオーバーレイ（シアン・赤等）は chroma が非常に高い。
         中立グレー景色であっても、シアンのクロスヘア1本でこの閾値を超える。
      2. 全体平均の RGB チャンネル差が GRAYSCALE_DIFF_MAX 超 → カラー
      3. それ以外 → グレースケール（IR詳細判定は将来対応）

    Returns:
      "color" / "grayscale" / "ir_white_hot" / "ir_black_hot" / "unknown"
    """
    r_f = rgb[:, :, 0].astype(np.float32)
    g_f = rgb[:, :, 1].astype(np.float32)
    b_f = rgb[:, :, 2].astype(np.float32)

    # ① 高彩度ピクセル（UIオーバーレイ）の存在チェック
    chroma = (
        np.max(rgb.astype(np.float32), axis=2)
        - np.min(rgb.astype(np.float32), axis=2)
    )
    high_chroma_ratio = float(np.sum(chroma > 60) / max(rgb.shape[0] * rgb.shape[1], 1))
    if high_chroma_ratio > 0.0002:  # 0.02%以上の高彩度ピクセル → カラー確定
        return "color"

    # ② 平均チャンネル差チェック
    if not mask.any():
        return "unknown"
    rg = np.mean(np.abs(r_f[mask] - g_f[mask]))
    gb = np.mean(np.abs(g_f[mask] - b_f[mask]))
    rb = np.mean(np.abs(r_f[mask] - b_f[mask]))
    if max(rg, gb, rb) > GRAYSCALE_DIFF_MAX:
        return "color"

    return "grayscale"


# ════════════════════════════════════════════════════════════════════════════
# 照明種別判定
# ════════════════════════════════════════════════════════════════════════════

def detect_lighting(mean_br: float, sensor_mode: str) -> str:
    if sensor_mode in ("ir_white_hot", "ir_black_hot"):
        return "ir"
    if mean_br < NIGHT_BRIGHTNESS:
        return "nighttime"
    return "daytime"


# ════════════════════════════════════════════════════════════════════════════
# 地表サブタイプ判定（scene_type == ground_surface のとき）
# ════════════════════════════════════════════════════════════════════════════

def detect_ground_subtype(rgb: np.ndarray, mask: np.ndarray,
                          sensor_mode: str) -> str:
    """
    地表面のサブタイプを RGB 色調から推定する。

    UI要素（シアン色のクロスヘア・マーカー）を除外するため、
    彩度（chroma）が高いピクセルをフィルタしてからシーン色調を評価する。

    Returns:
      "arid" / "rocky" / "vegetated" / "snow" / "water" / "unknown"
    """
    if sensor_mode != "color":
        return "unknown"

    r_ch = rgb[:, :, 0].astype(float)
    g_ch = rgb[:, :, 1].astype(float)
    b_ch = rgb[:, :, 2].astype(float)

    # UI要素フィルタ:
    # シアン色クロスヘア・Nマーカー等は chroma (max-min) が高い。
    # 地形・雲等のシーンコンテンツは chroma が低い（グレー〜薄い彩色）。
    chroma = (
        np.max(rgb.astype(float), axis=2)
        - np.min(rgb.astype(float), axis=2)
    )
    # chroma < 35: UI でないシーンピクセル
    scene_mask = mask & (chroma < 35)

    r = r_ch[scene_mask]
    g = g_ch[scene_mask]
    b = b_ch[scene_mask]

    if r.size < 500:   # 有効シーンピクセルが少なすぎる場合
        return "unknown"

    mean_r, mean_g, mean_b = np.mean(r), np.mean(g), np.mean(b)
    bright = (mean_r + mean_g + mean_b) / 3.0

    # 雪：高輝度・均一
    if bright > 180 and np.std(r) < 20:
        return "snow"

    # 水面：青が明確に優位・暗め（UI除去後でも青優位なら本当に水面の可能性）
    if mean_b > mean_r + 25 and mean_b > mean_g + 15 and bright < 100:
        return "water"

    # 植生：緑優位
    if mean_g > mean_r + 5 and mean_g > mean_b + 5:
        return "vegetated"

    # 乾燥地帯（砂漠/荒地）：茶・黄土色
    if mean_r > mean_b + 10 and bright > 80:
        return "arid"

    # 岩石地帯：灰色系・中輝度
    if abs(mean_r - mean_b) < 15 and abs(mean_r - mean_g) < 15 and bright < 160:
        return "rocky"

    return "unknown"


# ════════════════════════════════════════════════════════════════════════════
# Scene 分類（メイン判定ロジック）
# ════════════════════════════════════════════════════════════════════════════

def classify_scene(
    mean_br: float,
    tex_var: float,
    edge_dens: float,
    hi_freq: float,
    unif: float,
    lighting: str,
    sensor_mode: str = "unknown",
) -> tuple:
    """
    特徴量から scene_type と confidence を返す。

    識別の優先順位:
      1. 輝度（カラーセンサーの場合: 可視光の雲は白い / 地表面は中輝度）
      2. FFT 高周波比率（DC除去済み）
      3. テクスチャ分散（補助）
      4. エッジ密度（補助: 非常に高いエッジは地表確定のみ使用）

    Returns:
      (scene_type, confidence, score_ground, score_cloud, notes_list)
    """
    notes = []
    score_ground = 0
    score_cloud  = 0

    # ── 夜間は特別処理 ─────────────────────────────────────────────────────
    if lighting == "nighttime":
        return "night_sky", 0.70, 0, 0, ["輝度が低いため夜空と判定"]

    # ── 非常に高輝度 → 空（ホワイトアウト気味）──────────────────────────
    if mean_br > 215 and tex_var < 5.0:
        return "sky", 0.65, 0, 0, ["高輝度・低テクスチャのため空と判定"]

    # ── [最重要] カラー映像の輝度による識別 ─────────────────────────────
    # 可視光カラー映像では上空の雲面は白く明るい（180-255）。
    # 地表面（山岳・砂漠・海等）は中輝度グレー/褐色（40-140）。
    # PR062 のような高高度航空映像では輝度が最も信頼できる識別子。
    if sensor_mode == "color":
        if mean_br > COLOR_CLOUD_BRIGHT:
            score_cloud += 2
            notes.append(
                f"高輝度({mean_br:.0f}>{COLOR_CLOUD_BRIGHT})+color→雲"
                "（可視光の雲面は白い）"
            )
        elif mean_br < COLOR_GROUND_BRIGHT:
            score_ground += 2
            notes.append(
                f"低〜中輝度({mean_br:.0f}<{COLOR_GROUND_BRIGHT})+color→地表面"
                "（可視光の雲面は通常より明るい）"
            )

    # ── 高周波比率スコア（DC除去済み FFT）───────────────────────────────
    if hi_freq >= HIFREQ_GROUND_STRONG:
        score_ground += 2
        notes.append(f"高周波比率高({hi_freq:.4f}≥{HIFREQ_GROUND_STRONG})→地表")
    elif hi_freq >= HIFREQ_GROUND_WEAK:
        score_ground += 1
        notes.append(f"高周波比率やや高({hi_freq:.4f})→地表寄り")
    elif hi_freq <= HIFREQ_CLOUD_STRONG:
        score_cloud += 2
        notes.append(f"高周波比率低({hi_freq:.4f}≤{HIFREQ_CLOUD_STRONG})→雲")
    elif hi_freq <= HIFREQ_CLOUD_WEAK:
        score_cloud += 1
        notes.append(f"高周波比率やや低({hi_freq:.4f})→雲寄り")

    # ── エッジ密度スコア ──────────────────────────────────────────────────
    # 高高度映像では地表面でも edge が低くなるため、
    # 「雲の証拠」には使わず「地表確定の強証拠」のみ使用する。
    if edge_dens >= EDGE_GROUND_STRONG:
        score_ground += 2
        notes.append(f"エッジ密度高({edge_dens:.4f}≥{EDGE_GROUND_STRONG})→地表（稜線）")
    elif edge_dens >= EDGE_GROUND_WEAK:
        score_ground += 1
        notes.append(f"エッジ密度やや高({edge_dens:.4f})→地表寄り")
    elif edge_dens <= EDGE_CLOUD_MAX:
        score_cloud += 1
        notes.append(f"エッジ密度微小({edge_dens:.4f}≤{EDGE_CLOUD_MAX})→雲寄り（参考）")

    # ── テクスチャ分散スコア ──────────────────────────────────────────────
    if tex_var >= TEXTURE_GROUND_MIN:
        score_ground += 1
        notes.append(f"テクスチャ分散高({tex_var:.1f}≥{TEXTURE_GROUND_MIN})→地表")
    elif tex_var <= TEXTURE_CLOUD_MAX:
        # 極めて均一（TV≈0）な場合のみ雲証拠とする
        score_cloud += 1
        notes.append(f"テクスチャ分散極小({tex_var:.1f}≤{TEXTURE_CLOUD_MAX})→雲（参考）")

    # ── 最終判定 ──────────────────────────────────────────────────────────
    diff = score_ground - score_cloud

    if diff >= 3:
        scene_type = "ground_surface"
        confidence = min(0.55 + diff * 0.07, 0.92)
    elif diff == 2:
        scene_type = "ground_surface"
        confidence = 0.68
    elif diff == 1:
        scene_type = "ground_surface"
        confidence = 0.55
    elif diff == -1:
        scene_type = "cloud"
        confidence = 0.55
    elif diff == -2:
        scene_type = "cloud"
        confidence = 0.68
    elif diff <= -3:
        scene_type = "cloud"
        confidence = min(0.55 + abs(diff) * 0.07, 0.92)
    else:
        # diff == 0
        scene_type = "unknown"
        confidence = 0.35
        notes.append("スコア同点のため unknown")

    # ── センサーモード別 confidence スケーリング ───────────────────────────
    # color 映像は輝度識別が有効なのでスケーリングなし（factor=1.0）。
    # それ以外は輝度の意味が変わる可能性があるため confidence を低下させる。
    factor = SENSOR_CONFIDENCE_FACTOR.get(sensor_mode, 0.65)
    if factor < 1.0:
        notes.append(
            f"[sensor:{sensor_mode}] 輝度識別を無効化・confidence×{factor:.2f} "
            "（非color映像のため地表/雲判定は暫定）"
        )
        confidence = round(max(0.25, confidence * factor), 3)
    else:
        confidence = round(confidence, 3)

    return scene_type, confidence, score_ground, score_cloud, notes


# ════════════════════════════════════════════════════════════════════════════
# フレーム解析（1枚）
# ════════════════════════════════════════════════════════════════════════════

def analyze_frame(path: Path, sensor_mode_override: str = "auto") -> dict:
    """
    1フレームを解析して特徴量・分類結果を返す。

    sensor_mode_override:
      "auto" のとき自動検出。それ以外の値（"color"/"grayscale"/"ir"/"night_vision"）
      を渡すと検出結果を上書きする。
    """
    rgb  = load_rgb(path)
    gray = to_gray(rgb)
    mask = build_valid_mask(gray)

    masked_ratio = float(1.0 - mask.mean()) if mask.size > 0 else 1.0

    mb   = mean_brightness(gray, mask)
    tv   = texture_variance(gray, mask)
    ed   = sobel_edge_density(gray, mask)
    hf   = spatial_freq_ratio(gray, mask)
    un   = uniformity(gray, mask)
    sm   = (detect_sensor_mode(rgb, mask)
            if sensor_mode_override == "auto"
            else sensor_mode_override)
    lt   = detect_lighting(mb, sm)

    scene_type, conf, sg, sc, notes = classify_scene(mb, tv, ed, hf, un, lt, sm)

    ground_sub = (
        detect_ground_subtype(rgb, mask, sm)
        if scene_type == "ground_surface" else ""
    )

    notes_str = " / ".join(notes) if notes else "—"

    return {
        "scene_type":         scene_type,
        "ground_subtype":     ground_sub,
        "lighting_type":      lt,
        "sensor_mode":        sm,
        "scene_confidence":   conf,
        "mean_brightness":    round(mb, 2),
        "texture_variance":   round(tv, 2),
        "edge_density":       round(ed, 5),
        "spatial_freq_ratio": round(hf, 5),
        "masked_pixel_ratio": round(masked_ratio, 4),
        "scene_notes":        notes_str,
        "_score_ground":      sg,
        "_score_cloud":       sc,
    }


# ════════════════════════════════════════════════════════════════════════════
# フレーム収集
# ════════════════════════════════════════════════════════════════════════════

def collect_frames(d: Path) -> list:
    return sorted(d.glob("frame_*.png"), key=lambda p: p.name)


def ts_from_name(name: str) -> float:
    try:
        stem = Path(name).stem            # "frame_00054" など
        return float(stem.split("_", 1)[1])
    except Exception:
        return 0.0


# ════════════════════════════════════════════════════════════════════════════
# サマリー生成
# ════════════════════════════════════════════════════════════════════════════

def build_summary(results: list, source_id: str, article_id: str,
                  frames_dir: Path) -> str:
    scene_counts = Counter(r["scene_type"] for r in results)
    sub_counts   = Counter(r["ground_subtype"] for r in results if r["ground_subtype"])
    sensor_counts = Counter(r["sensor_mode"] for r in results)
    lighting_counts = Counter(r["lighting_type"] for r in results)

    # 平均特徴量
    mean_edge = float(np.mean([r["edge_density"] for r in results]))
    mean_hf   = float(np.mean([r["spatial_freq_ratio"] for r in results]))
    mean_tv   = float(np.mean([r["texture_variance"] for r in results]))
    mean_conf = float(np.mean([r["scene_confidence"] for r in results]))
    mean_mask = float(np.mean([r["masked_pixel_ratio"] for r in results]))

    # 多数決による最終判定
    most_common_scene = scene_counts.most_common(1)[0][0]
    most_common_sub   = sub_counts.most_common(1)[0][0] if sub_counts else ""

    lines = [
        "# Scene Analyzer Summary",
        "",
        f"- 実行日時   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- article_id : {article_id}",
        f"- source_id  : {source_id}",
        f"- frames_dir : {frames_dir}",
        f"- 分類器     : {VERSION}",
        f"- フレーム数 : {len(results)}",
        "",
        "---",
        "",
        "## 背景種別 集計",
        "",
        "| scene_type | 件数 | 割合 | 説明 |",
        "|-----------|------|------|------|",
    ]
    for st, cnt in scene_counts.most_common():
        pct = cnt / len(results) * 100
        desc = SCENE_DESC.get(st, st)
        lines.append(f"| {st} | {cnt} | {pct:.1f}% | {desc} |")

    lines += [
        "",
        "## 地表サブタイプ（ground_surface フレームのみ）",
        "",
        "| ground_subtype | 件数 |",
        "|---------------|------|",
    ]
    for sub, cnt in sub_counts.most_common():
        lines.append(f"| {sub or '（空白）'} | {cnt} |")
    if not sub_counts:
        lines.append("（該当フレームなし）")

    dominant_sensor = sensor_counts.most_common(1)[0][0]
    sensor_note     = SENSOR_MODE_NOTES.get(dominant_sensor, "")
    provisional     = SENSOR_CLASSIFICATION_PROVISIONAL.get(dominant_sensor, True)

    lines += [
        "",
        "## センサーモード / 照明種別",
        "",
        "| センサーモード | 件数 | 割合 |",
        "|--------------|------|------|",
    ]
    for sm_val, cnt in sensor_counts.most_common():
        pct = cnt / len(results) * 100
        lines.append(f"| {sm_val} | {cnt} | {pct:.1f}% |")

    lines += [
        "",
        "| 照明種別 | 件数 |",
        "|---------|------|",
    ]
    for lt, cnt in lighting_counts.most_common():
        lines.append(f"| {lt} | {cnt} |")

    lines += [
        "",
        "## センサーモード別 判定前提",
        "",
        f"**主要センサーモード: `{dominant_sensor}`**",
        "",
        f"> {sensor_note}",
        "",
    ]
    if provisional:
        lines += [
            "⚠️ **注意（暫定分類）**: このセンサー種別では地表/雲/海の断定は暫定扱いです。",
            "confidence が低下しています。Human review による最終確認を推奨します。",
            "",
            "| 注意事項 | 詳細 |",
            "|---------|------|",
            "| 輝度識別 | 無効化（可視光の明るさに対応しない可能性） |",
            "| 雲/地表判定 | 暫定 |",
            "| confidence | スケール済み（color映像より低値） |",
            "| 対応方法 | `--sensor-mode ir` 等で手動指定後に再実行 |",
            "",
        ]
    else:
        lines += [
            "✅ **カラー映像確認済み**: 輝度による地表/雲識別が有効です。",
            "現在の分類結果は最大信頼度で使用できます。",
            "",
        ]

    lines += [
        "",
        "## 平均特徴量",
        "",
        f"| 特徴量 | 平均値 |",
        f"|-------|--------|",
        f"| edge_density | {mean_edge:.5f} |",
        f"| spatial_freq_ratio | {mean_hf:.5f} |",
        f"| texture_variance | {mean_tv:.2f} |",
        f"| scene_confidence | {mean_conf:.3f} |",
        f"| masked_pixel_ratio | {mean_mask:.3f} |",
        "",
        "---",
        "",
        "## 総合判定（多数決）",
        "",
        f"- **scene_type : {most_common_scene}**（{SCENE_DESC.get(most_common_scene, most_common_scene)}）",
    ]
    if most_common_sub:
        lines.append(f"- ground_subtype : {most_common_sub}")
    lines += [
        f"- lighting_type : {lighting_counts.most_common(1)[0][0]}",
        f"- sensor_mode   : {dominant_sensor}",
    ]
    if provisional:
        lines.append(
            "- ⚠️ **分類は暫定扱い**"
            "（センサー種別により輝度・色の意味が変わる可能性。Human review 推奨）"
        )
    else:
        lines.append("- ✅ 分類信頼度: カラー映像・輝度識別有効")
    lines += [
        "",
        "## PR062 期待値との比較",
        "",
        "| 期待値 | 本結果 | 判定 |",
        "|-------|--------|------|",
        f"| scene_type = ground_surface | {most_common_scene} |"
        f" {'✅' if most_common_scene == 'ground_surface' else '⚠️'} |",
        f"| ground_subtype = rocky/arid | {most_common_sub or '—'} |"
        f" {'✅' if most_common_sub in ('rocky','arid') else '⚠️'} |",
        f"| sensor_mode = color | {sensor_counts.most_common(1)[0][0]} |"
        f" {'✅' if sensor_counts.most_common(1)[0][0] == 'color' else '⚠️'} |",
    ]

    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════════════════
# 引数解析
# ════════════════════════════════════════════════════════════════════════════

def parse_args():
    p = argparse.ArgumentParser(
        description=f"{VERSION} — Scene classification Agent for Media Inspector v4"
    )
    p.add_argument("--frames-dir",  required=True,
                   help="フレーム画像ディレクトリ (frame_*.png)")
    p.add_argument("--source-id",   required=True,
                   help="ソースID（ファイル名スラッグ）")
    p.add_argument("--article-id",  default="UNKNOWN",
                   help="article_id（例: R02-054）")
    p.add_argument("--output-dir",  default="",
                   help="出力先ディレクトリ（省略時は自動生成）")
    p.add_argument("--execute",     action="store_true",
                   help="ファイル出力あり（省略時は dry-run）")
    p.add_argument("--verbose",     action="store_true",
                   help="全フレームの詳細ログを表示")
    p.add_argument(
        "--sensor-mode",
        choices=["auto", "color", "grayscale", "ir", "night_vision", "unknown"],
        default="auto",
        help=(
            "センサーモードを手動指定（デフォルト: auto = 自動検出）。 "
            "IR映像・暗視カメラ等は自動検出不能のため手動指定を推奨。 "
            "例: --sensor-mode ir"
        ),
    )
    return p.parse_args()


# ════════════════════════════════════════════════════════════════════════════
# メイン
# ════════════════════════════════════════════════════════════════════════════

def main():
    args = parse_args()
    frames_dir = Path(args.frames_dir)
    if not frames_dir.exists():
        sys.exit(f"[ERROR] frames_dir が存在しない: {frames_dir}")

    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        run_date = date.today().strftime("%Y%m%d")
        out_dir = (
            Path("data") / "media_inspector_runs"
            / run_date / args.source_id / "scene_analysis"
        )

    frames = collect_frames(frames_dir)
    n = len(frames)
    if n == 0:
        sys.exit("[ERROR] frame_*.png が見つからない")

    sensor_override = args.sensor_mode  # "auto" or explicit mode

    mode_label = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"[{VERSION}] mode={mode_label}")
    print(f"  article_id  : {args.article_id}")
    print(f"  source_id   : {args.source_id}")
    print(f"  frames_dir  : {frames_dir}")
    print(f"  sensor_mode : {sensor_override}")
    print(f"  フレーム数  : {n}")
    print(f"  出力先      : {out_dir}/")
    if sensor_override != "auto" and sensor_override != "color":
        print(f"  ⚠️  非color映像モード: {SENSOR_MODE_NOTES.get(sensor_override, '')[:60]}...")
    print()

    # ── DRY-RUN: 先頭 5 フレームのみプレビュー ─────────────────────────
    if not args.execute:
        print("[DRY-RUN] 先頭 5 フレームをプレビュー...")
        for frm in frames[:5]:
            ts = ts_from_name(frm.name)
            res = analyze_frame(frm, sensor_mode_override=sensor_override)
            sg, sc = res["_score_ground"], res["_score_cloud"]
            print(
                f"  {frm.name}  ts={ts:.0f}s"
                f"  scene={res['scene_type']:<14}"
                f"  sub={res['ground_subtype'] or '—':<8}"
                f"  conf={res['scene_confidence']:.2f}"
                f"  edge={res['edge_density']:.4f}"
                f"  hifreq={res['spatial_freq_ratio']:.4f}"
                f"  tv={res['texture_variance']:.1f}"
                f"  [G{sg}:C{sc}]"
                f"  sensor={res['sensor_mode']}"
            )
        print()
        print(f"[DRY-RUN] 完了。--execute を付けると全 {n} フレームを処理・出力します。")
        return

    # ── EXECUTE ─────────────────────────────────────────────────────────
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    print(f"[1/2] 全フレーム解析中 ({n} フレーム)...")
    for i, frm in enumerate(frames, 1):
        ts  = ts_from_name(frm.name)
        res = analyze_frame(frm, sensor_mode_override=sensor_override)
        res["frame_name"]  = frm.name
        res["timestamp_s"] = ts

        if args.verbose or i % 20 == 0 or i == 1:
            sg, sc = res["_score_ground"], res["_score_cloud"]
            print(
                f"  {i:3d}/{n}: {frm.name}"
                f"  {res['scene_type']:<14}"
                f"  conf={res['scene_confidence']:.2f}"
                f"  edge={res['edge_density']:.4f}"
                f"  hifreq={res['spatial_freq_ratio']:.4f}"
                f"  tv={res['texture_variance']:.1f}"
                f"  [G{sg}:C{sc}]"
            )

        results.append(res)

    print(f"\n[2/2] ファイル出力中...")

    # CSV
    csv_path = out_dir / "scene_frames.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in results:
            w.writerow({k: r[k] for k in CSV_FIELDS})

    # サマリー
    summary_txt = build_summary(results, args.source_id, args.article_id, frames_dir)
    md_path = out_dir / "scene_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(summary_txt)

    # メタデータ JSON
    scene_counts  = Counter(r["scene_type"] for r in results)
    sensor_counts = Counter(r["sensor_mode"] for r in results)
    dom_sensor    = sensor_counts.most_common(1)[0][0]
    meta = {
        "version":                      VERSION,
        "run_date":                     date.today().isoformat(),
        "source_id":                    args.source_id,
        "article_id":                   args.article_id,
        "sensor_mode_override":         sensor_override,
        "n_frames":                     n,
        "scene_majority":               scene_counts.most_common(1)[0][0],
        "scene_counts":                 dict(scene_counts),
        "sensor_mode_majority":         dom_sensor,
        "sensor_mode_counts":           dict(sensor_counts),
        "classification_provisional":   SENSOR_CLASSIFICATION_PROVISIONAL.get(dom_sensor, True),
        "sensor_mode_notes":            SENSOR_MODE_NOTES.get(dom_sensor, ""),
    }
    with open(out_dir / "scene_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # 集計表示
    print()
    scene_counts = Counter(r["scene_type"] for r in results)
    print("[完了] scene_type 集計:")
    for st, cnt in scene_counts.most_common():
        pct = cnt / n * 100
        desc = SCENE_DESC.get(st, st)
        print(f"  {st:<16}: {cnt:3d} 件 ({pct:.1f}%) — {desc}")
    print(f"\n  出力: {out_dir}/")
    print(f"  CSV : {csv_path}")
    print(f"  MD  : {md_path}")


if __name__ == "__main__":
    main()
