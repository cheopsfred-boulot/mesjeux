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
- `GET /strategies/loto/balanced`

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

