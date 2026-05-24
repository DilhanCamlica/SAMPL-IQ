---
type: meta
purpose: critères de clôture aval (fermeture intentions, mise à jour Maps/People, création de Map manquante) déroulés au triage et en fin de session, source de vérité unique pour la cohérence du graphe
version: v1
status: active
created: 2026-05-03
last_updated: 2026-05-08
---

<!--
Changelog : externalisé vers _meta/doctrine-changelog.md (consulté à la demande).
Doctrine V1 anonymisée, packagée comme produit SAMPL-IQ.
-->

# Critères de clôture aval (lifecycle)

Source de vérité unique pour la **fermeture aval** des objets du vault : intentions consommées, questions partiellement répondues, People mises à jour, Maps qui passent un seuil de maturité, Maps manquantes à créer. Toute opération qui produit ou modifie de la matière typée doit dérouler la checklist §2 avant commit.

Voir aussi : [[triage-criteria]] (point d'application principal, §8.2), [[sessions-criteria]] (point d'application secondaire, §2 phase 7), [[vault-state]] (dashboard mis à jour en parallèle, §11), [[conventions]] (schemas frontmatter des cibles à modifier).

## §1. Principe directeur

Le **triage** et les **sessions** sont les deux moments structurants où la matière typée se cristallise. Ce sont eux qui doivent dérouler la lifecycle aval.

Les autres workflows restent des **créateurs purs** :

- `transcripts-import` crée 1 Source + N inbox, pas de fermeture aval.
- `youtube-import` crée 1 Source + N inbox, pas de fermeture aval.
- `journaling` crée 1 Log + N inbox, pas de fermeture aval.
- `capture` crée 1 inbox, pas de fermeture aval.

La fermeture aval se déclenche au moment où ces inbox passent au triage et deviennent typées. Cette séparation garde les workflows de création légers et concentre la cohérence du graphe sur les moments où l'agent voit déjà la matière typée émerger.

## §2. Checklist commune (6 points)

À dérouler **avant le commit final** d'un cluster de triage ou d'une session. L'ordre est libre, le point 6 (vault-state) reste le dernier.

### 2.1 Intentions consommables

Pour chaque dérivée typée créée pendant l'opération (Atom, Log event, Question, ou la Source-mère du cluster transcripts-import accessible via `source_call` du frontmatter inbox) :

1. Identifier les `people:` mentionnées + le sujet/verbe central.
2. Grep `7-intentions/*.md` :
   - Sur les wikilinks `[[<people-slug>]]` du champ `people:` de l'intention.
   - Sur le verbe d'attaque du slug d'intention (`appeler-`, `parler-`, `lire-`, `voir-`, `rencontrer-`, `apprendre-`, etc.) si la dérivée correspond à ce type d'action.
3. Évaluer la confidence du match.

#### Auto-fermeture (haute confiance, pas de validation)

L'agent ferme **auto** l'intention si **les 3 conditions sont réunies** :

- **Match `people:` exact** : un wikilink commun entre la dérivée et le champ `people:` de l'intention.
- **Match verbe d'attaque exact + médium cohérent** :
  - `appeler-` / `parler-` / `joindre-` + Source `medium: conversation` ou Log event entrevue.
  - `lire-` + Source `medium: book` / `article`.
  - `voir-` / `regarder-` + Source `medium: video`.
  - `rencontrer-` / `revoir-` + Log event ou Source `medium: conversation` en présentiel.
  - `apprendre-` + Source `medium: book` / `video` / `podcast` ou Log event de session/cours.
- **Intention créée dans les 30 jours précédant la dérivée** (`created` ≤ `realized_at` + 30 jours en valeur absolue).

Action auto : passer `status: realized`, renseigner `realized_at: <date dérivée>` (jamais date du triage), ajouter la dérivée dans `sources:`. Signalé dans le bloc LIFECYCLE PRÉ-DÉTECTÉ du brief one-shot triage et dans le diff final.

#### Validation requise (confidence moyenne)

Si **une seule** des 3 conditions manque (people seul, ou verbe seul sans médium cohérent, ou intention >30 jours) : reste validation requise. Listée dans le bloc AMBIGUÏTÉS À LEVER du brief one-shot avec default = ne pas fermer.

Si **aucune** condition ne matche : ignorer, l'intention n'est pas candidate.

