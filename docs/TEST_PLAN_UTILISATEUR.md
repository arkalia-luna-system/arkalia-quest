
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



### 10. Audio & Test Audio



- [ ] Lecture/stop/volume → fonctionnement immédiat


- [ ] **NOUVEAU** : Bouton "Test Audio" visible et fonctionnel


- [ ] **NOUVEAU** : Test audio génère son réel (note A4, 440Hz)


- [ ] **NOUVEAU** : Feedback visuel "✅ Audio OK" / "❌ Audio Désactivé"


- [ ] **NOUVEAU** : Persistance état audio dans localStorage


- [ ] **NOUVEAU** : Bouton change "🔊 Test Audio" / "🔇 Activer Audio"


- [ ] Pas de bug en l'absence de device audio


- [ ] Changement volume réactif, pas de bug/pic sonore



### 11. Accessibilité WCAG 2.1 AA



- [ ] Contraste élevé, texte taille +/-, réduction animation → bugs ?


- [ ] **NOUVEAU** : Test contraste renforcé (high-contrast-enhanced)


- [ ] **NOUVEAU** : Test texte agrandi (large-text)


- [ ] **NOUVEAU** : Test espacement large (large-spacing)


- [ ] **NOUVEAU** : Test indicateur audio (audio-indicator)


- [ ] Roles ARIA cohérents, navigation clavier complète


- [ ] **NOUVEAU** : Test axe-core sur toutes les pages (0 erreur)


- [ ] **NOUVEAU** : Test navigation clavier complète (Tab, Shift+Tab, Enter, Escape)


- [ ] **NOUVEAU** : Test focus visible sur tous les éléments interactifs


- [ ] Préférences accessibilité sauvegardées post-reload



### 12. Santé & Performance



- [ ] /health renvoie "healthy", /metrics lisible


- [ ] **NOUVEAU** : Test Lighthouse Performance > 90 sur toutes les pages


- [ ] **NOUVEAU** : Test First Contentful Paint (FCP) < 1.5s


- [ ] **NOUVEAU** : Test Largest Contentful Paint (LCP) < 2.5s


- [ ] **NOUVEAU** : Test Cumulative Layout Shift (CLS) < 0.1


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



### 16. Design & Cohérence Visuelle



- [ ] **NOUVEAU** : Validation couleurs Matrix (#00ff00) sur toutes les pages


- [ ] **NOUVEAU** : Test cohérence palette de couleurs (violet-lunaire, bleu-spectre)


- [ ] **NOUVEAU** : Test typographie (Cormorant, IBM Plex Mono, Inter)


- [ ] **NOUVEAU** : Test animations et transitions fluides


- [ ] **NOUVEAU** : Test responsive design sur 5 breakpoints (320px, 375px, 768px, 1024px, 1440px+)


- [ ] **NOUVEAU** : Test cohérence navbar sur toutes les pages


- [ ] **NOUVEAU** : Test effets visuels (glow, shadows, gradients)


- [ ] **NOUVEAU** : Test contraste et lisibilité sur tous les éléments


***


## ✅ Synthèse rapide (cocher Y/N)



- [ ] Accueil/landing impeccable


- [ ] **NOUVEAU** : Tutoriel complet et persistant (localStorage)


- [ ] **NOUVEAU** : Terminal fluent + design Matrix (#00ff00)


- [ ] **NOUVEAU** : Monde avec progression visible (barre animée)


- [ ] **NOUVEAU** : Dashboard avec valeurs N/A (pas de 0/--)


- [ ] **NOUVEAU** : Audio avec test fonctionnel et persistance


- [ ] Monde/Explorateur fonctionnels sans broken link


- [ ] Profil/Dashboard cohérent à chaque retour


- [ ] Classement/Leaderboard/tri réel


- [ ] **NOUVEAU** : Accessibilité WCAG 2.1 AA complète


- [ ] **NOUVEAU** : Performance Lighthouse > 90


- [ ] **NOUVEAU** : Design cohérent Matrix/terminal


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


- **NOUVEAU** : Score Lighthouse Performance :


- **NOUVEAU** : Score Lighthouse Accessibilité :


- **NOUVEAU** : Score axe-core (erreurs) :


- **NOUVEAU** : Validation design Matrix (#00ff00) :


***


## 🎯 Prompt IA pour analyse maximale


Voici le prompt à fournir à un LLM/chatbot qui doit "analyser" ARKALIA QUEST :

```

Tu es un testeur QA+UX+Design spécialisé IA.
En utilisant le plan ULTRA-PERFORMANT ci-dessus, teste ARKALIA QUEST sur https://arkalia-quest.onrender.com/ comme un utilisateur réel, et plus :

**NOUVEAU - Tests prioritaires :**

- Teste les améliorations récentes : persistance tutoriel, valeurs N/A dashboard, progression visible monde, test audio


- Valide le design Matrix/terminal avec couleurs #00ff00


- Lance Lighthouse sur toutes les pages (Performance, Accessibilité, Bonnes pratiques)


- Utilise axe-core pour tester l'accessibilité WCAG 2.1 AA


- Teste les nouveaux breakpoints responsive (320px, 375px, 768px, 1024px, 1440px+)


**Tests complets :**

- Suis chaque scénario dans l'ordre + teste chaque edge case


- Repère tous bugs visuels, libellés, incohérences données, crashes, lenteurs, soucis/responsivité


- Teste la cohérence visuelle et le design Matrix sur toutes les pages


- Liste pour chaque étape : ce qui ne marche pas, ce qui surprend, chaque suggestion d'UX


- Termine par une synthèse claire : axes d'amélioration, bugs "crash", bugs "mineurs", suggestions design/priorisation


- N'hésite pas à remplir la mini-checklist, évaluer chaque section et envoyer logs/screens


**Objectif :** tout voir, rien oublier, même les détails cachés, avec focus sur les améliorations récentes et la qualité design/UX!

```


***

*Ce plan de test est maintenu par l'équipe Arkalia Quest.*
