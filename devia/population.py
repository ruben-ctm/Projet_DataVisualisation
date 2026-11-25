"""Population : qui est dans l'analyse, et comment la décrire.

`Filters` est l'état des filtres du panneau latéral ; `apply_filters` produit la
population filtrée ; `describe` produit la phrase qui accompagne chaque figure.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from .config import VOLONTAIRES
from .labels import EXP_BANDS


@dataclass(frozen=True)
class Filters:
    scope: str = "pro"                      # "pro" : développeurs professionnels ; "all" : tous les répondants
    countries: tuple[str, ...] = ()         # vide = tous les pays
    exp_range: tuple[str, str] = (EXP_BANDS[0], EXP_BANDS[-1])  # tranches d'ancienneté pro (incluses)
    org_sizes: tuple[str, ...] = ()         # vide = toutes les tailles

    @property
    def exp_is_full(self) -> bool:
        return self.exp_range == (EXP_BANDS[0], EXP_BANDS[-1])


SCOPE_LABELS = {
    "pro": "Développeurs professionnels",
    "all": "Tous les répondants",
}
SCOPE_HELP = {
    "pro": ("Le code est une partie principale du métier, en emploi ou indépendant "
            "(2025 : « développeur de profession », même statut d'emploi)."),
    "all": "Tous les répondants de l'enquête, y compris étudiants, retraités et personnes sans emploi.",
}


def apply_filters(df: pd.DataFrame, f: Filters, pro_col: str = "is_pro_dev") -> pd.DataFrame:
    """Applique les filtres communs. Un filtre vide ne retire personne."""
    mask = pd.Series(True, index=df.index)
    if f.scope == "pro":
        mask &= df[pro_col]
    if f.countries:
        mask &= df["country_label"].isin(f.countries)
    if not f.exp_is_full:
        lo, hi = EXP_BANDS.index(f.exp_range[0]), EXP_BANDS.index(f.exp_range[1])
        allowed = EXP_BANDS[lo:hi + 1]
        mask &= df["exp_band"].isin(allowed)  # les réponses sans ancienneté sont retirées
    if f.org_sizes and "org_label" in df:
        mask &= df["org_label"].isin(f.org_sizes)
    return df[mask]
