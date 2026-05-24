---
type: meta
purpose: critères de classification utilisés par l'agent de triage
version: v1
status: active
created: 2026-04-25
last_updated: 2026-05-03
---

<!--
Changelog : externalisé vers _meta/doctrine-changelog.md (consulté à la demande).
Doctrine V1 anonymisée, packagée comme produit SAMPL-IQ.
-->

# Critères de triage

Ce fichier pilote les décisions de l'agent obsidian-triage. Il s'appuie sur
[[vault-doctrine-v1]] (les 8 types) et [[conventions]] (schemas YAML). Il ne
redéfinit pas les types, il donne les heuristiques pour les distinguer dans
les cas limites.

## 0. Détection journal-daily avant classification

Avant de tester les 8 types, vérifier si la note inbox est un **journaling
quotidien** (subtype `journal-daily` du type Log). Si oui, le workflow
dédié prend le relais : voir [[journaling-criteria]] (self-contained).

### Heuristique de détection

Une note inbox est candidate journal-daily si **au moins l'un** des
marqueurs suivants est détecté :

**Marqueur explicite primaire** :
- la note contient le mot `journaling` ou `journal du matin` ou
  `journal quotidien` dans les 200 premiers caractères du body, OU
- la note contient le tag `#journaling-daily` n'importe où dans le body,
  OU
- le frontmatter `device:` est `whisper` ET le titre H1 mentionne
  explicitement la journée (ex. "Journaling 27 avril").

**Marqueur structurel secondaire (fallback)** :
- la note contient au moins **3 mentions** de mesures typiques parmi :
  durée de sommeil, qualité de sommeil, humeur, énergie, stress, focus,
  sport, alcool, café, drogues, nicotine, sentiment social, fierté du
  jour, friction (client/équipe), décision impactante.

### Comportement

Proposer la détection à l'utilisateur avant de procéder, ne pas
auto-appliquer. Format :

```
Cette note ressemble à un journal-daily du <YYYY-MM-DD> :
  - Marqueur(s) détecté(s) : <explicite> | <structurel: N mesures>
  - Extrait : "<premières lignes>"

Action : "go" (déclencher le flux journaling) | "non, classer normalement" | "skip"
```

Si "go" : suivre [[journaling-criteria]] §3 workflow complet (parsing
datas, rédaction sections, identification dérivées, proposition,
création, commit). Le Log journal-daily atterrit dans `6-logs/journal/`,
les dérivées dans `0-inbox/` (et passeront ensuite par le triage normal,
les tests §1-§2 ci-dessous).

Si "non, classer normalement" : poursuivre avec §1 (classification par
type standard).

### Fusion de fragments matinaux

Si **plusieurs notes inbox** sont candidates journal-daily pour la même
date, fenêtre de moins de 60 minutes, même `device` (`whisper` ou
`journaling`) : proposer la fusion avant transformation. Détails dans
[[journaling-criteria]] §10.

## 0bis. Détection lifecycle-audit avant classification standard

Avant de tester les 8 types, vérifier également si la note inbox est un **rapport d'audit lifecycle** produit par `_meta/scripts/lifecycle-lint.py`. Si oui, elle n'est PAS triée comme une inbox standard : elle devient l'**input premier** du brief one-shot (§10).

### Heuristique de détection

Une note inbox est un rapport lifecycle-audit si **les deux marqueurs** sont vrais :

- frontmatter `device: lifecycle-audit`,
- frontmatter `type: inbox` avec `counts:` présent (block YAML avec sous-clés `intentions_auto`, `maps_incoherent`, etc.).

Aucune ambiguïté possible : le device est unique et signé par le script.

### Comportement

L'agent **lit intégralement** la note (toutes les sections), puis intègre son contenu dans le brief one-shot du triage (§10) :

- §1 du rapport (Intentions actives candidates à fermer) → bloc LIFECYCLE PRÉ-DÉTECTÉ du brief, partie intentions. Auto-confidence → ligne AUTO. Manual-confidence → ligne PROPOSE avec default.
- §2 du rapport (Maps avec maturity incohérente) → bloc LIFECYCLE PRÉ-DÉTECTÉ, partie Maps maturity. Bascules nettes en AUTO, frontières en PROPOSE.
- §3 du rapport (People last_seen obsolète) → ligne AUTO unique avec compteur (`last_seen mis à jour pour <n> People`).
- §4 du rapport (Maps manquantes recommandées) → bloc LIFECYCLE PRÉ-DÉTECTÉ, partie Map manquante. Conditions auto (§4 lifecycle) → AUTO, sinon PROPOSE.
- §5 du rapport (Doublons suspects) → bloc AMBIGUÏTÉS À LEVER avec defaults publiés.

Si **d'autres inbox** sont en attente : le triage les traite normalement APRÈS avoir intégré le rapport lifecycle-audit dans le brief. Les ambiguïtés des autres inbox sont ajoutées aux ambiguïtés du rapport dans le même brief unique.

### Absorption en fin de triage

