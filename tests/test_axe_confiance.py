import pytest

from devia.axes import confiance


def test_positive_capability_by_keeps_groups_present_both_years(d26):
    t = confiance.positive_capability_by(d26, d26, "exp_band", min_n=1)
    assert {"share_2025", "share_2026"} <= set(t.columns)
    assert (t["share_2025"] == t["share_2026"]).all()  # mêmes données des deux côtés


def test_compare_sentiment_covers_three_classes(d26):
    t = confiance.compare_sentiment(d26, d26)
    assert list(t["category"]) == ["Favorable", "Neutre", "Défavorable"]
    assert t["share_2026"].sum() == pytest.approx(1.0)


def test_trust_by_group_drops_tiny_groups(d26):
    t = confiance.trust_by(d26, "Ancienneté professionnelle")
    assert (t["n"] >= 30).all()
