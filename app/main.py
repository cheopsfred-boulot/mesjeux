from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.data_store import balanced_loto_grid, compare_lists, game_statistics, latest_record, load_records, search_records
from app.models import GameName, GridCompareRequest, MediaRegisterRequest, PresignRequest, PresignResponse, StorageStatus
from app.neon_store import insert_media_asset, list_media_assets
from app.r2_store import head_object, presign_upload, r2_configuration, r2_enabled
from app.settings import DATA_DIR, has_neon, has_r2
from app.neon_store import neon_enabled
from app.sync_service import load_rows, sync_game


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


@app.get("/storage/r2")
def storage_r2_status() -> dict[str, object]:
    return {"r2": r2_enabled(), **r2_configuration()}


@app.get("/storage/neon")
def storage_neon_status() -> dict[str, object]:
    return {"neon": neon_enabled(), "configured": has_neon()}


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


@app.post("/media/presign", response_model=PresignResponse)
def media_presign(payload: PresignRequest) -> PresignResponse:
    prefix = payload.game or "general"
    return PresignResponse(**presign_upload(prefix=prefix, filename=payload.filename, content_type=payload.content_type, expires_in=payload.expires_in))


@app.get("/media/head")
def media_head(object_key: str) -> dict[str, object]:
    try:
        return head_object(object_key)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/media/register")
def media_register(payload: MediaRegisterRequest) -> dict[str, object]:
    if not neon_enabled():
        raise HTTPException(status_code=400, detail="Neon is not configured")
    record = insert_media_asset(payload.model_dump())
    if not record:
        raise HTTPException(status_code=500, detail="Unable to register media asset")
    return record


@app.get("/media")
def media_list(game: GameName | None = None, kind: str | None = None, limit: int = Query(default=50, ge=1, le=200)) -> list[dict[str, object]]:
    if not neon_enabled():
        return []
    return list_media_assets(game=game, kind=kind, limit=limit)


@app.post("/admin/neon/sync")
def admin_sync_neon(game: GameName | None = None) -> dict[str, object]:
    if not neon_enabled():
        raise HTTPException(status_code=400, detail="Neon is not configured")
    games = [game] if game else ["loto", "euromillions", "crescendo"]
    total = 0
    for item in games:
        total += sync_game(item, load_rows(item))
    return {"synced": total, "games": games}


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
