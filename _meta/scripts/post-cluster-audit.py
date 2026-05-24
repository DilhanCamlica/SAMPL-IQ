#!/usr/bin/env python3
"""
post-cluster-audit.py

Audit lecture-seule des fichiers modifiés depuis HEAD~1 (ou un ref donné),
destiné à être lancé avant le commit final d'un cluster de triage ou de
session. Transforme les règles de discipline aval (lifecycle-criteria §2,
triage-criteria §7.2, CLAUDE.md règle wikilink stricte) en checks
factuels binaires.

5 catégories de trous détectés :
  1. Wikilinks rouges (cibles inexistantes dans le vault).
  2. Wikilinks suspects sur outils SaaS tiers génériques (whitelist
     extensible, voir GENERIC_SAAS_TOOLS).
  3. Maps wikilinkées dans frontmatter `maps:` d'atoms / questions /
     intentions nouvellement créés ou modifiés mais absentes du body
     de la Map cible (enrichissement aval Maps body manquant).
  4. People wikilinkées dans frontmatter `people:` ou `participants:`
     d'objets nouvellement créés ou modifiés mais absentes des
     "Sujets partagés" / corps de la People cible (enrichissement
     aval People body manquant).
  5. Sources `medium: conversation` avec `participants:` dont les
     People liées ont `last_seen` < `date_consumed` (last_seen
     non-mis-à-jour, lifecycle §2.3).

Mode strictement read-only sur les fichiers existants. Pas d'auto-fix.
Output stdout, exit 0 si propre, exit 1 si trous détectés (pour
intégration future en hook git si voulu).

Usage :
    cd ~/Documents/<VotreVault>
    python3 _meta/scripts/post-cluster-audit.py
    python3 _meta/scripts/post-cluster-audit.py --ref HEAD~3  # scope élargi

Doctrine de référence :
    - _meta/triage-criteria.md §8.2 (point d'application principal)
    - _meta/lifecycle-criteria.md §2.3 (last_seen People)
    - _meta/triage-criteria.md §7.2 (enrichissement aval body)
    - CLAUDE.md §"Règles comportementales" (règle wikilink stricte)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml


VAULT_ROOT = Path(__file__).resolve().parents[2]
TYPED_DIRS = [
    VAULT_ROOT / "1-atoms",
    VAULT_ROOT / "2-people",
    VAULT_ROOT / "3-sources",
    VAULT_ROOT / "4-projects",
    VAULT_ROOT / "5-maps",
    VAULT_ROOT / "6-logs" / "events",
    VAULT_ROOT / "6-logs" / "journal",
    VAULT_ROOT / "7-intentions",
    VAULT_ROOT / "8-questions",
]
META_DIR = VAULT_ROOT / "_meta"
PEOPLE_DIR = VAULT_ROOT / "2-people"
MAPS_DIR = VAULT_ROOT / "5-maps"
SOURCES_DIR = VAULT_ROOT / "3-sources"

# Wikilinks volontairement rouges (cf. CLAUDE.md + conventions.md).
# Ne génèrent jamais d'alerte rouge même si la cible n'existe pas.
INTENTIONAL_RED_WIKILINKS = {
    "john-doe",  # auto-référentiel, identité civile dans _meta/
    "vie-professionnelle",  # Map parente non créée volontairement
    # Sous-Maps spawnables annoncées dans posture.md (en attente masse critique)
    "posture-patterns",
    "posture-leadership",
    "posture-identite",
}

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")

# Whitelist d'outils SaaS tiers génériques qui doivent rester en texte plat.
# Extensible : ajouter ici les outils qui structurent un deal sans mériter
# une fiche typée propre. Casse-insensible.
GENERIC_SAAS_TOOLS = {
    "planity",
    "manychat",
    "chatfuel",
    "messengerbot",
    "notion",
    "linear",
    "cursor",
    "loveable",
    "stripe",
    "tinder",
    "solvay",
    "intercom",
    "zapier",
    "make",
    "n8n",
    "airtable",
    "figma",
    "miro",
    "gmail",
    "slack",
    "discord",
    "whatsapp",
    "instagram",
    "facebook",
    "twitter",
    "linkedin",
    "youtube",
    "tiktok",
    "google-meet",
    "google-drive",
    "google-agenda",
    "google-calendar",
    "calendly",
    "calcom",
    "openai",
    "anthropic",
    "claude",
    "gpt",
    "chatgpt",
    "hubspot",
    "salesforce",
    "odoo",
    "twilio",
    "vonage",
    "fullcalendar",
    "shadcn",
    "react",
    "vite",
    "next",
    "adonis",
    "postgres",
    "docker",
    "github",
    "gitlab",
    "vercel",
    "supabase",
    "drizzle",
    "tailwind",
    "typescript",
}


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Parse front matter et body. Retourne ({}, body) si pas de FM."""
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


