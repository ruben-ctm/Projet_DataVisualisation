"""Composants d'interface partagés : légende de population, garde d'effectif, en-tête de page."""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import streamlit as st

from .. import population
from ..config import MIN_N
from ..population import Filters


def header(title: str, question: str, owner: str | None = None) -> None:
    st.title(title)
    st.markdown(f"**Question posée au commanditaire :** {question}")
    if owner:
        st.caption(f"Axe porté par {owner}.")


def guard_min_n(n: int, what: str = "cette figure", minimum: int = MIN_N) -> None:
    """Si l'effectif est trop faible, le dit à la place de dessiner, puis arrête le script."""
    if n < minimum:
        st.warning(
            f"Seulement {n} répondant(s) pour {what} avec les filtres actuels (minimum {minimum}) : "
            "rien n'est dessiné. Élargissez la sélection (pays, ancienneté, taille d'organisation) "
            "ou choisissez « Tous les répondants »."
        )
        st.stop()


_FR = {"group": "Groupe", "category": "Modalité", "option": "Option", "tool": "Outil", "task": "Tâche", "exp_band": "Ancienneté",
       "usage": "Usage", "n": "Répondants", "k": "Effectif « oui »", "share": "Part", "lo": "IC 95 % bas", "hi": "IC 95 % haut",
       "net": "Solde", "share_pos": "Part positive", "share_neg": "Part négative", "share_used": "Part ayant utilisé",
       "share_want": "Part souhaitant", "admiration": "Taux d'admiration"}


def _fr(col: str) -> str:
    """Libellé français d'une colonne ; les suffixes d'année (`share_2025`) sont conservés."""
    m = re.fullmatch(r"(.+)_(2025|2026)", col)
    if m:
        return f"{_FR.get(m.group(1), m.group(1))} {m.group(2)}"
    return _FR.get(col, col)


def data_view(df: pd.DataFrame, filename: str, label: str = "Voir les données de la figure") -> None:
    """La table derrière une figure, avec téléchargement CSV : le lecteur retrouve les chiffres de l'image et peut les réutiliser."""
    out = df.rename(columns={c: _fr(c) for c in df.columns})
    with st.expander(label):
        st.dataframe(out, hide_index=True, use_container_width=True)
        st.download_button("Télécharger en CSV", out.to_csv(index=False).encode("utf-8-sig"),
                           file_name=f"{filename}.csv", mime="text/csv", key=f"dl_{filename}")


def markdown_doc(path: Path) -> None:
    """Affiche un document Markdown du dépôt ; les images relatives (`![légende](figures/x.png)`) sont rendues par `st.image`."""
    buf: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.fullmatch(r"!\[(.*?)\]\((.+?)\)", line.strip())
        if m:
            if buf:
                st.markdown("\n".join(buf))
                buf = []
            st.image(str(path.parent / m.group(2)), caption=m.group(1), use_container_width=True)
        else:
            buf.append(line)
    if buf:
        st.markdown("\n".join(buf))
