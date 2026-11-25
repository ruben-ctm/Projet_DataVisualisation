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