def extract_wikilinks_from_value(value) -> list[str]:
    """Extrait les slugs wikilinkés depuis une valeur YAML (string, liste, etc.)."""
    if value is None:
        return []
    out: list[str] = []
    if isinstance(value, list):
        for item in value:
            out.extend(extract_wikilinks_from_value(item))
        return out
    if isinstance(value, str):
        wikilinks = WIKILINK_RE.findall(value)
        if wikilinks:
            out.extend(wikilinks)
        elif re.fullmatch(r"[a-z0-9][a-z0-9\-]*", value):
            out.append(value)
    return out


def extract_wikilinks_from_text(text: str) -> list[tuple[str, int]]:
    """Extrait (slug, numéro de ligne) depuis du markdown."""
    out: list[tuple[str, int]] = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in WIKILINK_RE.findall(line):
            out.append((m, i))
    return out


def slug_exists_anywhere(slug: str) -> bool:
    """Vérifie si un slug existe dans n'importe quel dossier typé OU dans _meta/."""
    for d in TYPED_DIRS:
        if (d / f"{slug}.md").is_file():
            return True
    # Wikilinks vers fichiers _meta/ sont légitimes (doctrine référencée)
    if (META_DIR / f"{slug}.md").is_file():
        return True
    return False


def find_slug_dir(slug: str) -> Path | None:
    """Retourne le dossier où vit la note avec ce slug, ou None."""
    for d in TYPED_DIRS:
        p = d / f"{slug}.md"
        if p.is_file():
            return p
    return None


