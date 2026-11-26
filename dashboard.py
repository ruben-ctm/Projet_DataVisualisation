"""Tableau de bord principal : le message pour le commanditaire (page d'accueil, ouverte par app.py)."""
from pathlib import Path

import pandas as pd
import streamlit as st

from devia import indicators, message, population
from devia.stats import share
from devia.ui import charts, state
from devia.ui.components import data_view, footer_text, guard_min_n, markdown_doc, show_figure

d26, d25, f, pop26, pop25 = state.setup("Tableau de bord", "🤖")
n_pop = len(pop26)

st.title("L'IA au travail : plus capable aux yeux des développeurs, mais toujours vérifiée")
st.caption("Enquête Stack Overflow 2026 · pour la direction technique d'une ESN française de 3 000 personnes "
           "(commanditaire fictif) qui décide comment équiper ses développeurs en assistants et agents de code.")

guard_min_n(n_pop, "cette population")
h = indicators.headline(pop26, pop25)
adopt = indicators.overall_adoption(pop26)
st.subheader(message.headline(h, f))

# ----------------------------------------------------------------------------- indicateurs
c1, c2, c3, c4 = st.columns(4)


def _delta(now: dict | None, before: dict | None) -> str | None:
    if not (now and before and now["n"] >= 30 and before["n"] >= 30):
        return None
    return f"{100 * (now['share'] - before['share']):+.0f} pts vs 2025"


c1.metric("Utilisent l'IA au travail", message.pct(adopt["share"]) if adopt["n"] >= 30 else "n/d",
          help=f"Parmi les {adopt['n']} répondants de la sélection qui ont répondu à la question sur les outils d'IA. "
               "Non comparable à 2025 : la question a changé (voir Méthode).")
cap = h["capability_2026"]
c2.metric("IA jugée capable", message.pct(cap["share"]) if cap["n"] >= 30 else "n/d",
          delta=_delta(cap, h.get("capability_2025")),
          help=f"« Bonne » ou « très bonne », parmi {cap['n']} répondants ayant un avis. Question identique en 2025 et 2026.")
sen = h["sentiment_2026"]
c3.metric("Attitude favorable envers l'IA", message.pct(sen["share"]) if sen["n"] >= 30 else "n/d",
          delta=_delta(sen, h.get("sentiment_2025")),
          help=f"« Favorable » ou « très favorable », parmi {sen['n']} répondants. Échelles harmonisées en 3 classes.")
ver = h["verify"]
c4.metric("Confiance si vérifiable", message.pct(ver["share"]) if ver["n"] >= 30 else "n/d",
          help=f"Parmi {ver['n']} répondants. Seuls {message.pct(h['high']['share']) if h['high']['n'] >= 30 else 'n/d'} "
               "font confiance à l'IA y compris pour les décisions importantes.")
st.caption(f"Population des indicateurs : {population.describe(f, 2026)} ; {n_pop:,} répondants dans la sélection "
           "(effectifs par question dans les infobulles). ".replace(",", " ") + "Volontaires d'une enquête en ligne.")
_rows = [("Utilisent l'IA au travail", 2026, adopt), ("IA jugée capable", 2026, cap), ("IA jugée capable", 2025, h.get("capability_2025")),
         ("Attitude favorable", 2026, sen), ("Attitude favorable", 2025, h.get("sentiment_2025")),
         ("Confiance seulement si vérifiable", 2026, ver), ("Confiance y compris décisions importantes", 2026, h["high"])]
data_view(pd.DataFrame([{"Indicateur": name, "Année": year, "Répondants": d["n"], "Effectif « oui »": d["k"], "Part": d["share"],
                         "IC 95 % bas": d["lo"], "IC 95 % haut": d["hi"]} for name, year, d in _rows if d]),
          "tableau_de_bord_indicateurs", "Voir les chiffres des indicateurs et les télécharger")

tab_constat, tab_france, tab_impact, tab_methode = st.tabs(
    ["Le constat", "France et reste du monde", "Ce que ça change pour l'ESN", "Méthode et limites"])

