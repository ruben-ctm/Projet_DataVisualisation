"""Libellés français et ordres des modalités (les données restent en anglais).

Chaque dictionnaire associe la modalité d'origine de l'enquête à son libellé
d'affichage ; l'ordre des clés est l'ordre d'affichage.
"""

TRUST = {
    "I trust it when I can easily verify the output": "Seulement si je peux vérifier facilement",
    "I trust it for low-risk work tasks only": "Tâches à faible risque seulement",
    "I trust it for many tasks, but not important work decisions": "Beaucoup de tâches, pas les décisions importantes",
    "I trust it for many tasks, including important work decisions": "Y compris les décisions importantes",
    "I do not trust it for most work tasks": "Pas de confiance pour la plupart des tâches",
}
TRUST_ORDER_NOTE = "Du plus prudent au plus confiant (hors « pas de confiance »)."

CAPABILITY = {
    "Very poor at handling complex tasks": "Très mauvaise",
    "Bad at handling complex tasks": "Mauvaise",
    "Neither good or bad at handling complex tasks": "Ni bonne ni mauvaise",
    "Good, but not great at handling complex tasks": "Bonne, sans plus",
    "Very well at handling complex tasks": "Très bonne",
}
CAPABILITY_DONT_USE = "I don't use AI tools for complex tasks / I don't know"

SENTIMENT_2026 = {
    "Very favorable": "Favorable", "Somewhat favorable": "Favorable",
    "Neutral": "Neutre",
    "Somewhat unfavorable": "Défavorable", "Very unfavorable": "Défavorable",
}
SENTIMENT_2025 = {
    "Very favorable": "Favorable", "Favorable": "Favorable",
    "Indifferent": "Neutre",
    "Unfavorable": "Défavorable", "Very unfavorable": "Défavorable",
}
SENTIMENT_ORDER = ["Favorable", "Neutre", "Défavorable"]

AGE = {
    "Under 18 years old": "< 18 ans", "18-24 years old": "18-24 ans", "25-34 years old": "25-34 ans",
    "35-44 years old": "35-44 ans", "45-54 years old": "45-54 ans", "55-64 years old": "55-64 ans",
    "65 years or older": "65 ans et +",
}
ORG_SIZE = {
    "Just me - I am a freelancer, sole proprietor, etc.": "Indépendant",
    "Less than 20 employees": "< 20 salariés",
    "20 to 99 employees": "20-99",
    "100 to 499 employees": "100-499",
    "500 to 999 employees": "500-999",
    "1,000 to 4,999 employees": "1 000-4 999",
    "5,000 to 9,999 employees": "5 000-9 999",
    "10,000 or more employees": "10 000 et +",
}
EXP_BANDS = ["0-2 ans", "3-5 ans", "6-10 ans", "11-20 ans", "21 ans et +"]

COUNTRY = {
    "United States of America": "États-Unis",
    "United Kingdom of Great Britain and Northern Ireland": "Royaume-Uni",
    "Germany": "Allemagne", "France": "France", "India": "Inde", "Canada": "Canada",
    "Netherlands": "Pays-Bas", "Poland": "Pologne", "Australia": "Australie", "Ukraine": "Ukraine",
    "Italy": "Italie", "Spain": "Espagne", "Brazil": "Brésil", "Sweden": "Suède", "Switzerland": "Suisse",
}

AI_USE_ORG = {
    "My organization does not currently use AI tools or agents for work": "Aucun usage dans l'organisation",
    "AI use is mostly optional and left up to individuals": "Usage facultatif, laissé aux individus",
    "Some teams actively encourage AI use, but practices vary across the organization": "Encouragé par certaines équipes, pratiques hétérogènes",
    "My organization provides approved AI tools and guidance for how to use them": "Outils approuvés et consignes fournis",
    "My organization expects some employees to use AI tools for certain types of work": "Usage attendu pour certains métiers",
    "My organization measures or evaluates AI use as part of employee or team performance": "Usage mesuré dans l'évaluation des équipes",
}

