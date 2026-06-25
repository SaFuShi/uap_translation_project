#!/usr/bin/env python3
"""
apply_article_template.py — Release 02 VID記事ドラフト テンプレート一括修正 v2

Usage:
  python3 scripts/apply_article_template.py --dry-run
  python3 scripts/apply_article_template.py --dry-run --file DOW-UAP-PR021
  python3 scripts/apply_article_template.py --execute            # dry-run確認後のみ

安全方針:
  - workflow.db / source_registry.csv は変更しない
  - note公開しない / git操作しない
  - --execute 時のみファイル変更（.bak バックアップ付き）
  - published記事・archiveは除外

変換一覧 v2:
  T01  タイトルID        #R02-XXX → #2_XXX                    [AUTO]
  T02  Release Date      ・Release 02 追加                     [AUTO]
  T03  画像プレースホルダー ▼【画像】 + 掲載画像: 行追加         [AUTO+lookup]
  T04  目視確認注釈       標準フレーズ追加/タイムコード付き→標準化 [AUTO]
  T05  ファイル名由来注釈  注釈フレーズ + セクションヘッダー修正   [AUTO]
  T06+T07 ffprobe形式    パイプ区切り→展開箇条書き + intro追加   [AUTO]
  T08  ## 注意点          スケルトン追加                        [AUTO_SKELETON]
  T09  掲載画像出典       代表フレーム: → 掲載画像出典:          [AUTO]
  T10  ディスクレイマー   1行→3段落展開                        [AUTO]
  T11  語尾統一           です・ます調修正                      [AUTO]
  T12  ffprobe残留パイプ  解像度行のパイプ残留を2行分割で修正     [AUTO]  ★v2
  T13  ▲キャプション丁寧体 確認できる→確認できます等             [AUTO]  ★v2
  T14  DVIDS IDメタデータ （DVIDS＝...）→（DoW/DVIDS管理番号）  [AUTO]  ★v2
  T15  DVIDS IDファイル名由来 管理番号注記追加                   [AUTO]  ★v2
  T16  AI解析メモタイムコード Nフレーム→MM:SS列挙               [AUTO]  ★v2
  T17  セパレータ追加     ## 注意点と## 出典の間の---           [AUTO]  ★v2
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ─── 定数 ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(".")
DRAFTS_DIR = PROJECT_ROOT / "note_drafts"
ARCHIVE_DIR = DRAFTS_DIR / "archive"
THUMBS_DIR = PROJECT_ROOT / "thumbnails"
SOURCE_REGISTRY = PROJECT_ROOT / "review_logs" / "source_registry.csv"
REPORTS_DIR = PROJECT_ROOT / "review_reports"

# HOLD/SKIP対象の除外スラグ（先頭マッチ）
EXCLUDED_SLUG_PREFIXES = {
    "DOW-UAP-PR057",
    "DOW-UAP-PR058",
    "DOW-UAP-PR098",
}

STANDARD_VISUAL_ANNOTATION = "以下は映像フレームの目視確認によるものです。"
STANDARD_FILENAME_ANNOTATION = (
    "以下の情報はファイル名およびfiles_catalog.csvメタデータに基づくものです。"
    "映像フレームから直接確認したものではありません。"
)
FFPROBE_INTRO = "ffprobeによる技術情報を以下に示します。"

VERB_FIXES = [
    ("内容は本記事では扱わない",     "内容は本記事では扱いません"),
    ("扱わない。",                   "扱いません。"),
    ("確認できない",                 "確認できません"),
    ("特定できない",                 "特定できません"),
    ("断定できない",                 "断定できません"),
    ("示すものではない",             "示すものではありません"),
    ("確認されていない",             "確認されていません"),
    ("区別できない",                 "区別できません"),
    ("判断できない",                 "判断できません"),
    ("識別できない",                 "識別できません"),
]

DISCLAIMER_FIRST_LINE = (
    "※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。"
)
DISCLAIMER_FULL = """\
※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。

映像内容の判断には不確実性が含まれます。センサー種別・物体の性質・撮影状況の詳細は本映像単体では確認できません。

今後、追加情報・映像内テキスト確認・詳細解析を反映した「詳細解析版」へ更新・再公開する場合があります。

