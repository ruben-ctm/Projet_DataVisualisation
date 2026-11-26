"""Axe 1 - Adoption (Ruben COMBE--TAMAIN) : qui utilise l'IA au travail, à quelle fréquence, avec quels outils."""
import streamlit as st

from devia import message
from devia.axes import adoption as ax
from devia.ui import charts, components, state

d26, d25, f, pop, _ = state.setup("Adoption", "🚀")
n_pop = len(pop)
components.header("Axe 1 · Adoption de l'IA",
                  "Quels profils sont déjà équipés, avec quels types d'outils, et à quel rythme ?", "Ruben COMBE--TAMAIN")
components.guard_min_n(n_pop, "cette population")

overall = ax.overall_adoption(pop)
components.guard_min_n(overall["n"], "la question sur l'usage de l'IA")

# --- 1. Qui ? ---------------------------------------------------------------------------------
st.header("Qui utilise l'IA ?")
c1, c2 = st.columns([2, 3])
by = c1.selectbox("Regrouper par", list(ax.GROUPINGS), index=1, key="a1_by",
                  help="Dimension de comparaison. Pays et Métier montrent les groupes d'au moins 30 répondants (12 au plus).")
metric = c2.radio("Indicateur", ["Utilise l'IA au travail", "Utilise l'IA tous les jours"], horizontal=True, key="a1_metric",
                  help="« Tous les jours » : au moins une famille d'outils utilisée quotidiennement, parmi ceux qui ont indiqué des fréquences.")
tbl = ax.adoption_by(pop, by) if metric.startswith("Utilise l'IA au") else ax.daily_share_by(pop, by)
if tbl.empty:
    st.warning("Aucun groupe n'atteint 30 répondants avec ces filtres : rien n'est dessiné. Élargissez la sélection.")
else:
    n_fig = int(tbl["n"].sum())
    lo_g, hi_g = tbl.loc[tbl["share"].idxmin()], tbl.loc[tbl["share"].idxmax()]
    verb = "utilisent l'IA au travail" if metric.startswith("Utilise l'IA au") else "utilisent l'IA tous les jours"
    title = (f"Selon le groupe, entre {message.pct(lo_g['share'])} ({lo_g['group']}) et "
             f"{message.pct(hi_g['share'])} ({hi_g['group']}) {verb}")
    fig = charts.hbar_shares(tbl, "group", title, components.footer_text(f, 2026, n_fig),
                             subtitle=f"Groupe : {by.lower()}. Barres : intervalle à 95 %.", xlim=(0, 1.0))
    components.show_figure(fig, f, 2026, n_fig, n_pop, "Effectif = somme des répondants des groupes affichés.")
    components.dropped_note(tbl.attrs.get("dropped", []))
    components.data_view(tbl, "adoption_par_groupe")

# --- 2. Quels outils et quel rythme ? --------------------------------------------------------------
st.header("Quels types d'outils, à quel rythme ?")
fam = ax.tool_families(pop)
n_f = int(fam["n"].iloc[0])
components.guard_min_n(n_f, "la question sur les familles d'outils")
fig = charts.hbar_shares(fam, "option",
                         f"Les assistants et agents de code sont cités par {message.pct(fam['share'].iloc[0])}"
                         if fam["option"].iloc[0].startswith("Assistants") else
                         f"{fam['option'].iloc[0]} : {message.pct(fam['share'].iloc[0])} des répondants",
                         components.footer_text(f, 2026, n_f),
                         subtitle="Choix multiple : les parts ne somment pas à 100 %. Non-utilisateurs inclus dans le dénominateur.",
                         xlim=(0, 1.0), wrap=40)
components.show_figure(fig, f, 2026, n_f, n_pop)
components.data_view(fam, "adoption_familles_outils")

freq = ax.frequency_by_family(pop)
if not freq.empty and freq["n"].min() >= 30:
    n_q = int(freq["n"].min())
    wide = freq.copy()
    fig = charts.stacked_hbar(wide, [charts.SEQ_BLUES[3], charts.SEQ_BLUES[1], charts.SEQ_BLUES[0]],
                              "Parmi ceux qui s'en servent, l'usage est le plus souvent quotidien",
                              components.footer_text(f, 2026, n_q),
                              subtitle="Fréquence déclarée, parmi les répondants qui ont renseigné chaque famille d'outils.",
                              wrap=40)
    components.show_figure(fig, f, 2026, n_q, n_pop, "L'effectif affiché sous chaque ligne est propre à la famille d'outils.")
    components.data_view(freq, "adoption_frequence_par_famille")
else:
    st.warning("Pas assez de répondants (30 minimum par famille d'outils) pour dessiner les fréquences avec ces filtres.")

# --- 3. Combien d'outils ? -------------------------------------------------------------------------
st.header("Combien d'outils distincts ?")
cnt = ax.tool_count_distribution(pop)
n_c = int(cnt["n"].iloc[0]) if not cnt.empty else 0
components.guard_min_n(n_c, "la question sur le nombre d'outils")
multi = float(cnt.loc[cnt["category"].isin(["3", "4", "5 et +"]), "share"].sum())
fig = charts.hbar_shares(cnt, "category", f"{message.pct(multi)} des répondants utilisent au moins 3 outils d'IA par semaine",
                         components.footer_text(f, 2026, n_c),
                         subtitle="Nombre d'outils d'IA distincts utilisés dans une semaine type (saisie libre ; valeurs > 50 écartées).",
                         xlim=(0, 0.6), xlabel="Part des répondants")
components.show_figure(fig, f, 2026, n_c, n_pop)
components.data_view(cnt, "adoption_nombre_outils")
st.info("Pas de comparaison avec 2025 sur cet axe : la question d'usage a changé de forme "
        "(fréquence en 2025, types d'outils en 2026). Voir HARMONISATION.md.")
