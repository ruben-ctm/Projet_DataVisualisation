import pytest

from devia.axes import agents


def test_admiration_uses_respondents_answering_both(d26):
    t = agents.tool_table(d26, min_users=1).set_index("tool")
    both = d26["AICodeAgentHaveWorkedWith"].notna() & d26["AICodeAgentWantToUseNext6Months"].notna()
    users = d26.loc[both, "AICodeAgentHaveWorkedWith"].str.split(";").apply(lambda x: "GitHub Copilot" in x)
    assert t.loc["GitHub Copilot", "k_used_both"] == users.sum()
    assert 0 <= t.loc["GitHub Copilot", "admiration"] <= 1


def test_tools_per_person_sums_to_one(d26):
    assert agents.tools_per_person(d26)["share"].sum() == pytest.approx(1.0)


def test_tool_share_by_returns_shares(d26):
    t = agents.tool_share_by(d26, "Cursor", "Ancienneté professionnelle", min_n=1)
    assert ((t["share"] >= 0) & (t["share"] <= 1)).all()
