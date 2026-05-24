---
type: meta
purpose: doctrine fondatrice du vault, V1
version: v1
status: stable
frozen_at: 2026-04-29
created: 2026-04-25
last_updated: 2026-04-29
supersedes: null
---


<!--
Changelog : externalisé vers _meta/doctrine-changelog.md (consulté à la demande).
Doctrine V1 anonymisée, packagée comme produit SAMPL-IQ.
-->

> **Note de lecture** : ce fichier décrit la philosophie source du vault et les schemas par type. L'**index opérationnel** des fichiers `_meta/` (qui contient quoi, dans quel ordre lire selon la tâche) vit dans [[README]]. Si tu cherches "où trouver le workflow de capture / triage / session / transcripts-import / journaling / grill", va dans `_meta/README.md`, pas ici. Ce fichier est la doctrine source longue, le README est la table des matières.

> **Statut de la doctrine V1 : stable depuis 2026-04-29.** Les 8 types, leurs schemas YAML, les conventions de nommage et l'architecture des dossiers sont **figés**. Toute évolution doit passer par [[doctrine-roadmap]] avec un trigger explicite (et l'accord de l'utilisateur), ou être un patch de bug remontable à une incohérence avérée. Pas d'ajout / retrait de champ YAML, pas de renommage de type, pas de nouveau type, pas de fusion de dossier en cours de session de triage / capture / sessions. L'état du **contenu** (compteurs, hubs, zones sous-représentées) vit dans [[vault-state]] et reste, lui, en mouvement permanent.

### Doctrine générale sur le fonctionnement du Vault dans Obsidian

**Une note = un objet. Les relations sont des liens, pas des dossiers.**

Tu n'as pas besoin d'un dossier `cadeaux/`. Tu as une note `[[Sam]]` (People) qui contient une section "Idées cadeau" avec des liens vers des Atoms. Le jour de son anniversaire, tu ouvres `[[Sam]]`, tu vois tout.

Tu n'as pas besoin d'un dossier `philosophie/`. Tu as une **Map** `[[Absurde]]` qui liste les Atoms pertinents, les Sources qui les ont inspirés, et les People avec qui tu en as discuté. Tu ouvres la Map, tu as toute ta pensée sur le sujet en un endroit, sans avoir eu à pré-décider qu'elle vivait là.