# ----------------------------------------------------------------------------- Le constat
with tab_constat:
    if pop25 is None or len(pop25) < 30:
        st.info("Données 2025 indisponibles pour cette sélection : seules les valeurs 2026 sont affichées.")
    else:
        comp = indicators.compare_capability(pop26, pop25)
        n25, n26 = int(comp["n_2025"].iloc[0]), int(comp["n_2026"].iloc[0])
        if min(n25, n26) >= 30:
            fig = charts.paired_bars(
                comp["category"], comp["share_2025"], comp["share_2026"],
                f"Capacité perçue de l'IA sur les tâches complexes : {message.pct(h['capability_2025']['share'])} → "
                f"{message.pct(h['capability_2026']['share'])} d'avis « bonne » ou « très bonne »",
                footer_text(f, 2026, n26) + f" Référence : même population en 2025 (n = {n25:,}).".replace(",", " "),
                a_ci=(comp["lo_2025"], comp["hi_2025"]), b_ci=(comp["lo_2026"], comp["hi_2026"]),
                a_n=comp["n_2025"], b_n=comp["n_2026"],
                subtitle="Répondants ayant un avis ; « je ne sais pas / pas d'usage » exclu les deux années. Barres : intervalle à 95 %.")
            show_figure(fig, f, 2026, n26, n_pop,
                        "Comparaison 2025 ↔ 2026 sur une question identique et des modalités identiques (HARMONISATION.md).")
    trust = indicators.trust_distribution(pop26)
    n_t = int(trust["n"].iloc[0])
    guard_min_n(n_t, "la question sur la confiance")
    fig = charts.hbar_shares(
        trust, "category",
        f"Quelle confiance accorder à l'IA ? {message.pct(h['verify']['share'])} seulement si le résultat est vérifiable, "
        f"{message.pct(h['high']['share'])} y compris pour les décisions importantes",
        footer_text(f, 2026, n_t), highlight=[trust["category"].iloc[0]],
        subtitle="Une seule réponse par personne. Barres : intervalle à 95 %.", wrap=44)
    show_figure(fig, f, 2026, n_t, n_pop)
    st.markdown("**Aller plus loin :** les cinq axes (menu de gauche) détaillent l'adoption, la confiance, les agents de code, "
                "les coûts cachés et l'organisation.")

# ----------------------------------------------------------------------------- France vs reste du monde
with tab_france:
    st.markdown("Le commanditaire est français : que disent les répondants de **France** par rapport aux autres pays ? "
                "Cet onglet ignore le filtre « Pays » et applique les autres filtres.")
    g_all = population.Filters(scope=f.scope, countries=(), exp_range=f.exp_range, org_sizes=f.org_sizes)
    base = population.apply_filters(d26, g_all)
    fr, rest = base[base["country_label"] == "France"], base[base["country_label"] != "France"]
    rows = []
    for name, col, sel in [("Utilisent l'IA au travail", "ai_user", None),
                           ("IA jugée capable", "capability_positive", None),
                           ("Attitude favorable", "_fav", None),
                           ("Confiance si vérifiable", "trust_verify", None)]:
        def pick(d):
            d = indicators.with_trust(d)
            d["_fav"] = (d["sentiment3"] == "Favorable").astype("float").where(d["sentiment3"].notna())
            return share(d[col])
        rows.append((name, pick(fr), pick(rest)))
    n_fr_min = min(r[1]["n"] for r in rows)
    if n_fr_min < 30:
        st.warning(f"Seulement {n_fr_min} répondant(s) français sur au moins une question avec ces filtres "
                   "(minimum 30) : la comparaison n'est pas dessinée. Élargissez ancienneté ou taille d'organisation.")
    else:
        fig = charts.paired_bars(
            [r[0] for r in rows], [r[2]["share"] for r in rows], [r[1]["share"] for r in rows],
            "France et autres pays : les quatre indicateurs côte à côte",
            footer_text(g_all, 2026, min(r[1]["n"] for r in rows)) + " Gris : autres pays ; bleu : France.",
            a_name="Autres pays", b_name="France",
            a_ci=([r[2]["lo"] for r in rows], [r[2]["hi"] for r in rows]),
            b_ci=([r[1]["lo"] for r in rows], [r[1]["hi"] for r in rows]),
            a_n=[r[2]["n"] for r in rows], b_n=[r[1]["n"] for r in rows],
            subtitle="Barres : intervalle à 95 % ; les intervalles larges signalent peu de répondants français.")
        show_figure(fig, g_all, 2026, min(r[1]["n"] for r in rows), len(base),
                    "Le titre est volontairement neutre : à lire avec les intervalles, pas avec les seuls points.")
        # Un écart n'est signalé que si les intervalles à 95 % ne se recouvrent pas.
        clear = [(name, fr_, rest_) for name, fr_, rest_ in rows if fr_["hi"] < rest_["lo"] or fr_["lo"] > rest_["hi"]]
        if clear:
            for name, fr_, rest_ in clear:
                sens = "plus bas" if fr_["share"] < rest_["share"] else "plus haut"
                st.markdown(f"- **{name}** : {message.pct(fr_['share'])} en France contre {message.pct(rest_['share'])} dans les autres pays "
                            f"({sens} en France, intervalles qui ne se recouvrent pas).")
        else:
            st.markdown("Aucun écart net entre la France et les autres pays sur ces quatre indicateurs (intervalles qui se recouvrent).")

