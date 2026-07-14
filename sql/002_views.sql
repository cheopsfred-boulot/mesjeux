CREATE OR REPLACE VIEW fdj_latest_draws AS
SELECT DISTINCT ON (game)
  game, date, date_display, draw_id, draw_slot, weekday, hour,
  numbers, bonus, source, source_csv, archive_segment, my_million, jackpot, raw, created_at, updated_at
FROM fdj_draws
ORDER BY game, COALESCE(date, date_display::date) DESC NULLS LAST, draw_id DESC NULLS LAST;

