# Guide playtest — Arkalia Quest (ados)

Court guide pour faire tester le jeu par 2–3 adolescents et recueillir des retours utiles.

*Dernière mise à jour : 7 février 2026.*

---

## Objectif

Vérifier en 15–20 minutes :
- Ce que le joueur comprend du jeu (promesse, objectif).
- Où il bloque (navigation, première mission).
- Ce qu’il a aimé ou pas (gameplay, clarté).

---

## Avant la session

- Lancer le jeu en local ou sur l’URL de test.
- Prévoir un navigateur (Chrome/Firefox) sur ordinateur ou tablette.
- Ne pas aider pendant le test ; noter les actions et les remarques.

### Checklist rapide (vérifier que tout fonctionne)

- [ ] L’accueil s’affiche (promesse 15 mots, CTA « Commencer l’aventure »).
- [ ] Clic sur « Commencer l’aventure » → ouverture du terminal.
- [ ] Bannière « tape acte_1 » visible (si profil sans acte_1 fait).
- [ ] Une commande (ex. `aide`) renvoie une réponse et le bandeau Niveau/Score se met à jour.
- [ ] Commande `acte_1` → modal « Choisis le bon code » avec 3 boutons ; un bon code valide et affiche « Prochaine étape : tape acte_2 ».

---

## Scénario (15 min)

1. **Accueil (2 min)**  
   Dire : *« Ouvre la page d’accueil du jeu. En 30 secondes, dis-moi ce que tu crois qu’on fait dans ce jeu. »*  
   Noter : phrase lue (promesse), bouton cliqué en premier.

2. **Première mission (5 min)**  
   Dire : *« Tu peux jouer. Ton but est de faire ta première mission. »*  
   Noter : va-t-il au terminal ? Tape-t-il `acte_1` ? Fait-il le défi (choix du code) ? Où s’arrête-t-il ou hésite-t-il ?

3. **Après acte_1 (3 min)**  
   Dire : *« Continue un peu. Explore si tu veux. »*  
   Noter : quelles pages il ouvre (monde, profil, etc.), s’il comprend la progression (niveau, score).

4. **Retour (5 min)**  
   Poser (à l’oral ou court questionnaire) :
   - En une phrase, c’est quoi ce jeu pour toi ?
   - Qu’est-ce qui t’a plu ?
   - Qu’est-ce qui t’a déplu ou embrouillé ?
   - Sur 10, tu mettrais combien ? Pourquoi ?

---

## Grille d’observation (à imprimer ou noter)

| Moment            | Observé (actions, clics, commandes) | Blocage ? | Commentaire |
|-------------------|-------------------------------------|-----------|-------------|
| Accueil 30 s     |                                     |           |             |
| Navigation 1 min  |                                     |           |             |
| Terminal / acte_1 |                                     |           |             |
| Défi (code A/B/C) |                                     |           |             |
| Suite (monde, etc.) |                                   |           |             |
| Retour verbal     |                                     |           |             |

---

## Indicateurs utiles

- **Clarté** : a-t-il dit une phrase proche de « hacker qui aide LUNA / missions au terminal » ?
- **Premier pas** : a-t-il cliqué sur « Commencer l’aventure » (ou équivalent) puis ouvert le terminal ?
- **Boucle** : a-t-il tapé `acte_1` et fait le défi du code ?
- **Progression** : a-t-il remarqué le niveau / score (bandeau terminal) ?

---

## Après les playtests

- Regrouper les 3 retours : points communs, blocages récurrents, idées.
- Mettre à jour la doc (STATUT, audit) avec « Retours playtest du [date] ».
- Prioriser 1–2 changements (ex. texte d’aide, placement du bouton, difficulté du défi acte_1).

---

*Références : audit [AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md](audits/AUDIT_JEU_MEILLEURES_PRATIQUES_2026.md), checklist fun/visuel [COMPARAISON_JEUX_SOURCES_EXTERNES.md](COMPARAISON_JEUX_SOURCES_EXTERNES.md).*
