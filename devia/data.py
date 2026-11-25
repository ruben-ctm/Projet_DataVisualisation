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
