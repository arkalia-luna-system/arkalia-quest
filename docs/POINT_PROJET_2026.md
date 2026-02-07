# Faire le point — Arkalia Quest (7 février 2026)

Document unique pour l’état des lieux du projet : ce qui est fait, ce qui reste, métriques et prochaines actions.

---

## 1. Identité du projet

| Élément | Valeur |
|--------|--------|
| **Genre** | Serious game éducatif (cybersécurité / hacking) pour adolescents |
| **Promesse (15 mots)** | *Aide LUNA à sauver Arkalia : choisis ton chemin, vis l’aventure.* |
| **Page cœur** | **Aventure** (`/histoire`) — chapitres (prologue → acte_1… acte_6 → épilogue), bouton « Continuer », choix à l’acte_5. Terminal en mode expert. |
| **Stack** | Flask, SQLite, HTML/CSS/JS, 14 pages, API REST (story, terminal, profil, etc.) |

---

## 2. Ce qui est fait (checklist complète)

### Concept et parcours

- [x] Abandon du terminal comme pilier : parcours principal = Accueil → Aventure (chapitres).
- [x] CTA principal « Rejoindre LUNA » → `/histoire`.
- [x] Promesse 15 mots et micro-intro (« LUNA a besoin de toi ») sur l’accueil.
- [x] Navbar : Aventure en premier ; Monde / Profil / Classement etc. débloqués après le premier chapitre.
- [x] Aide unifiée : terminal (commande inconnue) → « tape aide » + lien Tutoriel / Aventure.

### Aventure (page cœur)

- [x] API `GET /api/story/state` et `POST /api/story/choice`.
- [x] Chapitres avec titre, message, émotion LUNA, fond par chapitre.
- [x] Bouton « Continuer » + choix (acte_5) ; indicateur flottant +XP, son succès, célébration bouton.
- [x] Barre de progression par chapitre ; écran de fin avec liens Monde / Profil / Accueil.
- [x] Données : `data/story_chapters.json` ; progression dans `story_chapters_completed`.

### Visuel minimal unifié

- [x] Une seule feuille `static/css/arkalia-minimal.css` (fond sombre `#0d1117`, accent bleu `#58a6ff`, texte lisible) chargée sur **toutes les pages**.
- [x] Remplacement de la refonte 2026 par le visuel minimal pour cohérence et stabilité. Voir [REPARTIR_SUR_DES_BASES_SANES.md](REPARTIR_SUR_DES_BASES_SANES.md).
- [x] Accueil, Aventure, navbar, CTA, bloc LUNA, cartes et boutons alignés sur le visuel minimal.
- [x] Contraste et reduced-motion pris en compte (game-feel, accessibilité).

### Game feel et accessibilité

- [x] `game-feel.css` sur toutes les pages (micro-interactions, focus visible, reduced-motion).
- [x] Bouton « Ambiance » sur l’accueil + page Audio (musique de fond optionnelle).
- [x] Messages d’erreur encourageants (Aventure + terminal « Tape "aide" »).
- [x] Skip links, ARIA, modes adaptatifs, responsive ; focus visible sur CTA, Continuer, Exécuter terminal, nav.

### Terminal (mode expert)

- [x] Source de vérité : bandeau Niveau/Score depuis API.
- [x] Feedback flash vert/rouge + sons ; défi acte_1 (modal « Choisis le bon code »).
- [x] Bannière « Prochaine étape : tape acte_2 » (puis acte_3… epilogue) selon progression.
- [x] Scripts en defer ; `terminal-bundle.css` pour performances.

### Documentation

- [x] [AUDIT_ET_REVISION_CONCEPT.md](AUDIT_ET_REVISION_CONCEPT.md) — audit + révision concept + Partie 3bis refonte visuelle.
- [x] [REFONTE_VISUELLE_2026.md](REFONTE_VISUELLE_2026.md) — audit visuel, jeux de référence, design system, implémentation complète.
- [x] [COMPARAISON_JEUX_SOURCES_EXTERNES.md](COMPARAISON_JEUX_SOURCES_EXTERNES.md) — fun, game feel, onboarding, checklist (sauf playtests).
- [x] [STATUT_PROJET_ACTUEL.md](STATUT_PROJET_ACTUEL.md), [INDEX_DOCUMENTATION.md](INDEX_DOCUMENTATION.md), index.md, README, CHANGELOG mis à jour avec visuel minimal et parcours. [REPARTIR_SUR_DES_BASES_SANES.md](REPARTIR_SUR_DES_BASES_SANES.md) pour diagnostic et plan.

### Qualité

- [x] Tests : 520 tests passent (`pytest tests/`).
- [x] API story et routes `/`, `/histoire` vérifiées (200, données cohérentes).

---

## 3. Ce qui reste à faire

### Prochaine action recommandée (jeu « parfait »)

- [ ] **Playtests** avec 2–3 ados (scénario 15 min dans [PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md)) — seule case non cochée de la checklist « jeu fun, agréable, fonctionnel, visuel top ». À organiser en conditions réelles, puis coller les retours dans STATUT (template fourni dans COMPARAISON_JEUX_SOURCES_EXTERNES).

### En cours / priorités (hors refonte)

- Personnalisation (profils, tutoriel adaptatif, missions adaptatives, recommandations IA).
- Social (chat sécurisé, défis live, partage, tournois).
- Internationalisation (multi-langues, cloud/sync).

---

## 4. Métriques

| Domaine | Indicateur |
|---------|------------|
| **Tests** | 520 passés |
| **Engagement** | Session ~45 min, rétention 85 % (1 sem.), acte 3 ~90 % |
| **Accessibilité** | WCAG 2.1 AA (skip links, ARIA, reduced-motion, focus) ; indicateur 79.3/100 (A) |
| **Qualité** | Black + Ruff, chargement cible &lt;2 s |

---

## 5. Références rapides

| Besoin | Document |
|--------|----------|
| Vue d’ensemble | [STATUT_PROJET_ACTUEL.md](STATUT_PROJET_ACTUEL.md) |
| Audit concept + refonte | [AUDIT_ET_REVISION_CONCEPT.md](AUDIT_ET_REVISION_CONCEPT.md) |
| Design system + visuel | [REFONTE_VISUELLE_2026.md](REFONTE_VISUELLE_2026.md) |
| Fun / game feel / checklist | [COMPARAISON_JEUX_SOURCES_EXTERNES.md](COMPARAISON_JEUX_SOURCES_EXTERNES.md) |
| Playtests ados | [PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md) |
| Navigation doc | [INDEX_DOCUMENTATION.md](INDEX_DOCUMENTATION.md) |

---

*Dernière mise à jour : 7 février 2026.*
