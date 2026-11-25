import pandas as pd

from devia import harmonisation as h


def test_sentiment_maps_both_years_to_three_classes_and_drops_unsure():
    s26 = pd.Series(["Very favorable", "Somewhat favorable", "Neutral", "Somewhat unfavorable", "Very unfavorable", "Not sure"])
    s25 = pd.Series(["Very favorable", "Favorable", "Indifferent", "Unfavorable", "Very unfavorable", "Unsure"])
    a, b = pd.Series(h.sentiment3(s26, 2026)), pd.Series(h.sentiment3(s25, 2025))
    assert list(a.dropna()) == list(b.dropna()) == ["Favorable", "Favorable", "Neutre", "Défavorable", "Défavorable"]
    assert a.isna().iloc[-1] and b.isna().iloc[-1]


def test_capability_excludes_dont_know_and_counts_positive():
    s = pd.Series(["Very well at handling complex tasks", "Good, but not great at handling complex tasks",
                   "Bad at handling complex tasks", "I don't use AI tools for complex tasks / I don't know"])
    cap = h.capability5(s)
    pos = h.capability_positive(pd.Series(cap))
    assert list(pos.dropna()) == [1.0, 1.0, 0.0] and pos.isna().iloc[-1]


def test_pro_dev_definitions_require_working_status():
    d26 = pd.DataFrame({"CodeMain": [h.PRO_2026] * 2, "Employment": ["Employed", "Student"]})
    d25 = pd.DataFrame({"MainBranch": [h.PRO_2025] * 2, "Employment": ["Employed", "Retired"]})
    assert list(h.is_pro_dev_2026(d26)) == [True, False]
    assert list(h.is_pro_dev_2025(d25)) == [True, False]