Tu n'as pas besoin d'un dossier `permaculture/`. Tu as une **Map** `[[Permaculture]]` avec des Atoms (règles compagnonnage, observations terrain), des Sources (livres, vidéos), et des People (qui t'a appris quoi).

### Pourquoi ça marche pour ton problème spécifique

Tu m'as dit deux choses critiques :

1. **Les sujets se croisent** ("il y a un lien avec tout ça")
2. **La liste va grandir énormément**

Avec une archi par dossiers thématiques, le croisement = duplication ou choix arbitraire ("je mets ce texte de rap dans `creative/` ou dans `relations/sam/`?"), et l'ajout d'un domaine = restructuration globale.

Avec une archi par **types d'objets + liens** :

- Le croisement est natif. Une note a autant de liens qu'elle veut. Pas de choix arbitraire.
- L'ajout d'un domaine ne casse rien. Tu crées une nouvelle Map (`[[Échecs]]`), elle commence vide, elle se remplit organiquement.

C'est exactement la différence entre une **base de données relationnelle** (tables = types, foreign keys = liens) et un **système de fichiers hiérarchique**. Tu connais bien le premier mode via Notion. Obsidian fait pareil, en local, avec markdown plat.

### Architecture de dossiers concrète

Très simple, alignée sur les 8 types :

```
~/Documents/<VotreVault>/
├── 0-inbox/              ← capture brute (input agent V1)
├── 1-atoms/              ← idées, citations, règles, datas
├── 2-people/             ← un fichier par personne
├── 3-sources/            ← livres, articles, podcasts
├── 4-projects/           ← projets bornés dans le temps
├── 5-maps/               ← notes d'index par domaine
├── 6-logs/
│   ├── journal/          ← entrées datées (YYYY-MM-DD.md)
│   └── events/           ← événements ponctuels (conflit, décision, voyage)
├── 7-intentions/         ← engagements personnels sans deadline (lire, apprendre, vivre)
├── 8-questions/         ← interrogations ouvertes sans réponse, à creuser plus tard
└── _meta/
    ├── templates/        ← templates pour chaque type
    └── README.md         ← doctrine du vault (la tienne)
```

Note : les préfixes numériques `0-`, `1-`, etc. sont juste pour ordonner visuellement dans la sidebar Obsidian. Aucune autre fonction.

### Convention de nommage

|Type|Format|Exemple|
|---|---|---|
|Atom|`<slug-court>.md`|`anthropic-70-pct-code-claude.md`|
|People|`<prenom-nom>.md`|`sam-doe.md`|
|Source|`<auteur>-<titre-court>.md`|`sequoia-services-as-new-software.md`|
|Project|`<verbe>-<sujet>-<année>.md`|`apprendre-blackjack-2026.md`|
|Map|`<domaine>.md`|`permaculture.md`, `absurde.md`|
|Log journal|`YYYY-MM-DD.md`|`2026-04-25.md`|
|Log event|`YYYY-MM-DD-<slug>.md`|`2026-03-12-conflit-x.md`|
|Intention|`<verbe>-<sujet>.md`|`lire-cyberpunk-william-gibson.md`|
|Question|`<slug-interrogatif>.md`|`comment-acme-survit-si-commoditisation-ia.md`|

Slug toujours en kebab-case, sans accents, ≤ 50 chars.

### Frontmatter par type (le squelette du système)

C'est ici que la magie opère. Chaque type a un schema YAML distinct → un LLM peut filtrer ton vault sans rien lire ("donne-moi tous les Atoms taggés `#acme` créés ce mois", "liste mes People avec qui j'ai discuté de philosophie").

**Atom**

yaml

```yaml
---
type: atom
created: YYYY-MM-DD
subtype: idea | quote | data | rule | mnemonic | creative
tags: [acme, ai, etf, ...]
people: [[sam-doe]]   # personnes liées
source: [[sequoia-services]] # source si applicable
maps: [[absurde]]          # maps auxquelles ce atom appartient
confidence: high | medium | low
---
```

**People**

yaml

```yaml
---
type: people
relation: family | friend | partner | team | colleague | client | prospect | mentor | contact | acquaintance
context: work | personal | both
last_seen: YYYY-MM-DD | null
birthday: MM-DD | null
birthday_year: YYYY | null
death_date: YYYY-MM-DD | null
anniversary_with_user: MM-DD | null
location_current: <string> | null
location_origin: <string> | null
related_people: [[...]] | []
met_through: [[...]] | []
tags: [...]
---
```

Pour le détail (sémantique de chaque champ, glose des nouveaux champs ajoutés
en avril 2026), voir [[conventions]] section `### People`.

**Source**

yaml

```yaml
---
type: source
medium: book | article | podcast | video | conversation
author: <name>
date_consumed: YYYY-MM-DD
status: to-read | reading | read | abandoned
rating: 1-5
tags: [...]
---
```

**Project**

yaml

```yaml
---
type: project
status: active | paused | done | abandoned
started: YYYY-MM-DD
deadline: YYYY-MM-DD | null
context: work | personal | both
tags: [...]
---
```

**Map**

yaml

```yaml
---
type: map
domain: <single-word>
maturity: stub | growing | mature
last_updated: YYYY-MM-DD
---
```

**Log**

yaml

```yaml
---
type: log
subtype: journal | event | decision
date: YYYY-MM-DD
people: [[...]]
projects: [[...]]
mood: optional
---
```

**Intention**

Une chose que je me promets d'envisager, faire, lire, vivre, ou décider à un horizon flou (semaines, mois, années). Cible sans deadline. Mouvement vers un futur état, à différencier d'un Atom (pensée stable) et d'un Project (exécution déjà décidée et bornée).

yaml

```yaml
---
type: intention
created: YYYY-MM-DD
category: read | watch | learn | meet | do | decide | create | explore | other
status: active | realized | abandoned | dormant
horizon: weeks | months | years | someday
priority: high | medium | low | null
people: [[...]]
sources: [[...]]
maps: [[...]]
realized_at: YYYY-MM-DD | null
abandoned_at: YYYY-MM-DD | null
abandoned_reason: <string> | null
---
```

**Question**

Une interrogation ouverte que je me pose sans avoir le temps ou l'envie de la résoudre sur le moment. Trou productif dans la réflexion, à creuser plus tard dans des moments réflexifs. Statique en soi : appelle à une réflexion, pas à une action (différent d'une Intention) ni à une exécution (différent d'un Project). Différent aussi d'un Atom : la note CHERCHE plutôt qu'elle AFFIRME.

yaml

```yaml
---
type: question
asked: YYYY-MM-DD
status: open | partial | answered | abandoned
domain: business | philosophy | finance | personal | other
priority: high | medium | low | null
people: [[...]]
maps: [[...]]
sources: [[...]]
related_atoms: [[...]]
answered_at: YYYY-MM-DD | null
abandoned_at: YYYY-MM-DD | null
---
```

### Sur le doublon Notion / Obsidian

Tu m'as soulevé la bonne question. Ma règle, à challenger :

|Origine de la pensée|Vit dans|Si dérivé pro|
|---|---|---|
|Lecture, idée, capture brute|Obsidian (Atom)|n/a|
|Réflexion philosophique, vision|Obsidian (Atom + Map)|n/a|
|Insight perso → process Acme|Obsidian capture, **puis** Notion process|Notion = transformation, pas copie|
|Décision personnelle|Obsidian (Log)|n/a|
|Décision Acme|Notion direct|n/a|
|People perso (Robin, Sam, Nina)|Obsidian|n/a|
|People client/équipe Acme|Notion CRM/équipe|Pas de doublon|
|People à cheval (Victor)|Obsidian côté humain, Notion côté COO|Distinction claire|

**Règle générale** : Obsidian est **émetteur**, Notion est **opérationnel**. Quand une réflexion perso devient un process à exécuter en équipe, elle migre vers Notion (transformée pour l'audience), et la note Obsidian originale garde une référence (`source_pro: notion://...`).

### Le rituel de fermeture adapté à ton vault

Le gars Instagram avait une bonne intuition mais ses 3 questions sont taillées pour du dev. Pour un second brain perso, je te propose 4 questions, 5 minutes, en fin de semaine (pas chaque session, ce serait insoutenable) :

1. **Capté** : Quelles notes ai-je créées cette semaine en `inbox/` ? Lesquelles je classe maintenant en Atom/Source/Log, lesquelles je supprime ?
2. **Connecté** : Quelles notes méritent un lien vers une Map ou une People que j'ai oublié de mettre ?
3. **Cristallisé** : Y a-t-il une réflexion récurrente cette semaine qui mérite de devenir une Map (nouveau domaine) ou de structurer une Map existante ?
4. **Cleané** : Y a-t-il une note doublon, périmée, ou qui devrait migrer vers Notion ?


### Méta-documentation
Ne va pas dans `1-atoms/`. Ça va dans `_meta/` (le dossier qui contient les règles du jeu, justement). `_meta/` est réservé strictement à la doctrine : aucun contenu (atom, source, log, etc.) ne doit y vivre, et aucun nouveau dossier ne doit y être créé sans entrée explicite dans cette table et validation l'utilisateur.

L'index opérationnel canonique de `_meta/` vit dans [[README]]. Cette table est le miroir doctrinal de cet index, à garder synchronisé. Quand un fichier est ajouté à `_meta/`, il doit être ajouté ici ET dans `_meta/README.md` dans le même commit.

#### Inventaire complet de `_meta/`

| Fichier | Rôle | Quand le lire |
|---|---|---|
| `_meta/README.md` | Index canonique des fichiers `_meta/` (doctrine-friendly, lisible humain) | Premier réflexe quand tu arrives dans `_meta/` sans savoir où chercher |
| `_meta/vault-doctrine-v1.md` | Doctrine source longue : philosophie, 8 types, schemas YAML, archi dossiers (ce fichier) | Pour comprendre POURQUOI le vault est structuré ainsi |
| `_meta/conventions.md` | Conventions de nommage et schemas frontmatter détaillés par type | Pour créer ou modifier une note typée correctement |
| `_meta/doctrine-roadmap.md` | Roadmap d'évolution doctrinale (trous structurels identifiés, triggers d'activation) | Avant de proposer un nouveau type ou une refonte structurelle |
| `_meta/identite-civile.md` | Facts civils objectifs sur l'utilisateur (état civil, géographie, structures pro, cercle proche) | En début de session pour résoudre les références People sans inventer |
| `_meta/capture-criteria.md` | Workflow self-contained de capture inbox (skill `obsidian-capture` pointe ici) | Quand l'utilisateur veut capturer une note brute |
| `_meta/triage-criteria.md` | Workflow self-contained de triage inbox (skill `obsidian-triage` pointe ici) | Quand l'utilisateur veut classer son inbox |
| `_meta/sessions-criteria.md` | Workflow self-contained des sessions de travail (8 portes d'entrée, free roam, Source conversation en sortie de session longue) | Quand l'utilisateur lance une session enrichissante (people, question, map, etc.) |
| `_meta/transcripts-import-criteria.md` | Workflow self-contained d'import d'un transcript de call, quel que soit l'outil (skill `obsidian-transcripts-to-inbox` pointe ici) | Quand l'utilisateur fournit un transcript de call |
| `_meta/journaling-criteria.md` | Workflow self-contained du rituel journal-daily (détecté par triage-criteria §0) | Quand une note inbox est candidate journal-daily |
| `_meta/lifecycle-criteria.md` | Checklist clôture aval (intentions consommables, Maps maturity, People last_seen, Map manquante). Déroulée au triage et en fin de session. | Toute opération de triage ou de session, avant commit final |
| `_meta/grill-criteria.md` | Workflow self-contained du grill-me (interview stress-test) | Quand l'utilisateur demande un grill-me |
| `_meta/toilettage-rules.md` | Règles de nettoyage du texte (référencé depuis `capture-criteria.md`) | Lu par l'agent de capture, pas en standalone |
| `_meta/rituals.md` | Rituel de fermeture hebdo (4 questions, 5 minutes) | En fin de semaine pour la passe de cleanup |
| `_meta/vault-state.md` | Dashboard dynamique de maturité du vault (compteurs, hubs, zones sous-représentées, recommandations next-session) | En début de session pour s'orienter ; mis à jour en fin de session |
| `_meta/vault-state-log.md` | Log append-only des sessions et clusters, externalisé depuis vault-state §9 au patch doctrine 2026-05-16 (rolling 14 jours) | **NE PAS charger en cold-start.** À la demande uniquement (retracer une décision, vérifier qu'une Map est recommandée depuis ≥3 sessions, comprendre le contexte d'évolution d'un objet) |
| `_meta/doctrine-changelog.md` | Historique append-only des évolutions de la doctrine `_meta/*.md`, externalisé depuis les commentaires HTML en tête de chaque fichier au patch doctrine 2026-05-16 | **NE PAS charger en cold-start.** À la demande uniquement (retracer l'historique complet d'une règle, comprendre pourquoi elle a été modifiée). Chaque fichier doctrine conserve dans son commentaire HTML uniquement les 3 dernières entrées + un pointeur vers ce fichier |
| `_meta/templates/*.md` | Un template par type, à dupliquer pour créer une nouvelle note | Quand l'agent crée une note typée et veut la base canonique |
| `_meta/scripts/lifecycle-lint.py` | Audit lecture-seule du vault qui produit une note inbox `device: lifecycle-audit` (5 catégories de dérives détectées) à consommer au prochain triage | Avant le rituel hebdo, ou après un sprint de captures intenses, pour rattraper les dérives accumulées que la doctrine de flux n'a pas attrapées |
| `_meta/scripts/README.md` | Documentation du dossier scripts (usage, output, limitations) | Avant de lancer un script |

#### Cas particuliers (notes liées à la doctrine mais hors `_meta/`)

| Élément | Type | Emplacement |
|---|---|---|
| Le projet de bootstrap initial | Project | `4-projects/bootstrap-second-brain-2026.md` |
| La conversation Claude qui a accouché de la doctrine V1 | Source | `3-sources/2026-04-25-conversation-claude-doctrine-vault.md` |
|**Idées spécifiques que tu retiens de la conversation**|Atoms (plusieurs, pas un seul)|`1-atoms/*.md`|
