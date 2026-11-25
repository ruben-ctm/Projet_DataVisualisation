"""Indicateurs partagés (tableau de bord + axes 1 et 2)."""
import pytest

from devia import indicators
from devia.labels import TRUST


def test_overall_adoption_matches_manual(d26):
    pop = d26[d26.is_pro_dev]
    manual = 1 - pop["AISelect"].dropna().str.startswith("I don").mean()
    assert indicators.overall_adoption(pop)["share"] == pytest.approx(manual)


def test_trust_excludes_not_sure(d26):
    t = indicators.trust_distribution(d26)
    assert t["n"].iloc[0] == d26["AITrust"].isin(list(TRUST)).sum()


def test_headline_has_both_years_when_given(d26):
    h = indicators.headline(d26, d26)
    assert {"capability_2025", "capability_2026", "verify", "high"} <= set(h)
    assert h["capability_2026"]["n"] == d26["capability_positive"].notna().sum()


def test_headline_without_2025_has_no_2025_keys(d26):
    assert "capability_2025" not in indicators.headline(d26, None)


def test_diff_points_sign_and_interval():
    a = {"share": 0.30, "n": 1000}; b = {"share": 0.60, "n": 1000}
    d, lo, hi = indicators.diff_points(a, b)
    assert d == pytest.approx(0.30) and lo < d < hi and lo > 0.2
