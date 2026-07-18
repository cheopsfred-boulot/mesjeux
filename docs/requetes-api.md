# Requetes API MesJeux

Ce fichier sert de pense-bete pour interroger rapidement l'API MesJeux.

Base publique Vercel :

```text
https://mesjeux.vercel.app
```

Base locale, si le serveur FastAPI tourne sur la machine :

```text
http://127.0.0.1:8000
```

## Commandes locales rapides

### Le plus simple

```bash
curl http://127.0.0.1:8000/games/euromillions/latest
```

### Pour voir un resume rapide

```bash
curl http://127.0.0.1:8000/games/euromillions/snapshot
```

### Pour voir l'historique recent

```bash
curl "http://127.0.0.1:8000/games/euromillions/history?limit=5"
```

## Commandes rapides sur Vercel

### Le plus simple

```bash
curl https://mesjeux.vercel.app/games/euromillions/latest
```

### Pour voir un resume rapide

```bash
curl https://mesjeux.vercel.app/games/euromillions/snapshot
```

### Pour voir l'historique recent

```bash
curl "https://mesjeux.vercel.app/games/euromillions/history?limit=5"
```

### Pour voir plus d'historique

```bash
curl "https://mesjeux.vercel.app/games/euromillions/history?limit=100"
```

## PROMPTS VERCEL A COPIER

### Prompt Vercel pour generer un algorithme prudent

```text
Tu es un assistant d'analyse FDJ.
Utilise l'API publique Vercel MesJeux comme source :
https://mesjeux.vercel.app/games/euromillions/latest
https://mesjeux.vercel.app/games/euromillions/snapshot
https://mesjeux.vercel.app/games/euromillions/history?limit=100

Objectif :
Genere un algorithme simple pour proposer des numeros EuroMillions equilibres.

Contraintes :
1. Base-toi sur les sorties historiques, les unites, les dizaines et des statistiques simples.
2. Analyse la repartition par dizaines : 1-9, 10-19, 20-29, 30-39, 40-50.
3. Analyse les unites finales : 0, 1, 2, 3, 4, 5, 6, 7, 8, 9.
4. Analyse les pairs/impairs et bas/hauts.
5. Analyse les etoiles separement.
6. Evite les suites trop visibles, les grilles trop concentrees et les repetitions excessives.
7. Propose 5 grilles equilibrees avec une explication courte pour chaque grille.
8. Dis clairement que les grilles ne sont pas des predictions certaines et ne garantissent aucun gain.
```

### Prompt Vercel pour demander les derniers numeros

```text
Interroge cette API :
https://mesjeux.vercel.app/games/euromillions/latest

Donne-moi le dernier tirage EuroMillions sous forme lisible :
Date, numeros, etoiles, My Million si disponible.
Ajoute une phrase de prudence si la date du dernier tirage ne correspond pas au tirage attendu le plus recent.
```

### Prompt Vercel pour analyser avant de proposer une grille

```text
Utilise ces endpoints Vercel :
https://mesjeux.vercel.app/games/euromillions/latest
https://mesjeux.vercel.app/games/euromillions/snapshot
https://mesjeux.vercel.app/games/euromillions/history?limit=50

Analyse :
1. Les numeros les plus presents.
2. Les numeros moins presents.
3. La repartition par dizaines.
4. Les unites finales.
5. Les etoiles les plus presentes.
6. Les ecarts simples entre derniers tirages.

Ensuite, propose 3 grilles EuroMillions equilibrees.
Chaque grille doit contenir 5 numeros et 2 etoiles.
Ne fais aucune promesse de prediction ou de gain.
```

## Derniers resultats

### Crescendo

```powershell
Invoke-RestMethod https://mesjeux.vercel.app/games/crescendo/latest
```

```bash
curl https://mesjeux.vercel.app/games/crescendo/latest
```

### EuroMillions

```powershell
Invoke-RestMethod https://mesjeux.vercel.app/games/euromillions/latest
```

