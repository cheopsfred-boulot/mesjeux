from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"


def env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def has_neon() -> bool:
    return bool(env("NEON_DATABASE_URL"))


def has_r2() -> bool:
    return all(
        env(name)
        for name in [
            "R2_ACCESS_KEY_ID",
            "R2_SECRET_ACCESS_KEY",
        ]
    ) and bool(r2_bucket())


def neon_dsn() -> str | None:
    return env("NEON_DATABASE_URL")


def r2_bucket() -> str | None:
    bucket = env("R2_BUCKET")
    if bucket:
        return bucket
    api_url = env("R2_S3_ENDPOINT") or env("R2_S3_URL")
    if api_url:
        path = urlsplit(api_url).path.strip("/")
        if path:
            return path.split("/")[0]
    return None


def r2_endpoint() -> str | None:
    api_url = env("R2_S3_ENDPOINT") or env("R2_S3_URL")
    if api_url:
        parsed = urlsplit(api_url)
        return f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else None
    account_id = env("R2_ACCOUNT_ID")
    if not account_id:
        return None
    return f"https://{account_id}.r2.cloudflarestorage.com"


def r2_api_url() -> str | None:
    return env("R2_S3_ENDPOINT") or env("R2_S3_URL")
