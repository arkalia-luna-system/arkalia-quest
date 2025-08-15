---
**Statut : ARCHIVÉ**
**Date d'archivage : Juillet 2025**
**Résumé :** Fichier d'optimisation Cursor, non utilisé dans la documentation active.

**Liens utiles :**
- [Documentation principale](../docs/README.md)
- [README archive](README_ARCHIVE.md)
---

# 🚀 CURSOR BOOST – RÈGLES D’AMÉLIORATION ARKALIA QUEST

> Fichier de référence pour booster, structurer et maintenir le projet *Arkalia Quest* dans Cursor, avec cohérence, clarté, et immersion. À lire en priorité avant toute modification importante.

---

## ✅ 1. COMPORTEMENTS ATTENDUS

- Toujours vérifier les fichiers existants avant de créer de nouveaux.
- Ne jamais surcharger un fichier unique (diviser logique, fonctions, UI, data).
- Éviter les hacks non testés ou les effets magiques implicites.
- Si un test est manquant : signaler, créer ou au moins documenter.
- Si un fichier devient trop long (700+ lignes) : proposer un refactor automatique.
- Préserver la **cohérence narrative** : LUNA n’agit pas comme un chatbot banal.

---

## 🧠 2. RÈGLES D’ÉCRITURE DU CODE

- **Langage :** Python 3.10+
- **Framework principal :** Flask + HTML minimal
- **Modularité :** tout nouveau composant doit être testable seul
- **Mémoire IA :** stockée sous forme de JSON ou TOML dans un dossier `/data/` clair
- **Logs :** toujours lisibles pour un ado (éviter les `Traceback` internes non gérés)

---

## 📜 3. STRUCTURE DES FICHIERS RECOMMANDÉE

arkalia-quest/
├── app.py
├── arkalia_engine.py
├── /routes/
│   ├── tutorial.py
│   ├── profile.py
│   └── memory_fragments.py
├── /static/
├── /templates/
├── /data/
│   ├── player_profile.json
│   └── memory_state.toml
├── /tests/
│   ├── test_tutorial.py
│   └── test_profile_loading.py

---

## 🧪 4. TESTS À PRIORISER

- Chargement profil joueur
- Affichage mission / dialogues
- Récupération fragments de mémoire
- Calcul du score / progression
- Choix utilisateur dans un chapitre

---

## 🎮 5. IMMERSION POUR ADO DE 13–15 ANS

- Pas de terminal au début.
- Interface web immersive (faux OS, mails, alertes).
- Mission = toujours un défi symbolique + une compétence réelle.
- Interface stylée, animations légères mais percutantes.
- LUNA doit rester intrigante, bienveillante mais mystérieuse.

---

## 🛠️ 6. PRÉFÉRENCES & ALIAS DEV

- `ark-clean` = suppression des fichiers indésirables :
  ```bash
  find . -name "__pycache__" -exec rm -rf {} +;
  find . -name "*.DS_Store" -delete;
  find . -name "._*" -delete;
  find . -name "*.pyc" -delete;

  	•	ark-test = run des tests + couverture
	•	ark-docs = preview local des fichiers Markdown utiles

⸻

🔮 7. MÉMOIRES COMPORTEMENTALES
	•	LUNA doit se souvenir de l’utilisateur à travers :
	•	Les choix passés (/data/choices.json)
	•	Les fragments de mémoire retrouvés
	•	Son ton change selon les émotions débloquées

⸻

📅 8. RÈGLES DE VERSIONNING / DÉPLOIEMENT
	•	Chaque version stable doit :
	•	Avoir 100 % de tests passés
	•	Avoir un README.md à jour
	•	Être taguée (vX.Y.Z)
	•	Être testée mobile et tablette
	•	Avoir ses fichiers .md mis à jour :
	•	README.md, AMELIORATIONS_FUTURES.md, ETAT_PROJET.md, etc.

⸻

💬 9. PHILOSOPHIE ARKALIA

“Un jeu qui apprend sans en avoir l’air. Une IA qui n’est ni une servante, ni une maîtresse, mais une sœur numérique.”

	•	Chaque ajout de feature doit respecter cette dualité : émotion + logique
	•	Le joueur ne contrôle pas LUNA. Il coopère avec elle.
	•	L’univers doit évoluer par fragments, comme une mémoire qui revient.

⸻

Fin du fichier. Mis à jour le : {{ 2025-07-09 }}