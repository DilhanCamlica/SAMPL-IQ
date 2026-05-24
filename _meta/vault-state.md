---
type: meta
purpose: dashboard dynamique de l'état de maturité du vault, lu en début de session par les agents pour s'orienter, mis à jour en fin de session
version: v1
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
last_session_id: null
---

<!--
Changelog
YYYY-MM-DD : fichier seed du produit SAMPL-IQ. Dashboard vierge, tous les
compteurs à zéro. À la première vraie session de travail, l'agent recalcule
§1 et §2 via les snippets §10, puis maintient ce fichier à jour en fin de
chaque session (discipline §11). Référencé depuis [[sessions-criteria]],
[[triage-criteria]], [[transcripts-import-criteria]], [[journaling-criteria]]
comme étape de lecture en début de session et de mise à jour en fin.
-->

# État du vault

Ce fichier est un **dashboard dynamique** de l'état de maturité du contenu du vault. Il sert deux usages :

1. **À l'entrée d'une session** : un agent (cloud, Mac, mobile) lit ce fichier après `CLAUDE.md` pour comprendre où le vault est faible et orienter l'utilisateur vers les enrichissements à plus fort levier, sans avoir à re-parcourir toutes les notes.
2. **À la sortie d'une session** : l'agent recalcule les compteurs et append une ligne au log dans [[vault-state-log]].

Ce fichier est **distinct** de `_meta/doctrine-roadmap.md` :

- `doctrine-roadmap.md` trace l'évolution de la **doctrine** (types pending, triggers d'activation).
- `vault-state.md` (ce fichier) trace l'évolution du **contenu** (compteurs, hubs, zones sous-représentées, sessions à recommander).

Si tu hésites à modifier l'un ou l'autre : la doctrine vit ailleurs, ici on ne décrit que l'état réel et les recommandations.

> [!note] Vault neuf
> Ce dashboard est dans son état initial. Tant que le vault est quasi vide, les sections §3 à §8 resteront pauvres : c'est normal. Elles se remplissent organiquement au fil des captures, triages et sessions. Le premier réflexe utile est de capturer puis trier quelques notes (voir `ONBOARDING.md`).

## 1. Compteurs

Snapshot initial (vault neuf, seuls `_meta/` et `CLAUDE.md` sont peuplés) :

| Type | Notes | Évolution depuis dernière session |
|---|---|---|
| 0-inbox | 0 | n/a |
| 1-atoms | 0 | n/a |
| 2-people | 0 | n/a |
| 3-sources | 0 | n/a |
| 4-projects | 0 | n/a |
| 5-maps | 0 | n/a |
| 6-logs | 0 | n/a |
| 7-intentions | 0 | n/a |
| 8-questions | 0 | n/a |
| **Total typés** | **0** | n/a |

## 2. Complétude des champs YAML structurants

Mesure la part des Atoms reliés à une Map / People / Source (un Atom orphelin est un signal de graphe pauvre). À recalculer via le snippet Python §10 dès qu'il existe des Atoms.

| Champ sur 1-atoms/ | % rempli | Cible |
|---|---|---|
| `maps:` | n/a (0 atom) | > 70% |
| `people:` | n/a | contextuel |
| `source:` | n/a | contextuel |

## 3. Cartographie des hubs (Maps)

Les Maps sont les hubs du graphe. Cette section liste les Maps existantes, leur maturité (`stub | growing | mature`) et le nombre d'objets qui pointent vers elles. Vide tant qu'aucune Map n'est créée.

_Aucune Map pour l'instant._

## 4. Zones de vie sous-représentées

Domaines de la vie de l'utilisateur peu ou pas couverts par le vault, à enrichir en priorité. Se remplit quand l'utilisateur a posé assez de contenu pour qu'un déséquilibre apparaisse.

_À déterminer après les premières sessions._

## 5. Questions ouvertes prioritaires en attente

Questions `status: open` et `priority: high` qui méritent une session de creusage. Vide tant qu'aucune Question n'est créée.

_Aucune Question pour l'instant._

## 6. Intentions dormantes

Intentions `status: dormant` ou anciennes `active` jamais rouvertes, candidates à réactivation ou abandon. Vide tant qu'aucune Intention n'est créée.

_Aucune Intention pour l'instant._

## 7. Portes d'entrée recommandées (prochaine session)

Recommandations concrètes pour la prochaine session de travail (voir les 8 portes d'entrée de [[sessions-criteria]]). Tant que le vault est neuf, la seule recommandation est :

- **Amorcer le flux de capture** : capturer 5 à 10 pensées brutes dans `0-inbox/`, puis lancer un premier triage pour voir le système typer le contenu. Voir `ONBOARDING.md` §"Premiers pas".

## 8. Volumétrie sources (doctrine "Source allégée")

Suit la taille des notes Source pour éviter qu'elles ne deviennent des copies intégrales de transcripts (doctrine "Source allégée" : la Source structure et pointe, l'archive durable reste externe). Vide tant qu'aucune Source n'est créée.

_Aucune Source pour l'instant._

## 9. Log des sessions

Externalisé vers [[vault-state-log]] pour alléger le cold-start agent. Le log live (rolling 14 jours) vit dans `_meta/vault-state-log.md`. Les entrées plus anciennes sont archivées trimestriellement dans `_meta/archive/vault-state-log-<YYYY-Q>.md` (le dossier `archive/` est créé à la demande).

**Discipline d'append à chaque session** : voir §11 ci-dessous. La cible d'append est `_meta/vault-state-log.md`, pas ce fichier.

