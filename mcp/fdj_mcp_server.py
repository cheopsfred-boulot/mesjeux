"""Local MCP server for FDJ history and comparison tools."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "The 'mcp' package is required to run this server. Install it in the local Python environment."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MCP = FastMCP("fdj-history")


def load_records(game: str) -> list[dict[str, Any]]:
    path = DATA_DIR / f"{game}.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else []


def latest_record(game: str) -> dict[str, Any]:
    records = load_records(game)
    return records[-1] if records else {}


def compare_lists(played: list[int], draw: list[int]) -> dict[str, Any]:
    exact = sorted(set(played) & set(draw))
    played_only = sorted(set(played) - set(draw))
    draw_only = sorted(set(draw) - set(played))
    return {
        "played": played,
        "draw": draw,
        "exact_matches": exact,
        "played_only": played_only,
        "draw_only": draw_only,
        "match_count": len(exact),
    }


@MCP.tool()
def get_last_result(game: str) -> dict[str, Any]:
    """Return the latest record for a game: loto, euromillions, or crescendo."""
    if game not in {"loto", "euromillions", "crescendo"}:
        return {"error": f"Unsupported game: {game}"}
    return latest_record(game)


@MCP.tool()
def get_history(game: str) -> list[dict[str, Any]]:
    """Return the full normalized history for a game."""
    if game not in {"loto", "euromillions", "crescendo"}:
        return []
    return load_records(game)


@MCP.tool()
def compare_grid_to_result(played: list[int], draw: list[int]) -> dict[str, Any]:
    """Compare a played grid to a draw and return exact/missing numbers."""
    return compare_lists(played, draw)


@MCP.tool()
def generate_balanced_loto_grid() -> dict[str, Any]:
    """Return the current heuristic Loto example grid."""
    return {
        "rule": "1 bloc bas consecutif + 1 bloc milieu + 1 bloc haut",
        "example": [9, 10, 25, 36, 41],
        "chance": 5,
        "warning": "Heuristic only; not a prediction.",
    }


@MCP.tool()
def get_statistics(game: str) -> dict[str, Any]:
    """Compute lightweight statistics for the latest normalized history."""
    records = get_history(game)
    if not records:
        return {"game": game, "count": 0}

    number_counts: dict[str, int] = {}
    for record in records:
        for number in record.get("numbers", []):
            key = str(number)
            number_counts[key] = number_counts.get(key, 0) + 1

    top_numbers = sorted(number_counts.items(), key=lambda item: (-item[1], int(item[0])))[:10]
    return {
        "game": game,
        "count": len(records),
        "top_numbers": top_numbers,
    }


@MCP.tool()
def search_history(game: str, number: int | None = None, bonus: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    """Search the normalized history by main number or bonus/star value."""
    records = get_history(game)
    matches: list[dict[str, Any]] = []
    for record in records:
        numbers = record.get("numbers", [])
        bonuses = record.get("bonus", [])
        if number is not None and number not in numbers:
            continue
        if bonus is not None and bonus not in {str(item) for item in bonuses}:
            continue
        matches.append(record)
        if len(matches) >= limit:
            break
    return matches


def main() -> None:
    MCP.run()


if __name__ == "__main__":
    main()
