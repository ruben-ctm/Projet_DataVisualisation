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


def sidebar_filters(d26: pd.DataFrame) -> Filters:
    """Filtres communs à toutes les pages. Chaque filtre répond à une question du lecteur."""
    _init_session()
    f: Filters = st.session_state["filters"]
    countries = data.top_countries(d26[d26["is_pro_dev"]], n=15)
    for c in f.countries:  # une sélection existante reste proposée
        if c not in countries:
            countries.append(c)
    with st.sidebar:
        st.header("Population")
        st.radio("Qui regarde-t-on ?", list(SCOPE_LABELS), format_func=SCOPE_LABELS.get,
                 index=list(SCOPE_LABELS).index(f.scope), key=_k("scope"), on_change=_sync,
                 help="Par défaut : les développeurs professionnels. " + SCOPE_HELP[f.scope])
        st.multiselect("Pays", countries, default=list(f.countries), key=_k("countries"), on_change=_sync,
                       placeholder="Tous les pays",
                       help="La France compte moins de répondants que les États-Unis ou l'Allemagne : "
                            "les figures le disent quand l'effectif devient trop faible.")
        st.select_slider("Ancienneté professionnelle", options=EXP_BANDS, value=f.exp_range, key=_k("exp"),
                         on_change=_sync, help="Années d'expérience professionnelle déclarées. "
                                               "Restreindre la plage retire les répondants qui n'ont pas répondu.")
        st.multiselect("Taille de l'organisation", list(ORG_SIZE.values()), default=list(f.org_sizes),
                       key=_k("org"), on_change=_sync, placeholder="Toutes les tailles",
                       help="Nombre de personnes employées par l'employeur principal.")
        st.button("Réinitialiser les filtres", on_click=_reset, use_container_width=True)
        st.caption("Les filtres s'appliquent à toutes les pages.")
        with st.expander("À propos"):
            st.markdown(
                "**Source :** enquête annuelle Stack Overflow Developer Survey 2026, comparée à 2025 lorsque les questions sont "
                "comparables. Les répondants sont des volontaires : les parts décrivent les répondants, pas tous les développeurs.\n\n"
                "Documentation : `README.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `HARMONISATION.md` et le dossier `docs/`.")
            st.caption(f"Réexécutions du script dans cette session : {st.session_state['reruns']}")
    return st.session_state["filters"]


def setup(page_title: str, icon: str = "📊"):
    """Début de chaque page : config, données, filtres. Renvoie (d26, d25, filtres, pop26, pop25)."""
    st.set_page_config(page_title=f"{page_title} · IA au travail", page_icon=icon, layout="wide")
    st.session_state["reruns"] = st.session_state.get("reruns", 0) + 1  # Streamlit réexécute tout le script à chaque interaction
    try:
        ensure_data()
        d26, d25 = load_frames()
    except Exception as exc:  # données absentes et téléchargement impossible
        st.error("Les données de l'enquête ne sont pas disponibles.")
        st.code("uv run python get_data.py", language="bash")
        st.caption(f"Détail : {exc}")
        st.stop()
    f = sidebar_filters(d26)
    pop26 = apply_filters(d26, f)
    pop25 = apply_filters(d25, f) if d25 is not None else None
    return d26, d25, f, pop26, pop25
