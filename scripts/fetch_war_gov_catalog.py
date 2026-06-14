"""
fetch_war_gov_catalog.py
========================
UAP公開文書 翻訳・要約プロジェクト — WAR.GOV/UFO カタログ取得ツール

目的:
    https://www.war.gov/UFO/ に掲載されている公開ファイル一覧を取得し、
    metadata/files_catalog.csv へ保存する。
    また、未取得のファイルをダウンロードして各メディアディレクトリへ保存する。

保存先:
    PDF  → raw_pdf/
    VID  → raw_media/video/  （DVIDS 経由で CloudFront MP4 を取得）
    AUD  → raw_media/audio/  （DVIDS 経由。実体はMP4、notes に記録）
    IMG  → raw_media/image/  （DVIDS ID 有りの場合のみ。無しは metadata_only）

metadata v2 追加列（Release 02 対応）:
    content_category, media_available, ocr_status, article_priority,
    reader_interest, risk_level, note_series, download_scope,
    human_review_required
    → 初期値は保守的な自動推定のみ。article_priority 等の判断は人間レビューが必要。

履歴管理列（metadata v3 追加）:
    first_downloaded_at — 初回取得日時。一度設定されたら上書きしない。
    last_verified_at    — 最終確認日時。ファイル存在確認のたびに更新。
    downloaded_at       — 後方互換のため残存（last_verified_at と同値）。

ページ構造調査結果（2026-05-11）:
    - ページ本体は Akamai WAF で保護。通常の User-Agent では 403。
    - Sec-Fetch-* ヘッダーと Accept-Encoding を含めることで200が返る。
    - ファイル一覧データは /Portals/1/Interactive/2026/UFO/uap-csv.csv に集約。
    - CSVは Sec-Fetch-Mode: cors + Referer: https://www.war.gov/UFO/ で取得可能。
    - PDFダウンロードURLは /medialink/ufo/release_1/*.pdf 形式だが、
      このパスは Akamai WAF により全ヘッダー組み合わせで 403 となる。
      手動でブラウザからダウンロードする必要がある。

運用フロー:
    1. このツールでカタログを取得・更新する
    2. downloaded=false のPDFをブラウザで手動DL → raw_pdf/ へ保存
    3. 再度このツールを実行すると downloaded=true に更新される

実行方法:
    python3 scripts/fetch_war_gov_catalog.py

必要ライブラリ:
    pip3 install requests
"""

import csv
import io
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("=" * 60)
    print("[エラー] requests がインストールされていません。")
    print("  pip3 install requests")
    print("=" * 60)
    sys.exit(1)

# -------------------------------------------------------
# パス設定
# -------------------------------------------------------
PROJECT_ROOT  = Path(__file__).resolve().parent.parent
RAW_PDF_DIR   = PROJECT_ROOT / "raw_pdf"
RAW_MEDIA_DIR = PROJECT_ROOT / "raw_media"
RAW_VIDEO_DIR = RAW_MEDIA_DIR / "video"
RAW_AUDIO_DIR = RAW_MEDIA_DIR / "audio"
RAW_IMAGE_DIR = RAW_MEDIA_DIR / "image"
METADATA_DIR  = PROJECT_ROOT / "metadata"
OUTPUT_CSV    = METADATA_DIR / "files_catalog.csv"

# -------------------------------------------------------
# WAR.GOV 設定
# -------------------------------------------------------
BASE_URL       = "https://www.war.gov"
CATALOG_CSV_PATH = "/Portals/1/Interactive/2026/UFO/uap-data.csv"
CATALOG_CSV_URL  = BASE_URL + CATALOG_CSV_PATH
REFERER_URL      = BASE_URL + "/UFO/"

# ローカルキャッシュパス
# 成功取得時に保存し、WAFブロック時のフォールバックとして使用する
CATALOG_CACHE    = METADATA_DIR / "uap-csv-cache.csv"

# Akamai WAF を通過するための必須ヘッダー
# 調査結果: Sec-Fetch-* ヘッダーがないと 403 になる
PAGE_HEADERS = {
    "User-Agent":      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36",
    "Accept":          "text/html,application/xhtml+xml,application/xml;"
                       "q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Dest":  "document",
    "Sec-Fetch-Mode":  "navigate",
    "Sec-Fetch-Site":  "none",
    "Sec-Fetch-User":  "?1",
    "Upgrade-Insecure-Requests": "1",
}

