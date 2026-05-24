---
type: meta-preset
purpose: vue exhaustive du vault, macro + doctrine technique `_meta/`
created: 2026-05-08
last_updated: 2026-05-08
---

# Preset : meta

## Objectif

Vue exhaustive du vault, sans aucun filtre. Identique à `macro` côté contenu typé, mais expose en plus le système (`_meta/` : doctrine, criteria, graph-presets, etc.).

À utiliser quand on veut auditer la doctrine elle-même : voir comment `_meta/*` est référencé depuis le contenu, repérer des criteria orphelins, vérifier les ponts entre doctrine et notes typées.

## Filtre

```
(vide)
```

Aucun filtre. Toutes les notes du vault sont exposées, y compris `_meta/`.

## Couleurs

Palette macro complète + une entrée pour `_meta/` :

| Type | Hex | Couleur | Décimal | Rôle |
|---|---|---|---|---|
| 1-atoms | `#B8B8B8` | gris clair | 12105912 | briques de connaissance |
| 2-people | `#44C9EF` | cyan | 4508143 | relations humaines |
| 3-sources | `#8B5CF6` | violet | 9133302 | input externe |
| 4-projects | `#FED100` | jaune | 16699648 | action structurée |
| 5-maps | `#0DC689` | vert émeraude | 902793 | hubs structurels |
| 6-logs | `#9A9A9A` | gris | 10132122 | chronologie |
| 7-intentions | `#F97316` | orange | 16347926 | engagement futur |
| 8-questions | `#EF4444` | rouge | 15680580 | questions ouvertes |
| 0-inbox | `#7CB1E7` | bleu pâle | 8172007 | backlog |
| _meta | `#334155` | slate foncé | 3359061 | doctrine, infra, criteria |

Le slate foncé `#334155` est volontairement sombre et froid pour signaler "infrastructure" sans se confondre avec les deux gris existants (atoms `#B8B8B8` et logs `#9A9A9A`). Couleur ajoutée hors palette de référence Tailwind 500, validée explicitement par l'utilisateur le 2026-05-08.

## Lecture attendue

Macro + un cluster slate distinct (les `_meta/*.md` : criteria, doctrine, graph-presets, vault-state, etc.). On voit visuellement quels nodes typés pointent vers la doctrine (CLAUDE.md, vault-doctrine-v1, conventions, criteria) et lesquels n'y sont pas connectés.

Utile pour :

- Diagnostiquer si la doctrine est correctement référencée depuis le contenu typé.
- Repérer des fichiers `_meta/` orphelins (mais `showOrphans: false` les cache).
- Vérifier les ponts entre `_meta/graph-presets/*` et le reste du système.

## JSON

```json
{
  "search": "",
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
    { "query": "path:0-inbox/",      "color": { "a": 1, "rgb": 8172007  } },
    { "query": "path:_meta/",        "color": { "a": 1, "rgb": 3359061  } }
  ]
}
```

## Notes / historique

- 2026-05-08 : création du preset, palette = macro + slate foncé `#334155` pour `_meta/`. Couleur arbitrée par l'utilisateur.

## Pour activer

```bash
bash _meta/graph-presets/swap.sh meta
```

Puis Cmd+R dans Obsidian.
