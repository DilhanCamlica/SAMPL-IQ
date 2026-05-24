---
type: meta
purpose: roadmap d'évolution de la doctrine du vault (trous structurels identifiés et triggers d'activation)
version: v1
status: active
created: 2026-04-25
last_updated: 2026-04-26
last_validated_by_user: 2026-04-26
---

<!--
Changelog : externalisé vers _meta/doctrine-changelog.md (consulté à la demande).
Doctrine V1 anonymisée, packagée comme produit SAMPL-IQ.
-->

# Roadmap d'évolution de la doctrine du vault

Trois trous structurels ont été identifiés dans la doctrine v1 lors
de la réflexion initiale, par ordre de priorité d'ajout. Ce fichier
trace leur statut et leurs triggers d'activation.

## Priority 1 : Questions ouvertes (`8-questions/`) ✅ ACTIVÉ

**Statut** : activé dans la doctrine v1 (post 2026-04-25). Dossier
`8-questions/` opérationnel, type `question` ajouté avec schema
complet (voir [[conventions]] et [[triage-criteria]]). Première
question du vault : capturée pendant le triage du 2026-04-26.

**Constat initial** : beaucoup de questions ouvertes sans temps de
chercher la réponse sur le moment. Méritent d'être capturées pour y
revenir dans des moments réflexifs.

**Pourquoi pas un Atom** : un Atom est une pensée stable, une
réponse, un fragment de connaissance. Une question ouverte est
l'inverse : un manque, un trou productif, un appel à creuser.
Sémantique opposée.

**Pourquoi pas une Intention** : une Intention est un mouvement vers
un futur état (faire, lire, vivre). Une question est statique en
soi (elle n'appelle pas à une action mais à une réflexion).

## Priority 2 : Créations originales (`8-creations/`) (PENDING)

**Statut** : non activé. À activer **quand 2 à 3 vraies créations
existeront**.

**Constat** : à venir : textes de rap, peut-être essais, contenus
longs. Aucun type actuel ne convient (Atom = pensée stable, Source =
input externe, Project = scope structurée).

**Volume probable** : faible au début (1 à 3 textes), montée
possible si l'écriture créative reprend (voir
[[reprendre-ecriture-creative-si-inspire]], intention `dormant`,
et la map [[musique]]).

**Schema YAML proposé** :

```yaml
---
type: creation
created: YYYY-MM-DD
medium: rap | poem | essay | article | story | other
status: draft | wip | final | published | abandoned
inspired_by: [[atoms-ou-sources]]
people: [[...]]
maps: [[...]]
mood: <optional>
last_revised: YYYY-MM-DD
---
```

**Convention de nommage** : `<titre-de-l-oeuvre-en-kebab-case>.md`

**Trigger d'activation** : 2 à 3 vraies créations existent quelque
part (drafts WhatsApp, notes iPhone, textes papier) qu'il faut
ramener dans le vault.

## Priority 3 : Recipes / méthodes répétables (`8-recipes/` ou `playbooks/`) (PENDING)

**Statut** : non activé. À activer **après 1ère session triage si
3+ items du vault ressemblent à des recipes**.

**Évaluation post-triage 2026-04-26** : pas de candidat clair
identifié pour le moment. Plusieurs Atoms `subtype: rule` capturent
des règles méthodologiques (ex.
[[local-avant-vps-pour-iterer-multi-agents]],
[[tva-belge-0pct-services-b2b-hors-ue]]) mais aucun n'est une
**procédure exécutable** au sens recipe (séquence d'étapes
reproductibles avec inputs / outputs explicites). Trigger non atteint.

**Constat initial** : accumulation possible de mnémotechniques
(blackjack), de règles (permaculture), de protocoles (recettes
cuisine, méthodes de prise de notes), de patterns prompting LLM.
Cycle de vie spécifique : on apprend, on affine, on exécute.

**Pourquoi pas un Atom** : un Atom est une pensée. Une recipe est
une procédure exécutable.

**Pourquoi pas une Map** : une Map indexe des notes connexes. Une
recipe contient la procédure elle-même.

**Schema YAML proposé** :

```yaml
---
type: recipe
created: YYYY-MM-DD
domain: cooking | game | productivity | investment | gardening | other
inputs: [<liste des prérequis>]
outputs: <résultat attendu>
status: learning | tested | mastered | deprecated
times_executed: <nombre>
last_executed: YYYY-MM-DD | null
people: [[...]]
maps: [[...]]
---
```

**Convention de nommage** : `<verbe>-<sujet>.md`. Exemples :
`compter-cartes-blackjack-hi-lo.md`,
`compagnonnage-permaculture-tomate.md`.

**Trigger d'activation** : 3+ items du vault ressemblent à des
recipes (à reposer à chaque session de triage).

## Procédure d'activation d'un nouveau type

Quand on ajoutera un de ces types, **mettre à jour systématiquement** :

- `_meta/vault-doctrine-v1.md` (ou v2 si refonte)
- `_meta/conventions.md` (schema YAML, nommage)
- `_meta/templates/<type>.md` (nouveau template)
- `_meta/triage-criteria.md` (signaux de détection, hiérarchie)
- `_meta/grill-criteria.md` si pertinent
- `_meta/README.md` (table des types)
- Le dossier dédié (avec `.gitkeep`)
- `_meta/doctrine-roadmap.md` (ce fichier, marquer activé + date)

## Tableau récapitulatif

| Priorité | Type | Dossier cible | Statut | Trigger |
|---|---|---|---|---|
| 1 | Question | `8-questions/` | ✅ activé | besoin déjà identifié |
| 2 | Creation | `8-creations/` | pending | 2-3 créations existent |
| 3 | Recipe | `8-recipes/` ou `playbooks/` | pending | 3+ items recipes-like détectés |
