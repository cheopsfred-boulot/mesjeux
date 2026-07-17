# Fiche rapide

## Jeux

- Loto
- EuroMillions / My Million
- Crescendo

## Noms acceptes

- `loto`
- `euromillions`
- `crescendo`

## Alias toleres

- `euromillion` -> `euromillions`
- `crecndo` -> `crescendo`
- `cresendo` -> `crescendo`

## Commandes utiles

### Refresh complet

```powershell
python scripts\refresh_all.py
```

### Synchro Neon

```powershell
python scripts\sync_neon.py
```

### Interrogation Neon

```powershell
curl http://127.0.0.1:8000/storage/neon
curl http://127.0.0.1:8000/games/loto/snapshot
curl "http://127.0.0.1:8000/games/loto/history?limit=5"
curl "http://127.0.0.1:8000/games/loto/statistics"
curl -X POST http://127.0.0.1:8000/admin/neon/sync
```

### Export CSV

```powershell
python scripts\export_csv.py --all
```

### Snapshot ultra-compact

```powershell
curl http://127.0.0.1:8000/games/loto/snapshot
```

### Historique CSV

```powershell
curl "http://127.0.0.1:8000/games/loto/history.csv?limit=1"
```

### Serveur MCP local

```powershell
python mcp\fdj_mcp_server.py
```

### Cron Windows

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\projets\mesjeux\scripts\cron_refresh.ps1" -FocusGame loto
```

## Rappels

- Ne jamais presenter les grilles comme des predictions certaines.
- Utiliser `snapshot` pour un resume rapide.
- Utiliser `history` pour le detail.
- Utiliser `/storage/neon` et `/admin/neon/sync` pour verifier/synchroniser Neon.
- Utiliser `compare_grid_to_result` pour comparer une grille a un tirage.
