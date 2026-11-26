"""Axe 4 - Coûts cachés (Arthur REYNAUD) : erreurs de l'IA, freins, utilité et satisfaction par tâche."""
import streamlit as st

from devia import message
from devia.axes import couts as ax
from devia.labels import DISRUPTION
from devia.ui import charts, components, state

d26, d25, f, pop, _ = state.setup("Coûts cachés", "⚠️")
n_pop = len(pop)
components.header("Axe 4 · Coûts cachés de l'IA",
                  "Où l'IA fait-elle perdre du temps, qui l'évite et pourquoi, et pour quelles tâches aide-t-elle vraiment ?",
                  "Arthur REYNAUD")
components.guard_min_n(n_pop, "cette population")

# --- 1. Erreurs coûteuses -------------------------------------------------------------------------------
st.header("Quelles erreurs font perdre le plus de temps ?")
dis = ax.disruption_shares(pop)
n_d = int(dis["n"].iloc[0]) if not dis.empty else 0
components.guard_min_n(n_d, "la question sur les erreurs de l'IA")
fig = charts.hbar_shares(dis, "option", f"« {dis['option'].iloc[0]} » : cité par {message.pct(dis['share'].iloc[0])} des répondants",
                         components.footer_text(f, 2026, n_d), xlim=(0, 1.0), highlight=[dis["option"].iloc[0], dis["option"].iloc[1]],
                         subtitle="Erreurs qui ont coûté le plus de temps à la personne ou à son équipe (choix multiple).", wrap=40)
components.show_figure(fig, f, 2026, n_d, n_pop)
components.data_view(dis, "couts_erreurs")

with st.expander("Une erreur donnée selon le profil"):
    c1, c2 = st.columns(2)
    option = c1.selectbox("Erreur", [v for k, v in DISRUPTION.items() if not k.startswith("Other")], key="a4_opt")
    by = c2.selectbox("Regrouper par", list(ax.GROUPINGS), key="a4_by")
    t = ax.disruption_by(pop, option, by)
    if t.empty:
        st.warning("Aucun groupe n'atteint 30 répondants avec ces filtres.")
    else:
        n_g = int(t["n"].sum())
        fig = charts.hbar_shares(t, "group", f"« {option} » selon le groupe", components.footer_text(f, 2026, n_g),
                                 xlim=(0, 1.0), subtitle=f"Groupe : {by.lower()}.")
        components.show_figure(fig, f, 2026, n_g, n_pop)

# --- 2. Freins ------------------------------------------------------------------------------------------
st.header("Pourquoi certains évitent-ils l'IA ?")
av = ax.avoid_reasons(pop)
n_a = int(av["n"].iloc[0]) if not av.empty else 0
components.guard_min_n(n_a, "la question sur l'évitement de l'IA")
share_not_avoid = float(av.loc[av["option"] == "Je n'évite pas l'IA", "share"].iloc[0])
fig = charts.hbar_shares(av, "option", f"{message.pct(1 - share_not_avoid)} des répondants évitent l'IA pour au moins une raison",
                         components.footer_text(f, 2026, n_a), xlim=(0, 0.8), highlight=[o for o in av["option"] if o != "Je n'évite pas l'IA"],
                         subtitle="Une seule raison par personne : la raison qui reflète le mieux leur position.", wrap=44)
components.show_figure(fig, f, 2026, n_a, n_pop)
components.data_view(av, "couts_raisons_evitement")

# --- 3. Utilité et satisfaction par tâche -----------------------------------------------------------------
st.header("Pour quelles tâches l'IA aide-t-elle vraiment ?")
kind = st.radio("Mesure", ["Utilité perçue", "Effet sur la satisfaction"], horizontal=True, key="a4_kind",
                help="Utilité : « utile » moins « plus gênant qu'utile » (non applicable exclu). "
                     "Satisfaction : « améliorée » moins « diminuée » après usage de l'IA.")
t = ax.usefulness_by_task(pop) if kind == "Utilité perçue" else ax.satisfaction_by_task(pop)
if t.empty or t["n"].min() < 30:
    st.warning("Pas assez de répondants (30 minimum par tâche) avec ces filtres.")
else:
    n_t = int(t["n"].min())
    worst, best = t.iloc[-1], t.iloc[0]
    fig = charts.diverging_bars(t["task"], t["net"], f"{best['task']} en tête, {worst['task'].lower()} en dernier ({kind.lower()})",
                                components.footer_text(f, 2026, n_t), ns=t["n"],
                                subtitle="Solde = part de réponses positives moins part de réponses négatives, par tâche.",
                                pos_name="positif", neg_name="négatif")
    components.show_figure(fig, f, 2026, n_t, n_pop, "Effectif affiché par tâche ; l'effectif de la légende est le plus petit.")
    components.data_view(t[["task", "n", "share_pos", "share_neg", "net"]], "couts_taches", "Voir parts positives et négatives")
st.info("Pas de comparaison avec 2025 sur cet axe : ces questions n'existent pas sous cette forme en 2025.")
