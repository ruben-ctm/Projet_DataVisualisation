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


def group_order(df: pd.DataFrame, by: str) -> list:
    """Ordre d'affichage des groupes : ordre des catégories si la colonne est ordonnée, sinon par effectif."""
    col = df[by]
    if isinstance(col.dtype, pd.CategoricalDtype):
        present = set(col.dropna().unique())
        return [c for c in col.cat.categories if c in present]
    return list(col.value_counts().index)


def shares_by_group(df: pd.DataFrame, flag: str, by: str, order: list[str] | None = None,
                    min_n: int = MIN_GROUP_N) -> pd.DataFrame:
    """Part de `flag` (booléen) dans chaque groupe de `by`, groupes trop petits écartés.

    Renvoie : group, n, k, share, lo, hi. Les groupes de moins de `min_n` répondants
    sont retirés (et listés dans `.attrs['dropped']` pour que l'interface puisse le dire).
    """
    rows, dropped = [], []
    groups = order if order is not None else group_order(df, by)
    for g in groups:
        sub = df.loc[df[by] == g, flag]
        r = share(sub)
        if r["n"] < min_n:
            if r["n"] > 0:
                dropped.append((g, r["n"]))
            continue
        rows.append({"group": g, **r})
    out = pd.DataFrame(rows, columns=["group", "n", "k", "share", "lo", "hi"])
    out.attrs["dropped"] = dropped
    return out


def multi_share(series: pd.Series, labels: dict[str, str] | None = None, sep: str = ";",
                exclude: tuple[str, ...] = ()) -> pd.DataFrame:
    """Réponses à choix multiples : part des répondants (ayant répondu) citant chaque option.

    Le dénominateur est le nombre de répondants à la question, pas le nombre de citations.
    Renvoie : option, n, k, share, lo, hi, triée par part décroissante.
    """
    s = series.dropna()
    n = len(s)
    exploded = s.str.split(sep).explode().str.strip()
    counts = exploded.value_counts()
    rows = []
    for opt, k in counts.items():
        if opt in exclude:
            continue
        lo, hi = wilson_ci(int(k), n)
        rows.append({"option": (labels or {}).get(opt, opt), "n": n, "k": int(k),
                     "share": k / n, "lo": lo, "hi": hi})
    return pd.DataFrame(rows, columns=["option", "n", "k", "share", "lo", "hi"])


def contains_flag(series: pd.Series, option: str, sep: str = ";") -> pd.Series:
    """Booléen « l'option est citée » ; NaN si la question n'a pas de réponse."""
    out = series.fillna("").str.split(sep).apply(lambda xs: option in [x.strip() for x in xs]).astype("float")
    out[series.isna()] = np.nan
    return out


def distribution_by_group(df: pd.DataFrame, col: str, by: str, categories: list[str],
                          group_order_: list | None = None, min_n: int = MIN_GROUP_N) -> pd.DataFrame:
    """Répartition d'une variable catégorielle dans chaque groupe (parts qui somment à 1 par groupe).

    `df[col]` doit déjà contenir les libellés de `categories` (NaN = pas de réponse, ignoré).
    Renvoie une table large : index = groupes, colonnes = catégories, + colonne `n` ; groupes < min_n écartés
    (listés dans `.attrs['dropped']`).
    """
    rows, dropped = {}, []
    for g in (group_order_ if group_order_ is not None else group_order(df, by)):
        sub = df.loc[df[by] == g, col].dropna()
        n = len(sub)
        if n < min_n:
            if n > 0:
                dropped.append((g, n))
            continue
        rows[g] = {**{c: float((sub == c).sum()) / n for c in categories}, "n": n}
    out = pd.DataFrame.from_dict(rows, orient="index", columns=[*categories, "n"])
    out.attrs["dropped"] = dropped
    return out
