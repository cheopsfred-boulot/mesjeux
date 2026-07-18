from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.settings import DATA_DIR, neon_dsn, has_neon


def _path_for_game(game: str) -> Path:
    return DATA_DIR / f"{game}.json"


@lru_cache(maxsize=1)
def get_connection() -> psycopg.Connection[Any] | None:
    dsn = neon_dsn()
    if not dsn:
        return None
    try:
        return psycopg.connect(dsn, row_factory=dict_row, autocommit=True)
    except Exception:
        return None


def neon_enabled() -> bool:
    return has_neon() and get_connection() is not None


def fetch_latest(game: str) -> dict[str, Any]:
    conn = get_connection()
    if conn is None:
        return {}
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT game, date, date_display, draw_id, draw_slot, weekday, hour,
                   numbers, bonus, source, source_csv, archive_segment,
                   my_million, jackpot, raw
            FROM fdj_draws
            WHERE game = %s
            ORDER BY date DESC NULLS LAST, draw_id DESC NULLS LAST
            LIMIT 1
            """,
            (game,),
        )
        row = cur.fetchone()
        return dict(row) if row else {}


def fetch_history(game: str, limit: int = 50) -> list[dict[str, Any]]:
    conn = get_connection()
    if conn is None:
        return []
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT game, date, date_display, draw_id, draw_slot, weekday, hour,
                   numbers, bonus, source, source_csv, archive_segment,
                   my_million, jackpot, raw
            FROM fdj_draws
            WHERE game = %s
            ORDER BY date DESC NULLS LAST, draw_id DESC NULLS LAST
            LIMIT %s
            """,
            (game, limit),
        )
        return [dict(row) for row in cur.fetchall()]


def fetch_search(game: str, number: int | None = None, bonus: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    conn = get_connection()
    if conn is None:
        return []
    clauses = ["game = %s"]
    params: list[Any] = [game]
    if number is not None:
        clauses.append("%s = ANY(numbers)")
        params.append(number)
    if bonus is not None:
        clauses.append("%s = ANY(bonus)")
        params.append(bonus)
    params.append(limit)
    query = f"""
        SELECT game, date, date_display, draw_id, draw_slot, weekday, hour,
               numbers, bonus, source, source_csv, archive_segment,
               my_million, jackpot, raw
        FROM fdj_draws
        WHERE {" AND ".join(clauses)}
        ORDER BY date DESC NULLS LAST, draw_id DESC NULLS LAST
        LIMIT %s
    """
    with conn.cursor() as cur:
        cur.execute(query, params)
        return [dict(row) for row in cur.fetchall()]


def fetch_statistics(game: str) -> dict[str, Any]:
    conn = get_connection()
    if conn is None:
        return {"game": game, "count": 0, "top_numbers": [], "top_bonus": []}
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*) AS count
            FROM fdj_draws
            WHERE game = %s
            """,
            (game,),
        )
        count = cur.fetchone()["count"]

        cur.execute(
            """
            SELECT n::text AS number, COUNT(*) AS count
            FROM fdj_draws, LATERAL unnest(numbers) AS n
            WHERE game = %s
            GROUP BY n
            ORDER BY COUNT(*) DESC, n ASC
            LIMIT 10
            """,
            (game,),
        )
        top_numbers = [(row["number"], row["count"]) for row in cur.fetchall()]

        cur.execute(
            """
            SELECT b::text AS bonus, COUNT(*) AS count
            FROM fdj_draws, LATERAL unnest(bonus) AS b
            WHERE game = %s
            GROUP BY b
            ORDER BY COUNT(*) DESC, b ASC
            LIMIT 10
            """,
            (game,),
        )
        top_bonus = [(row["bonus"], row["count"]) for row in cur.fetchall()]

    return {"game": game, "count": count, "top_numbers": top_numbers, "top_bonus": top_bonus}


def insert_media_asset(payload: dict[str, Any]) -> dict[str, Any]:
    conn = get_connection()
    if conn is None:
        return {}
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO fdj_media_assets (
              game, kind, file_name, object_key, bucket, content_type,
              size_bytes, source_url, metadata
            )
            VALUES (
              %(game)s, %(kind)s, %(file_name)s, %(object_key)s, %(bucket)s,
              %(content_type)s, %(size_bytes)s, %(source_url)s, %(metadata)s::jsonb
            )
            ON CONFLICT (object_key) DO UPDATE SET
              game = EXCLUDED.game,
              kind = EXCLUDED.kind,
              file_name = EXCLUDED.file_name,
              bucket = EXCLUDED.bucket,
              content_type = EXCLUDED.content_type,
              size_bytes = EXCLUDED.size_bytes,
              source_url = EXCLUDED.source_url,
              metadata = EXCLUDED.metadata,
              created_at = now()
            RETURNING id, game, kind, file_name, object_key, bucket, content_type, size_bytes, source_url, metadata, created_at
            """,
            {
                **payload,
                "metadata": payload.get("metadata", {}),
            },
        )
        row = cur.fetchone()
        return dict(row) if row else {}


def list_media_assets(game: str | None = None, kind: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
    conn = get_connection()
    if conn is None:
        return []
    clauses: list[str] = []
    params: list[Any] = []
    if game:
        clauses.append("game = %s")
        params.append(game)
    if kind:
        clauses.append("kind = %s")
        params.append(kind)
    params.append(limit)
    query = """
        SELECT id, game, kind, file_name, object_key, bucket, content_type, size_bytes, source_url, metadata, created_at
        FROM fdj_media_assets
    """
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY created_at DESC LIMIT %s"
    with conn.cursor() as cur:
        cur.execute(query, params)
        return [dict(row) for row in cur.fetchall()]
