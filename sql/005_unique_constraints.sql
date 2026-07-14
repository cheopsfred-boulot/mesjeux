CREATE UNIQUE INDEX IF NOT EXISTS uq_fdj_draws_identity
ON fdj_draws (
  game,
  COALESCE(date, '1970-01-01'::date),
  COALESCE(draw_id, ''),
  COALESCE(draw_slot, -1),
  COALESCE(hour, ''),
  numbers,
  bonus,
  COALESCE(archive_segment, '')
);