CSV_HEADERS = {
    "User-Agent":      PAGE_HEADERS["User-Agent"],
    "Accept":          "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer":         REFERER_URL,
    "Sec-Fetch-Dest":  "empty",
    "Sec-Fetch-Mode":  "cors",
    "Sec-Fetch-Site":  "same-origin",
}

PDF_HEADERS = {
    **CSV_HEADERS,
    "Accept": "application/pdf,*/*",
}

# DVIDS（国防省動画配信サービス）経由ダウンロード用ヘッダー
# VID/AUD は war.gov に直接 URL がないため DVIDS → CloudFront 経由で取得する
DVIDS_HEADERS = {
    "User-Agent":      PAGE_HEADERS["User-Agent"],
    "Accept":          "text/html,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer":         "https://www.dvidshub.net/",
}

# リクエスト間の待機秒数（サーバー負荷軽減）
REQUEST_DELAY = 2.0

# -------------------------------------------------------
# ソースCSVの列マッピング
# -------------------------------------------------------
# war.gov CSV の列名ベースマッピング（列順変更・列追加に対して安定）
# Release 03 (6/12/26) より "Featured" 列が先頭に追加されたため、
# インデックスではなく列名で参照する。
SRC_COL = {
    "redaction":        "Redaction",
    "release_date":     "Release Date",
    "title":            "Title",
    "type":             "Type",
    "description":      "Description Blurb",
    "dvids_id":         "DVIDS Video ID",   # VID/AUD のダウンロードキー
    "agency":           "Agency",
    "incident_date":    "Incident Date",
    "incident_location": "Incident Location",
    "download_url":     "PDF | Image Link",
}

# -------------------------------------------------------
# 出力CSVの列（metadata v2 列を末尾に追加）
# -------------------------------------------------------
CSV_FIELDS = [
    # --- 既存列（変更なし）---
    "file_name",
    "agency",
    "release_date",
    "incident_date",
    "incident_location",
    "file_type",
    "source_url",
    "download_url",
    "dvids_video_id",           # DVIDS Video ID（VID/AUD/IMG のダウンロードに使用）
    "downloaded",
    "downloaded_at",
    "first_downloaded_at",   # 初回取得日時（一度設定されたら上書きしない）
    "last_verified_at",      # 最終確認日時（ファイル存在確認のたびに更新）
    "notes",
    # --- metadata v2 追加列（Release 02 対応）---
    "content_category",         # 機密分類（初期値: unclassified）
    "media_available",          # メディア種別（file_type から自動推定）
    "ocr_status",               # OCR処理状況（PDFのみ対象、その他は not_applicable）
    "article_priority",         # 記事化優先度（人間レビューが必要。初期値: unreviewed）
    "reader_interest",          # 読者関心度（人間レビューが必要。初期値: unreviewed）
    "risk_level",               # リスク判定（人間レビューが必要。初期値: unreviewed）
    "note_series",              # noteシリーズ割当（初期値: unassigned）
    "download_scope",           # ダウンロード方針（file_type から自動推定）
    "human_review_required",    # 人間レビュー必須フラグ（常に true）
]


# -------------------------------------------------------
# metadata v2 自動推定
# -------------------------------------------------------

def infer_metadata_v2(file_type: str, dvids_id: str = "") -> dict:
    """
    file_type 文字列（大文字）から metadata v2 の各列の初期値を返す。

    自動判断しすぎないよう保守的な初期値を設定する。
    article_priority / reader_interest / risk_level は人間レビューまで unreviewed のまま。

    dvids_id が指定された場合、VID/AUD の download_scope を candidate に昇格する。
    """
    ft = file_type.upper()

    # war.gov CSV では VIDEO → VID、IMAGE → IMG と省略されている場合がある
    # 両形式を同等に扱う
    is_pdf   = ft == "PDF"
    is_video = ft in ("VIDEO", "VID")
    is_audio = ft in ("AUDIO", "AUD")
    is_image = ft in ("IMAGE", "IMG")

    # media_available: どのメディア形式が利用可能か
    if is_pdf:
        media_available = "pdf"
    elif is_video:
        media_available = "video"
    elif is_audio:
        media_available = "audio"
    elif is_image:
        media_available = "image"
    else:
        media_available = "unknown"

    # ocr_status: PDFのみ処理対象（動画・音声・画像はOCR非対象）
    if is_pdf:
        ocr_status = "unknown"
    elif is_video:
        ocr_status = "not_applicable_video"
    elif is_audio:
        ocr_status = "not_applicable_audio"
    elif is_image:
        ocr_status = "not_applicable_image"
    else:
        ocr_status = "unknown"

    # download_scope:
    #   PDF       → candidate
    #   VID/AUD   → DVIDS ID あり → candidate（CloudFront経由DL可）
    #             → DVIDS ID なし → metadata_only
    #   IMG       → DVIDS ID あり → candidate
    #             → DVIDS ID なし → metadata_only（war.gov URL は WAF 403）
    if is_pdf:
        download_scope = "candidate"
    elif is_video or is_audio or is_image:
        download_scope = "candidate" if dvids_id else "metadata_only"
    else:
        download_scope = "metadata_only"

    return {
        "content_category":      "unclassified",
        "media_available":       media_available,
        "ocr_status":            ocr_status,
        "article_priority":      "unreviewed",
        "reader_interest":       "unreviewed",
        "risk_level":            "unreviewed",
        "note_series":           "unassigned",
        "download_scope":        download_scope,
        "human_review_required": "true",
    }


