---
type: meta
purpose: doctrine-index
version: v1
last_updated: 2026-04-29
---

# Doctrine du vault

## Philosophie

Une note = un objet. Les relations sont des liens, pas des dossiers.

Le vault est une base relationnelle en markdown plat : les types sont des tables,
les wikilinks sont des foreign keys. Pas d'arborescence thématique. Le croisement
est natif (une note a autant de liens qu'elle veut), l'ajout d'un domaine ne casse
rien (on crée une nouvelle Map, elle se remplit organiquement).

## Les 8 types de notes

| Type | Rôle | Dossier | Exemple |
|---|---|---|---|
| Atom | Idée, citation, règle, donnée. Unité de pensée atomique. | `1-atoms/` | `anthropic-70-pct-code-claude.md` |
| People | Une personne, un fichier. | `2-people/` | `sam-doe.md` |
| Source | Livre, article, podcast, vidéo, conversation. | `3-sources/` | `sequoia-services-as-new-software.md` |
| Project | Initiative bornée dans le temps avec un objectif. | `4-projects/` | `apprendre-blackjack-2026.md` |
| Map | Index vivant sur un domaine. Pas un essai, un hub. | `5-maps/` | `permaculture.md` |
| Log | Journal daté ou événement ponctuel. | `6-logs/journal/` ou `6-logs/events/` | `2026-04-25.md` |
| Intention | Cible personnelle sans deadline, horizon flou. | `7-intentions/` | `lire-cyberpunk-william-gibson.md` |
| Question | Interrogation ouverte sans réponse, à creuser plus tard. | `8-questions/` | `comment-acme-survit-si-commoditisation-ia.md` |

## Arborescence

```
~/Documents/<VotreVault>/
├── 0-inbox/              capture brute (input agent V1)
├── 1-atoms/              idées, citations, règles, datas
├── 2-people/             un fichier par personne
├── 3-sources/            livres, articles, podcasts
├── 4-projects/           projets bornés dans le temps
├── 5-maps/               notes d'index par domaine
├── 6-logs/
│   ├── journal/          entrées datées (YYYY-MM-DD.md)
│   └── events/           événements ponctuels
├── 7-intentions/         engagements personnels sans deadline
├── 8-questions/         interrogations ouvertes sans réponse
└── _meta/
    ├── templates/             un template par type
    ├── scripts/               outils utilitaires read-only (lifecycle-lint.py)
    ├── README.md              ce fichier
    ├── conventions.md         nommage et schemas frontmatter
    ├── capture-criteria.md    workflow capture inbox (skill obsidian-capture)
    ├── triage-criteria.md     workflow triage inbox (skill obsidian-triage)
    ├── sessions-criteria.md   workflow sessions de travail (8 portes + free roam)
    ├── transcripts-import-criteria.md  workflow import transcript de call (skill obsidian-transcripts-to-inbox)
    ├── journaling-criteria.md  workflow rituel journal-daily (détecté par obsidian-triage)
    ├── lifecycle-criteria.md   checklist clôture aval (intentions, Maps, People, déroulée au triage et en fin de session)
    ├── grill-criteria.md      workflow grill-me
    ├── tag-hygiene-criteria.md doctrine + procédure cleaning des tags (référence pose courante + cleaning relançable)
    ├── toilettage-rules.md    règles de nettoyage du texte
    ├── doctrine-roadmap.md    roadmap d'évolution doctrine (trous structurels + triggers)
    ├── identite-civile.md     facts civils objectifs sur l'utilisateur (lu par les agents)
    ├── rituals.md             rituel de fermeture hebdo
    ├── vault-doctrine-v1.md   doctrine source longue
    ├── vault-state.md         dashboard dynamique de maturité du vault (lu en début de session, mis à jour en fin)
    ├── vault-state-log.md     log des sessions externalisé depuis vault-state §9 (NE PAS charger en cold-start, consulté à la demande)
    └── doctrine-changelog.md  historique des évolutions de la doctrine externalisé depuis les commentaires HTML (NE PAS charger en cold-start, consulté à la demande)
```

Les préfixes numériques `0-`, `1-` sont là pour ordonner la sidebar Obsidian.
Aucune autre fonction.

## Notion vs Obsidian

Obsidian est l'**émetteur** (réflexion personnelle). Notion est l'**opérationnel**
(process partagé, équipe, clients). Quand une réflexion perso devient un process
à exécuter en équipe, elle migre vers Notion (transformée pour l'audience), et
la note Obsidian originale garde une référence.

Voir la doctrine source pour le tableau complet de routage.

## Liens utiles

- [[conventions]] : nommage de fichiers et schemas frontmatter par type
- [[capture-criteria]] : workflow de capture inbox (source de vérité du skill `obsidian-capture`)
- [[triage-criteria]] : workflow de triage inbox (source de vérité du skill `obsidian-triage`)
- [[sessions-criteria]] : workflow des sessions de travail (8 portes d'entrée + free roam)
- [[transcripts-import-criteria]] : workflow d'import d'un transcript de call, quel que soit l'outil (Grain, tl;dv, Fathom, Fireflies, etc.), source de vérité du skill `obsidian-transcripts-to-inbox`
- [[journaling-criteria]] : workflow du rituel journal-daily (détecté et déclenché par `obsidian-triage` quand une note inbox correspond au pattern, voir aussi [[triage-criteria]] §0)
- [[lifecycle-criteria]] : checklist de clôture aval (intentions consommables, Maps maturity, People last_seen, Map manquante). Déroulée au triage ([[triage-criteria]] §8.2) et en fin de session ([[sessions-criteria]] §2 phase 7). Source de vérité unique de la cohérence du graphe post-cristallisation typée.
- [[grill-criteria]] : workflow grill-me (interview stress-test d'un plan ou design)
- [[tag-hygiene-criteria]] : doctrine et procédure d'hygiène des tags (référence pour la pose courante + procédure de cleaning relançable). Lu par tout agent qui ajoute un tag à une note.
- [[toilettage-rules]] : règles de nettoyage du texte (référencé depuis capture-criteria)
- [[doctrine-roadmap]] : roadmap d'évolution de la doctrine (trous structurels identifiés et triggers d'activation)
- [[identite-civile]] : facts civils objectifs sur l'utilisateur du vault, lus par les agents en début de session pour contextualisation opérationnelle
- [[rituals]] : rituel de fermeture hebdo (4 questions, 5 minutes)
- [[vault-doctrine-v1]] : doctrine source longue (la version complète)
- [[vault-state]] : dashboard dynamique de l'état de maturité du vault (compteurs, hubs, zones sous-représentées, recommandations next-session). Lu en début de session par les agents pour s'orienter, mis à jour en fin de session.
- [[vault-state-log]] : log append-only des sessions et clusters, externalisé depuis vault-state §9 au patch doctrine 2026-05-16 pour alléger le cold-start agent (rolling 14 jours, gain ~21k tokens en cold-start). **NE PAS charger en cold-start**, consulté uniquement à la demande (retracer une décision, vérifier qu'une Map est recommandée depuis ≥3 sessions, comprendre le contexte d'évolution d'un objet). Archives trimestrielles dans `_meta/archive/vault-state-log-<YYYY-Q>.md`.
- [[doctrine-changelog]] : historique append-only des évolutions de la doctrine `_meta/*.md`, externalisé depuis les commentaires HTML en tête de chaque fichier au patch doctrine 2026-05-16 (gain ~2k tokens en cold-start). Chaque fichier doctrine conserve dans son commentaire HTML uniquement les 3 dernières entrées + un pointeur vers ce fichier. **NE PAS charger en cold-start**, consulté uniquement à la demande pour retracer l'historique complet d'une règle ou comprendre pourquoi elle a été modifiée.
- `_meta/templates/` : un template par type, à dupliquer pour créer une nouvelle note
- `_meta/scripts/lifecycle-lint.py` : audit lecture-seule du vault qui produit une note inbox `device: lifecycle-audit` consommée par le prochain triage low-friction. Détecte 5 catégories de dérives (intentions à fermer, Maps maturity, People last_seen, Maps manquantes, doublons). Voir `_meta/scripts/README.md`.
