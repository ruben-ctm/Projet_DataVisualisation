# 1. Cadrage

*Premier temps de la méthode : décider avant de calculer. Ce document a été écrit avant les figures et n'a été corrigé qu'une fois, après l'exploration (voir en bas).*

## Qui, quoi, comment

| | |
|---|---|
| **Commanditaire (fictif)** | La direction technique d'une ESN française de 3 000 personnes. Elle décide comment équiper ses développeurs en assistants et agents de code. |
| **Décision attendue** | Où mettre le budget : distribuer des licences, ou investir aussi dans la vérification du code produit avec l'IA (revue, tests, traçabilité). |
| **Données** | Stack Overflow Developer Survey 2026, comparée à 2025 uniquement sur les questions identiques. Voir `02_BIOGRAPHIE.md`. |
| **Livrable** | Une application Streamlit (tableau de bord + cinq axes) et un brief d'une page (`04_BRIEF.md`). |

## La question

> Parmi les **développeurs professionnels** ayant répondu à l'enquête, la part qui juge l'IA capable sur les tâches complexes a-t-elle progressé d'**au moins 10 points** entre 2025 et 2026 (intervalles à 95 % qui ne se recouvrent pas) ? Et la confiance accordée à l'IA a-t-elle suivi ? **Si l'écart est net et que la confiance reste conditionnée, la direction finance la vérification en plus des licences.**

Elle contient les quatre éléments exigés : une population (développeurs professionnels), un indicateur (part « bonne » ou « très bonne » sur les tâches complexes, part de confiance), un seuil (10 points, intervalles disjoints, minimum 30 répondants par part) et une décision (budget vérification).

## La grande idée

> **Le sujet n'est plus l'adoption, c'est la vérification.** Les développeurs jugent l'IA plus capable, mais ils ne lui font confiance que lorsqu'ils peuvent contrôler le résultat.

## L'histoire en trois minutes

1. **Contexte (30 s).** L'IA est déjà dans le travail de la grande majorité des développeurs professionnels de l'échantillon. La question de l'équipement est donc posée : avec quoi, et avec quel garde-fou.
2. **Constat (90 s).** La capacité perçue sur les tâches complexes passe de 34 % à 60 %. L'attitude générale ne bouge pas (63 % → 64 %). La confiance reste conditionnée : près d'un répondant sur deux ne fait confiance que si le résultat est vérifiable.
3. **Nuance (45 s).** Deux choses peuvent fausser la hausse : qui répond (le taux de réponse au bloc IA a baissé) et ce que « utilisateur » veut dire d'une année à l'autre. Nous les contrôlons et nous disons ce qui reste ouvert.
4. **Décision (15 s).** Équiper, et budgéter la vérification ; la mesurer sur deux équipes pilotes avant de généraliser.

## Les cinq axes et leurs responsables

| Axe | Question posée au commanditaire | Responsable |
|---|---|---|
| 1. Adoption | Qui utilise l'IA, à quel rythme, avec quels types d'outils ? | Ruben COMBE--TAMAIN |
| 2. Confiance | La confiance suit-elle la capacité perçue ? Que change l'ancienneté ? | Antoine REVERSAT |
| 3. Agents de code | Quels outils d'agents sont utilisés, souhaités, admirés ? | Edwin DREAN-AVRILLON |
| 4. Coûts cachés | Quelles erreurs coûtent du temps ? Pour quelles tâches l'IA déçoit-elle ? | Arthur REYNAUD |
| 5. Organisation | Les règles de l'entreprise changent-elles l'usage et la satisfaction ? | Léo VAZ SAMPAIO--DESTOT |

## Maquette

Tableau de bord (page d'accueil). Le titre est une phrase calculée sur la sélection ; les filtres sont communs à toutes les pages.

```
+------------------+-----------------------------------------------------------------+
| FILTRES          | L'IA au travail : plus capable aux yeux des développeurs,       |
| Population       | mais toujours vérifiée                                          |
|  (pro / tous)    | commanditaire : direction technique d'une ESN                   |
| Pays             +-----------------------------------------------------------------+
| Ancienneté       | 87 %          | 60 %  (+26 pts) | 64 %  (+1 pt)  | 49 %           |
| Taille d'orga.   | utilisent l'IA| jugée capable   | attitude fav.  | confiance si   |
| [Réinitialiser]  |               |                 |                | vérifiable     |
|                  | Population : développeurs pro, 2026, n = ...                    |
| À propos         +--------------+------------------+-------------------------------+
|  source, bénévoles| Le constat  | France / monde   | Ce que ça change | Méthode    |
|  réexécutions : n |-------------+------------------+-------------------------------+
|                  |  [figure 2025 -> 2026, barres + IC]                              |
|                  |  [figure confiance, barres + IC]                                 |
|                  |  > Voir les chiffres et les télécharger (CSV)                    |
+------------------+-----------------------------------------------------------------+
Pages de gauche : Tableau de bord | 1 Adoption | 2 Confiance | 3 Agents | 4 Coûts | 5 Organisation
```

Chaque axe suit le même gabarit : question au commanditaire, titre-affirmation calculé, figure avec population en pied, légende « qui, quelle année, combien », bloc « Voir les données » avec export CSV.

## Ce que le projet ne fera pas

- Mesurer la productivité ou la qualité du code : l'enquête ne contient que des déclarations.
- Comparer 2025 et 2026 sur la confiance, la fréquence d'usage ou les agents : les questions ont changé (`HARMONISATION.md`).
- Prétendre représenter tous les développeurs : les répondants sont des volontaires.

## Ce que l'exploration a changé au cadrage

La première formulation ne prévoyait pas le contrôle sur les « utilisateurs » ni le taux de réponse : ils ont été ajoutés après avoir constaté que le taux de réponse au bloc IA passait de 70 % à 50 % (`03_EXPLORATION.md`, observation 2).
