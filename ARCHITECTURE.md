# Architecture technique

Premier document à lire (les documents de méthode sont dans `docs/` : cadrage, biographie des données, exploration, brief). Il répond à quatre questions : **quelles fonctionnalités**, **quels fichiers et fonctions les portent**, **comment circulent les données**, **qu'est-ce qui est en cache et en session**.

## 1. Vue d'ensemble

```
get_data.py ──► data/*.csv (non versionné)
                   │  devia/data.py : load_2026 / load_2025   (colonnes utiles seulement)
                   ▼
              prepare_2026 / prepare_2025  ── colonnes dérivées : is_pro_dev, exp_band, country_label,
                   │                          ai_user, ai_daily_any, sentiment3, capability5 (harmonisation)
                   ▼   [st.cache_data : load_frames]
        devia/ui/state.py : setup()  ──► filtres (session_state) ──► population.apply_filters ──► pop26, pop25
                   │
                   ├─► dashboard.py ──► devia/indicators.py (chiffres du message) ──► devia/ui/charts.py ──► st.pyplot
                   └─► pages/N_*.py ──► devia/axes/<axe>.py (tables) ────────────────► devia/ui/charts.py ──► st.pyplot
                                                         devia/stats.py (parts, IC de Wilson, seuils)
```

Règle : **la logique ne connaît pas Streamlit, l'interface ne calcule rien.** Une page appelle une fonction d'axe qui renvoie une table, puis une fonction de `charts.py` qui renvoie une figure, puis `components.show_figure` qui l'affiche avec sa population.

## 2. Fonctionnalités et fichiers

| Fonctionnalité | Fichiers | Fonctions clés |
|---|---|---|
| Télécharger les données | `get_data.py`, `devia/download.py`, `devia/config.py` | `ensure`, `download` (garde-fou contre un pointeur Git LFS) |
| Charger et préparer | `devia/data.py`, `devia/labels.py` | `load_2026`, `load_2025`, `prepare_2026`, `prepare_2025`, `exp_band` |
| Harmoniser 2025 ↔ 2026 | `devia/harmonisation.py`, `HARMONISATION.md` | `sentiment3`, `capability5`, `capability_positive`, `is_pro_dev_*` |
| Statistiques | `devia/stats.py` | `wilson_ci`, `share`, `multi_share`, `shares_by_group`, `distribution_by_group`, `enough` |
| Population et filtres | `devia/population.py` | `Filters`, `apply_filters`, `describe`, `caption` |
| Message du tableau de bord | `devia/indicators.py`, `devia/message.py` | `headline`, `overall_adoption`, `compare_capability`, `message.headline`, `message.takeaways` |
| Filtres, cache, session | `devia/ui/state.py` | `setup`, `sidebar_filters`, `load_frames`, `ensure_data` |
| Garde d'effectif, légendes | `devia/ui/components.py` | `guard_min_n`, `show_figure`, `footer_text`, `dropped_note` |
| Table derrière chaque figure + export CSV | `devia/ui/components.py` | `data_view` (expander, `st.dataframe`, `st.download_button`) |
| Lecture des documents dans l'application | `devia/ui/components.py`, `dashboard.py` | `markdown_doc` (brief affiché dans « Ce que ça change pour l'ESN ») |
| À propos et compteur de réexécutions | `devia/ui/state.py` | `setup` (incrémente `session_state["reruns"]`), `sidebar_filters` (bloc « À propos ») |
| Brief d'une page et ses preuves | `docs/04_BRIEF.md`, `docs/preuves.csv`, `scripts/build_brief.py`, `tests/test_brief.py` | `build`, `figures` ; le test vérifie que chaque chiffre du brief est dans `preuves.csv` |
| Graphiques | `devia/ui/charts.py` | `hbar_shares`, `stacked_hbar`, `paired_bars`, `diverging_bars`, `dumbbell` |
| Tableau de bord principal | `dashboard.py` | onglets Le constat / France et reste du monde / Ce que ça change / Méthode |
| Navigation | `app.py` | `st.navigation` (une page par axe, seulement si le fichier existe) |
| Axe 1 Adoption | `devia/axes/adoption.py`, `pages/1_Adoption.py` | `adoption_by`, `daily_share_by`, `tool_families`, `frequency_by_family`, `tool_count_distribution` |
| Axe 2 Confiance | `devia/axes/confiance.py`, `pages/2_Confiance.py` | `trust_by`, `capability_distribution`, `compare_sentiment`, `positive_capability_by` |
| Axe 3 Agents de code | `devia/axes/agents.py`, `pages/3_Agents_de_code.py` | `tool_table`, `providers`, `tools_per_person`, `tool_share_by` |
| Axe 4 Coûts cachés | `devia/axes/couts.py`, `pages/4_Couts_caches.py` | `disruption_shares`, `avoid_reasons`, `usefulness_by_task`, `satisfaction_by_task` |
| Axe 5 Organisation | `devia/axes/organisation.py`, `pages/5_Organisation.py` | `org_posture_by_size`, `adoption_criteria`, `learning_by`, `jobsat_by_exp_and_ai` |
| Tests | `tests/` | un fichier par module / axe ; `test_apps.py` exécute chaque page (Streamlit `AppTest`) |

