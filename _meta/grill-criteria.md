---
type: meta
purpose: critères pour décider si une note inbox mérite un grill-me avant classification
version: v1
status: active
created: 2026-04-25
last_updated: 2026-04-25
---

<!--
Changelog : externalisé vers _meta/doctrine-changelog.md (consulté à la demande).
Doctrine V1 anonymisée, packagée comme produit SAMPL-IQ.
-->

# Critères de grill-me

Ce fichier pilote l'agent obsidian-triage pour décider si une note inbox
mérite un passage par le skill `grill-me` avant classification. Le but :
challenger les notes qui en valent la peine, sans transformer chaque
capture en interrogatoire.

## 1. Quand proposer un grill-me

### Plan ou design avec dépendances multiples

Signaux :
- plusieurs étapes interdépendantes (A conditionne B conditionne C)
- mention d'incertitudes ou choix non tranchés ("à voir", "je pense que")
- contraintes externes (budget, deadline, parties prenantes)
- enchaînement implicite que la note ne déroule pas

Pourquoi : grill-me force à expliciter chaque dépendance et à vérifier que
les hypothèses tiennent ensemble plutôt qu'isolément.

> Exemple illustratif : "Idée d'organiser un séminaire annuel équipe
> Acme, budget ~30k, lieu sud de la France, sponsoring partiel par X."

### Décision de vie ou objectif long terme

Signaux :
- impact sur plus de 6 mois
- irréversibilité partielle (déménagement, réduction de temps de travail)
- énoncé en "je devrais", "je voudrais", "il faudrait"
- lié à valeurs ou identité

Pourquoi : exposer les coûts cachés et les hypothèses optimistes avant que
la décision se cristallise en évidence.

> Exemple illustratif : "Réduire à 4 jours par semaine sur Acme pour
> libérer du temps perso et créatif."

### Thèse stratégique business

Signaux :
- prédiction sur un marché ou une industrie
- hypothèse d'opportunité ou de pivot
- mention de concurrents ou tendances
- énoncé en "à terme X va devenir Y"

Pourquoi : exposer les assumptions, identifier les kill criteria, repérer
les angles morts.

> Exemple illustratif : "Le SaaS classique va être remplacé par des
> services AI en 2 à 3 ans, donc Acme doit pivoter."

### Concept philosophique en construction

Signaux :
- tentative de définir une notion floue
- opposition de concepts ("X n'est pas Y mais Z")
- intuition pas encore mise en mots ("je sens que...")
- pas encore lié à des Atoms ou Sources existants

Pourquoi : grill-me aide à distinguer la pensée originale du déjà-pensé,
à repérer les contradictions internes, à choisir le bon vocabulaire.

> Exemple illustratif : "La liberté n'est pas l'absence de contraintes
> mais le bon choix de contraintes."

### Hypothèse à challenger

Signaux :
- énoncé en "et si..."
- contre-intuitif ou contraire au consensus
- prédictif et testable en principe
- formulé comme certitude sans support visible

Pourquoi : c'est exactement la job du grill, exposer la note à des angles
d'attaque que l'utilisateur ne voit pas seul.

> Exemple illustratif : "Tous mes meilleurs investissements sont venus de
> moments où j'étais en désaccord avec le consensus."

### Choix d'investissement ou allocation de capital

Signaux :
- montant explicite
- horizon de placement
- mention d'alternatives (ETF vs actions vs immobilier)
- niveau de conviction affiché

Pourquoi : capital alloué = irréversibilité partielle, biais émotionnels
fréquents (FOMO, ancrage, surconfiance).

> Exemple illustratif : "Allouer 30k sur ETF émergents, conviction 5 ans,
> malgré la volatilité court terme."

### Intention contemplative