def get_modified_files(ref: str) -> list[Path]:
    """Liste les .md modifiés depuis ref via git diff."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=AM", ref],
            capture_output=True,
            text=True,
            cwd=str(VAULT_ROOT),
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"git diff failed: {e.stderr}", file=sys.stderr)
        return []
    files = []
    for line in result.stdout.splitlines():
        # Exclure les fichiers de doctrine (placeholders type [[slug]], [[name]])
        if line.startswith("_meta/") or line == "CLAUDE.md":
            continue
        p = VAULT_ROOT / line.strip()
        if p.suffix == ".md" and p.is_file():
            files.append(p)
    return files


# ---------- Check 1 : wikilinks rouges ----------


def check_red_wikilinks(files: list[Path]) -> list[str]:
    """Liste les wikilinks vers des cibles inexistantes."""
    issues = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        for slug, line in extract_wikilinks_from_text(text):
            if slug in INTENTIONAL_RED_WIKILINKS:
                continue
            if not slug_exists_anywhere(slug):
                rel = f.relative_to(VAULT_ROOT)
                issues.append(f"  {rel}:L{line}  [[{slug}]]  (cible introuvable)")
    return issues


# ---------- Check 2 : wikilinks SaaS génériques ----------


def check_generic_saas_wikilinks(files: list[Path]) -> list[str]:
    """Liste les wikilinks sur outils SaaS génériques (doivent être texte plat)."""
    issues = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        for slug, line in extract_wikilinks_from_text(text):
            if slug.lower() in GENERIC_SAAS_TOOLS:
                rel = f.relative_to(VAULT_ROOT)
                issues.append(
                    f"  {rel}:L{line}  [[{slug}]]  (outil SaaS tiers, doit rester texte plat)"
                )
    return issues


# ---------- Check 3 : Maps wikilinkées mais non enrichies dans body ----------


def check_map_body_enrichment(files: list[Path]) -> list[str]:
    """Pour chaque atom / question / intention / project modifié,
    vérifier que les Maps citées dans `maps:` ont un wikilink retour
    dans leur body."""
    issues = []
    for f in files:
        # Ne s'applique qu'aux objets typés qui ont un champ maps:
        if f.parent.name not in {"1-atoms", "7-intentions", "8-questions", "4-projects"}:
            continue
        fm, _ = parse_frontmatter(f)
        if fm.get("_parse_error"):
            continue
        slug = f.stem
        for map_slug in extract_wikilinks_from_value(fm.get("maps")):
            map_path = MAPS_DIR / f"{map_slug}.md"
            if not map_path.is_file():
                # Map cible inexistante : sera flaggée par check_red_wikilinks
                continue
            map_text = map_path.read_text(encoding="utf-8")
            if f"[[{slug}]]" not in map_text:
                rel = f.relative_to(VAULT_ROOT)
                issues.append(
                    f"  {rel}  →  Map [[{map_slug}]] cite l'objet en frontmatter mais "
                    f"body non enrichi (ajouter [[{slug}]] dans une section appropriée)"
                )
    return issues


# ---------- Check 4 : People wikilinkées mais non enrichies dans body ----------


def check_people_body_enrichment(files: list[Path]) -> list[str]:
    """Pour chaque objet typé modifié, vérifier que les People citées
    dans `people:` ont un wikilink retour dans leur body."""
    issues = []
    for f in files:
        # Ne s'applique qu'aux objets typés qui ont un champ people:
        if f.parent.name not in {
            "1-atoms",
            "7-intentions",
            "8-questions",
            "4-projects",
            "events",
            "journal",
        }:
            continue
        fm, _ = parse_frontmatter(f)
        if fm.get("_parse_error"):
            continue
        slug = f.stem
        for ppl_slug in extract_wikilinks_from_value(fm.get("people")):
            ppl_path = PEOPLE_DIR / f"{ppl_slug}.md"
            if not ppl_path.is_file():
                continue
            ppl_text = ppl_path.read_text(encoding="utf-8")
            if f"[[{slug}]]" not in ppl_text:
                rel = f.relative_to(VAULT_ROOT)
                issues.append(
                    f"  {rel}  →  People [[{ppl_slug}]] citée mais body non enrichi "
                    f"(ajouter [[{slug}]] dans 'Sujets partagés' ou section pertinente)"
                )
    return issues


# ---------- Check 5 : Sources participants vs last_seen People ----------


def check_source_participants_last_seen(files: list[Path]) -> list[str]:
    """Pour chaque Source `medium: conversation` modifiée, vérifier que
    chaque participant a `last_seen >= date_consumed`."""
    issues = []
    for f in files:
        if f.parent.name != "3-sources":
            continue
        fm, _ = parse_frontmatter(f)
        if fm.get("_parse_error"):
            continue
        if fm.get("medium") != "conversation":
            continue
        date_consumed = fm.get("date_consumed")
        if date_consumed is None:
            continue
        date_consumed_str = str(date_consumed)
        for ppl_slug in extract_wikilinks_from_value(fm.get("participants")):
            ppl_path = PEOPLE_DIR / f"{ppl_slug}.md"
            if not ppl_path.is_file():
                continue
            ppl_fm, _ = parse_frontmatter(ppl_path)
            last_seen = ppl_fm.get("last_seen")
            if last_seen is None:
                rel = f.relative_to(VAULT_ROOT)
                issues.append(
                    f"  {f.stem}  →  [[{ppl_slug}]] last_seen=null, "
                    f"date_consumed={date_consumed_str} (à renseigner)"
                )
                continue
            if str(last_seen) < date_consumed_str:
                rel = f.relative_to(VAULT_ROOT)
                issues.append(
                    f"  {f.stem}  →  [[{ppl_slug}]] last_seen={last_seen} < "
                    f"date_consumed={date_consumed_str} (à mettre à jour)"
                )
    return issues


# ---------- Main ----------


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ref",
        default="HEAD~1",
        help="Git ref de référence pour diff (défaut: HEAD~1)",
    )
    args = parser.parse_args()

    files = get_modified_files(args.ref)
    if not files:
        print(f"Aucun fichier .md modifié depuis {args.ref}.")
        sys.exit(0)

    print(f"📋 post-cluster-audit : {len(files)} fichier(s) modifié(s) depuis {args.ref}")
    print()

    sections = [
        ("1. Wikilinks rouges (cibles inexistantes)", check_red_wikilinks(files)),
        (
            "2. Wikilinks SaaS génériques (doivent être texte plat)",
            check_generic_saas_wikilinks(files),
        ),
        (
            "3. Maps wikilinkées non enrichies dans body (lifecycle §7.2)",
            check_map_body_enrichment(files),
        ),
        (
            "4. People wikilinkées non enrichies dans body (lifecycle §7.2)",
            check_people_body_enrichment(files),
        ),
        (
            "5. Sources participants vs last_seen People (lifecycle §2.3)",
            check_source_participants_last_seen(files),
        ),
    ]

    total_issues = sum(len(issues) for _, issues in sections)

    for title, issues in sections:
        if issues:
            print(f"⚠ {title}")
            for issue in issues:
                print(issue)
            print()

    if total_issues == 0:
        print("✅ Aucun trou détecté. Cluster propre, commit OK.")
        sys.exit(0)
    else:
        print(f"❌ {total_issues} trou(s) détecté(s). Corriger avant commit.")
        sys.exit(1)


if __name__ == "__main__":
    main()