# -------------------------------------------------------
# 日付正規化
# -------------------------------------------------------

def normalize_release_date(raw_date: str) -> tuple[str, str]:
    """
    war.gov CSV の release_date 表記を正規化する。
    生データキャッシュ（uap-csv-cache.csv）は変更せず、
    files_catalog.csv 生成時のみ適用する。

    Returns:
        (正規化後の日付文字列, 元の値（変換した場合のみ。変換なしは空文字）)

    対象ケース:
        "2005/8/26" → "2026-05-08"
            war.gov 側のデータ誤記。Release 01 の実際の公開日は 2026-05-08。
        "5/22/26"   → "2026-05-22"
            Release 02 の公開日を ISO 形式に統一。
    """
    d = raw_date.strip()
    if d == "2005/8/26":
        return "2026-05-08", d
    if d == "5/22/26":
        return "2026-05-22", d
    return d, ""


def append_note(record: dict, note: str) -> None:
    """
    record["notes"] に追記する（上書きではなく "; " で連結）。
    正規化メモなど既存の notes を消さないようにするため。
    """
    existing = record.get("notes", "").strip()
    record["notes"] = f"{existing}; {note}" if existing else note


# -------------------------------------------------------
# ユーティリティ
# -------------------------------------------------------

def now_jst() -> str:
    """現在時刻を JST 文字列で返す。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S JST")


def filename_from_url(url: str) -> str:
    """URLからファイル名部分を抽出する。"""
    path = urlparse(url).path
    return Path(path).name


def make_safe_filename(title: str, ext: str) -> str:
    """タイトル文字列からファイルシステムに安全なファイル名を生成する。"""
    safe = re.sub(r'[^\w\-]', '_', title.strip())
    safe = re.sub(r'_+', '_', safe).strip('_')[:100]
    return f"{safe}.{ext.lstrip('.')}"


def get_media_dir(file_type: str) -> Path:
    """file_type に応じた保存ディレクトリを返す。"""
    ft = file_type.upper()
    if ft in ("VID", "VIDEO"):
        return RAW_VIDEO_DIR
    elif ft in ("AUD", "AUDIO"):
        return RAW_AUDIO_DIR
    elif ft in ("IMG", "IMAGE"):
        return RAW_IMAGE_DIR
    return RAW_PDF_DIR


def is_already_downloaded(filename: str, file_type: str = "PDF") -> bool:
    """file_type に対応するディレクトリに同名ファイルが存在するか確認する。"""
    return (get_media_dir(file_type) / filename).exists()


# -------------------------------------------------------
# DVIDS 経由ダウンロード
# -------------------------------------------------------

def fetch_dvids_cloudfront_url(dvids_id: str) -> str:
    """
    DVIDS の動画ページ（/video/{id}）から CloudFront MP4 URL を取得する。
    VID・AUD 共通。AUD も DVIDS 上では /video/ に格納されている。
    取得できない場合は空文字を返す。
    """
    url = f"https://www.dvidshub.net/video/{dvids_id}"
    try:
        time.sleep(REQUEST_DELAY)
        resp = requests.get(url, headers=DVIDS_HEADERS, timeout=30)
        resp.raise_for_status()
        # <source src="https://d34w7g4gy10iej.cloudfront.net/video/.../....mp4" ...>
        match = re.search(
            r'<source\s+src="(https://d34w7g4gy10iej\.cloudfront\.net/[^"]+\.mp4)"',
            resp.text,
        )
        return match.group(1) if match else ""
    except Exception:
        return ""


def fetch_dvids_image_cloudfront_url(dvids_id: str) -> str:
    """
    DVIDS の画像ページ（/image/{id}）から CloudFront 高解像度 JPG URL を取得する。
    2000w → 1000w の順で優先。取得できない場合は空文字を返す。
    """
    url = f"https://www.dvidshub.net/image/{dvids_id}"
    try:
        time.sleep(REQUEST_DELAY)
        resp = requests.get(url, headers=DVIDS_HEADERS, timeout=30)
        resp.raise_for_status()
        for size in ("2000w", "1000w"):
            match = re.search(
                rf'(https://[^"\']+cloudfront\.net[^"\']+/{size}_q95\.jpg)',
                resp.text,
            )
            if match:
                return match.group(1)
        return ""
    except Exception:
        return ""


def _download_to(url: str, dest: Path, headers: dict) -> float:
    """
    URL のファイルを dest に保存し、ファイルサイズ（MB）を返す。
    失敗時は例外を送出する。
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    time.sleep(REQUEST_DELAY)
    resp = requests.get(url, headers=headers, timeout=120, stream=True)
    resp.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=65536):
            f.write(chunk)
    return dest.stat().st_size / 1024 / 1024


