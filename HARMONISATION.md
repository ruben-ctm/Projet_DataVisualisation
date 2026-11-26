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
