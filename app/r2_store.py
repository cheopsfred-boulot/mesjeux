from __future__ import annotations

import mimetypes
from functools import lru_cache
from typing import Any
from uuid import uuid4

import boto3
from botocore.client import Config

from app.settings import has_r2, r2_api_url, r2_bucket, r2_endpoint, env


@lru_cache(maxsize=1)
def get_client():
    if not has_r2():
        return None
    return boto3.client(
        "s3",
        endpoint_url=r2_endpoint(),
        aws_access_key_id=env("R2_ACCESS_KEY_ID"),
        aws_secret_access_key=env("R2_SECRET_ACCESS_KEY"),
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )


def r2_enabled() -> bool:
    return get_client() is not None


def r2_configuration() -> dict[str, Any]:
    return {
        "configured": has_r2(),
        "bucket": r2_bucket(),
        "endpoint": r2_endpoint(),
        "api_url": r2_api_url(),
    }


def build_object_key(prefix: str, filename: str) -> str:
    suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    safe_suffix = f".{suffix}" if suffix else ""
    return f"{prefix}/{uuid4().hex}{safe_suffix}"


def presign_upload(prefix: str, filename: str, content_type: str | None = None, expires_in: int = 3600) -> dict[str, Any]:
    client = get_client()
    bucket = r2_bucket()
    if client is None or bucket is None:
        raise RuntimeError("R2 is not configured")

    object_key = build_object_key(prefix, filename)
    inferred_content_type = content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"
    url = client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": object_key, "ContentType": inferred_content_type},
        ExpiresIn=expires_in,
    )
    public_url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": object_key},
        ExpiresIn=expires_in,
    )
    return {
        "bucket": bucket,
        "object_key": object_key,
        "upload_url": url,
        "download_url": public_url,
        "content_type": inferred_content_type,
        "expires_in": expires_in,
    }


def head_object(object_key: str) -> dict[str, Any]:
    client = get_client()
    bucket = r2_bucket()
    if client is None or bucket is None:
        raise RuntimeError("R2 is not configured")
    response = client.head_object(Bucket=bucket, Key=object_key)
    return {
        "bucket": bucket,
        "object_key": object_key,
        "content_type": response.get("ContentType"),
        "content_length": response.get("ContentLength"),
        "etag": response.get("ETag"),
        "last_modified": response.get("LastModified").isoformat() if response.get("LastModified") else None,
    }
