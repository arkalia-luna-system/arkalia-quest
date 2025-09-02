# 🌌 ARKALIA QUEST — Plan de test utilisateur ULTRA-PERFORMANT  
**URL du jeu** : https://arkalia-quest.onrender.com/  
**Cible** : Test complet UX/UI, design, accessibilité, performance et robustesse  
**Version** : 3.0.0 - Test post-améliorations utilisateur

***

## 📋 Pré-requis

- **Jeu testé** : ARKALIA QUEST — PORTAL LUNA
- **Lien du jeu** : https://arkalia-quest.onrender.com/
- **Testé sur** : Chrome, Edge ou Firefox à jour
- **Son activé**, mode privé désactivé, zoom à 100%
- **Session propre** (vider cache/cookies si possible)
- **Durée cible** : 25–40 min (hors tests avancés)
- **Outils :** chronomètre, capture d'écran, devtools, simulateur débit, Lighthouse, axe-core
- **Objectifs :**  
  - Détecter tout bug, ralentissement, incohérence UX/UI, souci accessibilité, données inexactes, edge case et problème d'immersion
  - **NOUVEAU** : Tester les améliorations récentes (persistance tutoriel, valeurs N/A, progression visible, test audio)
  - **NOUVEAU** : Validation design Matrix/terminal avec couleurs #00ff00
  - **NOUVEAU** : Tests d'accessibilité WCAG 2.1 AA complets

***

## 📝 Infos à relever

