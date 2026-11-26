"""Texte du message du tableau de bord : construit à partir des chiffres de la sélection courante.

Règle (chapitre V) : un titre n'affirme que ce que la sélection permet. Si l'effectif est trop faible
ou si la comparaison 2025 n'est pas possible, la phrase se réduit à ce qui reste vrai.
"""
from __future__ import annotations

from .config import MIN_N
from .population import Filters


def who(f: Filters) -> str:
    """Sujet de la phrase : « les développeurs professionnels répondants (France) »."""
    base = "les développeurs professionnels répondants" if f.scope == "pro" else "les répondants"
    if f.countries:
        base += f" ({', '.join(f.countries)})" if len(f.countries) <= 2 else f" ({len(f.countries)} pays)"
    return base


def pct(x: float) -> str:
    return f"{100 * x:.0f} %"


def _ok(d: dict | None) -> bool:
    return d is not None and d.get("n", 0) >= MIN_N


def headline(h: dict, f: Filters) -> str:
    """Titre du tableau de bord principal."""
    cap26, cap25 = h.get("capability_2026"), h.get("capability_2025")
    verify = h.get("verify")
    if _ok(cap26) and _ok(cap25) and _ok(verify):
        return (f"Parmi {who(f)}, la part qui juge l'IA bonne sur les tâches complexes passe de "
                f"{pct(cap25['share'])} (2025) à {pct(cap26['share'])} (2026), mais {pct(verify['share'])} "
                "ne lui font confiance que s'ils peuvent vérifier le résultat.")
    if _ok(cap26) and _ok(verify):
        return (f"Parmi {who(f)}, {pct(cap26['share'])} jugent l'IA bonne sur les tâches complexes "
                f"et {pct(verify['share'])} ne lui font confiance que s'ils peuvent vérifier le résultat "
                "(comparaison 2025 indisponible pour cette sélection).")
    return "Effectif trop faible avec ces filtres pour énoncer un constat : élargissez la sélection."


def takeaways(h: dict, f: Filters, adoption: dict | None) -> list[str]:
    """Trois à quatre phrases de lecture, chacune réservée aux chiffres que la sélection autorise."""
    out = []
    if _ok(adoption):
        out.append(f"**L'adoption n'est plus le sujet.** {pct(adoption['share'])} de {who(f)} qui ont répondu "
                   "utilisent des outils d'IA dans leur travail.")
    if _ok(h.get("sentiment_2026")) and _ok(h.get("sentiment_2025")):
        out.append(f"**Le sentiment général est stable.** {pct(h['sentiment_2025']['share'])} de favorables en 2025, "
                   f"{pct(h['sentiment_2026']['share'])} en 2026 : l'IA ne convainc pas plus, elle est jugée plus capable.")
    if _ok(h.get("high")):
        out.append(f"**La confiance reste conditionnelle.** Seuls {pct(h['high']['share'])} lui font confiance, "
                   "décisions importantes comprises.")
    return out
