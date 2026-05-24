---
type: meta
purpose: système de presets Graph View Obsidian, swappables depuis terminal sans toucher l'UI
version: v1
status: active
created: 2026-05-08
last_updated: 2026-05-08
---

# Graph view presets

Configs de Graph View Obsidian stockées en JSON, swappables en une commande terminal. Versionné git, voyage avec le vault, accessible dans n'importe quelle session future (toi ou agent IA).

## Doctrine de visualisation

- Le graphe Obsidian est un outil de **navigation et de diagnostic**, pas de la déco. Les couleurs portent du sens sémantique (Maps = vert structurel, People = rouge humain, Sources = violet input externe, etc.). Pas de palette arbitraire ni de skin esthétique au goût du jour.
- Les nodes `_meta/` sont **cachés par défaut** dans tous les presets de production. La doctrine technique ne doit pas parasiter la lecture du contenu.
- Les **paramètres physiques** (zoom `scale`, écartement `linkDistance`, force `repelStrength`, etc.) sont **orthogonaux** aux palettes et aux filtres. Le swap de preset ne les touche pas, ils restent calibrés à ce que tu as réglé manuellement dans l'UI Obsidian.
- Un preset = un **point de vue stable**. Pas une exploration libre. Si tu veux explorer ad hoc, fais-le dans l'UI Obsidian sans toucher aux presets. Quand le point de vue est validé et stable, on l'enregistre comme preset.

## Baseline = `macro`

`macro` est la **vue par défaut**, à laquelle on revient quand il n'y a pas de focus particulier. Elle expose tout le contenu typé du vault avec la palette complète par type.

Tout nouveau preset hérite mentalement de macro :
- On **filtre / sélectionne** dans la palette de référence ci-dessous, on n'invente pas une nouvelle palette ad hoc.
- Si une couleur de référence ne convient pas pour un preset spécifique (ex. besoin de plus de contraste sur un cluster de 2 dossiers), le justifier en commentaire dans le JSON du preset.
- **Ne pas modifier `macro` sans validation explicite de l'utilisateur** : c'est la baseline partagée. Toute évolution = nouveau preset à côté, pas modification de macro.

## Pour un agent IA qui démarre de zéro

Si l'utilisateur demande "passe en config X", "crée une nouvelle vue Y", ou "ajuste la palette de Z" :

1. Lis ce README en entier.
2. Liste les presets existants : `ls _meta/graph-presets/presets/`.
3. **Si le preset demandé existe** : `bash _meta/graph-presets/swap.sh <nom>`. Signale le rechargement Cmd+R à l'utilisateur.
4. **Si le preset n'existe pas** : propose un draft (search query + colorGroups en t'appuyant sur la palette de référence) AVANT de créer le fichier. Validation explicite de l'utilisateur requise. Une fois validé, crée le fichier dans `presets/`, swap, signale Cmd+R.
5. **Si l'utilisateur demande de modifier `macro`** : c'est la baseline partagée. Demande validation explicite avant de toucher. Préfère proposer un nouveau preset à côté plutôt que modifier macro.
6. **Ne JAMAIS inventer de couleurs hors palette** sans validation. Si une couleur supplémentaire est nécessaire (ex. preset avec 10 catégories alors que la palette en a 9), demande à l'utilisateur d'arbitrer.
7. Tout commit lié à graph-presets utilise le pattern `📐 doctrine: ...`.

## Usage

```bash
# Lister les presets disponibles + voir l'actif
bash _meta/graph-presets/swap.sh

# Appliquer un preset
bash _meta/graph-presets/swap.sh macro
bash _meta/graph-presets/swap.sh focus-people-maps
```

Après le swap, **reload Obsidian (Cmd+R)** pour voir l'effet.

## Comment ça marche

Le swap merge le preset dans `.obsidian/graph.json` :

- **Écrasé par le preset** : `search`, `colorGroups`, `showTags`, `showAttachments`, `hideUnresolved`, `showOrphans`
- **Préservé depuis ton état actuel** : `scale`, `linkDistance`, `centerStrength`, `repelStrength`, `linkStrength`, `textFadeMultiplier`, `nodeSizeMultiplier`, `lineSizeMultiplier`

Donc ta navigation physique (zoom, écartement) ne saute pas quand tu changes de palette.

Backup auto à chaque swap → `.obsidian/graph.json.bak`.

## Structure du dossier

```
_meta/graph-presets/
├── README.md         ← ce fichier
├── swap.sh           ← script de bascule
├── current.txt       ← preset actuellement appliqué (info)
└── presets/
    ├── macro.json
    └── ... (extensible)
```

## Schéma d'un preset

Un preset JSON contient uniquement les champs filtres/couleurs :

