# Cloudflare R2

Si tu n’as que l’URL S3 complète, par exemple :

`https://ae3310e8b16fc62752748432f8cbc8e7.r2.cloudflarestorage.com/mesjeux`

alors :

- le bucket est `mesjeux`
- l’endpoint S3 utilisable par `boto3` est `https://ae3310e8b16fc62752748432f8cbc8e7.r2.cloudflarestorage.com`
- il faut toujours les identifiants S3 :
  - `R2_ACCESS_KEY_ID`
  - `R2_SECRET_ACCESS_KEY`

Variables acceptées par l’API :

- `R2_S3_ENDPOINT`
- `R2_S3_URL`
- `R2_BUCKET`
- `R2_ACCOUNT_ID`

Règle pratique :

1. si tu as `R2_BUCKET`, on l’utilise
2. sinon, si tu as une URL qui finit par `/mesjeux`, on déduit `mesjeux`
3. sinon, l’API R2 reste désactivée

