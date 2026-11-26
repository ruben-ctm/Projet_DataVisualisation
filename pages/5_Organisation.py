"""Axe 5 - Organisation et carrière (Léo VAZ SAMPAIO--DESTOT) : politique d'usage, formation, adoption, satisfaction."""
import streamlit as st

from devia import message
from devia.axes import organisation as ax
from devia.ui import charts, components, state

d26, d25, f, pop, _ = state.setup("Organisation", "🏢")
n_pop = len(pop)
components.header("Axe 5 · Organisation et carrière",
                  "Comment les organisations encadrent-elles l'IA, qu'est-ce qui décide de l'adopter, et que change-t-elle pour les personnes ?",
                  "Léo VAZ SAMPAIO--DESTOT")
components.guard_min_n(n_pop, "cette population")

# --- 1. Politique d'usage selon la taille -------------------------------------------------------------------
st.header("Comment les organisations encadrent-elles l'IA ?")
st.caption("Le filtre « Taille de l'organisation » du panneau de gauche s'applique ici aussi.")
t = ax.org_posture_by_size(pop)
if t.empty:
    st.warning("Aucune taille d'organisation n'atteint 30 répondants avec ces filtres.")
else:
    n_fig = int(t["n"].sum())
    colors = [charts.GRAY, charts.SEQ_BLUES[0], charts.SEQ_BLUES[1], charts.SEQ_BLUES[2], charts.SEQ_BLUES[3], charts.SEQ_BLUES[4]]
    appr = ax.AI_USE_ORDER[3]
    lo_g, hi_g = t[appr].idxmin(), t[appr].idxmax()
    fig = charts.stacked_hbar(t, colors, f"Outils approuvés et consignes : {message.pct(t.loc[lo_g, appr])} ({lo_g}) contre {message.pct(t.loc[hi_g, appr])} ({hi_g})",
                              components.footer_text(f, 2026, n_fig), subtitle="Une seule réponse par personne ; « je ne sais pas » exclu.",
                              wrap=22, min_label=0.07)
    components.show_figure(fig, f, 2026, n_fig, n_pop)
    components.data_view(t, "organisation_posture_par_taille")
    components.dropped_note(t.attrs.get("dropped", []))

# --- 2. Critères d'adoption et gouvernance -----------------------------------------------------------------
st.header("Qu'est-ce qui décide d'adopter un outil ?")
crit = ax.adoption_criteria(pop)
n_c = int(crit["n"].iloc[0]) if not crit.empty else 0
components.guard_min_n(n_c, "la question sur les critères d'adoption")
fig = charts.hbar_shares(crit, "option", f"Critère n° 1 : « {crit['option'].iloc[0].lower()} » ({message.pct(crit['share'].iloc[0])})",
                         components.footer_text(f, 2026, n_c), xlim=(0, 0.6), highlight=list(crit["option"].head(3)),
                         subtitle="Trois facteurs au plus par personne ; « je ne sais pas » et « autre » exclus de l'affichage mais comptés au dénominateur.",
                         wrap=44)
components.show_figure(fig, f, 2026, n_c, n_pop)
components.data_view(crit, "organisation_criteres_adoption")

gov = ax.spending_governance(pop)
n_g = int(gov["n"].iloc[0]) if not gov.empty else 0
if n_g >= 30:
    fig = charts.hbar_shares(gov, "option", f"Dépenses d'IA : « {gov['option'].iloc[0].lower()} » est l'action la plus citée",
                             components.footer_text(f, 2026, n_g), xlim=(0, 0.7), subtitle="Actions de l'organisation sur ses dépenses d'IA (choix multiple).", wrap=44)
    components.show_figure(fig, f, 2026, n_g, n_pop)
    components.data_view(gov, "organisation_depenses_ia")

# --- 3. Apprentissage ---------------------------------------------------------------------------------------
st.header("Qui se forme à l'IA ?")
by = st.selectbox("Regrouper par", list(ax.GROUPINGS), index=1, key="a5_by")
t = ax.learning_by(pop, by)
if t.empty:
    st.warning("Aucun groupe n'atteint 30 répondants avec ces filtres.")
else:
    n_l = int(t["n"].sum())
    fig = charts.hbar_shares(t, "group", f"Part qui a consacré du temps à apprendre l'IA l'an passé, selon le groupe ({by.lower()})",
                             components.footer_text(f, 2026, n_l), xlim=(0, 1.0),
                             subtitle="Seul, au travail ou les deux, par opposition à « non ».")
    components.show_figure(fig, f, 2026, n_l, n_pop)
    components.data_view(t, "organisation_apprentissage")

# --- 4. Satisfaction professionnelle ------------------------------------------------------------------------------
st.header("Usage quotidien de l'IA et satisfaction au travail")
st.caption("Association observée chez des volontaires, pas un effet démontré : les personnes très satisfaites utilisent peut-être "
           "davantage l'IA. Satisfait = note de 8 à 10 sur 10.")
sat = ax.jobsat_by_exp_and_ai(pop)
if sat.empty:
    st.warning("Pas assez de répondants (30 minimum par groupe) avec ces filtres.")
else:
    bands = [b for b in sat["exp_band"].unique() if (sat["exp_band"] == b).sum() == 2]
    if not bands:
        st.warning("Aucune tranche d'ancienneté n'a assez de répondants dans les deux modes d'usage.")
    else:
        d = sat[sat["exp_band"].isin(bands)]
        a = d[d["usage"] == "Pas d'usage quotidien"].set_index("exp_band").loc[bands]
        b = d[d["usage"] == "Usage quotidien de l'IA"].set_index("exp_band").loc[bands]
        n_s = int(d["n"].sum())
        higher = int((b["share"] > a["share"].values).sum())
        fig = charts.paired_bars(
            [str(x) for x in bands], a["share"], b["share"],
            f"À ancienneté égale, plus de satisfaits chez les utilisateurs quotidiens dans {higher} tranche(s) sur {len(bands)}",
            components.footer_text(f, 2026, n_s), a_name="Pas d'usage quotidien", b_name="Usage quotidien de l'IA",
            a_ci=(a["lo"], a["hi"]), b_ci=(b["lo"], b["hi"]), a_n=a["n"], b_n=b["n"],
            subtitle="Part de satisfaits (note ≥ 8) par tranche d'ancienneté. Barres : intervalle à 95 %.")
        components.show_figure(fig, f, 2026, n_s, n_pop)
        components.data_view(sat, "organisation_satisfaction")
st.info("Pas de comparaison avec 2025 sur cet axe : politiques d'organisation et critères d'adoption sont nouveaux en 2026.")
