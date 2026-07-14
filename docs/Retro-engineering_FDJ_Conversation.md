# Rétro-engineering -- Conversation FDJ

## 1. Résumé exécutif

Cette conversation a construit une méthode de sélection de grilles pour
EuroMillions, Loto et Crescendo à partir des tirages, des grilles jouées
et des gains, sans prétendre prédire le hasard.

## 2. Contexte

Analyse continue des tirages FDJ, comparaison des grilles proposées et
jouées, conservation d'un historique.

## 3. Objectifs

-   Étudier les tirages.
-   Comparer propositions / grilles jouées / résultats.
-   Conserver les gains.
-   Améliorer une logique de construction.

## 4. Chronologie

### Crescendo

-   Historique des samedis 6, 13, 20 et 27 juin intégré.
-   Analyse des suites et des blocs.
-   Règle retenue : bloc bas + milieu + haut + éviter de rejouer une
    grille perdante.

### EuroMillions

Historique : - 26/06 : 6-16-26-34-35 ⭐11-12 - 30/06 : 1-8-37-44-48
⭐2-6 - 03/07 : 2-12-17-25-39 ⭐1-2 - 07/07 : 5-29-33-45-47 ⭐5-8

Grilles : - Jouée : 8-13-25-31-43 ⭐5-8 - Conseillée puis jouée :
8-12-25-34-43 ⭐5-8

Résultat : - Gain 7,80 € grâce aux étoiles 5 et 8.

### Loto

Rappel utilisé : 29/06, 01/07, 04/07, 06/07. Règle : bloc bas
consécutif + milieu + haut.

## 5. Tableaux

### EuroMillions

  Type              Valeur
  ----------------- ---------------------
  Grille initiale   8-13-25-31-43 ⭐5-8
  Grille retenue    8-12-25-34-43 ⭐5-8
  Résultat          5-29-33-45-47 ⭐5-8
  Gain              7,80 €

### Crescendo

Grille jouée : 2-6-8-10-13-15-17-20-23-24 + I

Résultat : 3-4-5-6-12-13-20-21-24-25 + E

Correspondances : 6,13,20,24.

## 6. Méthodes

-   équilibre des dizaines ;
-   étude des suites (3-4-5, 20-21...) ;
-   suivi des fréquences ;
-   comparaison systématique entre proposition, jeu et résultat.

## 7. Enseignements

-   équilibrer les dizaines ;
-   conserver quelques numéros récurrents ;
-   éviter de recopier une grille perdante ;
-   suivre les blocs consécutifs pour Crescendo.

## 8. Décisions finales

EuroMillions : 1 bas, 1 dizaine, 1 vingtaine, 1 trentaine, 1
quarantaine.

Loto : bloc bas + milieu + haut.

Crescendo : analyse des suites et des fréquences.

## 9. Informations à conserver

Historique des tirages, grilles jouées, propositions, gains,
statistiques par dizaines et suites.

Toutes les propositions sont des heuristiques ; chaque combinaison
conserve la même probabilité d'être tirée.