原文リンクを重視し、可能な限り一次ソースを確認できる形で整理しています。"""


# ─── データクラス ─────────────────────────────────────────────────────────────

@dataclass
class Change:
    """単一変換の結果レコード。"""
    transform_id: str
    name: str
    category: str          # AUTO | AUTO_SKELETON | SKIPPED | MANUAL_NOTE
    old_snippet: str = ""
    new_snippet: str = ""


@dataclass
class FileResult:
    path: Path
    slug: str
    changes: list[Change] = field(default_factory=list)
    error: Optional[str] = None
    modified: bool = False

    def count_by(self, category: str) -> int:
        return sum(1 for c in self.changes if c.category == category)

    def will_modify(self) -> bool:
        return any(c.category in ("AUTO", "AUTO_SKELETON") for c in self.changes)


# ─── ヘルパー ─────────────────────────────────────────────────────────────────

def load_published_slugs() -> set[str]:
    published: set[str] = set()
    if not SOURCE_REGISTRY.exists():
        return published
    with open(SOURCE_REGISTRY, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 5 and row[4].strip() == "published":
                # row[1] = ファイル名 (例: DOW-UAP-PR019_....mp4)
                slug = row[1].strip().removesuffix(".mp4").removesuffix(".pdf")
                published.add(slug)
    return published


def extract_slug(path: Path) -> str:
    stem = path.stem  # ai_summary_DOW-UAP-PR021_..._note_version
    return stem.removeprefix("ai_summary_").removesuffix("_note_version")


def get_slug_short(slug: str) -> str:
    """先頭識別子のみ返す (例: DOW-UAP-PR053)"""
    return slug.split("_")[0]


def find_thumbnail_info(slug: str) -> tuple[str, str]:
    """
    サムネイルフレームのパスとスラグ短縮形を返す。
    例: ("thumbnails/DOW-UAP-PR053/frame_0005.png", "DOW-UAP-PR053")
    """
    slug_short = get_slug_short(slug)
    thumbs_dir = PROJECT_ROOT / "thumbnails"

    candidates = sorted(thumbs_dir.glob(f"{slug_short}*/"), key=lambda p: len(p.name), reverse=True)
    if not candidates:
        return f"thumbnails/{slug}/frame_0005.png", slug_short

    thumb_dir = candidates[0]
    for frame_name in ("frame_0005.png", "frame_0000.png"):
        fp = thumb_dir / frame_name
        if fp.exists():
            return str(fp), slug_short
    frames = sorted(thumb_dir.glob("frame_*.png"))
    if frames:
        return str(frames[0]), slug_short
    return f"thumbnails/{slug}/frame_0005.png", slug_short


def get_draft_files(published_slugs: set[str]) -> list[Path]:
    files: list[Path] = []
    for f in sorted(DRAFTS_DIR.glob("ai_summary_*_note_version.md")):
        if ARCHIVE_DIR in f.parents:
            continue
        slug = extract_slug(f)
        if slug in published_slugs:
            continue
        if any(slug.startswith(p) for p in EXCLUDED_SLUG_PREFIXES):
            continue
        if not (slug.startswith("DOW-UAP-PR") or slug.startswith("FBI-UAP-PR")):
            continue
        files.append(f)
    return files


# ─── 変換関数 ─────────────────────────────────────────────────────────────────

def t01_title_id(content: str) -> tuple[str, Change]:
    """#R02-XXX → #2_XXX"""
    pattern = r"(# 【概要版)#R02-(\d{3})(】)"
    if not re.search(pattern, content):
        return content, Change("T01", "タイトルID", "SKIPPED")
    m = re.search(pattern, content)
    old_snip = m.group(0)
    new_content = re.sub(pattern, r"\g<1>#2_\2\g<3>", content, count=1)
    new_snip = old_snip.replace("#R02-", "#2_").replace("0", "", 1) if old_snip else ""
    # 正確な変換後スニペット
    new_snip = re.search(r"(# 【概要版#2_\d{3}】)", new_content)
    new_snip_str = new_snip.group(0) if new_snip else ""
    return new_content, Change("T01", "タイトルID #R02→#2", "AUTO", old_snip, new_snip_str)


def t02_release_date(content: str) -> tuple[str, Change]:
    """Release Dateに「・Release 02」追加"""
    # タイトル行にも「・Release 02」が含まれるため、Release Date行を特定して確認
    OLD_RDATE = "（war.gov/UFO/ にて公開）"
    NEW_RDATE = "（war.gov/UFO/ にて公開・Release 02）"

    if NEW_RDATE in content:
        return content, Change("T02", "Release Date", "SKIPPED")

    if OLD_RDATE not in content:
        return content, Change("T02", "Release Date", "MANUAL_NOTE",
                               "", "「（war.gov/UFO/ にて公開）」が見つかりません。手動確認要。")
    new_content = content.replace(OLD_RDATE, NEW_RDATE, 1)
    return new_content, Change("T02", "Release Date ・Release 02追加", "AUTO", OLD_RDATE, NEW_RDATE)


def t03_image_placeholder(content: str, slug: str) -> tuple[str, Change]:
    """▼【画像】ブロック追加（▲行の前）"""
    if "▼ 【画像】" in content:
        return content, Change("T03", "画像プレースホルダー", "SKIPPED")

    m = re.search(r"^▲ ", content, re.MULTILINE)
    if not m:
        return content, Change("T03", "画像プレースホルダー", "MANUAL_NOTE",
                               "", "▲キャプション行が見つかりません。手動追加要。")

    thumb_path, slug_short = find_thumbnail_info(slug)
    insert_text = (
        f"▼ 【画像】{slug_short} 代表フレーム（映像開始直後・約0秒時点）\n\n"
        f"掲載画像：{thumb_path}（アイキャッチ推奨）\n\n"
    )
    insert_pos = m.start()
    new_content = content[:insert_pos] + insert_text + content[insert_pos:]
    return new_content, Change("T03", "画像プレースホルダー ▼【画像】追加", "AUTO",
                               f"[▲行の直前]", insert_text[:70].rstrip() + "...")


def t04_visual_annotation(content: str) -> tuple[str, Change]:
    """映像フレーム目視確認注釈を標準フレーズへ統一"""
    STANDARD = STANDARD_VISUAL_ANNOTATION
    if STANDARD in content:
        return content, Change("T04", "目視確認注釈", "SKIPPED")

    # タイムコード付きバリアント: 「以下は映像フレーム（0秒・...）の目視確認によるものです。」
    tc_pattern = r"以下は映像フレーム（[^）]+）の目視確認によるものです。"
    m = re.search(tc_pattern, content)
    if m:
        old_str = m.group(0)
        new_content = content.replace(old_str, STANDARD, 1)
        return new_content, Change("T04", "目視確認注釈 タイムコード付き→標準形", "AUTO",
                                   old_str, STANDARD)

    # セクションヘッダーの後に挿入
    section_pat = r"(### 映像から視覚的に確認できる情報[^\n]*\n\n)"
    m = re.search(section_pat, content)
    if not m:
        return content, Change("T04", "目視確認注釈", "MANUAL_NOTE",
                               "", "### 映像から視覚的に確認できる情報セクションが見つかりません。")
    insert_pos = m.end()
    new_content = content[:insert_pos] + STANDARD + "\n\n" + content[insert_pos:]
    return new_content, Change("T04", "目視確認注釈追加", "AUTO", "[セクション直後]", STANDARD)


