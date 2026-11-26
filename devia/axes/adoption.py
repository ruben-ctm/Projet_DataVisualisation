"""Axe 1 - Adoption : qui utilise l'IA au travail, à quelle fréquence, avec quels types d'outils.

Porté par Ruben COMBE--TAMAIN. Logique pure : tables en entrée/sortie, aucun Streamlit.
"""
from __future__ import annotations

import pandas as pd

from ..labels import FREQ, FREQ_COLUMNS, TOOL_FAMILY
from ..indicators import overall_adoption  # noqa: F401  (indicateur partagé avec le tableau de bord)
from ..stats import category_shares, multi_share, shares_by_group

ROLE_FR = {
    "Developer, full-stack": "Développeur full-stack", "Developer, back-end": "Développeur back-end",
    "Developer, front-end": "Développeur front-end", "Developer, mobile": "Développeur mobile",
    "Developer, desktop or enterprise applications": "Développeur applications d'entreprise",
    "Developer, embedded applications or devices": "Développeur embarqué",
    "Architect, software or solutions": "Architecte", "Engineering manager": "Responsable d'ingénierie",
    "DevOps engineer or professional": "DevOps", "AI/ML engineer": "Ingénieur IA / ML",
    "Data engineer": "Data engineer", "Data scientist": "Data scientist",
    "Developer, QA or test": "Développeur QA / test", "Software engineer": "Ingénieur logiciel",
    "Cloud infrastructure engineer": "Ingénieur cloud", "Cybersecurity or InfoSec professional": "Cybersécurité",
}

# Regroupements proposés au lecteur : libellé affiché -> colonne de la table préparée
GROUPINGS = {
    "Tranche d'âge": "age_label",
    "Ancienneté professionnelle": "exp_band",
    "Taille de l'organisation": "org_label",
    "Pays": "country_label",
    "Métier": "role_label",
}
NOT_USER = "I don’t use AI tools"


def with_role_label(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["role_label"] = out["Role"].map(lambda r: ROLE_FR.get(r, None) if isinstance(r, str) else None)
    return out


def adoption_by(df: pd.DataFrame, by_label: str, min_n: int = 30) -> pd.DataFrame:
    """Part des répondants qui utilisent au moins un type d'outil d'IA au travail, par groupe."""
    col = GROUPINGS[by_label]
    d = with_role_label(df) if col == "role_label" else df
    order = None
    if col in ("country_label", "role_label"):  # beaucoup de modalités : celles qui ont assez de réponses, triées par effectif
        order = [g for g, k in d.loc[d["ai_user"].notna(), col].value_counts().items() if k >= min_n][:12]
    t = shares_by_group(d, "ai_user", col, order=order, min_n=min_n)
    if col in ("country_label", "role_label"):
        t = t.sort_values("share", ascending=False).reset_index(drop=True)
    return t


def tool_families(df: pd.DataFrame) -> pd.DataFrame:
    """Part des répondants (à AISelect) qui citent chaque famille d'outils d'IA utilisée au travail."""
    t = multi_share(df["AISelect"], labels=TOOL_FAMILY, exclude=(NOT_USER,))
    return t.sort_values("share", ascending=False).reset_index(drop=True)


def frequency_by_family(df: pd.DataFrame) -> pd.DataFrame:
    """Fréquence d'usage par famille d'outils, parmi ceux qui l'ont renseignée (table large, parts par ligne)."""
    rows = {}
    for col, fam in FREQ_COLUMNS.items():
        s = df[col].dropna()
        n = len(s)
        if n == 0:
            continue
        rows[fam] = {**{label: float((s == raw).sum()) / n for raw, label in FREQ.items()}, "n": n}
    return pd.DataFrame.from_dict(rows, orient="index", columns=[*FREQ.values(), "n"])


def daily_share_by(df: pd.DataFrame, by_label: str, min_n: int = 30) -> pd.DataFrame:
    """Part des répondants qui utilisent au moins une famille d'outils tous les jours, par groupe."""
    col = GROUPINGS[by_label]
    d = with_role_label(df) if col == "role_label" else df
    order = None
    if col in ("country_label", "role_label"):
        order = [g for g, k in d.loc[d["ai_daily_any"].notna(), col].value_counts().items() if k >= min_n][:12]
    t = shares_by_group(d, "ai_daily_any", col, order=order, min_n=min_n)
    if col in ("country_label", "role_label"):
        t = t.sort_values("share", ascending=False).reset_index(drop=True)
    return t


def tool_count_distribution(df: pd.DataFrame, cap: int = 5) -> pd.DataFrame:
    """Nombre d'outils d'IA distincts utilisés chaque semaine (0 à `cap`+), parmi les répondants."""
    n = pd.to_numeric(df["AIToolCount"], errors="coerce").dropna()
    n = n[(n >= 0) & (n <= 50)]  # saisie libre : on écarte les valeurs aberrantes
    labels = [str(i) for i in range(cap)] + [f"{cap} et +"]
    binned = n.clip(upper=cap).astype(int).map(lambda v: labels[v])
    return category_shares(binned, order=labels)
