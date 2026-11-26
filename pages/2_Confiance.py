"""Axe 2 - Confiance et vérification (Antoine REVERSAT) : confiance accordée à l'IA, capacité perçue, 2025 ↔ 2026."""
import streamlit as st

from devia import message
from devia.axes import confiance as ax
from devia.config import MIN_GROUP_N
from devia.ui import charts, components, state

d26, d25, f, pop, pop25 = state.setup("Confiance", "🔍")
n_pop = len(pop)
components.header("Axe 2 · Confiance et vérification",
                  "Les développeurs font-ils confiance à l'IA, pour quelles tâches, et cela a-t-il changé depuis 2025 ?",
                  "Antoine REVERSAT")
components.guard_min_n(n_pop, "cette population")

# --- 1. Confiance selon un groupe ---------------------------------------------------------------------
st.header("Quelle confiance, selon le profil ?")
by = st.selectbox("Regrouper par", list(ax.GROUPINGS), index=0, key="a2_by",
                  help="« Capacité perçue » croise la confiance avec le jugement porté sur les tâches complexes.")
tbl = ax.trust_by(pop, by)
if tbl.empty:
    st.warning("Aucun groupe n'atteint 30 répondants avec ces filtres : rien n'est dessiné.")
else:
    n_fig = int(tbl["n"].sum())
    colors = [charts.SEQ_BLUES[0], charts.SEQ_BLUES[1], charts.SEQ_BLUES[2], charts.SEQ_BLUES[4], charts.GRAY]
    first = tbl.iloc[:, 0]
    fig = charts.stacked_hbar(
        tbl, colors,
        f"Part « confiance seulement si je peux vérifier » : de {message.pct(first.min())} à {message.pct(first.max())} selon le groupe",
        components.footer_text(f, 2026, n_fig), subtitle=f"Groupe : {by.lower()}. Une seule réponse par personne.", wrap=34)
    components.show_figure(fig, f, 2026, n_fig, n_pop)
    components.data_view(tbl, "confiance_par_groupe")
    components.dropped_note(tbl.attrs.get("dropped", []))

# --- 2. Capacité perçue -----------------------------------------------------------------------------
st.header("Comment l'IA est-elle jugée sur les tâches complexes ?")
cap = ax.capability_distribution(pop)
n_c = int(cap["n"].iloc[0])
components.guard_min_n(n_c, "la question sur la capacité perçue")
fig = charts.hbar_shares(cap, "category", f"{message.pct(float(cap['share'].iloc[3:].sum()))} des répondants jugent l'IA bonne ou très bonne sur les tâches complexes",
                         components.footer_text(f, 2026, n_c), subtitle="Répondants ayant un avis ; « je ne sais pas / pas d'usage » exclu.",
                         highlight=list(cap["category"].iloc[3:]), xlim=(0, 0.7))
components.show_figure(fig, f, 2026, n_c, n_pop)
components.data_view(cap, "confiance_capacite_percue")

# --- 3. Comparaison 2025 ↔ 2026 -----------------------------------------------------------------------------
st.header("Qu'est-ce qui a changé depuis 2025 ?")
if pop25 is None:
    st.info("Les données 2025 ne sont pas chargées (lancer `uv run python get_data.py`) : comparaison indisponible.")
    st.stop()
st.caption("Seules deux questions sont identiques entre les deux années : attitude générale et capacité sur tâches complexes. "
           "Voir HARMONISATION.md pour les correspondances et les limites.")
tab_sent, tab_group = st.tabs(["Attitude générale", "Capacité positive selon le profil"])
with tab_sent:
    s = ax.compare_sentiment(pop, pop25)
    n26, n25 = int(s["n_2026"].iloc[0]), int(s["n_2025"].iloc[0])
    if min(n26, n25) < 30:
        st.warning(f"Effectif insuffisant (2026 : {n26}, 2025 : {n25}) pour comparer l'attitude générale.")
    else:
        fav26, fav25 = s.loc[0, "share_2026"], s.loc[0, "share_2025"]
        fig = charts.paired_bars(
            s["category"], s["share_2025"], s["share_2026"],
            f"Attitude envers l'IA : {message.pct(fav25)} de favorables en 2025, {message.pct(fav26)} en 2026",
            components.footer_text(f, 2026, n26) + f" Référence 2025 : n = {n25:,}.".replace(",", " "),
            a_ci=(s["lo_2025"], s["hi_2025"]), b_ci=(s["lo_2026"], s["hi_2026"]), a_n=s["n_2025"], b_n=s["n_2026"],
            subtitle="Échelles à 5 niveaux ramenées à 3 classes ; « je ne sais pas » exclu.")
        components.show_figure(fig, f, 2026, n26, n_pop, "Harmonisation 3 classes : voir HARMONISATION.md.")
        components.data_view(s, "attitude_2025_2026")
        h = ax.headline(pop, pop25)
        d, lo, hi = ax.diff_points(h["sentiment_2025"], h["sentiment_2026"])
        st.markdown(f"Écart de part de favorables : **{100 * d:+.1f} points** (intervalle approché à 95 % : "
                    f"{100 * lo:+.1f} à {100 * hi:+.1f}).")
with tab_group:
    st.caption("Seule l'ancienneté professionnelle existe sous la même forme dans les deux années : les autres profils ne sont pas comparés.")
    g = ax.positive_capability_by(pop, pop25, "exp_band")
    if g.empty:
        st.warning("Aucun groupe n'atteint 30 répondants les deux années avec ces filtres.")
    else:
        n26 = int(g["n_2026"].sum())
        fig = charts.paired_bars(
            g["group"], g["share_2025"], g["share_2026"],
            "La part d'avis positifs sur les tâches complexes progresse dans toutes les tranches d'ancienneté affichées"
            if (g["share_2026"] > g["share_2025"]).all() else "Évolution de la part d'avis positifs selon l'ancienneté",
            components.footer_text(f, 2026, n26),
            a_ci=(g["lo_2025"], g["hi_2025"]), b_ci=(g["lo_2026"], g["hi_2026"]), a_n=g["n_2025"], b_n=g["n_2026"],
            subtitle="« Bonne » ou « très bonne » parmi les répondants ayant un avis. Groupes d'au moins 30 répondants chaque année.")
        components.show_figure(fig, f, 2026, n26, n_pop)
        components.data_view(g, "capacite_positive_par_anciennete")
