# Harmonisation des questions 2025 ↔ 2026

Toute comparaison entre les deux enquêtes passe par `devia/harmonisation.py`. Ce document dit **ce qui est comparé, comment, et ce qui ne l'est pas**.

## Ce qui est comparé

| Notion | 2025 (`results.csv`) | 2026 (`survey_results_public.csv`) | Harmonisation |
|---|---|---|---|
| **Population** | `MainBranch` = « I am a developer by profession » et `Employment` ∈ {Employed, Independent contractor…} | `CodeMain` = « I create code as a primary part of my job » et même `Employment` | Deux libellés proches mais non identiques (voir limites). |
| **Attitude envers l'IA** | `AISent` : Very favorable / Favorable / Indifferent / Unfavorable / Very unfavorable / Unsure | `AISentiment` : Very favorable / Somewhat favorable / Neutral / Somewhat unfavorable / Very unfavorable / Not sure | 3 classes : **Favorable** (très favorable + favorable / un peu favorable), **Neutre**, **Défavorable**. « Unsure » / « Not sure » exclus. |
| **Capacité perçue sur tâches complexes** | `AIComplex` | `AIComplex` | Modalités **textuellement identiques** : Très mauvaise, Mauvaise, Ni bonne ni mauvaise, Bonne sans plus, Très bonne. « I don't use AI tools for complex tasks / I don't know » exclu les deux années. Indicateur « positif » = Bonne + Très bonne. |
| **Pays, ancienneté, taille d'organisation** | `Country`, `WorkExp`, `OrgSize` | idem | Ancienneté en tranches (0-2, 3-5, 6-10, 11-20, 21 et +) ; tailles d'organisation mises en correspondance une à une (`devia/data.py`). |

## Ce qui n'est volontairement pas comparé

| Notion | Pourquoi |
|---|---|
| Confiance (`AIAcc` 2025 / `AITrust` 2026) | 2025 : confiance dans l'**exactitude** des résultats, échelle trust/distrust. 2026 : confiance dans le **flux de travail**, avec des modalités de conditions (« si je peux vérifier »…). Questions différentes. |
| Fréquence / types d'usage (`AISelect`) | 2025 : fréquence d'usage (tous les jours, hebdo…). 2026 : types d'outils utilisés au travail. |
| Agents (`AIAgents` 2025 / `AIFreq_3`, `AICodeAgent*` 2026) | Formulations, bases et listes d'outils différentes. |
| Utilité, satisfaction par tâche, coûts, organisation | Questions nouvelles en 2026. |

## Limites à connaître

1. **Taux de réponse au bloc IA différent.** Parmi les développeurs professionnels : 70 % ont répondu à `AIComplex` en 2025, 50 % en 2026. Si les personnes qui répondent ont changé, une partie de l'écart peut venir de cette composition. L'application affiche ces taux (onglet « Méthode et limites »).
2. **Population presque identique, pas identique.** « Développeur de profession » (2025) et « le code est une partie principale de mon métier » (2026) se recouvrent largement sans coïncider.
3. **Volontaires.** Dans les deux années, ce sont des volontaires d'une enquête en ligne. Aucune pondération n'est publiée. Les parts décrivent les répondants.
4. **Échelle d'attitude.** « Favorable » (2025) est assimilé à « Somewhat favorable » (2026) : hypothèse de travail, non vérifiable avec ces données. C'est pourquoi la comparaison se fait sur 3 classes agrégées et non sur les 5 niveaux.

## Contrôle de robustesse (voir DECISIONS.md, §6)

La hausse de la capacité perçue (34 % → 60 % d'avis positifs, développeurs professionnels, tous pays) subsiste parmi les seuls utilisateurs d'IA (37 % → 60 % ; utilisateur = « Yes… » à `AISelect` en 2025, au moins une famille d'outils en 2026) : elle ne vient pas d'un simple changement de la part d'utilisateurs parmi les répondants. Ce contrôle ne lève pas le doute sur la composition des répondants au bloc IA (limite 1).
