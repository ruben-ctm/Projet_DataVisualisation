"""Axe 2 - Confiance et vérification : confiance accordée à l'IA, capacité perçue, comparaison 2025 <-> 2026.

Porté par Antoine REVERSAT. Logique pure. Seules deux questions sont comparables entre 2025 et 2026
(attitude générale et capacité sur tâches complexes) : voir HARMONISATION.md.
"""
from __future__ import annotations

import pandas as pd

from ..config import MIN_GROUP_N
from ..harmonisation import CAPABILITY_ORDER
from ..indicators import (HIGH, TRUST_ORDER, VERIFY, capability_distribution, compare_capability,  # noqa: F401
                          diff_points, headline, trust_distribution, with_trust)
from ..labels import SENTIMENT_ORDER
from ..stats import category_shares, distribution_by_group, shares_by_group


GROUPINGS = {
    "Ancienneté professionnelle": "exp_band",
    "Tranche d'âge": "age_label",
    "Taille de l'organisation": "org_label",
    "Capacité perçue sur tâches complexes": "capability5",
}


def trust_by(df: pd.DataFrame, by_label: str) -> pd.DataFrame:
    col = GROUPINGS[by_label]
    return distribution_by_group(with_trust(df), "trust_label", col, TRUST_ORDER)


def verify_share_by(df: pd.DataFrame, by_label: str) -> pd.DataFrame:
    """Part « ne fait confiance que s'il peut vérifier », par groupe."""
    return shares_by_group(with_trust(df), "trust_verify", GROUPINGS[by_label])


def compare_sentiment(p26: pd.DataFrame, p25: pd.DataFrame) -> pd.DataFrame:
    a = category_shares(p25["sentiment3"], order=SENTIMENT_ORDER)
    b = category_shares(p26["sentiment3"], order=SENTIMENT_ORDER)
    return pd.DataFrame({"category": SENTIMENT_ORDER, "share_2025": a["share"].values, "lo_2025": a["lo"].values,
                         "hi_2025": a["hi"].values, "n_2025": a["n"].values, "share_2026": b["share"].values,
                         "lo_2026": b["lo"].values, "hi_2026": b["hi"].values, "n_2026": b["n"].values})


def positive_capability_by(p26: pd.DataFrame, p25: pd.DataFrame, col: str, min_n: int = MIN_GROUP_N) -> pd.DataFrame:
    """Part « capacité bonne ou très bonne » par groupe, 2025 et 2026 ; groupes gardés si assez grands les deux années."""
    t26 = shares_by_group(p26, "capability_positive", col, min_n=min_n)
    t25 = shares_by_group(p25, "capability_positive", col, min_n=min_n)
    m = t25.merge(t26, on="group", suffixes=("_2025", "_2026"))
    order = [g for g in (p26[col].cat.categories if isinstance(p26[col].dtype, pd.CategoricalDtype) else []) if g in set(m["group"])]
    if order:
        m["group"] = pd.Categorical(m["group"], categories=order, ordered=True)
        m = m.sort_values("group")
    else:
        m = m.sort_values("share_2026", ascending=False)
    m["group"] = m["group"].astype(str)
    return m.reset_index(drop=True)


