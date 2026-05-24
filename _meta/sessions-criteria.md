---
type: meta
purpose: doctrine des sessions de travail dans le vault, utilisée par tous les agents (skill local, Claude Code Mac, Claude Code on the Web depuis iPhone, agents cloud, scripts tiers)
version: v1
status: active
created: 2026-04-26
last_updated: 2026-04-29
---

<!--
Changelog : externalisé vers _meta/doctrine-changelog.md (consulté à la demande).
Doctrine V1 anonymisée, packagée comme produit SAMPL-IQ.
-->

# Critères de session de travail

Source de vérité unique pour le workflow d'une session de travail dans le vault. Une "session" est un échange dirigé entre l'utilisateur et un agent qui produit des modifications structurelles dans `1-atoms/`, `2-people/`, `3-sources/`, `4-projects/`, `5-maps/`, `6-logs/`, `7-intentions/`, `8-questions/`. Distinct d'une capture (qui crée une note dans `0-inbox/` sans la classer) et d'un triage (qui classe l'inbox sans interview approfondie).

Ce fichier est **self-contained** : un agent qui n'a accès qu'au repo (cloud session, iPhone, autre machine) peut lire ce fichier + `_meta/conventions.md` + `_meta/vault-doctrine-v1.md` + `_meta/identite-civile.md` et exécuter une session de bout en bout.

Voir aussi : [[vault-doctrine-v1]] (les 8 types), [[conventions]] (schemas frontmatter), [[triage-criteria]] (heuristiques de classification, réutilisées au §1), [[identite-civile]] (cercle proche de l'utilisateur, utile pour résoudre les références People).

## §0. Principe directeur

**Effet "système neuronal".** Toute session de travail enrichit le graphe complet du vault, pas seulement l'objet d'entrée. Une session qui modifie un seul fichier sans produire d'objets dérivés (atoms, cross-links, stubs, questions, intentions, etc.) est un échec.

La porte d'entrée est un prétexte. Le vrai produit d'une session, c'est l'irrigation du réseau : nouveaux atoms qui formalisent ce qui émerge, cross-links qui consolident le maillage, stubs People qui ouvrent de futurs enrichissements, questions ou intentions déclenchées. Pas de mise à jour isolée.

## §1. Portes d'entrée possibles

Les 8 types peuvent servir de point de départ, plus un mode "free roam" où l'agent choisit la cible. Identifier la porte d'entrée à partir de la phrase de l'utilisateur via les signaux ci-dessous (réutilise les heuristiques de [[triage-criteria]] §1, adaptées au cas "session" au lieu de "classement").

| Porte d'entrée | Signal d'invocation | Exemple de phrase |
|---|---|---|
| People | "enrichir X", "session amis", "famille", "team" | "viens on enrichit Sam" |
| Question | "creuser", "répondre à", "explorer la question" | "creuse pourquoi-allergie-subordination" |
| Map | "enrichir le domaine", "élargir la map", "auditer" | "élargis la map permaculture" |
| Atom | "approfondir cette idée", "creuser cet atom" | "approfondis l'atom X" |
| Source | "exploiter cette lecture", "extraire de" | "extrais des atoms du livre Camus" |
| Project | "faire le point", "statuer", "où en est" | "où en est le projet Y" |
| Intention | "statuer", "promouvoir en project", "trancher" | "statue sur l'intention Z" |
| Log | "retour réflexif", "extraire du log" | "extrais des atoms du log de mardi" |
| Free roam | "j'ai 30 min", "propose", "pioche", "let's go", "parcours" | "let's go, parcours mon vault" |

En cas d'ambiguïté (deux portes d'entrée plausibles), demander à l'utilisateur plutôt que trancher seul.

## §2. Workflow générique de session

Huit phases, indépendantes du type d'entrée :

0. **Lire [[vault-state]]** : avant tout, l'agent lit `_meta/vault-state.md` pour s'orienter sur l'état actuel du vault (compteurs, hubs, zones sous-représentées, recommandations §7). Si l'utilisateur n'a pas de porte d'entrée explicite et que c'est une session free roam, utiliser §7 du vault-state comme première source de candidats (§4 ci-dessous reste la méthode de calcul dynamique en complément).
1. **Identifier la porte d'entrée** (§1). Si free roam, basculer en §4.
2. **Lire l'existant** : le fichier d'entrée + ses backlinks proches (grep des wikilinks `[[<slug>]]` dans les autres fichiers du vault). Pour une People, lire aussi son cluster `related_people` et `met_through`.
3. **Phase d'interview** : paliers de questions adaptés au type (§5). Une question à la fois (§6).
4. **Détecter les ramifications** : objets dérivés à créer ou enrichir (atoms, cross-links, people stubs, maps, questions, intentions, projects, logs). **Étape obligatoire**, c'est elle qui garantit l'effet graphe (§0).
5. **Présentation bloc + validation** : l'agent présente la liste consolidée des objets à toucher (créations + modifications + cross-links) avant toute écriture. L'utilisateur valide en bloc, corrige, ou skippe. L'agent ne crée RIEN tant que cette validation n'est pas obtenue.
6. **Création / modification / commit** : suivre les schemas de [[conventions]], les conventions de nommage, les patterns de wikilink. Commit selon §7. Si cloud session, créer la PR à la fin (§8).
7. **Dérouler [[lifecycle-criteria]] §2 + mettre à jour [[vault-state]]** : avant le commit final (ou dans un commit dédié si plus pratique), l'agent déroule la checklist de clôture aval ([[lifecycle-criteria]] §2 en 6 points : intentions consommables, questions partial, People last_seen, Map maturity, fermeture boucle Source ↔ Atoms (§2.5), Map manquante recommandée par vault-state) puis met à jour le dashboard `vault-state.md`. Au minimum vault-state : §1 (compteurs si notes créées/supprimées), §2 (complétude YAML si atoms touchés), **append `_meta/vault-state-log.md`** (log externalisé depuis vault-state §9 au patch doctrine 2026-05-16, rolling 14j, 1 ligne avec date, type de session, résumé court <30 mots), frontmatter `last_updated` et `last_session_id` de vault-state.md. Sections §3 à §7 mises à jour seulement si la session a fait évoluer significativement un hub, une zone, une question prioritaire, une intention. Voir [[vault-state]] §11 pour la discipline détaillée vault-state, et [[lifecycle-criteria]] §2-§4 pour la lifecycle complète.

## §3. Modes de session

- **Mode A, porte d'entrée explicite** : L'utilisateur donne l'objet de départ. L'agent applique §2.
- **Mode B, free roam** : L'utilisateur ne donne pas d'objet. L'agent applique §4 pour proposer une cible, puis bascule en §2 une fois la cible choisie.

## §4. Heuristiques free roam

Quand l'utilisateur dit "propose", "j'ai 30 min", "let's go", l'agent ne devine pas, il consulte [[vault-state]] §7 (recommandations pré-calculées par la dernière session) et calcule dynamiquement les candidats restants, puis présente top 3 à 5.

**Méthode de calcul** : combiner deux sources :

1. [[vault-state]] §7 : recommandations explicites mises à jour à la fin de chaque session précédente. Avantage : porte la mémoire entre sessions, permet de pousser une zone sous-représentée sur plusieurs sessions consécutives.
2. Grep dynamique du vault au moment de la session (méthode ci-dessous). Avantage : capture les évolutions depuis la dernière mise à jour de vault-state, et les candidats émergents.

Si vault-state §7 et le grep proposent la même cible, c'est un signal fort. Si vault-state propose une cible que le grep n'a pas relevée, la garder dans la liste : c'est probablement une zone qu'on enrichit à dessein sur plusieurs sessions.

Catégories de candidats :

- **People stubs** : fichiers dans `2-people/` dont le corps fait moins de 50 lignes ou dont le frontmatter a beaucoup de champs `null`/`[]`. Prioriser les People du cercle proche listé dans [[identite-civile]] (partenaire, famille, futurs people stubs créés lors de sessions précédentes).
- **Maps stubs** : fichiers dans `5-maps/` avec frontmatter `maturity: stub`. Au moment d'écriture de ce fichier : `geographie-nomadisme`, `hygiene-de-vie`, `second-brain`, `sports-adrenaline`. Recalculer à chaque session (peut avoir évolué).
- **Questions ouvertes** : fichiers dans `8-questions/` avec frontmatter `status: open`. Prioriser `priority: high` puis `domain` qui correspond à l'humeur ou au contexte mentionné par l'utilisateur.
- **Atoms isolés** : fichiers dans `1-atoms/` sans `maps:` ni backlinks (autre que leur source d'origine). Candidats à raccrocher au graphe.
- **Intentions sans statut clair** : fichiers dans `7-intentions/` avec `status: active` sans `priority` ou sans `horizon`, ou `status: dormant` depuis plus de 3 mois.
- **Projects en attente de point** : fichiers dans `4-projects/` avec `status: active` dont le dernier commit qui les touche date de plus de 30 jours.
- **Sources `to-read` ou `reading` depuis longtemps** : fichiers dans `3-sources/` avec `status: to-read` ou `reading` antérieur à 60 jours.

**Format de proposition** : présenter top 3 à 5 candidats avec une ligne chacun :

```
Free roam, voici ce qui mérite d'être attaqué (30 min) :

1. [[nina-smith]] : People stub, cousine Flora, jamais enrichie. Cluster Smith.
2. [[hygiene-de-vie]] : Map stub, 0 atom rattaché, sujet récurrent dans tes captures.
3. [[pourquoi-allergie-subordination]] : Question open priority high, déclenchée le 2026-04-26, jamais creusée.
4. [[apprendre-echecs-2026]] : Intention active sans horizon, status dormant depuis 2 mois.
5. [[acme-survit-commoditisation-ia]] : Question business open, deadline implicite cycle de planning Acme.

Sur quoi tu veux taper ?
```

Attendre le choix, basculer en §2 avec la porte d'entrée correspondante.

## §5. Protocoles spécifiques par type d'entrée

Paliers de questions adaptés au type. Une question à la fois (§6). Adapter au contexte (passé pour les décédés, skip si question intrusive, etc.).

### People

Pattern de référence : [[leo-doe]] (gold standard, 311 lignes, structure de sections H2 dense).

Paliers :
1. **Facts civils** (5 questions max) : nom complet, date de naissance, ville actuelle, ville d'origine, profession actuelle, structure familiale immédiate.
2. **Histoire relationnelle** (3 à 5) : comment vous vous êtes rencontrés, événements structurants partagés, dernière interaction marquante, fréquence de contact actuelle.
3. **Ce que la personne incarne** (3 à 5) : ce qu'elle t'a transmis (positif et négatif), ses traits de caractère saillants, sujets sur lesquels elle est référente pour toi, frictions historiques.
4. **Connexions au reste du vault** (2 à 3) : qui d'autre la connaît dans ton cercle, quelle Map elle peuplerait naturellement, quels atoms elle a inspirés ou pourrait inspirer.

Sections H2 typiques de la note finale : Contexte, Famille d'origine, Trajectoire pro, Histoire, Dynamique aujourd'hui, Transmissions, Friction historique, Sujets partagés, Idées cadeau, Historique, Liens, TODO.

Adaptations :
- Décédés : tout au passé, ajouter `death_date` au frontmatter, ne pas demander "dernière interaction".
- Famille alliée connue de loin : skip palier 3 si la matière est trop fine, ne pas forcer.
- Question intrusive (santé, divorce, secrets) : skip silencieux si l'utilisateur refuse.

Dérivés probables : atoms (idées extraites des transmissions et frictions), people stubs (membres mentionnés du cercle), cross-links (vers autres People, Maps, Projects), questions ouvertes (sur la relation), intentions (rattraper, proposer un échange).

### Question

Paliers :
1. **Contexte / déclencheur** : qu'est-ce qui a fait surgir cette question, pourquoi maintenant, quelle décision elle bloque ou éclaire.
2. **Pistes initiales** : intuitions de réponse, angles d'attaque, hypothèses qui te traversent l'esprit.
3. **Sources à consulter** : lectures à faire, gens à qui demander, expériences à tenter.
4. **Hypothèse de réponse partielle** : si l'interview fait émerger une réponse provisoire, la formaliser comme `## Réponse partielle` dans la note.

Dérivés probables : atoms (réponses partielles formalisées, hypothèses stables), intentions (engagements à explorer une piste), projects (si une piste cristallise en plan d'action borné), people stubs (gens à interroger), questions filles (sous-questions qui émergent).

Si le statut bascule de `open` à `partial` ou `answered`, mettre à jour le frontmatter (`status`, `answered_at`).

### Map

Paliers :
1. **Vision en 1-2 phrases** : qu'est-ce que ce domaine pour l'utilisateur aujourd'hui, comment il le formulerait à un tiers.
2. **Atoms reliés (audit + nouveaux)** : lister les atoms qui sont déjà rattachés via `maps: [[<slug>]]`, identifier ceux qui devraient l'être (grep), proposer de nouveaux atoms à extraire de la conversation.
3. **Questions ouvertes du domaine** : interrogations stables qui structurent la pensée de l'utilisateur sur ce sujet.
4. **People / Sources / Projects connectés** : qui pratique ce domaine dans son cercle, quelles sources l'ont nourri, quels projects en relèvent.

Si la Map passe de `maturity: stub` à `growing` (au moins 5 atoms rattachés et une vision rédigée), mettre à jour le frontmatter et `last_updated`.

Dérivés probables : atoms (vision distillée, principes), questions (creux à explorer), cross-links massifs (toute la Map est un hub), people stubs (références du domaine).

### Atom

Paliers :
1. **Approfondir l'idée** : nuances, contre-exemples, conditions de validité, cas limites.
2. **Sources / People qui en parlent** : qui ou quoi a formulé cette idée mieux ou différemment, références à creuser.
3. **Maps qui devraient le contenir** : à quel hub cet atom appartient. Mettre à jour `maps:` si un rattachement manque.

Dérivés probables : atoms voisins (nuances qui méritent leur propre note), cross-links, questions (si l'idée révèle une zone d'ombre), sources à explorer.

### Source

Paliers :
1. **Résumé en 3 idées clés** : ce que la source apporte, formulé en 3 atomes potentiels.
2. **Atoms à extraire** : pour chaque idée clé, une note Atom dérivée avec `source: [[<slug-source>]]`.
3. **Maps reliées** : à quels domaines cette source appartient.
4. **People qui devraient lire ou connaître** : à qui de ton cercle tu recommanderais, qui pourrait être impacté.

Mettre à jour `status` (`to-read` → `read`, `date_consumed`, `rating`).

Dérivés probables : atoms (le coeur de la session), cross-links Maps et People, intentions (lectures liées à explorer ensuite).

### Project

Paliers :
1. **Statut actuel** : où en est concrètement le projet, qu'est-ce qui a bougé depuis le dernier commit qui le touche.
2. **Jalons restants** : prochaines étapes opérationnelles, deadlines, bloqueurs.
3. **Frictions / risques** : ce qui freine, hypothèses non vérifiées, décisions non tranchées.
4. **Atoms à extraire des décisions prises** : ce qui mérite d'être formalisé hors du project (principes, règles, learnings).

Si `status` doit changer (`active` → `paused` / `done` / `abandoned`), mettre à jour le frontmatter.

Dérivés probables : atoms (learnings, principes émergents), logs decision (décisions tranchées pendant la session), intentions (suites possibles post-projet), people stubs (parties prenantes mentionnées).

### Intention

Paliers :
1. **Toujours pertinente ?** : est-ce que cette intention résonne encore, ou est-ce qu'elle a perdu sa charge.
2. **Horizon clarifié ?** : si `horizon: someday` peut basculer en `years` ou `months` parce que la matière a mûri.
3. **Promotion en project** ? : si le scope cristallise (verbe d'action + objectif borné + étapes en germe), créer un Project dérivé et basculer l'Intention en `realized` ou la conserver comme parent.
4. **Atoms si pensée stable** : si la session fait émerger une affirmation stable qui sous-tend l'intention, l'extraire en Atom.

Si `status` doit changer (`active` → `realized` / `abandoned` / `dormant`), mettre à jour le frontmatter avec `realized_at` ou `abandoned_at` + `abandoned_reason` selon le cas.

Dérivés probables : project (si cristallisation), atoms (pensée stable sous-jacente), intentions filles (sous-engagements).

### Log

Paliers :
1. **Atoms à extraire** : qu'est-ce qui dans cet événement mérite d'exister comme idée stable hors du log.
2. **Cross-links People / Projects** : qui apparaît dans le log et n'est pas encore lié, quels projects sont touchés.
3. **Questions ou intentions déclenchées** : l'événement a-t-il ouvert un creux à explorer ou un engagement à prendre.

Cocher les `Atoms à extraire` du log au fur et à mesure de leur création.

Dérivés probables : atoms (le coeur), cross-links, questions, intentions.

## §6. Règles de session communes

- **Une question à la fois.** Jamais de bloc de questions. Posture sparring partner, pas thérapeute.
- **Préservation des datas factuelles.** Pas de paraphrase, pas de compression. Les noms, dates, chiffres, citations exactes restent verbatim.
- **Pas d'invention.** Si une réponse est incomplète ou inconnue, laisser le champ `null` ou la section vide. Jamais de fait inventé pour combler un trou.
- **People manquante mentionnée** pendant l'interview : la signaler à la fin pour création de stub, ne pas la créer en cours d'interview (perturbe le flow).
- **"skip" et "pause"** sont obéis sans débat. Skip silencieux : l'agent reformule ailleurs ou passe au palier suivant.
- **Pas de plafond d'objets dérivés.** La règle "max 3 atoms par session" est explicitement abandonnée. Présenter tout ce qui mérite d'exister, l'utilisateur trie en bloc.
- **Reprise après interruption avec transcripts en bloc** : si l'utilisateur fournit un bloc de transcripts vocaux ou textuels au lieu de répondre interactivement, matcher implicitement question/réponse, structurer en paliers, présenter directement l'inventaire d'objets dérivés (ne pas rejouer l'interview).
- **No em dash** dans tout contenu écrit (le caractère `—`). Utiliser virgules, deux-points, parenthèses, ou retour à la ligne.
- **Discipline tags** : pour toute note typée créée ou enrichie pendant la session, suivre `[[tag-hygiene-criteria]]` au moment de poser des tags. Nomenclature `racine/sous-tag` (2 niveaux strict), 11 racines actuelles évolutives. Si l'idée touche un domaine absent des racines actuelles, proposer une nouvelle racine à l'utilisateur (procédure §5 du fichier), ne pas forcer.

## §7. Patterns de commit par porte d'entrée

| Porte d'entrée | Pattern de message |
|---|---|
| People | `👤 enrichissement: <prenom-nom> + <résumé>` |
| Question | `❓ creusage: <slug-question> + <résumé>` |
| Map | `🗺️ enrichissement map: <slug-map> + <résumé>` |
| Atom | `🔬 approfondissement: <slug-atom> + <résumé>` |
| Source | `📖 exploitation: <slug-source> + <résumé>` |
| Project | `📋 point projet: <slug-project> + <résumé>` |
| Intention | `🎯 statut intention: <slug-intention> + <résumé>` |
| Log | `🪞 retour log: <slug-log> + <résumé>` |
| Free roam multi-cibles | `🌱 free-roam: <résumé des objets touchés>` |

`<résumé>` doit lister les objets dérivés clés en notation compacte, par exemple `+ 6 atoms / 3 people stubs / 2 cross-links`.

## §8. Workflow Cloud session (Claude Code on the Web depuis iPhone, agent cloud)

Quand l'agent tourne dans une cloud VM Anthropic (lancée depuis claude.ai/code ou l'app Claude iOS), pas sur le Mac de l'utilisateur :

1. La cloud session crée automatiquement une branche `claude/<slug-auto>` poussée sur `origin`. Tu n'as pas besoin de la créer toi-même.
2. **Ne push JAMAIS direct sur `main` depuis une cloud session.** Si tu détectes que la branche courante est `main`, créer une branche dédiée avant tout commit (`git checkout -b claude/session-<YYYY-MM-DD>-<porte-entrée>`).
3. À la fin de la session, **créer la PR** via `gh pr create`. Format :
   - Titre = pattern de commit principal de la session (§7).
   - Body = liste des objets touchés (créations / modifications / cross-links) + résumé des décisions structurelles prises.
4. Si `gh` n'est pas authentifié dans la cloud VM, **signaler explicitement à l'utilisateur** : "branche poussée sur `claude/<slug>`, PR à créer manuellement, voici la commande : `gh pr create --title '...' --body '...'`". Ne pas tenter de bypass.
5. Confirmer à l'utilisateur en fin de session :
   - Nom de la branche.
   - URL de la PR ouverte (retournée par `gh pr view` ou `gh pr create`). **Pas de fin de session sans PR liée.**
   - Résumé compact des objets touchés.
6. **Pas de branche orpheline.** Si tu pousses une branche `claude/<slug>`, tu DOIS créer la PR avant la fin de la session (ou demander à l'utilisateur de la créer si gh auth manque). Le repo a le setting GitHub "Automatically delete head branches" activé, donc le cleanup est event-driven sur close ou merge de PR. Une branche poussée sans PR est un état illégal qui contourne le cleanup auto et oblige l'utilisateur à supprimer la branche à la main.

Tu n'as PAS accès aux skills locaux de `~/.claude/skills/` (ils ne sont pas clonés en cloud session, par design Anthropic). Tu n'as PAS accès à la memory locale de Claude Code Mac. Toute la doctrine dont tu as besoin vit dans le repo : ce fichier, [[conventions]], [[vault-doctrine-v1]], [[identite-civile]], plus les `_meta/templates/<type>.md`.

## §9. Pour un agent qui démarre de zéro

Si tu es un agent (Claude Code on the Web, agent cloud, script tiers) qui n'a accès qu'au repo et à rien d'autre :

1. Lis `CLAUDE.md` à la racine.
2. Lis ce fichier (`_meta/sessions-criteria.md`) en entier.
3. Lis `_meta/conventions.md` (schemas frontmatter et conventions de nommage).
4. Lis `_meta/identite-civile.md` (cercle proche de l'utilisateur, utile pour la résolution des références People).
5. Selon la porte d'entrée détectée, lis le template correspondant dans `_meta/templates/<type>.md`.
6. Pour une session People, lis `2-people/leo-doe.md` comme gold standard.
7. Applique les §2 à §10.

Tu es 100% autonome avec ces 6 ou 7 fichiers. Aucune autre dépendance externe. Aucun skill local requis.

Si l'utilisateur te donne une instruction très courte ("creuse pourquoi-allergie-subordination", "let's go, parcours mon vault"), c'est suffisant : ce fichier contient tout ce qu'il faut pour transformer cette phrase en session productive.

## §10. Sortie Source conversation pour sessions longues

Une session longue (réflexion structurée > 30 min, brainstorm stratégique, prep de call important, design doc cognitif) produit une matière conversationnelle qui a une valeur propre, distincte des objets dérivés (atoms, people enrichies, etc.). Cette matière mérite d'être archivée dans le vault comme **Source conversation** : livrable propre en sortie, exploitable comme source par les sessions futures.

### Distinction plan file vs Source conversation

| Artéfact | Localisation | Rôle | Lifecycle |
|---|---|---|---|
| **Plan file Claude Code** | `~/.claude/plans/<slug>.md` (hors-vault, hors-repo) | Working memory pendant la session, brouillon, peut être désordonné, évolue à chaque tour | Vit le temps de la session, reste accessible localement après mais pas synced cross-device |
| **Source conversation** | `3-sources/YYYY-MM-DD-<slug>.md` | Livrable final propre, structuré, exploitable comme source par les sessions futures et les autres agents | Permanent, indexé, exploité par triages et transcripts-imports ultérieurs |

Le plan file est un brouillon pour penser. La Source conversation est un artéfact pour transmettre.

### Trigger de production

Produire une Source conversation quand au moins UN des critères est vrai :

- La session a duré > ~30 min de réflexion structurée (pas un simple Q&A court).
- La session a produit ≥ 5 décisions ou pivots qu'un futur agent ou l'utilisateur ré-exploitera (préparation call, brainstorm stratégique, design doc, audit doctrine).
- La session a généré une matière conversationnelle de valeur cognitive propre, distincte des dérivés. Test décisif : "si je supprime le plan file, est-ce que je perds quelque chose qui n'est pas déjà dans les atoms / people / questions / etc. dérivés ?". Si oui : Source à produire.

NE PAS produire de Source pour :
- Sessions courtes (< 15 min) ou Q&A purs.
- Sessions qui produisent directement leurs dérivés sans matière conversationnelle additionnelle (enrichissement People simple, triage classique, capture).
- Sessions où l'utilisateur demande explicitement de ne pas garder de trace.

### Slug et localisation

Convention `conventions.md` §"Cas particulier conversation" : préfixe date obligatoire puisque pas d'auteur canonique unique.

```
3-sources/YYYY-MM-DD-<sujet-court>-<contexte>.md
```

Pattern `conversation-claude-<sujet>` recommandé pour cohérence avec l'existant. D'autres formes admises si plus parlantes.

Exemples :
- `2026-04-27-conversation-claude-prep-call-client.md`
- `2026-04-25-conversation-claude-doctrine-vault.md`

### Frontmatter

```yaml
---
type: source
medium: conversation
author: Claude Code (<contexte agent>) + l'utilisateur Doe
date_consumed: YYYY-MM-DD
status: read
rating: <1-5 ou null>
tags: [<tags pertinents>]
participants:
  - "[[john-doe]]"
  - "[[<autre-people-mentionnée>]]"   # optionnel, uniquement si fiche existe
plan_file: <chemin absolu plan file Claude Code>   # optionnel, traçabilité
---
```

Notes :
- `author` : identifier le contexte agent. Exemples : `Claude Code (Mac local) + l'utilisateur Doe`, `Claude Code (cloud session) + l'utilisateur Doe`, `Claude Code (iPhone) + l'utilisateur Doe`.
- `participants` : wikilink uniquement les People avec fiche existante (`conventions.md` §Source : "ne pas inventer le wikilink").
- `plan_file` : métadonnée traçabilité optionnelle, pas dans schema canonique mais admise pour pointer vers la working memory hors-vault.

### Workflow

1. La Source conversation est produite en **fin de session**, après la phase 6 du §2 (création des objets dérivés). Elle consolide la matière brute, ne la remplace pas.
2. Cross-link bidirectionnel : les atoms produits dans la même session doivent référencer la Source via `source: [[<slug-source>]]`. La Source contient une section "Atoms extraits" qui liste les wikilinks vers les atoms produits.
3. Corps de la Source : reproduit la structure de la session (sujet, faits clés, décisions, pivots, branches, action immédiate, notes dérivables). Format libre tant que lisible et ré-exploitable.
4. Préservation des datas factuelles (§6) : pas de paraphrase ni compression destructive. Citations, dates, chiffres restent verbatim.

### Hygiène, à ne PAS faire

- **Pas de fichier "checkpoint" dans le vault** (`_meta/`, `0-inbox/`, `3-sources/`, ou ailleurs). Le checkpoint en cours de session vit UNIQUEMENT dans le plan file Claude Code (`~/.claude/plans/`).
- **Pas de type nouveau** pour stocker une session en cours (`type: session-backup`, `type: scratch`, etc.). La doctrine est explicite : 8 types, point. Voir `CLAUDE.md` §"Règles comportementales".
- **Pas de nouveau dossier dans `_meta/`** pour du contenu. `_meta/` = doctrine pure, jamais contenu.
- La Source conversation est la **seule** sortie vault d'une session longue. Pas d'alternative parallèle.

### Cas où l'utilisateur ne veut pas de Source

Si l'utilisateur dit "pas besoin de garder la trace de cette session" ou équivalent, l'agent NE produit PAS de Source. Le plan file Claude Code reste accessible localement, c'est suffisant. Pas d'insistance.
