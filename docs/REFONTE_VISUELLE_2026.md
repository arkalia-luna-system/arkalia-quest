# Refonte visuelle Arkalia Quest — 2026

**Date :** 7 février 2026  
**Statut :** Référence conservée ; en production le projet utilise désormais le **visuel minimal** (`arkalia-minimal.css`) sur toutes les pages. Voir [REPARTIR_SUR_DES_BASES_SANES.md](REPARTIR_SUR_DES_BASES_SANES.md).

**Objectif (historique) :** Auditer le jeu (but, histoire, visuel), s’inspirer des meilleurs jeux similaires et **changer complètement le visuel** pour une identité forte et cohérente.

---

## 1. Audit du jeu

### 1.1 But et promesse

| Élément | Description |
|--------|--------------|
| **Genre** | Serious game éducatif (cybersécurité / hacking) pour ados |
| **Promesse (15 mots)** | *« Aide LUNA à sauver Arkalia : choisis ton chemin, vis l’aventure. »* |
| **Cœur du gameplay** | **Aventure narrative** : page /histoire avec chapitres (prologue → acte_1… acte_6 → épilogue), bouton « Continuer » et choix (acte_5). Terminal en mode expert. |
| **Histoire** | LUNA (IA émotionnelle) et le joueur (hacker) doivent sauver Arkalia : SOS d’Althea, NEXUS, PANDORA, fusion LUNA/NEXUS → ARKALIA. Thèmes : confiance, choix, cybersécurité. |

### 1.2 Problèmes du visuel actuel (corrigés)

- **Palette générique** : fond #0f0f12, violet #a78bfa, **vert matrix #00ff00 (supprimé)** → remplacé par ambre + cyan uniquement.
- **Peu d’identité** : mélange violet Luna + vert matrix → **palette unifiée ambre/corail + cyan, aucun vert**.
- **Typographie** : Inter + Cormorant + IBM Plex Mono → lisible mais sans personnalité forte.
- **Ressenti** : « outil » ou « dashboard » plutôt qu’« aventure narrative ».
- **Incohérence** : beaucoup de fichiers CSS (40+), variables éparpillées (--violet-lunaire, --matrix-green, --luna-*).

---

## 2. Jeux similaires et inspiration

### 2.1 Références retenues

| Jeu | Type | Ce qu’on en garde |
|-----|------|--------------------|
| **Solace State** | Visual novel cyberpunk émotionnel | Narratif centré personnage, thèmes pouvoir/communauté, ambiance cyberpunk mais chaleureuse. |
| **Read Only Memories: Neurodiver** | Visual novel / aventure pixel-art | Couleurs vives, personnage « Luna », identité visuelle forte, noir + couleurs expressives. |
| **Metaphor: ReFantazio** | JRPG (TGA 2024 Best Art Direction) | UI « hyper stylish », chaque écran distinct et lisible, UI qui connecte au monde. |
| **Hades (Supergiant)** | Action-RPG narratif | Intégrité artistique, encre/trait, UI non intrusive, feedback clair. |
| **Beastieball** | Sport / aventure | Langage visuel cohérent, UI = représentation claire des systèmes. |
| **The Gnorp Apologue** | Minimal | Design minimal à fort impact, pas de surcharge. |

### 2.2 Principes tirés de ces jeux

1. **Un langage visuel cohérent** : une palette principale + un accent, appliquée partout.
2. **Clarté > complexité** : lisibilité, hiérarchie claire, pas de surcharge.
3. **Émotion et chaleur** : le jeu raconte une histoire avec LUNA — le visuel doit soutenir l’émotion, pas seulement « cyber froid ».
4. **Identité mémorable** : éviter violet+vert matrix ; choisir une combinaison distinctive.
5. **UI au service du récit** : boutons et écrans qui font « partie du monde » (Metaphor).

---

## 3. Nouvelle direction visuelle

### 3.1 Choix artistique : « Arkalia — Nuit émotionnelle »