Signaux :
- note classifiée (ou en passe de l'être) comme Intention
- `horizon: years` ou `horizon: someday`
- formulation contemplative ou velléitaire ("j'aimerais bien", "un jour", "sérieusement")
- pas de premier pas concret énoncé

Pourquoi : grill-me aide à distinguer une vraie envie ancrée d'un caprice
passager, et à clarifier le "premier pas" réaliste. Sans ce passage, la
note risque de rester dormante des années sans jamais bouger ni s'éteindre
proprement.

> Exemple illustratif : "j'aimerais bien apprendre le portugais
> sérieusement un jour" → grill peut faire émerger : pourquoi maintenant,
> premier pas concret, échéance à se donner.

### Question ouverte profonde

Signaux :
- note classifiée (ou en passe de l'être) comme Question
- `domain: philosophy` ou `domain: business`
- `priority: high`
- tone contemplatif sur un sujet à enjeu (identité, stratégie, valeurs)

Pourquoi : grill-me permet de structurer l'arbre des sous-questions,
identifier les hypothèses cachées, faire émerger les angles non explorés,
et potentiellement produire des Atoms de réponse partielle reliés à la
Question via `related_atoms`. Sans ce passage, la Question peut rester
floue et ne jamais déclencher de réflexion structurée.

> Exemple illustratif : "comment Acme survit dans 5 ans si
> commoditisation IA ?" → grill peut faire émerger : quelles hypothèses
> sur le rythme de commoditisation, quels signaux early warning, quels
> positionnements alternatifs, quelles protections fossées défendables.

## 2. Quand NE PAS proposer un grill-me

Patterns où grill-me serait friction inutile :

| Pattern | Exemple | Destination |
|---|---|---|
| Donnée factuelle brute | "Anthropic dit que 70% du code Claude est écrit par Claude" | Atom (data) |
| Citation | "Camus : 'Il faut imaginer Sisyphe heureux'" | Atom (quote) |
| Idée cadeau ou todo court | "Idée cadeau pour Sam : livre sur la permaculture" | Update People note |
| Capture de moment | "Sentiment ce matin : tout est plus calme quand je m'éloigne du téléphone" | Atom (creative) ou Log |
| Observation terrain | "Les fraises et les épinards sont de bons compagnons" | Atom (rule) |
| Note déjà mature | Réflexion structurée avec arguments, contre-arguments, décision déjà prise | Classifier tel quel |

Règle de pouce : si la note serait égale à elle-même après 5 questions de
grill, ne pas proposer. Le grill doit changer la note, sinon il coûte du
temps pour rien.

## 3. Format de la proposition

### Ne pas faire

- question fermée : "On grille ?"
- pression : "Ça mérite vraiment un grill-me"
- proposition sans alternative

### Faire

Structure type :

```
Cette note touche à <thème>.
J'identifie <N> dépendances ou hypothèses non explicitées :
- <hypothèse 1>
- <hypothèse 2>
- <hypothèse 3>

Coût estimé : ~<N> questions, ~<durée> minutes.

Action : creuser via grill-me / classifier tel quel / skip
```

Toujours :
- un constat sur ce qui mérite grill (pas une demande aveugle)
- l'estimation de coût (questions + durée)
- l'option "classifier tel quel" comme alternative explicite
- l'option "skip" si l'utilisateur veut différer

## 4. Comportement après grill-me

### Réintégration dans la note finale

L'agent extrait du transcript du grill :
- 3 à 5 insights nouveaux ou clarifiés
- les hypothèses qui ont tenu
- les hypothèses qui sont tombées (utile : L'utilisateur saura ce qu'il a écarté)
- les décisions prises

Ces éléments sont synthétisés et intégrés dans la note finale, pas
collés en verbatim. La note doit rester dense et lisible hors contexte.

### Éviter le bloating

- pas de paste du transcript dans la note source
- pas de section "Grill-me" qui occupe 80% de la note
- la note finale ressemble à une note normale du type cible (Atom, Map,
  Project, etc.), pas à un transcript d'interview

### Recommandation : créer un Log séparé pour le grill brut

Oui, créer un fichier dans `6-logs/events/` avec le format :

`YYYY-MM-DD-grill-<slug-de-la-note-source>.md`

> Exemple illustratif : `2026-04-25-grill-pivot-services-ai.md`

Frontmatter du Log de grill (subtype `grill-event`) :

```yaml
---
type: log
subtype: grill-event
date: 2026-04-25
produced_note: [[slug-de-la-note-finale]]
people: []
projects: []
mood: 
---
```

Contenu : transcript brut du grill, structuré question / réponse.

Lien depuis la note finale (Atom ou autre) via le frontmatter :

```yaml
derived_from_grill: [[2026-04-25-grill-pivot-services-ai]]
```

Les deux champs sont symétriques : `produced_note` pointe du Log vers la
note finale, `derived_from_grill` pointe de la note finale vers le Log.
Ces deux champs sont documentés dans [[conventions]].

Bénéfices :
- la note source reste propre
- le transcript reste accessible si l'utilisateur veut ré-explorer
- recherche future possible sur les grills passés (ce qui a été challengé,
  comment, avec quel résultat)

Coût : un fichier Log de plus par grill. Acceptable vu la valeur
archivistique.
