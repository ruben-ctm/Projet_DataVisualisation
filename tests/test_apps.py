"""Tests d'interface : chaque page s'exécute sans exception sur les vraies données (ignorés si data/ est absent)."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from devia.download import is_ready

ROOT = Path(__file__).resolve().parent.parent
_ALL = ["app.py", "dashboard.py", "pages/1_Adoption.py", "pages/2_Confiance.py", "pages/3_Agents_de_code.py",
        "pages/4_Couts_caches.py", "pages/5_Organisation.py"]
PAGES = [p for p in _ALL if (ROOT / p).exists()]  # les axes arrivent branche par branche
pytestmark = pytest.mark.skipif(not is_ready(2026), reason="données 2026 absentes (uv run python get_data.py)")


@pytest.mark.parametrize("page", PAGES)
def test_page_runs_without_exception(page):
    at = AppTest.from_file(str(ROOT / page), default_timeout=120).run()
    assert not at.exception, [e.value for e in at.exception]
    assert not at.error, [e.value for e in at.error]


def _run(page, **widgets):
    at = AppTest.from_file(str(ROOT / page), default_timeout=120).run()
    for key, value in widgets.items():
        getattr(at, "multiselect" if isinstance(value, list) else "select_slider")(key=key).set_value(value)
    return at.run()


@pytest.mark.parametrize("page", PAGES)
def test_france_filter_runs_on_every_page(page):
    at = _run(page, flt_countries_0=["France"])
    assert not at.exception, [e.value for e in at.exception]


@pytest.mark.parametrize("page", [p for p in PAGES if p.startswith("pages/")])
def test_tiny_selection_says_so_instead_of_drawing(page):
    """France + indépendants + 0-2 ans : trop peu de répondants -> avertissement, aucune exception."""
    at = AppTest.from_file(str(ROOT / page), default_timeout=120).run()
    at.multiselect(key="flt_countries_0").set_value(["France"])
    at.multiselect(key="flt_org_0").set_value(["Indépendant"])
    at.select_slider(key="flt_exp_0").set_range("0-2 ans", "0-2 ans")
    at.run()
    assert not at.exception, [e.value for e in at.exception]
    assert at.warning, "un avertissement d'effectif insuffisant est attendu"


def test_reset_button_restores_defaults():
    at = AppTest.from_file(str(ROOT / "dashboard.py"), default_timeout=120).run()
    at.multiselect(key="flt_countries_0").set_value(["France"]).run()
    assert at.session_state["filters"].countries == ("France",)
    at.button[0].click().run()
    assert at.session_state["filters"].countries == ()
