---
type: log
subtype: journal-daily
date: YYYY-MM-DD
date_veille: YYYY-MM-DD
type_jour: work
type_jour_veille: work
localisation: 

# Veille (J-1, journée terminée, dictée rétrospective ce matin)
sport: false
sport_type: []
alcool_verres: 0
sucre_ajoute: false
cafe_tasses: 0
drogues: null
nicotine: false
fierte_veille: 
decision_impactante: false
friction_client: false
friction_equipe: false
sentiment_social: 

# Nuit (J-1 → J, qui vient de s'écouler)
sommeil_h: 
sommeil_qualite: 

# Matin (J, état au moment de la dictée)
energie_matin: 
humeur: 
stress: 
focus: 

# Schema log canonique conservé
people: []
projects: []
mood: 

# Traçabilité
derived_from_inbox: 

tags: [meta/journal-daily]
---

<!-- Sémantique temporelle : le journaling matinal documente trois temporalités. -->
<!--   Veille (J-1) : datas finalisées de la journée écoulée (substances, sport, fierté, frictions pro, social, decision). -->
<!--   Nuit (J-1 → J) : durée et qualité du sommeil qui vient de s'écouler. -->
<!--   Matin (J) : état émotionnel au moment de la dictée (énergie, humeur, stress, focus). -->
<!-- date = jour de la dictée (matin J). date_veille = J-1 (auto = date - 1 jour). -->
<!-- type_jour : work | weekend | voyage | off | férié -->
<!-- localisation : Floripa | Lisbonne | <texte libre> -->
<!-- Échelles 1-6 (paire, pas de milieu neutre). Laisser vide / null si non mesuré. -->
<!-- sport_type : [box, kite, moto, trail, surf, gym, course, autre] -->
<!-- drogues : null | MD | LSD | champis | cannabis | autre (ou liste comma-separated en string) -->
<!-- sentiment_social : seul | entoure | mixte -->
<!-- mood : texte libre, distinct des scores numériques (ex. "lucidité, légèreté") -->
<!-- derived_from_inbox : slug de la note inbox source (sans .md) si dictée arrivée d'abord en inbox, sinon vide -->
<!-- nommage du fichier : YYYY-MM-DD.md dans 6-logs/journal/ (date de la dictée) -->

# YYYY-MM-DD

## Contexte du matin

État au réveil, ce que j'attendais de la journée qui démarre, état d'esprit. (J)

## Déroulé de la veille

Ce qui s'est passé la veille, moments marquants, décisions, frictions, wins. (J-1)

## Ressenti

Évolution émotionnelle sur la veille, ce qui a pesé, ce qui a porté, état au moment de la dictée. (mix J-1 et J)

## Notes libres

Idées, réflexions, choses à creuser, observations sur moi-même.

## Atoms à extraire

- [ ] [[slug-derivee-candidate]]

## Liens

- People : [[prenom-nom]]
- Projets : [[projet-en-cours]]
- Maps : [[map-domaine]]
