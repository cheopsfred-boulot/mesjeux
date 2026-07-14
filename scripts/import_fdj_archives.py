"""Import FDJ CSV archives into normalized JSON history files."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import DATA_DIR, ROOT, save_json


ARCHIVE_ROOT = ROOT / "archives"
OUTPUTS = {
    "loto": DATA_DIR / "loto.json",
    "euromillions": DATA_DIR / "euromillions.json",
    "crescendo": DATA_DIR / "crescendo.json",
}


def parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_date(raw: str | None) -> tuple[str | None, str | None]:
    if not raw:
        return None, None
    raw = raw.strip()
    for fmt in ("%Y%m%d", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(raw, fmt)
            return dt.date().isoformat(), raw
        except ValueError:
            pass
    return raw, raw


def normalize_row(row: dict[str, str]) -> dict[str, Any]:
    return {k: v for k, v in row.items() if v not in ("", None)}


def game_from_path(path: Path) -> str | None:
    lowered = str(path).lower()
    if "\\loto\\" in lowered or "/loto/" in lowered:
        return "loto"
    if "\\euromillions\\" in lowered or "/euromillions/" in lowered:
        return "euromillions"
    if "\\crescendo\\" in lowered or "/crescendo/" in lowered:
        return "crescendo"
    return None


def build_loto_record(row: dict[str, str], source_csv: Path, archive_segment: str) -> dict[str, Any]:
    numbers_keys = [f"boule_{i}" for i in range(1, 7) if row.get(f"boule_{i}")]
    chance = parse_int(row.get("numero_chance") or row.get("boule_complementaire"))
    numbers = [parse_int(row[k]) for k in numbers_keys]
    numbers = [n for n in numbers if n is not None]
    date_iso, date_display = parse_date(row.get("date_de_tirage"))
    record = {
        "game": "loto",
        "date": date_iso,
        "date_display": date_display,
        "draw_id": row.get("annee_numero_de_tirage"),
        "draw_slot": parse_int(row.get("1er_ou_2eme_tirage")),
        "weekday": row.get("jour_de_tirage"),
        "numbers": numbers,
        "bonus": [chance] if chance is not None else [],
        "source_csv": str(source_csv),
        "archive_segment": archive_segment,
        "winning_combination_sorted": row.get("combinaison_gagnante_en_ordre_croissant"),
        "raw": normalize_row(row),
    }
    return record


def build_euromillions_record(row: dict[str, str], source_csv: Path, archive_segment: str) -> dict[str, Any]:
    numbers = [parse_int(row.get(f"boule_{i}")) for i in range(1, 6)]
    numbers = [n for n in numbers if n is not None]
    stars = [parse_int(row.get("etoile_1")), parse_int(row.get("etoile_2"))]
    stars = [n for n in stars if n is not None]
    date_iso, date_display = parse_date(row.get("date_de_tirage"))
    record = {
        "game": "euromillions",
        "date": date_iso,
        "date_display": date_display,
        "draw_id": row.get("annee_numero_de_tirage"),
        "weekday": row.get("jour_de_tirage"),
        "numbers": numbers,
        "bonus": stars,
        "my_million": row.get("numero_jokerplus") or None,
        "source_csv": str(source_csv),
        "archive_segment": archive_segment,
        "winning_combination_sorted": row.get("boules_gagnantes_en_ordre_croissant"),
        "winning_stars_sorted": row.get("etoiles_gagnantes_en_ordre_croissant"),
        "raw": normalize_row(row),
    }
    return record


def build_crescendo_record(row: dict[str, str], source_csv: Path, archive_segment: str) -> dict[str, Any]:
    numbers = [parse_int(row.get(f"boule{i}")) for i in range(1, 11)]
    numbers = [n for n in numbers if n is not None]
    date_iso, date_display = parse_date(row.get("date_de_tirage"))
    record = {
        "game": "crescendo",
        "date": date_iso,
        "date_display": date_display,
        "draw_id": row.get("annee_numero_de_tirage"),
        "hour": row.get("heure_de_tirage"),
        "numbers": numbers,
        "bonus": [row.get("lettre")] if row.get("lettre") else [],
        "source_csv": str(source_csv),
        "archive_segment": archive_segment,
        "winning_combination_sorted": row.get("combinaison_gagnante_en_ordre_croissant"),
        "raw": normalize_row(row),
    }
    return record


def load_archives() -> dict[str, list[dict[str, Any]]]:
    output: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for csv_path in sorted(ARCHIVE_ROOT.rglob("*.csv")):
        game = game_from_path(csv_path)
        if not game:
            continue
        archive_segment = csv_path.stem
        with csv_path.open(encoding="utf-8-sig", errors="replace", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                if game == "loto":
                    output[game].append(build_loto_record(row, csv_path, archive_segment))
                elif game == "euromillions":
                    output[game].append(build_euromillions_record(row, csv_path, archive_segment))
                elif game == "crescendo":
                    output[game].append(build_crescendo_record(row, csv_path, archive_segment))
    return output


def dedupe_and_sort(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    unique: list[dict[str, Any]] = []
    for record in records:
        key = (
            record.get("game"),
            record.get("date"),
            tuple(record.get("numbers", [])),
            tuple(record.get("bonus", [])),
            record.get("draw_id"),
            record.get("draw_slot"),
            record.get("hour"),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(record)
    unique.sort(key=lambda item: (item.get("date") or "", item.get("draw_id") or "", item.get("hour") or ""))
    return unique


def main() -> int:
    parser = argparse.ArgumentParser(description="Import FDJ archives into normalized JSON")
    args = parser.parse_args()

    data = load_archives()
    for game, records in data.items():
        save_json(OUTPUTS[game], dedupe_and_sort(records))

    print(f"Imported: loto={len(data['loto'])}, euromillions={len(data['euromillions'])}, crescendo={len(data['crescendo'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

