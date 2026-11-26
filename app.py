"""Point d'entrée : navigation entre le tableau de bord principal et les axes d'approfondissement.

Lancer : uv run streamlit run app.py
Chaque axe vit dans son fichier `pages/N_*.py` (une branche par membre). La page n'apparaît dans le menu que si son
fichier existe : l'application tourne donc avec le socle seul, puis s'enrichit à mesure que les axes sont fusionnés.
"""
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent
AXES = [
    ("pages/1_Adoption.py", "1 · Adoption", "🚀"),
    ("pages/2_Confiance.py", "2 · Confiance", "🔍"),
    ("pages/3_Agents_de_code.py", "3 · Agents de code", "🛠️"),
    ("pages/4_Couts_caches.py", "4 · Coûts cachés", "⚠️"),
    ("pages/5_Organisation.py", "5 · Organisation", "🏢"),
]
pages = [st.Page("dashboard.py", title="Tableau de bord", icon="🤖", default=True)]
pages += [st.Page(path, title=title, icon=icon) for path, title, icon in AXES if (ROOT / path).exists()]
st.navigation(pages).run()
