# Ce qu’il manque pour passer de « null » à « super »

*Résumé après vérification du 7 février 2026 : app lancée, /, /histoire, /tutorial OK ; commit poussé en local ; push à faire par toi avec `git push origin develop`.*

---

## Déjà en place (pour ne plus être « null »)

- Parcours clair : **Accueil → Aventure** (bouton « Rejoindre LUNA » → `/histoire`).
- Page Histoire : chapitres, bouton **Continuer**, barre de progression, bloc LUNA, **feedback** (son, +X pts, célébration du bouton).
- Tutoriel orienté **Aventure** (REJOINDRE L’AVENTURE → `/histoire`).
- Messages d’erreur encourageants, doc à jour (COMPARAISON, checklist Aventure).
- **Choisir dans l’histoire** : chapitre « Le choix final » (acte_5) propose 3 boutons (Fusion LUNA et NEXUS, Détruire PANDORA, Neutraliser sans détruire) ; `POST /api/story/choice` accepte `choice_id` (optionnel).
- **Fonds par chapitre** : chaque chapitre a un `background` CSS (dégradés : story-bg-mystery, story-bg-cyber, story-bg-tension, etc.) appliqué sur la page.
- **Émotions LUNA** : chaque chapitre a une `emotion` affichée dans le bloc LUNA (ex. « LUNA : déterminée », « LUNA : sereine »).
- **Transition entre chapitres** : courte animation (opacité + translateY) au passage au chapitre suivant.
- **Écran de fin** : sous-titre « Tu as accompli ta mission », boutons mis en avant (Explorer le monde, Mon profil, Accueil).
- **Ambiance** : bouton « 🔊 Ambiance » / « 🔇 Couper ambiance » sur la page Histoire (synchro avec accueil).
- **Badge « Nouveau »** : affiché à côté du titre quand on passe au chapitre suivant (5 s).
- **« Tu as choisi : … »** : après un choix (acte_5), la phrase s’affiche au-dessus du titre du chapitre suivant.
- **Navbar** : Monde, Profil, Classement, etc. visibles dès le premier chapitre complété (prologue ou acte_1).
- **Message narratif par choix** (acte_5) : `choice_messages` dans le JSON, API retourne `choice_message`, affiché sur la page (« Tu as choisi la fusion… », etc.).
- **Un seul endroit aide** : en cas de commande inconnue au terminal, hint « tape aide » + « Va au Tutoriel ou à l’Aventure (menu) ».
- **Sauvegarde / reprise** : GET /api/story/state = chapitre en cours ; reprise correcte au retour sur /histoire.

---

## Ce qu’il reste à faire pour que le jeu devienne « super »

### 1. **Push Git (à faire par toi)**

- Lancer : `git push origin develop` (les commits sont faits en local).

---

### 2. **Contenu et ressenti « jeu »**

| Priorité | Action | Impact |
|----------|--------|--------|
| ~~Haute~~ ✅ | ~~**Vrais choix**~~ : acte_5 a 3 boutons de choix ; API accepte `choice_id`. À étendre à d’autres chapitres ou branches si besoin. | Fait. |
| ~~Haute~~ ✅ | ~~**Fonds par chapitre**~~ : fonds CSS (dégradés) par chapitre dans `story_chapters.json` + classe sur `.story-workspace`. | Fait. |
| ~~Moyenne~~ ✅ | ~~**Musique / ambiance**~~ : bouton « 🔊 Ambiance » sur la page Histoire (toggle, synchro localStorage avec l’accueil). | Fait. |
| ~~Moyenne~~ ✅ | ~~**Texte des chapitres**~~ : prologue légèrement raccourci ; une idée forte par écran. | Fait (prologue). |

---

### 3. **Game feel et polish**

| Priorité | Action | Impact |
|----------|--------|--------|
| ~~Moyenne~~ ✅ | ~~**Transitions**~~ : classe `.story-transition` (opacité + translateY) au changement de chapitre. | Fait. |
| ~~Moyenne~~ ✅ | ~~**Émotions LUNA**~~ : champ `emotion` par chapitre dans le JSON, affiché dans le bloc LUNA. | Fait. |
| ~~Basse~~ ✅ | ~~**Badge « Nouveau »**~~ : affiché à côté du titre quand on avance au chapitre suivant (disparition après 5 s). | Fait. |

