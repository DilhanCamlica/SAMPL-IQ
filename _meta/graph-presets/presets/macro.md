---
type: meta-preset
purpose: vue d'ensemble baseline du vault, palette complète par type
created: 2026-05-08
last_updated: 2026-05-08
---

# Preset : macro

## Objectif

Vue d'ensemble du vault, baseline. C'est le preset par défaut, à appliquer quand il n'y a pas de focus particulier. Toute autre vue se construit en filtrant/sélectionnant à partir de macro, pas en inventant une palette ad hoc.

> **Règle stricte** : ne pas modifier macro sans validation explicite de l'utilisateur. C'est la baseline partagée. Toute évolution de palette ou de filtre = nouveau preset à côté.

## Filtre

```
-path:_meta/
```

Cache uniquement les nodes techniques de doctrine (`_meta/`). Tout le reste du contenu typé est exposé.

## Couleurs (palette de référence complète)

| Type | Hex | Couleur | Décimal | Rôle |
|---|---|---|---|---|
| 1-atoms | `#B8B8B8` | gris clair | 12105912 | briques de connaissance, décor neutre |
| 2-people | `#44C9EF` | cyan | 4508143 | relations humaines |
| 3-sources | `#8B5CF6` | violet | 9133302 | input externe (calls, lectures) |
| 4-projects | `#FED100` | jaune | 16699648 | action structurée |
| 5-maps | `#0DC689` | vert émeraude | 902793 | hubs structurels |
| 6-logs | `#9A9A9A` | gris | 10132122 | chronologie |
| 7-intentions | `#F97316` | orange | 16347926 | engagement futur |
| 8-questions | `#EF4444` | rouge | 15680580 | questions ouvertes |
| 0-inbox | `#7CB1E7` | bleu pâle | 8172007 | backlog (visible mais discret) |

## Lecture attendue

Toutes les notes typées du vault, regroupées par couleur de dossier. Les nodes Atoms (gris) forment le maillage le plus dense, autour duquel gravitent les Maps (vert), People (cyan), Sources (violet), etc. Permet de repérer visuellement :

- Les zones denses (clusters mature) vs zones clairsemées (à enrichir)
- Les nodes orphelins ou faiblement connectés (mais `showOrphans: false` les cache)
- Les ponts entre domaines (Atoms qui pointent vers plusieurs Maps)

## JSON

```json
{
  "search": "-path:_meta/",
  "showTags": false,
  "showAttachments": false,
  "hideUnresolved": true,
  "showOrphans": false,
  "colorGroups": [
    { "query": "path:1-atoms/",      "color": { "a": 1, "rgb": 12105912 } },
    { "query": "path:2-people/",     "color": { "a": 1, "rgb": 4508143  } },
    { "query": "path:3-sources/",    "color": { "a": 1, "rgb": 9133302  } },
    { "query": "path:4-projects/",   "color": { "a": 1, "rgb": 16699648 } },
    { "query": "path:5-maps/",       "color": { "a": 1, "rgb": 902793   } },
    { "query": "path:6-logs/",       "color": { "a": 1, "rgb": 10132122 } },
    { "query": "path:7-intentions/", "color": { "a": 1, "rgb": 16347926 } },
    { "query": "path:8-questions/",  "color": { "a": 1, "rgb": 15680580 } },
    { "query": "path:0-inbox/",      "color": { "a": 1, "rgb": 8172007  } }
  ]
}
```

## Notes / historique

- 2026-05-08 : création du preset, palette initiale Tailwind 500-series.
- 2026-05-08 : ajustement palette par l'utilisateur (atoms gris au lieu de ambre, people cyan au lieu de rouge, questions rouge au lieu de fuchsia, projects jaune au lieu de bleu, etc.). Sémantique stabilisée.

## Pour activer

```bash
bash _meta/graph-presets/swap.sh macro
```

Puis Cmd+R dans Obsidian.