## 3. Circulation des données, du fichier à la figure (exemple : la figure-clé)

1. `survey_results_public.csv` (2026) et `results.csv` (2025) sont lus par `load_2026` / `load_2025` : seules les colonnes de `config.COLS_*` sont chargées.
2. `prepare_*` ajoute `is_pro_dev`, `exp_band`, `country_label`, et les variables **harmonisées** `sentiment3`, `capability5`, `capability_positive`.
3. `state.setup()` lit les filtres de la session, `population.apply_filters` produit `pop26` et `pop25`.
4. `dashboard.py` appelle `indicators.compare_capability(pop26, pop25)` : une table (catégorie, part, IC, n) par année.
5. `charts.paired_bars` dessine la figure avec le **pied de population dans l'image** ; `components.show_figure` ajoute la légende « Population : qui, année, n ».
6. Si `n < 30`, `guard_min_n` affiche un avertissement et arrête le script avant tout dessin.

## 4. Cache et session

| Quoi | Où | Durée de vie | Pourquoi |
|---|---|---|---|
| Téléchargement des CSV | `@st.cache_resource` `ensure_data` | processus serveur | capacité partagée, exécutée une fois |
| DataFrames 2026 / 2025 préparés | `@st.cache_data` `load_frames` | processus serveur (une copie par appel) | lecture coûteuse, dépend de fichiers seulement |
| Filtres communs | `st.session_state["filters"]` | session du navigateur | survivent au changement de page |
| Versions des clés de widgets | `st.session_state["filters_ver"]` | session | « Réinitialiser » incrémente : les widgets repartent de leurs valeurs par défaut |
| Sélecteurs propres à un axe | clés de widgets `a1_*` … `a5_*` | page | choix locaux (regroupement, outil, tâche) |
| Compteur de réexécutions | `st.session_state["reruns"]` | session | rend visible le modèle Streamlit : chaque interaction relance tout le script |
| Calculs d'analyse | rien | une réexécution | rapides et dépendants des filtres |

Après modification de la préparation des données, vider le cache (touche **C** dans la page, ou redémarrer).

## 5. Tests

`uv run pytest` : tests unitaires (`test_stats`, `test_harmonisation`, `test_population`, `test_message`, `test_indicators`, `test_axe_*`) sur données synthétiques, et tests d'interface (`test_apps`) sur les vraies données : chaque page s'exécute, le filtre France fonctionne, une sélection trop étroite déclenche l'avertissement, le bouton Réinitialiser rétablit les filtres. Les tests d'interface sont ignorés si `data/` est absent.