def try_download_video(record: dict) -> dict:
    """
    VID ファイルを DVIDS 経由で raw_media/video/ にダウンロード試行する。
    DVIDS ID がない場合はスキップ。
    """
    dvids_id  = record.get("dvids_video_id", "").strip()
    file_name = record["file_name"]
    dest      = RAW_VIDEO_DIR / file_name

    if not dvids_id:
        append_note(record, "dvids_id_missing; manual_download_required")
        return record

    if dest.exists():
        record["downloaded"]       = "true"
        record["downloaded_at"]    = now_jst()
        record["last_verified_at"] = now_jst()
        append_note(record, "already exists in raw_media/video")
        return record

    cf_url = fetch_dvids_cloudfront_url(dvids_id)
    if not cf_url:
        append_note(record, f"cloudfront_url_not_found (dvids_id={dvids_id})")
        return record

    try:
        size_mb = _download_to(cf_url, dest, DVIDS_HEADERS)
        ts = now_jst()
        record["downloaded"]    = "true"
        record["downloaded_at"] = ts
        if not record.get("first_downloaded_at"):
            record["first_downloaded_at"] = ts
        record["last_verified_at"] = ts
        append_note(record, f"downloaded {size_mb:.1f} MB via dvids")
        print(f"    → 保存完了: {file_name} ({size_mb:.1f} MB)")
    except Exception as e:
        append_note(record, f"video download error: {e}")

    return record


def try_download_audio(record: dict) -> dict:
    """
    AUD ファイルを DVIDS 経由で raw_media/audio/ にダウンロード試行する。
    実体は MP4（音声トラック付き動画コンテナ）のため notes に記録する。
    DVIDS ID がない場合はスキップ。
    """
    dvids_id  = record.get("dvids_video_id", "").strip()
    file_name = record["file_name"]
    dest      = RAW_AUDIO_DIR / file_name

    if not dvids_id:
        append_note(record, "dvids_id_missing; manual_download_required")
        return record

    if dest.exists():
        record["downloaded"]       = "true"
        record["downloaded_at"]    = now_jst()
        record["last_verified_at"] = now_jst()
        append_note(record, "already exists in raw_media/audio")
        return record

    cf_url = fetch_dvids_cloudfront_url(dvids_id)
    if not cf_url:
        append_note(record, f"cloudfront_url_not_found (dvids_id={dvids_id})")
        return record

    try:
        size_mb = _download_to(cf_url, dest, DVIDS_HEADERS)
        ts = now_jst()
        record["downloaded"]    = "true"
        record["downloaded_at"] = ts
        if not record.get("first_downloaded_at"):
            record["first_downloaded_at"] = ts
        record["last_verified_at"] = ts
        # AUD の実体は MP4 コンテナ。file_type=AUD のまま保存するため notes に明記
        append_note(record, f"downloaded {size_mb:.1f} MB via dvids; audio_downloaded_as_mp4")
        print(f"    → 保存完了: {file_name} ({size_mb:.1f} MB)")
    except Exception as e:
        append_note(record, f"audio download error: {e}")

    return record


