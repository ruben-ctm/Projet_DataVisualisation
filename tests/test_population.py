from devia import population as p
from devia.labels import EXP_BANDS


def test_default_filters_keep_only_pro_devs(d26):
    out = p.apply_filters(d26, p.Filters())
    assert out["is_pro_dev"].all() and 0 < len(out) < len(d26)


def test_all_scope_keeps_everyone(d26):
    assert len(p.apply_filters(d26, p.Filters(scope="all"))) == len(d26)


def test_country_and_experience_filters(d26):
    f = p.Filters(scope="all", countries=("France",), exp_range=(EXP_BANDS[0], EXP_BANDS[1]))
    out = p.apply_filters(d26, f)
    assert (out["country_label"] == "France").all() and out["exp_band"].isin(EXP_BANDS[:2]).all()


def test_empty_filter_removes_nobody(d26):
    assert len(p.apply_filters(d26, p.Filters(scope="all", countries=(), org_sizes=()))) == len(d26)


def test_caption_states_who_year_and_n():
    txt = p.caption(p.Filters(countries=("France",)), 2026, 339, 545)
    for needle in ("France", "2026", "n = 339", "545", "volontaires"):
        assert needle in txt


def test_describe_is_neutral_wording():
    assert "développeurs professionnels" in p.describe(p.Filters(), 2025)
