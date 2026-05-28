"""
fetch_war_gov_catalog.py
========================
UAP公開文書 翻訳・要約プロジェクト — WAR.GOV/UFO カタログ取得ツール

目的:
    https://www.war.gov/UFO/ に掲載されている公開ファイル一覧を取得し、
    metadata/files_catalog.csv へ保存する。
    また、未取得のPDFファイルをダウンロードして raw_pdf/ へ保存する。

metadata v2 追加列（Release 02 対応）:
    content_category, media_available, ocr_status, article_priority,
    reader_interest, risk_level, note_series, download_scope,
    human_review_required
    → 初期値は保守的な自動推定のみ。article_priority 等の判断は人間レビューが必要。

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
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PDF_DIR  = PROJECT_ROOT / "raw_pdf"
METADATA_DIR = PROJECT_ROOT / "metadata"
OUTPUT_CSV   = METADATA_DIR / "files_catalog.csv"

# -------------------------------------------------------
# WAR.GOV 設定
# -------------------------------------------------------
BASE_URL       = "https://www.war.gov"
CATALOG_CSV_PATH = "/Portals/1/Interactive/2026/UFO/uap-csv.csv"
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

# リクエスト間の待機秒数（サーバー負荷軽減）
REQUEST_DELAY = 2.0

# -------------------------------------------------------
# ソースCSVの列マッピング
# -------------------------------------------------------
# war.gov CSV の列: Redaction(0), Release Date(1), Title(2), Type(3),
#   Video Pairing(4), PDF Pairing(5), Description Blurb(6),
#   DVIDS Video ID(7), Video Title(8), Agency(9),
#   Incident Date(10), Incident Location(11), PDF | Image Link(12),
#   Modal Image(13)
SRC_COL = {
    "redaction":        0,
    "release_date":     1,
    "title":            2,
    "type":             3,
    "description":      6,
    "agency":           9,
    "incident_date":    10,
    "incident_location": 11,
    "download_url":     12,
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
    "downloaded",
    "downloaded_at",
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

def infer_metadata_v2(file_type: str) -> dict:
    """
    file_type 文字列（大文字）から metadata v2 の各列の初期値を返す。

    自動判断しすぎないよう保守的な初期値を設定する。
    article_priority / reader_interest / risk_level は人間レビューまで unreviewed のまま。
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

    # download_scope: PDFと画像はダウンロード候補、動画・音声はメタデータのみ
    if is_pdf or is_image:
        download_scope = "candidate"
    elif is_video or is_audio:
        download_scope = "metadata_only"
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
# ユーティリティ
# -------------------------------------------------------

