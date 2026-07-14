# Base de connaissance FDJ consolidée

## Périmètre

Ce document centralise l’historique de travail, les règles de stratégie, les écarts observés entre grilles et résultats, ainsi que les solutions gratuites ou open source pour récupérer automatiquement les résultats FDJ.

Rappel important : aucune grille ne constitue une prédiction certaine. Le projet sert uniquement à suivre l’historique, comparer des stratégies, calculer des tendances simples et produire des grilles équilibrées.

## 1. Inventaire du dossier

- Dossier racine vérifié : `C:\projets\jeux`
- Dossier documentation vérifié : `C:\projets\jeux\docs`

Fichiers Markdown présents dans `docs` au moment de la consolidation :

- `C:\projets\jeux\docs\Retro-engineering_FDJ_Conversation.md`
- `C:\projets\jeux\docs\retro_engineering_fdj_loto_euromillions.md`

## 2. Historique FDJ consolidé

### 2.1 Loto / Grand Loto

#### Gain de référence

- Date : vendredi 26 juin
- Grille jouée : `7 - 16 - 18 - 29 - 34 - 48 + Chance 5`
- Tirage réel : `5 - 14 - 29 - 38 - 48 + Chance 8`
- Gain : `47,60 €`
- Numéros communs : `29`, `48`

#### Enseignements tirés

- Les numéros `29` et `48` sont devenus des pivots historiques.
- La première stratégie a trop insisté sur la reprise des numéros gagnants récents.
- Une règle plus robuste a ensuite été retenue :
  - `1 bloc bas consécutif`
  - `1 bloc milieu`
  - `1 bloc haut`
  - `éviter de rejouer exactement la grille perdante`

#### Grilles et résultats importants

- Samedi 27 juin : résultat `18 - 21 - 24 - 35 - 36 + Chance 3`
- Lundi 29 juin : résultat `1 - 13 - 27 - 32 - 41 + Chance 2`
- Mercredi 1 juillet : résultat `8 - 9 - 10 - 25 - 31 + Chance 5`

#### Grilles proposées ou retenues

- `7 - 16 - 29 - 34 - 38 - 48 + Chance 5`
- `5 - 14 - 29 - 31 - 38 - 48 + Chance 8`
- `8 - 13 - 25 - 31 - 36 + Chance 5`
- `8 - 9 - 25 - 36 - 41 + Chance 5`
- `9 - 10 - 25 - 36 - 41 + Chance 5`
- Variantes de travail :
  - `8 - 9 - 27 - 32 - 38 + Chance 2`
  - `13 - 14 - 24 - 35 - 48 + Chance 8`

#### Erreurs à éviter

- Rejouer une grille perdante sans modification.
- Surpondérer un gain ancien parce qu’il a payé une fois.
- Construire une grille trop concentrée en zone haute.
- Confondre proximité numérique et gain réel.

### 2.2 EuroMillions / My Million

#### Résultats et grilles suivis

- Vendredi 26 juin : `6 - 16 - 26 - 34 - 35` étoiles `11 - 12`
- Mardi 30 juin : `1 - 8 - 37 - 44 - 48` étoiles `2 - 6`
- Vendredi 3 juillet : `2 - 12 - 17 - 25 - 39` étoiles `1 - 2`

#### Grille jouée et perdante

- Grille jouée le vendredi 3 juillet : `5 - 18 - 29 - 36 - 48` étoiles `8 - 9`
- Gain : aucun

#### Écarts observés

- `18` était proche de `17`
- `36` était proche de `39`
- La grille jouée était trop haute
- Les étoiles `8 - 9` étaient trop éloignées du résultat `1 - 2`

#### Règles de travail retenues

- Réintroduire davantage de bas et de milieu.
- Éviter les grilles trop hautes.
- Garder une structure équilibrée :
  - 1 ou 2 petits numéros
  - 1 ou 2 numéros de milieu
  - 1 ou 2 numéros hauts
  - étoiles variées, pas uniquement hautes

### 2.3 Crescendo

#### Historique consolidé

- Samedi 6 juin
- Samedi 13 juin
- Samedi 20 juin
- Samedi 27 juin

#### Grille suivie

- Grille jouée : `2 - 6 - 8 - 10 - 13 - 15 - 17 - 20 - 23 - 24 + I`
- Résultat : `3 - 4 - 5 - 6 - 12 - 13 - 20 - 21 - 24 - 25 + E`
- Correspondances exactes : `6`, `13`, `20`, `24`

#### Règle retenue

- Analyser les suites et les blocs.
- Favoriser une logique de couverture de zones.
- Éviter de rejouer une grille perdante à l’identique.

## 3. Base documentaire à conserver

Les éléments suivants doivent rester systématiquement tracés :

- tirages gagnants ;
- grilles jouées ;
- grilles proposées ;
- gains et pertes ;
- écarts entre propositions et résultats ;
- règles de construction ;
- erreurs à éviter ;
- décisions de stratégie.

## 4. Solutions gratuites ou open source pour récupérer automatiquement les résultats FDJ

### 4.1 Source officielle FDJ

La source la plus sûre et gratuite reste FDJ elle-même.

#### Loto

- Page historique officielle : `https://www.fdj.fr/jeux-de-tirage/loto/historique`
- La page indique que les archives Loto sont téléchargeables en ZIP et remontent jusqu’en 1976.

#### EuroMillions / My Million

- Page historique officielle : `https://www.fdj.fr/jeux-de-tirage/euromillions-my-million/historique`
- La page indique que les archives sont téléchargeables en ZIP et remontent jusqu’en février 2004.

#### Crescendo