def t05_filename_annotation(content: str) -> tuple[str, Change]:
    """ファイル名由来注釈フレーズ + セクションヘッダー括弧修正"""
    changes_made: list[str] = []
    new_content = content

    # 1. セクションヘッダー修正（括弧なし → 括弧付き）
    old_hdr = "### ファイル名・メタデータ由来の情報\n"
    new_hdr = "### ファイル名・メタデータ由来の情報（映像フレームでの直接確認なし）\n"
    if old_hdr in new_content and new_hdr not in new_content:
        new_content = new_content.replace(old_hdr, new_hdr, 1)
        changes_made.append("セクションヘッダー括弧追加")

    # 2. 注釈フレーズ確認（2文セットで確認）
    ANNOTATION_KEY1 = "以下の情報はファイル名および"
    ANNOTATION_KEY2 = "映像フレームから直接確認したものではありません。"

    # 1文目あり・2文目なし → 2文目を1文目の末尾に追記
    if ANNOTATION_KEY1 in new_content and ANNOTATION_KEY2 not in new_content:
        pat1 = r"(以下の情報はファイル名および[^\n]+に基づくものです。)(\n)"
        m1 = re.search(pat1, new_content)
        if m1:
            new_content = new_content.replace(
                m1.group(0),
                m1.group(1) + ANNOTATION_KEY2 + m1.group(2),
                1,
            )
            changes_made.append("注釈2文目追加")

    if ANNOTATION_KEY1 not in new_content:
        sec_pat = r"(### ファイル名・メタデータ由来の情報[^\n]*\n\n)"
        m = re.search(sec_pat, new_content)
        if m:
            pos = m.end()
            new_content = (
                new_content[:pos] + STANDARD_FILENAME_ANNOTATION + "\n\n" + new_content[pos:]
            )
            changes_made.append("注釈フレーズ追加")
        else:
            return new_content, Change("T05", "ファイル名由来注釈", "MANUAL_NOTE",
                                       "", "ファイル名由来セクションが見つかりません。")

    if changes_made:
        return new_content, Change("T05", "ファイル名由来注釈 " + "・".join(changes_made), "AUTO", "", "")
    return new_content, Change("T05", "ファイル名由来注釈", "SKIPPED")


def _parse_pipe_fields(line: str) -> dict[str, str]:
    """「- key：value | key2：value2」形式をパース（空白なしパイプも対応）"""
    content = re.sub(r"^- ", "", line.strip())
    fields: dict[str, str] = {}
    for part in re.split(r"\s*\|\s*", content):
        if "：" in part:
            key, _, val = part.partition("：")
            fields[key.strip()] = val.strip()
    return fields


def _frame_to_timecode(frame_name: str) -> str:
    """frame_0005.png → '00:05'（ファイル名の数字 = 秒数）"""
    m = re.search(r"frame_(\d+)\.png", frame_name)
    if not m:
        return "??"
    secs = int(m.group(1))
    return f"{secs // 60:02d}:{secs % 60:02d}"


def t06_t07_ffprobe(content: str) -> tuple[str, Change]:
    """ffprobe: intro句追加 + パイプ区切り→展開箇条書き変換"""
    has_intro = FFPROBE_INTRO in content
    # パイプ区切り行の検出: 「- コンテナ：... | 解像度：...」
    PIPE_PAT = r"(- コンテナ：[^\n]+ \| [^\n]+\n)(- 再生時間：[^\n]+\n)"
    pipe_m = re.search(PIPE_PAT, content)

    if has_intro and not pipe_m:
        return content, Change("T06+T07", "ffprobe形式", "SKIPPED")

    changes_made: list[str] = []
    new_content = content

    if pipe_m:
        line1 = pipe_m.group(1).rstrip("\n")
        line2 = pipe_m.group(2).rstrip("\n")
        fields: dict[str, str] = {}
        fields.update(_parse_pipe_fields(line1))
        fields.update(_parse_pipe_fields(line2))

        container  = fields.get("コンテナ", "MP4")
        resolution = fields.get("解像度", "")
        fps        = fields.get("フレームレート", "")
        duration   = fields.get("再生時間", "")
        bitrate    = fields.get("ビットレート", "")
        size       = fields.get("ファイルサイズ", "")
        audio      = fields.get("音声", "AAC")

        # 解像度にアスペクト比追加（FHD が含まれ未追加の場合）
        if resolution and "FHD" in resolution and "アスペクト比" not in resolution:
            resolution = resolution.rstrip("）") + "・アスペクト比 16:9）"

        # ビットレートに「約」追加
        if bitrate and not bitrate.startswith("約"):
            bitrate = f"約{bitrate}"

        codec = "H.264 / AVC"

        new_block_lines: list[str] = []
        if not has_intro:
            new_block_lines += [FFPROBE_INTRO, ""]
        new_block_lines += [f"- コンテナ：{container}", f"- 映像コーデック：{codec}"]
        if resolution:
            new_block_lines.append(f"- 解像度：{resolution}")
        if fps:
            new_block_lines.append(f"- フレームレート：{fps}")
        if duration:
            new_block_lines.append(f"- 再生時間：{duration}")
        if bitrate:
            new_block_lines.append(f"- ビットレート：{bitrate}")
        new_block_lines.append(f"- 音声コーデック：{audio}（音声内容は本記事では確認対象外）")
        if size:
            new_block_lines.append(f"- ファイルサイズ：{size}")

        new_block = "\n".join(new_block_lines) + "\n"
        old_block = pipe_m.group(0)
        new_content = new_content.replace(old_block, new_block, 1)
        changes_made.append("パイプ区切り→展開箇条書き変換")
        if not has_intro:
            changes_made.append("intro追加")

    elif not has_intro:
        # 展開済みだがintroなし → introのみ追加
        sec_pat = r"(### 映像メタデータ（ffprobe解析より）\n\n)"
        m = re.search(sec_pat, new_content)
        if m:
            pos = m.end()
            new_content = new_content[:pos] + FFPROBE_INTRO + "\n\n" + new_content[pos:]
            changes_made.append("intro追加")

    if changes_made:
        return new_content, Change("T06+T07", "ffprobe " + "・".join(changes_made), "AUTO", "", "")
    return new_content, Change("T06+T07", "ffprobe形式", "SKIPPED")