- **Appareil** : modèle, OS, navigateur, version
- **Type de connexion** : fibre/ADSL/4G/5G, débit, stabilité
- **Durée totale constatée**
- **Impression générale** : fluidité, facilité, fun, bugs rencontrés
- **Temps perçu pour chaque étape/page**
- **Tout bug, message inattendu ou ressenti à noter pendant le test**
- **NOUVEAU** : Score Lighthouse (Performance, Accessibilité, Bonnes pratiques, SEO)
- **NOUVEAU** : Temps de chargement First Contentful Paint (FCP), Largest Contentful Paint (LCP)
- **NOUVEAU** : Validation couleurs Matrix (#00ff00) et cohérence visuelle

***

## 🔍 Scénarios & Checklist avancée à cocher (scénario par scénario)

### 1. Première visite — Accueil & Design Matrix

- [ ] L'URL s'ouvre sans bug, chargement <2s
- [ ] Page d'accueil : rien de cassé, pas de "None/undefined"
- [ ] **NOUVEAU** : Validation couleurs Matrix (#00ff00) présentes et cohérentes
- [ ] **NOUVEAU** : Test Lighthouse Performance > 90, Accessibilité > 95
- [ ] Les CTA/nav sont immédiatement visibles
- [ ] Test : resize la fenêtre (desktop/mobile) → pas de bug
- [ ] Zoom 150%+ → contenu lisible, rien qui déborde/casse
- [ ] Navigation clavier possible, tabulation/focus logique
- [ ] Aucun flickering, layout shift fort ou bug visuel
- [ ] Focus initial logique pour accessibilité
- [ ] **NOUVEAU** : Test axe-core : 0 erreur d'accessibilité
- [ ] Screenshot avant/après resize/zoom

### 2. Tutoriel — Parcours complet & Persistance

- [ ] Ouverture tutoriel par le menu/lien direct OK
- [ ] 5 à 10 étapes parcourues : "suivant", choix, feedback
- [ ] **NOUVEAU** : Reload à mi-parcours > progression conservée (localStorage)
- [ ] **NOUVEAU** : Notification "Progression sauvegardée" visible
- [ ] **NOUVEAU** : Confirmation avant quitter tutoriel fonctionne
- [ ] Feedback immédiat : animation/son/visuel à chaque étape
- [ ] Spam clics successifs sur "suivant" → stabilité
- [ ] Aucun placeholder "..." ou incohérent
- [ ] Erreur logique affichée si mauvaise action (compréhensible)
- [ ] Changement langue (si dispo) à la volée
- [ ] Responsive mobile validé
- [ ] **NOUVEAU** : Test accessibilité tutoriel (navigation clavier, ARIA)
- [ ] Screenshot étape clé

### 3. Terminal — Noyau du gameplay & Design Matrix

- [ ] Commande help/profile/mission intro/decode_portal → réponses rapides
- [ ] **NOUVEAU** : Validation design Matrix (#00ff00) dans terminal
- [ ] **NOUVEAU** : Test commandes "aide", "commands", "liste", "menu" (nouveaux alias)
- [ ] Commande inconnue → erreur propre, jamais de blocage/crash
- [ ] Commandes répétées/spam → aucune instabilité (anti-flood)
- [ ] Typo ou commande mal saisie → message d'erreur adapté
- [ ] Test copier/coller et navigation clavier
- [ ] UI résistante : zoom fort, vieux navigateur, fenêtrage maximal, dark mode
- [ ] **NOUVEAU** : Test accessibilité terminal (focus visible, navigation clavier)
- [ ] Transitions vers autres modules fluides (pas de reload sauvage)

### 4. Monde — Navigation & Progression Visible

- [ ] /monde affiche tous les éléments interactifs
- [ ] **NOUVEAU** : Barre de progression visible avec pourcentage animé
- [ ] **NOUVEAU** : Animation de brillance sur barre de progression
- [ ] Feedback dynamique lié à la progression (après tutoriel : monde évolue ?)
- [ ] Pas de zone vide, lien mort ni incohérence 
- [ ] Reload/retour arrière/déconnexion à tester
- [ ] **NOUVEAU** : Test responsive barre de progression mobile
- [ ] Immersion et ambiance notées

### 5. Profil — XP, badges, stats

- [ ] Page lisible, données réalistes/à jour, rien de faux/undefined
- [ ] Après tuto ou terminal, retour profil → stats modifiées ?
- [ ] Refresh/remontée UI ok
- [ ] Copier/coller+responsive mobile validé

### 6. Dashboard — Synthèse & Valeurs N/A

- [ ] Missions, badges, leaderboard visibles, pas de chargement infini
- [ ] **NOUVEAU** : Valeurs par défaut affichent "N/A" au lieu de "0" ou "--"
- [ ] **NOUVEAU** : Test persistance valeurs N/A après reload
- [ ] Graphes affichés, données cohérentes avec profil/leaderboard
- [ ] Impossible de casser l'affichage en resize/zoom
- [ ] **NOUVEAU** : Test responsive dashboard avec valeurs N/A

### 7. Leaderboard

- [ ] Classement visible, tri correct
- [ ] Score mis à jour après mission 
- [ ] Pas de doublons, value "None", bug en scroll/clics rapides

### 8. Explorateur

- [ ] Les flèches/boutons naviguent sur tout le contenu
- [ ] Aucun lien mort, JS error, bug visuel
- [ ] Reload revient au même contenu
- [ ] Responsive mode paysage/mobile

### 9. Mail in-game

- [ ] Messages scénarisés présents, pertinents après progression 
- [ ] Aucun contenu inopiné
- [ ] Spam/répétition : boîte mail reste utilisable

### 10. Audio

- [ ] Lecture/stop/volume → fonctionnement immédiat
- [ ] Pas de bug en l'absence de device audio
- [ ] Changement volume réactif, pas de bug/pic sonore

### 11. Accessibilité

- [ ] Contraste élevé, texte taille +/-, réduction animation → bugs ?
- [ ] Roles ARIA cohérents, navigation clavier complète
- [ ] Préférences accessibilité sauvegardées post-reload

### 12. Santé & Perf

- [ ] /health renvoie "healthy", /metrics lisible
- [ ] TOUTES pages <2s (p50), aucune >5s même en 3G simulée
- [ ] JAMAIS d'erreur 500

### 13. Mobile/Tablette

- [ ] Accueil + tutoriel + terminal testés sur vrai device ou simulateur mobile
- [ ] Layout, inputs, scroll OK
- [ ] Orientation paysage/portrait
- [ ] Touch/swipe : comportements attendus

### 14. Sécurité/Robustesse

- [ ] Check : aucune data pers, clé, token visible DOM/console
- [ ] Données utilisateurs anonymisées / privées
- [ ] Déco/session expiry : déconnexion propre
- [ ] Tests URLs critiques → comportement safe/logiquement attendu

### 15. Edge-cases/Anti-patterns

- [ ] Spam click n'importe où : jamais de plantage
- [ ] Navigation très rapide : jeu reste stable
- [ ] Multitabs ouvert → tout cohérent côté user
- [ ] Reload/relogin pendant action : pas de bug bloquant
- [ ] Dark/light mode/contraste/tonalité cohérence
- [ ] Feedback UI sur chaque action sensible

***

## ✅ Synthèse rapide (cocher Y/N)

- [ ] Accueil/landing impeccable
- [ ] Tutoriel complet et persistant
- [ ] Terminal fluent + erreur propre
- [ ] Monde/Explorateur fonctionnels sans broken link
- [ ] Profil/Dashboard cohérent à chaque retour
- [ ] Classement/Leaderboard/tri réel
- [ ] Accessibilité prefs persistantes/rejouables
- [ ] Audio OK en toutes circonstances
- [ ] Santé, perf sans stress
- [ ] Zéro bug/crash signalé — jamais

***

## 📋 Formulaire feedback instantané

- **Appareil/Navigateur** :
- **Facilité d'utilisation (1–5)** :
- **Fun/engagement (1–5)** :
- **Pages lentes/notées** :
- **Bugs rencontrés (story + page + message)**:
- **Suggestions rapides (< 3)** :
- **Screens/logs + URL en cas de bug** :
- **Points forts** :
- **Points négatifs/incohérences** :
- **Score global (1–5)** :

***

## 🎯 Prompt IA pour analyse maximale

Voici le prompt à fournir à un LLM/chatbot qui doit "analyser" ARKALIA QUEST :
```
Tu es un testeur QA+UX spécialisé IA.  
En utilisant le plan ci-dessus, joue à ARKALIA QUEST sur https://arkalia-quest.onrender.com/ comme un utilisateur réel, et plus :  
- Suis chaque scénario dans l'ordre + teste chaque edge case.
- Repère tous bugs visuels, libellés, incohérences données, crashes, lenteurs, soucis/responsivité.
- Liste pour chaque étape : ce qui ne marche pas, ce qui surprend, chaque suggestion d'UX.
- Termine par une synthèse claire : axes d'amélioration, bugs "crash", bugs "mineurs", suggestions design/priorisation.
- N'hésite pas à remplir la mini-checklist, évaluer chaque section et envoyer logs/screens.
Objectif : tout voir, rien oublier, même les détails cachés!
```

***

*Ce plan de test est maintenu par l'équipe Arkalia Quest.*
