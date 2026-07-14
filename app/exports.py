from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path
from typing import Any, Iterable


CSV_FIELDS = [
    "game",
    "date",
    "date_display",
    "draw_id",
    "draw_slot",
    "weekday",
    "hour",
    "numbers",
    "bonus",
    "source",
    "source_csv",
    "archive_segment",
    "my_million",
    "jackpot",
]


def _serialize_values(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value)


def record_to_csv_row(game: str, record: dict[str, Any]) -> dict[str, str]:
    return {
        "game": game,
        "date": _serialize_values(record.get("date")),
        "date_display": _serialize_values(record.get("date_display")),
        "draw_id": _serialize_values(record.get("draw_id")),
        "draw_slot": _serialize_values(record.get("draw_slot")),
        "weekday": _serialize_values(record.get("weekday")),
        "hour": _serialize_values(record.get("hour")),
        "numbers": _serialize_values(record.get("numbers", [])),
        "bonus": _serialize_values(record.get("bonus", [])),
        "source": _serialize_values(record.get("source")),
        "source_csv": _serialize_values(record.get("source_csv")),
        "archive_segment": _serialize_values(record.get("archive_segment")),
        "my_million": _serialize_values(record.get("my_million")),
        "jackpot": _serialize_values(record.get("jackpot")),
    }


def records_to_csv_text(game: str, records: Iterable[dict[str, Any]]) -> str:
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for record in records:
        writer.writerow(record_to_csv_row(game, record))
    return buffer.getvalue()


def write_csv_file(game: str, records: Iterable[dict[str, Any]], output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(records_to_csv_text(game, records), encoding="utf-8")
    return output