def _extract_filename_terms(content: str, slug: str) -> str:
    """注意点スケルトン用: ファイル名由来語句を抽出"""
    terms: list[str] = []
    if "Unresolved" in slug:
        terms.append("Unresolved（未解決）")
    m = re.search(r"\*\*Related Location：\*\*\s+([^（\n（f]+?)（", content)
    if m:
        loc = m.group(1).strip().rstrip("（").strip()
        if loc:
            terms.append(loc)
    m2 = re.search(r"\*\*Incident Date：\*\*\s+([^（\n]+?)（", content)
    if m2:
        date = m2.group(1).strip()
        if date:
            terms.append(date)
    if terms:
        return "".join(f"「{t}」" for t in terms)
    return "ファイル名由来の地域・日時・事案分類"


def t08_caution_section(content: str, slug: str) -> tuple[str, Change]:
    """## 注意点 スケルトン追加"""
    if "## 注意点" in content:
        return content, Change("T08", "## 注意点", "SKIPPED")

    agency_label = "DoWが公開した" if slug.startswith("FBI-UAP-") else "DoWが付与した"
    filename_terms = _extract_filename_terms(content, slug)

    skeleton = (
        "## 注意点\n"
        "\n"
        "**物体の正体・種別について**\n"
        "本映像内でUAPとされる対象物は、抽出フレームでは明確に識別できませんでした。"
        "「UAP」「Unresolved」はファイル名に付与された分類名称であり、物体の正体・性質を示すものではありません。\n"
        "\n"
        "**ファイル名情報の位置付けについて**\n"
        f"{filename_terms}はすべて{agency_label}ファイル名由来の情報です。"
        "映像フレーム内に対応する地名・タイムスタンプ等の文字情報は確認されておらず、"
        "事実の出典はファイル名に限定されます。\n"
        "\n"
        "**IR映像の判断について**\n"
        "映像はグレースケールでIRセンサー映像の特徴を示しますが、"
        "フレーム内にセンサー種別を示す表示は確認されていません。"
        "本記事では「IR映像と推定」と記述します。\n"
        "\n"
        "**映像の撮影状況・プラットフォームについて**\n"
        "撮影したプラットフォーム・機材・乗員の観察記録等は本映像単体では確認できません。"
        "コールサインは黒塗りです。\n"
        "\n"
    )

    # ## 出典 の前に挿入
    if "## 出典" in content:
        new_content = content.replace("## 出典", skeleton + "## 出典", 1)
        return new_content, Change("T08", "## 注意点 スケルトン追加", "AUTO_SKELETON",
                                   "[## 出典の前]", skeleton[:80] + "...")

    # ディスクレイマー行の前に挿入
    m = re.search(r"\n---\n\n※ 本記事は", content)
    if m:
        pos = m.start() + 1
        new_content = content[:pos] + "\n" + skeleton + content[pos:]
        return new_content, Change("T08", "## 注意点 スケルトン追加", "AUTO_SKELETON",
                                   "[ディスクレイマー前]", skeleton[:80] + "...")

    return content, Change("T08", "## 注意点", "MANUAL_NOTE",
                           "", "## 出典セクションが見つかりません。手動追加要。")


def t09_source_citation(content: str, slug: str) -> tuple[str, Change]:
    """代表フレーム: → 掲載画像出典: に統一"""
    if "掲載画像出典：" in content:
        return content, Change("T09", "掲載画像出典", "SKIPPED")

    # 「- 代表フレーム：thumbnails/PATH.png（追加情報）」形式
    pattern = r"- 代表フレーム：thumbnails/[^\n]+\.png([^\n]*)"
    m = re.search(pattern, content)
    if not m:
        return content, Change("T09", "掲載画像出典", "MANUAL_NOTE",
                               "", "「代表フレーム：thumbnails/」行が見つかりません。")

    old_line = m.group(0)
    extra_info = m.group(1).strip()

    if extra_info:
        # 既存のタイムコード情報を活用（例: 「（5秒時点）」→「（約5秒時点）」）
        new_line = f"- 掲載画像出典：{slug}.mp4 より抽出{extra_info}"
    else:
        new_line = f"- 掲載画像出典：{slug}.mp4 より抽出（約0秒時点）"

    new_content = content.replace(old_line, new_line, 1)
    return new_content, Change("T09", "掲載画像出典 代表フレーム→掲載画像出典", "AUTO",
                               old_line, new_line)


