"""Refresh the full FDJ workspace in one command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh all FDJ data and exports")
    parser.add_argument("--download-archives", action="store_true", help="Download official FDJ history archives first")
    args = parser.parse_args()

    if args.download_archives:
        run([PYTHON, str(ROOT / "scripts" / "download_fdj_archives.py"), "--all"])

    run([PYTHON, str(ROOT / "scripts" / "import_fdj_archives.py")])

    run([PYTHON, str(ROOT / "scripts" / "export_csv.py"), "--game", "loto"])
    run([PYTHON, str(ROOT / "scripts" / "export_csv.py"), "--game", "euromillions"])
    run([PYTHON, str(ROOT / "scripts" / "export_csv.py"), "--game", "crescendo"])

    run([PYTHON, str(ROOT / "scripts" / "update_docs.py")])
    print("Refresh completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
