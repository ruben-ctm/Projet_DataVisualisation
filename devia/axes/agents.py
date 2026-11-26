"""Axe 3 - Agents de code et outils : quels assistants / agents de code, quels fournisseurs de modèles.

Porté par Edwin DREAN-AVRILLON. Logique pure.
Les listes d'outils sont des réponses à choix multiples stockées sous forme « A;B;C ».
"""
from __future__ import annotations

import pandas as pd

from ..config import MIN_GROUP_N
from ..stats import category_shares, contains_flag, multi_share, shares_by_group, wilson_ci

HAVE, WANT, ADMIRED = "AICodeAgentHaveWorkedWith", "AICodeAgentWantToUseNext6Months", "AICodeAgentAdmired"

GROUPINGS = {
    "Ancienneté professionnelle": "exp_band",
    "Tranche d'âge": "age_label",
    "Taille de l'organisation": "org_label",
    "Pays": "country_label",
}


def _split(series: pd.Series) -> pd.Series:
    return series.dropna().str.split(";").apply(lambda xs: [x.strip() for x in xs if x.strip()])


def tool_table(df: pd.DataFrame, min_users: int = MIN_GROUP_N) -> pd.DataFrame:
    """Une ligne par outil : part d'utilisateurs, part qui veut le (ré)utiliser, taux d'admiration.

    - part d'utilisation = utilisateurs / répondants à la question « utilisé l'an passé » ;
    - souhait = répondants citant l'outil / répondants à « veux utiliser dans 6 mois » ;
    - admiration = parmi les utilisateurs de l'outil **qui ont aussi répondu à la question « souhait »**, part
      qui veulent le réutiliser. Une case « souhait » vide est traitée comme une absence de réponse : sinon
      39 % des utilisateurs de Claude Code seraient comptés « ne veut pas le réutiliser » sans l'avoir dit
      (voir DECISIONS.md). Les outils de moins de `min_users` utilisateurs sont écartés.
    """
    have, want = _split(df[HAVE]), _split(df[WANT])
    n_have, n_want = len(have), len(want)
    both = df[HAVE].notna() & df[WANT].notna()
    have_b, want_b = _split(df.loc[both, HAVE]), _split(df.loc[both, WANT])
    used = have.explode().value_counts()
    wanted = want.explode().value_counts()
    used_b = have_b.explode().value_counts()
    # admiré = a utilisé ET veut réutiliser (parmi ceux qui ont répondu aux deux questions)
    admired = pd.Series([t for h_, w_ in zip(have_b, want_b) for t in set(h_) & set(w_)]).value_counts()
    rows = []
    for tool, k in used.items():
        if k < min_users:
            continue
        lo, hi = wilson_ci(int(k), n_have)
        kb = int(used_b.get(tool, 0))
        ka = int(admired.get(tool, 0))
        alo, ahi = wilson_ci(ka, kb) if kb else (float("nan"),) * 2
        kw = int(wanted.get(tool, 0))
        wlo, whi = wilson_ci(kw, n_want) if n_want else (float("nan"),) * 2
        rows.append({"tool": tool, "n_have": n_have, "k_used": int(k), "share_used": k / n_have, "lo": lo, "hi": hi,
                     "k_used_both": kb, "k_admired": ka, "admiration": ka / kb if kb else float("nan"),
                     "adm_lo": alo, "adm_hi": ahi,
                     "n_want": n_want, "k_want": kw, "share_want": kw / n_want if n_want else float("nan"),
                     "want_lo": wlo, "want_hi": whi})
    cols = ["tool", "n_have", "k_used", "share_used", "lo", "hi", "k_used_both", "k_admired", "admiration", "adm_lo",
            "adm_hi", "n_want", "k_want", "share_want", "want_lo", "want_hi"]
    return pd.DataFrame(rows, columns=cols).sort_values("share_used", ascending=False).reset_index(drop=True)


def tools_per_person(df: pd.DataFrame, cap: int = 4) -> pd.DataFrame:
    """Nombre d'assistants / agents de code différents utilisés l'an passé (1, 2, 3, 4 et +)."""
    counts = _split(df[HAVE]).apply(len)
    labels = [str(i) for i in range(1, cap)] + [f"{cap} et +"]
    binned = counts.clip(lower=1, upper=cap).map(lambda v: labels[v - 1])
    return category_shares(binned, order=labels)


def providers(df: pd.DataFrame, top: int = 10) -> pd.DataFrame:
    """Fournisseurs de modèles de langage utilisés l'an passé (part des répondants à la question)."""
    t = multi_share(df["LLMHaveWorkedWith"], exclude=("Other, please specify",))
    return t.head(top).reset_index(drop=True)


def tool_share_by(df: pd.DataFrame, tool: str, by_label: str, min_n: int = MIN_GROUP_N) -> pd.DataFrame:
    """Part des répondants (à la question « utilisé l'an passé ») qui ont utilisé `tool`, par groupe."""
    d = df.copy()
    d["_uses"] = contains_flag(d[HAVE], tool)
    col = GROUPINGS[by_label]
    order = None
    if col == "country_label":
        order = [g for g, k in d.loc[d["_uses"].notna(), col].value_counts().items() if k >= min_n][:10]
    t = shares_by_group(d, "_uses", col, order=order, min_n=min_n)
    return t.sort_values("share", ascending=False).reset_index(drop=True) if col == "country_label" else t
