# Guide d'utilisation

Ce guide resume le fonctionnement courant du projet `mesjeux`:

- lecture de l'historique FDJ normalise
- export CSV automatique
- exposition FastAPI
- usage du serveur MCP local
- mise a jour automatisee par cron

## 1. Lancer le projet en local

Installation:

```powershell
python -m pip install -r requirements.txt
```

Lancement de l'API:

```powershell
uvicorn app.main:app --reload
```

L'API sera accessible sur:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## 2. Lire les donnees

Les donnees normalisees vivent dans:

- `data/loto.json`
- `data/euromillions.json`
- `data/crescendo.json`

Les endpoints utiles:

- `GET /games/{game}/latest`
- `GET /games/{game}/history`
- `GET /games/{game}/history.csv`
- `GET /games/{game}/snapshot`
- `GET /games/{game}/statistics`
- `GET /games/{game}/search`

Exemples:

```powershell
curl http://127.0.0.1:8000/games/loto/snapshot
curl "http://127.0.0.1:8000/games/loto/history.csv?limit=5"
curl "http://127.0.0.1:8000/games/loto/search?number=31&limit=10"
```

## 3. Utiliser le serveur MCP local

Le serveur MCP lit directement l'historique local normalise et expose les outils suivants:

- `list_games`
- `get_last_result`
- `get_history`
- `search_history`
- `get_statistics`
- `get_snapshot`
- `compare_grid_to_result`
- `generate_balanced_loto_grid`
- `export_csv`

Lancement:

```powershell
python mcp\fdj_mcp_server.py
```

Configuration client MCP:

```json
{
  "mcpServers": {
    "fdj-history": {
      "command": "python",
      "args": ["C:\\projets\\mesjeux\\mcp\\fdj_mcp_server.py"]
    }
  }
}
```

Usage recommande:

- `get_snapshot("loto")` pour une vue tres compacte
- `get_history("loto", limit=20)` pour les derniers tirages
- `search_history("loto", number=31)` pour retrouver les tirages contenant un numero
- `compare_grid_to_result(...)` pour comparer une grille jouee a un tirage

## 4. Refresh des resultats

Le script central de mise a jour est:

```powershell
python scripts\refresh_all.py
```

Ce flux fait, dans l'ordre:

1. import des archives FDJ dans `data/*.json`
2. export CSV dans `data/*.csv`
3. regeneration des notes Markdown

Si tu veux aussi retoucher la base Neon ensuite:

```powershell
python scripts\sync_neon.py
```

## 5. Cron de mise a jour

Le principe recommande est simple:

- le cron lance `scripts\refresh_all.py`
- l'API et le MCP lisent ensuite les fichiers normalises et la base Neon
- le script PowerShell charge automatiquement `.env.local` puis `.env` si ces fichiers existent
- tu peux forcer l'interpreteur avec `PYTHON_EXE=C:\projets\python313\python.exe`

### Option Windows Task Scheduler

Commande de base a planifier:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\projets\mesjeux\scripts\cron_refresh.ps1" -FocusGame loto
```

### Trois taches Windows pretes a copier

Tu peux creer 3 taches distinctes dans le Planificateur de taches Windows.

#### Tache 1: Loto

- Nom: `FDJ - Refresh Loto`
- Declencheur: lundi, mercredi, samedi a 06:00
- Action:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\projets\mesjeux\scripts\cron_refresh.ps1" -FocusGame loto
```

#### Tache 2: EuroMillions

- Nom: `FDJ - Refresh EuroMillions`
- Declencheur: mardi, vendredi a 06:10
- Action:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\projets\mesjeux\scripts\cron_refresh.ps1" -FocusGame euromillions
```

#### Tache 3: Crescendo

- Nom: `FDJ - Refresh Crescendo`
- Declencheur: samedi a 06:20
- Action:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\projets\mesjeux\scripts\cron_refresh.ps1" -FocusGame crescendo
```

### Ce que fait le script

- rafraichit les archives et le JSON normalise
- met a jour Neon
- regenere les CSV via `refresh_all.py`
- affiche un snapshot compact du jeu cible pour verification
- charge automatiquement `.env.local` puis `.env` si ces fichiers existent

Fichier modele d'environnement local:

- [C:\projets\mesjeux\.env.local.example](C:\projets\mesjeux\.env.local.example)

### Option cron Linux

```cron
0 6 * * * cd /path/to/mesjeux && PYTHONPATH=. python scripts/refresh_all.py && PYTHONPATH=. python scripts/sync_neon.py
```

### Option GitHub Actions

Tu peux aussi lancer le meme flux chaque jour via un workflow planifie qui execute:

```bash
python scripts/refresh_all.py
python scripts/sync_neon.py
```

## 6. Regles de travail

- Ne pas presenter les grilles comme des predictions certaines.
- Utiliser `snapshot` pour un affichage rapide.
- Utiliser `history` pour l'historique detaille.
- Utiliser `refresh_all.py` comme source de verite pour la mise a jour locale.
- Utiliser `sync_neon.py` apres refresh si tu veux propager dans Neon.

## 7. Cas d'usage hebdomadaire

Tu peux organiser le suivi comme ceci:

- Loto: lundi, mercredi, samedi
- EuroMillions / My Million: mardi, vendredi
- Crescendo: samedi

### Loto

Le matin du lundi, mercredi et samedi:

```powershell
python scripts\refresh_all.py
curl http://127.0.0.1:8000/games/loto/snapshot
curl "http://127.0.0.1:8000/games/loto/history?limit=10"
```

Usage utile:

- comparer les grilles jouees avec `POST /compare`
- regarder les numeros qui reviennent le plus via `GET /games/loto/statistics`
- exporter le CSV via `GET /games/loto/history.csv`

### EuroMillions / My Million

Le mardi et le vendredi:

```powershell
python scripts\refresh_all.py
curl http://127.0.0.1:8000/games/euromillions/snapshot
curl "http://127.0.0.1:8000/games/euromillions/history?limit=10"
```

Usage utile:

- suivre les boules et les etoiles
- analyser la presence du code My Million via le champ `my_million`
- exporter le CSV via `GET /games/euromillions/history.csv`

### Crescendo

Le samedi:

```powershell
python scripts\refresh_all.py
curl http://127.0.0.1:8000/games/crescendo/snapshot
curl "http://127.0.0.1:8000/games/crescendo/history?limit=10"
```

Usage utile:

- verifier la progression des numeros de la grille
- regarder le dernier tirage disponible
- exporter le CSV via `GET /games/crescendo/history.csv`

### Routine simple conseillee

1. lancer `refresh_all.py`
2. lire `snapshot`
3. regarder `history` si besoin de detail
4. comparer les grilles avec `compare_grid_to_result`
5. si la base Neon est active, lancer `sync_neon.py`
