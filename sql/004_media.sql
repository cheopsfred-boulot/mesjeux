CREATE TABLE IF NOT EXISTS fdj_media_assets (
  id BIGSERIAL PRIMARY KEY,
  game TEXT NULL,
  kind TEXT NOT NULL,
  file_name TEXT NOT NULL,
  object_key TEXT NOT NULL UNIQUE,
  bucket TEXT NOT NULL,
  content_type TEXT NULL,
  size_bytes BIGINT NULL,
  source_url TEXT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fdj_media_assets_game_kind ON fdj_media_assets (game, kind);
CREATE INDEX IF NOT EXISTS idx_fdj_media_assets_object_key ON fdj_media_assets (object_key);