def try_download_image(record: dict) -> dict:
    """
    IMG ファイルをダウンロード試行する。取得ルート優先順位:

    Plan A（優先）: DVIDS ID あり
        DVIDS /image/{id} ページから CloudFront 高解像度 JPG URL を解決して取得。
        R01/R02 の IMG 14件はこのルートで取得済み。

    Plan B（フォールバック）: DVIDS ID なし + download_url が画像拡張子
        war.gov medialink URL を PDF_HEADERS（Sec-Fetch-Mode: cors）で直接 GET。
        war.gov の Akamai WAF はこのヘッダーセットで画像を配信することを確認済み
        （R03 IMG 10件、2026-06-14 検証・取得完了）。
        発動条件: dvids_video_id 空 かつ download_url が .jpg/.jpeg/.png/.gif/.webp で終わる。

    Plan C（手動）: URL なし / DVIDS ID なし / 上記いずれも失敗
        notes に manual_download_required を記録し終了。
        raw_media/image/ に手動保存後、スクリプト再実行で downloaded=true に自動更新。
    """
    dvids_id     = record.get("dvids_video_id", "").strip()
    file_name    = record["file_name"]
    download_url = record.get("download_url", "").strip()
    dest         = RAW_IMAGE_DIR / file_name

    if dest.exists():
        record["downloaded"]       = "true"
        record["downloaded_at"]    = now_jst()
        record["last_verified_at"] = now_jst()
        append_note(record, "already exists in raw_media/image")
        return record

    # --- ルート1: DVIDS 経由 ---
    if dvids_id:
        cf_url = fetch_dvids_image_cloudfront_url(dvids_id)
        if not cf_url:
            append_note(record, f"cloudfront_image_url_not_found (dvids_id={dvids_id})")
            return record
        try:
            size_mb = _download_to(cf_url, dest, DVIDS_HEADERS)
            ts = now_jst()
            record["downloaded"]    = "true"
            record["downloaded_at"] = ts
            if not record.get("first_downloaded_at"):
                record["first_downloaded_at"] = ts
            record["last_verified_at"] = ts
            append_note(record, f"downloaded {size_mb:.1f} MB via dvids")
            print(f"    → 保存完了: {file_name} ({size_mb:.1f} MB)")
        except Exception as e:
            append_note(record, f"image download error (dvids): {e}")
        return record

    # --- ルート2: war.gov 直接 GET (DVIDS IDなし・画像拡張子あり) ---
    img_exts = (".jpg", ".jpeg", ".png", ".gif", ".webp")
    if download_url and download_url.lower().endswith(img_exts):
        try:
            time.sleep(REQUEST_DELAY)
            resp = requests.get(download_url, headers=PDF_HEADERS, timeout=60, stream=True)
            if resp.status_code == 403:
                append_note(record,
                    f"WAF 403: direct image download blocked. "
                    f"Manual download required: {download_url}"
                )
                return record
            resp.raise_for_status()
            ct = resp.headers.get("content-type", "")
            if not any(x in ct.lower() for x in ("image", "octet-stream")):
                append_note(record, f"unexpected content-type: {ct} — not saved")
                return record
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    f.write(chunk)
            size_mb = dest.stat().st_size / 1024 / 1024
            ts = now_jst()
            record["downloaded"]    = "true"
            record["downloaded_at"] = ts
            if not record.get("first_downloaded_at"):
                record["first_downloaded_at"] = ts
            record["last_verified_at"] = ts
            append_note(record, f"downloaded {size_mb:.1f} MB via war.gov direct")
            print(f"    → 保存完了: {file_name} ({size_mb:.1f} MB)")
        except requests.HTTPError as e:
            append_note(record, f"HTTP error (direct): {e}")
        except Exception as e:
            append_note(record, f"image download error (direct): {e}")
        return record

    # --- ルート3: 取得不可 ---
    append_note(record, "dvids_id_missing; no_image_url; manual_download_required")
    return record


# -------------------------------------------------------
# 既存カタログ読み込み（履歴継承用）
# -------------------------------------------------------

def load_existing_catalog() -> dict:
    """
    既存の files_catalog.csv を読み込み、file_name → record の辞書を返す。
    first_downloaded_at などの履歴フィールドを再実行時に引き継ぐために使用する。
    ファイルが存在しない場合は空の辞書を返す。
    """
    if not OUTPUT_CSV.exists():
        return {}
    with open(OUTPUT_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["file_name"]: dict(row) for row in reader}


# -------------------------------------------------------
# カタログCSV取得
# -------------------------------------------------------

