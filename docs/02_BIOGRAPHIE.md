# 2. Biographie des données

*Deuxième temps : faire connaissance avec les données avant de les interroger. Sources : pages « méthodologie » de Stack Overflow pour 2025 et 2026, fichiers de schéma publiés avec les données, et vérifications faites dans `notebooks/00_prise_en_main.ipynb`.*

## Qui les a produites, pourquoi, comment

| | 2026 | 2025 |
|---|---|---|
| **Producteur** | Stack Overflow, enquête annuelle auprès des développeurs | idem |
| **Pourquoi** | Suivre les pratiques, outils et opinions de la communauté ; publier les résultats et les données | idem |
| **Collecte** | En ligne, du 23 juin au 5 août 2026 | En ligne, du 29 mai au 23 juin 2025 |
| **Recrutement** | Volontaires, invités via stackoverflow.com, le blog Stack Overflow et la liste d'e-mails (inscription volontaire) | Volontaires, recrutés surtout par les canaux de Stack Overflow (messages sur le site, blog, lettre d'information, bannières, réseaux sociaux ; Reddit moins de 2 %) |
| **Lignes brutes → valides** | 39 266 → **30 903** réponses valides | 49 009 réponses annoncées (le fichier public contient 49 191 lignes, écart non expliqué dans la documentation ; nous gardons toutes les lignes du fichier) |
| **Validité** | Consentement, statut d'emploi renseigné, filtres anti-robots (reCAPTCHA, doublons, réponses en ligne droite, progression, durée) avec une règle de récupération (les dix questions de base renseignées) | Filtres comparables |
| **Pondération** | Aucune décrite | Aucune décrite |
| **Licence** | ODbL 1.0 (base) et DbCL 1.0 (contenu) | idem |
| **Taille du fichier utilisé** | 30 903 lignes × 212 colonnes, 169 pays | 49 191 lignes × 172 colonnes, 177 pays |

## Ce que représente une ligne

**Une ligne = une personne ayant rempli l'enquête**, identifiée par un numéro séquentiel public (`ResponseId`), pas par une identité. Ce n'est ni un employeur, ni une équipe, ni une période d'observation : c'est une opinion déclarée à un moment donné. Une même personne peut avoir répondu aux deux années sans que les fichiers permettent de le savoir : les deux échantillons sont comparés comme deux photographies, pas comme un suivi.

Les cases vides n'ont pas toutes le même sens : la question n'a pas été posée (bloc non affiché), la personne l'a sautée, ou elle a répondu « je ne sais pas / pas d'usage ». L'application ne les traite jamais comme une réponse négative (voir `DECISIONS.md` §6 et §7).

## Qui est dans l'analyse

| Étape | 2026 | 2025 |
|---|---|---|
| Réponses valides | 30 903 | 49 191 lignes |
| Développeurs professionnels (population par défaut) | **20 220** | **34 146** |
| Dont ayant répondu à la question sur les outils d'IA (2026) | 11 803 | non comparable |
| Dont ayant répondu à la question de capacité sur tâches complexes | 9 598 | 20 397 |

Définition de « développeur professionnel » : le code est une partie principale du métier (2026, variable `CodeMain`) ou « développeur de profession » (2025, `MainBranch`), en emploi ou indépendant. Les deux libellés diffèrent légèrement : c'est dit dans l'application (onglet Méthode) et dans `HARMONISATION.md`.

## Ce qui manque ou peut fausser

- **Auto-sélection.** Les volontaires sont probablement plus engagés avec la communauté Stack Overflow que la moyenne des développeurs. Les parts décrivent les répondants, pas tous les développeurs.
- **Pas de pondération.** Les États-Unis pèsent 3 177 des 20 220 développeurs professionnels de 2026 ; la France 545. Les comparaisons par pays à petit effectif affichent leur intervalle ou sont retirées sous 30 répondants.
- **Taux de réponse au bloc IA.** Parmi les développeurs professionnels, 70 % ont répondu à la question de capacité en 2025 contre 50 % en 2026. Si ceux qui répondent ont changé, une partie de l'évolution vient de la composition (`DECISIONS.md` §6).
- **Questions qui changent.** Seules l'attitude générale et la capacité sur tâches complexes sont comparables. Confiance, fréquence d'usage et agents ont changé de formulation : non comparés.
- **Déclaratif.** Aucune mesure de productivité, de qualité du code ou d'erreurs réelles.
- **Pas de lien entre années.** Pas d'identifiant commun : aucune analyse de trajectoire individuelle.

## Précautions prises

Données jamais versionnées (`data/` ignoré par Git, téléchargement par `get_data.py` depuis le dépôt public de Stack Overflow, fichiers LFS) ; colonnes chargées limitées à l'utile ; toutes les parts accompagnées de leur effectif et d'un intervalle de Wilson à 95 % ; minimum 30 répondants par part.
