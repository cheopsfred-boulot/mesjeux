"""Compare a played grid to a draw.

The comparison keeps the output simple so it can feed both Markdown reports and
MCP tools later.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import save_json


def compare(play: list[int], draw: list[int], chance_played: list[int] | None = None, chance_drawn: list[int] | None = None) -> dict[str, object]:
    exact = sorted(set(play) & set(draw))
    missing = sorted(set(play) - set(draw))
    unexpected = sorted(set(draw) - set(play))
    chance_played = chance_played or []
    chance_drawn = chance_drawn or []
    chance_exact = sorted(set(chance_played) & set(chance_drawn))
    return {
        "played": play,
        "draw": draw,
        "exact_matches": exact,
        "played_only": missing,
        "draw_only": unexpected,
        "match_count": len(exact),
        "chance_played": chance_played,
        "chance_drawn": chance_drawn,
        "chance_exact_matches": chance_exact,
        "chance_match_count": len(chance_exact),
    }


def parse_numbers(value: str) -> list[int]:
    return [int(item) for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare a played grid with a draw")
    parser.add_argument("--game", choices=["loto", "euromillions", "crescendo"], help="Optional game context")
    parser.add_argument("--played", required=True, help="Comma-separated numbers")
    parser.add_argument("--draw", required=True, help="Comma-separated numbers")
    parser.add_argument("--chance-played", help="Comma-separated chance/star values")
    parser.add_argument("--chance-drawn", help="Comma-separated chance/star values")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()

    result = compare(
        parse_numbers(args.played),
        parse_numbers(args.draw),
        parse_numbers(args.chance_played) if args.chance_played else None,
        parse_numbers(args.chance_drawn) if args.chance_drawn else None,
    )
    if args.game:
        result["game"] = args.game
    if args.output:
        save_json(Path(args.output), result)
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
