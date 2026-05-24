---
name: obsidian-triage
description: Triage des notes inbox de ton vault Obsidian SAMPL-IQ (0-inbox/). À utiliser quand l'utilisateur demande "lance un triage de mon inbox", "vide l'inbox", "classe les notes inbox", "obsidian-triage", "triage du second brain". Le skill lit chaque note inbox, propose une classification selon les 8 types du vault (atom, people, source, project, map, log, intention, question), crée les notes typées dérivées, supprime ou archive les notes inbox traitées, et commit chaque triage.
---

# Skill: obsidian-triage

> ⚠️ **Avant le premier usage** : remplace `<CHEMIN_DU_VAULT>` par le chemin absolu de ton vault. Voir `ONBOARDING.md`.

## Source de vérité

La doctrine et les heuristiques de triage vivent dans le vault. Lis ces fichiers **dans cet ordre** avant d'opérer :

1. **`<CHEMIN_DU_VAULT>/_meta/vault-doctrine-v1.md`** : fondation, les 8 types d'objets, philosophie "une note = un objet", relations par liens.
2. **`<CHEMIN_DU_VAULT>/_meta/conventions.md`** : schemas frontmatter détaillés par type, conventions de nommage, règles YAML.
3. **`<CHEMIN_DU_VAULT>/_meta/triage-criteria.md`** : §0 détection journal-daily, heuristiques de classification par type, hiérarchie de décision, gestion des doublons, du flag `needs_clarification`, des références ambiguës, des tâches urgentes court terme.
4. **`<CHEMIN_DU_VAULT>/_meta/journaling-criteria.md`** : workflow complet du rituel journal-daily. Déclenché quand la §0 de `triage-criteria.md` détecte le pattern.
5. **`<CHEMIN_DU_VAULT>/_meta/templates/<type>.md`** : template à suivre pour chaque type créé.
6. **`<CHEMIN_DU_VAULT>/_meta/identite-civile.md`** : facts civils objectifs sur l'utilisateur (cercle proche, géographie, structures), utiles pour résoudre les références People courantes.
7. **`<CHEMIN_DU_VAULT>/_meta/toilettage-rules.md`** : uniquement si une note inbox nécessite un re-toilettage avant classement.

Ces fichiers sont la **seule** source de vérité pour les règles de triage. Ce SKILL.md ne les duplique pas.

## Démarrage rapide

- **Vault** : `<CHEMIN_DU_VAULT>` (repo Git, branche `main`).
- **Source** : `0-inbox/` (notes avec frontmatter `type: inbox`).
- **Cibles** : `1-atoms/`, `2-people/`, `3-sources/`, `4-projects/`, `5-maps/`, `6-logs/`, `7-intentions/`, `8-questions/`.

Étapes générales :

1. Lire les 3 fichiers doctrine (`vault-doctrine-v1.md`, `conventions.md`, `triage-criteria.md`).
2. Lister les notes dans `0-inbox/`.
3. Pour chaque note : lire le contenu, proposer une classification, attendre validation utilisateur, créer la(les) note(s) dérivée(s) selon le template du type, supprimer la note inbox, commit.
4. Quand l'inbox est vide ou que l'utilisateur arrête, conclure (et dérouler la lifecycle, voir `_meta/lifecycle-criteria.md`).

## Garde-fous

- **Une note à la fois**, **une question à la fois**. Posture sparring partner.
- **Lossless** : si tu ne sais pas trancher, pose le flag `needs_clarification` plutôt que de classer arbitrairement.
- **Ne pas supprimer une note inbox** avant que les notes dérivées soient créées **et** validées.
- **Tâches urgentes court terme** : ne PAS les classer dans le vault (voir `_meta/triage-criteria.md` §3).
- **Doublons sémantiques** : signaler, proposer fusion / garder séparées / skip. Ne pas fusionner unilatéralement.
- **Références ambiguës** : interrompre et proposer des candidats.
- **Slugs** : kebab-case, sans accents, ≤ 50 chars pour les notes typées.
- **Wikilinks** : toujours via `[[slug-exact]]`, jamais le titre humain. Règle wikilink stricte : voir `CLAUDE.md`.
- **Frontmatter** : suivre exactement le schema du type dans `_meta/conventions.md`.

## Pattern de commit

```
🗂️ triage note <N>: <slug-source> → <résumé bref>
🗂️ triage inbox: <N notes> → <M dérivées> (<types-créés>)
```

## Pour un agent distant

Si tu es appelé sans accès à ce SKILL.md mais avec accès au repo, les 7 fichiers `_meta/` listés en §"Source de vérité" sont **self-contained** et suffisent pour exécuter un triage de bout en bout.
