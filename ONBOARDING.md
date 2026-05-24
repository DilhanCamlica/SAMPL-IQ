# SAMPL-IQ : guide de lancement

Bienvenue. SAMPL-IQ est un système de second brain dans Obsidian : une base de connaissance personnelle relationnelle, pilotée par IA (Claude Code), pensée comme une alternative plus complète à PARA. Ce repo te donne la structure vide et toutes les règles. À toi de le remplir.

Le nom vient des 8 dossiers maîtres : **A**toms, **P**eople, **S**ources, **P**rojects, **M**aps, **L**ogs, **I**ntentions, **Q**uestions. Anagramme jouable : SAMPL-IQ, "Sample your IQ with your second brain".

---

## 0. Comment lire ce guide (lecture imposée)

> [!important] Si tu es une IA (Claude Code, agent cloud) invoquée sur ce repo pour la première fois
> Tu DOIS lire dans cet ordre avant toute action :
> 1. Ce fichier (`ONBOARDING.md`) en entier.
> 2. `CLAUDE.md` à la racine (règles comportementales, ton, garde-fous).
> 3. `_meta/vault-doctrine-v1.md` (philosophie, 8 types, schemas YAML).
> 4. `_meta/README.md` (index opérationnel : quel fichier `_meta/` lire selon la tâche).
> 5. `_meta/conventions.md` (nommage et frontmatter détaillés).
> Puis le `_meta/<x>-criteria.md` correspondant à la tâche demandée. Ne devine jamais une règle : si un fichier `_meta/` est inaccessible, demande à l'utilisateur. La source de vérité, c'est ce repo, pas tes connaissances générales sur Obsidian ou les "second brain".

> [!note] Si tu es un humain qui démarre
> Lis les sections 1 à 5 dans l'ordre (concept, pré-requis, installation, architecture multi-appareils, capture). Puis garde la section 6 (les flux) sous la main comme référence. La section 7 te fait faire tes premiers pas. La section 9 te permet de déléguer toute l'installation à Claude Code.

---

## 1. Le concept en 3 minutes

**Une note = un objet. Les relations sont des liens, pas des dossiers.**

Pas d'arborescence thématique (`philosophie/`, `clients/`, `cadeaux/`). À la place, 8 types d'objets dans 8 dossiers, reliés par des wikilinks `[[...]]`. C'est une base de données relationnelle en markdown plat : les types sont des tables, les wikilinks sont des foreign keys.

| Type | Dossier | Rôle |
|---|---|---|
| Atom | `1-atoms/` | Idée, citation, règle, donnée. Unité de pensée atomique. |
| People | `2-people/` | Une personne, un fichier. |
| Source | `3-sources/` | Livre, article, podcast, vidéo, conversation. |
| Project | `4-projects/` | Initiative bornée dans le temps avec un objectif. |
| Map | `5-maps/` | Index vivant sur un domaine. Pas un essai, un hub. |
| Log | `6-logs/` | Journal daté (`journal/`) ou événement ponctuel (`events/`). |
| Intention | `7-intentions/` | Cible personnelle sans deadline, horizon flou. |
| Question | `8-questions/` | Interrogation ouverte sans réponse, à creuser plus tard. |

`0-inbox/` est le sas de capture brute (input). Tout y atterrit non classé, puis le **triage** transforme l'inbox en notes typées. `_meta/` contient les règles du jeu (la doctrine). Lis `_meta/vault-doctrine-v1.md` pour le pourquoi complet.