La note `device: lifecycle-audit` est **supprimée** à la fin du triage, au même titre que toute inbox traitée. Ses actions sont tracées dans :

- les frontmatter des cibles modifiées (intentions, Maps, People),
- `_meta/vault-state-log.md` append,
- le commit du cluster.

Pas de conservation de l'historique des rapports : si l'utilisateur veut un nouveau rapport, il relance le script.

### Cas multi-rapports

Si plusieurs notes `device: lifecycle-audit` sont en attente (rapports successifs non consommés faute de triage), garder la **plus récente** (`captured` le plus récent), supprimer les autres en signalant à l'utilisateur dans le brief one-shot. Les anciens rapports sont obsolètes par construction (le vault a évolué entre-temps).

## 1. Critères de classification par type

> **Discipline tags** : pour toute note typée créée ou modifiée pendant le triage, suivre `[[tag-hygiene-criteria]]` au moment de remplir le champ `tags:` du frontmatter. Nomenclature `racine/sous-tag` (2 niveaux strict), 11 racines actuelles (évolutives), checklist de pose, cas hors-périmètre racine et procédure pour proposer une nouvelle racine. Si une idée triagée touche à un domaine absent des racines actuelles (politique, écologie, etc.), proposer une nouvelle racine à l'utilisateur, ne pas forcer dans une racine inadaptée.

### Atom

Unité de pensée atomique, dense, autonome, lisible hors contexte.

Signaux :
- exprime UNE idée, citation, donnée, règle ou image créative
- pas de structure narrative ni datée
- pas centré sur une personne ou un artefact externe
- tient en quelques phrases sans perdre son sens

Contre-exemple : "Conversation avec Sam hier sur l'absurde". C'est un
Log event. L'Atom serait l'idée distillée extraite ensuite, reliée à
`[[sam-doe]]` et `[[absurde]]`.

### People

Une personne réelle, un fichier.

Signaux :
- note centrée sur "qui est X" (contexte, relation, historique)
- contient bio, idées cadeau, sujets partagés
- la personne est le sujet, pas une mention
- pas de fait/idée isolée qui pourrait vivre sans elle

Contre-exemple : "Sam m'a dit que les services AI vont remplacer le SaaS".
C'est un Atom (data ou idea), avec `people: [[sam-doe]]` dans le
frontmatter. La People note de Sam existe en parallèle.

### Source

Artefact externe consommé (livre, article, podcast, vidéo, conversation).

Signaux :
- titre + auteur (ou interlocuteur) identifiables
- medium externe explicite
- la note décrit le contenu produit par autrui, pas ma réflexion sur lui
- on en extrait ensuite des Atoms

Contre-exemple : "Mes notes de réflexion après le livre X". Ce sont des
Atoms (mes idées), reliés via `source: [[livre-x]]`. La Source est la fiche
de l'artefact, pas le contenu cognitif que j'en tire.

### Project

Initiative bornée dans le temps avec un objectif mesurable.

