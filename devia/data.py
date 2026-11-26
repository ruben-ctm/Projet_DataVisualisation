"""Chargement et préparation des données (sans Streamlit).

Flux : CSV brut -> `load_*` (colonnes utiles seulement) -> `prepare_*` (colonnes
dérivées : population, ancienneté, pays, harmonisation) -> DataFrame d'analyse.
La mise en cache est faite côté interface (devia/ui/state.py), pas ici.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from . import harmonisation as h
from .config import COLS_2025, COLS_2026, SOURCES, TOP_COUNTRIES
from .labels import AGE, COUNTRY, EXP_BANDS, FREQ_COLUMNS, ORG_SIZE


class DataMissingError(FileNotFoundError):
    """Les CSV ne sont pas présents : lancer `uv run python get_data.py`."""


def _path(year: int, key: str = "responses") -> Path:
    return SOURCES[year][key][1]


def _check(path: Path) -> None:
    if not path.exists():
        raise DataMissingError(f"{path} introuvable. Lancez : uv run python get_data.py")
    with open(path, "rb") as fh:
        if fh.read(40).startswith(b"version https://git-lfs"):
            raise DataMissingError(f"{path} est un pointeur Git LFS, pas les données. Relancez get_data.py --force.")


def load_2026() -> pd.DataFrame:
    path = _path(2026)
    _check(path)
    return pd.read_csv(path, usecols=COLS_2026, low_memory=False)


def load_2025() -> pd.DataFrame:
    path = _path(2025)
    _check(path)
    return pd.read_csv(path, usecols=COLS_2025, low_memory=False, encoding="utf-8-sig")


def load_schema(year: int = 2026) -> pd.DataFrame:
    path = _path(year, "schema")
    _check(path)
    return pd.read_csv(path, encoding="utf-8-sig")


def exp_band(years: pd.Series) -> pd.Categorical:
    """Ancienneté professionnelle en tranches (WorkExp est une saisie libre : valeurs non numériques ignorées)."""
    x = pd.to_numeric(years, errors="coerce")
    binned = pd.cut(x, [-1, 2, 5, 10, 20, 200], labels=EXP_BANDS)
    return pd.Categorical(binned, categories=EXP_BANDS, ordered=True)


def country_label(series: pd.Series) -> pd.Series:
    return series.map(lambda c: COUNTRY.get(c, c) if isinstance(c, str) else c)


def top_countries(df: pd.DataFrame, n: int = TOP_COUNTRIES, min_count: int = 0) -> list[str]:
    """Pays les plus représentés (libellés français), triés par effectif."""
    vc = df["country_label"].value_counts()
    return [c for c, k in vc.head(n).items() if k >= min_count]


def prepare_2026(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df["is_pro_dev"] = h.is_pro_dev_2026(df)
    df["exp_band"] = exp_band(df["WorkExp"])
    df["country_label"] = country_label(df["Country"])
    df["age_label"] = pd.Categorical(df["Age"].map(AGE), categories=list(AGE.values()), ordered=True)
    df["org_label"] = pd.Categorical(df["OrgSize"].map(ORG_SIZE), categories=list(ORG_SIZE.values()), ordered=True)
    # Utilisation de l'IA au travail : NaN si la question n'a pas de réponse
    answered = df["AISelect"].notna()
    ai_user = (~df["AISelect"].fillna("").str.startswith("I don")).astype("float")
    ai_user[~answered] = float("nan")
    df["ai_user"] = ai_user
    # Usage quotidien d'au moins une famille d'outils (NaN si aucune fréquence renseignée)
    freq = df[list(FREQ_COLUMNS)]
    any_answer = freq.notna().any(axis=1)
    daily = (freq == "Daily").any(axis=1).astype("float")
    daily[~any_answer] = float("nan")
    df["ai_daily_any"] = daily
    # Variables harmonisées (comparables avec 2025)
    df["sentiment3"] = h.sentiment3(df["AISentiment"], 2026)
    df["capability5"] = h.capability5(df["AIComplex"])
    df["capability_positive"] = h.capability_positive(df["capability5"])
    df["job_sat"] = pd.to_numeric(df["JobSat"], errors="coerce")
    return df


def prepare_2025(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df["is_pro_dev"] = h.is_pro_dev_2025(df)
    df["exp_band"] = exp_band(df["WorkExp"])
    df["country_label"] = country_label(df["Country"])
    df["org_label"] = pd.Categorical(df["OrgSize"].map(_ORG_2025), categories=list(ORG_SIZE.values()), ordered=True)
    df["sentiment3"] = h.sentiment3(df["AISent"], 2025)
    df["capability5"] = h.capability5(df["AIComplex"])
    df["capability_positive"] = h.capability_positive(df["capability5"])
    return df


# Les tailles d'organisation 2025 sont libellées légèrement autrement : correspondance explicite.
_ORG_2025 = {
    "Just me - I am a freelancer, sole proprietor, etc.": "Indépendant",
    "Less than 20 employees": "< 20 salariés",
    "20 to 99 employees": "20-99",
    "100 to 499 employees": "100-499",
    "500 to 999 employees": "500-999",
    "1,000 to 4,999 employees": "1 000-4 999",
    "5,000 to 9,999 employees": "5 000-9 999",
    "10,000 or more employees": "10 000 et +",
}
