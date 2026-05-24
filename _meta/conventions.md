---
type: meta
purpose: conventions-technical
version: v1
last_updated: 2026-05-10
---

<!--
Changelog : externalisé vers _meta/doctrine-changelog.md (consulté à la demande).
Doctrine V1 anonymisée, packagée comme produit SAMPL-IQ.
-->


# Conventions

## Nommage des fichiers

Toujours kebab-case, sans accents, slug court (≤ 50 chars).

| Type | Format | Exemple |
|---|---|---|
| Atom | `<slug-court>.md` | `anthropic-70-pct-code-claude.md` |
| People | `<prenom-nom>.md` | `sam-doe.md` |
| Source | `<auteur>-<titre-court>.md` | `sequoia-services-as-new-software.md` |
| Project | `<verbe>-<sujet>-<annee>.md` | `apprendre-blackjack-2026.md` |
| Map | `<domaine>.md` | `permaculture.md` |
| Log journal | `YYYY-MM-DD.md` | `2026-04-25.md` |
| Log event | `YYYY-MM-DD-<slug>.md` | `2026-03-12-conflit-x.md` |
| Intention | `<verbe>-<sujet>.md` | `lire-cyberpunk-william-gibson.md` |
| Question | `<slug-interrogatif>.md` | `comment-acme-survit-si-commoditisation-ia.md` |

Cas particulier Intention : pas de date dans le slug (l'horizon est flou,
pas de point d'ancrage temporel utile). Le verbe d'attaque indique la
catégorie d'action (`lire-`, `apprendre-`, `scout-`, `ecrire-`, `parler-`,
etc.). Exemples : `apprendre-echecs-serieusement.md`,
`scout-albanie-investissement.md`.