def t10_disclaimer(content: str) -> tuple[str, Change]:
    """ディスクレイマーを3段落形式へ展開・欠落段落を補完"""
    PARA2_KEY = "映像内容の判断には不確実性が含まれます。"
    PARA3_KEY = "今後、追加情報"
    PARA4_KEY = "原文リンクを重視し"
    FOOTER_PAT = r"\n---\n\n📋 \*\*article_id"

    PARA3_TEXT = (
        "今後、追加情報・映像内テキスト確認・詳細解析を反映した"
        "「詳細解析版」へ更新・再公開する場合があります。"
    )
    PARA4_TEXT = "原文リンクを重視し、可能な限り一次ソースを確認できる形で整理しています。"

    # 完全準拠: 4段落すべて存在
    if PARA4_KEY in content:
        return content, Change("T10", "ディスクレイマー", "SKIPPED")

    # 部分準拠: para2 存在 → 欠落段落を article_id footerの前に補完
    if PARA2_KEY in content:
        missing_parts: list[str] = []
        if PARA3_KEY not in content:
            missing_parts.append(PARA3_TEXT)
        missing_parts.append(PARA4_TEXT)

        fm = re.search(FOOTER_PAT, content)
        if fm:
            insert_pos = fm.start()
            append_text = "".join(f"\n\n{p}" for p in missing_parts)
            new_content = content[:insert_pos] + append_text + content[insert_pos:]
            label = "・".join([p[:15] + "…" for p in missing_parts])
            return new_content, Change("T10", f"ディスクレイマー 欠落段落補完（{label}）", "AUTO", "", "")
        return content, Change("T10", "ディスクレイマー", "MANUAL_NOTE",
                               "", "フッターが見つかりません。手動追加要。")

    # 1行形式のディスクレイマー行を展開
    pattern = (
        r"※ 本記事はAI映像解析・ffprobe技術情報・フレーム目視確認を用いた「AI概要版」です。[^\n]*"
    )
    m = re.search(pattern, content)
    if m:
        old_str = m.group(0)
        new_content = content.replace(old_str, DISCLAIMER_FULL, 1)
        return new_content, Change("T10", "ディスクレイマー 3段落展開", "AUTO",
                                   old_str[:60] + "...", DISCLAIMER_FULL[:60] + "...")

    # ディスクレイマー行が完全欠落 → article_id footerの前に追加
    fm = re.search(FOOTER_PAT, content)
    if fm:
        insert_pos = fm.start() + 1
        insert_text = "\n---\n\n" + DISCLAIMER_FULL + "\n"
        new_content = content[:insert_pos] + insert_text + content[insert_pos:]
        return new_content, Change("T10", "ディスクレイマー 新規追加（欠落）", "AUTO",
                                   "[article_id行の前]", DISCLAIMER_FULL[:60] + "...")

    return content, Change("T10", "ディスクレイマー", "MANUAL_NOTE",
                           "", "article_id footerも見つかりません。手動追加要。")


def t11_verb_endings(content: str) -> tuple[str, Change]:
    """語尾をです・ます調へ統一"""
    fixes_applied: list[str] = []
    new_content = content

    for old, new in VERB_FIXES:
        if old in new_content:
            new_content = new_content.replace(old, new)
            fixes_applied.append(f"{old}→{new}")

    if fixes_applied:
        summary = "、".join(fixes_applied[:3]) + ("…" if len(fixes_applied) > 3 else "")
        return new_content, Change("T11", f"語尾統一（{len(fixes_applied)}箇所）", "AUTO",
                                   summary, "→ です・ます調")
    return content, Change("T11", "語尾統一", "SKIPPED")


def t12_ffprobe_pipe_repair(content: str) -> tuple[str, Change]:
    """ffprobe残留パイプ修正: 解像度行に残ったパイプ区切りを2行に分割"""
    # Pattern: - 解像度：X（FHD）| フレームレート：Yfps・アスペクト比 Z:W）
    pattern = (
        r"^(- 解像度：[^（\n]+)（(\w+)）\s*\|\s*(フレームレート：[^\n・]+)"
        r"・アスペクト比 ([^\）\n]+)）$"
    )
    m = re.search(pattern, content, re.MULTILINE)
    if not m:
        return content, Change("T12", "ffprobe残留パイプ修正", "SKIPPED")

    old_line = m.group(0)
    res_part = f"{m.group(1)}（{m.group(2)}・アスペクト比 {m.group(4)}）"
    fps_part = f"- {m.group(3)}"
    new_block = f"{res_part}\n{fps_part}"
    new_content = content.replace(old_line, new_block, 1)
    return new_content, Change(
        "T12", "ffprobe残留パイプ修正", "AUTO",
        old_line[:80], new_block[:80].replace("\n", "↩"),
    )


def t13_image_caption_polite(content: str) -> tuple[str, Change]:
    """▲キャプション行の普通体をです・ます調へ変換（文末述語のみ対象）

    連体修飾節（〜とみられる名詞）は平常体のまま維持するため
    `みられる` パターンは変換対象から除外する。
    文末述語のみを丁寧体へ変換する。
    """
    # 文末(。の直前)のみ対象とするパターン
    CAPTION_FIXES = [
        ("確認できる。", "確認できます。"),
        ("広がっている。", "広がっています。"),
        ("伴っている。", "伴っています。"),
    ]

    lines = content.split("\n")
    changed_count = 0
    new_lines: list[str] = []
    for line in lines:
        if line.startswith("▲ "):
            new_line = line
            for old, new in CAPTION_FIXES:
                new_line = new_line.replace(old, new)
            if new_line != line:
                changed_count += 1
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if changed_count:
        return "\n".join(new_lines), Change(
            "T13", f"▲キャプション丁寧体変換（{changed_count}行）", "AUTO", "", "確認できます等",
        )
    return content, Change("T13", "▲キャプション丁寧体", "SKIPPED")


