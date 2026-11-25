import math

import pandas as pd
import pytest

from devia import stats


def test_wilson_known_value():
    lo, hi = stats.wilson_ci(50, 100)
    assert lo == pytest.approx(0.4038, abs=1e-3) and hi == pytest.approx(0.5962, abs=1e-3)


def test_wilson_edges_and_empty():
    lo, hi = stats.wilson_ci(0, 10)
    assert lo == 0.0 and hi > 0
    assert math.isnan(stats.wilson_ci(0, 0)[0])


def test_share_ignores_missing():
    r = stats.share(pd.Series([1.0, 0.0, 1.0, float("nan")]))
    assert (r["n"], r["k"]) == (3, 2) and r["share"] == pytest.approx(2 / 3)


def test_enough_threshold():
    assert stats.enough(30) and not stats.enough(29)


def test_multi_share_denominator_is_respondents_not_mentions():
    s = pd.Series(["A;B", "A", None, "B;C"])
    t = stats.multi_share(s).set_index("option")
    assert t.loc["A", "n"] == 3 and t.loc["A", "share"] == pytest.approx(2 / 3)  # 2 citations / 3 répondants
    assert t["share"].sum() > 1  # choix multiple : somme > 100 %


def test_multi_share_labels_and_exclude():
    t = stats.multi_share(pd.Series(["A;B", "A"]), labels={"A": "Alpha"}, exclude=("B",))
    assert list(t["option"]) == ["Alpha"]


def test_shares_by_group_drops_small_groups_and_reports_them():
    df = pd.DataFrame({"g": ["a"] * 40 + ["b"] * 5, "flag": [1.0] * 20 + [0.0] * 20 + [1.0] * 5})
    t = stats.shares_by_group(df, "flag", "g", min_n=30)
    assert list(t["group"]) == ["a"] and t.loc[0, "share"] == 0.5
    assert t.attrs["dropped"] == [("b", 5)]


def test_group_order_follows_categories():
    df = pd.DataFrame({"g": pd.Categorical(["z", "a"], categories=["z", "a"], ordered=True)})
    assert stats.group_order(df, "g") == ["z", "a"]


def test_distribution_by_group_sums_to_one():
    df = pd.DataFrame({"g": ["a"] * 40, "c": ["x"] * 10 + ["y"] * 30})
    t = stats.distribution_by_group(df, "c", "g", ["x", "y"], min_n=30)
    assert t.loc["a", ["x", "y"]].sum() == pytest.approx(1.0) and t.loc["a", "n"] == 40


def test_contains_flag_keeps_nan_for_unanswered():
    f = stats.contains_flag(pd.Series(["A;B", "C", None]), "A")
    assert f.iloc[0] == 1.0 and f.iloc[1] == 0.0 and math.isnan(f.iloc[2])
