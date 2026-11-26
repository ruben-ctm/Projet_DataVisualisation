"""Le brief d'une page : structure, longueur, et traçabilité de chaque chiffre vers `docs/preuves.csv`."""
import re
import sys
from pathlib import Path

import pandas as pd
import pytest

from devia.download import is_ready

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BRIEF = DOCS / "04_BRIEF.md"
pytestmark = pytest.mark.skipif(not BRIEF.exists(), reason="docs/ absent")

SECTIONS = ["Ce que nous savons", "Ce que nous ne savons pas", "Ce que nous recommandons", "Figures", "Source et méthode"]


def _norm(s: str) -> str:
    return s.replace(" ", " ")


def _words(text: str) -> int:
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"<!--.*?-->", "", text)
    return len(re.findall(r"\w[\w'’]*", text))


def test_brief_has_the_one_pager_structure():
    t = BRIEF.read_text(encoding="utf-8")
    assert t.startswith("# "), "le titre est une affirmation"
    assert "**En une phrase.**" in t
    assert "Niveau de confiance" in t
    for s in SECTIONS:
        assert f"## {s}" in t, s


def test_brief_length_is_250_to_400_words():
    assert 250 <= _words(BRIEF.read_text(encoding="utf-8")) <= 400


def test_brief_has_three_figures_that_exist():
    t = BRIEF.read_text(encoding="utf-8")
    figs = re.findall(r"!\[(.*?)\]\((.+?)\)", t)
    assert len(figs) == 3
    for caption, rel in figs:
        assert (DOCS / rel).exists(), rel
        assert "Source" in caption, "chaque figure porte sa source"


def test_brief_names_a_limit_and_how_to_verify():
    t = BRIEF.read_text(encoding="utf-8").lower()
    assert "ne savons pas" in t and "volontaires" in t
    assert "si l'écart est faible, la recommandation tombe" in t


def test_every_number_in_the_brief_comes_from_preuves():
    """Chaque ligne annotée `<!-- P02 P03 -->` doit contenir la valeur arrondie de chacune de ces preuves."""
    pre = pd.read_csv(DOCS / "preuves.csv").set_index("id")
    cited = set()
    for line in BRIEF.read_text(encoding="utf-8").splitlines():
        m = re.search(r"<!--\s*((?:P\d+\s*)+)-->", line)
        if not m:
            continue
        body = _norm(line)
        for pid in m.group(1).split():
            assert pid in pre.index, pid
            assert _norm(pre.loc[pid, "texte"]) in body, f"{pid} ({pre.loc[pid, 'texte']}) absent de : {line[:80]}"
            cited.add(pid)
    assert cited == set(pre.index), f"preuves non citées dans le brief : {set(pre.index) - cited}"


def test_every_percentage_in_the_brief_is_backed_by_a_proof():
    """Aucun pourcentage ne figure dans le brief sans être une valeur de preuves.csv (seul « 95 % » : niveau des intervalles)."""
    known = {_norm(x) for x in pd.read_csv(DOCS / "preuves.csv")["texte"]} | {"95 %"}
    t = re.sub(r"!\[.*?\]\(.*?\)", "", BRIEF.read_text(encoding="utf-8"))
    for pct in re.findall(r"\d+\s?%", _norm(t)):
        assert pct in known, pct


@pytest.mark.skipif(not is_ready(2026) or not is_ready(2025), reason="données absentes")
def test_preuves_csv_is_what_the_code_computes():
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_brief

    fresh, _ = build_brief.build()
    saved = pd.read_csv(DOCS / "preuves.csv")
    assert list(fresh["id"]) == list(saved["id"])
    assert fresh["n"].tolist() == saved["n"].tolist()
    assert fresh["valeur"].round(4).tolist() == saved["valeur"].round(4).tolist()
    assert [_norm(x) for x in fresh["texte"]] == [_norm(x) for x in saved["texte"]]
