# Déploiement Vercel

## Prérequis

- le dépôt GitHub `cheopsfred-boulot/mesjeux`
- un projet Vercel relié au dépôt
- des variables d’environnement configurées dans Vercel

## Variables à définir dans Vercel

- `NEON_DATABASE_URL`
- `R2_ACCOUNT_ID`
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

## Vérifications utiles

- `GET /health` doit répondre `200`.
- `GET /storage/status` doit afficher les services activés.
- `GET /games/loto/statistics` doit retourner un compteur non nul.

## Conseils

- Garder l’historique local en JSON comme fallback.
- Brancher Neon seulement après la validation du déploiement.
- Utiliser R2 pour les images et captures plutôt que pour les données de jeu.

