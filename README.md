# MesJeux FDJ

API FastAPI compatible Vercel pour l'historique FDJ, les statistiques simples,
la comparaison de grilles et la préparation d'un futur stockage Neon + R2.

## Ce qui est inclus

- lecture de l'historique normalisé FDJ
- comparaison grille / tirage
- statistiques simples
- règle de grille Loto équilibrée
- export CSV automatique depuis `data/*.json`
- serveur MCP local pour l'historique normalisé
- routes FastAPI filtrables et exportables en CSV
- snapshot compact par jeu
- configuration Vercel

## Endpoints

- `GET /`
- `GET /health`
- `GET /games`
- `GET /games/{game}/latest`
- `GET /games/{game}/history`
- `GET /games/{game}/history.csv`
- `GET /games/{game}/snapshot`
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
- `scripts/export_csv.py`
- `scripts/cron_refresh.ps1`

## Serveur MCP local

Lancement:

```powershell
python mcp\fdj_mcp_server.py
```

Exemple de configuration client: [docs/mcp-local.md](./docs/mcp-local.md)

Outils principaux:

- `list_games`
- `get_last_result`
- `get_history`
- `search_history`
- `get_statistics`
- `get_snapshot`
- `compare_grid_to_result`
- `generate_balanced_loto_grid`
- `export_csv`

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
Guide d'utilisation : [docs/guide-utilisation.md](./docs/guide-utilisation.md)

Rythme d'usage recommandé:

- Loto: lundi, mercredi, samedi
- EuroMillions / My Million: mardi, vendredi
- Crescendo: samedi
