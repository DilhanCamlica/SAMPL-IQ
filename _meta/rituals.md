---
type: meta
purpose: operational-rituals
version: v1
last_updated: 2026-04-25
---

# Rituels

## Fermeture hebdo (5 minutes, fin de semaine)

Pas chaque session, ce serait insoutenable. Une fois par semaine, 4 questions :

### 1. Capté

Quelles notes ai-je créées cette semaine en `0-inbox/` ?
- Lesquelles je classe maintenant en Atom, Source, Log, People, Map, Project, Intention ou Question ?
- Lesquelles je supprime (ou sortent du vault si tâche urgente court terme) ?

L'inbox doit être vide à la fin du rituel.

### 2. Connecté

Quelles notes méritent un lien vers une Map ou une People que j'ai oublié de mettre ?
- Ouvrir les Atoms de la semaine.
- Vérifier que chacun a au moins une Map et, si pertinent, une Source ou un People.
- Une note orpheline (zéro lien) n'est pas mémorisable.

### 3. Cristallisé

Y a-t-il une réflexion récurrente cette semaine qui mérite de devenir une Map
(nouveau domaine), ou de structurer une Map existante ?
- Si trois Atoms parlent du même sujet sans Map d'attache, créer la Map.
- Si une Map existante a maturé, mettre à jour `maturity:` (`stub` → `growing` → `mature`)
  et `last_updated:`.

### 4. Cleané

Y a-t-il une note doublon, périmée, ou qui devrait migrer vers Notion ?
- Doublon : merger en gardant le slug le plus stable, supprimer l'autre.
- Périmé : marquer le statut (`abandoned`, `read`, `done`) plutôt que supprimer.
- Migration Notion : si une réflexion est devenue un process à exécuter en équipe,
  la transformer pour Notion. Garder la note Obsidian comme source originale avec
  un pointeur Notion dans le frontmatter.

## Cadence

Hebdo uniquement pour V1. Si un besoin de cadence plus longue émerge,
on l'ajoutera dans une V2.

## Outil de rattrapage : lifecycle-lint

Avant de lancer le rituel hebdo (ou en remplacement quand la semaine
a été dense), exécuter le linter lecture-seule qui produit une note
inbox structurée listant les dérives accumulées :

```bash
python3 _meta/scripts/lifecycle-lint.py
```

5 catégories scannées : intentions actives à fermer, Maps maturity
incohérente, People `last_seen` obsolète, Maps manquantes recommandées
par vault-state, doublons sémantiques suspects.

Le rapport atterrit dans `0-inbox/<YYYY-MM-DD-HHmm>-lifecycle-audit-...md`
avec `device: lifecycle-audit`. Au prochain triage low-friction, il est
détecté ([[triage-criteria]] §0bis) et intégré en tête du brief one-shot
comme plan d'action structuré. Pas comme une idée à la volée.

Voir [[lifecycle-criteria]] §10 et `_meta/scripts/README.md` pour le
détail du workflow et les limitations connues.
