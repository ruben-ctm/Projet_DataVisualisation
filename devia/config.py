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
