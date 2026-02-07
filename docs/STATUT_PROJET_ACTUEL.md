# Statut du projet — Arkalia Quest

Jeu narratif éducatif (hacking) pour adolescents, inclusif et accessible.

**Promesse (15 mots) :** Tu es un hacker qui aide LUNA : missions au terminal, actes et mini-jeux.

*Dernière mise à jour : 7 février 2026.*

---

## Vue d’ensemble

**Fonctionnalités principales (v3.3 / v4.0)**

- **Narratif** : 6 actes + prologue + épilogue
- **LUNA** : IA émotionnelle, 10 émotions dynamiques
- **Terminal** : commandes, progression (points, badges, niveaux), profils persistants
- **Mini-jeux** : 9 jeux (logique, code, cybersécurité, cryptographie, réseaux), interface immersive
- **Guidage** : visual guidance, célébrations tutoriel, états vides, récompenses, API REST
- **Analytics** : tracking, anonymisation, recommandations, métriques, terminal
- **Accessibilité** : WCAG 2.1 AA (skip links, ARIA, modes adaptatifs, responsive)
- **Qualité** : 179–225 tests, Black + Ruff, performance et intégration

**Améliorations récentes**

- LUNA AI V3, défis quotidiens, thèmes (Matrix, Cyberpunk, Neon, Dark, Retro, Ocean)
- Performance (réduction appels API), nettoyage code, UI/UX modernisées
- API Terminal v4.0, popups closables, smart empty states, reward feedback, monde interactif
- **Audit UX 2026** : promesse 15 mots et micro-intro sur l’accueil, CTA principal, accueil plus léger (4 scripts). Terminal : source de vérité (progression depuis API), feedback succès/échec + sons, bannière première mission, défi acte_1 (modal « Choisis le bon code », code correct aléatoire A/B/C). Navbar simplifiée (Accueil, Terminal, Tutoriel) jusqu’à acte_1 complété. Parcours recommandé : **Accueil → Terminal → acte_1**. Guide playtest : [PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md).
- **Fun & visuel** : Comparaison avec sources externes dans [COMPARAISON_JEUX_SOURCES_EXTERNES.md](COMPARAISON_JEUX_SOURCES_EXTERNES.md). Accroche 30 s ; game-feel (micro-interactions, +XP/✓, reduced-motion, focus visible) ; bouton Ambiance sur l’accueil ; messages d’erreur terminal amicaux ; célébration modal acte_1 ; bannière « Prochaine étape : tape acte_2 » (puis acte_3… epilogue) après chaque mission.
- **Couverture visuelle et accessibilité** : Les 13 pages (accueil, terminal, monde, profil, dashboard, leaderboard, tutoriel, arbre de compétences, explorateur, mail, audio, accessibilité, tutoriels techniques) chargent `game-feel.css`, ont un focus visible (boutons, liens, zones, input terminal, modal acte_1) et respectent `prefers-reduced-motion` (animations désactivées à la demande). Voir le tableau « Couverture des pages » dans [COMPARAISON_JEUX_SOURCES_EXTERNES.md](COMPARAISON_JEUX_SOURCES_EXTERNES.md). Focus burger (menu mobile) dans game-feel.css.
- **Prêt pour playtests** : [PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md) avec scénario 15 min et checklist de vérification avant session.
- **Audit "pourquoi le jeu semble nul"** : [audits/AUDIT_COMPLET_POURQUOI_LE_JEU_SEMBLE_NUL.md](audits/AUDIT_COMPLET_POURQUOI_LE_JEU_SEMBLE_NUL.md) — parcours, contenu, technique. P0 fait (accueil « LUNA a besoin de toi », aide acte_1 en premier). P1 fait : CTA renforcé (« 👉 Clique ici pour lancer ta première mission »), états vides encourageants (leaderboard + profil). P2 à traiter si besoin (allègement terminal, unifier flux).

---

## En cours

- Personnalisation (profils, tutoriel adaptatif, missions adaptatives, recommandations IA)
- Social (chat sécurisé, défis live, partage, tournois)
- Internationalisation (multi-langues, cloud/sync)

---

## Métriques

| Domaine      | Indicateur                    |
|-------------|-------------------------------|
| Engagement  | Session ~45 min, rétention 85 % (1 sem.), acte 3 ~90 % |
| Accessibilité | WCAG 79.3/100 (A), clavier, lecteurs d’écran |
| Qualité     | Tests 100 % pass, chargement <2 s, Black + Ruff |

---

## Priorités

1. Personnalisation avancée (profils, tutoriel et missions adaptatifs)
2. Social & communautaire (chat, défis live, tournois)
3. Internationalisation et cloud

---

## Références

- Documentation : `docs/`, [INDEX_DOCUMENTATION.md](INDEX_DOCUMENTATION.md)
- Déploiement : [GUIDE_DEPLOIEMENT.md](GUIDE_DEPLOIEMENT.md)
- Audit consolidé : [rapports/RAPPORT_AUDIT_PROJET.md](rapports/RAPPORT_AUDIT_PROJET.md)
- Audit UX / bonnes pratiques 2026 : [audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md](audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md)
