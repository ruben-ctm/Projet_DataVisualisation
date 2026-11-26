"""Axe 4 - Coûts cachés de l'IA : erreurs qui font perdre du temps, freins, utilité et satisfaction par tâche.

Porté par Arthur REYNAUD. Logique pure.
"""
from __future__ import annotations

import pandas as pd

from ..config import MIN_GROUP_N
from ..labels import (AI_AVOID, DISRUPTION, SAT_NEGATIVE, SAT_POSITIVE, TASKS, USEFUL_IGNORE, USEFUL_NEGATIVE,
                      USEFUL_POSITIVE)
from ..stats import contains_flag, multi_share, shares_by_group, wilson_ci

GROUPINGS = {
    "Ancienneté professionnelle": "exp_band",
    "Tranche d'âge": "age_label",
    "Taille de l'organisation": "org_label",
}
DISRUPTION_REV = {v: k for k, v in DISRUPTION.items()}


def disruption_shares(df: pd.DataFrame, top: int | None = None) -> pd.DataFrame:
    """Erreurs d'IA qui ont fait perdre le plus de temps (choix multiple) : part des répondants citant chacune."""
    t = multi_share(df["Disruption"], labels=DISRUPTION)
    t = t[t["option"] != DISRUPTION["Other, please specify"]]
    return (t.head(top) if top else t).reset_index(drop=True)


def disruption_by(df: pd.DataFrame, option_fr: str, by_label: str, min_n: int = MIN_GROUP_N) -> pd.DataFrame:
    """Part des répondants citant une erreur donnée, par groupe."""
    d = df.copy()
    d["_cited"] = contains_flag(d["Disruption"], DISRUPTION_REV[option_fr])
    return shares_by_group(d, "_cited", GROUPINGS[by_label], min_n=min_n)


def avoid_reasons(df: pd.DataFrame) -> pd.DataFrame:
    """Raisons d'éviter l'IA (une seule réponse possible) : parts parmi les répondants."""
    s = df["AIAvoid"].dropna()
    n = len(s)
    rows = []
    for raw, label in AI_AVOID.items():
        k = int((s == raw).sum())
        lo, hi = wilson_ci(k, n)
        rows.append({"option": label, "n": n, "k": k, "share": k / n if n else float("nan"), "lo": lo, "hi": hi})
    t = pd.DataFrame(rows)
    return t.sort_values("share", ascending=False).reset_index(drop=True)


def _task_rows(df: pd.DataFrame, prefix: str, positive: list[str], negative: list[str], ignore: list[str]) -> pd.DataFrame:
    rows = []
    for i, task in TASKS.items():
        s = df[f"{prefix}_{i}"].dropna()
        s = s[~s.isin(ignore)]
        n = len(s)
        if n == 0:
            continue
        kp, kn = int(s.isin(positive).sum()), int(s.isin(negative).sum())
        plo, phi = wilson_ci(kp, n)
        nlo, nhi = wilson_ci(kn, n)
        rows.append({"task": task, "n": n, "share_pos": kp / n, "pos_lo": plo, "pos_hi": phi,
                     "share_neg": kn / n, "neg_lo": nlo, "neg_hi": nhi, "net": (kp - kn) / n})
    return pd.DataFrame(rows)


def usefulness_by_task(df: pd.DataFrame) -> pd.DataFrame:
    """Utilité perçue par tâche : « Utile / Très utile » contre « Plus gênant qu'utile » ('Non applicable' exclu)."""
    return _task_rows(df, "AIImpact", USEFUL_POSITIVE, USEFUL_NEGATIVE, USEFUL_IGNORE).sort_values("net", ascending=False).reset_index(drop=True)


def satisfaction_by_task(df: pd.DataFrame) -> pd.DataFrame:
    """Effet de l'IA sur la satisfaction à accomplir la tâche : « améliorée » contre « diminuée »."""
    return _task_rows(df, "AISat", SAT_POSITIVE, SAT_NEGATIVE, []).sort_values("net", ascending=False).reset_index(drop=True)


def net_by_group(df: pd.DataFrame, task: str, by_label: str, kind: str = "useful", min_n: int = MIN_GROUP_N) -> pd.DataFrame:
    """Part « positif » pour une tâche donnée, par groupe (kind = 'useful' ou 'sat')."""
    idx = {v: k for k, v in TASKS.items()}[task]
    d = df.copy()
    if kind == "useful":
        s = d[f"AIImpact_{idx}"]
        s = s.where(~s.isin(USEFUL_IGNORE))
        d["_pos"] = s.isin(USEFUL_POSITIVE).astype("float").where(s.notna())
    else:
        s = d[f"AISat_{idx}"]
        d["_pos"] = s.isin(SAT_POSITIVE).astype("float").where(s.notna())
    return shares_by_group(d, "_pos", GROUPINGS[by_label], min_n=min_n)
