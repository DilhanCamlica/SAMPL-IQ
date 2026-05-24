---
type: meta
purpose: doctrine et procédure d'hygiène des tags du vault. Référence opérationnelle pour tout agent qui pose un tag, et procédure d'audit/cleaning relançable sans recompiler le contexte.
version: v1
status: active
created: 2026-04-29
last_updated: 2026-05-10
---

<!--
Changelog : externalisé vers _meta/doctrine-changelog.md (consulté à la demande).
Doctrine V1 anonymisée, packagée comme produit SAMPL-IQ.
-->

# Hygiène des tags

Ce fichier sert deux usages distincts :

1. **Référence pour la pose courante de tags** (lu par les agents capture, triage, transcripts-import, journaling, sessions au moment où ils ajoutent un tag à une note). Il rassemble la nomenclature, la liste opérationnelle des racines avec exemples, la checklist de validation, et la procédure pour proposer une nouvelle racine quand l'idée ne rentre dans aucune racine actuelle.
2. **Procédure de cleaning relançable** (lu par un agent à qui l'utilisateur dit "lance un cleaning des tags du vault, base-toi sur tag-hygiene-criteria"). Il codifie l'audit et le workflow de cleaning des 6 étapes du Volet C du 2026-04-29, formulé en générique pour pouvoir être rejoué dans 6 mois sans contexte préalable.

La source de vérité doctrinale reste `[[conventions]] §"Hiérarchie des tags"`. Ce fichier ne la contredit jamais.

## 1. Nomenclature V1

Format strict : `racine/sous-tag`. Le séparateur est `/`. Pas de 3ème niveau, ni en V1 ni dans les racines très denses (sous une racine saturée comme `acme`, on multiplie les sous-tags plats plutôt que de créer un sous-niveau).

Une racine seule est autorisée quand le tag s'applique à la racine entière sans sous-domaine pertinent (ex. `acme`, `famille`). Un sous-tag est toujours sous une racine, jamais isolé (`acme/pricing` oui, `pricing` seul non).

Slug du sous-tag : kebab-case, ASCII, ≤30 caractères.

## 2. Racines de tags (liste de départ, évolutive)

**Cette liste n'est PAS une closed list.** Le vault démarre sans tag. Les racines ci-dessous sont des **exemples courants** pour t'amorcer : tu les adoptes, les renommes ou en crées d'autres au fil de ton contenu. Le gel V1 fige la **grammaire** (8 types, schemas frontmatter, nomenclature 2 niveaux `racine/sous-tag`), pas le **vocabulaire** (la liste des racines en circulation). Procédure d'ajout d'une racine : voir §6.

| Racine (exemple) | Périmètre | Exemples de sous-tags |
| --- | --- | --- |
| `<entreprise>`  | Une de tes structures pro : clients, produits, positionnement, gouvernance, ops, équipe, ventes. Crée une racine par société structurante (ex. `acme`, `globex`).                                                  | `acme/pricing`, `acme/produit`, `acme/gouvernance`, `acme/ops`, `acme/equipe`, `acme/sales`, `acme/client`, `acme/contrats` |
| `famille`     | Famille élargie, fratrie, dynamiques familiales. Sous-tags par branche.                                                                                                                                            | `famille/<branche>`, `famille/fratrie`, `famille/role`, `famille/origine` |
| `finance`     | Patrimoine, allocation, immobilier, fiscalité, transmission, stratégie financière personnelle.                                                                                                                     | `finance/strategie`, `finance/allocation`, `finance/immobilier`, `finance/fiscalite`, `finance/transmission` |
| `sante`       | Hygiène de vie, sport, sommeil, nutrition, médical.                                                                                                                                                                | `sante/hygiene-de-vie`, `sante/sport`, `sante/medical` |
| `geo`         | Lieux, géographie, nomadisme, pays liés à ta vie.                                                                                                                                                                  | `geo/<pays>`, `geo/<ville>`, `geo/nomadisme` |
| `culture`     | Musique, lectures, arts, références culturelles consommées.                                                                                                                                                        | `culture/musique`, `culture/cinema`, `culture/lecture` |
| `philosophie` | Pensée existentielle, métaphysique, éthique, posture face au monde. Champ d'idées, distinct de `posture` (personnel).                                                                                              | `philosophie/ethique`, `philosophie/epistemologie`, `philosophie/liberte`, `philosophie/finitude` |
| `tech`        | Stack technique, dev, langages, outils, IA générative. L'IA y vit comme sous-domaine technique (`tech/ia`).                                                                                                         | `tech/ia`, `tech/dev`, `tech/stack`, `tech/saas`, `tech/lang` |
| `vault`       | Doctrine, structure, méta-réflexion sur le second brain lui-même.                                                                                                                                                  | `vault/doctrine`, `vault/structure`, `vault/second-brain`, `vault/workflow` |
| `posture`     | Patterns comportementaux personnels, valeurs, vision, mode de fonctionnement. Distinct de `philosophie` (champ d'idées).                                                                                            | `posture/patterns`, `posture/identite`, `posture/leadership`, `posture/decision`, `posture/relations`, `posture/vision` |
| `creativite`  | Production créative personnelle (écriture, dessin, musique produite). Distinct de `culture` (consommation).                                                                                                        | `creativite/ecriture`, `creativite/musique` |
| `meta`        | Marqueurs transversaux non-domaine. Voir `_meta/conventions.md` §"Tags transversaux" pour la nomenclature complète et les usages.                                                                                  | **Statuts/qualifs** : `meta/needs-enrichment`, `meta/needs-validation`, `meta/decision`, `meta/vigilance`, `meta/silence-question`, `meta/no-photo`, `meta/prive`. **Traçabilité d'import** : `meta/call`, `meta/youtube`, `meta/journal-daily`. **Perspective sourcée** (pattern `meta/perspective-<prenom>`) : ex. `meta/perspective-anna`. |

## 3. Règles de pose (checklist agent)

Avant d'ajouter un tag à une note, valider :

1. **Format** : `racine/sous-tag` ou racine pure. Jamais 3 niveaux. Slug kebab-case, ASCII, ≤30 caractères.
2. **Racine** : dans la liste §2, OU nouvelle racine proposée explicitement à l'utilisateur via §6 (pas de création silencieuse).
3. **Sous-tag** : ≥2 occurrences attendues dans le vault, ou clairement sourcé par un texte stratégique. Sinon candidat drop au prochain cleaning.
4. **Pas de marqueur temporel** : `tag-2026-04-25`, `profil-consolide-YYYY-MM-DD`, `phase-1` sont interdits. La date vit dans le frontmatter (`created`, `date_consumed`, `last_updated`).
5. **Pas de tag prénom isolé** : un tag qui est juste un prénom (`sam`, `john`) est redondant avec le champ `people:` du frontmatter. Drop.
6. **Pas de tag client générique** : `client`, `prospect` non, plutôt `acme/client` ou un sous-tag client précis (`acme/compte-cle`, `acme/projet-alpha`).
7. **Dédupliquer** : si un Atom touche à la fois `acme/pricing` et `pricing` (qui ne devrait pas exister mais peut survenir d'une mauvaise saisie), ne garder que la forme hiérarchique.
8. **Cohérence avec les autres champs** : si la note a `[[flora-smith]]` dans `people:`, le tag `famille/smith` est probablement utile. Si la note référence `[[acme]]` dans `maps:`, le tag `acme` ou un sous-tag `acme/x` est cohérent. Tags et wikilinks ne sont pas redondants : les wikilinks lient des objets, les tags catégorisent.
9. **Cohérence Map racine / sous-Maps / tag racine** : si une Map racine existe pour le domaine du tag (ex. [[philosophie]] pour `philosophie/*`), le frontmatter `maps:` doit pointer vers la Map la plus spécifique disponible (sous-Map dédiée si existante, sinon Map parent). Voir §4bis pour la règle complète et les cas d'application.

## 4. Quand l'idée ne rentre dans aucune racine actuelle

Ne pas forcer. Trois options par ordre de préférence :

1. **Domaine émergent** (politique, écologie, éthique appliquée, créativité, etc.) absent du tableau §2 → **proposer une nouvelle racine à l'utilisateur**. Voir §6.
2. **Variation d'une racine existante mais sous-tag manquant** (ex. la racine `tech` existe, mais on parle de `tech/devops` qui n'a pas encore d'occurrence) → **créer le sous-tag librement**. Pas d'autorisation l'utilisateur nécessaire si la racine est dans la liste §2. Le sous-tag entrera dans le vocabulaire courant et apparaîtra dans `vault-state.md §13` au prochain update.
3. **Idée trop diffuse pour mériter un tag de domaine** → laisser sans tag de domaine plutôt qu'inventer une racine bidon. La note reste retrouvable via wikilinks et fulltext. Mieux vaut un index propre qu'un index complet et bruité.

## 4bis. Cohérence Map racine / sous-Maps / tag racine

Codifie la relation entre une **Map racine** (ex. [[philosophie]]), ses **sous-Maps spécialisées** (ex. [[absurde]] sous-Map de [[philosophie]]), et le **tag racine** correspondant (ex. `philosophie/*`). Règle ajoutée 2026-05-09 après audit post-création Map [[philosophie]] qui a révélé que ~10 atoms taggués philosophie/* n'étaient pas backlinkés à la Map racine.

### Mécanique technique

- **Tag** = filtre sémantique transversal (Dataview, recherche). N'établit AUCUN lien dans le graphe Obsidian.
- **Wikilink** dans le frontmatter `maps:` ou dans le body d'une Map = lien direct, génère un backlink visible dans la Map cible.
- **Map** = note hub. Sa richesse en backlinks dépend des wikilinks qui pointent vers elle, pas des tags.

Conséquence : un atom taggué `philosophie/liberte` n'apparaît PAS dans les backlinks de [[philosophie]] uniquement par son tag. Il faut un wikilink quelque part.

### Règle d'appartenance (frontmatter `maps:`)

Quand une Map racine existe pour un domaine, tout atom du domaine doit être rattaché via `maps:` à AU MOINS la Map la plus spécifique disponible :

- **Sous-Map dédiée existe** (ex. [[absurde]] pour atoms `philosophie/absurde`) → pointer la sous-Map uniquement. La Map parent voit l'atom indirectement via sa section "Sous-Maps thématiques" du body, pas par appartenance frontmatter.
- **Pas de sous-Map dédiée** (ex. atoms `philosophie/liberte`, `philosophie/finitude`, `philosophie/juridique`) → pointer la Map parent (`maps: [[philosophie]]`). L'atom devient atom transversal visible directement dans la Map parent (section "Atoms transversaux par sous-domaine" du body).
- **Multi-rattachement parent + sous-Map** : autorisé seulement pour les atoms qui dépassent le périmètre d'une seule sous-Map (ex. atom transversal qui touche absurde + épistémologie + posture). Par défaut, **un seul rattachement à la plus spécifique** pour éviter doublons de backlinks.
- **Multi-rattachement Maps de domaines différents** (ex. `[[acme]] + [[philosophie]]` pour un atom philo appliquée au pro) : autorisé sans restriction, c'est le cas normal d'un atom transversal multi-domaines.

### Deux mécanismes d'inclusion dans une Map

| Mécanisme | Définition | Effet backlinks Obsidian |
|---|---|---|
| Frontmatter `maps: [[X]]` | **Appartenance forte** : l'atom est du domaine X | Backlink visible dans [[X]] |
| Body de la Map [[X]] listant l'atom en wikilink dans une section H3 | **Mention éditoriale** : la Map X affiche l'atom dans une vue thématique sans revendiquer l'appartenance principale | Backlink visible dans [[X]] (équivalent technique) |

Les deux génèrent des backlinks dans Obsidian, mais la distinction sémantique reste : appartenance vs mention. Cas typique : un Atom de philosophie issu d'une transmission familiale (`philosophie/ethique` ou `philosophie` racine) a son appartenance forte sur [[famille]] (la transmission), et est mentionné éditorialement dans [[philosophie]] (le champ d'idées). Pas de double-rattachement frontmatter, juste mention dans deux Maps adjacentes.

### Statut du tag racine `racine/*`

Le tag `racine/X` est un **filtre transversal universel** orthogonal aux wikilinks. Toutes les notes du domaine restent retrouvables par tag même si leur `maps:` pointe vers une sous-Map ou un autre domaine adjacent (ex. un Atom de philosophie rattaché à [[famille]] dans `maps:` garde son tag `philosophie/*`).

C'est ce qui permet à un agent ou à l'utilisateur de filtrer "toutes les notes philo du vault" via Dataview `where contains(tags, "philosophie")`, indépendamment de l'architecture Map / sous-Map.

### Cas où une Map racine n'existe pas

Toutes les racines de tag du vault n'ont PAS forcément une Map racine du même nom. Au 2026-05-09 :

| Racine de tag | Map racine ? | Maps de domaine équivalentes |
|---|---|---|
| `acme` | ✅ [[acme]] mature | sous-Maps thématiques nombreuses (juridique-contractuel-acme, etc.) |
| `famille` | ✅ [[famille]] growing | sous-Maps [[smith-genealogie]], [[doe-genealogie]] + cross-link [[couple]] |
| `philosophie` | ✅ [[philosophie]] growing | sous-Map [[absurde]] mature, sous-Maps spawnables (epistemologie, ethique-conflit) |
| `tech` | ✅ [[tech]] growing | (pas de sous-Map dédiée pour l'instant) |
| `posture` | ✅ [[posture]] growing (créée 2026-05-09) | sous-Maps spawnables : [[posture-patterns]] (14 atoms), [[posture-leadership]] (9), [[posture-identite]] (12) en attente masse critique |
| `finance` | ❌ pas de Map racine | [[strategie-financiere]] mature + [[patrimoine-familial]] growing couvrent le domaine |
| `sante` | ❌ pas de Map racine | [[hygiene-de-vie]] growing + [[sports-adrenaline]] stub |
| `geo` | ❌ pas de Map racine | [[voyage]] growing + [[japon]] sous-Map |
| `culture` | ❌ pas de Map racine | [[musique]] growing seule |
| `vault` | ❌ pas de Map racine | [[second-brain]] stub |
| `meta` | n/a | racine de marqueurs transversaux, pas un domaine cognitif |

Quand pas de Map racine : les atoms sont rattachés à la Map de domaine la plus pertinente parmi les Maps disponibles, sans contrainte hiérarchique. Si une dynamique d'accumulation pousse à créer une Map racine (ex. >15 atoms taggués `posture/*` sans Map dédiée), c'est un signal à proposer dans une session future, pas une obligation immédiate.

### Application au triage

Le triage doit appliquer cette règle systématiquement quand un atom typé est créé :

1. Identifier le tag `racine/X` ou `racine` racine pure de l'atom.
2. Vérifier si une Map racine existe pour cette racine (cf tableau ci-dessus).
3. Si Map racine existe :
   - Sous-Map dédiée pour le sous-tag → `maps: [[sous-map]]`.
   - Pas de sous-Map → `maps: [[map-racine]]` (atom devient transversal de la Map racine).
4. Si pas de Map racine : utiliser la Map de domaine la plus spécifique disponible.
5. Multi-rattachement Maps de domaines différents reste autorisé (cas normal d'atom transversal).

### Application au cleaning

Lors d'un cleaning de tags ou d'une session de rétro-rattachement, l'agent peut grep `1-atoms/` par sous-tag et vérifier que chaque atom respecte la règle. Audit type :

```bash
# Trouver les atoms taggués philosophie/* sans rattachement Map cohérent
grep -l "philosophie/" 1-atoms/*.md | while read f; do
  if ! grep -qE 'maps:.*\[\[(philosophie|absurde)\]\]' "$f"; then
    echo "À auditer: $f"
  fi
done
```

## 5. Comment proposer une nouvelle racine

Procédure légère (pas de passage par `_meta/doctrine-roadmap.md` : l'ajout d'une racine n'est pas une modification structurelle de la doctrine V1, c'est une extension de vocabulaire).

**Étape 1 : flag explicite à l'utilisateur**, avec un mini-pitch de 4 lignes :

```
Racine proposée : `<nom>`
Périmètre : <1 phrase>
Exemples de sous-tags qu'on imaginerait y mettre : <2-3 exemples>
Racine voisine la plus proche : <nom> (mais distincte parce que <raison brève>)
Note(s) du vault qui justifient l'ajout : [[<slug>]] (et/ou la note inbox courante)
```

**Étape 2 : si l'utilisateur valide**, mises à jour à faire dans le même commit :

1. Ajouter la racine au tableau §2 de ce fichier (avec périmètre + exemples).
2. Ajouter au tableau de `_meta/conventions.md §"Hiérarchie des tags"` (avec périmètre, ton aligné).
3. Ajouter au snapshot `_meta/vault-state.md §13` (distribution par racine, mettre la nouvelle racine avec 0 ou peu de sous-tags initiaux).

**Étape 3 : commit**. Pattern : `📐 doctrine: ajout racine tag <nom>` avec body de 1-3 phrases qui explique la justification (le mini-pitch suffit en général).

**Pas besoin de** : refaire un audit complet du vault, modifier `vault-doctrine-v1.md`, passer par `doctrine-roadmap.md`.

## 6. Procédure d'audit (lecture seule)

Prend 30 secondes. À lancer avant d'ouvrir un cleaning, et de temps en temps en fin de session de triage pour mesurer la dérive.

```bash
# Compter les tags distincts dans le frontmatter
python3 -c "
import re, glob
tags = set()
for f in glob.glob('[0-8]-*/**/*.md', recursive=True) + glob.glob('0-inbox/*.md'):
    content = open(f).read()
    if not content.startswith('---'): continue
    parts = content.split('---', 2)
    if len(parts) < 3: continue
    m = re.search(r'^tags:\s*\[(.*?)\]', parts[1], re.M)
    if m:
        for t in m.group(1).split(','):
            t = t.strip()
            if t: tags.add(t)
print(f'Distinct tags: {len(tags)}')
"

# Lister les tags non-conformes (ni racine pure, ni racine/sous-tag)
python3 -c "
import re, glob
tags = set()
for f in glob.glob('[0-8]-*/**/*.md', recursive=True) + glob.glob('0-inbox/*.md'):
    content = open(f).read()
    if not content.startswith('---'): continue
    parts = content.split('---', 2)
    if len(parts) < 3: continue
    m = re.search(r'^tags:\s*\[(.*?)\]', parts[1], re.M)
    if m:
        for t in m.group(1).split(','):
            t = t.strip()
            if t: tags.add(t)
ROOTS = {'acme','acme','acme','acme','famille','finance','sante','geo','culture','philosophie','tech','vault','posture','creativite','politique','meta'}
non_compliant = [t for t in tags if not re.match(r'^[a-z-]+/[a-z-]+$', t) and t not in ROOTS]
print(f'Non-compliant: {len(non_compliant)}: {sorted(non_compliant)}')
"
```

**Lecture du résultat** :

- Conformité 100% (0 non-compliant) : tout va bien.
- 1-3 tags non-compliant : probable signal d'une racine émergente à proposer (cf. §5) ou d'un oubli de migration (cleaning ciblé sur ces tags).
- ≥4 tags non-compliant ou nb tags distincts >120 : déclencher un cleaning complet (§7).

## 7. Procédure de cleaning (modifications)

Workflow codifié des 6 étapes du Volet C (2026-04-29). À rejouer chaque fois que le compteur §13 du `vault-state.md` montre une dérive significative.

**Principe défensif** : tous les artefacts intermédiaires (TSV, scripts) vivent à la racine du repo et sont supprimés en fin de chantier. `_meta/` reste irréprochable.

### Étape 1 : Inventaire

```bash
grep -h "^tags:" -r 0-inbox 1-atoms 2-people 3-sources 4-projects 5-maps 6-logs 7-intentions 8-questions 2>/dev/null | grep -oP '\[.*?\]' | tr -d '[]' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sort | uniq -c | sort -rn > tag-frequencies.txt
```

Lire `tag-frequencies.txt` : top tags par fréquence, longue traîne. Identifier les tags non-conformes et les patterns qui suggèrent des racines émergentes.

### Étape 2 : Mapping noyau (tags ≥3 occurrences)

Créer `tag-mapping.tsv` à la racine du repo. Colonnes : `old_tag, freq, new_tag, action, notes`. Action : `keep` / `rename` / `drop`. Mapper manuellement les ~50-80 tags ≥3 occ avec son jugement, en référence aux racines §2.

Pour les ambigus : flagger avec `action=review` et lister les ambigus à arbitrer avec l'utilisateur en un seul échange (pas un par un).

### Étape 3 : Mapping orphelins (tags 1-2 occurrences)

Script Python à la racine (`tag-mapping-build.py`) qui applique des heuristiques par mot-clé sur le nom du tag. Exemples de règles : `r"\b(client|compte|deal)\b" → acme/client`, `r"\b(sport|kite|trail)\b" → sante/sport`. Output : `tag-mapping-orphans.tsv` avec colonne confidence (high/med/low).

**Politique long-tail** : tag à 1 occurrence sans match heuristique évident → DROP (sauf signe d'une racine émergente, cf. §5). L'info reste retrouvable via fulltext et wikilinks.

Pour les 2-occ sans match : arbitrer manuellement (en général 30-50 cas, gérable en 10 minutes).

### Étape 4 : Script migration + dry-run

Script `tag-migrate.py` à la racine. Modes `--dry-run` et `--apply`.

**Bug à éviter** : limiter le parsing au frontmatter (entre les 2 délimiteurs `---`). Si le script scanne tout le fichier, il va matcher des lignes `tags:` dans des exemples textuels du body (cas des fichiers de spec). Restreindre `process_file` à la zone frontmatter.

**Récursivité** : utiliser `Path.rglob("*.md")` pour atteindre les sous-dossiers (`6-logs/journal/`, `6-logs/events/`).

Lancer `--dry-run` d'abord. Output : `tag-migration-diff.txt` avec tous les changements proposés. Faire un échantillon dans le chat (10 cas variés), valider avec l'utilisateur.

### Étape 5 : Apply + vérifications

`python3 tag-migrate.py --apply`. Puis vérifier :

- Compteurs identiques avant/après (`for d in 0-inbox 1-atoms ... ; do echo "$d: $(find $d -name '*.md' | wc -l)" ; done`). Aucune note perdue.
- Conformité 100% via le snippet d'audit §6.
- Cas particuliers à restaurer manuellement : si une note avait une racine pure (ex. `finance` seul) qui a été DROP par erreur, la racine pure à 1 occurrence doit être `keep` dans le TSV (les racines V1 ne sont jamais des orphelins long-tail). Restaurer dans le frontmatter du fichier concerné si nécessaire.

### Étape 6 : Cleanup et update doctrine

- Supprimer les artefacts à la racine : `tag-frequencies.txt`, `tag-mapping.tsv`, `tag-mapping-orphans.tsv`, `tag-mapping-build.py`, `tag-migrate.py`, `tag-migration-diff.txt`, et tout autre fichier ad-hoc créé pendant le chantier.
- Mettre à jour `_meta/vault-state.md §13` : nouveau snapshot tags distincts, distribution par racine. Append au log de session via `_meta/vault-state-log.md` (log externalisé depuis vault-state §9 au patch doctrine 2026-05-16, rolling 14j).
- Si une nouvelle racine est apparue pendant le cleaning : appliquer la procédure §5 (mise à jour 3 fichiers).

### Découpage en sous-commits

Recommandé pour la traçabilité :

- Commit 1 : doctrine (si modif de conventions ou de ce fichier)
- Commit 2 : mapping noyau (TSV partiel)
- Commit 3 : mapping orphelins (script + TSV)
- Commit 4 : script migration + dry-run
- Commit 5 : migration appliquée
- Commit 6 : cleanup + update vault-state

Chaque commit ≤10 minutes de travail. Si le shell coupe (cloud session, idle timeout), reprendre depuis le dernier commit.

## 8. Triggers de cleaning

À déclencher quand :

- `_meta/vault-state.md §13` montre **conformité <95%** (présence de tags hors nomenclature dans le frontmatter de notes existantes).
- Nb tags distincts **>120**.
- Un tag plat hors racines actuelles est détecté pendant un triage et **n'est pas justifiable par une nouvelle racine** (cf. §5). Cleaning ciblé sur ce tag suffit.
- À la demande explicite de l'utilisateur ("lance un cleaning des tags du vault").

À ne pas déclencher si :

- Le seul "non-compliant" détecté est en réalité un signal d'une racine émergente. Dans ce cas, appliquer §5 (proposer racine) plutôt que cleaning.

## 9. Tone et format

Ce fichier suit les règles de tous les `_meta/*-criteria.md` :

- Pas d'em dash dans le contenu écrit (règle CLAUDE.md). Utiliser virgules, deux-points, parenthèses, retour à la ligne.
- Direct, factuel, pas de flatterie.
- Self-contained : un agent doit pouvoir exécuter la pose ou le cleaning rien qu'avec ce fichier (plus `conventions.md` en référence si besoin de la doctrine source).
- Si l'utilisateur propose une évolution qui dérive vers la complexité (ex. ajouter un 3ème niveau de hiérarchie tag), signaler.