Exemple concret. Triage du cluster transcripts-import 2026-05-01 (call Sam). Lifecycle §2.1 grep `7-intentions/` :
- Match sur `[[sam-doe]]` dans `appeler-sam-prendre-nouvelles.md` (people exact).
- Verbe `appeler-` + Source `medium: conversation` (verbe + médium exacts).
- Intention créée 2026-04-30, dérivée datée 2026-05-01 (1 jour, ≤30j).
- **3/3 conditions** → auto-fermeture. `status: realized`, `realized_at: 2026-05-01`, `sources: ["[[2026-05-01-call-sam-nouvelles-philosophie]]"]`.

### 2.2 Questions partiellement répondues

Pour chaque Atom créé qui formalise une réponse, hypothèse ou prise de position :

1. Grep `8-questions/*.md` :
   - Sur le `domain:` de la question (business, philosophy, finance, personal, other) et les tags de l'Atom.
   - Sur les `people:` partagés.
   - Sur les `maps:` partagées.
2. Pour chaque question `status: open` qui matche :
   - Présenter à l'utilisateur : "cet Atom apporte-t-il une réponse partielle à `<question>` ?"
   - **Validation requise**.
   - Si l'utilisateur valide : passer `status: partial` (jamais `answered` automatiquement, c'est une décision plus structurelle), ajouter l'Atom dans `related_atoms:`.
   - Si la question est déjà `partial`, juste enrichir `related_atoms:` (pas de changement de status).
   - Le passage à `status: answered` reste une décision de session dédiée (porte d'entrée Question, voir [[sessions-criteria]] §5 Question).

### 2.3 People last_seen

Pour chaque People mentionnée comme **participant** ou **sujet** d'une dérivée datée (Source `medium: conversation`, Log event, Atom avec date d'événement) :

