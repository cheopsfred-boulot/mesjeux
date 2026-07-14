from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.data_store import balanced_loto_grid, compare_lists, game_statistics, latest_record, load_records, search_records
from app.models import GridCompareRequest, GameName, StorageStatus
from app.settings import DATA_DIR, has_neon, has_r2


app = FastAPI(
    title="MesJeux FDJ API",
    version="1.0.0",
    description="API FDJ locale et Vercel-compatible pour l'historique, les statistiques et les comparaisons.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, object]:
    return {
        "service": "mesjeux-fdj-api",
        "status": "ok",
        "games": ["loto", "euromillions", "crescendo"],
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "local_json": DATA_DIR.exists(),
        "neon": has_neon(),
        "r2": has_r2(),
    }


@app.get("/storage/status", response_model=StorageStatus)
def storage_status() -> StorageStatus:
    return StorageStatus(local_json=DATA_DIR.exists(), neon=has_neon(), r2=has_r2())


@app.get("/games")
def games() -> dict[str, list[str]]:
    return {"games": ["loto", "euromillions", "crescendo"]}


@app.get("/games/{game}/latest")
def get_latest(game: GameName) -> dict[str, object]:
    return latest_record(game)


@app.get("/games/{game}/history")
def get_history(game: GameName, limit: int = Query(default=50, ge=1, le=1000)) -> list[dict[str, object]]:
    records = load_records(game)
    return records[-limit:]


@app.get("/games/{game}/statistics")
def get_stats(game: GameName) -> dict[str, object]:
    return game_statistics(game)


@app.get("/games/{game}/search")
def search_history(game: GameName, number: int | None = None, bonus: str | None = None, limit: int = Query(default=20, ge=1, le=100)) -> list[dict[str, object]]:
    return search_records(game, number=number, bonus=bonus, limit=limit)


@app.post("/compare")
def compare_grid(payload: GridCompareRequest) -> dict[str, object]:
    return compare_lists(payload.played, payload.draw, payload.chance_played, payload.chance_drawn)


@app.get("/strategies/loto/balanced")
def strategy_loto_balanced() -> dict[str, object]:
    return balanced_loto_grid()


@app.get("/strategies/loto/recommendation")
def strategy_loto_recommendation() -> dict[str, object]:
    return {
        "disclaimer": "Heuristic only; not a prediction.",
        "grid": [9, 10, 25, 36, 41],
        "chance": 5,
    }


@app.get("/meta")
def meta() -> dict[str, object]:
    return {
        "local_json_exists": DATA_DIR.exists(),
        "games_loaded": {game: len(load_records(game)) for game in ("loto", "euromillions", "crescendo")},
    }


@app.get("/games/{game}")
def game_summary(game: GameName) -> dict[str, object]:
    records = load_records(game)
    if not records:
        raise HTTPException(status_code=404, detail="No records available")
    return {
        "game": game,
        "count": len(records),
        "latest": records[-1],
        "statistics": game_statistics(game),
    }