def fetch_catalog_csv() -> list[dict]:
    """
    war.gov からカタログ CSV を取得し、行の辞書リストを返す。
    各行は output CSV のフィールドにマッピング済み。

    Akamai WAF が 403 を返す場合はローカルキャッシュ(uap-csv-cache.csv)にフォールバックする。
    成功した場合はキャッシュを更新する。
    """
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    raw = None

    print(f"  カタログCSV取得中: {CATALOG_CSV_URL}")
    try:
        resp = requests.get(CATALOG_CSV_URL, headers=CSV_HEADERS, timeout=30)
        resp.raise_for_status()
        raw = resp.content.decode("utf-8-sig", errors="replace")
        # 成功したらキャッシュを更新
        CATALOG_CACHE.write_text(raw, encoding="utf-8")
        print("  → ライブ取得成功。キャッシュを更新しました。")
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            print(f"  → WAF 403: ライブ取得ブロック。ローカルキャッシュを使用します。")
            if CATALOG_CACHE.exists():
                raw = CATALOG_CACHE.read_text(encoding="utf-8-sig")
                print(f"  → キャッシュ: {CATALOG_CACHE} ({CATALOG_CACHE.stat().st_size:,} bytes)")
            else:
                raise RuntimeError(
                    "ライブ取得が403でブロックされ、ローカルキャッシュも存在しません。\n"
                    "ブラウザで以下URLへアクセスし、CSVを metadata/uap-csv-cache.csv として保存してください:\n"
                    f"  {CATALOG_CSV_URL}"
                ) from e
        else:
            raise

    if raw is None:
        raise RuntimeError("CSVデータを取得できませんでした。")

    dict_reader = csv.DictReader(io.StringIO(raw))
    src_rows = list(dict_reader)
    fieldnames = dict_reader.fieldnames or []

    if not src_rows:
        raise ValueError("CSV が空でした")

    print(f"  列数: {len(fieldnames)}  データ行数: {len(src_rows)}")

    existing = load_existing_catalog()

    records = []
    for row in src_rows:
        # 空行スキップ
        if not any(v.strip() for v in row.values() if v):
            continue

        def col(name: str) -> str:
            return (row.get(name) or "").strip().replace("\n", " ").replace("\r", "")

        raw_type     = col(SRC_COL["type"]).upper()
        download_url = col(SRC_COL["download_url"]).split("|")[0].strip()
        dvids_id     = col(SRC_COL["dvids_id"])

        # ファイル名を決定する
        #   VID/AUD: col12 はペアPDFへのリンクであり download_url ではない。
        #            常にタイトルから .mp4 名を生成する。
        #   PDF/IMG: URL からファイル名を取得
        #   IMG with DVIDS but no URL: DVIDS ID ベースのファイル名
        is_vid = raw_type in ("VID", "VIDEO")
        is_aud = raw_type in ("AUD", "AUDIO")
        is_img = raw_type in ("IMG", "IMAGE")

        title_raw = col(SRC_COL["title"]).strip()
        if is_vid or is_aud:
            # "PDF | Image Link" 列は VID/AUD ではペアPDFへのリンク。タイトルから命名する
            file_name = make_safe_filename(title_raw, "mp4")
        else:
            file_name = filename_from_url(download_url) if download_url else ""
            if not file_name:
                if is_img and dvids_id:
                    file_name = f"dvids_{dvids_id}.jpg"
                else:
                    file_name = title_raw + ("." + raw_type.lower() if raw_type else "")

        # metadata v2 列（DVIDS ID の有無で download_scope が変わる）
        meta_v2 = infer_metadata_v2(raw_type, dvids_id)

        # release_date を正規化する（生データキャッシュは変更せず、出力CSVのみ適用）
        raw_release_date = col(SRC_COL["release_date"])
        normalized_date, original_date = normalize_release_date(raw_release_date)
        norm_note = f"release_date_normalized_from:{original_date}" if original_date else ""

        # 履歴フィールドを既存CSVから引き継ぐ
        on_disk = is_already_downloaded(file_name, raw_type)
        prev    = existing.get(file_name, {})
        # first_downloaded_at: 既存値を優先。なければ downloaded_at をフォールバックとして引き継ぐ。
        # ファイル不在でも歴史値は保持（削除・移動時の記録を残す）。
        # ダウンロード関数が初回DL時に設定するため、ここでは空のまま渡す。
        prev_first_dl = prev.get("first_downloaded_at") or prev.get("downloaded_at") or ""
        first_dl = prev_first_dl  # on_disk=False でも既存値があれば引き継ぐ

        records.append({
            "file_name":            file_name,
            "agency":               col(SRC_COL["agency"]),
            "release_date":         normalized_date,
            "incident_date":        col(SRC_COL["incident_date"]),
            "incident_location":    col(SRC_COL["incident_location"]),
            "file_type":            raw_type,
            "source_url":           REFERER_URL,
            "download_url":         download_url,
            "dvids_video_id":       dvids_id,
            "downloaded":           "true" if on_disk else "false",
            "downloaded_at":        now_jst() if on_disk else "",
            "first_downloaded_at":  first_dl,
            "last_verified_at":     now_jst() if on_disk else "",
            "notes":                norm_note,
            # metadata v2 列
            **meta_v2,
        })

    return records