```bash
curl https://mesjeux.vercel.app/games/euromillions/latest
```

### Loto

```powershell
Invoke-RestMethod https://mesjeux.vercel.app/games/loto/latest
```

```bash
curl https://mesjeux.vercel.app/games/loto/latest
```

## Snapshots compacts

Les snapshots sont utiles pour une interface, un agent ou une reponse courte.

```powershell
Invoke-RestMethod https://mesjeux.vercel.app/games/crescendo/snapshot
Invoke-RestMethod https://mesjeux.vercel.app/games/euromillions/snapshot
Invoke-RestMethod https://mesjeux.vercel.app/games/loto/snapshot
```

## Historique

```powershell
Invoke-RestMethod "https://mesjeux.vercel.app/games/crescendo/history?limit=20"
Invoke-RestMethod "https://mesjeux.vercel.app/games/euromillions/history?limit=20"
Invoke-RestMethod "https://mesjeux.vercel.app/games/loto/history?limit=20"
```

## Export CSV

```powershell
Invoke-WebRequest https://mesjeux.vercel.app/games/crescendo/history.csv -OutFile data\crescendo-api.csv
Invoke-WebRequest https://mesjeux.vercel.app/games/euromillions/history.csv -OutFile data\euromillions-api.csv
Invoke-WebRequest https://mesjeux.vercel.app/games/loto/history.csv -OutFile data\loto-api.csv
```

## Comparer une grille

Exemple EuroMillions :

```powershell
$body = @{
  numbers = @(2, 14, 28, 33, 48)
  bonus = @("8", "10")
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri https://mesjeux.vercel.app/games/euromillions/compare `
  -ContentType "application/json" `
  -Body $body
```

## Cas d'usage en prompt

Ces prompts servent a analyser l'historique et a produire des grilles equilibrees. Ils ne doivent jamais presenter une grille comme une prediction certaine.

### Generer une grille equilibree EuroMillions

```text
Base-toi sur l'historique EuroMillions disponible via l'API locale.
Analyse les derniers tirages, les unites, les dizaines, les etoiles, la repartition pairs/impairs et bas/hauts.
Genere 3 grilles EuroMillions equilibrees.
Explique pour chaque grille la logique statistique simple utilisee.
Ne presente jamais ces grilles comme des predictions certaines.
Endpoint utile :
http://127.0.0.1:8000/games/euromillions/history?limit=50
```

### Chercher des numeros qui ressortent souvent

```text
Analyse l'historique EuroMillions recent.
Liste les numeros et etoiles les plus frequents sur les 50 derniers tirages.
Separe l'analyse par dizaines : 1-9, 10-19, 20-29, 30-39, 40-50.
Propose ensuite une grille equilibree qui melange numeros frequents, numeros moyens et numeros moins sortis.
Rappelle que ce n'est pas une prediction certaine.
Endpoint utile :
http://127.0.0.1:8000/games/euromillions/history?limit=50
```

### Eviter les grilles trop simples

```text
Compare cette grille avec le dernier tirage EuroMillions et avec les tendances recentes :
Numeros : 2, 14, 28, 33, 48
Etoiles : 8, 10

Verifie si elle est trop concentree sur une meme dizaine, trop paire ou impaire, trop basse ou trop haute.
Propose une version plus equilibree si necessaire.
Ne fais aucune promesse de gain.
Endpoints utiles :
http://127.0.0.1:8000/games/euromillions/latest
http://127.0.0.1:8000/games/euromillions/snapshot
```

### Generer une grille Loto equilibree

```text
Base-toi sur l'historique Loto disponible via l'API locale.
Analyse les dizaines, les unites, les numeros pairs/impairs et la repartition bas/hauts.
Genere 3 grilles Loto equilibrees avec un numero chance.
Explique les criteres utilises.
Ne presente pas les grilles comme des predictions.
Endpoint utile :
http://127.0.0.1:8000/games/loto/history?limit=50
```

### Analyser Crescendo

