CREATE OR REPLACE FUNCTION fdj_touch_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_fdj_touch_updated_at ON fdj_draws;
CREATE TRIGGER trg_fdj_touch_updated_at
BEFORE UPDATE ON fdj_draws
FOR EACH ROW
EXECUTE FUNCTION fdj_touch_updated_at();

