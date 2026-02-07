# Repartir sur des bases saines

**Date :** 7 février 2026  
**Constat :** Le visuel est jugé affreux et rien ne fonctionne comme prévu. Ce doc décrit le diagnostic et le plan pour stabiliser le jeu.

---

## 1. Ce qui pose problème (diagnostic)

### 1.1 Visuel

- **Trop de couches CSS** : 40+ fichiers (arkalia-core, themes, components, responsive, accessibility, smart-empty-states, interface-improvements, empty-states, reward-animations, loading-animations, progression-animations, adaptive-guidance, adaptive-ui, instant-feedback, interactive-zones, progression-feedback, casual-system, contextual-feedback, mini-games, animations-optimized, performance-optimized, arkalia-visual-2026, etc.). L’ordre de chargement et les `!important` créent des conflits.
- **Deux directions en même temps** : la refonte 2026 (ambre/corail, cyan) surcharge les variables Luna/Matrix (violet, vert). Les templates utilisent encore `--violet-lunaire`, `--matrix-green` dans des styles inline, donc le rendu peut être incohérent ou « cassé » selon la page.
- **Résultat** : rendu imprévisible, parfois « affreux », selon les écrans.

### 1.2 Comportement (« rien ne fonctionne comme prévu »)

À clarifier avec toi, point par point :

- **Accueil** : le bouton « Rejoindre LUNA » mène-t-il bien à `/histoire` ? La page s’affiche-t-elle correctement ?
- **Aventure** : en arrivant sur `/histoire`, vois-tu le bloc LUNA, la barre de progression, le message du chapitre et le bouton « Continuer » ? En cliquant sur « Continuer », le chapitre suivant s’affiche-t-il ?
- **Choix (acte 5)** : les boutons de choix apparaissent-ils ? En cliquant, vois-tu « Tu as choisi : … » et la suite ?
- **Navigation** : les liens du menu (Monde, Profil, Terminal, etc.) fonctionnent-ils ? Des 404 ou des pages vides ?
- **Terminal** : les commandes répondent-elles (ex. `aide`, `statut`) ? Message d’erreur pour commande inconnue ?

Dès qu’on sait **quelles actions** ne marchent pas (et sur **quelle page**), on peut cibler les corrections.

---

## 2. Plan proposé

### 2.1 Court terme : visuel minimal pour accueil + histoire

- **Option A** : Désactiver `arkalia-visual-2026.css` sur l’accueil (`index.html`) et sur l’Aventure (`histoire.html`), et ne garder qu’une base cohérente (arkalia-core + thèmes Luna existants). Rendu plus prévisible, moins « chargé ».
- **Option B** : Introduire une feuille `arkalia-minimal.css` utilisée uniquement pour `/` et `/histoire` : fond sombre, texte lisible, un accent (ex. vert ou bleu), pas de refonte 2026, pas de dizaines de fichiers. Objectif : propre et lisible.

Tu peux choisir A ou B (ou les deux : A pour tout désactiver 2026 sur ces pages, B pour un style volontairement minimal).

### 2.2 Vérifier le flux principal

- S’assurer que :
  - `GET /api/story/state` et `POST /api/story/choice` répondent correctement ;
  - Les liens « Rejoindre LUNA », « Aventure », « Continuer » et les choix mènent aux bonnes URLs et mettent à jour l’affichage.
- Corriger les bugs identifiés (liens cassés, JS qui ne s’exécute pas, API qui renvoie une erreur).

### 2.3 Moyen terme

- Réduire le nombre de CSS chargés sur les pages critiques (accueil, histoire) : viser 2–3 fichiers max pour ces écrans.
- Documenter dans ce fichier (ou dans STATUT_PROJET_ACTUEL) ce qui a été changé et ce qui reste à faire.

---

## 3. Ce qu’on a fait dans cette session

- Création de ce doc (`REPARTIR_SUR_DES_BASES_SANES.md`).
- **Visuel minimal appliqué partout** : création de `static/css/arkalia-minimal.css` (fond sombre, texte lisible, accent bleu unique). **Toutes** les pages (accueil, histoire, terminal, monde, profil, dashboard, leaderboard, tutoriel, skill-tree, explorateur, mail, audio, accessibilité, tutoriels techniques) chargent désormais ce CSS à la place de la refonte 2026 — rendu sobre et cohérent sur l’ensemble du jeu.
- Les routes `/`, `/histoire`, `GET /api/story/state` et `POST /api/story/choice` existent bien dans le projet ; le flux reste à valider en lançant l’app et en testant (bouton « Rejoindre LUNA », « Continuer », choix acte 5).
- (À faire avec toi) Liste précise des écrans et actions qui « ne fonctionnent pas » pour corriger en priorité.

---

## 4. Comment me dire ce qui ne va pas

Si tu peux, précise pour chaque point **OUI** ou **NON** (ou « je n’ai pas testé ») :

| # | Question | Oui / Non |
|---|----------|-----------|
| 1 | Accueil : le bouton « Rejoindre LUNA » mène à /histoire ? | |
| 2 | /histoire : tu vois le bloc LUNA + message + bouton « Continuer » ? | |
| 3 | Clic sur « Continuer » : le chapitre suivant s’affiche ? | |
| 4 | Acte 5 : les choix s’affichent et réagissent au clic ? | |
| 5 | Les liens du menu (Monde, Profil, etc.) fonctionnent ? | |
| 6 | Tu préfères qu’on retire la refonte 2026 (visuel plus sobre) ou qu’on garde les couleurs ambre/cyan mais qu’on simplifie ? | |

Avec ça, on pourra corriger en priorité ce qui bloque vraiment et ajuster le visuel selon ta préférence.
