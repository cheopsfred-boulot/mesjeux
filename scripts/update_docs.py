"""Refresh Markdown notes from JSON data.

This is intentionally minimal for the bootstrap phase.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import DATA_DIR, DOCS_DIR, load_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Update markdown documentation")
    parser.add_argument("--source", help="Optional data file to summarize")
    args = parser.parse_args()

    if args.source:
        sources = [Path(args.source)]
    else:
        sources = [DATA_DIR / "loto.json", DATA_DIR / "euromillions.json", DATA_DIR / "crescendo.json", DATA_DIR / "archive-manifest.json"]

    lines = ["# Auto summary", ""]
    for source in sources:
        payload = load_json(source, [])
        count = len(payload) if hasattr(payload, "__len__") else "n/a"
        lines.append(f"- Source: `{source}`")
        lines.append(f"  - Items: `{count}`")
    (DOCS_DIR / "auto-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
