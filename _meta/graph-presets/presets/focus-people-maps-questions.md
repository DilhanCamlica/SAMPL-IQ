---
type: meta-preset
purpose: squelette de réflexion humaine et structurelle, sans bruit atomique
created: 2026-05-08
last_updated: 2026-05-08
---

# Preset : focus-people-maps-questions

## Objectif

Vue de réflexion : qui je connais, dans quels domaines (hubs structurels), et quelles questions je porte sur eux ou ces domaines. Pas d'input externe (sources), pas de chrono (logs), pas de briques de connaissance (atoms). Le squelette structurel + humain + interrogatif uniquement.

Usage typique :
- Préparer une session de creusage Question pour voir quels acteurs et domaines gravitent autour.
- Avant un appel ou un retour Portugal pour visualiser le réseau des personnes proches du sujet.
- Diagnostic graphe : repérer les People orphelines de Maps, les Questions non rattachées à des People.

## Filtre

```
path:2-people/ OR path:5-maps/ OR path:8-questions/
```

Inclus : People, Maps, Questions.
Exclus : Atoms, Sources, Projects, Logs, Intentions, Inbox, _meta.

## Couleurs (subset palette de référence)

| Type | Hex | Couleur | Décimal | Rôle dans cette vue |
|---|---|---|---|---|
| 2-people | `#44C9EF` | cyan | 4508143 | relations humaines (star de la vue) |
| 5-maps | `#0DC689` | vert émeraude | 902793 | hubs structurels (pont entre clusters) |
| 8-questions | `#EF4444` | rouge | 15680580 | questions ouvertes (signal fort, à traiter) |

## Lecture attendue

Trois clusters de couleurs très contrastées : cyan (People), vert (Maps), rouge (Questions). Les Maps font le pont entre People et Questions là où ces liens existent directement.

Si le graphe paraît clairsemé, c'est un signal valide :
- Beaucoup de Questions sont reliées à People via Atoms intermédiaires (donc absents ici).
- Beaucoup de People sont rattachées à des Maps via leur frontmatter `maps:`, mais pas toujours.
- Matière pour wikilinker plus directement People ↔ Question quand pertinent (au lieu de passer toujours par un Atom).

## JSON

```json
{
  "search": "path:2-people/ OR path:5-maps/ OR path:8-questions/",
  "showTags": false,
  "showAttachments": false,
  "hideUnresolved": true,
  "showOrphans": false,
  "colorGroups": [
    { "query": "path:2-people/",    "color": { "a": 1, "rgb": 4508143  } },
    { "query": "path:5-maps/",      "color": { "a": 1, "rgb": 902793   } },
    { "query": "path:8-questions/", "color": { "a": 1, "rgb": 15680580 } }
  ]
}
```

## Notes / historique

- 2026-05-08 : création du preset à la demande de l'utilisateur, premier preset thématique après macro.

## Pour activer

```bash
bash _meta/graph-presets/swap.sh focus-people-maps-questions
```

Puis Cmd+R dans Obsidian.
