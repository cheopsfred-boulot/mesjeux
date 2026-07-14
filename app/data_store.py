from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.models import GameName
from app.settings import DATA_DIR


def _path_for_game(game: GameName) -> Path:
    return DATA_DIR / f"{game}.json"


@lru_cache(maxsize=8)
def load_records(game: GameName) -> list[dict[str, Any]]:
    path = _path_for_game(game)
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else []


def latest_record(game: GameName) -> dict[str, Any]:
    records = load_records(game)
    return records[-1] if records else {}


def search_records(game: GameName, number: int | None = None, bonus: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for record in load_records(game):
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


def compare_lists(
    played: list[int],
    draw: list[int],
    chance_played: list[int] | None = None,
    chance_drawn: list[int] | None = None,
) -> dict[str, Any]:
    chance_played = chance_played or []
    chance_drawn = chance_drawn or []
    exact = sorted(set(played) & set(draw))
    chance_exact = sorted(set(chance_played) & set(chance_drawn))
    return {
        "played": played,
        "draw": draw,
        "exact_matches": exact,
        "played_only": sorted(set(played) - set(draw)),
        "draw_only": sorted(set(draw) - set(played)),
        "match_count": len(exact),
        "chance_played": chance_played,
        "chance_drawn": chance_drawn,
        "chance_exact_matches": chance_exact,
        "chance_match_count": len(chance_exact),
    }


def game_statistics(game: GameName) -> dict[str, Any]:
    records = load_records(game)
    if not records:
        return {"game": game, "count": 0, "top_numbers": []}

    counts: dict[str, int] = {}
    bonus_counts: dict[str, int] = {}
    for record in records:
        for number in record.get("numbers", []):
            key = str(number)
            counts[key] = counts.get(key, 0) + 1
        for bonus in record.get("bonus", []):
            key = str(bonus)
            bonus_counts[key] = bonus_counts.get(key, 0) + 1

    top_numbers = sorted(counts.items(), key=lambda item: (-item[1], int(item[0])))[:10]
    top_bonus = sorted(bonus_counts.items(), key=lambda item: (-item[1], item[0]))[:10]
    return {
        "game": game,
        "count": len(records),
        "top_numbers": top_numbers,
        "top_bonus": top_bonus,
    }


def balanced_loto_grid() -> dict[str, Any]:
    return {
        "rule": "1 bloc bas consecutif + 1 bloc milieu + 1 bloc haut",
        "example": [9, 10, 25, 36, 41],
        "chance": 5,
        "warning": "Heuristic only; not a prediction.",
    }

