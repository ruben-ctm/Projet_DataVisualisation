"""Indicateurs partagés : les chiffres du message principal, calculés une seule fois pour tout le monde.

Le tableau de bord (socle commun) et les axes 1 et 2 s'appuient sur ces fonctions : le chiffre affiché sur la
page d'accueil est donc exactement celui de l'axe qui le détaille. Logique pure, sans Streamlit.
"""
from __future__ import annotations

import math

import pandas as pd

from .harmonisation import CAPABILITY_ORDER
from .labels import TRUST
from .stats import category_shares, share

TRUST_ORDER = list(TRUST.values())
VERIFY = TRUST["I trust it when I can easily verify the output"]
HIGH = TRUST["I trust it for many tasks, including important work decisions"]


def with_trust(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute `trust_label` (libellé français ordonné ; « Not sure / I do not use » exclu) et deux indicateurs."""
    out = df.copy()
    out["trust_label"] = pd.Categorical(out["AITrust"].map(TRUST), categories=TRUST_ORDER, ordered=True)
    known = out["trust_label"].notna()
    out["trust_verify"] = (out["trust_label"] == VERIFY).astype("float").where(known)
    out["trust_high"] = (out["trust_label"] == HIGH).astype("float").where(known)
    return out


def trust_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return category_shares(with_trust(df)["trust_label"], order=TRUST_ORDER)


def capability_distribution(df: pd.DataFrame) -> pd.DataFrame:
    return category_shares(df["capability5"], order=CAPABILITY_ORDER)


# ------------------------------------------------------------------ comparaison 2025 <-> 2026


def compare_capability(p26: pd.DataFrame, p25: pd.DataFrame) -> pd.DataFrame:
    """Distribution de la capacité perçue (5 modalités harmonisées), 2025 et 2026 côte à côte."""
    a, b = capability_distribution(p25), capability_distribution(p26)
    return pd.DataFrame({"category": CAPABILITY_ORDER, "share_2025": a["share"].values, "lo_2025": a["lo"].values,
                         "hi_2025": a["hi"].values, "n_2025": a["n"].values, "share_2026": b["share"].values,
                         "lo_2026": b["lo"].values, "hi_2026": b["hi"].values, "n_2026": b["n"].values})


def headline(p26: pd.DataFrame, p25: pd.DataFrame | None) -> dict:
    """Chiffres du message principal : une seule source pour le tableau de bord et l'axe."""
    t = with_trust(p26)
    out = {
        "capability_2026": share(p26["capability_positive"]),
        "sentiment_2026": share((p26["sentiment3"] == "Favorable").where(p26["sentiment3"].notna())),
        "verify": share(t["trust_verify"]),
        "high": share(t["trust_high"]),
    }
    if p25 is not None:
        out["capability_2025"] = share(p25["capability_positive"])
        out["sentiment_2025"] = share((p25["sentiment3"] == "Favorable").where(p25["sentiment3"].notna()))
    return out


def diff_points(a: dict, b: dict) -> tuple[float, float, float]:
    """Écart b - a (en part) et intervalle approché à 95 % (méthode de Wald sur la différence)."""
    d = b["share"] - a["share"]
    se = math.sqrt(b["share"] * (1 - b["share"]) / b["n"] + a["share"] * (1 - a["share"]) / a["n"])
    return d, d - 1.96 * se, d + 1.96 * se


def overall_adoption(df: pd.DataFrame) -> dict:
    return share(df["ai_user"])