def now_jst() -> str:
    """現在時刻を JST 文字列で返す。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S JST")


def filename_from_url(url: str) -> str:
    """URLからファイル名部分を抽出する。"""
    path = urlparse(url).path
    return Path(path).name


def is_already_downloaded(filename: str) -> bool:
    """raw_pdf/ に同名ファイルが存在するか確認する。"""
    return (RAW_PDF_DIR / filename).exists()


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

    reader = csv.reader(io.StringIO(raw))
    reader = csv.reader(io.StringIO(raw))
    src_rows = list(reader)

    if not src_rows:
        raise ValueError("CSV が空でした")

    headers = src_rows[0]
    print(f"  列数: {len(headers)}  データ行数: {len(src_rows)-1}")

    records = []
    for row in src_rows[1:]:
        # 空行スキップ
        if not any(c.strip() for c in row):
            continue

        def col(idx: int) -> str:
            return row[idx].strip().replace("\n", " ").replace("\r", "") if len(row) > idx else ""

        raw_type    = col(SRC_COL["type"]).upper()
        download_url = col(SRC_COL["download_url"]).split("|")[0].strip()

        # ファイル名：タイトルからフォールバック → URLから取得
        file_name = filename_from_url(download_url) if download_url else ""
        if not file_name:
            title_raw = col(SRC_COL["title"]).strip()
            file_name = title_raw + ("." + raw_type.lower() if raw_type else "")

        # metadata v2 列を file_type から自動推定する（断定しすぎない保守的な初期値）
        meta_v2 = infer_metadata_v2(raw_type)

        records.append({
            # 既存列（変更なし）
            "file_name":         file_name,
            "agency":            col(SRC_COL["agency"]),
            "release_date":      col(SRC_COL["release_date"]),
            "incident_date":     col(SRC_COL["incident_date"]),
            "incident_location": col(SRC_COL["incident_location"]),
            "file_type":         raw_type,
            "source_url":        REFERER_URL,
            "download_url":      download_url,
            "downloaded":        "true" if is_already_downloaded(file_name) else "false",
            "downloaded_at":     now_jst() if is_already_downloaded(file_name) else "",
            "notes":             "",
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
        record["notes"] = "download_url missing in catalog"
        return record

    if dest.exists():
        # すでに存在：スキップ（上書きしない）
        record["downloaded"]    = "true"
        record["downloaded_at"] = now_jst()
        record["notes"]         = "already exists in raw_pdf"
        return record

    try:
        time.sleep(REQUEST_DELAY)
        resp = requests.get(url, headers=PDF_HEADERS, timeout=60, stream=True)

        if resp.status_code == 403:
            record["notes"] = (
                "WAF 403: programmatic download blocked by Akamai. "
                f"Manual download required: {url}"
            )
            return record

        resp.raise_for_status()

        # PDF 以外のコンテンツが返ってきた場合のガード
        ct = resp.headers.get("content-type", "")
        if "pdf" not in ct.lower() and "octet-stream" not in ct.lower():
            record["notes"] = f"unexpected content-type: {ct} — not saved"
            return record

        # 保存
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                f.write(chunk)

        size_mb = dest.stat().st_size / 1024 / 1024
        record["downloaded"]    = "true"
        record["downloaded_at"] = now_jst()
        record["notes"]         = f"downloaded {size_mb:.1f} MB"
        print(f"    → 保存完了: {file_name} ({size_mb:.1f} MB)")

    except requests.HTTPError as e:
        record["notes"] = f"HTTP error: {e}"
    except requests.RequestException as e:
        record["notes"] = f"request error: {e}"
    except Exception as e:
        record["notes"] = f"unexpected error: {e}"

    return record


# -------------------------------------------------------
# メイン処理
# -------------------------------------------------------

def main():
    print("=" * 60)
    print("WAR.GOV/UFO カタログ取得ツール（UAP_TRANSLATION_PROJECT）")
    print("=" * 60)
    print(f"  カタログURL : {CATALOG_CSV_URL}")
    print(f"  PDF保存先  : {RAW_PDF_DIR}")
    print(f"  出力CSV    : {OUTPUT_CSV}")
    print()

    RAW_PDF_DIR.mkdir(parents=True, exist_ok=True)
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
    other_recs = [r for r in records if r["file_type"] != "PDF"]

    print(f"  合計: {total} 件（PDF={len(pdf_recs)}, その他={len(other_recs)}）")
    print()

    # --- PDF ダウンロード試行 ---
    print("[Step 2] PDFダウンロード試行（未取得のみ）")
    already  = sum(1 for r in pdf_recs if r["downloaded"] == "true")
    to_fetch = [r for r in pdf_recs if r["downloaded"] == "false"]
    print(f"  取得済み: {already} 件  未取得: {len(to_fetch)} 件")
    print()

    success = 0
    blocked = 0
    errors  = 0

    for i, rec in enumerate(to_fetch, start=1):
        print(f"  [{i:>3}/{len(to_fetch)}] {rec['file_name']}")
        updated = try_download_pdf(rec)

        if updated["downloaded"] == "true":
            success += 1
        elif "403" in updated["notes"]:
            blocked += 1
        else:
            errors += 1

        # records リスト内の dict を更新
        for j, r in enumerate(records):
            if r["file_name"] == rec["file_name"]:
                records[j] = updated
                break

    print()
    print(f"  成功: {success}  WAFブロック: {blocked}  エラー: {errors}")
    print()

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
    downloaded_total = sum(1 for r in records if r["downloaded"] == "true")
    # file_type 別の件数（PDF以外を詳細表示）
    type_counts: dict[str, int] = {}
    for r in records:
        ft = r["file_type"] or "UNKNOWN"
        type_counts[ft] = type_counts.get(ft, 0) + 1

    print(f"完了")
    print(f"  カタログ総件数    : {total}")
    for ft, cnt in sorted(type_counts.items()):
        print(f"  {ft:<20}: {cnt} 件")
    print(f"  PDF取得済み       : {downloaded_total}")
    print(f"  WAFブロック       : {blocked}  ← ブラウザで手動DL後、再実行してください")
    print(f"  出力CSV列数       : {len(CSV_FIELDS)}  （metadata v2 列を含む）")
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
