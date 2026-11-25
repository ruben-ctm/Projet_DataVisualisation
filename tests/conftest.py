"""Données synthétiques minimales : les tests unitaires n'ont pas besoin des CSV."""
import numpy as np
import pandas as pd
import pytest

from devia import data


@pytest.fixture(scope="session")
def raw26() -> pd.DataFrame:
    """200 répondants 2026 avec toutes les colonnes lues par `devia.data` (valeurs construites à la main)."""
    from devia.config import COLS_2026
    rng = np.random.default_rng(0)
    n = 200
    df = pd.DataFrame({c: [np.nan] * n for c in COLS_2026})
    df["ResponseId"] = range(n)
    df["Age"] = rng.choice(["18-24 years old", "25-34 years old", "35-44 years old"], n)
    df["Employment"] = rng.choice(["Employed", "Student"], n, p=[0.8, 0.2])
    df["CodeMain"] = rng.choice(["I create code as a primary part of my job", "I do not create code"], n, p=[0.9, 0.1])
    df["Role"] = "Developer, full-stack"
    df["WorkExp"] = rng.integers(0, 30, n).astype(str)
    df["Country"] = rng.choice(["France", "Germany", "United States of America"], n)
    df["OrgSize"] = rng.choice(["20 to 99 employees", "10,000 or more employees"], n)
    df["JobSat"] = rng.integers(0, 11, n).astype(float)
    df["AISelect"] = rng.choice(["General-purpose AI chat tools", "AI coding assistants or coding agents;General-purpose AI chat tools",
                                 "I don’t use AI tools"], n, p=[0.3, 0.5, 0.2])
    df["AIFreq_1"] = rng.choice(["Daily", "Weekly", "Monthly or Infrequent"], n)
    df["AISentiment"] = rng.choice(["Very favorable", "Somewhat favorable", "Neutral", "Somewhat unfavorable", "Not sure"], n)
    df["AIComplex"] = rng.choice(["Very well at handling complex tasks", "Good, but not great at handling complex tasks",
                                  "Bad at handling complex tasks", "I don't use AI tools for complex tasks / I don't know"], n)
    df["AITrust"] = rng.choice(["I trust it when I can easily verify the output", "I do not trust it for most work tasks",
                                "Not sure / I do not use AI tools"], n)
    df["Disruption"] = rng.choice(["Plausible but wrong code;Missing context", "Missing context"], n)
    df["AICodeAgentHaveWorkedWith"] = rng.choice(["Claude Code;GitHub Copilot", "GitHub Copilot", "Cursor"], n)
    df["AICodeAgentWantToUseNext6Months"] = rng.choice(["Claude Code", "GitHub Copilot", np.nan], n)
    df["AICodeAgentAdmired"] = np.nan
    for i in range(1, 8):
        df[f"AIImpact_{i}"] = rng.choice(["Very useful", "Useful", "Not applicable", "More impractical than useful, not useful"], n)
        df[f"AISat_{i}"] = rng.choice(["Greatly improved", "No change", "Somewhat decreased"], n)
    return df


@pytest.fixture(scope="session")
def d26(raw26) -> pd.DataFrame:
    return data.prepare_2026(raw26)
