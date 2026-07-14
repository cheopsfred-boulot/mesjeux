from __future__ import annotations

from datetime import date as DateType
from typing import Any, Literal

from pydantic import BaseModel, Field


GameName = Literal["loto", "euromillions", "crescendo"]


class GridCompareRequest(BaseModel):
    played: list[int] = Field(default_factory=list)
    draw: list[int] = Field(default_factory=list)
    chance_played: list[int] = Field(default_factory=list)
    chance_drawn: list[int] = Field(default_factory=list)
    game: GameName | None = None


class DrawRecord(BaseModel):
    game: GameName
    date: DateType | None = None
    date_display: str | None = None
    draw_id: str | None = None
    draw_slot: int | None = None
    weekday: str | None = None
    hour: str | None = None
    numbers: list[int] = Field(default_factory=list)
    bonus: list[int | str] = Field(default_factory=list)
    source: str | None = None
    source_csv: str | None = None
    archive_segment: str | None = None
    my_million: str | None = None
    jackpot: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class StorageStatus(BaseModel):
    local_json: bool
    neon: bool
    r2: bool
