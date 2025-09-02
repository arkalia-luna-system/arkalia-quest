# Document
---
# **Statut : ARCHIVÉ**
# **Date d'archivage : Juillet 2025**
**Résumé :** Plan de refonte du tutoriel, implémenté et remplacé par la documentation centralisée.

# **Liens utiles :**


- [Documentation principale](../docs/README.md)



- [README archive](../docs/archive/README_ARCHIVE.md)


---


# 📚 PLAN DE REFONTE TUTORIEL & ONBOARDING - ARKALIA QUEST



## 1. État actuel du tutoriel et de l'histoire



### Tutoriel interactif (data/tutoriel_interactif.json)



- 5 étapes linéaires (bienvenue, rencontre LUNA, premier hack, mission, récompense)



- Récompenses, messages de motivation, missions rapides prévues



- Intégration technique : commande `start_tutorial`, progression, badges



### Histoire de LUNA (data/story.json)



- IA centrale, personnalité forte, arcs narratifs, secrets, relations



- Dialogues variés, rôle de guide et d'alliée



### Fil conducteur



- Histoire principale "Sauver Internet de La Corp" en 5 étapes



- Progression narrative, cliffhangers, badges, timers



## 2. Limites actuelles



- Tutoriel linéaire, peu d'adaptation au joueur



- Peu d'effets visuels/sonores immersifs



- Pas de choix, de branches, ni de tutoriel adaptatif



- LUNA peu interactive (pas de dialogue évolutif)



- Pas de gestion avancée de la progression (reprise, skip, relance)



- Difficulté à ajouter des variantes ou mini-jeux



## 3. Recommandations pour un tutoriel AAA et durable



### Architecture



- JSON modulaire enrichi (étapes, effets, sons, branches, dialogues, choix)



- Système de scènes, hooks pour effets JS/CSS/sons/confettis



- Gestion de la progression (étape en cours, reprise, skip, relance)



- LUNA interactive (choix, réactions dynamiques, adaptation au style du joueur)



- API analytics (log des étapes, temps, taux de réussite)



- Accessibilité (clavier, synthèse vocale, contrastes)



### Expérience utilisateur



- Immersion narrative à chaque étape



- Feedback immédiat (animations, sons, félicitations)



- Personnalisation selon le style du joueur



- Choix et conséquences (tuto rapide, tuto complet, skip)



### Scalabilité



- Ajout facile de nouvelles étapes, variantes, mini-jeux



- Séparation logique/contenu (Python/JS vs JSON)



- Prévoir un tuto avancé pour les anciens joueurs



## 4. Plan d'action


1. Enrichir le JSON du tutoriel (effets, sons, branches, dialogues, choix)
2. Créer un gestionnaire de progression avancé
3. Développer des hooks front-end pour effets immersifs
4. Rendre LUNA interactive et adaptative
5. Prévoir l'extension (mini-jeux, défis, variantes)
6. Inclure analytics et accessibilité

---

# **Ce plan doit toujours accompagner le fichier tutoriel pour garantir une évolution durable et éviter tout refactoring massif à l'avenir.**
