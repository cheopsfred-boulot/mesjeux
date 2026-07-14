from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.neon_store import get_connection
from app.settings import DATA_DIR


def load_rows(game: str) -> list[dict[str, Any]]:
    path = DATA_DIR / f"{game}.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else []


def sync_game(game: str, rows: list[dict[str, Any]]) -> int:
    conn = get_connection()
    if conn is None:
        return 0
    inserted = 0
    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                """
                INSERT INTO fdj_draws (
                  game, date, date_display, draw_id, draw_slot, weekday, hour,
                  numbers, bonus, source, source_csv, archive_segment,
                  my_million, jackpot, raw
                )
                VALUES (
                  %(game)s, %(date)s, %(date_display)s, %(draw_id)s, %(draw_slot)s,
                  %(weekday)s, %(hour)s, %(numbers)s, %(bonus)s, %(source)s,
                  %(source_csv)s, %(archive_segment)s, %(my_million)s,
                  %(jackpot)s, %(raw)s::jsonb
                )
                ON CONFLICT DO NOTHING
                """,
                {
                    "game": row.get("game", game),
                    "date": row.get("date"),
                    "date_display": row.get("date_display"),
                    "draw_id": row.get("draw_id"),
                    "draw_slot": row.get("draw_slot"),
                    "weekday": row.get("weekday"),
                    "hour": row.get("hour"),
                    "numbers": row.get("numbers", []),
                    "bonus": [str(item) for item in row.get("bonus", [])],
                    "source": row.get("source"),
                    "source_csv": row.get("source_csv"),
                    "archive_segment": row.get("archive_segment"),
                    "my_million": row.get("my_million"),
                    "jackpot": row.get("jackpot"),
                    "raw": json.dumps(row.get("raw", row), ensure_ascii=False),
                },
            )
            inserted += cur.rowcount or 0
    return inserted

