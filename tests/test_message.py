from devia import message
from devia.population import Filters


def _h(n=500):
    s = lambda v: {"n": n, "k": int(n * v), "share": v, "lo": v - .02, "hi": v + .02}
    return {"capability_2026": s(.6), "capability_2025": s(.34), "verify": s(.48), "high": s(.07),
            "sentiment_2026": s(.64), "sentiment_2025": s(.63)}


def test_headline_with_comparison():
    t = message.headline(_h(), Filters())
    assert "34 %" in t and "60 %" in t and "48 %" in t


def test_headline_refuses_to_claim_with_tiny_sample():
    assert "trop faible" in message.headline(_h(n=10), Filters())


def test_headline_without_2025_does_not_mention_change():
    h = _h(); h.pop("capability_2025")
    t = message.headline(h, Filters())
    assert "passe de" not in t and "indisponible" in t


def test_subject_names_the_country():
    assert "France" in message.who(Filters(countries=("France",)))