def t14_dvids_id_metadata(content: str) -> tuple[str, Change]:
    """メタデータ行のDVIDS ID注記を統一: （DVIDS＝...）→（DoW/DVIDS管理番号）"""
    OLD = "（DVIDS＝国防映像情報配信サービス）"
    NEW = "（DoW/DVIDS管理番号）"
    if OLD not in content:
        return content, Change("T14", "DVIDS ID メタデータ統一", "SKIPPED")
    new_content = content.replace(OLD, NEW)
    return new_content, Change("T14", "DVIDS ID メタデータ統一", "AUTO", OLD, NEW)


def t15_dvids_id_filename_section(content: str) -> tuple[str, Change]:
    """ファイル名由来セクションのDVIDS ID行に（DoW/DVIDS管理番号）を追加"""
    SUFFIX = "（DoW/DVIDS管理番号）"
    # - DVIDS ID：XXXXXXX（末尾が数字のみ＝注記なし）
    pattern = r"^- DVIDS ID：(\d+)$"
    m = re.search(pattern, content, re.MULTILINE)
    if not m:
        return content, Change("T15", "DVIDS ID ファイル名由来", "SKIPPED")
    old_line = m.group(0)
    new_line = f"- DVIDS ID{SUFFIX}：{m.group(1)}"
    new_content = content.replace(old_line, new_line, 1)
    return new_content, Change("T15", "DVIDS ID ファイル名由来 統一", "AUTO", old_line, new_line)


def t16_ai_memo_timecodes(content: str, slug: str) -> tuple[str, Change]:
    """AI解析メモのフレーム数表記をタイムコード列挙に変換"""
    FRAME_PAT = r"映像フレーム目視確認済み（(\d+)フレーム）"
    m = re.search(FRAME_PAT, content)
    if not m:
        return content, Change("T16", "AI解析メモ タイムコード", "SKIPPED")

    slug_short = get_slug_short(slug)
    thumbs_dir = PROJECT_ROOT / "thumbnails"
    candidates = sorted(
        thumbs_dir.glob(f"{slug_short}*/"), key=lambda p: len(p.name), reverse=True
    )
    if not candidates:
        return content, Change(
            "T16", "AI解析メモ タイムコード", "MANUAL_NOTE",
            m.group(0), "サムネイルフォルダが見つかりません。手動確認要。",
        )

    frames = sorted(candidates[0].glob("frame_*.png"))
    if not frames:
        return content, Change(
            "T16", "AI解析メモ タイムコード", "MANUAL_NOTE",
            m.group(0), "フレームファイルが見つかりません。手動確認要。",
        )

    timecodes = [_frame_to_timecode(f.name) for f in frames]
    old_str = m.group(0)
    new_str = f"映像フレーム目視確認済み（{'・'.join(timecodes)}）"
    new_content = content.replace(old_str, new_str, 1)
    return new_content, Change("T16", "AI解析メモ タイムコード変換", "AUTO", old_str, new_str)


def t17_separator_before_source(content: str) -> tuple[str, Change]:
    """## 注意点 と ## 出典 の間にセパレータ（---）を補完"""
    GOOD = "\n---\n\n## 出典\n"
    BAD  = "\n\n## 出典\n"
    if GOOD in content:
        return content, Change("T17", "セパレータ（注意点→出典）", "SKIPPED")
    if BAD in content:
        new_content = content.replace(BAD, "\n\n---\n\n## 出典\n", 1)
        return new_content, Change("T17", "セパレータ追加（注意点→出典）", "AUTO",
                                   "↩↩## 出典↩", "↩↩---↩↩## 出典↩")
    return content, Change("T17", "セパレータ（注意点→出典）", "MANUAL_NOTE",
                           "", "## 出典前のパターンが不明。手動確認要。")


def t18_revert_mirareru_relative_clause(content: str) -> tuple[str, Change]:
    """▲キャプション内で誤変換されたとみられます（連体修飾節）をとみられるへ戻す

    T13 v1の誤適用で「とみられる名詞」→「とみられます名詞」に変換された
    連体修飾節を正しい平常体（とみられる）に差し戻す。

    保持する正しい用法: とみられますが / とみられます。 / とみられます） / とみられます（
    差し戻す誤用法: とみられます + 名詞（漢字・カタカナ・ひらがな名詞等）
    """
    # とみられますの後が句読点・接続詞が・括弧でない = 連体修飾節（誤変換）
    REVERT_PAT = r"とみられます(?=[^。、！？」\nが）（])"
    lines = content.split("\n")
    changed_count = 0
    new_lines: list[str] = []
    for line in lines:
        if line.startswith("▲ "):
            new_line = re.sub(REVERT_PAT, "とみられる", line)
            if new_line != line:
                changed_count += 1
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if changed_count:
        return "\n".join(new_lines), Change(
            "T18", f"とみられます連体修飾節を差し戻し（{changed_count}行）", "AUTO",
            "とみられます+名詞", "→ とみられる+名詞",
        )
    return content, Change("T18", "とみられます差し戻し", "SKIPPED")


# ─── ファイル処理 ─────────────────────────────────────────────────────────────