# -------------------------------------------------------
# PDFダウンロード試行
# -------------------------------------------------------

def try_download_pdf(record: dict) -> dict:
    """
    PDFを raw_pdf/ にダウンロード試行する。
    成功した場合: downloaded=true を設定。
    失敗（403など）: notes にエラーを記録し downloaded=false のまま。
    元ファイル名を変更しない。
    """
    url       = record["download_url"]
    file_name = record["file_name"]
    dest      = RAW_PDF_DIR / file_name

    if not url:
        append_note(record, "download_url missing in catalog")
        return record

    if dest.exists():
        record["downloaded"]       = "true"
        record["downloaded_at"]    = now_jst()
        record["last_verified_at"] = now_jst()
        append_note(record, "already exists in raw_pdf")
        return record

    try:
        time.sleep(REQUEST_DELAY)
        resp = requests.get(url, headers=PDF_HEADERS, timeout=60, stream=True)

        if resp.status_code == 403:
            append_note(record,
                "WAF 403: programmatic download blocked by Akamai. "
                f"Manual download required: {url}"
            )
            return record

        resp.raise_for_status()

        # PDF 以外のコンテンツが返ってきた場合のガード
        ct = resp.headers.get("content-type", "")
        if "pdf" not in ct.lower() and "octet-stream" not in ct.lower():
            append_note(record, f"unexpected content-type: {ct} — not saved")
            return record

        # 保存
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                f.write(chunk)

        ts = now_jst()
        size_mb = dest.stat().st_size / 1024 / 1024
        record["downloaded"]    = "true"
        record["downloaded_at"] = ts
        if not record.get("first_downloaded_at"):
            record["first_downloaded_at"] = ts
        record["last_verified_at"] = ts
        append_note(record, f"downloaded {size_mb:.1f} MB")
        print(f"    → 保存完了: {file_name} ({size_mb:.1f} MB)")

    except requests.HTTPError as e:
        append_note(record, f"HTTP error: {e}")
    except requests.RequestException as e:
        append_note(record, f"request error: {e}")
    except Exception as e:
        append_note(record, f"unexpected error: {e}")

    return record


# -------------------------------------------------------
# メイン処理
# -------------------------------------------------------

