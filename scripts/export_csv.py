"""Export normalized FDJ JSON data to CSV files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from _common import DATA_DIR, load_json
from app.exports import write_csv_file

GAMES = ("loto", "euromillions", "crescendo")


def export_game(game: str, output_dir: Path) -> tuple[Path, int]:
    rows = load_json(DATA_DIR / f"{game}.json", [])
    output = output_dir / f"{game}.csv"
    write_csv_file(game, rows, output)
    return output, len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export JSON data to CSV")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--game", choices=GAMES, help="Export a single game")
    group.add_argument("--all", action="store_true", help="Export every normalized game")
    parser.add_argument("--output", help="CSV output path when exporting a single game")
    parser.add_argument("--output-dir", help="Directory for exported CSV files", default=str(DATA_DIR))
    args = parser.parse_args()

    if args.game and args.all:
        parser.error("--game and --all are mutually exclusive")

    output_dir = Path(args.output_dir)
    if args.game:
        output = Path(args.output) if args.output else output_dir / f"{args.game}.csv"
        rows = load_json(DATA_DIR / f"{args.game}.json", [])
        write_csv_file(args.game, rows, output)
        print(f"Exported {len(rows)} rows to {output}")
        return 0

    games = GAMES if args.all or not args.game else (args.game,)
    for game in games:
        output, count = export_game(game, output_dir)
        print(f"Exported {count} rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