def process_file(path: Path, dry_run: bool) -> FileResult:
    slug = extract_slug(path)
    result = FileResult(path=path, slug=slug)

    try:
        original = path.read_text(encoding="utf-8")
    except Exception as e:
        result.error = f"読み込みエラー: {e}"
        return result

    content = original

    # 変換を順番に適用
    transforms = [
        ("T01",      lambda c: t01_title_id(c)),
        ("T02",      lambda c: t02_release_date(c)),
        ("T03",      lambda c: t03_image_placeholder(c, slug)),
        ("T04",      lambda c: t04_visual_annotation(c)),
        ("T05",      lambda c: t05_filename_annotation(c)),
        ("T06+T07",  lambda c: t06_t07_ffprobe(c)),
        ("T12",      lambda c: t12_ffprobe_pipe_repair(c)),
        ("T08",      lambda c: t08_caution_section(c, slug)),
        ("T09",      lambda c: t09_source_citation(c, slug)),
        ("T10",      lambda c: t10_disclaimer(c)),
        ("T11",      lambda c: t11_verb_endings(c)),
        ("T13",      lambda c: t13_image_caption_polite(c)),
        ("T14",      lambda c: t14_dvids_id_metadata(c)),
        ("T15",      lambda c: t15_dvids_id_filename_section(c)),
        ("T16",      lambda c: t16_ai_memo_timecodes(c, slug)),
        ("T17",      lambda c: t17_separator_before_source(c)),
        ("T18",      lambda c: t18_revert_mirareru_relative_clause(c)),
    ]

    for _t_id, fn in transforms:
        try:
            content, change = fn(content)
            result.changes.append(change)
        except Exception as e:
            result.changes.append(Change(_t_id, _t_id, "MANUAL_NOTE",
                                         "", f"変換エラー: {e}"))

    if content != original:
        result.modified = True
        if not dry_run:
            bak_path = path.with_suffix(".md.bak")
            bak_path.write_text(original, encoding="utf-8")
            path.write_text(content, encoding="utf-8")

    return result


# ─── レポート生成 ─────────────────────────────────────────────────────────────

