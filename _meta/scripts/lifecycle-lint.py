#!/usr/bin/env python3
"""
lifecycle-lint.py

Audite le vault Obsidian de l'utilisateur en lecture seule et produit une note
inbox structurée (`device: lifecycle-audit`) qui sera consommée par le
prochain triage low-friction.

5 catégories de détection :
  1. Intentions actives candidates à fermer (auto vs manual confidence)
  2. Maps avec maturity incohérente (stub avec ≥5 atoms, growing avec <5
     ou ≥15)
  3. People avec last_seen obsolète (dernière mention dérivée >7j après)
  4. Maps manquantes recommandées (vault-state §4/§7 ≥3 sessions + ≥3
     atoms candidats)
  5. Doublons sémantiques suspects (≥2 signaux convergents)

Mode strictement read-only sur les notes existantes. Le seul fichier écrit
est la note inbox produite.

Usage : `python3 _meta/scripts/lifecycle-lint.py`
       (à lancer depuis la racine du vault)

Doctrine de référence :
  - _meta/lifecycle-criteria.md §2-§4 et §7
  - _meta/triage-criteria.md §0bis et §9-§10
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from datetime import datetime, date, timedelta
from pathlib import Path

import yaml


VAULT_ROOT = Path(__file__).resolve().parents[2]
INBOX_DIR = VAULT_ROOT / "0-inbox"
ATOMS_DIR = VAULT_ROOT / "1-atoms"
PEOPLE_DIR = VAULT_ROOT / "2-people"
SOURCES_DIR = VAULT_ROOT / "3-sources"
PROJECTS_DIR = VAULT_ROOT / "4-projects"
MAPS_DIR = VAULT_ROOT / "5-maps"
LOGS_DIR = VAULT_ROOT / "6-logs"
INTENTIONS_DIR = VAULT_ROOT / "7-intentions"
QUESTIONS_DIR = VAULT_ROOT / "8-questions"
VAULT_STATE = VAULT_ROOT / "_meta" / "vault-state.md"

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
H2_RE = re.compile(r"^## (?!\s*$)", re.MULTILINE)
SLUG_VERB_PREFIXES = {
    "appeler": ("conversation",),
    "parler": ("conversation",),
    "joindre": ("conversation",),
    "rencontrer": ("conversation",),
    "revoir": ("conversation",),
    "voir": ("video", "conversation"),
    "regarder": ("video",),
    "lire": ("book", "article"),
    "apprendre": ("book", "video", "podcast", "article"),
    "ecouter": ("podcast",),
    "rattraper": ("conversation",),
    "reprendre": ("conversation",),
    "debriefer": ("conversation",),
}


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Parse front matter et body. Retourne ({}, '') si parsing impossible."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}, ""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {"_parse_error": True}, parts[2]
    if not isinstance(fm, dict):
        return {}, parts[2]
    return fm, parts[2]


def extract_wikilinks(value) -> list[str]:
    """Extrait les slugs de wikilinks depuis une valeur YAML.

    Gère :
    - string `"[[slug]]"` → ['slug']
    - liste de strings `["[[a]]", "[[b]]"]` → ['a', 'b']
    - liste de listes (parsing YAML de `- [[slug]]` non quoté) :
      `[['slug']]` → ['slug']
    - mix.
    """
    if value is None:
        return []
    out: list[str] = []
    if isinstance(value, list):
        for item in value:
            out.extend(extract_wikilinks(item))
        return out
    if isinstance(value, str):
        wikilinks = WIKILINK_RE.findall(value)
        if wikilinks:
            out.extend(wikilinks)
        elif re.fullmatch(r"[a-z0-9][a-z0-9\-]*", value):
            # Slug non wikilinké (ex: liste YAML écrite `- slug-name` sans crochets).
            out.append(value)
        return out
    return out


def to_date(value) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
    return None


def slug_of(path: Path) -> str:
    return path.stem


def list_md(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(p for p in directory.rglob("*.md") if p.is_file())


def main() -> int:
    parse_errors: list[str] = []

    # Index global ----------------------------------------------------------
    intentions = []
    for path in list_md(INTENTIONS_DIR):
        fm, body = parse_frontmatter(path)
        if fm.get("_parse_error"):
            parse_errors.append(str(path.relative_to(VAULT_ROOT)))
            continue
        if fm.get("type") != "intention":
            continue
        intentions.append(
            {
                "slug": slug_of(path),
                "path": path,
                "status": fm.get("status"),
                "created": to_date(fm.get("created")),
                "people": extract_wikilinks(fm.get("people")),
                "sources": extract_wikilinks(fm.get("sources")),
            }
        )

    sources = []
    for path in list_md(SOURCES_DIR):
        if path.suffix != ".md":
            continue
        fm, body = parse_frontmatter(path)
        if fm.get("_parse_error"):
            parse_errors.append(str(path.relative_to(VAULT_ROOT)))
            continue
        if fm.get("type") != "source":
            continue
        sources.append(
            {
                "slug": slug_of(path),
                "path": path,
                "medium": fm.get("medium"),
                "date_consumed": to_date(fm.get("date_consumed")),
                "participants": extract_wikilinks(fm.get("participants")),
                "body_people": extract_wikilinks(body),
            }
        )

    logs_events = []
    for path in list_md(LOGS_DIR / "events"):
        fm, body = parse_frontmatter(path)
        if fm.get("_parse_error"):
            parse_errors.append(str(path.relative_to(VAULT_ROOT)))
            continue
        logs_events.append(
            {
                "slug": slug_of(path),
                "path": path,
                "date": to_date(fm.get("date")),
                "people": extract_wikilinks(fm.get("people")),
                "body_people": extract_wikilinks(body),
            }
        )

    atoms = []
    atom_maps = defaultdict(list)
    for path in list_md(ATOMS_DIR):
        fm, body = parse_frontmatter(path)
        if fm.get("_parse_error"):
            parse_errors.append(str(path.relative_to(VAULT_ROOT)))
            continue
        if fm.get("type") != "atom":
            continue
        a = {
            "slug": slug_of(path),
            "path": path,
            "created": to_date(fm.get("created")),
            "tags": fm.get("tags") or [],
            "people": extract_wikilinks(fm.get("people")),
            "maps": extract_wikilinks(fm.get("maps")),
            "source": extract_wikilinks(fm.get("source")),
            "title": (body.lstrip().split("\n", 1)[0].lstrip("# ").strip() or path.stem),
        }
        atoms.append(a)
        for m in a["maps"]:
            atom_maps[m].append(a["slug"])

    maps_existing = {}
    for path in list_md(MAPS_DIR):
        fm, body = parse_frontmatter(path)
        if fm.get("_parse_error"):
            parse_errors.append(str(path.relative_to(VAULT_ROOT)))
            continue
        if fm.get("type") != "map":
            continue
        vision_match = re.search(
            r"^##\s+Vision\s*\n+(.+?)(?=\n##\s|\Z)", body, re.MULTILINE | re.DOTALL
        )
        vision_lines = 0
        if vision_match:
            content = vision_match.group(1).strip()
            content = re.sub(r"^>\s*\[!.*?\].*", "", content, flags=re.MULTILINE)
            vision_lines = len([l for l in content.splitlines() if l.strip()])
        h2_count = len(H2_RE.findall(body))
        maps_existing[slug_of(path)] = {
            "slug": slug_of(path),
            "path": path,
            "maturity": fm.get("maturity"),
            "vision_ok": vision_lines >= 2,
            "h2_count": h2_count,
            "atoms_attached": len(atom_maps.get(slug_of(path), [])),
        }

    people = {}
    for path in list_md(PEOPLE_DIR):
        fm, body = parse_frontmatter(path)
        if fm.get("_parse_error"):
            parse_errors.append(str(path.relative_to(VAULT_ROOT)))
            continue
        if fm.get("type") != "people":
            continue
        people[slug_of(path)] = {
            "slug": slug_of(path),
            "path": path,
            "last_seen": to_date(fm.get("last_seen")),
        }

    # 1. Intentions actives candidates à fermer -----------------------------
    intentions_auto: list[str] = []
    intentions_manual: list[str] = []

    for it in intentions:
        if it["status"] != "active":
            continue
        if not it["people"] or not it["created"]:
            continue
        verb = it["slug"].split("-", 1)[0]
        expected_media = SLUG_VERB_PREFIXES.get(verb)
        candidates = []
        for src in sources:
            if not src["date_consumed"]:
                continue
            if src["date_consumed"] < it["created"]:
                continue
            people_match = bool(set(it["people"]) & set(src["participants"]))
            if not people_match:
                continue
            verb_ok = expected_media is not None and src["medium"] in expected_media
            within_30 = (src["date_consumed"] - it["created"]).days <= 30
            score = sum([people_match, verb_ok, within_30])
            candidates.append((score, src, verb_ok, within_30))
        if not candidates:
            continue
        candidates.sort(key=lambda x: (-x[0], x[1]["date_consumed"]))
        score, src, verb_ok, within_30 = candidates[0]
        line = (
            f"- [[{it['slug']}]] (active depuis {it['created']}, "
            f"{(date.today() - it['created']).days} jours)\n"
            f"  → Source [[{src['slug']}]] (medium: {src['medium']}, "
            f"{', '.join(it['people'])} participant)\n"
        )
        if score == 3:
            line += (
                f"  → Action triage : fermeture auto, "
                f"`realized_at: {src['date_consumed']}`, "
                f"`sources: [[{src['slug']}]]`"
            )
            intentions_auto.append(line)
        else:
            missing = []
            if not verb_ok:
                missing.append(f"verbe/médium ({verb} vs {src['medium']})")
            if not within_30:
                missing.append("30 jours")
            line += (
                f"  → Action triage : à confirmer manuellement "
                f"(manque : {', '.join(missing) or 'people seul'})"
            )
            intentions_manual.append(line)

    # 2. Maps avec maturity incohérente ------------------------------------
    maps_incoherent: list[str] = []
    for slug, m in maps_existing.items():
        n = m["atoms_attached"]
        mat = m["maturity"]
        vision = m["vision_ok"]
        h2 = m["h2_count"]
        diag = None
        if mat == "stub" and n >= 5 and vision:
            diag = (
                f"`stub` avec {n} atoms attachés ET vision OK\n"
                f"  → Devrait être `growing`. Bascule auto au prochain triage "
                f"(lifecycle §2.4)"
            )
        elif mat == "growing" and n < 5:
            diag = (
                f"`growing` avec seulement {n} atoms attachés\n"
                f"  → Devrait être `stub`. Régression non auto, "
                f"validation requise (lifecycle §7.4)"
            )
        elif mat == "growing" and n >= 15 and vision and h2 >= 3:
            diag = (
                f"`growing` avec {n} atoms ET vision OK ET {h2} sous-sections H2\n"
                f"  → Devrait être `mature`. Bascule auto au prochain triage"
            )
        elif mat == "stub" and n == 4 and vision:
            diag = (
                f"`stub` avec {n} atoms (à la frontière). "
                f"Reste `stub`. Si 1 atom ajouté, bascule"
            )
        if diag:
            maps_incoherent.append(f"- [[{slug}]] : {diag}")

    # 3. People last_seen obsolète -----------------------------------------
    people_stale: list[str] = []
    last_mention: dict[str, tuple[date, str]] = {}
    for src in sources:
        if not src["date_consumed"]:
            continue
        for p in src["participants"]:
            cur = last_mention.get(p)
            if cur is None or src["date_consumed"] > cur[0]:
                last_mention[p] = (src["date_consumed"], src["slug"])
    for ev in logs_events:
        if not ev["date"]:
            continue
        for p in ev["people"]:
            cur = last_mention.get(p)
            if cur is None or ev["date"] > cur[0]:
                last_mention[p] = (ev["date"], ev["slug"])

    for slug, p in people.items():
        mention = last_mention.get(slug)
        if not mention:
            continue
        last_date, src_slug = mention
        if p["last_seen"] is None:
            people_stale.append(
                f"- [[{slug}]] : `last_seen` null, mentionné dans [[{src_slug}]] le {last_date}\n"
                f"  → MAJ auto last_seen → {last_date} (lifecycle §2.3)"
            )
        elif (last_date - p["last_seen"]).days > 7:
            people_stale.append(
                f"- [[{slug}]] : last_seen {p['last_seen']}, "
                f"mentionné dans [[{src_slug}]] le {last_date}\n"
                f"  → MAJ auto last_seen → {last_date} (lifecycle §2.3)"
            )

    # 4. Maps manquantes recommandées --------------------------------------
    maps_missing: list[str] = []
    vault_state_text = ""
    try:
        vault_state_text = VAULT_STATE.read_text(encoding="utf-8")
    except Exception:
        pass

    # Index global de tous les slugs existants dans le vault (tous types).
    # Un candidat Map manquante est un wikilink dans vault-state qui n'existe
    # dans aucun dossier typé (pas de fichier `<slug>.md`).
    all_existing_slugs = set()
    for d in (
        ATOMS_DIR, PEOPLE_DIR, SOURCES_DIR, PROJECTS_DIR,
        MAPS_DIR, LOGS_DIR, INTENTIONS_DIR, QUESTIONS_DIR,
    ):
        for p in list_md(d):
            all_existing_slugs.add(slug_of(p))

    referenced_in_state = set(WIKILINK_RE.findall(vault_state_text))
    missing_candidates = referenced_in_state - all_existing_slugs

    for slug in sorted(missing_candidates):
        if not re.search(r"^[a-z0-9-]+$", slug):
            continue
        occurrences = vault_state_text.lower().count(f"[[{slug}".lower())
        if occurrences < 2:
            continue
        slug_words = set(slug.split("-"))
        candidate_atoms = []
        for a in atoms:
            tag_words = set()
            tag_roots = set()
            for t in a["tags"]:
                if isinstance(t, str):
                    tag_roots.add(t.split("/")[0])
                    tag_words.update(t.replace("/", "-").split("-"))
            atom_slug_words = set(a["slug"].split("-"))
            in_tag_root = bool(slug_words & tag_roots)
            in_maps = slug in (a["maps"] or [])
            overlap_other = len(slug_words & (tag_words | atom_slug_words))
            # Conditions de candidature :
            # 1. Map déjà référencée dans le frontmatter de l'atom.
            # 2. Atom taggé sous la racine du slug Map (ex: tag famille/* pour Map famille).
            # 3. Overlap ≥ 2 mots du slug avec les tags ou le slug de l'atom (Maps multi-mots).
            if in_maps or in_tag_root or overlap_other >= 2:
                candidate_atoms.append(a["slug"])
        if len(candidate_atoms) >= 3:
            maps_missing.append(
                f"- `{slug}.md` : référencée {occurrences}× dans vault-state, "
                f"{len(candidate_atoms)} atoms candidats détectés "
                f"({', '.join(candidate_atoms[:5])}{'...' if len(candidate_atoms) > 5 else ''})\n"
                f"  → Création auto au triage (lifecycle §4 conditions remplies)"
            )

    # 5. Doublons sémantiques suspects -------------------------------------
    duplicates: list[str] = []
    sorted_atoms = sorted(
        [a for a in atoms if a["created"]],
        key=lambda a: a["created"],
    )
    for i, a in enumerate(sorted_atoms):
        for b in sorted_atoms[i + 1 :]:
            if (b["created"] - a["created"]).days > 7:
                break
            tags_a = set(a["tags"]) if isinstance(a["tags"], list) else set()
            tags_b = set(b["tags"]) if isinstance(b["tags"], list) else set()
            tag_overlap = len(tags_a & tags_b)
            people_overlap = len(set(a["people"]) & set(b["people"]))
            map_overlap = len(set(a["maps"]) & set(b["maps"]))
            signals = sum(
                [tag_overlap >= 2, people_overlap >= 1, map_overlap >= 1]
            )
            if signals >= 2:
                duplicates.append(
                    f"- [[{a['slug']}]] (créé {a['created']}) ↔ "
                    f"[[{b['slug']}]] (créé {b['created']})\n"
                    f"  Signaux : {tag_overlap} tags communs, "
                    f"{people_overlap} people partagés, {map_overlap} map commune\n"
                    f"  → Action triage : à confirmer (validation requise)"
                )
    duplicates = duplicates[:10]

    # Génération de la note inbox ------------------------------------------
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H%M")
    captured = now.strftime("%Y-%m-%d %H:%M:%S")
    counts = {
        "intentions_auto": len(intentions_auto),
        "intentions_manual": len(intentions_manual),
        "maps_incoherent": len(maps_incoherent),
        "people_stale_last_seen": len(people_stale),
        "maps_missing": len(maps_missing),
        "duplicates_suspect": len(duplicates),
    }
    total_notes = (
        len(intentions) + len(sources) + len(logs_events) + len(atoms)
        + len(maps_existing) + len(people)
    )
    slug_summary = (
        f"{counts['intentions_auto']}-int-{counts['maps_incoherent']}-maps-"
        f"{counts['people_stale_last_seen']}-people"
    )
    out_path = INBOX_DIR / f"{timestamp}-lifecycle-audit-{slug_summary}.md"

    sections: list[str] = []
    sections.append(
        f"---\n"
        f"type: inbox\n"
        f"captured: {captured}\n"
        f"device: lifecycle-audit\n"
        f"status: unprocessed\n"
        f"vault_snapshot: {total_notes}\n"
        f"counts:\n"
        + "\n".join(f"  {k}: {v}" for k, v in counts.items())
        + "\n---\n"
    )
    sections.append(
        f"# Audit lifecycle {now.strftime('%Y-%m-%d %H:%M')}\n\n"
        f"> [!info] Cette note n'est pas une capture. C'est un plan d'audit "
        f"produit par `_meta/scripts/lifecycle-lint.py` qui a scanné "
        f"{total_notes} notes du vault. Elle doit être traitée comme "
        f"l'input premier d'un triage low-friction : les sections ci-dessous "
        f"deviennent les actions du brief one-shot.\n"
        f"> Une fois le triage fait, cette note est absorbée (supprimée).\n"
    )
    sections.append(
        "## Pourquoi cette note existe\n\n"
        "Le linter détecte les dérives accumulées avant que la doctrine "
        "[[lifecycle-criteria]] ne soit en place (créée 2026-05-03), ainsi "
        "que les oublis ponctuels d'agents de triage. Il scanne en lecture "
        "seule les 8 types du vault et identifie 5 catégories de "
        "corrections à appliquer. Aucune modification n'est faite par le "
        "script lui-même : la décision et l'application passent par le "
        "triage doctrine ([[triage-criteria]] §0bis et §10)."
    )

    sections.append("## 1. Intentions actives candidates à fermer\n")
    if intentions_auto:
        sections.append(
            "### Auto-confidence (lifecycle §2.1 conditions remplies, fermeture auto au triage)\n\n"
            + "\n\n".join(intentions_auto)
        )
    if intentions_manual:
        sections.append(
            "\n### Manual-confidence (1-2 conditions remplies, validation requise au triage)\n\n"
            + "\n\n".join(intentions_manual)
        )
    if not intentions_auto and not intentions_manual:
        sections.append("Aucune intention candidate détectée.")

    sections.append("\n## 2. Maps avec maturity incohérente\n")
    sections.append("\n".join(maps_incoherent) if maps_incoherent else "Aucune incohérence détectée.")

    sections.append("\n## 3. People avec last_seen obsolète\n")
    sections.append("\n".join(people_stale[:20]) if people_stale else "Aucune People obsolète détectée.")
    if len(people_stale) > 20:
        sections.append(f"\n\n_({len(people_stale) - 20} autres signalés mais tronqués pour lisibilité.)_")

    sections.append("\n## 4. Maps manquantes recommandées par vault-state\n")
    sections.append("\n".join(maps_missing) if maps_missing else "Aucune Map manquante avec conditions auto remplies.")

    sections.append("\n## 5. Doublons sémantiques suspects\n")
    sections.append("\n\n".join(duplicates) if duplicates else "Aucun doublon suspect détecté.")

    sections.append(
        "\n## Comment ce rapport est consommé\n\n"
        "1. Au prochain triage low-friction, l'agent détecte les notes "
        "`device: lifecycle-audit` dans `0-inbox/`.\n"
        "2. Il les place en **tête** du brief one-shot ([[triage-criteria]] §10), "
        "comme contexte structurant.\n"
        "3. Pour chaque section, il intègre les actions dans le brief avec "
        "defaults publiés (auto pour les cas haute confidence, validation "
        "pour confidence moyenne).\n"
        "4. À la fin du triage, cette note inbox est **absorbée** "
        "(supprimée) puisque ses actions ont été appliquées et tracées dans "
        "les frontmatter cibles + `vault-state.md` §9 log."
    )

    sections.append(
        f"\n## Statistiques\n\n"
        f"- {total_notes} notes scannées\n"
        f"- Date : {now.strftime('%Y-%m-%d %H:%M')}\n"
        f"- Doctrine de référence : [[lifecycle-criteria]] §2-§4 et §7, "
        f"[[triage-criteria]] §0bis et §9-§10\n"
    )

    if parse_errors:
        sections.append(
            f"\n## Fichiers avec frontmatter cassé (skippés, à fixer manuellement)\n\n"
            + "\n".join(f"- `{e}`" for e in parse_errors)
        )

    out_path.write_text("\n".join(sections), encoding="utf-8")
    print(f"✅ Rapport déposé dans {out_path.relative_to(VAULT_ROOT)}")
    print(
        f"   counts: intentions_auto={counts['intentions_auto']}, "
        f"intentions_manual={counts['intentions_manual']}, "
        f"maps_incoherent={counts['maps_incoherent']}, "
        f"people_stale={counts['people_stale_last_seen']}, "
        f"maps_missing={counts['maps_missing']}, "
        f"duplicates={counts['duplicates_suspect']}"
    )
    if parse_errors:
        print(f"⚠️  {len(parse_errors)} fichier(s) avec frontmatter cassé, voir rapport.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
