"""Statistiques élémentaires : parts, intervalles de confiance, seuils d'effectif.

Fonctions pures (pandas/numpy), sans Streamlit.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .config import MIN_GROUP_N, MIN_N


def wilson_ci(k: float, n: float, z: float = 1.96) -> tuple[float, float]:
    """Intervalle de Wilson à 95 % pour une part k/n (bien défini même pour n petit)."""
    if n <= 0:
        return (math.nan, math.nan)
    p = k / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def enough(n: int, minimum: int = MIN_N) -> bool:
    """Vrai si l'effectif permet de dessiner une part."""
    return int(n) >= minimum


def share(mask: pd.Series) -> dict:
    """Part de `True` parmi les valeurs non manquantes : n, k, part et IC 95 %."""
    valid = mask.dropna()
    n = int(len(valid))
    k = int(valid.astype(bool).sum())
    lo, hi = wilson_ci(k, n)
    return {"n": n, "k": k, "share": k / n if n else math.nan, "lo": lo, "hi": hi}


def category_shares(series: pd.Series, order: list[str] | None = None) -> pd.DataFrame:
    """Répartition d'une variable catégorielle : une ligne par modalité (n, k, part, IC)."""
    s = series.dropna()
    n = len(s)
    cats = order if order is not None else list(s.value_counts().index)
    rows = []
    for c in cats:
        k = int((s == c).sum())
        lo, hi = wilson_ci(k, n)
        rows.append({"category": c, "n": n, "k": k, "share": k / n if n else math.nan, "lo": lo, "hi": hi})
    return pd.DataFrame(rows)
