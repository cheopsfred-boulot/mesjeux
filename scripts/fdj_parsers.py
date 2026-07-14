"""FDJ HTML parsers for official result pages.

These parsers are intentionally narrow and dependency-free. They focus on the
official result page HTML rendered by fdj.fr.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict
from html import unescape
from pathlib import Path
from typing import Any
from urllib.request import urlopen

from _common import Draw


_WS = re.compile(r"\s+")


def fetch_text(source: str) -> str:
    if source.startswith("http://") or source.startswith("https://"):
        with urlopen(source) as response:
            return response.read().decode("utf-8", errors="replace")
    return Path(source).read_text(encoding="utf-8")


def normalize_text(value: str) -> str:
    value = unescape(value)
    value = value.replace("\u202f", " ")
    value = value.replace("\xa0", " ")
    value = _WS.sub(" ", value)
    return value.strip()


def _numbers_from_hyphen_block(text: str) -> list[int]:
    return [int(item) for item in re.findall(r"\d+", text)]


def parse_loto_result(source: str) -> dict[str, Any]:
    html = fetch_text(source)
    match = re.search(
        r"Combinaison gagnante du tirage Loto du ([^<]+)</h2>.*?La combinaison gagnante est le ([0-9-]+) et le num[eé]ro chance est le (\d+)",
        html,
        re.IGNORECASE | re.S,
    )
    if not match:
        raise ValueError("Unable to parse Loto result page")
    date_label, numbers_block, chance = match.groups()
    numbers = _numbers_from_hyphen_block(numbers_block)
    return asdict(
        Draw(
            game="loto",
            date=normalize_text(date_label),
            numbers=numbers,
            bonus=[int(chance)],
            source=source,
        )
    )


def parse_euromillions_result(source: str) -> dict[str, Any]:
    html = fetch_text(source)
    match = re.search(
        r"La combinaison à laquelle a abouti ce tirage est composée des numéros ([0-9-]+) et les deux étoiles, le (\d+) et le (\d+)",
        html,
        re.IGNORECASE | re.S,
    )
    if not match:
        raise ValueError("Unable to parse EuroMillions result page")
    numbers_block, star_1, star_2 = match.groups()
    numbers = _numbers_from_hyphen_block(numbers_block)

    million_match = re.search(
        r"Le code gagnant tiré au sort aujourd[’']hui est : ([A-Z]{2}\s*\d+\s*\d+)",
        html,
        re.IGNORECASE,
    )
    million_code = normalize_text(million_match.group(1)) if million_match else None

    url_label = re.search(r"/resultats/([^/?#]+)", source)
    date_label = normalize_text(url_label.group(1).replace("-", " ") if url_label else "EuroMillions")

    return {
        **asdict(
            Draw(
                game="euromillions",
                date=date_label,
                numbers=numbers,
                bonus=[int(star_1), int(star_2)],
                source=source,
            )
        ),
        "my_million": million_code,
    }


def parse_crescendo_results(source: str) -> list[dict[str, Any]]:
    html = fetch_text(source)
    block = re.search(r'id="result-wrapper-grid-1".*?data-theme="fdj"', html, re.S)
    if not block:
        raise ValueError("Unable to locate Crescendo result block")

    start = block.start()
    tail = html[start:]
    grid_match = re.search(r'id="result-grid-1".*?</div></div></div></div>', tail, re.S)
    chunk = grid_match.group(0) if grid_match else tail[:20000]

    numbers = [int(n) for n in re.findall(r'<span class="relative heading4 lg:heading5">(\d+)</span>', chunk)]
    if not numbers:
        raise ValueError("Unable to parse Crescendo numbers")

    level_match = re.search(r'<span class="relative heading4 lg:heading5">([A-Z])</span>', chunk)
    level = level_match.group(1) if level_match else None

    header_match = re.search(r'<h4 class="heading4" aria-label="([^"]+)">([^<]+)</h4>', chunk)
    url_label = re.search(r"/resultats/([^/?#]+)", source)
    draw_label = normalize_text(url_label.group(1).replace("-", " ") if url_label else (header_match.group(1) if header_match else "Crescendo"))

    jackpot_match = re.search(r'<p class="text-subheading-md[^>]*>(.*?)</p>', chunk, re.S)
    jackpot = normalize_text(re.sub(r'<[^>]+>', '', jackpot_match.group(1))) if jackpot_match else None

    return [
        {
            "game": "crescendo",
            "date": draw_label,
            "numbers": numbers,
            "bonus": [level] if level else [],
            "source": source,
            "jackpot": jackpot,
        }
    ]


def load_json_file(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