```json
{
  "search": "-path:_meta/",
  "showTags": false,
  "showAttachments": false,
  "hideUnresolved": true,
  "showOrphans": false,
  "colorGroups": [
    { "query": "path:5-maps/", "color": { "a": 1, "rgb": 1096065 } }
  ]
}
```

- `search` : query de filtre global (cache des nodes). Syntaxe Obsidian : `path:`, `-path:`, `tag:`, `OR`, `AND`, parenthèses.
- `colorGroups` : liste ordonnée. Premier match gagne. `query` = même syntaxe que `search`. `color.rgb` = entier décimal (hex sans `#` converti : `RR*65536 + GG*256 + BB`).

## Palette de référence (Tailwind 500)

| Type         | Hex     | Couleur       | Décimal  | Sémantique                      |
| ------------ | ------- | ------------- | -------- | ------------------------------- |
| 1-atoms      | #B8B8B8 | gris clair    | 12105912 | briques de connaissance         |
| 2-people     | #44C9EF | cyan          | 4508143  | relations humaines              |
| 3-sources    | #8B5CF6 | violet        | 9133302  | input externe (calls, lectures) |
| 4-projects   | #FED100 | jaune         | 16699648 | action structurée               |
| 5-maps       | #0DC689 | vert émeraude | 902793   | hubs structurels                |
| 6-logs       | #9A9A9A | gris          | 10132122 | chronologie                     |
| 7-intentions | #F97316 | orange        | 16347926 | engagement futur                |
| 8-questions  | #EF4444 | rouge         | 15680580 | questions ouvertes              |
| 0-inbox      | #7CB1E7 | bleu pâle     | 8172007  | backlog (visible mais discret)  |

Conversion hex → décimal :
```bash
printf "%d\n" 0xF59E0B
```

## Créer un nouveau preset

Procédure :

1. Copier un preset existant comme base :
   ```bash
   cp _meta/graph-presets/presets/macro.json \
      _meta/graph-presets/presets/focus-X.json
   cp _meta/graph-presets/presets/macro.md \
      _meta/graph-presets/presets/focus-X.md
   ```
2. Éditer `focus-X.json` (filtre `search`, `colorGroups`).
3. Éditer `focus-X.md` (objectif, filtre, tableau couleurs, JSON inline copié du `.json`, notes).
4. Ajouter une ligne dans le tableau "Catalogue des presets" du README.
5. Tester : `bash _meta/graph-presets/swap.sh focus-X` puis Cmd+R Obsidian.
6. Commit unique : `🎨 graph-presets: nouveau preset focus-X` ou `📐 doctrine: ...` si la modif touche aussi la doctrine.

### Démarrer depuis l'état UI actuel (configuré via Settings → Graph view dans Obsidian)

Si tu as bricolé la vue dans l'UI Obsidian et veux la sauver :

```bash
# Extraction du JSON depuis l'état actif
jq '{search, colorGroups, showTags, showAttachments, hideUnresolved, showOrphans}' \
   .obsidian/graph.json \
   > _meta/graph-presets/presets/<nom>.json

# Puis créer la fiche markdown manuellement à partir du .json
# en utilisant macro.md ou focus-people-maps-questions.md comme template
```

## Pré-requis

- `jq` installé : `brew install jq`
- `.obsidian/graph.json` existe (créé automatiquement par Obsidian au premier ouverture du Graph View)

## Versionnement

Tout est versionné git :
- `presets/*.json` → fichiers d'exécution (lus par swap.sh)
- `presets/*.md` → fiches humaines lisibles dans Obsidian
- `swap.sh` → le script
- `README.md` → cette doctrine + catalogue
- `current.txt` → preset actif (info)

`.obsidian/graph.json` lui-même est aussi versionné (pas dans `.gitignore`), donc l'état actif voyage avec le repo.

## Catalogue des presets

Chaque preset = paire de fichiers dans `presets/` :
- `<nom>.md` → fiche humaine lisible dans Obsidian (objectif, filtre, couleurs, JSON, historique)
- `<nom>.json` → fichier d'exécution lu par `swap.sh`

**Discipline** : à chaque création ou modification d'un preset, les deux fichiers (`.md` et `.json`) sont touchés ensemble dans le même commit. Le `.md` est la source de vérité humaine, le `.json` est l'artefact d'exécution.

| Preset | Fiche | Description courte |
|---|---|---|
| macro | [[macro]] | vue d'ensemble baseline, palette complète par type |
| meta | [[meta]] | vue exhaustive sans filtre, macro + doctrine `_meta/` en slate foncé |
| focus-people-maps-questions | [[focus-people-maps-questions]] | squelette de réflexion humaine et structurelle (cyan/vert/rouge) |
| focus-people-maps-questions-atoms | [[focus-people-maps-questions-atoms]] | variante de focus-people-maps-questions avec atoms en gris neutre (maillage de connaissance) |
