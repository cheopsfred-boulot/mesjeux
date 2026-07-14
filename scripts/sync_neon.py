"""Sync local normalized JSON history into Neon/Postgres."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.neon_store import neon_enabled
from app.sync_service import load_rows, sync_game


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync local data/*.json to Neon")
    parser.add_argument("--game", choices=["loto", "euromillions", "crescendo"], help="Sync only one game")
    args = parser.parse_args()

    if not neon_enabled():
        print("Neon is not configured; nothing synced.")
        return 0

    games = [args.game] if args.game else ["loto", "euromillions", "crescendo"]
    total = 0
    for game in games:
        total += sync_game(game, load_rows(game))
    print(f"Synced {total} rows into Neon.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