---

### 4. **Cohérence et clarté**

| Priorité | Action | Impact |
|----------|--------|--------|
| ~~Haute~~ ✅ | ~~**Lien Monde / Profil**~~ : navbar affiche Monde/Profil/Classement/etc. dès qu’au moins un chapitre est complété (`missions_completed` non vide). | Fait. |
| ~~Moyenne~~ ✅ | ~~**Écran de fin**~~ : sous-titre + boutons .story-link-btn (Monde, Profil, Accueil). | Fait. |
| ~~Basse~~ ✅ | ~~**Un seul endroit « aide »**~~ : terminal en cas d’erreur indique « tape aide » + « Va au Tutoriel ou à l’Aventure (menu) » pour un seul parcours aide/aventure. | Fait. |

---

### 5. **Validation réelle : playtests**

| Priorité | Action | Impact |
|----------|--------|--------|
| Haute | **Playtests avec 2–3 ados** (15 min) en suivant [PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md). | Tu sauras si le parcours Aventure + Continuer est compris, si c’est fun, et ce qui bloque. |
| Haute | **Noter les retours** dans STATUT_PROJET_ACTUEL (template dans COMPARAISON_JEUX_SOURCES_EXTERNES.md) et **prioriser 1–2 changements** (texte, bouton, difficulté, ordre des chapitres). | Itération basée sur du concret, pas du feeling. |

---

### 6. **Technique et données (optionnel mais utile)**

| Priorité | Action | Impact |
|----------|--------|--------|
| ~~Moyenne~~ ✅ | ~~**Branches narratives**~~ : acte_5 a des `choice_messages` (phrase narrative par choix) ; l’API retourne `choice_message` et la page l’affiche. | Fait. |
| ~~Basse~~ ✅ | ~~**Sauvegarde / reprise**~~ : l’API `GET /api/story/state` renvoie le chapitre en cours ; quitter puis revenir sur `/histoire` reprend au bon chapitre. | Vérifié. |

---

## Pour un jeu parfait — ce qui reste (à faire par toi)

Tout le reste listé dans ce doc est **fait** (choix, fonds, émotions, transitions, ambiance, badge Nouveau, « Tu as choisi », message narratif par choix, aide unifiée Terminal → Tutoriel/Aventure, sauvegarde vérifiée). Il ne reste que :

1. **Playtests avec 2–3 ados** (15 min) : suivre [PLAYTEST_GUIDE_ADOS.md](PLAYTEST_GUIDE_ADOS.md), noter les retours dans STATUT_PROJET_ACTUEL (template dans COMPARAISON_JEUX_SOURCES_EXTERNES.md), prioriser 1–2 changements.
2. **Itérer** après les playtests (texte, bouton, difficulté, ordre des chapitres).

---

## Ordre recommandé (après le push)

1. **Push** : `git add .` puis `git commit -m "..."` (si besoin) puis `git push origin develop`.
2. **Playtests** avec 2–3 ados ; noter les retours.
3. **Ajuster** 1–2 points prioritaires d’après les retours.

---

## Résumé en une phrase

Le jeu est passé de « null » à **très avancé** : vrais choix, image/ambiance, feedback, aide claire. Pour le rendre **parfait** : **tester avec de vrais joueurs** (playtests) puis **itérer**.

---

## Commandes pour pousser sur develop

À exécuter dans le terminal, **une commande après l’autre** (ne pas coller tout en une ligne) :

```bash
cd /Volumes/T7/devstation/arkalia-quest
git add .
git status
git commit -m "feat: jeu parfait — message narratif par choix, aide unifiée terminal, doc à jour"
git push origin develop
```

Si tu as déjà des changements commités et que tu veux seulement pousser :

```bash
cd /Volumes/T7/devstation/arkalia-quest
git push origin develop
```
