"""Constantes partagées : chemins, URLs, seuils de rigueur, colonnes utilisées."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

RAW_BASE = "https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive"
# Fichiers stockés avec Git LFS : on utilise l'adresse media.githubusercontent.com,
# jamais l'adresse « raw » qui ne renvoie qu'un pointeur LFS.
SOURCES = {
    2026: {
        "responses": (f"{RAW_BASE}/2026/survey_results_public.csv", DATA_DIR / "2026" / "survey_results_public.csv"),
        "schema": (f"{RAW_BASE}/2026/survey_results_schema.csv", DATA_DIR / "2026" / "survey_results_schema.csv"),
    },
    2025: {
        "responses": (f"{RAW_BASE}/2025/results.csv", DATA_DIR / "2025" / "results.csv"),
        "schema": (f"{RAW_BASE}/2025/schema.csv", DATA_DIR / "2025" / "schema.csv"),
    },
}

# --- Seuils de rigueur -------------------------------------------------------
MIN_N = 30          # en dessous, une part n'est pas dessinée : l'application le dit
MIN_GROUP_N = 30    # taille minimale d'un sous-groupe dans une comparaison
TOP_COUNTRIES = 12  # pays proposés dans les filtres (les plus représentés)

# --- Colonnes lues dans les CSV (le fichier 2026 pèse 120 Mo : on ne charge que l'utile)
COLS_2026 = [
    "ResponseId", "Age", "Employment", "CodeMain", "Role", "ICorPM", "WorkExp", "WorkSetting",
    "Country", "OrgSize", "JobSat", "LearnAI",
    "AISelect", "AIUse", "AISentiment", "AITrust", "AIComplex", "AIDaily", "AIToolCount",
    "AIFreq_1", "AIFreq_2", "AIFreq_3", "AIFreq_4",
    "AIAvoid", "Disruption", "AIAdopt", "AIToken",
    *[f"AIImpact_{i}" for i in range(1, 8)],
    *[f"AISat_{i}" for i in range(1, 8)],
    "AICodeAgentHaveWorkedWith", "AICodeAgentWantToUseNext6Months", "AICodeAgentAdmired",
    "LLMHaveWorkedWith",
]
COLS_2025 = [
    "ResponseId", "MainBranch", "Age", "Employment", "WorkExp", "OrgSize", "Country",
    "AISent", "AIComplex",
]

ANNEE = 2026
ANNEE_REF = 2025

VOLONTAIRES = (
    "Les répondants sont des volontaires qui ont répondu à une enquête en ligne : "
    "les parts affichées décrivent les répondants, pas l'ensemble des développeurs."
)
