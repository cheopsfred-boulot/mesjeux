"""Apply SQL migrations to Neon/Postgres."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.neon_store import get_connection, neon_enabled
SQL_DIR = ROOT / "sql"


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply SQL migrations in lexical order")
    args = parser.parse_args()

    if not neon_enabled():
        print("Neon is not configured; migrations not applied.")
        return 0

    conn = get_connection()
    if conn is None:
        print("Unable to open Neon connection.")
        return 1

    files = sorted(SQL_DIR.glob("*.sql"))
    with conn.cursor() as cur:
        for file in files:
            sql = file.read_text(encoding="utf-8")
            cur.execute(sql)
            print(f"Applied {file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
