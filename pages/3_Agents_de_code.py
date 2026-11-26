"""Axe 3 - Agents de code et outils (Edwin DREAN-AVRILLON) : quels assistants / agents, quels fournisseurs de modèles."""
import streamlit as st

from devia import message
from devia.axes import agents as ax
from devia.ui import charts, components, state

d26, d25, f, pop, _ = state.setup("Agents de code", "🛠️")
n_pop = len(pop)
components.header("Axe 3 · Assistants et agents de code",
                  "Quels outils les développeurs utilisent-ils déjà, lesquels veulent-ils garder, et lesquels progressent ?",
                  "Edwin DREAN-AVRILLON")
components.guard_min_n(n_pop, "cette population")

tbl_all = ax.tool_table(pop)
components.guard_min_n(int(tbl_all["n_have"].iloc[0]) if not tbl_all.empty else 0, "la question sur les assistants de code")
n_have = int(tbl_all["n_have"].iloc[0])

top = st.slider("Nombre d'outils affichés", 5, 20, 10, key="a3_top",
                help="Les outils les plus utilisés. Un outil doit avoir au moins 30 utilisateurs parmi les répondants pour apparaître.")
tbl = tbl_all.head(top)

# --- 1. Utilisation ---------------------------------------------------------------------------------
st.header("Quels outils sont utilisés ?")
fig = charts.hbar_shares(tbl.rename(columns={"k_used": "k"}), "tool",
                         f"{tbl['tool'].iloc[0]} est l'outil le plus cité : {message.pct(tbl['share_used'].iloc[0])} des répondants l'ont utilisé",
                         components.footer_text(f, 2026, n_have), value="share_used", lo="lo", hi="hi", n="k",
                         subtitle="Utilisé au cours de l'année passée (choix multiple). Effectif entre parenthèses = nombre d'utilisateurs.",
                         xlim=(0, 1.0), highlight=[tbl["tool"].iloc[0]])
components.show_figure(fig, f, 2026, n_have, n_pop)
components.data_view(tbl, "agents_outils")

# --- 2. Souhait pour les 6 prochains mois ----------------------------------------------------------------
st.header("Lesquels veut-on garder ou adopter ?")
n_want = int(tbl["n_want"].iloc[0])
if n_want >= 30:
    fig = charts.dumbbell(tbl["tool"], tbl["share_used"], tbl["share_want"],
                          "Utilisé l'an passé → souhaité pour les 6 prochains mois",
                          components.footer_text(f, 2026, n_have) + f" Souhait : n = {n_want:,} répondants.".replace(",", " "),
                          a_name="A utilisé (année passée)", b_name="Veut utiliser (6 mois)",
                          subtitle="Chaque part est rapportée à ses propres répondants ; une case vide peut signifier « aucun » ou « pas de réponse ».")
    components.show_figure(fig, f, 2026, n_have, n_pop,
                           "Deux bases différentes : répondants à la question « utilisé », puis à la question « souhaité ».")
else:
    st.warning("Pas assez de répondants à la question « souhaité » avec ces filtres.")

st.header("Les utilisateurs d'un outil le gardent-ils ?")
adm = tbl[tbl["k_used_both"] >= 30].sort_values("admiration", ascending=False)
best = adm.iloc[0]
fig = charts.hbar_shares(adm.assign(k=adm["k_used_both"]), "tool",
                         f"Taux d'admiration : {best['tool']} en tête avec {message.pct(best['admiration'])}",
                         components.footer_text(f, 2026, n_have), value="admiration", lo="adm_lo", hi="adm_hi", n="k_used_both",
                         subtitle="Parmi les utilisateurs de l'outil ayant répondu aussi à la question « souhait » : part qui veulent encore l'utiliser dans les 6 mois.",
                         xlim=(0, 1.0))
components.show_figure(fig, f, 2026, n_have, n_pop, "Effectif entre parenthèses = utilisateurs de l'outil qui ont répondu aux deux questions.")

# --- 3. Fournisseurs et combinaison ------------------------------------------------------------------------
st.header("Fournisseurs de modèles et multi-outils")
c1, c2 = st.columns(2)
prov = ax.providers(pop)
if not prov.empty and int(prov["n"].iloc[0]) >= 30:
    with c1:
        n_p = int(prov["n"].iloc[0])
        fig = charts.hbar_shares(prov, "option", "Fournisseurs de modèles utilisés", components.footer_text(f, 2026, n_p),
                                 xlim=(0, 1.0), subtitle="Choix multiple, année passée.")
        components.show_figure(fig, f, 2026, n_p, n_pop)
tpp = ax.tools_per_person(pop)
if not tpp.empty and int(tpp["n"].iloc[0]) >= 30:
    with c2:
        n_t = int(tpp["n"].iloc[0])
        multi = float(tpp.loc[tpp["category"].isin(["2", "3", "4 et +"]), "share"].sum())
        fig = charts.hbar_shares(tpp, "category", f"{message.pct(multi)} ont utilisé au moins 2 outils de code",
                                 components.footer_text(f, 2026, n_t), xlim=(0, 0.6),
                                 subtitle="Nombre d'assistants / agents de code différents.")
        components.show_figure(fig, f, 2026, n_t, n_pop)

# --- 4. Un outil au choix selon le profil -----------------------------------------------------------------
st.header("Qui utilise quel outil ?")
c1, c2 = st.columns(2)
tool = c1.selectbox("Outil", list(tbl_all["tool"].head(15)), index=0, key="a3_tool")
by = c2.selectbox("Regrouper par", list(ax.GROUPINGS), index=0, key="a3_by")
t = ax.tool_share_by(pop, tool, by)
if t.empty:
    st.warning("Aucun groupe n'atteint 30 répondants avec ces filtres.")
else:
    n_g = int(t["n"].sum())
    fig = charts.hbar_shares(t, "group", f"Part des répondants ayant utilisé {tool}, selon le groupe",
                             components.footer_text(f, 2026, n_g), xlim=(0, 1.0), subtitle=f"Groupe : {by.lower()}.")
    components.show_figure(fig, f, 2026, n_g, n_pop)
    components.data_view(t, "agents_outil_par_profil")
    components.dropped_note(t.attrs.get("dropped", []))
st.info("Pas de comparaison avec 2025 sur cet axe : les listes d'outils et les formulations ont changé. Voir HARMONISATION.md.")