Cas particulier Question : la formulation doit rester interrogative (le
slug doit se lire comme une vraie question, sans nécessiter le point
d'interrogation graphique). Exemples :
`comment-acme-survit-si-commoditisation-ia.md`,
`est-ce-que-je-veux-vraiment-retourner-en-belgique.md`,
`quelle-est-ma-vraie-these-sur-l-education.md`. Pas de date dans le slug
(la question est intemporelle, l'horizon de réponse est inconnu).

Cas particulier : pour une Source qui est une **conversation** (donc sans auteur
canonique unique), on peut préfixer par la date pour ancrer la source dans le temps :
`YYYY-MM-DD-<slug>.md`.

## Schemas frontmatter par type

Toutes les dates au format ISO `YYYY-MM-DD`. Listes YAML entre crochets,
wikilinks valides à l'intérieur (`[[slug]]`).

### Atom

```yaml
---
type: atom
created: YYYY-MM-DD
subtype: idea | quote | data | rule | mnemonic | creative
tags: [acme, ai, etf]
people: [[sam-doe]]
source: [[sequoia-services]]
maps: [[absurde]]
confidence: high | medium | low
derived_from_grill: [[YYYY-MM-DD-grill-slug]] | null
---
```

`derived_from_grill` est optionnel. Présent uniquement si l'Atom a été
produit après un grill-me ; pointe alors vers le Log de grill correspondant
(subtype `grill-event`). Voir [[grill-criteria]].

### People

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
tags: []
---
```

`relation` :
- `family` : lien familial (consanguin ou par alliance).
- `friend` : ami personnel.
- `partner` : co-fondateur shareholder Acme post-signing du partnership.
- `team` : membre équipe Acme (devs, futurs employés). Lien
  hiérarchique ou collaboratif fort.
- `colleague` : collaborateur pro hors équipe directe (à cheval, en cours
  de signing, etc.).
- `client` : client actif ou ancien.
- `prospect` : relation pro prospectée sans engagement formel (en évaluation, pitch, exploration partenariat). Devient `client` après signature.
- `mentor` : personne à qui je confère une autorité par choix (coach,
  advisor, business mentor).
- `contact` : prestataire pro fonctionnel ponctuel (avocat, comptable,
  consultant ponctuel).
- `acquaintance` : connaissance, lien faible.

`context` situe la relation dans une sphère de ta vie :

- `work` : la relation s'inscrit dans une phase professionnelle (entreprise,
  équipe, clients, prospects, partenaires, fournisseurs, conseillers).
- `personal` : relation hors sphère pro identifiable. Famille, amis, voyages,
  social, contacts hors structure pro.
- `both` : chevauchement réel pro et perso (ex. un mentor qui est aussi un
  ami, un collègue devenu proche, un associé d'enfance).

L'enum de base est `work | personal | both`. Tu peux le **spécialiser** selon
ta vie : si tu veux distinguer plusieurs phases ou structures professionnelles
(ex. remplacer `work` par `acme`, `globex`, etc. correspondant à tes sociétés
successives), c'est prévu. Procédure d'extension identique à celle de l'enum
`relation` : flag explicite, validation, mise à jour cohérente de
[[vault-doctrine-v1]], [[conventions]], et `_meta/templates/people.md`.

`last_seen` peut être `null` si la dernière interaction n'est pas datable
ou si la relation est en sommeil.

`birthday` au format `MM-DD` (mois-jour, ex. `04-26`). Permet à un agent de
rappel d'anniversaires de matcher directement la date du jour formatée pareil,
sans branchement sur la présence ou l'absence d'année.

`birthday_year` (entier YAML, ex. `1985`) quand l'année de naissance est
connue. Séparer ce champ de `birthday` évite l'ambiguïté de type YAML (un
`04-26` reste une string ; un `1985-04-26` peut être auto-parsé en Date par
certains parseurs) et représente proprement le cas fréquent "je connais le
jour mais pas l'année". Reste `null` si non connu.

`death_date` au format `YYYY-MM-DD` (date complète) quand la personne est
décédée. Permet de garder la note et ses backlinks intacts plutôt que de la
supprimer (préservation des Atoms qui la mentionnent) et d'adapter le
comportement de l'agent de rappel.

`anniversary_with_user` : date marquante de la relation avec l'utilisateur du
vault (rencontre, mariage, début d'amitié structurante), au format `MM-DD`.
Pertinent surtout pour les relations fortes (partenaire, amis proches).

`location_current` : ville et pays actuels de la personne, format libre
(ex. `"Lisbonne, Portugal"`, `"Lisbonne, Portugal"`). Permet à un agent
de répondre à "qui est à Lisbonne en ce moment ?".

`location_origin` : ville et pays d'origine, distincts de
`location_current`. Format libre.

`related_people` : liste de wikilinks vers d'autres People du vault avec un
lien direct (frère, sœur, conjoint, parents, enfants, meilleur ami).
Construit le graphe relationnel. Vide par défaut (`[]`).

`met_through` : liste de wikilinks vers la (ou les) People qui a présenté
cette personne à l'utilisateur. Permet de tracer les ponts sociaux et de
visualiser les clusters relationnels. Vide par défaut (`[]`).

Tous les champs ajoutés ci-dessus (`birthday`, `birthday_year`, `death_date`,
`anniversary_with_user`, `location_current`, `location_origin`,
`related_people`, `met_through`) sont **optionnels** dans l'usage : une note
People reste valide avec leurs valeurs par défaut (`null` ou `[]`).

### Source

```yaml
---
type: source
medium: book | article | podcast | video | conversation | creation
author: <name>
date_consumed: YYYY-MM-DD
status: to-read | reading | read | abandoned
rating: 1-5
tags: []
participants:                                         # optionnel, voir ci-dessous
  - "[[slug-people-1]]"
  - "[[slug-people-2]]"
external_link: <URL du média original>                # voir ci-dessous
---
```

`participants` : champ **optionnel**, pertinent uniquement pour `medium: conversation` (call, entretien, coaching, debrief). Liste de wikilinks vers les fiches People des participants au call. Permet à Obsidian de générer les backlinks et à un agent de retrouver toutes les Sources où une personne a participé. Pour les Sources non-conversation (book, article, podcast, video), ce champ est absent. Si un participant n'a pas encore de fiche People, ne pas inventer le wikilink, le mentionner uniquement dans la section "Participants" du corps de la note.

`external_link` : champ **optionnel mais fortement recommandé**. URL stable pointant vers le média original (l'outil de transcript pour un call, YouTube pour une vidéo, page éditeur pour un article, Audible / Goodreads pour un livre). C'est la référence durable vers le contenu source. Si la source n'a pas d'URL stable (livre papier, conversation off-record), le champ est absent ou null.

#### Doctrine "Source allégée" (contenu de la note)

Une note Source dans le vault est une **fiche de référence**, pas une archive de contenu. Elle contient :

1. Un **abstract structurant** de 200 à 500 mots : sujet central, angle ou thèse, points clés retenus, contexte de consommation. En français.
2. Le **lien vers le média original** via `external_link` ou dans une section "Lien externe" du corps.
3. Les **liens vers les notes dérivées** : Atoms extraits, People mentionnés, Maps thématiques.
4. Optionnellement, des **citations courtes** (1 à 3 phrases verbatim maximum) si elles sont structurantes.

Une note Source NE contient PAS :

- Transcript intégral d'un call (l'enregistrement source est l'archive durable).
- Retranscription complète d'une vidéo YouTube ou d'un podcast (le média original l'est).
- Texte intégral d'un article ou d'un livre (lecture en clair sur le site éditeur ou liseuse).

Motivation : à plusieurs centaines de Sources, le vault explose en volume sans gain proportionnel de signal. Le verbatim sert très rarement, et quand il sert, il vit dans le média externe (l'outil de transcript, YouTube, etc.) qui le présente bien mieux qu'un fichier markdown. Le vault capture le **signal cognitif extrait** (Atoms), pas le contenu brut consommé.

Cas particulier des transcripts existants pré-doctrine : non migrés rétroactivement par défaut. Les Sources actuelles avec transcript intégral peuvent être compressées en abstract lors d'une session de migration dédiée, mais ce n'est pas urgent : c'est la croissance future qui est cappée par cette règle, pas le legacy.

#### Cas particulier `medium: creation`

`medium: creation` désigne une œuvre personnelle de l'utilisateur (rap, écrit littéraire, dessin, projet créatif). `author` = "l'utilisateur Doe" typiquement. Slug = kebab-libre du titre, sans préfixe date (la date d'origine est souvent incertaine pour le legacy importé). `date_consumed` = date de création approximative ou d'archivage si origine inconnue ; si reconstruite à la louche, le préciser dans le body en note explicite.

**Exception explicite à la doctrine "Source allégée"** : le contenu de l'œuvre est préservé tel quel dans une section `## Texte` du body (verbatim absolu, jamais retouché, langues mixtes OK, pas de toilettage, pas de wikilinks insérés, pas de retrait d'em-dash, pas de correction orthographique). Justification : il n'existe pas de "média externe durable" pour ces œuvres legacy (pas de plateforme tierce qui les héberge), donc le vault EST l'archive.

Wikilinks et toilettage standard appliqués uniquement dans les sections d'enrobage du body (`## Contexte`, `## Notes`). Toute mention de famille / domaine Map / projet dans ces sections d'enrobage doit être wikilinkée selon la règle stricte CLAUDE.md (zéro mention nue).

### Project

```yaml
---
type: project
status: active | paused | done | abandoned
started: YYYY-MM-DD
deadline: YYYY-MM-DD | null
context: work | personal | both
tags: []
---
```

### Map

```yaml
---
type: map
domain: <kebab-case>
maturity: stub | growing | mature
last_updated: YYYY-MM-DD
---
```

`domain` accepte un mot unique (`permaculture`) ou plusieurs mots en kebab-case
(`second-brain`, `vie-pro`). Toujours en minuscules, sans accents.

### Log

```yaml
---
type: log
subtype: journal | journal-daily | event | decision | grill-event
date: YYYY-MM-DD
people: [[]]
projects: [[]]
mood: optional
---
```

`subtype` :
- `journal` : journal sporadique, format libre (introspection ponctuelle, journée riche, session marquante). Pas de cadence imposée.
- `journal-daily` : rituel journaling quotidien, frontmatter enrichi pour permettre tracking de tendances (sommeil, humeur, scores 1-6, substances, signaux pro/social). Voir cas particulier ci-dessous et [[journaling-criteria]].
- `event` : événement ponctuel marquant (altercation, conversation structurante, milestone).
- `decision` : décision documentée, contexte + raison + implication.
- `grill-event` : archive d'une session grill-me, transcript brut + champ `produced_note`. Voir cas particulier ci-dessous.

Cas particulier `subtype: grill-event` : le Log archive le transcript brut
d'une session grill-me. Champ `produced_note` obligatoire, pointant vers
la note finale issue du grill.

```yaml
---
type: log
subtype: grill-event
date: YYYY-MM-DD
produced_note: [[slug-de-la-note-finale]]
people: [[]]
projects: [[]]
mood: 
---
```

Voir [[grill-criteria]] pour l'usage complet.

Cas particulier `subtype: journal-daily` : frontmatter étendu pour le
rituel journaling matinal quotidien. Les champs supplémentaires (physio,
substances, mental, pro, social, traçabilité) sont **valides uniquement
pour ce subtype**. Le frontmatter canonique du Log (type, subtype, date,
people, projects, mood) reste présent en plus, pas en remplacement.

```yaml
---
type: log
subtype: journal-daily
date: YYYY-MM-DD              # jour de la dictée (matin J)
date_veille: YYYY-MM-DD       # J-1, auto = date - 1 jour
type_jour: work               # work | weekend | voyage | off | férié (jour J qui démarre)
type_jour_veille: work        # work | weekend | voyage | off | férié (jour J-1 documenté)
localisation:                 # Floripa | Lisbonne | <texte libre>

# Veille (J-1, journée terminée, dictée rétrospective ce matin)
sport: false                  # true | false
sport_type: []                # [box, kite, moto, trail, surf, gym, course, autre]
alcool_verres: 0              # entier
sucre_ajoute: false           # true | false
cafe_tasses: 0                # entier
drogues: null                 # null | MD | LSD | champis | cannabis | autre
nicotine: false               # true | false
fierte_veille:                # 1-6, ou null
decision_impactante: false    # true | false
friction_client: false        # true | false
friction_equipe: false        # true | false
sentiment_social:             # seul | entoure | mixte | null

# Nuit (J-1 → J, qui vient de s'écouler)
sommeil_h:                    # nombre décimal, ex: 7.5, ou null
sommeil_qualite:              # 1-6, ou null

# Matin (J, état au moment de la dictée)
energie_matin:                # 1-6, ou null
humeur:                       # 1-6, ou null
stress:                       # 1-6, ou null
focus:                        # 1-6, ou null

# Schema log canonique conservé
people: []                    # [[slug-people-1]], [[slug-people-2]]
projects: []                  # [[slug-projet-1]]
mood:                         # texte libre, ex: "lucidité, légèreté", ou null

# Traçabilité
derived_from_inbox:           # slug de la note inbox source (sans .md), null sinon

tags: [meta/journal-daily]
---
```

Règles spécifiques au subtype `journal-daily` :

- **Sémantique temporelle** : trois blocs distincts. `Veille` = datas
  finalisées de J-1 (substances, sport, fierté, frictions pro, social,
  decision). `Nuit` = sommeil J-1→J. `Matin` = état au moment de la
  dictée (énergie, humeur, stress, focus). Voir
  [[journaling-criteria]] §16 pour le rationnel complet.
- `date` = jour de la dictée (matin J). `date_veille` = J-1 calculé auto.
  Un dataview "jours où j'ai bu" doit joindre sur `date_veille`, pas sur
  `date`, pour obtenir la date calendaire réelle de la consommation.
- **Clés YAML sans accents** : `fierte_veille`, `energie_matin`,
  `sucre_ajoute`, etc. Volontaire pour éviter les surprises de parsing
  avec Dataview ou scripts Python. Les valeurs peuvent contenir des
  accents.
- **Booléens stricts** : `true` ou `false`, jamais des strings `"oui"`,
  `"non"`. Le scripting filtre proprement.
- **Échelles 1-6** (paire, sans milieu neutre) : 1 et 2 = négatif marqué,
  3 = légèrement négatif, 4 = légèrement positif, 5 et 6 = positif marqué.
  `null` accepté quand non mesuré, jamais `0`.
- `drogues` : `null` quand non mesuré ou non consommé. Si plusieurs,
  string comma-separated (ex. `"MD, cannabis"`).
- `mood` (texte libre, bloc Matin) coexiste avec `humeur` (score 1-6,
  bloc Matin) : le premier capture la couleur émotionnelle au moment T,
  le second permet le tracking.
- `derived_from_inbox` : slug (sans `.md`) de la note inbox source qui a
  déclenché la transformation, `null` pour les canaux sans inbox.
- `tags` : doit toujours contenir au moins `meta/journal-daily` pour permettre
  filtrage Dataview trivial.
- **Nommage** : `YYYY-MM-DD.md` dans `6-logs/journal/`, identique aux
  logs `subtype: journal` sporadiques. Le subtype dans le frontmatter
  distingue. La date du fichier = jour de la dictée (matin J), pas le
  jour documenté. Un seul Log journal-daily par jour (cas multi-sessions
  documentés dans [[journaling-criteria]] §11).

Voir [[journaling-criteria]] pour le workflow complet (détection,
parsing, dérivation, commit) et §16 pour la sémantique temporelle
détaillée.

### Intention

```yaml
---
type: intention
created: YYYY-MM-DD
category: read | watch | learn | meet | do | decide | create | explore | other
status: active | realized | abandoned | dormant
horizon: weeks | months | years | someday
priority: high | medium | low | null
people: [[]]
sources: [[]]
maps: [[]]
realized_at: 
abandoned_at: 
abandoned_reason: 
---
```

`status` :
- `active` : toujours dans le radar
- `realized` : accomplie (renseigner `realized_at`)
- `abandoned` : explicitement écartée (renseigner `abandoned_at` et `abandoned_reason`)
- `dormant` : mise en pause sans abandon (à reprendre plus tard)

`horizon` est flou par construction. `someday` = pas de pression temporelle
même implicite (différent de `years`, qui suppose un échéancier large).

`priority` reste optionnel. Laisser à `null` quand pas tranché.

`people`, `sources`, `maps` permettent de connecter l'intention au reste
du graphe (la personne qui l'a inspirée, la source qui l'a déclenchée, le
domaine auquel elle appartient).

### Question

```yaml
---
type: question
asked: YYYY-MM-DD
status: open | partial | answered | abandoned
domain: business | philosophy | finance | personal | other
priority: high | medium | low | null
people: [[]]
maps: [[]]
sources: [[]]
related_atoms: [[]]
answered_at: 
abandoned_at: 
---
```

`status` :
- `open` : interrogation en cours, non résolue.
- `partial` : une réponse partielle commence à émerger.
- `answered` : résolue (renseigner `answered_at`).
- `abandoned` : jugée non pertinente (renseigner `abandoned_at`).

`domain` désigne un grand domaine de vie. `business` (et non `acme`) :
plus durable sémantiquement (`acme` est un nom propre, `business` est un
domaine de vie). Le lien spécifique à Acme se fait via `maps` ou
`people`, pas via le `domain`.

`priority` reste optionnel. Laisser à `null` quand pas tranché.

`sources` capture les Sources externes qui ont déclenché la question ou qui
aideront à y répondre. Le champ est obligatoire dans le schema (cohérent
avec Atom et Intention) mais optionnel dans l'usage : peut rester `[[]]`
vide.

`related_atoms` capture les Atoms qui touchent au territoire de la question
(réponses partielles, hypothèses formalisées, fragments de pensée).

## Règles de cohérence YAML

- Pas de virgule manquante dans les listes inline.
- Wikilinks dans les champs `people`, `source`, `maps`, `projects` : toujours
  via `[[slug-exact]]`, jamais le titre humain.
- **Listes de wikilinks à plusieurs entrées** : notation block obligatoire
  (`-` puis `"[[slug]]"` entre guillemets, un par ligne). La forme inline
  ❌ `people: [[a]], [[b]]` casse le parser YAML (virgule hors crochet
  invalide) et fait apparaître le frontmatter en rouge dans Obsidian. Une
  seule entrée : `people: "[[slug]]"` ou notation block, au choix.
- Champs vides : laisser le champ avec une valeur vide ou liste vide `[]`,
  ne pas le supprimer (un LLM filtre par schema, pas par présence).

## Hiérarchie des tags

Les tags du vault suivent une nomenclature **hiérarchique à 2 niveaux** : `racine/sous-tag`. Le séparateur est `/`. Pas de 3ème niveau autorisé en V1, même pour les racines très denses (sous une racine saturée, on multiplie les sous-tags plats plutôt que de créer un sous-niveau).

Cette nomenclature a été introduite le 2026-04-29 dans le cadre du Volet C de l'audit de scalabilité (voir `_meta/vault-state.md` §13). Avant ce chantier, les tags étaient plats et la mer de tags distincts saturait à 366 pour 262 notes.

### Format

- Une racine seule est autorisée (`acme`, `famille`) quand le tag s'applique à la racine entière sans sous-domaine pertinent.
- Un sous-tag est toujours sous une racine, jamais isolé (`acme/pricing` oui, `pricing` seul non).
- Slug du sous-tag : kebab-case, ASCII, ≤30 caractères.

### Racines actuelles (état évolutif au 2026-04-29)

État du vault au 2026-04-29. **Cette liste est évolutive** : de nouveaux domaines de vie (politique, écologie, éthique appliquée, créativité, etc.) peuvent justifier de nouvelles racines au fil de la croissance du vault. Le gel V1 (2026-04-29) fige la **grammaire** (8 types, schemas frontmatter, nomenclature 2 niveaux), pas le **vocabulaire** (liste des racines en circulation). Procédure d'ajout d'une racine : voir `[[tag-hygiene-criteria]]` §5 (flag explicite à l'utilisateur, mise à jour de 3 fichiers, pas de passage par `doctrine-roadmap.md`).

| Racine (exemple) | Périmètre |
|---|---|
| `<entreprise>` | Une de tes structures pro (clients, produits, positionnement, gouvernance interne). Crée une racine par société structurante, ex. `acme`, `globex`. |
| `famille` | Famille élargie, fratrie, transmission, dynamiques. Sous-tags par branche. |
| `finance` | Patrimoine, allocation, immobilier, stratégie financière personnelle. |
| `sante` | Hygiène de vie, sport, sommeil, nutrition, médical. |
| `geo` | Lieux, géographie, nomadisme, pays liés à ta vie. |
| `culture` | Musique, lectures, arts, références culturelles consommées. |
| `philosophie` | Pensée existentielle, métaphysique, éthique, posture face au monde. Champ d'idées, distinct de `posture` qui est personnel. |
| `tech` | Stack technique, dev, langages, outils, IA générative. L'IA y vit comme sous-tag (`tech/ia`), sous-domaine technique parmi d'autres. |
| `vault` | Doctrine, structure, méta-réflexion sur le second brain lui-même. |
| `posture` | Patterns comportementaux personnels, valeurs, vision, mode de fonctionnement (distinct de `philosophie` qui est le champ d'idées). |
| `creativite` | Production créative personnelle (écriture, dessin, musique produite). Distinct de `culture` qui est consommation. |
| `meta` | Marqueurs transversaux non-domaine. Sous-tags documentés ci-dessous §"Tags transversaux". |

Procédure opérationnelle de pose de tags (checklist de validation, cas hors-périmètre racine, ajout d'une racine) dans `[[tag-hygiene-criteria]]`. Snapshot d'utilisation effective dans `[[vault-state]]` §13.

### Tags transversaux

Les marqueurs non-domaine (statuts, qualifications, types d'événements, traçabilité d'imports, perspectives sourcées par une People) vivent sous la racine `meta/` :

**Statuts et qualifications de note** :

- `meta/needs-enrichment` : la note est un stub à enrichir.
- `meta/needs-validation` : la note contient un fait ou une hypothèse à valider avec l'utilisateur ou une source externe (donnée généalogique, citation, attribution).
- `meta/decision` : la note documente une décision.
- `meta/vigilance` : point de vigilance, alerte, risque identifié.
- `meta/silence-question` : la note pose une question dont l'absence de réponse est elle-même un signal cognitif (silence radio, non-réponse, esquive).
- `meta/no-photo` : fiche People sans photo disponible (signal pour les imports d'arbres généalogiques ou les fiches stub à compléter visuellement).
- `meta/prive` : note à diffusion restreinte, contenu sensible.

**Traçabilité d'origine d'import** (orthogonal au champ `source:`, signale la chaîne d'import qui a produit la note) :

- `meta/call` : la note dérive d'un call (transcript de conversation enregistrée, quel que soit l'outil). Voir `[[transcripts-import-criteria]]`.
- `meta/youtube` : la note dérive d'un import de vidéo YouTube. Voir `[[youtube-import-criteria]]`.
- `meta/journal-daily` : la note est une entrée de journal quotidien (porte d'entrée journaling).

**Perspective sourcée** (pattern `meta/perspective-<prenom>`, extensible) :

- `meta/perspective-<prenom>` : la note reflète la perspective d'une personne précise (typiquement une mémoire vivante d'une branche familiale, ex. `meta/perspective-anna`). Pose un disclaimer implicite : la lecture est sourcée par cette personne, à recroiser avant action structurelle.
- Pattern extensible à toute People mémoire-source (`meta/perspective-<prenom>`) sans nouvelle doctrine. Garde-fou : utiliser seulement quand la perspective de la personne est structurellement orientée et qu'un futur recroisement est nécessaire, pas pour toute mention.

### Marqueurs temporels

Les tags datés (ex. `profil-consolide-2026-04-25`) sont **interdits**. L'information de date vit déjà dans les frontmatter (`created`, `date_consumed`, `last_updated`). Si un snapshot daté doit être marqué, utiliser un fichier dédié (note Log par exemple), pas un tag.

### Politique long-tail

Un tag à 1 occurrence sans match clair vers une racine est **droppé** au lieu d'être préservé en orphelin. Justification : l'information de classement reste retrouvable via fulltext et wikilinks, et un re-tagging propre pourra émerger plus tard si une racine pertinente apparaît. Mieux vaut un index propre qu'un index complet et bruité.

### Granularité maximale

Un sous-tag doit avoir au moins 2 occurrences pour mériter son existence (ou être un terme déjà cité dans un texte stratégique du vault). Sinon, il est mergé dans un sous-tag plus large ou supprimé. Cette règle se vérifie en fin de session de triage : si une note pousse un sous-tag à 1 occurrence, l'agent propose la fusion.

### Règle d'extension du vocabulaire

L'ajout d'une racine n'est **pas** une modification structurelle de la doctrine V1 (qui fige la grammaire : 8 types, schemas frontmatter, nomenclature 2 niveaux). C'est une extension de **vocabulaire**, et le vocabulaire est explicitement évolutif.

Procédure dans `[[tag-hygiene-criteria]]` §5 : flag explicite à l'utilisateur avec mini-pitch (nom, périmètre, exemples, racine voisine), validation, puis mise à jour cohérente de 3 fichiers (ce tableau ci-dessus dans `conventions.md`, `[[vault-state]]` §13 distribution, `[[tag-hygiene-criteria]]` §2 tableau opérationnel). Pas de passage par `_meta/doctrine-roadmap.md` (réservé aux modifications structurelles).

## Cas spécial : fichier `_meta/identite-civile.md`

Le fichier `_meta/identite-civile.md` est un cas spécial dans `_meta/`. Il ne
contient pas de règles du système, mais des facts civils objectifs sur
l'utilisateur du vault, destinés à être lus par les agents IA en début de
session pour contextualisation opérationnelle.

Règles strictes :

- Ne contient QUE des facts civils objectifs (état civil, géographie,
  structures juridiques, cercle proche immédiat).
- Ne contient JAMAIS de contenu cognitif : philosophie, patterns
  comportementaux, valeurs, vision stratégique.
- Reste court (moins de 50 lignes hors frontmatter). Test décisif : si en
  l'ouvrant on apprend quelque chose d'intéressant sur qui est l'utilisateur
  cognitivement, c'est qu'il contient trop. C'est l'inverse d'une Map
  réussie.
- Les agents lisent ce fichier pour CONTEXTUALISER, pas pour répondre à des
  questions cognitives. Pour ça, ils consultent les Maps dans `5-maps/`.

Mise à jour : à chaque évolution structurelle (déménagement, nouvelle
structure juridique, changement état civil, évolution du cercle proche),
pas en continu. Mettre à jour `last_validated_by_user` à chaque relecture
explicite par l'utilisateur.

### Wikilink `[[john-doe]]` : lien rouge volontaire

La fiche `2-people/john-doe.md` n'existe pas et **ne doit pas être créée**. Le vault entier est la fiche cognitive de l'utilisateur : créer une note auto-référentielle au format People serait redondant et confondrait l'objet (utilisateur du vault) avec un sujet (People observée par l'utilisateur).

Conséquence : tout wikilink `[[john-doe]]` posé dans une note du vault (sources WhatsApp, conversations, atoms transversaux mentionnant l'utilisateur en interaction avec une People) est un **lien rouge volontaire**. Ce n'est pas un broken target à corriger. Les agents qui auditent les liens cassés doivent traiter `[[john-doe]]` comme une cible rouge intentionnelle (équivalent doctrinal de `[[vie-professionnelle]]` pour la Map parente non encore créée).

La source canonique de l'identité civile reste `_meta/identite-civile.md`. Tout agent qui a besoin d'un fact civil sur l'utilisateur (date de naissance, géographie, structures pro, cercle proche) lit ce fichier.

Règles pour les imports et la rédaction :

- Les imports de transcript / autres conversations ne sont **pas obligés** de lister `[[john-doe]]` dans `participants:`. Le wikilink reste autorisé en mention éditoriale dans le body (section "Acteurs récurrents" par exemple) sans que ce soit imposé par doctrine.
- Pour une conversation 1-1 entre l'utilisateur et X, `participants: [[<x>]]` seul suffit (l'utilisateur est implicitement l'utilisateur du vault).
- Pour une conversation à 3+ où l'utilisateur est partie prenante au même titre que les autres, `[[john-doe]]` peut apparaître pour symétrie éditoriale, mais reste un lien rouge.

## Pièces jointes et médias

Le vault est principalement du texte et des liens, pour rester
lisible et indexable par une IA, et pour ne pas transformer le repo
GitHub de backup en stockage de fichiers lourds.

### Règle hybride par poids

| Type de média | Stratégie | Exemples |
|---|---|---|
| **Léger** (≤ 2 MB) : schémas manuscrits scannés, captures d'écran, diagrammes simples, photos compressées illustratives | **In-vault, co-localisés** dans le même dossier que le MD source, **même slug** sauf extension. Référencé via `![[<slug>.<ext>]]`. | `3-sources/decision-tree-alcool-manuscrit.png` à côté de `decision-tree-alcool-manuscrit.md` |
| **Lourd** (> 2 MB) : vidéos, photos hi-res, scans haute qualité, audio, dossiers de plusieurs photos | **Lien externe** (Google Drive, YouTube, dossier local référencé par chemin) inscrit comme URL ou texte dans le MD, avec un descriptif texte qui résume le contenu pour préserver l'idée si le lien meurt. | `https://drive.google.com/...` dans le MD, jamais committé dans le vault |

Seuil indicatif : 2 MB. À ajuster collectivement si la pratique
montre que c'est trop strict ou trop laxe. Surveiller le bloat
GitHub : si la croissance dépasse ~50 MB/an, repenser
(GitHub LFS ou bascule des médias vers stockage externe).

### Workflow drag-and-drop d'une image dans une Source

1. Claude crée la Source MD avec un placeholder dans la section
   "Image source" (un bloc `[!todo]` qui rappelle l'emplacement
   cible).
2. L'utilisateur drag-and-drop l'image dans la page Obsidian. Obsidian
   l'écrit par défaut à la racine du vault avec un nom du type
   `Screenshot YYYY-MM-DD at HH.MM.SS.png` et insère le wikilink
   `![[Screenshot ...]]` dans le MD.
3. L'utilisateur signale "image dropped" à Claude.
4. Claude :
   - déplace le fichier image vers le dossier du MD source
     (ex. `3-sources/`),
   - le renomme avec le slug du MD source (ex.
     `decision-tree-alcool-manuscrit.png`),
   - met à jour le wikilink dans le MD pour pointer le nouveau nom,
   - bascule le frontmatter `status: to-import` → `status: read`
     et renseigne `date_consumed`,
   - retire le bloc `[!todo]` placeholder.

### Multi-images pour une même source

Cas rare. Si plusieurs images sont attachées à une seule Source,
créer un sous-dossier `<source-slug>-attachments/` à côté du MD et
y déposer les images, nommées `<source-slug>-01.png`,
`<source-slug>-02.png`, etc.

### Photos extraites partagées entre plusieurs notes consommatrices

Cas spécifique : une Source d'extraction (ex. PDF généalogique, dump
photo album) produit N photos individuelles que **plusieurs notes
consommatrices** (typiquement des fiches People) référencent. La doctrine
autorise alors la co-localisation des photos avec la **Source mère**
(le PDF d'extraction), pas avec chaque consommateur. Les fiches
consommatrices référencent les photos via wikilink simple `![[<slug>.png]]`,
qu'Obsidian résout via recherche globale dans le vault.

Exemple : `3-sources/2024-04-20-arbre-genealogique-doe-leo.jpg` est la
Source d'extraction. Les photos individuelles `max-doe.png`,
`seth-doe.png`, etc. vivent à côté dans `3-sources/`. Les fiches
`2-people/max-doe.md`, `2-people/seth-doe.md`, etc. référencent
chacune `![[max-doe.png]]` ou `![[seth-doe.png]]`. Pas de
duplication, pas de copie dans `2-people/<slug>-attachments/`.

Pourquoi cette autorisation : (a) duplication coûteuse en cas de N
consommateurs, (b) Obsidian search global garantit la résolution,
(c) la Source d'extraction reste l'origine factuelle des photos
(traçabilité préservée).

Limite : ne pas étendre cette pratique à des cas où il n'y a pas
de Source d'extraction commune. Pour une photo unique attachée à une
seule note, la règle co-localisée standard reste la règle.

### Raw archive attachments (convention agent-safe)

Cas spécifique : un import volumineux (export WhatsApp, dump email,
transcript Slack archivé, log de chat, transcript brut d'un appel
long) produit dans le vault une Source distillée + N inbox structurées
+ une copie du fichier raw d'origine co-localisée pour préservation
factuelle. Le fichier raw n'est pas destiné à être lu par un agent IA :
tout son contenu cognitivement signifiant a déjà été extrait dans la
Source (frise temporelle, métriques, verbatims clés horodatés et
contextualisés) et dans les inbox dérivées. Le raw existe pour archive,
pour l'utilisateur, et pour fallback si la distillation devait être refaite
plus tard avec d'autres critères.

Pour signaler cette intention au file system **et** aux agents IA
futurs (sessions cloud, agents distants, recherche AI dans le vault) :

1. **Naming convention** : suffixe `-raw-archive-do-not-read` avant
   l'extension. Le naming est le signal physique au file system.
   Exemples :
   - `2021-2023-conversation-whatsapp-jane-doe-raw-archive-do-not-read.txt`
   - `gmail-export-2018-2020-raw-archive-do-not-read.mbox`
   - `slack-export-team-canal-2022-raw-archive-do-not-read.json`

2. **Disclaimer dans la Source body** : la section `## Attachments`
   de la Source mère doit ouvrir par un avertissement explicite,
   parsable par un agent IA :

   > ⚠️ Agent IA : ne pas lire le fichier raw archive ci-dessous.
   > Tout le contenu cognitivement signifiant a déjà été distillé
   > dans cette Source (frise + verbatims clés + métriques) et dans
   > les inbox dérivées listées au-dessus. Lecture du raw = pollution
   > contexte sans gain cognitif. Le fichier reste co-localisé pour
   > préservation factuelle, pas pour exploration agent.

3. **Co-localisation** : le raw archive vit dans
   `<source-slug>-attachments/` à côté de la Source MD, comme tout
   attachment. Si plusieurs attachments cohabitent (PNG screenshots
   + raw archive), le naming `*-raw-archive-do-not-read` les
   distingue.

4. **Seuil de poids** : raw archive co-localisé seulement si ≤2 MB
   (cf. règle hybride supra). Au-delà, externaliser en `external_link`
   avec le même disclaimer dans la Source body.

Cette convention est réutilisable par toute doctrine d'import qui produit un
raw préservé (transcripts, mail dumps, exports Slack, archives Discord, etc.).

### Sur la lecture par les agents IA

Claude (multimodal) peut lire les images PNG / JPG / PDF
in-vault quand on lui pointe le chemin explicitement. Une image
in-vault est donc lisible. Une image hébergée en lien externe
(Drive, etc.) ne l'est pas directement (téléchargement préalable
nécessaire). Pour les médias importants conceptuellement mais lourds
(donc en lien externe), capturer une **transcription textuelle** ou
un résumé dans le MD parent pour préserver l'idée même si le lien
casse.
