"""Local MCP server for FDJ history, search, statistics, and grid comparison."""

from __future__ import annotations

import sys
from datetime import date as DateType
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MCP_DIR = Path(__file__).resolve().parent
for path in (ROOT, MCP_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "The 'mcp' package is required to run this server. Install it in the local Python environment."
    ) from exc

from app.data_store import (
    balanced_loto_grid,
    compare_lists,
    filter_records,
    game_statistics,
    game_snapshot,
    latest_record,
    load_records,
    search_records,
)
from app.exports import write_csv_file
from app.settings import DATA_DIR


MCP = FastMCP("fdj-history")
GAMES = ("loto", "euromillions", "crescendo")


def _validate_game(game: str) -> str:
    if game not in GAMES:
        raise ValueError(f"Unsupported game: {game}")
    return game


@MCP.tool()
def list_games() -> dict[str, Any]:
    """Return the supported games and local row counts."""
    return {
        "games": {
            game: {"records": len(load_records(game)), "csv_path": str(DATA_DIR / f"{game}.csv")}
            for game in GAMES
        }
    }


@MCP.tool()
def get_last_result(game: str) -> dict[str, Any]:
    """Return the latest normalized record for a game."""
    _validate_game(game)
    return latest_record(game)


@MCP.tool()
def get_history(
    game: str,
    limit: int = 1000,
    offset: int = 0,
    number: int | None = None,
    bonus: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict[str, Any]]:
    """Return normalized history with optional filtering."""
    _validate_game(game)
    records = load_records(game)
    return filter_records(
        records,
        number=number,
        bonus=bonus,
        date_from=DateType.fromisoformat(date_from) if date_from else None,
        date_to=DateType.fromisoformat(date_to) if date_to else None,
        offset=offset,
        limit=limit,
        newest_first=False,
    )


@MCP.tool()
def search_history(game: str, number: int | None = None, bonus: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    """Search the normalized history by main number or bonus/star value."""
    _validate_game(game)
    return search_records(game, number=number, bonus=bonus, limit=limit)


@MCP.tool()
def get_statistics(game: str) -> dict[str, Any]:
    """Compute lightweight statistics for the normalized history."""
    _validate_game(game)
    return game_statistics(game)


@MCP.tool()
def get_snapshot(game: str) -> dict[str, Any]:
    """Return a compact summary for UI or agent consumption."""
    _validate_game(game)
    return game_snapshot(game)


@MCP.tool()
def compare_grid_to_result(played: list[int], draw: list[int], chance_played: list[int] | None = None, chance_drawn: list[int] | None = None) -> dict[str, Any]:
    """Compare a played grid to a draw and return exact/missing numbers."""
    return compare_lists(played, draw, chance_played=chance_played, chance_drawn=chance_drawn)


@MCP.tool()
def generate_balanced_loto_grid() -> dict[str, Any]:
    """Return the current heuristic Loto example grid."""
    return balanced_loto_grid()


@MCP.tool()
def export_csv(game: str) -> dict[str, Any]:
    """Generate the CSV export for a game from the normalized local history."""
    _validate_game(game)
    records = load_records(game)
    output = write_csv_file(game, records, DATA_DIR / f"{game}.csv")
    return {"game": game, "records": len(records), "csv_path": str(output)}


def main() -> None:
    MCP.run()


if __name__ == "__main__":
    main()
