# Décisions

Chaque choix de conception ou d'analyse, avec sa justification. Les chiffres cités sont ceux de la population par défaut (développeurs professionnels, tous pays) ; ils sont recalculés par l'application selon les filtres.

## 1. Thème et commanditaire
- **Thème : l'IA au travail.** C'est le thème le plus développé de l'enquête 2026 (61 des 212 colonnes commencent par `AI` ou `LLM`, sans compter les questions sur les agents et le contexte) et une question de décision concrète pour un décideur technique.
- **Commanditaire : la direction technique d'une ESN française de 3 000 personnes** (commanditaire fictif, un des exemples du sujet). Sa décision : comment équiper les développeurs en assistants et agents de code, et sur quoi investir à côté.
- **Message du tableau de bord :** les développeurs jugent l'IA nettement plus capable sur les tâches complexes qu'en 2025 (34 % → 60 % d'avis positifs), mais l'attitude générale n'a pas bougé (63 % → 64 %) et seuls 7 % lui font confiance y compris pour les décisions importantes : le sujet n'est plus l'adoption, c'est la vérification.
- **Pourquoi ce message :** il combine les deux seules questions comparables avec 2025 et la confiance 2026, et il débouche sur une décision (investir dans la revue et les tests, pas seulement dans les licences).

## 2. Cinq axes, un par membre
| Axe | Question au commanditaire | Porteur |
|---|---|---|
| 1 Adoption | Qui est déjà équipé, avec quels types d'outils, à quel rythme ? | Ruben COMBE--TAMAIN |
| 2 Confiance | Quelle confiance, pour quel profil, et qu'est-ce qui a changé depuis 2025 ? | Antoine REVERSAT |
| 3 Agents de code | Quels outils, lesquels veut-on garder ou adopter ? | Edwin DREAN-AVRILLON |
| 4 Coûts cachés | Où l'IA fait-elle perdre du temps, pour quelles tâches aide-t-elle ? | Arthur REYNAUD |
| 5 Organisation | Comment les organisations encadrent l'IA, que change-t-elle pour les personnes ? | Léo VAZ SAMPAIO--DESTOT |

Les axes se suivent comme un entonnoir de décision : *qui utilise* → *peut-on se fier* → *avec quels outils* → *ce que ça coûte* → *comment l'organiser*.

## 3. Population par défaut
Développeurs professionnels : le code est une partie principale du métier (2026) / « développeur de profession » (2025), **en emploi ou indépendant**. Les étudiants, retraités et personnes sans emploi sont exclus par défaut, car le commanditaire équipe des salariés. Le lecteur peut passer à « Tous les répondants ». La différence de libellés entre 2025 et 2026 est une limite (HARMONISATION.md).

## 4. Rigueur statistique
- **Volontaires :** dit dans chaque légende de figure, dans l'onglet Méthode et dans le README. Aucune part n'est présentée comme celle de « tous les développeurs ».
- **Intervalles de Wilson à 95 %** sur toutes les parts : ils restent valables pour de petits effectifs et près de 0 % ou 100 %.
- **Seuil de 30 répondants** (`devia/config.py`) : en dessous, l'application ne dessine pas et le dit (`guard_min_n`). Les sous-groupes de moins de 30 sont retirés et listés sous la figure. Valeur courante en statistique descriptive, pas un seuil magique : un IC large reste affiché au-dessus. **Justification chiffrée :** pour une part proche de 50 %, la demi-largeur de l'intervalle de Wilson à 95 % est de ±26 points pour n = 10, **±17 points pour n = 30**, ±10 points pour n = 100 et ±5 points pour n = 400. À 30, un écart de 10 points entre deux groupes est déjà noyé dans l'incertitude ; en dessous, la part n'apprend presque rien. Nous gardons 30 comme plancher d'affichage et laissons l'intervalle dire l'incertitude restante ; relever le seuil à 100 ferait disparaître la France de plusieurs figures (545 développeurs professionnels au total, bien moins une fois filtrés).
- **Choix multiples :** le dénominateur est le nombre de **répondants** à la question, pas le nombre de citations ; les parts ne somment donc pas à 100 %.
- **Titres dynamiques :** chaque titre est construit à partir des chiffres de la sélection (`devia/message.py`) et se réduit à ce qui reste vrai si l'effectif est trop faible ou si 2025 est indisponible.

## 5. Harmonisation 2025 ↔ 2026
Seules deux questions sont comparées (attitude, capacité sur tâches complexes). La confiance, la fréquence d'usage et les agents ne le sont **pas** : les questions ont changé. Un graphique d'évolution fabriqué à partir de questions différentes aurait eu l'air net et aurait été faux. Voir HARMONISATION.md.

## 6. Contrôles sur le résultat principal (34 % → 60 %)
- **Capacité « positive » = Bonne + Très bonne, parmi les répondants ayant un avis** : « je ne sais pas / pas d'usage » est exclu les deux années, car sa part a fortement changé (15 % → 6 %).
- **Contrôle composition d'utilisateurs :** parmi les seuls utilisateurs d'IA, 37 % (2025) → 60 % (2026). La hausse n'est pas due à un simple changement de la part d'utilisateurs.
- **Réserve non levée :** le taux de réponse au bloc IA a baissé (70 % → 50 %). On ne peut pas exclure que les répondants de 2026 diffèrent de ceux de 2025. L'application l'affiche.
- **Nuance non retenue dans le message :** parmi les seuls utilisateurs, la part d'attitude favorable est plus basse en 2026 (64 %) qu'en 2025 (74 %), alors qu'elle est stable sur l'ensemble des répondants (63 % → 64 %). Les définitions d'« utilisateur » diffèrent entre les années, donc nous ne tirons pas de conclusion : à discuter si le jury pose la question.
- **Ce que le message ne dit pas :** que l'IA *est* plus capable. Il dit que les répondants *la jugent* plus capable.

## 7. Axe 3 : taux d'admiration
« Admiré » = utilisateur de l'outil qui veut encore l'utiliser dans les 6 mois, **parmi les utilisateurs qui ont aussi répondu à la question « souhait »**. Première version : rapportée à tous les utilisateurs. Constat : 39 % des utilisateurs de Claude Code n'ont pas répondu à « souhait » (case vide) ; les compter comme « ne veut pas » donnait 47 % contre 77 % parmi les répondants aux deux questions. Une case vide est traitée comme une absence de réponse. Le choix est affiché sous la figure.

## 8. Axe 5 : « satisfait »
Note de satisfaction professionnelle ≥ 8 sur 10 (`SATISFIED_FROM`). Seuil conventionnel (les 3 derniers points de l'échelle), modifiable. La comparaison usage quotidien / pas d'usage quotidien est faite **par tranche d'ancienneté**, car l'ancienneté joue à la fois sur l'usage et sur la satisfaction. C'est une association, jamais présentée comme un effet.

## 9. Architecture et état
- **Séparation :** `devia/` (analyse, sans Streamlit hors de `devia/ui/`) et `dashboard.py`, `pages/` (interface). Les tests unitaires n'ont donc pas besoin de Streamlit ni des CSV.
- **`st.cache_data`** uniquement pour le chargement : `load_frames` (lecture + préparation des CSV). **`st.cache_resource`** pour le téléchargement initial (une capacité partagée, pas une donnée). Aucun calcul d'analyse n'est mis en cache : il est assez rapide et dépend des filtres.
- **`st.session_state`** : l'état canonique des filtres (`filters`) et un compteur `filters_ver`. Les widgets utilisent des clés versionnées ; « Réinitialiser » incrémente le compteur et les widgets repartent de leurs valeurs par défaut. Les filtres survivent au changement de page (Streamlit supprime l'état d'un widget absent de la page : on recopie donc la valeur dans l'état canonique via `on_change`).
- **Navigation `st.navigation`** : une page par axe, filtrée sur l'existence du fichier. L'application tourne avec le socle seul et s'enrichit au fil des fusions de branches.
- **Indicateurs partagés (`devia/indicators.py`)** : le chiffre du tableau de bord est calculé par la même fonction que celui de l'axe qui le détaille.

## 10. Graphiques
Figures **matplotlib** (`st.pyplot`) pour les figures présentées : contrôle total de l'intervalle, des effectifs et du **pied de population écrit dans l'image** (une capture d'écran garde sa population). Style : barres fines, grille discrète, bleu = 2026 / mise en avant, gris = 2025 / contexte, rouge = négatif ; pas d'axe double. Chaque figure est suivie d'une légende Streamlit « Population : qui, année, n ».

## 11. Reproductibilité
`uv sync` reconstruit l'environnement depuis `uv.lock` ; `uv run python get_data.py` télécharge les données dans `data/` (ignoré par git, jamais versionné) ; l'adresse `media.githubusercontent.com` est utilisée car les fichiers sont en Git LFS (l'adresse « raw » ne renvoie qu'un pointeur). Au premier lancement, l'application télécharge elle-même les données si elles manquent (utile au déploiement).

## 12. Ce que nous n'avons pas fait
- Pas de modèle prédictif ni de test d'hypothèse formel : l'enquête est faite de volontaires, sans pondération ; un p-value donnerait une fausse précision. Les intervalles montrent l'incertitude d'échantillonnage seulement, pas le biais de sélection.
- Pas de salaires ni de comparaison de technologies hors IA : hors du sujet du commanditaire.
