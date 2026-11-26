import pytest

from devia.axes import adoption


def test_frequency_rows_sum_to_one(d26):
    t = adoption.frequency_by_family(d26)
    assert t.iloc[0, :3].sum() == pytest.approx(1.0)


def test_adoption_by_experience_has_ordered_bands(d26):
    t = adoption.adoption_by(d26, "Ancienneté professionnelle", min_n=1)
    assert list(t["group"]) == sorted(t["group"], key=lambda g: ["0-2 ans", "3-5 ans", "6-10 ans", "11-20 ans", "21 ans et +"].index(g))


def test_tool_families_excludes_non_users(d26):
    t = adoption.tool_families(d26)
    assert not any("n'utilis" in o.lower() for o in t["option"]) and (t["share"] <= 1).all()
