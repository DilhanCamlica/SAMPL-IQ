# CLAUDE.md

Bienvenue dans un vault Obsidian SAMPL-IQ. Ce fichier te donne le contexte minimal pour interagir avec ce vault.

> [!important] Première lecture
> Si tu arrives ici pour la première fois (Claude Code Mac, Claude Code iPhone, agent cloud, machine sans skills locaux installés), lis `ONBOARDING.md` à la racine AVANT ce fichier. Il explique le concept, l'installation, l'architecture multi-appareils et tous les flux. Ce `CLAUDE.md` se concentre sur les règles d'interaction avec un vault déjà en place.

## Qui est l'utilisateur

Voir `_meta/identite-civile.md` pour les facts civils objectifs (état civil, géographie, structures pro, cercle proche immédiat). Ce fichier ne contient PAS de contenu cognitif (philosophie, valeurs, vision). Pour ça, va dans `5-maps/`. Sur un vault neuf, ce fichier est un template à remplir.

## Comment ce vault est organisé

8 types de notes, chacun dans son dossier numéroté : `1-atoms/`, `2-people/`, `3-sources/`, `4-projects/`, `5-maps/`, `6-logs/`, `7-intentions/`, `8-questions/`. Plus `0-inbox/` pour les captures non triées et `_meta/` pour la doctrine.

Les règles complètes vivent dans `_meta/`. Lis dans cet ordre selon ta tâche :