1. Lire le frontmatter actuel de la People.
2. Si `last_seen` est plus ancien que la date de la dérivée : **mettre à jour en auto** (pas de validation requise, c'est factuel sans risque).
3. Si `last_seen` est null : remplir avec la date de la dérivée.
4. Ne pas toucher si la dérivée n'implique pas une interaction réelle (un Atom qui mentionne X comme sujet sans interaction effective ne met pas à jour `last_seen` de X).

Cas limite : transcripts-import avec participants. Au triage de la première inbox du cluster, mettre à jour `last_seen` de tous les participants listés dans le frontmatter `participants:` de la Source-mère, en utilisant `date_consumed` de la Source.

### 2.4 Map maturity

Pour chaque Map référencée dans `maps:` des notes créées ou modifiées pendant l'opération :

1. Recompter les atoms attachés (grep `1-atoms/*.md` sur `maps:.*[[<map-slug>]]`).
2. Vérifier si une section "Vision" est rédigée dans le body de la Map (au moins 2 lignes de prose, pas juste un placeholder `> [!todo]`).
3. Compter les sous-sections H2 thématiques distinctes dans le body.
4. Appliquer les seuils §3 ci-dessous.
5. Si seuil franchi nettement : **bascule auto** + mise à jour `last_updated`.
6. Si à la frontière (4 atoms ou 14 atoms exactement, ou vision marginale) : proposer à l'utilisateur, validation requise.

### 2.5 Fermeture boucle Source ↔ Atoms

Pour chaque inbox triée vers une note typée pendant l'opération, si cette inbox a un frontmatter `source_call:` / `source_youtube:` / autre champ `source*` qui pointe vers une Source du vault, l'agent ferme la boucle en éditant la Source.

1. Ouvrir la Source pointée.
2. Localiser dans la section `## Atoms à extraire` le bullet textuel correspondant à l'inbox triée. Le slug du bullet est `<YYYY-MM-DD-HHMM-theme>` (= nom de fichier inbox sans extension).
3. Remplacer selon le type produit :
   - **Atom** → `- [[<slug-atom>]]`
   - **Question / Project / Log / Intention / People** → `- [[<slug>]] (<Type>)` avec le type entre parenthèses
   - **Fission en N notes typées** → `- [[<slug-1>]] + [[<slug-2>]]` (et plus si applicable)
   - **Tâche urgente déplacée hors vault, info opérationnelle ou triviale non-atomisable** → retirer le bullet en intégralité, l'info reste portée par le body de la Source. Ajouter en bas de section une note one-liner `Note : <X bullets> retirés (info opérationnelle conservée dans le body).` au moins une fois par cluster pour traçabilité.
   - **`needs_clarification` posé sur l'inbox** → laisser le bullet textuel inchangé, suffixer ` (en attente, needs_clarification)` à la fin du bullet.
4. **Atomes orphelins** : si pendant le triage un Atom (ou autre note typée) est créé qui dérive de la Source mais n'apparaissait pas dans la liste originale (fission, relecture, atom additionnel), l'ajouter en bas de la section avec mention `(atom additionnel dérivé)` ou `(<Type> additionnel dérivé)`.
5. **Renommage H2** : quand toute la liste est devenue 100% wikilinks/notes typées (zéro bullet textuel résiduel), renommer la H2 `## Atoms à extraire` → `## Atoms extraits`. Tant qu'il reste un bullet textuel (résiduel ou `needs_clarification`), la H2 reste `## Atoms à extraire`.

Action **auto**, pas d'interruption. Signalée silencieusement dans le diff final sous forme `Sources fermées : N (cluster)`.

Source d'erreur typique évitée : décalage indéfini entre la liste "à extraire" de la Source et la réalité des atoms produits, nécessitant une opération d'audit rétroactif. Cf. réconciliation 2026-05-08 qui a réparé 13 sources accumulées.

### 2.6 Mise à jour vault-state.md

Voir [[vault-state]] §11 pour la discipline détaillée. Ce point reste inchangé sur le principe : compteurs §1 + append `_meta/vault-state-log.md` (log externalisé depuis le patch doctrine 2026-05-16, rolling 14j) + frontmatter `last_updated` et `last_session_id` de `vault-state.md`.

## §3. Seuils maturity Map (explicites)

| Maturité | Atoms attachés | Vision rédigée | Sous-sections H2 thématiques | Action |
|---|---|---|---|---|
| `stub` | 0 à 4 | optionnelle | optionnelles | Maturity initiale d'une Map fraîchement créée |
| `growing` | 5 à 14 | **obligatoire** | au moins 1 | Bascule depuis `stub` quand seuil atteint |
| `mature` | 15+ | **obligatoire** | au moins 3 | Bascule depuis `growing` quand seuil atteint |

Règles :

- Bascule **auto** si seuil franchi nettement et conditions remplies (passe de 4 à 6 atoms avec vision = `stub` → `growing` auto).
- Bascule **avec validation** si à la frontière exacte (4 atoms ou 14 atoms) ou si vision marginale (1 ligne).
- **Jamais de régression auto** : une Map qui perd des atoms (suppressions, déclassement) ne redescend pas auto. Régression = décision explicite l'utilisateur.
- Mise à jour de `last_updated: <date du jour>` à chaque bascule.

## §4. Création de Map manquante

Trigger : la session courante (triage cluster ou session typée) produit ≥3 atoms qui pointeraient vers une Map qui **n'existe pas encore** dans `5-maps/`, ET cette Map est **recommandée** dans `vault-state.md` §4 (zones sous-représentées) ou §7 (portes recommandées).

### Auto-création (haute confiance)

L'agent crée **auto** la Map si **les 2 conditions sont réunies** :

- Map recommandée par `vault-state.md` §4 ou §7 depuis **≥3 sessions consécutives** (lisible dans `_meta/vault-state-log.md` où la recommandation persiste sans bouger, ou via la formulation explicite "Confirmé par N clusters" dans `vault-state.md` §7). Le log externalisé est le fichier à consulter à la demande pour ce check (cold-start agent NE le charge PAS).
- Cluster courant pousse **≥3 atoms** qui pointeraient vers cette Map.

Action auto :

1. Créer la Map avec :
   - Slug kebab-case (ex: `famille.md`).
   - Frontmatter `type: map`, `domain: <slug>`, `maturity: stub`, `last_updated: <date>`.
   - Section "Vision" en 2-3 lignes, dérivée du contexte de la session et des recommandations vault-state.
   - Section "Atoms attachés" pré-remplie avec les 3+ atoms qui ont déclenché la création.
   - Sections H2 supplémentaires si évidentes depuis la matière (People liées, Sources, Questions ouvertes).
2. Ajouter `maps: [[<nouvelle-map>]]` aux atoms qui la peuplent.
3. Mettre à jour `vault-state.md` §3 (nouvelle ligne dans la cartographie des hubs).

Signalé dans le bloc LIFECYCLE PRÉ-DÉTECTÉ du brief one-shot triage et dans le diff final.

### Proposition (confidence moyenne)

Si **une seule** des 2 conditions manque (ex. recommandée seulement 1 session, ou seulement 2 atoms convergents) : reste proposition. Listée dans le bloc AMBIGUÏTÉS À LEVER du brief one-shot avec default = créer ou ne pas créer selon le poids du faisceau.

Si l'utilisateur refuse : **persister la recommandation**. Ajouter une ligne dans `vault-state.md` §7 si pas déjà présente, avec date et raison du refus si fournie. La proposition pourra revenir à une session ultérieure.

Cas concret en attente au 2026-05-03 : `famille.md` (recommandée par `vault-state.md` §4 et §7 depuis 2026-04-29, ≥3 sessions confirmées). **Auto-création** au prochain triage ou session qui pousse ≥3 atoms famille.

## §5. Patterns de tasks dans le body (clarification, pas nouveau type)

Le pattern checkbox Markdown `- [ ]` / `- [x]` dans le body des Projects et Intentions est **reconnu** comme un usage légitime, pas un nouveau type.

### Projects

Section `## Étapes` (ou `## Roadmap`, `## Jalons`) avec checkboxes Markdown. Exemple existant : `4-projects/signer-partenariat-victor-2026.md`.

Discipline pour l'agent qui touche un Project pendant une session :

- Cocher les étapes réalisées depuis la dernière session (`- [ ]` → `- [x]`).
- Ajouter de nouvelles étapes si la session les fait émerger.
- Conserver les étapes barrées comme historique (ne pas supprimer).

### Intentions

Section `## Premier pas` ou `## Étapes` avec checkboxes possible (pattern moins fréquent mais autorisé).

Discipline : si le `Premier pas` a été franchi, soit le cocher, soit (plus probable) la lifecycle §2.1 a déjà fermé l'intention en `realized`.

### Pas de tracking inter-fichiers

**V1 explicite** : pas de "vue tâches globale" via un champ frontmatter ou un script de tracking. Si l'utilisateur veut une vue d'ensemble, c'est un script lecture-seule qui grep les `- [ ]` non cochés à la demande, pas une donnée stockée dans le frontmatter.

Cette posture sera réévaluée si après plusieurs mois d'usage, l'absence de vue globale pose un vrai problème opérationnel. Voir `doctrine-roadmap.md` pour rouvrir un type `task` éventuel.

## §6. Intégration dans les criteria existants

Lifecycle s'applique aux deux moments de cristallisation typée :

| Criteria | Section | Application lifecycle |
|---|---|---|
| `triage-criteria.md` | §8.2 (en fin de cluster) | **Point d'application principal**. Dérouler `[[lifecycle-criteria]]` §2 avant commit du cluster, pour chaque inbox triagée + la Source-mère si cluster transcripts-import (via `source_call`). |
| `sessions-criteria.md` | §2 phase 7 | Dérouler `[[lifecycle-criteria]]` §2 sur les objets touchés par la session avant commit. |

Et **rappel** dans les workflows créateurs purs :

| Criteria | Section | Rappel |
|---|---|---|
| `transcripts-import-criteria.md` | Phase 8 | Le triage des inbox déclenchera lifecycle. La Source elle-même est candidate à fermer une intention `appeler-`/`parler-` matchant ses participants au triage de la première inbox du cluster. |
| `youtube-import-criteria.md` | Phase 8 ou équivalente | Idem transcripts-import. |
| `journaling-criteria.md` | Phase 9 (commit) | Le triage des dérivées inbox déclenchera lifecycle. |

**Une seule source de vérité, plus de duplication.** Si la checklist §2 évolue, ce fichier est le seul à modifier.

## §7. Règles strictes

1. **Auto autorisé** dans les cas suivants (signalés dans le brief et le diff final) :
   - `last_seen` People mis à jour (factuel sans risque).
   - Bascule Map maturity à seuil franchi nettement (≥6 atoms ou ≥16 atoms avec conditions §3).
   - Fermeture intention si 3 conditions §2.1 réunies (people exact + verbe+médium exacts + ≤30 jours).
   - Création Map manquante si 2 conditions §4 réunies (vault-state ≥3 sessions + ≥3 atoms convergents).
   - Fusion doublon ≥3 signaux convergents avec slug clairement plus stable (cf. `triage-criteria.md` §5).
   - Création People stub minimale (cf. `triage-criteria.md` §7.1).
   - Recompte vault-state §1, append `_meta/vault-state-log.md`.
2. **Validation l'utilisateur requise** dans les cas restants (confidence moyenne) :
   - Question `open` → `partial` (toujours validation, contenu cognitif).
   - Question `partial` → `answered` (jamais auto, décision structurelle).
   - Bascule Map à la frontière (4 ou 14 atoms exactement).
   - Fermeture intention avec une seule condition §2.1 manquante.
   - Création Map avec une seule condition §4 manquante.
   - Fusion doublon à confidence moyenne (2 signaux ou slug pas clairement plus stable).
   - Désambiguïsation sans discriminant clair.
   - **Suppression de note inbox** (toujours, via brief one-shot uniquement).
3. **Pas d'em dash** dans les modifications de body ou frontmatter (règle CLAUDE.md).
4. **Pas de régression auto** : une intention `realized` ne redevient pas `active`, une Map `growing` ne redevient pas `stub` sans décision l'utilisateur.
5. **Préservation factuelle** : si la dérivée date du 2026-05-01, `realized_at: 2026-05-01` (jamais la date du triage qui a fermé l'intention).
6. **Cardinalité respectée** : l'agent regroupe les actions auto et propositions dans le brief one-shot et le diff final, sans chercher à les noyer. Si une session produit >10 fermetures auto + >5 propositions, signaler que c'est un cluster anormalement dense et proposer de scinder en deux triages.

## §8. Pour un agent qui démarre de zéro

Si tu es un agent (Claude Code iPhone, agent cloud, script tiers) qui exécute un triage ou une session sans contexte préalable :

1. Lis `CLAUDE.md` à la racine.
2. Lis le criteria de l'opération en cours (`triage-criteria.md` ou `sessions-criteria.md`).
3. Lis ce fichier (`_meta/lifecycle-criteria.md`).
4. Applique le criteria de l'opération, puis avant le commit final, déroule la checklist §2.
5. Tu es 100% autonome.

## §9. Tone

Ce fichier est opérationnel. Pas d'em dash. Pas de flatterie. Si un match lifecycle est ambigu (confidence basse), signaler à l'utilisateur plutôt que de proposer arbitrairement.

Une question à la fois quand plusieurs propositions de fermeture sont à valider : grouper visuellement mais demander oui/non par item, pas un bloc opaque.

## §10. Audit legacy via linter (rattrapage des dérives accumulées)

La lifecycle telle que codifiée ici corrige le flux nouveau (à partir du prochain triage ou session). Pour rattraper les dérives accumulées **avant** la création de cette doctrine (2026-05-03) ou les oublis ponctuels d'agents, un linter lecture-seule est disponible :

```bash
python3 _meta/scripts/lifecycle-lint.py
```

### Workflow

1. Le script scanne le vault en lecture seule et détecte les 5 catégories de dérives (cf. `_meta/scripts/README.md`).
2. Il dépose une **note inbox** `0-inbox/<YYYY-MM-DD-HHmm>-lifecycle-audit-<résumé>.md` avec frontmatter `device: lifecycle-audit`.
3. Au prochain triage low-friction, l'agent détecte la note via `[[triage-criteria]]` §0bis et l'intègre en tête du brief one-shot (§10) comme input premier de classe.
4. Les actions auto-confidence (3/3 conditions §2.1, 2/2 conditions §4) sont appliquées sans validation. Les actions manual-confidence passent par le brief avec defaults publiés.
5. La note inbox est absorbée à la fin du triage.

### Quand lancer le linter

- En rattrapage initial post-création de la doctrine lifecycle (1 fois pour nettoyer le legacy).
- Hebdomadaire dans le rituel `[[rituals]]` (cf. fichier rituals).
- Après un sprint de captures intenses (transcripts-imports répétés, journaling quotidien sur 2 semaines, etc.) si un soupçon de dérive accumulée existe.

Le linter ne remplace pas la doctrine, il **rattrape** ce que la doctrine n'a pas pu attraper en flux. Si tu lances le linter et qu'il ne trouve rien, c'est que la doctrine fonctionne.
