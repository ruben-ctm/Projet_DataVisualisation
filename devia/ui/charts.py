"""Graphiques matplotlib partagés par tous les axes (style, palette, pied de population).

Chaque fonction reçoit des tables déjà calculées par la logique et renvoie une
`Figure` : aucun calcul d'analyse ici, et aucun appel Streamlit.
Palette : bleu = 2026 / mise en avant, gris = 2025 / contexte, rouge = négatif,
dégradé de bleus pour les échelles ordonnées (valeurs validées avec le script de palette).
"""
from __future__ import annotations

import textwrap
from typing import Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

INK, INK2, GRID, SURFACE = "#191919", "#666666", "#e6e6e6", "#ffffff"
BLUE, ORANGE, GRAY, RED = "#257de0", "#f47230", "#9c9c9c", "#ec4647"
SEQ_BLUES = ["#cce3fd", "#84b9f3", "#338ced", "#1b64be", "#0e3d7e"]   # clair -> foncé
DIVERGING = ["#ec4647", "#f4a3a4", "#d9d9d9", "#9dc8f7", "#257de0"]    # négatif -> positif

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK, "text.color": INK, "axes.facecolor": SURFACE,
    "figure.facecolor": SURFACE, "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.axisbelow": True,
})


def _wrap(label: str, width: int = 34) -> str:
    return "\n".join(textwrap.wrap(str(label), width)) or str(label)


def _frame(fig, title: str, subtitle: str | None, footer: str) -> None:
    """Titre (à la ligne si long), sous-titre et pied de population ; réserve la place en pouces."""
    height = fig.get_size_inches()[1]
    t_lines = textwrap.wrap(title, 92) or [title]
    f_lines = textwrap.wrap(footer, 125) or [footer]
    top_in = 0.12 + 0.24 * len(t_lines)
    fig.text(0.01, 1 - 0.08 / height, "\n".join(t_lines), ha="left", va="top", fontsize=12.5,
             fontweight="bold", color=INK, linespacing=1.25)
    if subtitle:
        s_lines = textwrap.wrap(subtitle, 130)
        fig.text(0.01, 1 - (top_in + 0.04) / height, "\n".join(s_lines), ha="left", va="top", fontsize=9, color=INK2)
        top_in += 0.06 + 0.17 * len(s_lines)
    bottom_in = 0.1 + 0.15 * len(f_lines)
    fig.text(0.01, 0.06 / height, "\n".join(f_lines), ha="left", va="bottom", fontsize=7.5, color=INK2)
    fig.get_layout_engine().set(rect=(0.0, bottom_in / height, 1.0, 1 - (top_in + bottom_in) / height))


def _fig(n_rows: int, height_per_row: float = 0.46, base: float = 2.5, width: float = 9.2):
    fig, ax = plt.subplots(figsize=(width, base + height_per_row * n_rows), layout="constrained")
    return fig, ax


def _pct(x: float) -> str:
    return f"{100 * x:.0f} %"


def hbar_shares(table: pd.DataFrame, label: str, title: str, footer: str, *, subtitle: str | None = None,
                value: str = "share", lo: str | None = "lo", hi: str | None = "hi", n: str | None = "n",
                highlight: Sequence[str] = (), xlim: tuple[float, float] | None = None,
                xlabel: str = "Part des répondants", wrap: int = 34) -> plt.Figure:
    """Barres horizontales de parts avec intervalle de confiance à 95 % et effectif en bout de barre."""
    t = table.reset_index(drop=True)
    fig, ax = _fig(len(t))
    ypos = np.arange(len(t))[::-1]
    colors = [BLUE if (not highlight or str(l) in highlight) else GRAY for l in t[label]]
    ax.barh(ypos, t[value], height=0.58, color=colors, zorder=3)
    if lo and hi and lo in t and hi in t:
        ax.errorbar(t[value], ypos, xerr=[t[value] - t[lo], t[hi] - t[value]], fmt="none",
                    ecolor=INK2, elinewidth=1, capsize=2.5, zorder=4)
    show_n = bool(n and n in t and t[n].nunique() > 1)
    top = float(t[hi].max() if hi in t else t[value].max())
    pad = 0.012 * (xlim[1] if xlim else max(top, 0.01) * 1.0)
    for y, (_, r) in zip(ypos, t.iterrows()):
        x_end = r[hi] if hi in t else r[value]
        txt = _pct(r[value]) + (f"  (n = {int(r[n]):,})".replace(",", " ") if show_n else "")
        ax.text(x_end + pad, y, txt, va="center", ha="left", fontsize=8.5, color=INK, zorder=5)
    ax.set_yticks(ypos, [_wrap(l, wrap) for l in t[label]])
    ax.set_xlim(*(xlim if xlim else (0, min(1.0, top * 1.38 + 0.02))))
    ax.xaxis.set_major_formatter(lambda x, _: f"{100 * x:.0f} %")
    ax.set_xlabel(xlabel, fontsize=9)
    ax.tick_params(axis="y", length=0)
    _frame(fig, title, subtitle, footer)
    return fig


def stacked_hbar(wide: pd.DataFrame, colors: Sequence[str], title: str, footer: str, *,
                 subtitle: str | None = None, n_col: str | None = "n", xlabel: str = "Part des répondants du groupe",
                 wrap: int = 30, min_label: float = 0.06, text_dark_from: int = 99) -> plt.Figure:
    """Répartition à 100 % par groupe. `wide` : index = groupes, colonnes = modalités ordonnées, valeurs = parts."""
    cols = [c for c in wide.columns if c != n_col]
    fig, ax = _fig(len(wide), height_per_row=0.55, base=2.9)
    ypos = np.arange(len(wide))[::-1]
    left = np.zeros(len(wide))
    for i, c in enumerate(cols):
        vals = wide[c].to_numpy(dtype=float)
        ax.barh(ypos, vals, left=left, height=0.62, color=colors[i % len(colors)], edgecolor=SURFACE,
                linewidth=1.6, label=c, zorder=3)
        for y, v, l in zip(ypos, vals, left):
            if v >= min_label:
                dark_bg = colors[i % len(colors)] in (DIVERGING[0], SEQ_BLUES[2], SEQ_BLUES[3], SEQ_BLUES[4], BLUE)
                ax.text(l + v / 2, y, _pct(v), ha="center", va="center", fontsize=8,
                        color="white" if dark_bg else INK, zorder=5)
        left += vals
    labels = []
    for g in wide.index:
        lab = _wrap(g, wrap)
        if n_col and n_col in wide:
            lab += f"\n(n = {int(wide.loc[g, n_col]):,})".replace(",", " ")
        labels.append(lab)
    ax.set_yticks(ypos, labels)
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(lambda x, _: f"{100 * x:.0f} %")
    ax.set_xlabel(xlabel, fontsize=9)
    ax.tick_params(axis="y", length=0)
    ax.legend(ncol=min(len(cols), 3), loc="upper center", bbox_to_anchor=(0.5, -0.16 if len(wide) > 2 else -0.3),
              frameon=False, fontsize=8.5, handlelength=1.2)
    _frame(fig, title, subtitle, footer)
    return fig
