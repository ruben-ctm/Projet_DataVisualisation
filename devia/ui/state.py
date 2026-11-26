"""Cache et état de session : tout ce qui touche à `st.cache_*` et `st.session_state` est ici.

Ce qui est mis en cache (processus serveur) :
  - `ensure_data`   (cache_resource) : téléchargement unique des CSV si absents (capacité, pas une donnée).
  - `load_frames`   (cache_data)     : lecture + préparation des CSV -> DataFrames 2026 et 2025.
Ce qui est gardé en session (par navigateur) :
  - `filters`       : état canonique des filtres communs (survit au changement de page).
  - `filters_ver`   : compteur qui versionne les clés de widgets (le bouton « Réinitialiser » l'incrémente).
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from .. import data, download
from ..config import ANNEE, ANNEE_REF
from ..labels import EXP_BANDS, ORG_SIZE
from ..population import SCOPE_HELP, SCOPE_LABELS, Filters, apply_filters


@st.cache_resource(show_spinner="Téléchargement des données de l'enquête (première exécution)…")
def ensure_data() -> bool:
    """Télécharge les CSV manquants une seule fois pour tout le processus (utile au déploiement)."""
    download.ensure((2026,), log=lambda *_: None)
    try:
        download.ensure((2025,), log=lambda *_: None)
    except Exception:  # 2025 est optionnel : l'application fonctionne sans comparaison
        pass
    return True


@st.cache_data(show_spinner="Lecture et préparation des données…")
def load_frames() -> tuple[pd.DataFrame, pd.DataFrame | None]:
    """Données 2026 (obligatoires) et 2025 (optionnelles), préparées. Mise en cache : chargement seulement."""
    d26 = data.prepare_2026(data.load_2026())
    try:
        d25 = data.prepare_2025(data.load_2025())
    except data.DataMissingError:
        d25 = None
    return d26, d25


# --------------------------------------------------------------------------- filtres


def _init_session() -> None:
    if "filters" not in st.session_state:
        st.session_state["filters"] = Filters()
    if "filters_ver" not in st.session_state:
        st.session_state["filters_ver"] = 0


def _k(name: str) -> str:
    return f"flt_{name}_{st.session_state['filters_ver']}"


def _sync() -> None:
    """Callback : recopie les widgets (clés versionnées) vers l'état canonique `filters`."""
    ss = st.session_state
    ss["filters"] = Filters(
        scope=ss[_k("scope")],
        countries=tuple(ss[_k("countries")]),
        exp_range=tuple(ss[_k("exp")]),
        org_sizes=tuple(ss[_k("org")]),
    )


def _reset() -> None:
    st.session_state["filters"] = Filters()
    st.session_state["filters_ver"] += 1  # de nouvelles clés => widgets remis à leurs valeurs par défaut
