---
type: meta
purpose: log append-only des sessions et clusters, externalisé depuis vault-state §9 pour alléger le cold-start agent (rolling 14 jours)
version: v1
created: YYYY-MM-DD
---

# Log des sessions

> [!important] Ne PAS charger ce fichier en cold-start
> Ce log est consulté **uniquement à la demande** : retracer une décision, vérifier
> qu'une Map est recommandée depuis ≥3 sessions consécutives (lifecycle §4), comprendre
> le contexte d'évolution d'un objet. En début de session, l'agent lit `vault-state.md`,
> pas ce fichier.

## Format

Une ligne par session, append-only, la plus récente en bas. Format :

```
- YYYY-MM-DD | <type-session> | <résumé court < 30 mots>
```

`<type-session>` ∈ `capture | triage | transcripts-import | youtube-import | session-people | session-question | session-map | session-atom | session-source | session-project | session-intention | session-log | free-roam | journaling | doctrine`.

**Rolling 14 jours** : en fin de session, si la première entrée (la plus ancienne) date de plus de 14 jours, la déplacer dans `_meta/archive/vault-state-log-<YYYY-Q>.md` (créer le fichier et le dossier `archive/` si besoin). Ça garde ce fichier lisible sans saturer le contexte agent.

## Entrées

<!-- Exemple de format (à remplacer par tes vraies entrées) :
- 2026-01-15 | triage | 6 notes inbox → 4 atoms + 1 question + 1 people ; création Map [[exemple]]
-->

_Aucune session encore. La première session de travail appendra ici._
