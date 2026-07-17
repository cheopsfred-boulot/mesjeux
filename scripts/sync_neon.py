"""Sync local normalized JSON history into Neon/Postgres."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.neon_store import neon_enabled
from app.sync_service import load_rows, sync_game


def import_env_file(path: Path) -> None:
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        if key and os.getenv(key, "") == "":
            os.environ[key] = value


for env_path in (ROOT / ".env.local", ROOT / ".env"):
    import_env_file(env_path)


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
