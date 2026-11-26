# 3. Exploration des données

*Troisième et quatrième temps : explorer avec un journal, puis mettre les affirmations à l'épreuve. Les chiffres sont ceux de l'application et des notebooks `notebooks/00` à `05` ; ceux qui figurent dans le brief sont recalculés par `scripts/build_brief.py` (`preuves.csv`). Population par défaut : développeurs professionnels.*

## Journal d'exploration

Chaque entrée : ce que nous remarquons, ce que nous nous demandons, ce que nous avons fait ensuite.

| # | Je remarque | Je me demande | Suite donnée |
|---|---|---|---|
| 1 | La capacité perçue de l'IA sur les tâches complexes passe de 34 % (n = 20 397) à 60 % (n = 9 598). | Est-ce un vrai changement d'opinion ou un effet de qui répond ? | Observations 2 et 3 ; contrôles dans `DECISIONS.md` §6. |
| 2 | Le taux de réponse à cette question parmi les développeurs professionnels baisse : 70 % → 50 %. | Les répondants de 2026 sont-ils plus enthousiastes que ceux de 2025 ? | Affiché sous le tableau de bord (onglet Méthode) ; **réserve non levée**, citée dans le brief. |
| 3 | Parmi les seuls utilisateurs d'IA, la capacité perçue passe de 37 % à 60 %. | La hausse vient-elle d'une plus grande part d'utilisateurs ? | Non : elle existe chez les utilisateurs. Limite : la définition d'« utilisateur » diffère entre années. |
| 4 | L'attitude générale est stable (63 % → 64 %), alors que la capacité perçue bondit. | Les deux questions mesurent-elles la même chose ? | Non : capacité ≠ envie. Retenu comme nuance du message. |
| 5 | Parmi les seuls utilisateurs, l'attitude favorable baisse (74 % → 64 %) alors qu'elle est stable sur l'ensemble. | Est-ce un signal ou un artefact de définition ? | **Écarté du message** : définitions d'« utilisateur » différentes. À discuter si le jury interroge. |
| 6 | 49 % des répondants ne font confiance que si le résultat est vérifiable ; 7 % acceptent l'IA pour les décisions importantes. | Cette prudence diminue-t-elle avec l'expérience ? | Axe 2 : la part « vérifiable seulement » reste entre 45 % et 52 % selon l'ancienneté ; la confiance élevée passe de 4,5 % (0-2 ans) à 9,5 % (21 ans et plus). Prudence persistante, légère hausse de la confiance forte. |
| 7 | Erreurs les plus coûteuses : code « plausible mais faux » (72 %) et code difficile à relire (58 %), n = 9 514. | Quelles tâches déçoivent le plus ? | Axe 4 : l'implémentation est jugée utile par 80 % des répondants, la communication par 41 % ; 22 % se disent insatisfaits sur l'implémentation, contre 9 à 18 % pour les six autres tâches. |
| 8 | L'adoption est très hétérogène selon le rôle : 95,5 % en IA/ML, 76,3 % en systèmes embarqués. | L'écart vient-il du rôle ou de la taille des équipes ? | Axe 1 : filtres par taille d'organisation ; le rôle reste un groupe descriptif, pas une explication. |
| 9 | Politique d'organisation : « outils approuvés et règles » à 36,3 % dans les organisations de 10 000 salariés et plus, 7,9 % chez les indépendants. | Les règles changent-elles l'usage ? | Axe 5 : association descriptive seulement. |
| 10 | Satisfaction au travail ≥ 8 : 49,2 % chez les utilisateurs quotidiens, 41,2 % chez les autres. | L'IA rend-elle plus satisfait, ou l'ancienneté joue-t-elle sur les deux ? | Même direction dans les cinq tranches d'ancienneté ; intervalles disjoints seulement à partir de 6 ans. **Association, pas causalité** (formulé ainsi dans l'application). |
| 11 | Claude Code : 71,3 % d'utilisateurs, mais 39 % d'entre eux n'ont pas répondu à la question « souhait ». | Que faire d'une case vide ? | Première version : case vide = « ne veut pas » → 47 % d'admiration. Corrigé : non-réponse exclue → **77 %** (n = 3 741). Le choix est affiché sous la figure (`DECISIONS.md` §7). |

## Table de preuves

Une affirmation n'entre dans le message que si elle tient avec sa population, son effectif et son intervalle. Le détail chiffré des affirmations du brief est dans `preuves.csv` (13 lignes : id, valeur, n, intervalle, population, fonction de calcul).

| Affirmation | Preuve | Verdict | Limite |
|---|---|---|---|
| La capacité perçue a fortement augmenté. | P02 → P03 : 34 % → 60 %, intervalles disjoints, même question, mêmes modalités. | **Tenue** | Déclaratif ; changement possible de composition (obs. 2). |
| La hausse n'est pas un simple effet de la part d'utilisateurs. | P08 → P09 : 37 % → 60 % chez les utilisateurs. | **Tenue, avec réserve** | Définition d'« utilisateur » différente entre années. |
| L'attitude générale n'a pas bougé. | P04 → P05 : 63 % → 64 %, intervalles qui se recouvrent. | **Tenue** | Échelles à 3 classes harmonisées (`HARMONISATION.md`). |
| La confiance reste conditionnée à la vérification. | P06 : 49 % ; P07 : 7 %. | **Tenue pour 2026** | Question non comparable à 2025 : aucune évolution affirmée. |
| Les erreurs coûteuses sont celles que l'on ne voit pas d'abord. | P12 : 72 % ; P13 : 58 %. | **Tenue (déclaratif)** | Choix multiple ; parts non sommables ; pas de mesure du coût réel. |
| L'IA est réellement plus capable. | Aucune. | **Écartée** | L'enquête ne mesure pas la capacité réelle. |
| Les utilisateurs quotidiens sont plus satisfaits *grâce* à l'IA. | Association (obs. 10). | **Écartée comme causale** | Ancienneté, métier et organisation peuvent jouer sur les deux. |
| L'attitude des utilisateurs a baissé. | Obs. 5. | **Écartée du message** | Définitions non comparables. |

## Ce que l'exploration a changé

- Ajout du taux de réponse et du contrôle « utilisateurs » (obs. 2 et 3) au tableau de bord et au brief.
- Passage de l'admiration à un dénominateur « répondants aux deux questions » (obs. 11).
- Reformulation « à ancienneté égale » en « même direction dans les cinq tranches » (obs. 10), car l'écart n'est net qu'à partir de 6 ans d'ancienneté.