TOOL_FAMILY = {
    "General-purpose AI chat tools": "Assistants conversationnels généralistes",
    "AI coding assistants or coding agents": "Assistants / agents de code",
    "AI agents or automated workflows": "Agents ou workflows automatisés",
    "Internal AI tools built by my company": "Outils internes de l'entreprise",
}
FREQ_COLUMNS = {
    "AIFreq_1": "Assistants / agents de code",
    "AIFreq_2": "Assistants conversationnels généralistes",
    "AIFreq_3": "Agents ou workflows automatisés",
    "AIFreq_4": "Outils internes de l'entreprise",
}
FREQ = {"Daily": "Tous les jours", "Weekly": "Chaque semaine", "Monthly or Infrequent": "Mensuel ou moins"}

TASKS = {
    1: "Conception", 2: "Implémentation", 3: "Revue de code", 4: "Débogage / refactoring",
    5: "Documentation", 6: "Exploration d'architecture", 7: "Communication",
}
USEFUL_POSITIVE = ["Very useful", "Useful"]
USEFUL_NEGATIVE = ["More impractical than useful, not useful"]
USEFUL_IGNORE = ["Not applicable"]
SAT_POSITIVE = ["Greatly improved", "Somewhat improved"]
SAT_NEGATIVE = ["Greatly decreased", "Somewhat decreased"]

DISRUPTION = {
    "Plausible but wrong code": "Code plausible mais faux",
    "Hard-to-review generated code": "Code généré difficile à relire",
    "Missing context": "Contexte manquant",
    "Hallucinated package/config": "Paquet ou configuration inventé",
    "Incorrect or stale internal knowledge": "Connaissance interne fausse ou périmée",
    "Outdated APIs": "API obsolètes",
    "Poor debugging path": "Mauvaise piste de débogage",
    "Security/privacy issue": "Problème de sécurité / confidentialité",
    "Licensing/source uncertainty": "Incertitude de licence / source",
    "Other, please specify": "Autre",
}
AI_AVOID = {
    "I do not avoid using AI at work or school": "Je n'évite pas l'IA",
    "Concern over losing job skills or training an AI to replace you": "Peur de perdre ses compétences / de former son remplaçant",
    "Moral or ethical concerns": "Raisons morales ou éthiques",
    "Issues with privacy or security": "Confidentialité ou sécurité",
    "Environmental concerns": "Impact environnemental",
    "Difficulty or lack of training": "Difficulté ou manque de formation",
    "Other, please specify:": "Autre",
}
AI_ADOPT = {
    "The tool produces useful and accurate results": "Résultats utiles et exacts",
    "The tool meets security, privacy requirements": "Exigences de sécurité / confidentialité",
    "The price is acceptable for the value it provides": "Prix acceptable pour la valeur",
    "The tool meets legal or compliance requirements": "Exigences légales / conformité",
    "Your company policy allows for usage": "La politique de l'entreprise l'autorise",
    "Employees or teams are asking to use it": "Les équipes le demandent",
    "There is evidence that the tool improves business outcomes": "Preuve d'un effet sur les résultats métier",
    "The tool reduces time spent correcting, retrying, or reworking outputs": "Moins de temps à corriger / refaire",
    "The tool is worth paying more for because of better results": "Vaut un surcoût grâce à de meilleurs résultats",
    "Usage and spending are easy to monitor or limit": "Usage et dépenses faciles à suivre / plafonner",
    "The tool works well with how people already do their jobs": "S'intègre aux pratiques existantes",
    "The tool connects with systems people already use": "Se connecte aux systèmes existants",
    "The organization can switch tools or models without major disruption": "Changement d'outil sans rupture",
    "Human oversight is manageable": "Supervision humaine gérable",
    "Review burden is low": "Charge de relecture faible",
    "The tool has observability already integrated or built in": "Observabilité intégrée",
}
