# Roadmap — LUNA Hors Connexion

Mise a jour: **27 avril 2026**

## Etat actuel

- Boucle narrative principale jouable (chapitres + fins).
- Sauvegarde locale stable (SQLite + cookie).
- Profil et leaderboard fonctionnels.
- Base UX solide (typewriter, reactions, transitions).

## Priorites court terme (P1)

- Renforcer la coherence narrative de chaque chapitre.
- Ajouter des tests API supplementaires sur les cas d'erreur.
- Stabiliser le wording UI (accueil, fin, profil) pour ton adolescent.
- Reduire le code historique non utilise dans la configuration.
- Rationaliser les tags Git (garder uniquement des tags de release significatifs).
- Ajouter les assets visuels de demo dans `docs/assets/` et les lier depuis `README.md`.

## Priorites moyen terme (P2)

- Playtests encadres (ados cible) avec feedback structure.
- Telemetrie locale minimale (sans tracking intrusif) pour UX tuning.
- Plus de variation conditionnelle dans les dialogues de LUNA.
- Equilibrage XP/confiance pour mieux differencier les runs.

## Priorites long terme (P3)

- Mode saison narrative (nouveaux arcs).
- Outils auteur pour editer `story.json` sans casser les references.
- Packaging distribution simplifiee (Docker) avec checks automatises.

## Hors scope actuel

- Multijoueur
- App mobile native
- Microservices
- Internationalisation complete
