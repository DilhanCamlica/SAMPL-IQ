---
type: meta-preset
purpose: squelette de réflexion (people, maps, questions) avec maillage atomique en décor
created: 2026-05-08
last_updated: 2026-05-10
---

# Preset : focus-people-maps-questions-atoms

## Objectif

Variante de [[focus-people-maps-questions]] qui réintroduit les Atoms en gris neutre, comme tissu conjonctif entre les trois clusters colorés (People, Maps, Questions). Toujours pas d'input externe (Sources), pas de chrono (Logs), pas d'engagement futur (Intentions), pas de Projects, pas d'Inbox.

Usage typique :
- Préparer une session de creusage Question en voyant non seulement les acteurs et domaines, mais aussi les briques de connaissance déjà capturées qui s'y rattachent.
- Diagnostic graphe : repérer les Atoms qui font le pont entre People et Questions (chemin sémantique réel) vs les Atoms isolés.
- Avant un appel, voir le contexte humain + les notes déjà accumulées sur la personne ou le domaine.

Différence vs [[focus-people-maps-questions]] : ici les Atoms sont visibles (gris neutre, en arrière-plan), donc le graphe est plus dense mais aussi plus informatif. Choisir selon le besoin du moment :
- `focus-people-maps-questions` quand on veut juste le squelette structurel + humain + interrogatif sans bruit.
- `focus-people-maps-questions-atoms` quand on veut le même squelette mais en sachant aussi quelles briques de connaissance sont déjà accumulées autour.

## Filtre

```
(path:1-atoms/ OR path:2-people/ OR path:5-maps/ OR path:8-questions/) -["status":"answered"]
```

Inclus : Atoms, People, Maps, Questions.
Exclus : Sources, Projects, Logs, Intentions, Inbox, _meta. Plus toute note dont le frontmatter `status: answered` (en pratique : Questions résolues, qui n'ont plus à parasiter le squelette de réflexion vivante).

## Couleurs (subset palette de référence)

| Type | Hex | Couleur | Décimal | Rôle dans cette vue |
|---|---|---|---|---|
| 1-atoms | `#B8B8B8` | gris clair | 12105912 | maillage de connaissance, décor neutre |
| 2-people | `#44C9EF` | cyan | 4508143 | relations humaines |
| 5-maps | `#0DC689` | vert émeraude | 902793 | hubs structurels (pont entre clusters) |
| 8-questions | `#EF4444` | rouge | 15680580 | questions ouvertes (signal fort, à traiter) |

## Lecture attendue

Trois clusters colorés (cyan People, vert Maps, rouge Questions) émergent au-dessus d'un maillage gris (Atoms). Les Atoms gris jouent le rôle de tissu conjonctif : ils relient People à Questions, Maps à People, etc.

À surveiller :
- Atoms gris isolés ou faiblement connectés : candidats à enrichissement ou archive.
- Atoms qui font le pont entre 2+ Maps : nodes structurellement riches.
- Questions sans Atom au voisinage : potentiellement encore brutes, peu creusées.
- People avec beaucoup d'Atoms gris autour : zone de connaissance dense sur cette personne.

## JSON

```json
{
  "search": "(path:1-atoms/ OR path:2-people/ OR path:5-maps/ OR path:8-questions/) -[\"status\":\"answered\"]",
  "showTags": false,
  "showAttachments": false,
  "hideUnresolved": true,
  "showOrphans": false,
  "colorGroups": [
    { "query": "path:1-atoms/",     "color": { "a": 1, "rgb": 12105912 } },
    { "query": "path:2-people/",    "color": { "a": 1, "rgb": 4508143  } },
    { "query": "path:5-maps/",      "color": { "a": 1, "rgb": 902793   } },
    { "query": "path:8-questions/", "color": { "a": 1, "rgb": 15680580 } }
  ]
}
```

## Notes / historique

- 2026-05-08 : création du preset comme variante de [[focus-people-maps-questions]] à la demande de l'utilisateur, pour réintroduire le maillage atomique en arrière-plan.
- 2026-05-10 : ajout exclusion `-["status":"answered"]` pour cacher les Questions résolues (signal mort), à la demande de l'utilisateur.

## Pour activer

```bash
bash _meta/graph-presets/swap.sh focus-people-maps-questions-atoms
```

Puis Cmd+R dans Obsidian.