- Page historique officielle : `https://www.fdj.fr/jeux-de-tirage/crescendo/historique`
- La page propose aussi un téléchargement des tirages passés en ZIP.

#### Point d’attention

- Ce ne sont pas toujours des API publiques documentées.
- En pratique, le moyen le plus stable et gratuit est d’exploiter les archives ZIP officielles ou les pages de résultats.
- Ces sources sont localement exploitables si on automatise le téléchargement et le parsing.

### 4.2 Open source pour Loto

#### `winning-number/fdj-sdk`

- Dépôt GitHub : `https://github.com/winning-number/fdj-sdk`
- Licence visible : GPL-3.0
- Intérêt :
  - SDK FDJ orienté Loto
  - accès à l’historique
  - prise en charge de décodeurs personnalisés pour d’autres jeux
  - présence d’informations sur l’endpoint `service-draw-info/v3/draws`

#### Utilisation recommandée

- Très bonne piste pour le Loto.
- À tester en premier pour un mode local et gratuit.
- Peut servir de base pour un connecteur MCP local.

### 4.3 Open source pour EuroMillions

#### `pedro-mealha/euromillions-api`

- Dépôt GitHub : `https://github.com/pedro-mealha/euromillions-api`
- Intérêt :
  - API REST gratuite et open source
  - résultats disponibles depuis 2004
  - filtrage par année ou par dates

#### Utilisation recommandée

- Bon candidat pour l’historique EuroMillions.
- À valider avant usage productif, car ce n’est pas une source officielle FDJ.

### 4.4 Crescendo

#### Constat actuel

- Aucun équivalent open source robuste et clairement exploitable n’a été validé dans les recherches effectuées.
- La voie gratuite la plus simple reste l’archive officielle FDJ.
- Si besoin, on peut envisager :
  - scraping des pages de résultats FDJ ;
  - téléchargement automatique des ZIP officiels ;
  - extraction locale vers JSON/CSV.

## 5. Architecture technique simple recommandée

### 5.1 Objectif d’architecture

Construire une chaîne locale simple, reproductible et totalement gratuite :

1. récupérer les résultats ;
2. normaliser les données ;
3. conserver l’historique ;
4. comparer les grilles ;
5. exposer les données via un MCP local.

### 5.2 Structure de dossiers conseillée

```text
C:\projets\jeux
├── docs
│   ├── base_connaissance_fdj.md
│   ├── historique-fdj.md
│   ├── loto.md
│   ├── euromillions.md
│   ├── crescendo.md
│   ├── strategies.md
│   └── retro-engineering-conversation.md
├── data
│   ├── loto.json
│   ├── euromillions.json
│   ├── crescendo.json
│   ├── grilles-jouees.json
│   └── decisions-algorithmiques.json
├── scripts
│   ├── fetch_loto.py
│   ├── fetch_euromillions.py
│   ├── fetch_crescendo.py
│   ├── normalize_results.py
│   ├── compare_grids.py
│   └── update_docs.py
└── mcp
    └── fdj_mcp_server.py
```

### 5.3 Pipeline de données

#### Étape 1 : récupération

- Télécharger les archives ZIP FDJ lorsque c’est disponible.
- Utiliser `fdj-sdk` pour le Loto si l’API communautaire est suffisante.
- Utiliser `euromillions-api` pour l’historique EuroMillions.

#### Étape 2 : normalisation

- Convertir les tirages en JSON canonique.
- Exporter aussi en CSV si l’analyse tabulaire est utile.
- Conserver le Markdown pour la lecture humaine.

#### Étape 3 : historique algorithmique

- Enregistrer chaque proposition de grille.
- Enregistrer chaque résultat réel.
- Calculer automatiquement :
  - correspondances exactes ;
  - proximités ;
  - pertes ;
  - écarts de structure ;
  - respect ou non des règles de bloc.

#### Étape 4 : documentation

- Générer ou mettre à jour les fichiers Markdown dans `docs`.
- Conserver la trace des décisions stratégiques.

#### Étape 5 : exposition MCP

Exposer un serveur MCP local avec des outils comme :

- `get_last_loto_result`
- `get_last_euromillions_result`
- `get_last_crescendo_result`
- `get_loto_history`
- `compare_grid_to_result`
- `generate_balanced_loto_grid`
- `apply_user_strategy_rule`

### 5.4 Format de conservation conseillé

#### JSON

- meilleur format pour l’automatisation ;
- facilite les comparaisons et l’historique algorithmique ;
- adapté aux calculs de fréquence et d’écart.

#### CSV

- utile pour les tableaux et l’export ;
- pratique pour les filtres et les statistiques simples.

#### Markdown

- utile pour la lecture humaine ;
- parfait pour les synthèses, règles et décisions.

## 6. Règles de stratégie à conserver

- Ne jamais parler de certitude ou de prédiction.
- Ne jamais rejouer exactement une grille perdante.
- Ne pas surpondérer un ancien gain.
- Garder une répartition bas / milieu / haut.
- Ne pas confondre proximité numérique et gain.
- Séparer clairement la logique Loto et la logique EuroMillions.

## 7. Décision de travail actuelle

La règle prioritaire à appliquer au Loto reste :

> `bloc bas consécutif + bloc milieu + bloc haut + pas de replay exact perdant`

Grille de référence actuelle :

> `9 - 10 - 25 - 36 - 41 + Chance 5`

## 8. Conclusion opérationnelle

La base de connaissance est désormais structurée autour de trois axes :

- historique consolidé FDJ ;
- sources gratuites et open source ;
- architecture locale simple et extensible.

La prochaine étape logique est de transformer cette base en scripts de récupération et de normalisation, puis en serveur MCP local.
