import pytest

from devia.axes import organisation


def test_satisfied_threshold_is_eight(d26):
    flag = organisation.satisfied_flag(d26)
    assert flag.equals((d26["job_sat"] >= 8).astype(float).where(d26["job_sat"].notna()))


def test_jobsat_groups_are_labelled(d26):
    t = organisation.jobsat_by_ai_intensity(d26)
    assert set(t["group"]) <= {"Usage quotidien de l'IA", "Pas d'usage quotidien"}


def test_learning_flag_counts_any_yes(d26):
    d = d26.copy()
    d["LearnAI"] = ["Yes, on my own", "No"] * (len(d) // 2)
    t = organisation.learning_by(d, "Ancienneté professionnelle", min_n=1)
    assert ((t["share"] >= 0) & (t["share"] <= 1)).all()