def main():
    catalog_only = "--catalog-only" in sys.argv

    print("=" * 60)
    print("WAR.GOV/UFO カタログ取得ツール（UAP_TRANSLATION_PROJECT）")
    if catalog_only:
        print("  モード: カタログ確認のみ（ダウンロードはスキップ）")
    print("=" * 60)
    print(f"  カタログURL    : {CATALOG_CSV_URL}")
    print(f"  PDF保存先      : {RAW_PDF_DIR}")
    print(f"  動画保存先     : {RAW_VIDEO_DIR}")
    print(f"  音声保存先     : {RAW_AUDIO_DIR}")
    print(f"  画像保存先     : {RAW_IMAGE_DIR}")
    print(f"  出力CSV        : {OUTPUT_CSV}")
    print()

    RAW_PDF_DIR.mkdir(parents=True, exist_ok=True)
    RAW_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    RAW_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    RAW_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    # --- カタログCSV取得 ---
    print("[Step 1] カタログCSV取得")
    try:
        records = fetch_catalog_csv()
    except Exception as e:
        print(f"  [エラー] カタログ取得失敗: {e}")
        traceback.print_exc()
        sys.exit(1)

    total      = len(records)
    pdf_recs   = [r for r in records if r["file_type"] == "PDF"]
    vid_recs   = [r for r in records if r["file_type"] in ("VID", "VIDEO")]
    aud_recs   = [r for r in records if r["file_type"] in ("AUD", "AUDIO")]
    img_recs   = [r for r in records if r["file_type"] in ("IMG", "IMAGE")]

    print(f"  合計: {total} 件（PDF={len(pdf_recs)}, VID={len(vid_recs)}, "
          f"AUD={len(aud_recs)}, IMG={len(img_recs)}）")
    print()

    def run_download_step(label: str, recs: list, fn) -> tuple[int, int, int]:
        """指定リストに対してダウンロード関数を実行し (成功, ブロック, エラー) を返す。"""
        already  = sum(1 for r in recs if r["downloaded"] == "true")
        to_fetch = [r for r in recs if r["downloaded"] == "false"]
        print(f"  取得済み: {already} 件  未取得: {len(to_fetch)} 件")
        s = b = e = 0
        for i, rec in enumerate(to_fetch, start=1):
            print(f"  [{i:>3}/{len(to_fetch)}] {rec['file_name'][:70]}")
            updated = fn(rec)
            if updated["downloaded"] == "true":
                s += 1
            elif "403" in updated.get("notes", ""):
                b += 1
            else:
                e += 1
            for j, r in enumerate(records):
                if r["file_name"] == rec["file_name"] and r["file_type"] == rec["file_type"]:
                    records[j] = updated
                    break
        return s, b, e

    if catalog_only:
        print("[Step 2] ダウンロードスキップ（--catalog-only モード）")
        pdf_s = pdf_b = pdf_e = 0
        vid_s = vid_b = vid_e = 0
        aud_s = aud_b = aud_e = 0
        img_s = img_b = img_e = 0
        for label, recs in [("PDF", pdf_recs), ("VID", vid_recs), ("AUD", aud_recs), ("IMG", img_recs)]:
            already  = sum(1 for r in recs if r["downloaded"] == "true")
            to_fetch = [r for r in recs if r["downloaded"] == "false"]
            print(f"  {label}: 取得済み {already} 件  未取得（追加予定）: {len(to_fetch)} 件")
        print()
    else:
        # --- PDF ダウンロード試行 ---
        print("[Step 2a] PDFダウンロード試行（未取得のみ）")
        pdf_s, pdf_b, pdf_e = run_download_step("PDF", pdf_recs, try_download_pdf)
        print(f"  成功: {pdf_s}  WAFブロック: {pdf_b}  エラー: {pdf_e}")
        print()

        # --- VID ダウンロード試行 ---
        print("[Step 2b] VIDダウンロード試行（DVIDS経由 → CloudFront MP4）")
        vid_s, vid_b, vid_e = run_download_step("VID", vid_recs, try_download_video)
        print(f"  成功: {vid_s}  スキップ/エラー: {vid_e + vid_b}")
        print()

        # --- AUD ダウンロード試行 ---
        print("[Step 2c] AUDダウンロード試行（DVIDS経由 → CloudFront MP4）")
        aud_s, aud_b, aud_e = run_download_step("AUD", aud_recs, try_download_audio)
        print(f"  成功: {aud_s}  スキップ/エラー: {aud_e + aud_b}")
        print()

        # --- IMG ダウンロード試行 ---
        print("[Step 2d] IMGダウンロード試行（DVIDS ID あり のみ）")
        img_s, img_b, img_e = run_download_step("IMG", img_recs, try_download_image)
        print(f"  成功: {img_s}  スキップ/エラー: {img_e + img_b}")
        print()

    blocked = pdf_b

    # --- CSV書き出し ---
    print("[Step 3] CSV書き出し")
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(records)
    print(f"  → {OUTPUT_CSV}  ({total} 行)")
    print()

    # --- サマリ ---
    print("=" * 60)
    print(f"完了")
    print(f"  カタログ総件数    : {total}")
    for label, recs, s in [
        ("PDF", pdf_recs, pdf_s),
        ("VID", vid_recs, vid_s),
        ("AUD", aud_recs, aud_s),
        ("IMG", img_recs, img_s),
    ]:
        total_dl = sum(1 for r in recs if r["downloaded"] == "true")
        print(f"  {label:<6}: {len(recs):>3} 件  取得済み: {total_dl}")
    print(f"  出力CSV列数       : {len(CSV_FIELDS)}  （metadata v2・v3 列を含む）")
    if blocked > 0:
        print(f"  PDF WAFブロック   : {blocked}  ← ブラウザで手動DL後、再実行してください")
    print("=" * 60)

    if blocked > 0:
        print()
        print("[手動DL手順]")
        print("  以下のURLをブラウザで開き raw_pdf/ に保存してください:")
        for r in records:
            if r["file_type"] == "PDF" and r["downloaded"] == "false" and "WAF" in r.get("notes",""):
                print(f"    {r['download_url']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[中断] ユーザーによって処理が中断されました。")
        sys.exit(0)
    except Exception:
        print("[予期しないエラー]")
        traceback.print_exc()
        sys.exit(1)
