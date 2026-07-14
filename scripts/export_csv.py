"""Export normalized FDJ JSON data to CSV files."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import DATA_DIR, load_json


def export_rows(game: str, rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "game",
        "date",
        "date_display",
        "draw_id",
        "draw_slot",
        "hour",
        "numbers",
        "bonus",
        "source",
        "source_csv",
        "archive_segment",
        "my_million",
        "jackpot",
    ]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "game": game,
                    "date": row.get("date"),
                    "date_display": row.get("date_display"),
                    "draw_id": row.get("draw_id"),
                    "draw_slot": row.get("draw_slot"),
                    "hour": row.get("hour"),
                    "numbers": " ".join(map(str, row.get("numbers", []))),
                    "bonus": " ".join(map(str, row.get("bonus", []))),
                    "source": row.get("source"),
                    "source_csv": row.get("source_csv"),
                    "archive_segment": row.get("archive_segment"),
                    "my_million": row.get("my_million"),
                    "jackpot": row.get("jackpot"),
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Export JSON data to CSV")
    parser.add_argument("--game", choices=["loto", "euromillions", "crescendo"], required=True)
    parser.add_argument("--output", help="CSV output path")
    args = parser.parse_args()

    rows = load_json(DATA_DIR / f"{args.game}.json", [])
    output = Path(args.output) if args.output else DATA_DIR / f"{args.game}.csv"
    export_rows(args.game, rows, output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
