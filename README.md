# L'IA au travail : ce que disent les développeurs (Stack Overflow 2026)

Application Streamlit d'analyse de l'enquête annuelle Stack Overflow 2026, comparée à 2025 lorsque les questions sont comparables.
Projet final du module *Data Visualisation* (ECE Paris, Ing4 Data & IA).

**Commanditaire (fictif) :** la direction technique d'une ESN française de 3 000 personnes qui décide comment équiper ses développeurs en assistants et agents de code.
**Message du tableau de bord :** les développeurs jugent l'IA nettement plus capable qu'en 2025 sur les tâches complexes, mais l'attitude générale n'a pas bougé et la confiance reste conditionnée à la vérification : le sujet n'est plus l'adoption, c'est la vérification.

> **À lire en premier : [ARCHITECTURE.md](ARCHITECTURE.md)** (fonctionnalités → fichiers et fonctions, circulation des données, cache et session). Les documents de méthode sont dans [`docs/`](docs/).

> Les répondants sont des volontaires qui ont rempli une enquête en ligne. Les parts décrivent les répondants, pas l'ensemble des développeurs.

## Lancer l'application depuis un clone frais

Prérequis : [uv](https://docs.astral.sh/uv/) (il installe Python 3.12 si besoin) et une connexion pour télécharger les données (~260 Mo).

```bash
git clone https://github.com/ruben-ctm/Projet_DataVisualisation.git
cd Projet_DataVisualisation
uv sync                          # reconstruit l'environnement depuis uv.lock
uv run python get_data.py        # télécharge les données dans data/ (jamais versionné)
uv run streamlit run app.py      # ouvre http://localhost:8501
```

- `uv run python get_data.py --only-2026` : sans les données 2025 (la comparaison 2025 ↔ 2026 est alors désactivée).
- Si les données manquent au lancement, l'application les télécharge elle-même (utile en déploiement).
- Tests : `uv run pytest` (les tests d'interface sont ignorés si `data/` est absent).

## Contenu de l'application

- **Tableau de bord** : le message pour le commanditaire, quatre indicateurs, la figure-clé 2025 ↔ 2026, un onglet France / reste du monde, les conséquences pour l'ESN, la méthode et les limites.
- **Cinq axes**, un par membre, chacun avec ses filtres et ses vues :

| Axe | Page | Porteur |
|---|---|---|
| 1 Adoption : qui utilise l'IA, à quel rythme, avec quels types d'outils | `pages/1_Adoption.py` | Ruben COMBE--TAMAIN |
| 2 Confiance et vérification, comparaison 2025 ↔ 2026 | `pages/2_Confiance.py` | Antoine REVERSAT |
| 3 Assistants et agents de code : usage, souhait, admiration | `pages/3_Agents_de_code.py` | Edwin DREAN-AVRILLON |
| 4 Coûts cachés : erreurs, freins, utilité et satisfaction par tâche | `pages/4_Couts_caches.py` | Arthur REYNAUD |
| 5 Organisation et carrière : politiques, critères d'adoption, satisfaction | `pages/5_Organisation.py` | Léo VAZ SAMPAIO--DESTOT |

- **Filtres communs** (panneau de gauche, valables sur toutes les pages) : population (développeurs professionnels / tous), pays, ancienneté, taille d'organisation, bouton Réinitialiser.
- **Chiffres et exports** : sous chaque figure, un bloc « Voir les données » montre la table qui l'a produite et la télécharge en CSV ; le tableau de bord a le même bloc pour ses indicateurs.
- **Rigueur** : chaque figure indique sa population (qui, année, nombre de répondants) dans l'image et dans sa légende ; en dessous de 30 répondants l'application le dit au lieu de dessiner ; intervalles de confiance à 95 % ; comparaison 2025 uniquement sur les questions harmonisées.

## Documentation

| Document | Contenu |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | fonctionnalités → fichiers et fonctions, circulation des données, cache et session |
| [DECISIONS.md](DECISIONS.md) | chaque choix, justifié, y compris les limites et ce qui n'a pas été fait |
| [HARMONISATION.md](HARMONISATION.md) | correspondances 2025 ↔ 2026, ce qui n'est pas comparé et pourquoi |
| [docs/01_CADRAGE.md](docs/01_CADRAGE.md) | commanditaire, question, grande idée, histoire en trois minutes, cinq axes, maquette |
| [docs/02_BIOGRAPHIE.md](docs/02_BIOGRAPHIE.md) | d'où viennent les données, ce que représente une ligne, ce qui manque |
| [docs/03_EXPLORATION.md](docs/03_EXPLORATION.md) | journal d'exploration et table de preuves |
| [docs/04_BRIEF.md](docs/04_BRIEF.md) | brief d'une page (3 figures) ; chiffres recalculés par `uv run python scripts/build_brief.py` dans `docs/preuves.csv` |
| `notebooks/` | exploration : prise en main des données (socle) et un notebook par axe |

## Organisation du dépôt

```
app.py                  navigation        dashboard.py   tableau de bord principal
pages/                  un fichier par axe
devia/                  analyse (aucun import de Streamlit hors de devia/ui/)
  data.py  population.py  stats.py  harmonisation.py  indicators.py  message.py  labels.py  config.py  download.py
  axes/                 une logique pure par axe
  ui/                   state.py (cache, session, filtres)  components.py  charts.py
tests/                  tests unitaires et d'interface
notebooks/              exploration
docs/                   cadrage, biographie, exploration, brief, figures, preuves.csv, captures
scripts/build_brief.py  recalcule les chiffres et figures du brief
get_data.py             téléchargement des données dans data/
```

## Travail en groupe

Chaque membre a déposé un commit à son nom, qui contient sa part du projet (`git log` donne l'ordre et les auteurs) :

| Membre | Part du projet |
|---|---|
| Ruben COMBE--TAMAIN | socle du dépôt (uv, configuration, téléchargement des données), README, **axe 1 Adoption**, captures d'écran |
| Edwin DREAN-AVRILLON | libellés, statistiques (parts, intervalles de Wilson), **harmonisation 2025-2026**, indicateurs partagés, **axe 3 Agents de code**, biographie des données |
| Antoine REVERSAT | chargement et préparation des données, filtres et population, **axe 2 Confiance**, cadrage, notebook de prise en main |
| Arthur REYNAUD | graphiques et composants partagés, thème, **axe 4 Coûts cachés**, journal d'exploration, script du brief |
| Léo VAZ SAMPAIO--DESTOT | tableau de bord et message, cache et état de session, **axe 5 Organisation**, brief d'une page, architecture et décisions |

Les tests de chaque module sont dans le commit de la personne qui l'a écrit.

## Déploiement (bonus)

Application déployée sur **Streamlit Community Cloud** (gratuit) : <https://share.streamlit.io>.

1. Se connecter avec le compte GitHub qui possède le dépôt (autoriser l'accès au dépôt, public ou privé).
2. **Create app** → *Deploy a public app from GitHub* : dépôt `ruben-ctm/Projet_DataVisualisation`, branche `main`, fichier principal `app.py`.
3. *Advanced settings* : Python **3.12**. Aucun secret n'est nécessaire.
4. **Deploy**. Les dépendances sont lues dans `uv.lock` (premier fichier reconnu par la plateforme ; ne pas ajouter de `requirements.txt` en parallèle). Les données (~260 Mo) sont téléchargées au premier lancement depuis le dépôt public de Stack Overflow : compter quelques minutes.
5. Mettre l'adresse publique (`https://<nom>.streamlit.app`) en tête de ce README et dans la remise.

Limites à connaître : mémoire limitée (l'application consomme environ 500 Mo au pic, mesuré) et mise en veille après environ 12 h sans visite (le premier visiteur la réveille, ce qui relance le chargement). Avant une démonstration, ouvrir l'adresse une fois.

## Données et licence

Enquête annuelle des développeurs Stack Overflow, 2025 et 2026, archive officielle : <https://github.com/StackExchange/Survey> (`packages/archive`). Publiées par Stack Overflow sous licence ODbL 1.0 (contenu : DbCL 1.0). Attribution : *Stack Overflow Developer Survey*, Stack Exchange Inc. Restitution officielle : <https://survey.stackoverflow.co/2026>.