Signaux :
- verbe d'action + sujet + horizon temporel
- objectif concret atteignable
- étapes ou checklist en germe
- décision déjà prise (sinon c'est une réflexion en amont)

Contre-exemple : "Devrais-je apprendre le blackjack ?". C'est un Atom
(raisonnement) ou un Log (decision quand tranchée). Le Project naît quand
la décision est prise ET l'objectif borné.

### Map

Index vivant d'un domaine. Hub, pas essai.

Signaux :
- note panoramique sur un sujet large
- liste ou regroupe des Atoms / Sources / People / Projects
- contient une "vision" courte et des "questions ouvertes"
- pas de contenu unitaire qui suffirait à lui seul

Contre-exemple : "Définition de la permaculture en une phrase". C'est un
Atom (definition / idea). La Map `[[permaculture]]` est le hub qui pointe
vers cet Atom et beaucoup d'autres.

### Log

Journal daté ou événement ponctuel.

Signaux :
- date dans le slug ou en frontmatter
- format narratif (ce qui s'est passé, ce que j'en pense)
- ressenti, mood, people impliqués
- événement, conflit, décision, voyage

Contre-exemple : "Idée qui m'est venue hier matin". La date dans la capture
ne fait pas un Log : c'est le format narratif événementiel qui le détermine.
Ici c'est un Atom.

### Intention

Cible personnelle sans deadline. Mouvement vers un futur état.

Signaux :
- verbe au futur ou conditionnel ("je devrais", "j'aimerais", "il faut que je")
- horizon flou ("à un moment", "un jour", "cette année", "dans les prochains mois")
- engagement personnel énoncé sans plan d'exécution
- contemplation sur soi-même, ce qu'on veut devenir, vivre, lire, apprendre
- décision pas encore prise (sinon Project), pas encore stabilisée en pensée (sinon Atom)
- pas d'urgence, pas de deadline implicite courte (sinon tâche court terme, voir §3)

Contre-exemple : "Apprendre les échecs cette année, inscription au club X
le 15 mai, tournoi visé en septembre". Décision prise, étapes posées,
horizon mesurable : c'est un Project, pas une Intention.

### Question

Interrogation ouverte que je me pose sans avoir le temps ou l'envie de la
résoudre sur le moment. Trou productif dans la réflexion, à creuser plus
tard.

Signaux :
- vraie question avec point d'interrogation (graphique ou conceptuel) en
  formulation centrale
- verbes interrogatifs au cœur du contenu (pourquoi, comment, est-ce que,
  dans quelle mesure, à quel point)
- absence de réponse dans la note (la note pose, ne résout pas)
- tone contemplatif ou exploratoire, pas d'urgence d'exécution
- lien à une décision long terme, une thèse stratégique, une réflexion
  philosophique

Comment distinguer Question des autres types :
- Question vs Atom : la note CHERCHE (Question) vs la note AFFIRME (Atom).
- Question vs Intention : matière à réflexion passive (Question) vs
  mouvement vers une action (Intention).
- Question vs Project : exploration ouverte sans scope (Question) vs
  exécution structurée et bornée (Project).

Contre-exemple : "Apprendre les échecs sérieusement un jour" formulé comme
intention de vie. Pas une Question (pas d'interrogation, c'est un
engagement) : c'est une Intention.

## 2. Hiérarchie de décision en cas d'ambiguïté

Tester les types dans cet ordre, du plus spécifique au plus générique :

1. **People** : note centrée sur une personne identifiable ?
2. **Source** : artefact externe avec auteur/titre/medium ?
3. **Project** : objectif borné + horizon + décision prise ?
4. **Intention** : engagement personnel sans deadline, horizon flou, mouvement vers un futur état ?
5. **Question** : interrogation ouverte sans réponse, à creuser plus tard, pas d'appel à l'action ?
6. **Log** : narratif daté d'un événement ou décision ?
7. **Map** : index panoramique d'un domaine ?
8. **Atom** : par défaut, si rien de plus spécifique ne colle.

Règles de conflit fréquentes :

| Conflit | Tranchage |
|---|---|
| Atom vs Source | Si la note décrit un artefact externe : Source. Si elle décrit une idée que j'en tire : Atom + lien `source:`. |
| Atom vs Log | Si format narratif daté : Log. Si idée distillée : Atom. Un Log peut produire des Atoms (`Atoms à extraire`). |
| Atom vs Map | Une Map sans Atoms attachés est un Atom déguisé. Si une seule idée centrale : Atom. Si hub vers plusieurs notes : Map. |
| Project vs Log decision | Décision = Log (subtype decision). Mise en oeuvre bornée = Project. La décision peut déclencher un Project. |
| People vs Atom mentionnant une personne | La personne est le sujet : People. La personne est citée comme contexte : Atom avec `people: [[...]]`. |
| Intention vs Atom | Atom = pensée stable ("la liberté est le bon choix de contraintes"). Intention = mouvement vers un futur état ("j'aimerais lire plus de stoïciens cette année"). En cas de mixte, l'Atom capture la pensée et l'Intention capture l'engagement, on peut créer les deux et les linker. |
| Intention vs Project | Intention = cible sans deadline, décision pas tranchée. Project = décision prise, scope borné, étapes en germe. Si on hésite, Intention par défaut : la promotion en Project se fait quand le scope se cristallise. |
| Intention vs tâche court terme | Voir §3 ci-dessous. Si urgence ou deadline courte implicite, sortir du vault. |
| Question vs Atom | La note formule une interrogation ouverte sans réponse : Question. La note formule une réponse stable ou une assertion : Atom. Une Question peut produire des Atoms (réponses partielles, hypothèses formalisées) liés via `related_atoms`. |
| Question vs Intention | Question = matière à contemplation passive, pas d'action en germe. Intention = engagement personnel vers un futur état, mouvement actif. En cas de mixte (interrogation qui débouche sur une cible), créer les deux et les linker. |

## 3. Détection des tâches urgentes court terme

Certaines notes inbox ne sont pas du contenu pour le second brain mais des
tâches à exécuter vite. Elles ne doivent PAS être classées dans le vault.

### Signaux

- verbe d'action immédiat ("envoyer", "appeler", "payer", "signer", "réserver")
- deadline implicite ou explicite courte ("avant vendredi", "demain", "ce soir", "cette semaine")
- formulations d'urgence ("il faut absolument que", "ne pas oublier de", "urgent")
- objet opérationnel sans valeur réflexive (admin, logistique, transactionnel)
- pas de "pourquoi" derrière, juste un "quoi" et un "quand"

### Comportement de l'agent (mode low-friction)

NE PAS classer la note dans le vault. Regrouper toutes les tâches urgentes détectées dans le **brief one-shot initial** (§10) sous un bloc dédié `TÂCHES URGENTES DÉTECTÉES`. Pas de question note par note.

Default appliqué si l'utilisateur ne dicte rien dans le brief : **préserver l'inbox** (ne pas supprimer), signaler le contenu dans le diff final pour copie manuelle. La suppression d'une inbox tâche urgente nécessite mention explicite de l'utilisateur dans le brief ("supprime les tâches urgentes" ou équivalent).

Si signaux mixtes (tâche urgente ET réflexion durable), l'agent scinde auto : la pensée durable est classée comme Atom ou Intention, la partie tâche est listée dans le bloc tâches urgentes du brief.

### Distinction Intention vs tâche court terme

| Critère | Intention | Tâche urgente |
|---|---|---|
| Horizon | flou (semaines, mois, années) | court (jours, semaine) |
| Charge cognitive | engagement personnel, lié à valeurs ou direction de vie | exécution, transactionnel |
| Si je l'oublie | dommage durable, pas de conséquence immédiate | conséquence concrète rapide (manque rdv, oubli paiement) |
| Forme verbale | "j'aimerais", "à un moment", "il faut que je" sans deadline | "il faut absolument que", verbe d'action + date proche |
| Destination | `7-intentions/` | hors vault (Notes iPhone) |

En cas de doute, demander à l'utilisateur plutôt que de trancher seul : la
classification erronée d'une tâche urgente comme Intention génère un risque
opérationnel (oubli), alors que l'inverse génère du bruit dans le vault.

## 4. Désambiguïsation des références (People, Project, Map)

### Mode low-friction par défaut

**L'agent tranche en autonomie quand un discriminant existe.** Il ne demande PAS pour les cas suivants :

- Un seul match évident dans le vault (slug existant, contexte cohérent).
- Référence explicite par slug exact (`[[sam-doe]]`).
- La note inbox cite déjà la People / Map / Project sans ambiguïté.
- Homonyme avec **discriminant contextuel clair** : tag `geo/`, cluster cohérent (autre People co-mentionnée appartient au même cercle), mention d'un proche commun, profession évoquée. L'agent tranche en confidence et signale dans le diff final.
- Map candidate non existante mais voisinage évident : rattacher auto à la Map existante du domaine.

### Cas d'interruption stricte (1 seule fois dans le brief one-shot)

L'agent regroupe **toutes** les ambiguïtés non-résolvables auto dans le brief one-shot initial (§10), avec un default proposé pour chacune. Pas d'interruption en cours d'exécution.

Cas qui justifient une ligne dans le brief :

- Homonymes sans discriminant contextuel (deux Nina sans tag/cercle).
- Référence implicite floue irrécupérable ("le projet de l'année dernière" sans contexte).
- People mentionnée pour la première fois comme **sujet** sans aucun contexte (relation et profession inconnues).
- Map candidate à créer ET rattachement à Map existante voisine également plausible.

### Format dans le brief one-shot

Dans le bloc `AMBIGUÏTÉS À LEVER` du brief (§10), une ligne par ambiguïté avec default proposé en gras :

```
A1. Homonyme "Nina" : **default [[nina-smith]]** (cousine, plus citée),
    alt [[nina-rossi]] (collègue) | skip
```

Si l'utilisateur ne dicte pas, l'agent applique le default. Si l'utilisateur refuse tout (`skip` sur cette ligne), flag `needs_clarification` posé et l'inbox passe à la suivante.

## 5. Fusion de doublons sémantiques

### Détection

L'agent suspecte un doublon quand au moins deux signaux sont vrais :

- overlap thématique fort (idée centrale identique reformulée)
- proximité temporelle (notes créées à moins de 7 jours d'écart)
- mêmes liens (mêmes people, source, ou map)
- titres / slugs proches en distance d'édition

Le seuil est un indicateur, pas une règle. L'agent peut signaler un doublon
avec moins de signaux si la confiance est haute (ex: titres quasi
identiques), ou ne rien signaler avec plus de signaux si l'overlap est
superficiel. En cas de doute, signale et laisse l'utilisateur trancher.

Doublon ≠ versions complémentaires : si les deux notes traitent le même
sujet sous des angles différents et se complètent, garder séparées et
linker entre elles.

### Comportement low-friction

**Auto-fusion si haute confiance** (≥3 signaux convergents ET un slug clairement plus stable que l'autre) :

- Overlap thématique fort (idée centrale identique).
- Proximité temporelle <7 jours.
- ≥2 liens partagés (people, source, maps).
- Un slug est ≥3 caractères plus court ET sans pattern temporel `YYYY-MM-DD` au profit d'un slug abstrait.

L'agent fusionne auto sous le slug stable, conserve la traçabilité (`Fusionné le YYYY-MM-DD depuis [[slug-supprimé]]`), signale la fusion dans le diff final.

**Validation requise dans le brief one-shot** si :

- ≥3 signaux convergents MAIS deux slugs aussi stables l'un que l'autre.
- 2 signaux seulement (confidence moyenne).
- Slug plus court n'est pas plus stable (ex: titre court mais opportuniste).

Format dans le brief :

```
A2. Doublon possible [[note-A]] ↔ [[note-B]] : **default fusionner sous [[slug-A]]** (overlap fort + 2 liens partagés) | garder séparées et linker | skip
```

Si l'utilisateur ne dicte pas : default appliqué. Si l'utilisateur dit "garder séparées" : ajout cross-link bidirectionnel "Voir aussi" dans les deux notes.

### Méthode de fusion

- garder le slug le plus court et le plus stable (celui qui décrit le mieux
  l'idée durable, pas l'humeur du jour de la capture)
- concaténer les datas factuelles uniques des deux notes
- préserver tous les liens des deux côtés (people, source, maps, projects)
- en bas de la note fusionnée, ajouter une ligne `Fusionné le YYYY-MM-DD
  depuis [[slug-supprimé]]` pour traçabilité
- supprimer l'autre fichier seulement après confirmation visuelle de
  l'utilisateur ou si l'agent opère en mode autonome validé

## 6. Flag needs_clarification

### Quand poser le flag

- l'agent ne peut pas trancher seul ET l'utilisateur n'est pas dispo à
  interrompre (mode batch)
- l'utilisateur a explicitement skippé une question de désambiguïsation
- une référence est bloquante mais non urgente

### Format dans le frontmatter inbox

```yaml
needs_clarification: <slug-court-de-la-raison>
flagged_at: YYYY-MM-DD
```

`flagged_at` permet à l'utilisateur de filtrer en Dataview les notes flaggées par
ancienneté, sans imposer un comportement automatique à l'agent.

Slugs recommandés pour `needs_clarification` (kebab-case, descriptif) :
- `type-atom-vs-source`
- `people-homonyme-sam`
- `map-creer-ou-rattacher-permaculture`
- `doublon-suspecte-avec-slug-x`
- `reference-implicite-projet-annee-derniere`

### Comportement à la session suivante

L'agent lit le flag dès qu'il rouvre la note. La raison kebab-case lui dit
quoi reposer comme question, sans rerefaire toute l'analyse. Si l'utilisateur
relit la note 3 mois plus tard, le flag lui dit aussi pourquoi elle est
restée bloquée.

## 7. Posture enrichissement du réseau

Le triage est le moment où le graphe se construit. La seule porte d'entrée
du vault, c'est l'inbox : si le triage crée des dérivées sans rétro-alimenter
les pages liées, le système neuronal reste un tas de notes au lieu d'un
réseau. Trois principes complémentaires.

### 7.1 People stubs au triage, pas plus tard (auto, pas de question)

Quand une dérivée (Atom, Log event, Question, Project, Intention) mentionne
une personne **comme sujet** (pas juste référence en passant), créer la
fiche People stub **auto, sans demander à l'utilisateur**, même avec contexte
minimal (`relation`, `context`, 2-3 lignes de body, le reste à `null`).
Faire le lookup sémantique avant pour éviter les doublons (cf. mémoires
Claude `feedback_lookup_semantique_avant_creation_people` et
`feedback_creer_people_stubs_au_triage` si chargées). Si pas de match,
créer-puis-affiner plutôt que reporter.

**Mode low-friction** : la création de People stub minimale ne génère
JAMAIS une interruption au triage. Les nouveaux stubs créés sont signalés
dans le diff final (§10). Si l'utilisateur veut rectifier une création, il le
fait au moment du diff final ou dans une session People ultérieure.

Cas limite "mention en passant" (ex. "Sam m'a dit que..." dans un Atom) :
reste mention texte sauf si la personne est aussi sujet ailleurs.

Justification : le triage est le seul moment où la référence apparaît avec
son contexte minimal (rôle, structure, relation suspectée). Plus tard =
oubli, ou stub orphelin créé sans contexte. Ne pas skip "par prudence".

### 7.2 Enrichissement aval des pages liées

À chaque dérivée typée créée, mettre à jour le **corps** des pages
People / Maps / Projects référencées par wikilink. Pas juste les wikilinks
dans le frontmatter, qui suffisent à la navigation mécanique mais pas à la
lecture humaine.

Ajouter dans la cible :
- une ligne dans la section "Sujets partagés" / "Notes liées" / "Atoms
  attachés" / "Sources" (selon le type cible),
- une mention dans "Historique" (People) ou "Journal du projet" (Project)
  si la dérivée est datée,
- si la dérivée révèle un fait nouveau structurant (diagnostic comportemental,
  décision majeure, pattern récurrent, position stratégique), corps avec
  traçabilité minimale (1-3 phrases + lien vers la dérivée).

Filtre anti-spam : la mise à jour doit apporter de la valeur de lecture
future. Ne pas spammer une fiche People avec une ligne pour chaque atom
trivial qui la mentionne.

Test décisif : ouvrir une People avec 50 backlinks. Si le corps reste un
stub d'origine, le triage a fait la moitié du travail.

#### Wikilink-check sur les fichiers modifiés (règle stricte CLAUDE.md)

Pour chaque fichier que le triage modifie (dérivée typée nouvellement créée, page People/Map/Project enrichie en aval), faire une passe de **wikilink-check** : repérer toutes les mentions en texte plat qui devraient être wikilinkées vers une note existante OU candidate claire à création. Cohérent avec `CLAUDE.md` §"Règles comportementales" règle wikilink stricte.

Cas concrets à wikilinker auto :
- Prénom seul d'une People existante : `Sam` → `[[sam-doe]]`.
- Nom de domaine d'une Map existante : `acme` → `[[acme]]`, `absurde` → `[[absurde]]`.
- Verbe + sujet d'une intention/question/project existante : "appeler Sam" → `[[appeler-sam-prendre-nouvelles]]` si l'intention existe, sinon laisser en texte.
- Référence à une Source datée : `2026-05-01 call Sam` → `[[2026-05-01-call-sam-nouvelles-philosophie]]` si la Source existe.

Cas où laisser en texte (pas wikilinker) :
- Concept générique non-typable (`Solvay`, `Linear`, `Notion`, `Tinder`).
- Lieu sans note dédiée (`Lisbonne` non typé, sauf si Map `geographie-nomadisme` ou similar le couvre comme candidat).
- Citation entre guillemets verbatim (préservation de la voix originale).

Cas ambigu (candidat à création mais pas évident) :
- Wikilinker quand même avec lien rouge (signal volontaire pour le triage suivant), ET ajouter une ligne dans le bloc AMBIGUÏTÉS du brief one-shot signalant le candidat. Le triage suivant tranche.

Test rapide en fin de modification : `grep -E '(\b(Sam|Robin|Victor|Acme|...) )' <fichier>` pour vérifier qu'aucune mention nue n'a été laissée. Si un cas reste flou, flag dans le diff final plutôt que pollution silencieuse.

### 7.3 Défaut "la totale", pas la version minimale

Quand on hésite entre "créer juste un Atom" et "créer Atom + Intention +
Question + People stub + cross-links + enrichissement aval", **prendre la
version maximale**. Un atom isolé sans son réseau est une note morte.

Heuristiques d'expansion :
- Si l'Atom encode une vision / un engagement → créer aussi l'Intention.
- Si l'Atom soulève une question ouverte attachée → créer aussi la Question.
- Si l'Atom mentionne une personne comme sujet ou sponsor d'idée → créer
  le stub People (cf. §7.1).
- Si l'Atom appartient à un domaine d'une Map existante → enrichir le
  corps de la Map (cf. §7.2).
- Si plusieurs notes existantes overlap thématiquement avec la dérivée →
  ajouter "Voir aussi" cross-links bilatéraux dans les deux sens.

Cas limite "spam" : si la totale produit > 5 dérivées pour un seul fragment
inbox, c'est un signal que le fragment était une Map ou une Source en
réalité, pas un Atom unique. Reconsidérer la classification de base avant
de tout créer.

Cas limite "trop minimal" : un Atom seul, sans relation, sans Intention,
sans People stub, sans enrichissement de la Map. Si c'est le résultat,
c'est qu'on a sous-traité. Reprendre en mode totale.

## 8. Lecture et mise à jour de [[vault-state]]

Le triage est un événement structurant : il crée des notes typées, modifie
des Maps et People, change les compteurs et la complétude YAML. Il doit
nourrir le dashboard `_meta/vault-state.md`.

### 8.1 En début de cluster de triage

Avant de commencer la classification, l'agent lit `_meta/vault-state.md` :

- §3 Cartographie des hubs : pour savoir quelles Maps sont stubs ou growing
  et privilégier le rattachement des nouvelles dérivées à ces Maps quand le
  contenu le justifie (densification organique).
- §4 Zones sous-représentées : pour repérer si une note inbox parle d'une
  zone identifiée (ex. famille élargie Doe, hygiène de vie) et choisir
  le type cible en conscience (créer la People stub et la Map manquante
  plutôt que juste un Atom orphelin).
- §7 Portes recommandées : si une porte recommandée concerne le même domaine
  que les notes inbox triagées, le signaler à l'utilisateur en fin de cluster (porte
  potentielle pour une session de creusage).

### 8.2 En fin de cluster de triage

Avant le commit final, **dérouler [[lifecycle-criteria]] §2 (checklist en 6 points)**. Le triage est le point d'application principal de la lifecycle aval. Résumé :

1. **Intentions consommables** ([[lifecycle-criteria]] §2.1) : grep `7-intentions/` sur les `people:` + verbe d'attaque pour chaque dérivée typée et la Source-mère du cluster (via `source_call`). Proposer fermeture à l'utilisateur, validation requise.
2. **Questions partiellement répondues** ([[lifecycle-criteria]] §2.2) : grep `8-questions/` sur les Atoms créés. Proposer passage `open → partial`, validation requise.
3. **People last_seen** ([[lifecycle-criteria]] §2.3) : auto pour les People participants ou sujets d'une dérivée datée.
4. **Map maturity** ([[lifecycle-criteria]] §2.4) : recompter atoms attachés, appliquer seuils §3 du fichier lifecycle, basculer auto si franchissement net, valider sinon.
5. **Fermeture boucle Source ↔ Atoms** ([[lifecycle-criteria]] §2.5) : pour chaque inbox triée avec frontmatter `source_call:` / `source_youtube:` / autre `source*`, éditer la Source-mère pour remplacer le bullet textuel correspondant dans la section "Atoms à extraire" par le wikilink réel produit (Atom, Question, Project, Log, etc.). Atomes orphelins ajoutés en bas avec mention. Renommer H2 en "Atoms extraits" si liste 100% fermée. **Auto, pas d'interruption.**
6. **Map manquante** ([[lifecycle-criteria]] §4) : si ≥3 atoms convergent vers une Map qui n'existe pas mais que [[vault-state]] §4 ou §7 recommande, proposer création avec draft de vision.
7. **vault-state** : recalculer §1 (compteurs), §2 (complétude YAML, cible 90% sur `maps:`, 70% sur `people:`), §3 (hubs), §4 (zones), append à `_meta/vault-state-log.md` (rolling 14j, log <30 mots), frontmatter `last_updated` + `last_session_id` de `vault-state.md`. Snippets bash/python dans [[vault-state]] §10. Vérifier l'archivage rolling 14j du log (cf. [[vault-state]] §11 point 8).

Si le triage est minimal (1-2 notes, pas de structurel), update §1 vault-state + append `vault-state-log.md` suffit, plus la lifecycle §2.3 (last_seen) si applicable.

Le commit de mise à jour de `_meta/vault-state.md` et des cibles touchées par lifecycle peut être inclus dans le commit du cluster (recommandé) ou être un commit séparé `📐 doctrine: vault-state + lifecycle <cluster-id>` si plus pratique.

**Avant le commit final, lancer `python3 _meta/scripts/post-cluster-audit.py`.** Le script flag automatiquement les 5 catégories de trous (wikilinks rouges, wikilinks SaaS génériques, Maps/People wikilinkées non enrichies aval, Sources participants vs last_seen). Si output non vide, corriger les trous signalés puis re-lancer. Cf. `_meta/scripts/README.md`. C'est le seul garde-fou mécanique qui transforme les règles de discipline aval en check binaire avant commit.

## 9. Mode low-friction et garde-fous d'interruption stricts

Le triage tourne en **autonomie maximale** par défaut. L'agent applique les heuristiques §1-§8, déroule lifecycle §2 et commit, en bloc, sans intervenir.

### 9.1 Les 4 SEULS cas qui justifient une interruption en cours d'exécution

Si l'un de ces 4 cas survient APRÈS le brief one-shot (§10) et qu'il n'y était pas couvert, l'agent peut interrompre proprement. Sinon, il continue.

1. **Homonyme People non-résolvable.** Plusieurs People avec le même prénom dans `2-people/` ET aucun signal contextuel discriminant (pas de tag `geo/`, pas de cluster cohérent, pas de mention d'un proche commun). Si discriminant existe, l'agent tranche et signale dans le diff final.
2. **Doublon haute confiance avec choix de slug ambigu.** ≥3 signaux convergent ET les deux slugs candidats sont aussi stables l'un que l'autre. Si un slug est clairement plus court ou plus stable, l'agent fusionne auto sous celui-là (§5).
3. **Cluster ambigu à ≥2 classifications plausibles équivalentes.** Une note pourrait être Atom OU Question OU Intention avec des arguments équivalents. Pour les ambiguïtés simples (Atom vs Log, Atom vs People), l'agent tranche par défaut sur le type le plus fréquent dans le cluster ou via §2 hiérarchie de décision.
4. **Suppression de note inbox confirmée.** L'agent ne supprime jamais une inbox sans mention explicite dans le brief one-shot (ex: "supprime les tâches urgentes" en bloc). Le brief vaut pour tout le triage.

### 9.2 Tout le reste est auto

Aucune interruption pour :
- Création People stub minimale (§7.1, auto, juste signalée).
- Enrichissement aval Maps/People (§7.2, auto).
- Bascule Map maturity à seuil net (lifecycle §2.4, auto).
- Fermeture intention si match haute confiance (lifecycle §2.1 conditions auto).
- Création Map manquante si recommandée vault-state ≥3 sessions ET ≥3 atoms convergents (lifecycle §4 conditions auto).
- Fusion doublon ≥3 signaux convergents avec slug clairement plus stable (§5 auto).
- Désambiguïsation avec discriminant contextuel clair (§4 auto).
- Tâches urgentes (§3 traitées dans le brief, default = préserver inbox sans supprimer).
- Mise à jour `last_seen` People (lifecycle §2.3, auto, factuel).
- Fermeture boucle Source ↔ Atoms (lifecycle §2.5, auto, factuel : remplace bullet textuel par wikilink dans la section "Atoms à extraire" de la Source-mère pour chaque inbox triée).
- Recalcul vault-state §1 + append `vault-state-log.md` (auto).

### 9.3 Defaults appliqués si l'utilisateur ne dicte rien dans le brief

Pour chaque ambiguïté listée dans le brief one-shot (§10), l'agent applique le default proposé en gras. Pas de re-prompt. Si l'utilisateur répond "go defaults" ou ne dicte rien, le triage tourne intégralement en autonomie.

## 10. Brief one-shot et diff final

### 10.1 Brief one-shot initial (Phase A)

Au lancement du triage, l'agent fait un scan rapide de `0-inbox/` (lecture frontmatter + 200 premiers caractères de chaque note, ~1-2 min) et présente UN SEUL bloc compact.

Format :

```
═══════════════════════════════════════════════════════════
🗂️ TRIAGE : <N> inbox détectées (<K> clusters)
═══════════════════════════════════════════════════════════

CLUSTERS PRÉ-IDENTIFIÉS
  C1. <thème> (<n> inbox) : <résumé une ligne>
  C2. <thème> (<n> inbox) : <résumé une ligne>
  ...

AMBIGUÏTÉS À LEVER (defaults proposés en gras)
  A1. <description> : **default <choix>** | alt <choix> | skip
  A2. ...
  (omis si aucune)

LIFECYCLE PRÉ-DÉTECTÉ
  L1. AUTO : fermer intention [[<slug>]] avec [[<source>]] (match double)
  L2. AUTO : créer Map [[<slug>]] (vault-state ≥3 sessions, <n> atoms convergents)
  L3. PROPOSE : passage Map [[<slug>]] de stub à growing (à la frontière)
  L4. AUTO : last_seen mis à jour pour <n> People
  ...

TÂCHES URGENTES DÉTECTÉES (default : préserver, signaler dans diff final)
  T1. inbox <slug> : "<extrait>"
  ...
  (omis si aucune)

ACTIONS AUTO STANDARD (sans validation)
  - Création People stub si nouveau sujet (§7.1)
  - Enrichissement aval Maps/People (§7.2)
  - Cross-links bidirectionnels selon §7.3 "la totale"

═══════════════════════════════════════════════════════════
Dicte une validation longue qui couvre tout ce qui n'est pas
default, ou dis simplement "go defaults" pour lancer en bloc.
═══════════════════════════════════════════════════════════
```

Règles du brief :
- **Compact**, pas de blabla. Une ligne par item, defaults visibles d'un coup.
- **Defaults publiés** : L'utilisateur voit ce qui se passera s'il ne dicte rien.
- **Pas de re-prompt** : une fois la dictée l'utilisateur reçue (ou "go defaults"), l'agent ne reposera AUCUNE question structurelle pendant l'exécution sauf cas §9.1.

### 10.2 Exécution autonome (Phase B)

L'agent applique les décisions du brief + ses defaults + ses heuristiques. Traite tous les clusters en bloc, déroule lifecycle, commit. Sans interruption sauf §9.1.

Si une interruption §9.1 survient : un seul prompt court, format identique aux ambiguïtés du brief (`default <choix> | alt <choix> | skip`). Réponse, l'agent reprend. Pas d'enchaînement de prompts.

### 10.3 Diff final (Phase C)

À la fin, l'agent présente :

```
═══════════════════════════════════════════════════════════
✅ TRIAGE TERMINÉ : <N> inbox absorbées en <M> minutes
═══════════════════════════════════════════════════════════

GIT DIFF
  Created : <X> fichiers (+<a> atoms, +<b> people, +<c> log, +<d> question)
  Modified : <Y> fichiers (<m> maps, <p> people, <i> intention, vault-state)
  Deleted : <N> inbox absorbées

ACTIONS STRUCTURELLES
  - Fermé intention [[<slug>]] → realized <date>
  - Créé Map [[<slug>]] avec <n> atoms initiaux
  - Fusionné [[<a>]] + [[<b>]] → [[<a>]] (slug stable)
  - Map [[<slug>]] : stub → growing
  - ...

DÉCISIONS AUTO PRISES
  - Nina → [[nina-smith]] (homonyme, default)
  - <n> People stubs créés : [[<a>]], [[<b>]], ...
  - last_seen mis à jour sur <n> People
  - ...

FLAGS POSÉS (<n>)
  - inbox <slug> : needs_clarification = "<raison-kebab>"

TÂCHES URGENTES NON SUPPRIMÉES (<n>)
  - inbox <slug> : "<extrait court>"

═══════════════════════════════════════════════════════════
Dicte : "commit" / "rollback X et Y" / "modifie classification Z" / "supprime tâches urgentes" / "skip flag"
═══════════════════════════════════════════════════════════
```

Règles du diff final :
- **Compact**, lecture en <2 min par l'utilisateur.
- **Tout est listé** : ce qui a été fait, ce qui a été décidé en auto, ce qui reste flaggé.
- **Rollback possible** par item : L'utilisateur peut dicter "rollback la fusion A/B" ou "modifie classification Z en Question au lieu d'Atom" et l'agent re-traite sans tout perdre.
- **Default si l'utilisateur ne dicte rien** : commit en bloc dans 30 secondes (compatible avec un l'utilisateur qui revient juste lire et valide tacitement).
