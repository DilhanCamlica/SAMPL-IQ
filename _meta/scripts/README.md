# Scripts utilitaires du vault

Outils en lecture seule pour auditer le vault sans modifier le contenu typé. Toute correction passe par la doctrine (triage low-friction, sessions), pas par les scripts.

## lifecycle-lint.py

Audit lecture-seule du vault qui produit une **note inbox** (`device: lifecycle-audit`) destinée à être consommée par le prochain triage low-friction.

### Usage

```bash
cd ~/Documents/<VotreVault>
python3 _meta/scripts/lifecycle-lint.py
```

### Pré-requis

- Python 3.9+
- PyYAML 6.0+ (déjà installé sur le Mac de l'utilisateur)

### Output

Une note dans `0-inbox/<YYYY-MM-DD-HHmm>-lifecycle-audit-<résumé>.md`, structurée en 5 sections :

1. Intentions actives candidates à fermer (auto vs manual confidence).
2. Maps avec maturity incohérente.
3. People avec `last_seen` obsolète.
4. Maps manquantes recommandées par vault-state.
5. Doublons sémantiques suspects.

### Consommation

Au prochain triage, l'agent détecte la note via son `device: lifecycle-audit` (cf. `_meta/triage-criteria.md` §0bis), la lit intégralement et intègre ses sections en tête du brief one-shot (§10). Les actions auto sont appliquées sans validation, les actions manuelles passent par le brief avec defaults publiés. La note est absorbée (supprimée) à la fin du triage.

### Limitations connues

- Faux positifs sur les wikilinks aliasés `[[slug|texte]]` : l'alias est ignoré (slug seul gardé). Pas critique.
- Frontmatter cassé : les fichiers avec YAML invalide sont signalés en fin de note inbox sans crasher le script.
- Détection de doublons : seuil bas (≥2 signaux convergents), faux positifs probables, validation requise au triage.
- Détection de Maps manquantes : repose sur les wikilinks dans `vault-state.md` §4 et §7. Si un slug est référencé sans crochets, il est manqué.

### Mode strictement read-only

Le script ne modifie **aucun** fichier sauf la note inbox produite. Pas d'argument `--apply`, pas d'auto-fix. Toute correction structurelle passe par la doctrine.
