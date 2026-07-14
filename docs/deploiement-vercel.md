# Déploiement Vercel

## Prérequis

- le dépôt GitHub `cheopsfred-boulot/mesjeux`
- un projet Vercel relié au dépôt
- des variables d’environnement configurées dans Vercel

## Variables à définir dans Vercel

- `NEON_DATABASE_URL`
- `R2_ACCOUNT_ID`
- `R2_S3_ENDPOINT`
- `R2_S3_URL`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET`

## Étapes recommandées

1. Importer le dépôt dans Vercel.
2. Vérifier que la racine du projet est bien la racine du dépôt.
3. Configurer les variables d’environnement.
4. Laisser le build Python s’exécuter avec `api/index.py`.
5. Vérifier les routes :
   - `/health`
   - `/games/loto/latest`
   - `/games/loto/statistics`
   - `/strategies/loto/balanced`
6. Si Neon est branché, lancer la synchronisation :
   - `POST /admin/neon/sync`
7. Si R2 est branché, tester :
   - `POST /media/presign`
   - `POST /media/register`

## Cas R2 avec URL S3 complète

Si tu n’as que quelque chose comme :

`https://ae3310e8b16fc62752748432f8cbc8e7.r2.cloudflarestorage.com/mesjeux`

alors :

- le bucket est `mesjeux`
- l’endpoint S3 est `https://ae3310e8b16fc62752748432f8cbc8e7.r2.cloudflarestorage.com`
- tu peux le mettre dans `R2_S3_ENDPOINT` ou `R2_S3_URL`
- il faut toujours `R2_ACCESS_KEY_ID` et `R2_SECRET_ACCESS_KEY`

## Vérifications utiles

- `GET /health` doit répondre `200`.
- `GET /storage/status` doit afficher les services activés.
- `GET /games/loto/statistics` doit retourner un compteur non nul.

## Conseils

- Garder l’historique local en JSON comme fallback.
- Brancher Neon seulement après la validation du déploiement.
- Utiliser R2 pour les images et captures plutôt que pour les données de jeu.
