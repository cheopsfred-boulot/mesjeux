CREATE TABLE IF NOT EXISTS fdj_draws (
  id BIGSERIAL PRIMARY KEY,
  game TEXT NOT NULL,
  date DATE NULL,
  date_display TEXT NULL,
  draw_id TEXT NULL,
  draw_slot INTEGER NULL,
  weekday TEXT NULL,
  hour TEXT NULL,
  numbers INTEGER[] NOT NULL DEFAULT '{}',
  bonus TEXT[] NOT NULL DEFAULT '{}',
  source TEXT NULL,
  source_csv TEXT NULL,
  archive_segment TEXT NULL,
  my_million TEXT NULL,
  jackpot TEXT NULL,
  raw JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fdj_draws_game_date ON fdj_draws (game, date DESC);
CREATE INDEX IF NOT EXISTS idx_fdj_draws_game_draw_id ON fdj_draws (game, draw_id DESC);
CREATE INDEX IF NOT EXISTS idx_fdj_draws_numbers_gin ON fdj_draws USING GIN (numbers);
CREATE INDEX IF NOT EXISTS idx_fdj_draws_bonus_gin ON fdj_draws USING GIN (bonus);