- Comprendre la philosophie globale du vault : `_meta/vault-doctrine-v1.md`
- Schemas YAML et conventions de nommage : `_meta/conventions.md`
- **S'orienter sur l'état actuel du vault** (compteurs, hubs, zones sous-représentées, recommandations de session) : `_meta/vault-state.md`. À lire systématiquement après ce CLAUDE.md, et à mettre à jour en fin de session si tu as créé / modifié des notes typées.
- **Deux fichiers `_meta/` à NE PAS charger en cold-start, consultés à la demande uniquement** : `_meta/vault-state-log.md` (log append-only des sessions, rolling 14 jours) et `_meta/doctrine-changelog.md` (historique des évolutions de la doctrine). Va dans ces fichiers seulement à la demande : retracer une décision, vérifier qu'une Map est recommandée depuis ≥3 sessions, comprendre l'historique complet d'une règle.
- Trier l'inbox : `_meta/triage-criteria.md` (workflow complet, self-contained)
- Capturer une nouvelle note : `_meta/capture-criteria.md` puis `_meta/toilettage-rules.md` (nettoyage texte)
- Importer un transcript de call (Grain, tl;dv, Fathom, Fireflies, Zoom, ou texte collé) : `_meta/transcripts-import-criteria.md` (workflow complet, self-contained)
- Importer un transcript de vidéo YouTube via une URL : `_meta/youtube-import-criteria.md` (workflow complet, self-contained)
- Lancer une session de travail (enrichir une People, creuser une Question, élargir une Map, free roam, etc.) : `_meta/sessions-criteria.md` (8 portes d'entrée + mode free roam, self-contained)
- **Clôture aval après triage ou session** (fermer une intention consommée, basculer une Map de stub à growing, mettre à jour `last_seen` People, fermer la boucle Source ↔ Atoms, créer une Map manquante recommandée) : `_meta/lifecycle-criteria.md` (checklist en 6 points). Déroulée par `triage-criteria.md` et `sessions-criteria.md`. Le transcripts-import, le youtube-import, le journaling et la capture restent des créateurs purs et NE déclenchent PAS la lifecycle eux-mêmes.
- Rituel journal quotidien : `_meta/journaling-criteria.md` (détecté par `triage-criteria.md` §0)
- Hygiène des tags (pose courante + cleaning relançable) : `_meta/tag-hygiene-criteria.md`
- Lancer un grill-me : `_meta/grill-criteria.md`
- **Visualiser le graphe Obsidian** (filtres, palettes, presets swappables depuis terminal) : `_meta/graph-presets/README.md`. Activables par `bash _meta/graph-presets/swap.sh <nom>`. Preset baseline = `macro`.

## Architecture mobile / Cloud session

Les fichiers `_meta/*.md` sont la source de vérité unique. Les skills locaux (`~/.claude/skills/obsidian-*`) sont de simples pointeurs vers ces fichiers, installés sur la machine de l'utilisateur (voir `ONBOARDING.md` §3.5).

Si tu es invoqué depuis Claude Code on the Web (cloud VM) ou un agent distant, tu n'as PAS accès aux skills locaux ni à la memory locale. Toute la doctrine vit dans le repo. Workflow obligatoire :

1. Lis `ONBOARDING.md`, ce `CLAUDE.md`, puis le fichier `_meta/<x>-criteria.md` correspondant à ta tâche. Ces fichiers sont self-contained.
2. **Ne push JAMAIS direct sur `main` depuis une cloud session.** Crée une branche dédiée avant tout commit.
3. À la fin de la session, **crée une PR** via `gh pr create` (titre = pattern de commit principal, body = liste des objets touchés).
4. Si `gh` n'est pas authentifié dans la cloud VM, signale-le explicitement avec la commande à lancer manuellement. Ne pas tenter de bypass.
5. Confirme en fin de session : nom de branche, URL de la PR (ou commande à lancer), résumé compact des objets touchés.

**Exception** : pour une capture inbox, le push immédiat sur la branche courante reste obligatoire (voir `_meta/capture-criteria.md`).

## Règles comportementales

- Ne modifie JAMAIS la doctrine (`_meta/*.md` et `_meta/graph-presets/presets/macro.*`) sans validation explicite de l'utilisateur. Pour les autres presets graph (non-macro), modification possible avec validation note par note.
- Ne crée JAMAIS de nouveau type de note (au-delà des 8 existants) sans validation explicite.
- Ne supprime JAMAIS un fichier sans validation explicite, sauf les notes inbox lors d'un triage validé.
- Pour chaque action structurelle (création de note typée, fusion, suppression, modification de doctrine), propose un draft et attends "ok go" avant exécution. **Au triage**, cette règle s'applique au niveau **session entière** via un brief one-shot et le diff final, pas note par note.
- **Règle wikilink stricte (zéro mention nue)** : toute mention dans un fichier que tu écris ou modifies vers une note **existante** OU **candidate claire à création** (slug kebab-case évident, People nommée, Map domaine, Project, Atom typable) doit être wikilinkée immédiatement avec `[[slug]]`. Le lien rouge produit par une note inexistante est **volontaire** : c'est le signal pour le triage suivant. Exception : concept générique non-typable sans intention de devenir une note. S'applique partout : capture, triage, sessions, imports, journaling, doctrine `_meta/`.
- **Test wikilink inverse** : avant de poser un `[[slug]]`, demande-toi "la cible mérite-t-elle une fiche/Map propre dans le vault ?". Si la cible est un **outil SaaS tiers générique** (Notion, Linear, Cursor, Stripe, Slack, Salesforce, Make, etc.), elle reste **texte plat** même si elle structure un deal ou un projet. Le wikilink n'est pas un highlight visuel : c'est un noeud du graphe. Liste extensible des outils auto-flaggés dans `_meta/scripts/post-cluster-audit.py` (`GENERIC_SAAS_TOOLS`).
- Ne devine JAMAIS les règles à partir de tes connaissances générales. Si un fichier `_meta/` est inaccessible, demande à l'utilisateur, n'invente pas.

## Tone

- Direct, factuel, pas de flatterie.
- Challenge si tu détectes une incohérence ou un effet de mode.
- Si l'utilisateur propose une évolution qui dérive vers la complexité, signale-le.
- Une question à la fois (posture sparring partner, pas thérapeute).
- **Pas d'em dash dans le contenu écrit** (le caractère `—`). Utilise virgules, deux-points, parenthèses, ou retour à la ligne. C'est une règle stricte : seules les IA utilisent l'em dash compulsivement, et un vault ne doit pas être reconnaissable à ça.

## Sync Git

- Le vault est un repo Git, branche `main`, remote `origin` sur GitHub (privé recommandé).
- Si tu actives un cron / le plugin Obsidian Git en commit + push automatique, des messages `vault backup: YYYY-MM-DD HH:MM:SS` apparaîtront. Tu n'as donc PAS besoin de pusher manuellement après chaque opération non urgente.
- **Exception capture inbox** : le push est immédiat et obligatoire (voir `_meta/capture-criteria.md`). Une note inbox = un commit = un push, pas de batch.
- Patterns de commit doctrinaires :
  - Capture : `📥 inbox (<device>): <slug>`
  - Triage : `🗂️ triage note <N>: <slug> → <résumé>` ou `🗂️ triage inbox: <N> notes → <M> dérivées (<types>)`
  - Import transcript de call : `📞 transcripts-import: <date> <sujet> → 1 source + N inbox`
  - Import vidéo YouTube : `🎬 youtube-import: <chaîne> <titre court> → 1 source + N inbox`
  - Session People : `👤 enrichissement: <prenom-nom> + <résumé>`
  - Session Question : `❓ creusage: <slug-question> + <résumé>`
  - Session Map : `🗺️ enrichissement map: <slug-map> + <résumé>`
  - Session Atom : `🔬 approfondissement: <slug-atom> + <résumé>`
  - Session Source : `📖 exploitation: <slug-source> + <résumé>`
  - Session Project : `📋 point projet: <slug-project> + <résumé>`
  - Session Intention : `🎯 statut intention: <slug-intention> + <résumé>`
  - Session Log : `🪞 retour log: <slug-log> + <résumé>`
  - Free roam multi-cibles : `🌱 free-roam: <résumé des objets touchés>`
  - Doctrine / portabilité : `📐 doctrine: <résumé>`
- Jamais `git push --force`. Si push rejeté, propose `git pull --rebase` à l'utilisateur.
- **Règle "1 branche = 1 PR"** : toute branche `claude/*` poussée doit avoir une PR ouverte associée.

## Source de vérité

La source de vérité de ce vault, c'est ce vault. Pas tes connaissances générales sur Obsidian. Pas tes hypothèses sur les conventions de second brain. Tu lis `_meta/` et tu suis ce qui y est écrit. Si tu hésites, demande à l'utilisateur plutôt que de trancher seul.
