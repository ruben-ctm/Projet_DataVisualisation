"""Recalcule tous les chiffres du brief d'une page et ses trois figures à partir des données brutes.

    uv run python scripts/build_brief.py

Sorties : `docs/preuves.csv` (une ligne par chiffre cité dans `docs/04_BRIEF.md`, avec sa population et son
intervalle) et `docs/figures/figure_{1,2,3}.png`. Les calculs réutilisent les fonctions de l'application
(`devia/`) : le brief et le tableau de bord ne peuvent donc pas diverger.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from devia import data, indicators, population  # noqa: E402
from devia.axes import couts  # noqa: E402
from devia.config import DATA_DIR  # noqa: E402
from devia.stats import share  # noqa: E402
from devia.ui import charts  # noqa: E402

DOCS = ROOT / "docs"
POP = "Développeurs professionnels, Stack Overflow {year}"


def pct0(x: float) -> str:
    """Format du brief : pourcentage entier, espace insécable avant « % »."""
    return f"{round(100 * x)} %"


def build() -> tuple[pd.DataFrame, dict]:
    d26, d25 = data.prepare_2026(data.load_2026()), data.prepare_2025(data.load_2025())
    f = population.Filters()
    p26, p25 = population.apply_filters(d26, f), population.apply_filters(d25, f)
    h = indicators.headline(p26, p25)

    # Contrôle « utilisateurs » : en 2025 la variable d'usage n'est pas dans les colonnes lues par l'application.
    raw25 = pd.read_csv(DATA_DIR / "2025" / "results.csv", usecols=["ResponseId", "AISelect"], encoding="utf-8-sig")
    u25 = p25.merge(raw25, on="ResponseId")
    u25 = u25[u25["AISelect"].fillna("").str.startswith("Yes")]
    u26 = p26[p26["ai_user"] == 1]

    err = couts.disruption_shares(p26, top=2)
    rows: list[dict] = []

    def add(pid: str, claim: str, d: dict, year: int, pop_note: str, fn: str) -> None:
        rows.append({"id": pid, "affirmation": claim, "valeur": round(d["share"], 4), "texte": pct0(d["share"]),
                     "n": d["n"], "ic_bas": round(d["lo"], 4), "ic_haut": round(d["hi"], 4),
                     "population": f"{POP.format(year=year)}{pop_note}", "calcul": fn})

    add("P01", "Utilisent l'IA au travail", indicators.overall_adoption(p26), 2026, "", "indicators.overall_adoption")
    add("P02", "IA jugée capable (bonne ou très bonne), 2025", h["capability_2025"], 2025, ", ayant un avis", "indicators.headline")
    add("P03", "IA jugée capable (bonne ou très bonne), 2026", h["capability_2026"], 2026, ", ayant un avis", "indicators.headline")
    add("P04", "Attitude favorable, 2025", h["sentiment_2025"], 2025, "", "indicators.headline")
    add("P05", "Attitude favorable, 2026", h["sentiment_2026"], 2026, "", "indicators.headline")
    add("P06", "Confiance seulement si le résultat est vérifiable", h["verify"], 2026, "", "indicators.headline")
    add("P07", "Confiance y compris pour les décisions importantes", h["high"], 2026, "", "indicators.headline")
    add("P08", "IA jugée capable parmi les utilisateurs d'IA, 2025", share(u25["capability_positive"]), 2025,
        ", utilisateurs d'IA", "contrôle (AISelect = Yes)")
    add("P09", "IA jugée capable parmi les utilisateurs d'IA, 2026", share(u26["capability_positive"]), 2026,
        ", utilisateurs d'IA", "contrôle (ai_user = 1)")
    add("P10", "A répondu à la question de capacité, 2025", share(p25["AIComplex"].notna()), 2025, ", tous", "taux de réponse")
    add("P11", "A répondu à la question de capacité, 2026", share(p26["AIComplex"].notna()), 2026, ", tous", "taux de réponse")
    for i, r in err.iterrows():
        add(f"P{12 + i}", f"Erreur ayant fait perdre le plus de temps : {r['option']}",
            {"share": r["share"], "n": int(r["n"]), "lo": r["lo"], "hi": r["hi"]}, 2026, ", ayant répondu", "axes.couts.disruption_shares")

    pre = pd.DataFrame(rows)
    return pre, {"h": h, "p26": p26, "p25": p25, "f": f, "u25": u25, "u26": u26, "pre": pre}


def figures(ctx: dict) -> None:
    h, p26, f, pre = ctx["h"], ctx["p26"], ctx["f"], ctx["pre"].set_index("id")
    foot = lambda year, n: population.plain_caption(f, year, n) + " Volontaires d'une enquête en ligne, pas tous les développeurs."  # noqa: E731
    row = lambda k: pre.loc[k]  # noqa: E731

    # Figure 1 : comparaison principale (même question et mêmes modalités les deux années).
    a = [row("P02"), row("P04")]
    b = [row("P03"), row("P05")]
    fig = charts.paired_bars(
        ["IA jugée capable sur les tâches complexes", "Attitude générale favorable envers l'IA"],
        [x["valeur"] for x in a], [x["valeur"] for x in b],
        f"Les développeurs jugent l'IA plus capable ({row('P02')['texte']} → {row('P03')['texte']}), "
        f"sans être plus favorables ({row('P04')['texte']} → {row('P05')['texte']})".replace(" ", " "),
        foot(2026, int(row("P03")["n"])) + " 2025 : mêmes questions, échelles harmonisées.",
        a_ci=([x["ic_bas"] for x in a], [x["ic_haut"] for x in a]), b_ci=([x["ic_bas"] for x in b], [x["ic_haut"] for x in b]),
        a_n=[x["n"] for x in a], b_n=[x["n"] for x in b],
        subtitle="Parts parmi les répondants ayant un avis. Barres d'erreur : intervalle de confiance à 95 %.")
    fig.savefig(DOCS / "figures" / "figure_1.png", dpi=160)

    # Figure 2 : la nuance (la confiance reste conditionnée).
    trust = indicators.trust_distribution(p26)
    fig = charts.hbar_shares(
        trust, "category",
        f"Malgré tout, {row('P06')['texte']} ne font confiance à l'IA que si le résultat est vérifiable ; "
        f"{row('P07')['texte']} l'acceptent pour les décisions importantes".replace(" ", " "),
        foot(2026, int(trust["n"].iloc[0])), highlight=[trust["category"].iloc[0]],
        subtitle="Une seule réponse par personne. Barres d'erreur : intervalle de confiance à 95 %.", wrap=44)
    fig.savefig(DOCS / "figures" / "figure_2.png", dpi=160)

    # Figure 3 : la méthode (ce qui pourrait fausser la hausse).
    labels = ["IA jugée capable, parmi les répondants ayant un avis", "IA jugée capable, parmi les seuls utilisateurs d'IA",
              "A répondu à la question de capacité (taux de réponse)"]
    a = [row("P02"), row("P08"), row("P10")]
    b = [row("P03"), row("P09"), row("P11")]
    fig = charts.paired_bars(
        labels, [x["valeur"] for x in a], [x["valeur"] for x in b],
        f"La hausse tient chez les seuls utilisateurs ({row('P08')['texte']} → {row('P09')['texte']}), "
        f"mais moins de répondants ont répondu ({row('P10')['texte']} → {row('P11')['texte']})".replace(" ", " "),
        foot(2026, int(row("P11")["n"])) + " Définition d'« utilisateur » différente entre 2025 et 2026 (voir DECISIONS.md).",
        a_ci=([x["ic_bas"] for x in a], [x["ic_haut"] for x in a]), b_ci=([x["ic_bas"] for x in b], [x["ic_haut"] for x in b]),
        a_n=[x["n"] for x in a], b_n=[x["n"] for x in b], wrap=36,
        subtitle="Le contrôle écarte un simple changement de la part d'utilisateurs ; il n'écarte pas un changement de qui répond.")
    fig.savefig(DOCS / "figures" / "figure_3.png", dpi=160)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "figures").mkdir(exist_ok=True)
    pre, ctx = build()
    pre.to_csv(DOCS / "preuves.csv", index=False, encoding="utf-8")
    figures(ctx)
    print(pre[["id", "affirmation", "texte", "n", "ic_bas", "ic_haut"]].to_string(index=False))


if __name__ == "__main__":
    main()
