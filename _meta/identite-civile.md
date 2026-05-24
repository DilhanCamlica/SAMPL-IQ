---
type: meta
purpose: facts civils objectifs sur l'utilisateur du vault, lus par les agents pour contextualisation opérationnelle uniquement
version: v1
status: template
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
last_validated_by_user: null
---

# Identité civile

> [!warning] Ce fichier ne contient QUE des facts civils objectifs.
> Aucun contenu cognitif (philosophie, patterns, valeurs, vision).
> Pour ça, voir les Maps dans `5-maps/`.
> Maximum 50 lignes hors frontmatter. Si ce fichier grossit, c'est qu'il dérive.

> [!note] À remplir (template SAMPL-IQ)
> Ce fichier est un gabarit. Remplace les `<placeholders>` par tes propres facts,
> supprime les lignes non pertinentes, puis passe `status: active` dans le frontmatter
> et renseigne `last_validated_by_user`. Les agents lisent ce fichier en début de
> session pour résoudre les références People courantes (cercle proche, géographie,
> structures) sans inventer. Plus il est juste, moins l'agent se trompe.

## État civil

- Nom complet : `<Prénom Nom>`
- Sexe : `<...>`
- Date de naissance : `YYYY-MM-DD`
- Nationalités : `<...>`
- Lieu de naissance : `<ville, pays>`

## Géographie

- Localisation actuelle : `<ville, pays>`
- Adresse précédente : `<...>`
- Adresse actuelle / future : `<...>`

## Structures professionnelles

- `<Nom société / structure>` (`<pays, identifiant légal optionnel>`)
- `<autre structure si applicable>`

## Cercle proche immédiat

> Wikilinke les People que tu cites ici. Les liens rouges (notes inexistantes) sont
> normaux : ils seront créés quand tu rempliras `2-people/`.

- Partenaire : `[[prenom-nom]]`
- Famille : `[[prenom-nom]]`, `[[prenom-nom]]`
- Animaux : `<noms, espèces>`

## Pour aller plus loin

Ce fichier ne dit rien sur qui tu es cognitivement. Pour ça :

- Patterns comportementaux : voir `[[patterns-comportementaux]]` (à créer)
- Posture philosophique : voir une Map dédiée dans `5-maps/`
- Vision stratégique : voir une Map dédiée dans `5-maps/`
