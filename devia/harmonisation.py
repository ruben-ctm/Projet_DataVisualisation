"""Harmonisation explicite des questions et des réponses entre 2025 et 2026.

Le détail et les limites de chaque correspondance sont écrits dans HARMONISATION.md.
Seules deux questions sont comparables ; les autres sont volontairement exclues.
"""
import pandas as pd

from .labels import (CAPABILITY, CAPABILITY_DONT_USE, SENTIMENT_2025, SENTIMENT_2026, SENTIMENT_ORDER)

EMPLOYMENT_WORKING = ["Employed", "Independent contractor, freelancer, or self-employed"]
PRO_2026 = "I create code as a primary part of my job"
PRO_2025 = "I am a developer by profession"

CAPABILITY_ORDER = list(CAPABILITY.values())


def is_pro_dev_2026(df: pd.DataFrame) -> pd.Series:
    """2026 : le code est une partie principale du métier, en emploi ou indépendant."""
    return (df["CodeMain"] == PRO_2026) & df["Employment"].isin(EMPLOYMENT_WORKING)


def is_pro_dev_2025(df: pd.DataFrame) -> pd.Series:
    """2025 : « développeur de profession », en emploi ou indépendant."""
    return (df["MainBranch"] == PRO_2025) & df["Employment"].isin(EMPLOYMENT_WORKING)


def sentiment3(series: pd.Series, year: int) -> pd.Series:
    """Attitude envers l'IA, ramenée à 3 classes comparables ; « Not sure » est exclu."""
    mapping = SENTIMENT_2026 if year == 2026 else SENTIMENT_2025
    out = series.map(mapping)
    return pd.Categorical(out, categories=SENTIMENT_ORDER, ordered=True)


def capability5(series: pd.Series) -> pd.Series:
    """Capacité perçue sur les tâches complexes : mêmes 5 modalités en 2025 et 2026.

    La réponse « je n'utilise pas l'IA pour les tâches complexes / je ne sais pas »
    est exclue : elle ne dit rien de la capacité et sa part a changé entre les deux années.
    """
    out = series.map(CAPABILITY)  # la modalité « je ne sais pas » devient NaN
    return pd.Categorical(out, categories=CAPABILITY_ORDER, ordered=True)


def capability_positive(cap: pd.Series) -> pd.Series:
    """Booléen « Bonne » ou « Très bonne » ; NaN si pas d'avis exprimé."""
    cap = pd.Series(cap)
    pos = cap.isin(["Bonne, sans plus", "Très bonne"]).astype("float")
    pos[cap.isna()] = float("nan")
    return pos


assert CAPABILITY_DONT_USE not in CAPABILITY  # garde-fou : la modalité exclue n'est pas mappée