- **Ambiance** : Nuit profonde (monde en danger) mais **chaleur** (LUNA, espoir, lien). Pas « terminal froid ».
- **Fond** : Bleu nuit profond (#0a0e17) avec très légers dégradés (indigo/violet très sombre), pas de néon agressif.
- **Couleur principale (LUNA / héros)** : **Ambre / corail** (#e07c54, #f59e7c) — chaleur, vie, personnage.
- **Couleur secondaire (actions, succès)** : **Cyan doux** (#67d4e0) uniquement — clic, validation, progression. **Aucun vert.**
- **Texte** : Blanc cassé (#f4f4f5) pour le principal, gris doux (#94a3b8) pour secondaire.
- **Typographie** :  
  - **Titres** : une police avec caractère (ex. **Outfit** ou **Sora**) — moderne, lisible, pas « serif classique ».  
  - **Corps** : Inter ou équivalent système pour lisibilité et accessibilité.
- **Composants** : Cartes avec bordure fine (1px) et léger glow au hover ; boutons avec fond semi-transparent et bordure accent ; pas de gradients lourds partout.

### 3.2 Variables CSS (design system)

```css
/* Design system Arkalia 2026 */
--arkalia-bg: #0a0e17;
--arkalia-surface: #111827;
--arkalia-card: #1a2234;
--arkalia-hero: #e07c54;        /* ambre / LUNA */
--arkalia-hero-light: #f59e7c;
--arkalia-accent: #67d4e0;     /* cyan actions */
--arkalia-success: var(--arkalia-accent);  /* plus de vert */
--arkalia-text: #f4f4f5;
--arkalia-text-muted: #94a3b8;
--arkalia-border: rgba(224, 124, 84, 0.25);
--arkalia-glow: rgba(224, 124, 84, 0.4);
```

### 3.3 Ce qu’on change concrètement

| Zone | Avant | Après |
|------|--------|--------|
| Fond global | #0f0f12, violet | #0a0e17, dégradé léger indigo |
| Titres / LUNA | Violet #a78bfa | Ambre #e07c54 |
| CTA / boutons principaux | Vert matrix | Bordure + fond ambre/cyan, texte clair |
| Cartes / blocs | Bordure violet | Bordure --arkalia-border, hover glow ambre |
| Barre de progression | Vert matrix | --arkalia-success ou --arkalia-accent |
| Navbar | Style Luna violet | Fond surface, liens ambre au hover/active |
| Page Histoire | Fonds par chapitre (déjà en place) | Conserver logique, adapter couleurs aux nouvelles variables |

---

## 4. Plan d’implémentation

1. **Design system** : Fichier `static/css/arkalia-visual-2026.css` avec variables et overrides des anciennes variables Luna/Matrix.
2. **Accueil** : Appliquer nouveau fond, titre, sous-titre, CTA (ambre/cyan), cartes avec nouvelles bordures.
3. **Page Aventure (/histoire)** : Bloc LUNA, barre de progression, titre, message, bouton Continuer et choix avec nouveau style.
4. **Navbar** : Couleurs et hover selon design system.
5. **Pages secondaires** : Monde, Profil, etc. — charger le même design system pour cohérence.
6. **Tests** : Vérifier navigation, API story, accessibilité (contraste, focus), reduced-motion.

---

## 5. Checklist post-refonte

- [x] Accueil : nouveau fond et palette, CTA lisible et contrasté.
- [x] /histoire : chapitres s’affichent, Continuer et choix fonctionnent, +XP et son OK.
- [x] Navbar : tous les liens cliquables, page active visible (couleurs refonte).
- [x] Contraste WCAG AA : ambre #e07c54 et cyan #67d4e0 sur fond #0a0e17 vérifiables.
- [x] Reduced-motion respecté (animations désactivées dans le CSS refonte).
- [x] Aucune régression : API story testée, routes / et /histoire OK ; refonte appliquée à index, histoire, monde, profil, dashboard, leaderboard, tutoriel, skill-tree, terminal.

---

## 6. Références doc

- [AUDIT_ET_REVISION_CONCEPT.md](AUDIT_ET_REVISION_CONCEPT.md) — Audit concept et passage à l’aventure sans terminal.
- [COMPARAISON_JEUX_SOURCES_EXTERNES.md](COMPARAISON_JEUX_SOURCES_EXTERNES.md) — Fun, game feel, 30 s, checklist.
- [STATUT_PROJET_ACTUEL.md](STATUT_PROJET_ACTUEL.md) — Vue d’ensemble projet.

---

## 7. Implémentation complète (réalisée)

- **Fichier design system** : `static/css/arkalia-visual-2026.css` (variables `--arkalia-*`, override des anciennes variables, styles hero/CTA/navbar/story/cartes, fonds par chapitre, reduced-motion).
- **Pages avec refonte** (lien CSS chargé en dernier) : Accueil (`index.html`), Aventure (`histoire.html`), Monde, Profil, Dashboard, Leaderboard, Tutoriel welcome, Arbre de compétences, Terminal, Tutoriels techniques, Accessibilité, Audio, Mail, Explorateur — soit **14 templates**.
- **Docs mis à jour** : AUDIT_ET_REVISION_CONCEPT (Partie 3bis), COMPARAISON_JEUX_SOURCES_EXTERNES (section Refonte 2026), STATUT_PROJET_ACTUEL, INDEX_DOCUMENTATION, index.md, README (table Documentation).
- **Vérifications** : GET/POST API story OK, routes / et /histoire 200, tests critiques passés.
