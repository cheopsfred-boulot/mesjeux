"""Fetch or import Crescendo results."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import DATA_DIR, load_json, save_json
from fdj_parsers import fetch_text, parse_crescendo_results


OUTPUT = DATA_DIR / "crescendo.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Crescendo results into data/crescendo.json")
    parser.add_argument("--source", help="Local file path or URL to import")
    parser.add_argument("--raw-output", help="Optional path to store the raw payload")
    args = parser.parse_args()

    if not args.source:
        raise SystemExit("Provide --source with a local file path or URL.")

    records = parse_crescendo_results(args.source)
    if args.raw_output:
        Path(args.raw_output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.raw_output).write_text(fetch_text(args.source), encoding="utf-8")

    current = load_json(OUTPUT, [])
    current.extend(records)
    save_json(OUTPUT, current)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
