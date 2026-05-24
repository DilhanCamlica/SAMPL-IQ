---
type: meta
purpose: historique append-only des évolutions de la doctrine _meta/*.md, externalisé depuis les commentaires HTML en tête de chaque fichier pour alléger le cold-start
version: v1
created: YYYY-MM-DD
---

# Changelog de la doctrine

> [!important] Ne PAS charger ce fichier en cold-start
> Consulté **uniquement à la demande** : retracer l'historique complet d'une règle,
> comprendre pourquoi elle a été modifiée. Chaque fichier doctrine `_meta/*.md` conserve
> dans son commentaire HTML de tête uniquement les 3 dernières entrées le concernant +
> un pointeur vers ce fichier.

## Format

Une entrée par modification doctrinale, append-only, la plus récente en haut. Format :

```
## YYYY-MM-DD : <titre court de l'évolution>
Fichiers touchés : <liste>.
<Quoi a changé et pourquoi. Quel trigger l'a déclenché.>
```

Toute modification de doctrine (`_meta/*.md`) doit, idéalement, laisser une trace ici. Voir `_meta/doctrine-roadmap.md` pour la gouvernance de l'évolution doctrinale (la doctrine est read-only sauf trigger explicite + accord de l'utilisateur).

## Entrées

<!-- Exemple de format (à remplacer par tes vraies entrées) :
## 2026-01-20 : ajout d'une valeur à l'enum `relation` du type People
Fichiers touchés : conventions.md, vault-doctrine-v1.md, templates/people.md.
Émergé pendant un triage : besoin de distinguer un contact pro d'un simple
acquaintance. Validé avec l'utilisateur avant application.
-->

## YYYY-MM-DD : seed initial du produit SAMPL-IQ
Fichiers touchés : tous les `_meta/*.md`.
Version anonymisée de la doctrine V1 d'un vault personnel, packagée comme produit clonable. 8 types fermés, schemas YAML figés, conventions de nommage figées. Point de départ de ta propre doctrine : tu peux la faire évoluer, mais lis `vault-doctrine-v1.md` et `doctrine-roadmap.md` d'abord.