Pourquoi ça marche : les sujets se croisent nativement (une note a autant de liens qu'elle veut), et ajouter un domaine ne casse rien (tu crées une nouvelle Map, elle se remplit organiquement).

---

## 2. Pré-requis

Sur ton Mac (l'appareil principal, là où Claude Code tourne) :

- **Obsidian** (gratuit) : https://obsidian.md
- **Claude Code** (CLI) : https://claude.com/claude-code . C'est le moteur qui nourrit le vault depuis le terminal.
- **Homebrew** (gestionnaire de paquets macOS) : https://brew.sh
- **Git** : `brew install git` (souvent déjà présent).
- **Python 3** : `python3 --version` (présent sur macOS récent, sinon `brew install python`).
- **yt-dlp** (pour l'import YouTube) : `brew install yt-dlp`.
- **Un compte GitHub** : le vault est un repo Git privé poussé sur GitHub. C'est ce qui permet la sync multi-appareils et la capture mobile.

Optionnel mais recommandé pour la capture on-the-go (section 5) :

- **Superwhisper** (iOS, dictée vocale) ou équivalent.
- **Un compte Make.com** (automatisation no-code) pour le pipeline webhook → GitHub.

---

## 3. Installation pas à pas

### 3.1 Récupérer SAMPL-IQ comme ton vault

Ce repo est un **template**. Crée ton propre repo à partir de lui (bouton "Use this template" sur GitHub, ou clone puis re-init), puis place-le à l'emplacement iCloud recommandé (voir 3.2). Donne-lui le nom que tu veux (ex. `MonVault`, `knowledge`, `brain`).

```sh
# Exemple : cloner le template puis le détacher pour en faire TON vault
git clone <url-du-template> ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/MonVault
cd ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/MonVault
rm -rf .git && git init        # repart d'un historique propre
```

### 3.2 Choisir l'emplacement : iCloud (clé pour le multi-appareils)

Range le dossier du vault **dans iCloud Drive**, précisément sous le dossier qu'Obsidian Mobile sait lire :

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<TonVault>
```

Tout ce qui vit là est synchronisé par iCloud entre ton Mac, ton iPad et ton iPhone. Le Mac édite, iCloud propage, les apps Obsidian mobiles voient les fichiers à jour. **Lis la section 4 sur les risques avant d'éditer sur plusieurs appareils.**

### 3.3 Ouvrir dans Obsidian + installer les 2 plugins communautaires

1. Ouvre Obsidian, "Open folder as vault", pointe vers ton dossier.
2. Réglages → Community plugins → désactive le Restricted mode.
3. Installe et active :
   - **Obsidian Git** (`obsidian-git`) : commit/push/pull automatiques. C'est lui qui synchronise le vault avec GitHub en arrière-plan.
   - **Terminal** (`terminal`) : ouvre un terminal directement dans Obsidian, pour lancer Claude Code sans quitter l'app.

Le repo embarque déjà la liste de ces plugins dans `.obsidian/community-plugins.json` ; Obsidian te proposera de les installer.

### 3.4 Installer Claude Code

Suis https://claude.com/claude-code . Une fois installé, depuis le plugin Terminal d'Obsidian (ou un terminal classique), place-toi dans le vault et lance `claude`. Au premier lancement sur ce repo, Claude lira `CLAUDE.md` et ce guide.

### 3.5 Installer les 4 skills

Les skills sont des extensions Claude Code qui encapsulent les flux (capture, triage, import). Ils vivent dans `~/.claude/skills/` sur ta machine. Le repo les fournit dans `skills/`. Installe-les un par un :

```sh
# Depuis la racine de ton vault
cp -R skills/obsidian-capture            ~/.claude/skills/
cp -R skills/obsidian-triage             ~/.claude/skills/
cp -R skills/obsidian-transcripts-to-inbox ~/.claude/skills/
cp -R skills/obsidian-youtube-import     ~/.claude/skills/
```

Puis, dans chaque `~/.claude/skills/obsidian-*/SKILL.md`, **remplace le placeholder `<CHEMIN_DU_VAULT>`** par le chemin absolu de ton vault. En une commande :

```sh
VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/MonVault"
for s in obsidian-capture obsidian-triage obsidian-transcripts-to-inbox obsidian-youtube-import; do
  sed -i '' "s|<CHEMIN_DU_VAULT>|$VAULT|g" "$HOME/.claude/skills/$s/SKILL.md"
done
```

Vérifie ensuite avec `claude` : tape `/` et tu devrais voir les skills `obsidian-capture`, `obsidian-triage`, etc.

> Les skills sont volontairement minces : ils pointent vers les fichiers `_meta/*-criteria.md` du vault, qui sont la **source de vérité unique**. Tu peux donc faire évoluer un flux en éditant le `_meta/` correspondant, sans toucher au skill.

### 3.6 GitHub : repo, remote, authentification

1. Crée un repo **privé** sur GitHub (ex. `mon-vault`).
2. Branche ton vault local dessus :
   ```sh
   git remote add origin git@github.com:<ton-org>/mon-vault.git
   git add -A && git commit -m "init: SAMPL-IQ vault"
   git branch -M main && git push -u origin main
   ```
3. **Authentification** : configure une clé SSH (recommandé) ou un Personal Access Token (PAT). Le PAT te servira aussi pour la capture mobile (section 5).
4. Dans Obsidian Git (réglages du plugin), active le commit + push automatique à intervalle régulier (ex. toutes les 10 minutes). C'est ton filet de sync.

---

## 4. Architecture multi-appareils iCloud, et ses risques

Le setup recommandé : **un seul dossier dans iCloud, trois appareils**.

- **Mac** : c'est le poste de travail. Claude Code y tourne, le plugin Git y commit/push/pull. Config Obsidian desktop dans `.obsidian/`.
- **iPad / iPhone** : consultation et capture légère. Config Obsidian mobile distincte (Obsidian sépare automatiquement la config desktop et mobile).

> [!warning] Trois règles de sécurité à ne JAMAIS enfreindre
> 1. **Désactive le plugin Obsidian Git sur iPad et iPhone.** Le plugin Git mobile + la sync iCloud en parallèle corrompent le dépôt (`.git` à moitié synchronisé par iCloud = état incohérent). Sur mobile, tu laisses iCloud faire la sync des fichiers `.md`, et c'est tout. Le Git, c'est uniquement le Mac.
> 2. **Ne travaille jamais sur deux appareils en parallèle.** Si tu édites sur le Mac pendant qu'iCloud n'a pas fini de propager une modif faite sur l'iPhone, tu crées des conflits iCloud (`fichier 2.md`, versions divergentes). Règle simple : un appareil à la fois, et attends que la petite icône de sync iCloud soit terminée avant de changer d'appareil.
> 3. **La capture mobile passe par GitHub, pas par l'édition directe.** Pour ajouter une note depuis ton téléphone en déplacement, utilise le pipeline de la section 5 (qui écrit dans GitHub), puis laisse le Mac faire le `pull`. Tu évites ainsi les conflits iCloud sur les nouvelles notes.

En résumé : **Git = Mac uniquement. iCloud = transport des fichiers. Mobile = lecture + capture via GitHub.**

---

## 5. Capture on-the-go : le système maison à reproduire

Le problème : tu as une idée en marchant, loin du Mac. Tu veux qu'elle atterrisse proprement dans `0-inbox/` avec le bon frontmatter, sans ouvrir le laptop. La solution de l'auteur, à reproduire ou adapter :

```
Dictée vocale (Superwhisper iOS)
        │  transcript brut
        ▼
Webhook Make.com
        │  applique les règles de toilettage (_meta/toilettage-rules.md)
        │  enveloppe dans le frontmatter inbox (device: whisper)
        ▼
API GitHub (Create file content)  →  écrit 0-inbox/<slug>.md, commit + push
        │
        ▼
Plugin Obsidian Git sur le Mac  →  pull : la note apparaît dans le vault
        │
        ▼
Au prochain triage, la note est classée en note typée
```

Pour le rebâtir :

1. **Superwhisper** (ou Drafts, ou un raccourci iOS) configuré pour POSTer le transcript vers un webhook.
2. **Scénario Make.com** :
   - Trigger : webhook (reçoit le transcript).
   - Étape de toilettage : un module IA (ou des règles) qui applique `_meta/toilettage-rules.md` (corrige la ponctuation de dictée, retire les hésitations, ne reformule pas le fond).
   - Génère un slug kebab-case et le frontmatter inbox (voir `_meta/capture-criteria.md` §4 pour le format exact et la valeur `device`).
   - Module **GitHub → Create/Update a file** : path `0-inbox/<slug>.md`, contenu = frontmatter + texte, commit message `📥 inbox (whisper): <slug>`.
3. **Authentification GitHub** : le module Make utilise ton PAT (scope `repo`). C'est la même logique que tout client qui parle à l'API GitHub : un token qui autorise l'écriture dans ton repo depuis n'importe où.

> Tu n'es pas obligé d'utiliser Superwhisper + Make. N'importe quelle chaîne qui finit par "écrire un fichier markdown dans `0-inbox/` via l'API GitHub" fonctionne (Raccourcis iOS, un petit script, Zapier, n8n, etc.). Le contrat est : **frontmatter inbox conforme + commit dans `0-inbox/`**.

**Alternative sans pipeline** : installe Claude Code sur iPhone (ou utilise un agent cloud) et invoque le skill `obsidian-capture`. Le fichier `_meta/capture-criteria.md` est self-contained : un agent distant sait capturer de bout en bout sans le skill local.

---

## 6. Les flux de complétion (référence)

Chaque flux a un fichier doctrine self-contained dans `_meta/`. Les skills pointent dessus.

| Flux | Déclencheur | Ce qu'il fait | Doctrine |
|---|---|---|---|
| **Capture** | "capture cette idée" / dictée / webhook | Toilette le texte, pose le frontmatter, écrit dans `0-inbox/`, commit + push immédiat. Ne classe pas. | `_meta/capture-criteria.md` + `_meta/toilettage-rules.md` |
| **Triage** | "vide mon inbox" | Lit chaque note inbox, propose une classification dans les 8 types, crée les notes typées dérivées, supprime l'inbox, commit. | `_meta/triage-criteria.md` |
| **Transcripts → inbox** | "import ce call" + transcript collé | 1 Source (conversation, allégée) + 3-7 inbox thématiques. Agnostique à l'outil (Grain, tl;dv, Fathom, Fireflies, Zoom, texte collé). | `_meta/transcripts-import-criteria.md` |
| **YouTube → inbox** | URL YouTube | 1 Source (video, allégée) + 3-7 inbox. Utilise `yt-dlp` + oEmbed. | `_meta/youtube-import-criteria.md` |
| **Sessions** | "lance une session people / question / map..." | Enrichissement guidé d'un objet ou free roam. 8 portes d'entrée. | `_meta/sessions-criteria.md` |
| **Lifecycle** | automatique en fin de triage/session | Ferme les intentions consommées, fait monter les Maps en maturité, met à jour `last_seen`, détecte les Maps manquantes. | `_meta/lifecycle-criteria.md` |
| **Journaling** | note inbox détectée comme journal-daily | Rituel de journal quotidien : parse, rédige les sections, dérive des inbox. | `_meta/journaling-criteria.md` |
| **Grill-me** | "grille-moi sur ce plan" | Interview de stress-test d'un plan ou design. | `_meta/grill-criteria.md` |
| **Hygiène des tags** | à la pose et au cleaning | Nomenclature 2 niveaux `racine/sous-tag`, racines évolutives, procédure de cleaning relançable. | `_meta/tag-hygiene-criteria.md` |

Le **dashboard d'état** (`_meta/vault-state.md`) est lu par l'agent en début de session pour s'orienter, et mis à jour en fin de session. Il démarre vide, c'est normal.

---

## 7. Premiers pas

Une fois l'installation faite, fais ce parcours pour sentir le système :

1. **Capture 5 pensées brutes.** Dans Claude Code : "capture cette idée : <ta pensée>". Répète. Regarde-les apparaître dans `0-inbox/`.
2. **Lance un triage.** "Lance un triage de mon inbox." L'agent te propose, note par note, une classification dans les 8 types. Valide. Tu vois tes premières notes typées et tes premiers wikilinks.
3. **Crée ta première Map.** Quand 3-4 atoms tournent autour d'un même thème, demande "crée une Map pour <domaine>". C'est le moment où le graphe prend vie.
4. **Importe un contenu.** Colle un transcript de call ("import ce call") ou une URL YouTube. Observe la Source + les fragments inbox, puis trie-les.
5. **Ouvre la vue graphe d'Obsidian.** Les presets sont dans `_meta/graph-presets/` (active avec `bash _meta/graph-presets/swap.sh macro`).

---

## 8. Personnaliser le système

Le squelette est figé (8 types, schemas YAML, nomenclature), mais le contenu et certains vocabulaires sont à toi :

- **`_meta/identite-civile.md`** : remplis ce template avec tes facts civils (qui tu es, ton cercle proche, ta géographie). Les agents le lisent pour résoudre les références People sans inventer.
- **Enum `context` des People** : par défaut `work | personal | both`. Tu peux le spécialiser avec tes propres sociétés (voir `_meta/conventions.md` §People). Si tu le fais, mets à jour les 3 fichiers indiqués.
- **Racines de tags** : la liste de `_meta/tag-hygiene-criteria.md` §2 est une liste de départ, évolutive. Adopte, renomme, crée les tiennes.
- **Doctrine** : elle est stable mais pas gravée. Pour la faire évoluer proprement, lis `_meta/doctrine-roadmap.md` (gouvernance des changements) et trace tes décisions dans `_meta/doctrine-changelog.md`.

---

## 9. Mode "agent" : déléguer l'installation à Claude Code

Tu peux laisser Claude Code te guider pas à pas. Une fois Claude Code installé et lancé dans le repo, copie-colle ce prompt :

> "Tu es mon assistant d'installation pour SAMPL-IQ. Lis `ONBOARDING.md` puis `CLAUDE.md`. Ensuite, déroule avec moi l'installation des sections 3 à 5, une étape à la fois : vérifie mes pré-requis (Obsidian, Homebrew, python3, yt-dlp, git, compte GitHub), aide-moi à placer le vault dans iCloud, installe les 4 skills dans `~/.claude/skills/` en remplaçant le chemin, configure le remote GitHub, et explique-moi le pipeline de capture mobile. Pose-moi une question à la fois, attends ma validation avant chaque action irréversible, et ne touche jamais à la doctrine `_meta/` sans me demander."

L'agent te fera avancer proprement, en respectant les garde-fous de `CLAUDE.md`.

---

Bon vault. Le système ne vaut que par ce que tu y mets : capture souvent, trie régulièrement, et laisse les Maps émerger.