```text
Base-toi sur l'historique Crescendo disponible via l'API locale.
Recupere le dernier resultat et l'historique recent.
Analyse les repetitions, les dizaines et les ecarts simples.
Propose une lecture statistique prudente et une grille equilibree si le format du jeu le permet.
Ne presente pas cette grille comme une prediction certaine.
Endpoints utiles :
http://127.0.0.1:8000/games/crescendo/latest
http://127.0.0.1:8000/games/crescendo/history?limit=50
```

### Prompt complet pour un agent

```text
Tu es un assistant d'analyse FDJ.
Utilise uniquement les donnees de l'API MesJeux locale.
Commence par appeler :
http://127.0.0.1:8000/games/euromillions/latest
http://127.0.0.1:8000/games/euromillions/snapshot
http://127.0.0.1:8000/games/euromillions/history?limit=100

Objectif :
1. Resumer le dernier tirage.
2. Analyser les tendances simples : dizaines, unites, pairs/impairs, bas/hauts, etoiles.
3. Identifier les ecarts visibles entre tirages recents.
4. Generer 5 grilles equilibrees.
5. Expliquer les regles appliquees.
6. Rappeler clairement que ce ne sont pas des predictions certaines.
```

### Prompt Vercel pour generer un algorithme prudent

```text
Tu es un assistant d'analyse FDJ.
Utilise l'API publique Vercel MesJeux comme source :
https://mesjeux.vercel.app/games/euromillions/latest
https://mesjeux.vercel.app/games/euromillions/snapshot
https://mesjeux.vercel.app/games/euromillions/history?limit=100

Objectif :
Genere un algorithme simple pour proposer des numeros EuroMillions equilibres.

Contraintes :
1. Base-toi sur les sorties historiques, les unites, les dizaines et des statistiques simples.
2. Analyse la repartition par dizaines : 1-9, 10-19, 20-29, 30-39, 40-50.
3. Analyse les unites finales : 0, 1, 2, 3, 4, 5, 6, 7, 8, 9.
4. Analyse les pairs/impairs et bas/hauts.
5. Analyse les etoiles separement.
6. Evite les suites trop visibles, les grilles trop concentrees et les repetitions excessives.
7. Propose 5 grilles equilibrees avec une explication courte pour chaque grille.
8. Dis clairement que les grilles ne sont pas des predictions certaines et ne garantissent aucun gain.
```

### Prompt Vercel pour demander les derniers numeros

```text
Interroge cette API :
https://mesjeux.vercel.app/games/euromillions/latest

Donne-moi le dernier tirage EuroMillions sous forme lisible :
Date, numeros, etoiles, My Million si disponible.
Ajoute une phrase de prudence si la date du dernier tirage ne correspond pas au tirage attendu le plus recent.
```

### Prompt Vercel pour analyser avant de proposer une grille

```text
Utilise ces endpoints Vercel :
https://mesjeux.vercel.app/games/euromillions/latest
https://mesjeux.vercel.app/games/euromillions/snapshot
https://mesjeux.vercel.app/games/euromillions/history?limit=50

Analyse :
1. Les numeros les plus presents.
2. Les numeros moins presents.
3. La repartition par dizaines.
4. Les unites finales.
5. Les etoiles les plus presentes.
6. Les ecarts simples entre derniers tirages.

Ensuite, propose 3 grilles EuroMillions equilibrees.
Chaque grille doit contenir 5 numeros et 2 etoiles.
Ne fais aucune promesse de prediction ou de gain.
```

## Mise a jour manuelle

Depuis `C:\projets\mesjeux` :

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\projets\mesjeux\scripts\cron_refresh.ps1" -FocusGame loto
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\projets\mesjeux\scripts\cron_refresh.ps1" -FocusGame euromillions
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\projets\mesjeux\scripts\cron_refresh.ps1" -FocusGame crescendo
```

## Important

Les grilles generees ou comparees ne sont jamais des predictions certaines. Le projet sert a suivre l'historique, comparer des strategies, calculer des tendances simples et generer des grilles equilibrees.