# ----------------------------------------------------------------------------- Ce que ça change
with tab_impact:
    st.markdown("Lecture pour la direction technique, **dans les limites de ce que montrent des volontaires** :")
    for line in message.takeaways(h, f, adopt):
        st.markdown(f"- {line}")
    st.markdown(
        "- **Décision suggérée :** équiper, puis investir dans la vérification (revue de code, tests automatiques, "
        "traçabilité) plutôt que dans la seule distribution de licences. Les erreurs les plus coûteuses citées sont le code "
        "« plausible mais faux » et le code généré difficile à relire (axe 4).\n"
        "- **Ce que l'enquête ne dit pas :** elle ne mesure ni la productivité ni la qualité réelle du code, seulement ce que les "
        "répondants déclarent. Une hausse de la capacité perçue n'est pas une hausse de la capacité réelle."
    )
    _brief = Path(__file__).parent / "docs" / "04_BRIEF.md"
    if _brief.exists():
        with st.expander("Lire le brief d'une page"):
            markdown_doc(_brief)

# ----------------------------------------------------------------------------- Méthode
with tab_methode:
    st.markdown(
        "**Qui répond ?** Des volontaires qui ont rempli une enquête en ligne. Ce ne sont pas tous les développeurs : "
        "les parts décrivent les répondants. Aucun poids de redressement n'est publié.\n\n"
        "**Population par défaut.** Développeurs professionnels : le code est une partie principale du métier (2026) ou "
        "« développeur de profession » (2025), en emploi ou indépendant. Les deux libellés diffèrent légèrement.\n\n"
        "**Comparaison 2025 ↔ 2026.** Deux questions seulement sont comparables (attitude générale, capacité sur tâches "
        "complexes). La confiance, la fréquence d'usage et les agents ont changé de formulation : volontairement non comparées. "
        "Détail dans `HARMONISATION.md`."
    )
    if pop25 is not None:
        r26 = pop26["AIComplex"].notna().mean()
        r25 = pop25["AIComplex"].notna().mean()
        st.warning(f"**Taux de réponse au bloc IA :** {message.pct(r25)} des répondants de la sélection en 2025, "
                   f"{message.pct(r26)} en 2026. Si les personnes qui répondent ont changé, une partie de l'évolution "
                   "peut venir de cette composition. Contrôle : la hausse de capacité perçue existe aussi parmi les seuls "
                   "utilisateurs d'IA (voir DECISIONS.md).")
    st.dataframe(
        {"Question": ["Attitude envers l'IA", "Capacité sur tâches complexes", "Confiance", "Fréquence d'usage", "Agents"],
         "2025 → 2026": ["Comparée (3 classes)", "Comparée (5 modalités identiques)", "Non comparée : questions différentes",
                         "Non comparée : échelles différentes", "Non comparée : formulations différentes"]},
        hide_index=True, use_container_width=True)
