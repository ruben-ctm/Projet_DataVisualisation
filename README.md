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
git clone <url-du-depot>
cd stackoverflow-ia-2026
uv sync                          # reconstruit l'environnement depuis uv.lock
uv run python get_data.py        # télécharge les données dans data/ (jamais versionné)
uv run streamlit run app.py      # ouvre http://localhost:8501
```

- `uv run python get_data.py --only-2026` : sans les données 2025 (la comparaison 2025 ↔ 2026 est alors désactivée).
- Si les données manquent au lancement, l'application les télécharge elle-même (utile en déploiement).
- Tests : `uv run pytest` (les tests d'interface sont ignorés si `data/` est absent).
