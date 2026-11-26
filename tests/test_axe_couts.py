import pytest

from devia.axes import couts


def test_usefulness_ignores_not_applicable(d26):
    t = couts.usefulness_by_task(d26)
    s = d26["AIImpact_2"].dropna()
    assert t.set_index("task").loc["Implémentation", "n"] == (s != "Not applicable").sum()


def test_disruption_denominator_is_respondents(d26):
    t = couts.disruption_shares(d26).set_index("option")
    assert t.loc["Contexte manquant", "share"] == pytest.approx(1.0)  # cité par tous dans la fixture


def test_net_is_positive_minus_negative(d26):
    t = couts.satisfaction_by_task(d26)
    assert t["net"].to_numpy() == pytest.approx((t["share_pos"] - t["share_neg"]).to_numpy())
