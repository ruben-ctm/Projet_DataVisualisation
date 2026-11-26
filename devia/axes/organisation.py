"""Axe 5 - Organisation et carrière : politique d'usage dans l'organisation, formation, critères d'adoption,
gouvernance des dépenses et satisfaction professionnelle.

Porté par Léo VAZ SAMPAIO--DESTOT. Logique pure.
"""
from __future__ import annotations

import pandas as pd

from ..config import MIN_GROUP_N
from ..labels import AI_ADOPT, AI_USE_ORG
from ..stats import distribution_by_group, multi_share, share, shares_by_group

AI_USE_ORDER = list(AI_USE_ORG.values())
SATISFIED_FROM = 8  # note de satisfaction (0-10) à partir de laquelle on dit « satisfait » : voir DECISIONS.md

TOKEN_FR = {
    "Set limits on AI tool or model usage or spending": "Plafonner l'usage ou les dépenses",
    "Reviewed internal usage or spending data for AI tools or models": "Suivre l'usage et les dépenses",
    "Approved different AI tools or models for different types of work": "Autoriser des outils différents selon le travail",
    "Set limits on who can use certain AI tools or models": "Limiter qui peut utiliser quels outils",
    "Increased spending on AI tools or models because results justified it": "Augmenter les dépenses car les résultats le justifiaient",
    "Compared buying an AI tool with building something internally": "Comparer acheter et construire en interne",
    "Stopped using or reduced spending on other software tools while increasing investment in AI tools or models": "Réduire d'autres logiciels pour investir dans l'IA",
    "Negotiated shorter commitments or the ability to switch AI tools or models over time": "Négocier des engagements courts / réversibles",
}

GROUPINGS = {
    "Ancienneté professionnelle": "exp_band",
    "Tranche d'âge": "age_label",
    "Taille de l'organisation": "org_label",
}


def with_org_use(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["org_use"] = pd.Categorical(out["AIUse"].map(AI_USE_ORG), categories=AI_USE_ORDER, ordered=True)
    return out


def org_posture_by_size(df: pd.DataFrame) -> pd.DataFrame:
    """Politique d'usage de l'IA dans l'organisation, selon la taille de l'organisation (« Not sure » exclu)."""
    return distribution_by_group(with_org_use(df), "org_use", "org_label", AI_USE_ORDER)


def org_posture_overall(df: pd.DataFrame) -> pd.DataFrame:
    s = with_org_use(df)["org_use"].dropna()
    n = len(s)
    return pd.DataFrame({"category": AI_USE_ORDER, "n": n,
                         "share": [float((s == c).sum()) / n if n else float("nan") for c in AI_USE_ORDER]})


def learning_by(df: pd.DataFrame, by_label: str, min_n: int = MIN_GROUP_N) -> pd.DataFrame:
    """Part qui a consacré du temps à apprendre l'IA l'an passé (seul, au travail ou les deux), par groupe."""
    d = df.copy()
    d["_learned"] = (d["LearnAI"] != "No").astype("float").where(d["LearnAI"].notna())
    return shares_by_group(d, "_learned", GROUPINGS[by_label], min_n=min_n)


def learning_where(df: pd.DataFrame) -> pd.DataFrame:
    """Où l'apprentissage a lieu (seul, au travail, les deux, non)."""
    labels = {"Yes, both on my own and at work": "Seul et au travail", "Yes, on my own": "Seul seulement",
              "Yes, at work": "Au travail seulement", "No": "Pas d'apprentissage"}
    from ..stats import category_shares
    t = category_shares(df["LearnAI"].map(labels), order=list(labels.values()))
    return t


def adoption_criteria(df: pd.DataFrame, top: int = 10) -> pd.DataFrame:
    """Facteurs qui comptent le plus pour adopter, poursuivre ou étendre un outil d'IA (3 choix max)."""
    t = multi_share(df["AIAdopt"], labels=AI_ADOPT, exclude=("Not sure", "Other, please specify"))
    return t.head(top).reset_index(drop=True)


def spending_governance(df: pd.DataFrame) -> pd.DataFrame:
    t = multi_share(df["AIToken"], labels=TOKEN_FR, exclude=("None of the above", "Not sure"))
    return t.reset_index(drop=True)


def satisfied_flag(df: pd.DataFrame) -> pd.Series:
    return (df["job_sat"] >= SATISFIED_FROM).astype("float").where(df["job_sat"].notna())


def jobsat_by_ai_intensity(df: pd.DataFrame) -> pd.DataFrame:
    """Part de satisfaits (note >= 8) selon l'usage quotidien de l'IA. Association, pas causalité."""
    d = df.copy()
    d["_sat"] = satisfied_flag(d)
    d["_grp"] = d["ai_daily_any"].map({1.0: "Usage quotidien de l'IA", 0.0: "Pas d'usage quotidien"})
    t = shares_by_group(d, "_sat", "_grp", order=["Usage quotidien de l'IA", "Pas d'usage quotidien"])
    return t


def jobsat_by_exp_and_ai(df: pd.DataFrame, min_n: int = MIN_GROUP_N) -> pd.DataFrame:
    """Même comparaison à ancienneté égale : l'ancienneté influe à la fois sur l'usage et sur la satisfaction."""
    d = df.copy()
    d["_sat"] = satisfied_flag(d)
    rows = []
    for band in d["exp_band"].cat.categories:
        for lab, val in (("Usage quotidien de l'IA", 1.0), ("Pas d'usage quotidien", 0.0)):
            sub = d[(d["exp_band"] == band) & (d["ai_daily_any"] == val)]["_sat"]
            r = share(sub)
            if r["n"] >= min_n:
                rows.append({"exp_band": band, "usage": lab, **r})
    return pd.DataFrame(rows, columns=["exp_band", "usage", "n", "k", "share", "lo", "hi"])
