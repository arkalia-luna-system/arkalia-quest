# Audit visuel et performances – Arkalia Quest

**Date :** 7 février 2026  
**Objectif :** Identifier pourquoi le visuel et les perfs semblent "nuls" et corriger sans casser l’existant.

---

## 1. Synthèse

| Problème | Impact | Priorité |
|----------|--------|----------|
| Trop de fichiers CSS/JS sur l’index | LCP, FCP, temps de chargement | Haute |
| Scripts bloquants dans le `<head>` | First Contentful Paint retardé | Haute |
| Règle CSS `* { transition }` globale | Repaints inutiles, jank | Haute |
| ~365 Ko de CSS au total, 25+ feuilles sur l’index | Parsing, cascade, latence réseau | Moyenne |
| Animations et keyframes dispersés (20+ fichiers) | Main thread, batterie mobile | Moyenne |
| accessibilité.css 31 Ko + bordure `*` en mode contraste | Reflow massif en mode accessibilité | Moyenne |

---

## 2. Audit visuel

### 2.1 Structure des styles

- **43 fichiers CSS** dans `static/css/` (~365 Ko au total).
- **Index seul :** plus de **25 feuilles** chargées (blocking + preload) + ~300 lignes de styles inline.
- **Conséquences :** cascade lourde, risques de conflits, premier rendu qui attend beaucoup de CSS.

**Fichiers les plus lourds :**
- `accessibility.css` ~31 Ko
- `interface-improvements.css` ~37 Ko  
- `arkalia-luna-vision.css` ~20 Ko  
- `empty-states.css` ~14 Ko  
- `arkalia-responsive.css` ~14 Ko  

### 2.2 Cohérence visuelle

- Variables définies à plusieurs endroits : `arkalia-core.css`, `accessibility.css`, thèmes.
- Risque de couleurs / espacements incohérents si une feuille charge en retard ou est désactivée.
- **Recommandation :** une seule source de variables (ex. `arkalia-core.css`) et les autres en héritent.

### 2.3 Animations

- **Keyframes** dans au moins 20 fichiers (progression, reward, loading, casual-system, etc.).
- Beaucoup d’éléments avec `animation` sans `prefers-reduced-motion` dans certains fichiers.
- `will-change` et `transform: translateZ(0)` déjà utilisés dans `performance-optimized.css` (bon), mais `performance-optimized.css` applique aussi une transition globale à `*` (mauvais pour les perfs).

### 2.4 Accessibilité visuelle

- `accessibility.css` en mode `high-contrast` applique `* { border: 2px solid ... !important }` → très coûteux en reflow.
- **Recommandation :** cibler les éléments interactifs et les blocs principaux au lieu de `*`.

---

## 3. Audit performances

### 3.1 Chargement de l’index

- **Dans le `<head>` :** 4 scripts **sans** `defer`/`async` :  
  `universal-notifications.js`, `universal-empty-states.js`, `smart-empty-states.js`, `reward-feedback-system.js`, `ui-perfection.js`  
  → Ils bloquent le parsing et retardent le First Contentful Paint.
- **Recommandation :** déplacer tous les scripts non critiques en fin de `<body>` ou les charger en `defer`.

### 3.2 CSS

- Beaucoup de `link` (blocking) puis beaucoup de `preload as="style"` avec `onload` → bon pour le différé, mais trop de fichiers.
- `performance-optimized.css` contient :
  - `* { transition-duration: 0.2s; transition-timing-function: ease-out; }`  
  → Applique des transitions à tous les éléments, ce qui peut provoquer des repaints et du jank.
- **Recommandation :** supprimer la règle globale `*` et limiter les transitions à des classes dédiées (ex. `.perf-transition` ou composants ciblés).

### 3.3 JS

- Sur l’index, une vingtaine de scripts au total (critiques + différés + après `DOMContentLoaded`).
- Doublons possibles : `performance-ux-optimizer.js` et `audio-manager.js` chargés dans le head puis relancés dans `portalScripts` après `load`.
- **Recommandation :** un seul chargement par script ; privilégier `defer` pour tout ce qui n’est pas strictement critique au premier rendu.

---

## 4. Actions réalisées (ce correctif)

1. **performance-optimized.css**  
   - Suppression de la règle `* { transition-duration; transition-timing-function }`.  
   - Ajout de la classe `.perf-transition` et ciblage des composants (`.btn`, `.cta-btn`, `.nav-link`, `.feature-card`, `.card`) pour des transitions courtes sans impacter tout le DOM.

