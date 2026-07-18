from __future__ import annotations

import json
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.models import GameName
from app.neon_store import fetch_history as neon_fetch_history
from app.neon_store import fetch_latest as neon_fetch_latest
from app.neon_store import fetch_search as neon_fetch_search
from app.neon_store import fetch_statistics as neon_fetch_statistics
from app.neon_store import neon_enabled
from app.settings import DATA_DIR


def _path_for_game(game: GameName) -> Path:
    return DATA_DIR / f"{game}.json"


@lru_cache(maxsize=8)
def load_records(game: GameName) -> list[dict[str, Any]]:
    if neon_enabled():
        records = neon_fetch_history(game, limit=100000)
        if records:
            return records
    path = _path_for_game(game)
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else []


def parse_record_date(value: Any) -> date | None:
    if value is None or isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None

    text = value.strip()
    if not text:
        return None

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def filter_records(
    records: list[dict[str, Any]],
    *,
    number: int | None = None,
    bonus: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    offset: int = 0,
    limit: int | None = None,
    newest_first: bool = False,
) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for record in records:
        record_date = parse_record_date(record.get("date"))
        if date_from and record_date and record_date < date_from:
            continue
        if date_to and record_date and record_date > date_to:
            continue
        if number is not None and number not in record.get("numbers", []):
            continue
        if bonus is not None and bonus not in {str(item) for item in record.get("bonus", [])}:
            continue
        filtered.append(record)

    filtered.sort(
        key=lambda record: (
            parse_record_date(record.get("date")) or date.min,
            str(record.get("draw_id") or ""),
            int(record.get("draw_slot") or -1),
        ),
        reverse=newest_first,
    )
    if offset:
        filtered = filtered[offset:]
    if limit is not None:
        filtered = filtered[:limit]
    return filtered


def latest_record(game: GameName) -> dict[str, Any]:
    if neon_enabled():
        record = neon_fetch_latest(game)
        if record:
            return record
    records = load_records(game)
    return records[-1] if records else {}


def search_records(
    game: GameName,
    number: int | None = None,
    bonus: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[dict[str, Any]]:
    if neon_enabled() and date_from is None and date_to is None and offset == 0:
        records = neon_fetch_search(game, number=number, bonus=bonus, limit=limit)
        if records:
            return records
    return filter_records(
        load_records(game),
        number=number,
        bonus=bonus,
        date_from=date_from,
        date_to=date_to,
        offset=offset,
        limit=limit,
        newest_first=True,
    )


def history_records(
    game: GameName,
    *,
    number: int | None = None,
    bonus: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    offset: int = 0,
    limit: int = 1000,
) -> list[dict[str, Any]]:
    if neon_enabled() and number is None and bonus is None and date_from is None and date_to is None:
        records = neon_fetch_history(game, limit=limit + offset)
        if records:
            return records[offset: offset + limit]
    return filter_records(
        load_records(game),
        number=number,
        bonus=bonus,
        date_from=date_from,
        date_to=date_to,
        offset=offset,
        limit=limit,
        newest_first=True,
    )


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
    if neon_enabled():
        stats = neon_fetch_statistics(game)
        if stats.get("count", 0):
            return stats
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


def game_snapshot(game: GameName, recent_limit: int = 3) -> dict[str, Any]:
    records = load_records(game)
    latest = latest_record(game)
    stats = game_statistics(game)
    recent_records = records[-recent_limit:] if recent_limit > 0 else []
    return {
        "game": game,
        "count": stats.get("count", len(records)),
        "latest": latest,
        "top_numbers": stats.get("top_numbers", []),
        "top_bonus": stats.get("top_bonus", []),
        "recent": recent_records,
        "sources": {
            "local_json": bool(records),
            "neon": neon_enabled(),
        },
    }


def balanced_loto_grid() -> dict[str, Any]:
    return {
        "rule": "1 bloc bas consecutif + 1 bloc milieu + 1 bloc haut",
        "example": [9, 10, 25, 36, 41],
        "chance": 5,
        "warning": "Heuristic only; not a prediction.",
    }
