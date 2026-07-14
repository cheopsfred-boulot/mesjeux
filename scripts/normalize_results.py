"""Normalize imported FDJ results into a canonical JSON structure."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import DATA_DIR, load_json, save_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize raw FDJ payloads")
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--output", help="Output JSON file")
    args = parser.parse_args()

    payload = load_json(Path(args.input), [])
    output = Path(args.output) if args.output else DATA_DIR / "normalized.json"
    save_json(output, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