2. **index.html**  
   - Déplacement des 5 scripts du `<head>` (universal-notifications, universal-empty-states, smart-empty-states, reward-feedback-system, ui-perfection) en **fin de `<body>`** avec `defer`, pour ne plus bloquer le First Contentful Paint.  
   - Suppression du double chargement de `performance-ux-optimizer.js` et `audio-manager.js` (présents une seule fois en « Scripts critiques »).  
   - Ajout de `content-visibility: auto` et `contain-intrinsic-size` sur `.features-grid` pour améliorer le rendu (section sous la fold).

3. **accessibility.css**  
   - Mode haute visibilité : remplacement de `* { border: 2px solid ... }` par des sélecteurs ciblés (main, nav, section, .card, .cta-btn, a, button, input, etc.) pour limiter le reflow tout en gardant l’effet visuel.

4. **Documentation**  
   - Ce fichier `AUDIT_VISUEL_ET_PERFORMANCES.md` sert de référence pour les prochaines optimisations (bundling CSS/JS, réduction du nombre de feuilles, etc.).

### Correctif 4.0.2 (suite)

5. **accessibility.css – mode `high-contrast-enhanced`**  
   - Remplacement de `body.high-contrast-enhanced * { color; background-color; border-color }` par des **sélecteurs ciblés** (main, nav, section, .card, .cta-btn, .terminal-container, a, button, input, h1–h4, p, span, li, td, th, etc.) pour limiter le reflow en mode contraste renforcé.

6. **Terminal – bundle CSS**  
   - Script `scripts/build_terminal_css.py` : concatène les 16 feuilles CSS du terminal en un seul fichier `static/css/terminal-bundle.css`.  
   - `templates/terminal.html` charge désormais **1 feuille** au lieu de 16 (moins de requêtes, parsing plus simple).  
   - Après modification d’une CSS source du terminal, relancer : `python scripts/build_terminal_css.py`.

### Correctif suite « continuer »

7. **Index – scripts en defer**  
   - Tous les scripts de l’accueil (accessibility, performance-ux-optimizer, audio-manager, personalized-messages, mini-games-interactive, audit-visual-enhancements, zone-exploration-enhanced, popup-manager, progression-sync, etc.) passés en **defer** pour ne plus bloquer le parsing HTML → FCP (First Contentful Paint) plus rapide.

8. **Terminal – preconnect polices**  
   - Ajout de `preconnect` vers `fonts.googleapis.com` et `fonts.gstatic.com` pour accélérer le chargement de la police Share Tech Mono.

---

## 5. Suite des actions (correctifs « continuer »)

- **Index** : Critical CSS inline (variables, body, .portal-container) ; CSS gameplay en `preload` + `onload` ; fallback `<noscript>` pour popup-manager.
- **Terminal** : Critical CSS inline (body, .terminal-workspace) ; page déjà servie avec `terminal-bundle.css` (1 requête).
- **Monde** : Critical CSS inline (body, .world-workspace).
- **Profil** : Critical CSS inline (body, .profile-workspace) ; tous les scripts externes passés en `defer` pour chargement non bloquant.

## 6. Pistes restantes

- **Bundle CSS** : un ou deux fichiers par page (critical + non-critical) au lieu de 25+.
- **Bundle JS** : un `portal.js` pour l’accueil au lieu d’une vingtaine de scripts.
- **Critical CSS** : extraire le strict minimum pour le viewport (nav + hero) et l’inliner dans le `<head>`.
- **Mode accessibilité** : remplacer `* { border }` par des sélecteurs ciblés (`.main-nav a`, `.cta-btn`, `.feature-card`, etc.).
- **Lazy-load des feuilles** : charger certaines CSS seulement quand une section est visible (Intersection Observer) ou quand on navigue vers une page (ex. zone-exploration, popup-manager).
- **Images / polices** : vérifier `loading="lazy"`, `font-display: swap`, et tailles d’icônes.

---

## 7. Métriques à surveiller

- **LCP** (Largest Contentful Paint) sur la page d’accueil.
- **FCP** (First Contentful Paint) avant / après déplacement des scripts.
- **CLS** (Cumulative Layout Shift) : éviter les décalages quand les CSS différées se chargent.
- **Nombre de requêtes** et **poids total** (CSS + JS) sur l’index.

Une fois ces correctifs déployés, repasser un test Lighthouse (ou équivalent) sur `/` pour comparer.
