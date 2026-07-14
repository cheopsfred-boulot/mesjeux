# MesJeux FDJ

API FastAPI compatible Vercel pour l'historique FDJ, les statistiques simples,
la comparaison de grilles et la préparation d'un futur stockage Neon + R2.

## Ce qui est inclus

- lecture de l'historique normalisé FDJ
- comparaison grille / tirage
- statistiques simples
- règle de grille Loto équilibrée
- configuration Vercel

## Endpoints

- `GET /`
- `GET /health`
- `GET /games`
- `GET /games/{game}/latest`
- `GET /games/{game}/history`
- `GET /games/{game}/statistics`
- `GET /games/{game}/search`
- `POST /compare`
- `POST /media/presign`
- `POST /media/register`
- `GET /media`
- `GET /media/head`
- `POST /admin/neon/sync`
- `GET /strategies/loto/balanced`

## Scripts utiles

- `scripts/import_fdj_archives.py`
- `scripts/sync_neon.py`
- `scripts/apply_sql_migrations.py`
- `scripts/download_fdj_archives.py`
- `scripts/refresh_all.py`

## Schéma SQL

- `sql/001_init.sql`
- `sql/002_views.sql`
- `sql/003_sync_helpers.sql`
- `sql/004_media.sql`
- `sql/005_unique_constraints.sql`

## Flux média R2

1. appeler `POST /media/presign`
2. envoyer le fichier vers l’URL signée
3. appeler `POST /media/register` pour tracer l’asset en base
4. consulter `GET /media`

## Variables d'environnement prévues

- `NEON_DATABASE_URL`
- `R2_ACCOUNT_ID`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET`

## Lancement local

```powershell
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Vercel

Le dépôt contient `vercel.json` et `api/index.py`.
Une fois poussé sur GitHub, il peut être importé dans Vercel comme projet Python.

Guide détaillé : [docs/deploiement-vercel.md](./docs/deploiement-vercel.md)
Guide R2 : [docs/r2-cloudflare.md](./docs/r2-cloudflare.md)