**Cold-start agent** : NE PAS charger `vault-state-log.md` au démarrage. Il est consulté uniquement à la demande pour retracer une décision ou vérifier qu'une Map est recommandée depuis ≥3 sessions consécutives (lifecycle §4).

## 10. Comment recalculer (référence pour les agents)

Snippets bash/python utiles pour mettre à jour les compteurs §1 et §2 en fin de session sans re-parcourir tout le vault à la main.

```bash
# §1 Compteurs simples
for d in 0-inbox 1-atoms 2-people 3-sources 4-projects 5-maps 6-logs 7-intentions 8-questions; do
  echo "$d: $(find $d -name '*.md' -type f | wc -l)"
done
```

```python
# §2 Complétude YAML structurants sur 1-atoms/
import os, re
total=with_maps=with_people=with_source=0
for f in sorted(os.listdir('1-atoms')):
    if not f.endswith('.md'): continue
    total+=1
    content=open(f'1-atoms/{f}').read()
    fm=re.match(r'^---\n(.+?)\n---', content, re.DOTALL)
    if not fm: continue
    fm=fm.group(1)
    if re.search(r'^maps:(.*?)(?=^[a-z_]+:|\Z)', fm, re.M|re.S) and '[[' in re.search(r'^maps:(.*?)(?=^[a-z_]+:|\Z)', fm, re.M|re.S).group(1):
        with_maps+=1
    if re.search(r'^people:(.*?)(?=^[a-z_]+:|\Z)', fm, re.M|re.S) and '[[' in re.search(r'^people:(.*?)(?=^[a-z_]+:|\Z)', fm, re.M|re.S).group(1):
        with_people+=1
    if re.search(r'^source:(.*?)(?=^[a-z_]+:|\Z)', fm, re.M|re.S) and '[[' in re.search(r'^source:(.*?)(?=^[a-z_]+:|\Z)', fm, re.M|re.S).group(1):
        with_source+=1
print(f'Total atoms: {total}')
if total:
    print(f'maps: {with_maps} ({100*with_maps//total}%)')
    print(f'people: {with_people} ({100*with_people//total}%)')
    print(f'source: {with_source} ({100*with_source//total}%)')
```

## 11. Discipline de mise à jour

Déroulée par `_meta/sessions-criteria.md`, `_meta/triage-criteria.md`, `_meta/transcripts-import-criteria.md`, `_meta/journaling-criteria.md`, `_meta/lifecycle-criteria.md` :

**En début de session** : lire ce fichier après `CLAUDE.md`. Utiliser §7 pour proposer une porte d'entrée si l'utilisateur n'en a pas spécifié une. **Ne PAS charger `_meta/vault-state-log.md` en cold-start** (cf. §9 ci-dessus, le log est consulté à la demande uniquement).

**En fin de session** :

1. Recalculer §1 (compteurs) si des notes ont été créées/supprimées.
2. Recalculer §2 (complétude YAML) si des Atoms ont été créés ou modifiés.
3. Mettre à jour §3 si une Map a changé de maturité ou gagné/perdu des atoms attachés notables.
4. Mettre à jour §4-§6 si une zone, une question ou une intention a évolué.
5. Mettre à jour §7 (recommandations next-session) en fonction de ce qui a bougé.
6. **Append à `_meta/vault-state-log.md`** : 1 ligne avec date, type de session, résumé court (<30 mots).
7. Mettre à jour le frontmatter `last_updated` et `last_session_id` de ce fichier (vault-state.md).
8. **Archivage rolling 14 jours `vault-state-log.md`** : si la première entrée (la plus ancienne) date de plus de 14 jours, la déplacer dans `_meta/archive/vault-state-log-<YYYY-Q>.md` correspondant à son trimestre. Créer le fichier d'archive (et le dossier `archive/`) s'il n'existe pas.

Si la session est triviale (1 capture inbox, pas de structurel), update §1 + append log + check archivage suffit.

## 12. Tone

Ce fichier ne contient **pas de jugement émotionnel**, pas de "bravo, tu progresses". C'est un état des lieux factuel. Les agents qui lisent ce fichier l'utilisent pour orienter, pas pour féliciter ou pousser.

Pas d'em dash dans ce fichier (règle CLAUDE.md). Utiliser virgules, deux-points, parenthèses, retour à la ligne.

## 13. Hygiène des tags

Le vault démarre sans tag. La liste des racines de tags est **évolutive** (pas une closed list) et se construit organiquement. Toute la doctrine de pose et de cleaning des tags vit dans [[tag-hygiene-criteria]].

| Métrique | Valeur | Cible |
|---|---|---|
| Tags distincts dans le frontmatter | 0 | tenir bas par hygiène régulière |
| Total occurrences | 0 | n/a |
| Conformité hiérarchie (`racine/sous-tag` ou racine pure) | n/a | 100% |
| Racines actuelles effectivement utilisées | 0 | (liste évolutive) |

**Discipline** :

- Tout nouveau tag dans une note doit être conforme : `racine/sous-tag` (2 niveaux strict) ou racine pure.
- La liste des racines est **évolutive**. Si une note touche un domaine absent, proposer une nouvelle racine via la procédure [[tag-hygiene-criteria]] §5.
- Au triage, vérifier que les tags ajoutés sont conformes.
- Cible long-terme : les sous-tags à 1 occurrence sont des candidats à fusion ou suppression à chaque triage qui les recroise.

**Procédure d'audit et de cleaning** : voir [[tag-hygiene-criteria]] §6 (audit lecture seule) et §7 (procédure de cleaning relançable). Triggers de cleaning dans §8 du même fichier.
