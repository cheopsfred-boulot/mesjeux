"""Download official FDJ history archives exposed on the result history pages."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import ROOT, save_json


ARCHIVE_ROOT = ROOT / "archives"
MANIFEST = ROOT / "data" / "archive-manifest.json"
HISTORY_URLS = {
    "loto": "https://www.fdj.fr/jeux-de-tirage/loto/historique",
    "euromillions": "https://www.fdj.fr/jeux-de-tirage/euromillions-my-million/historique",
    "crescendo": "https://www.fdj.fr/jeux-de-tirage/crescendo/historique",
}


def fetch_html(url: str) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req) as response:
        return response.read().decode("utf-8", errors="replace")


def discover_links(game: str) -> list[dict[str, str]]:
    html = fetch_html(HISTORY_URLS[game])
    pattern = re.compile(
        r'<a class="block"[^>]+download="([^"]+)"[^>]+title="([^"]+)"[^>]+href="([^"]+)"',
        re.S,
    )
    links = []
    for download_name, title, href in pattern.findall(html):
        if "documentations" in href:
            links.append(
                {
                    "game": game,
                    "download_name": download_name,
                    "title": title,
                    "href": href,
                }
            )
    return links


def download_and_extract(entry: dict[str, str]) -> dict[str, str]:
    game_dir = ARCHIVE_ROOT / entry["game"]
    game_dir.mkdir(parents=True, exist_ok=True)

    zip_path = game_dir / f'{entry["download_name"]}.zip'
    target_dir = game_dir / entry["download_name"]

    req = Request(entry["href"], headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "")

    zip_path.write_bytes(payload)

    if not zipfile.is_zipfile(zip_path):
        return {
            **entry,
            "zip_path": str(zip_path),
            "extracted_to": "",
            "status": "not_zip",
            "content_type": content_type,
        }

    if target_dir.exists():
        return {
            **entry,
            "zip_path": str(zip_path),
            "extracted_to": str(target_dir),
            "status": "exists",
            "content_type": content_type,
        }

    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(target_dir)

    return {
        **entry,
        "zip_path": str(zip_path),
        "extracted_to": str(target_dir),
        "status": "downloaded",
        "content_type": content_type,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Download FDJ history archives")
    parser.add_argument("--game", choices=list(HISTORY_URLS.keys()), help="Game to download")
    parser.add_argument("--all", action="store_true", help="Download archives for all supported games")
    args = parser.parse_args()

    games = list(HISTORY_URLS.keys()) if args.all or not args.game else [args.game]
    manifest: list[dict[str, str]] = []
    for game in games:
        for link in discover_links(game):
            manifest.append(download_and_extract(link))

    save_json(MANIFEST, manifest)
    print(f"Saved {len(manifest)} archive entries to {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