def generate_report(results: list[FileResult], mode: str, date_str: str = "2026-06-24") -> str:
    total = len(results)
    will_mod = sum(1 for r in results if r.modified)
    no_change = sum(1 for r in results if not r.modified and not r.error)
    errors = sum(1 for r in results if r.error)

    # 変換別カウント
    t_counts: dict[str, dict[str, int]] = {}
    t_ids = [
        "T01", "T02", "T03", "T04", "T05", "T06+T07",
        "T12", "T08", "T09", "T10", "T11",
        "T13", "T14", "T15", "T16", "T17", "T18",
    ]
    for tid in t_ids:
        t_counts[tid] = {"AUTO": 0, "AUTO_SKELETON": 0, "SKIPPED": 0, "MANUAL_NOTE": 0}
    for r in results:
        for c in r.changes:
            tid = c.transform_id
            if tid not in t_counts:
                t_counts[tid] = {"AUTO": 0, "AUTO_SKELETON": 0, "SKIPPED": 0, "MANUAL_NOTE": 0}
            cat = c.category
            if cat in t_counts[tid]:
                t_counts[tid][cat] += 1

    total_auto = sum(v["AUTO"] for v in t_counts.values())
    total_skel = sum(v["AUTO_SKELETON"] for v in t_counts.values())
    total_manual = sum(v["MANUAL_NOTE"] for v in t_counts.values())

    lines: list[str] = [
        f"# apply_article_template.py — {mode}レポート",
        "",
        f"**実行日：** {date_str}  ",
        f"**モード：** {mode}  ",
        f"**対象ディレクトリ：** `note_drafts/`  ",
        "",
        "## サマリー",
        "",
        "| 項目 | 件数 |",
        "|---|---|",
        f"| 対象ファイル総数 | {total} |",
        f"| 修正予定ファイル数 | {will_mod} |",
        f"| 修正不要ファイル数（既準拠） | {no_change} |",
        f"| エラー | {errors} |",
        f"| AUTO変換延べ件数 | {total_auto} |",
        f"| AUTO_SKELETON延べ件数 | {total_skel} |",
        f"| 手動確認必要延べ件数 | {total_manual} |",
        "",
    ]

    if mode == "DRY-RUN":
        lines += [
            "> ⚠️ **DRY-RUNモード**：ファイルは変更されていません。",
            "> `--execute` で実行すると上記件数のファイルが修正されます（.bakバックアップ付き）。",
            "",
        ]

    # 変換別集計表
    lines += [
        "## 変換内容別集計",
        "",
        "| 変換ID | 変換名 | AUTO/SKELETON | SKIPPED | MANUAL_NOTE |",
        "|---|---|---|---|---|",
    ]
    T_NAMES = {
        "T01": "タイトルID #R02→#2",
        "T02": "Release Date ・Release 02追加",
        "T03": "画像プレースホルダー ▼【画像】",
        "T04": "目視確認注釈",
        "T05": "ファイル名由来注釈",
        "T06+T07": "ffprobe形式変換+intro追加",
        "T12": "ffprobe残留パイプ修正 [v2]",
        "T08": "## 注意点 スケルトン",
        "T09": "掲載画像出典統一",
        "T10": "ディスクレイマー3段落展開",
        "T11": "語尾統一（です・ます調）",
        "T13": "▲キャプション丁寧体変換 [v2]",
        "T14": "DVIDS IDメタデータ統一 [v2]",
        "T15": "DVIDS IDファイル名由来統一 [v2]",
        "T16": "AI解析メモタイムコード変換 [v2]",
        "T17": "セパレータ追加（注意点→出典） [v2]",
        "T18": "とみられます連体修飾節差し戻し [v2fix]",
    }
    for tid in t_ids:
        c = t_counts.get(tid, {})
        auto_n = c.get("AUTO", 0) + c.get("AUTO_SKELETON", 0)
        skip_n = c.get("SKIPPED", 0)
        manual_n = c.get("MANUAL_NOTE", 0)
        name = T_NAMES.get(tid, tid)
        lines.append(f"| {tid} | {name} | {auto_n} | {skip_n} | {manual_n} |")
    lines.append("")

    # 手動確認必要項目
    manual_files = [r for r in results if r.count_by("MANUAL_NOTE") > 0]
    if manual_files:
        lines += ["## 手動確認が必要な項目", ""]
        for r in manual_files:
            manual_changes = [c for c in r.changes if c.category == "MANUAL_NOTE"]
            lines.append(f"### `{r.slug}`")
            for c in manual_changes:
                lines.append(f"- ⚠️ [{c.transform_id}] {c.name}: {c.new_snippet}")
            lines.append("")
    else:
        lines += ["## 手動確認が必要な項目", "", "なし", ""]

    # エラー
    error_files = [r for r in results if r.error]
    if error_files:
        lines += ["## エラー", ""]
        for r in error_files:
            lines.append(f"- `{r.path.name}`: {r.error}")
        lines.append("")

    # 全ファイルサマリー表
    lines += [
        "## 全ファイル変換サマリー",
        "",
        "| スラグ | AUTO | SKEL | MANUAL | SKIP | 修正予定 |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        auto_n = r.count_by("AUTO")
        skel_n = r.count_by("AUTO_SKELETON")
        manual_n = r.count_by("MANUAL_NOTE")
        skip_n = r.count_by("SKIPPED")
        mark = "✅ 修正" if r.modified else ("❌ ERROR" if r.error else "➖ 変更なし")
        lines.append(f"| `{r.slug}` | {auto_n} | {skel_n} | {manual_n} | {skip_n} | {mark} |")
    lines.append("")

    # ファイル別変換詳細（AUTO/SKELETON/MANUAL のみ、SKIPは省略）
    lines += ["## ファイル別変換詳細", ""]
    for r in results:
        notable = [c for c in r.changes if c.category != "SKIPPED"]
        if not notable and not r.error:
            continue
        lines.append(f"### `{r.slug}`")
        if r.error:
            lines.append(f"❌ エラー: {r.error}")
            lines.append("")
            continue
        for c in notable:
            icon = "🔧" if c.category == "AUTO" else ("📋" if c.category == "AUTO_SKELETON" else "⚠️")
            lines.append(f"- {icon} [{c.transform_id}] **{c.name}**")
            if c.old_snippet and c.category not in ("MANUAL_NOTE",):
                old_disp = c.old_snippet[:90].replace("\n", "↩")
                new_disp = c.new_snippet[:90].replace("\n", "↩")
                if old_disp:
                    lines.append(f"  - 変更前: `{old_disp}`")
                if new_disp:
                    lines.append(f"  - 変更後: `{new_disp}`")
        lines.append("")

    return "\n".join(lines) + "\n"


# ─── メイン ──────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Release 02 VID記事ドラフト テンプレート一括修正"
    )
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--dry-run", action="store_true",
                            help="変更内容を確認のみ（ファイル変更なし）")
    mode_group.add_argument("--execute", action="store_true",
                            help="変更を実際に適用（.bakバックアップ付き）")
    parser.add_argument("--report", metavar="PATH",
                        help="レポートファイルの出力先（省略時は標準出力のみ）")
    parser.add_argument("--file", metavar="SLUG",
                        help="特定ファイルのみ処理（例: DOW-UAP-PR021）")
    parser.add_argument("--verbose", action="store_true",
                        help="詳細ログを表示")
    args = parser.parse_args()

    if not DRAFTS_DIR.is_dir():
        sys.exit("[ERROR] note_drafts/ が見つかりません。プロジェクトルートから実行してください。")

    mode = "DRY-RUN" if args.dry_run else "EXECUTE"
    print(f"\n[apply_article_template.py] mode={mode}")

    published_slugs = load_published_slugs()
    print(f"  公開済みスラグ: {len(published_slugs)}件を除外対象として読み込みました")

    draft_files = get_draft_files(published_slugs)

    if args.file:
        # 特定ファイルのみ
        draft_files = [f for f in draft_files if args.file in f.name]
        if not draft_files:
            sys.exit(f"[ERROR] --file '{args.file}' に一致するドラフトが見つかりません。")

    print(f"  処理対象ファイル: {len(draft_files)}件")
    if args.execute:
        print(f"  ⚠️  EXECUTEモード：ファイルを修正します（.bakバックアップ付き）")

    results: list[FileResult] = []
    for path in draft_files:
        result = process_file(path, dry_run=args.dry_run)
        results.append(result)
        if args.verbose:
            auto_n = result.count_by("AUTO") + result.count_by("AUTO_SKELETON")
            status = "MODIFY" if result.modified else ("ERROR" if result.error else "NO_CHANGE")
            print(f"  [{status}] {result.slug} AUTO:{auto_n}")

    # サマリー出力
    will_mod = sum(1 for r in results if r.modified)
    total_auto = sum(r.count_by("AUTO") + r.count_by("AUTO_SKELETON") for r in results)
    total_manual = sum(r.count_by("MANUAL_NOTE") for r in results)
    errors = sum(1 for r in results if r.error)

    print(f"\n  ── 結果サマリー ──")
    print(f"  対象ファイル:       {len(results)}件")
    print(f"  修正{'実施' if args.execute else '予定'}ファイル:     {will_mod}件")
    print(f"  変更なし:           {len(results) - will_mod - errors}件")
    print(f"  AUTO変換延べ:       {total_auto}件")
    print(f"  手動確認必要:       {total_manual}件")
    print(f"  エラー:             {errors}件")

    # レポート生成
    report_text = generate_report(results, mode)

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_text, encoding="utf-8")
        print(f"\n  レポート出力: {report_path}")
    else:
        print("\n" + "=" * 60)
        print(report_text[:3000])
        if len(report_text) > 3000:
            print(f"... (省略: {len(report_text) - 3000}文字)")

    if args.dry_run:
        print(f"\n  [DRY-RUN完了] ファイルは変更されていません。")
        print(f"  確認後、--execute で実際に適用できます。")
    else:
        print(f"\n  [EXECUTE完了] {will_mod}件のファイルを修正しました。")

    print()


if __name__ == "__main__":
    main()
