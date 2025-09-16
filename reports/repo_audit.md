## Audit dépôt Arkalia Quest — lecture seule (non destructif)

Date: 2025-09-16
Portée: inventaire, actifs statiques, doublons, modules Python non référencés, documentation.

### Synthèse exécutable
- Mise à jour V4: références obsolètes corrigées, systèmes unifiés actés.
- Volumétrie clé: beaucoup de JSON en `data/` (backups et contenus), ~50+ JS, ~35+ CSS, ~100+ Python, ~55+ HTML, ~59 Markdown. Taille totale ~41 Mo (hors venv/.git/DB et fichiers cachés macOS).
- Problèmes principaux:
  - Fichiers macOS « dot-underscore » (`._*`) détectés en JS/CSS/Python: à supprimer en sécurité.
  - Plusieurs références d’actifs dans les templates pointent vers des fichiers inexistants (icônes et JS expérimentaux).
  - Au moins un JS potentiellement non utilisé: `static/js/tutorial.js`.
  - Pas de doublons exacts de contenu JS/CSS (hors `._*`).

---

### 1) Inventaire par type (agrégé)
- html ≈ 56 fichiers
- css ≈ 36 fichiers
- js ≈ 53 fichiers
- py ≈ 109 fichiers
- md ≈ 59 fichiers
- json ≈ 1244 fichiers (surtout `data/`)
- Autres: sh, yaml/yml, ini/toml, logs

Observation: La volumétrie JSON masque une base code relativement propre. Les répertoires applicatifs clés sont `core/`, `engines/`, `utils/`, `templates/`, `static/`.

### 2) Actifs statiques — références manquantes / nettoyage (V4)

Références manquantes relevées dans les templates (véritables manquants + faux positifs avec query string):

Vrais manquants (après consolidation):
- Icônes PWA: à créer ou retirer si non utilisées
  - `static/icons/icon-16x16.png`
  - `static/icons/icon-32x32.png`
  - `static/icons/icon-192x192.png`
  - `static/images/apple-touch-icon.png`
- JS legacy remplacés (ne doivent plus être inclus dans templates prod):
  - `contextual-feedback.js` → remplacé par `universal-notifications.js` (shim OK)
  - `progression-animations.js` → remplacé par `reward-feedback-system.js`
  - `empty-states-enhanced.js` → remplacé par `smart-empty-states.js`
  - `visual-feedback-system.js` → remplacé par `universal-notifications.js`
  - `advanced-features.js`, `competitive-system.js`, `creative-system.js`, `luna-personality.js`, `terminal-enhancements.js` — historiques; non requis en V4

Faux positifs (query string):
- `static/css/arkalia-responsive.css?v=4.0.0` — le fichier existe sans query string. Recommandation: strip `?v=*` lors des vérifications ou adapter le script de contrôle.

JS potentiellement non référencé:
- `static/js/tutorial.js` (aucune inclusion directe). À valider avant suppression.

Fichiers macOS parasites (doublons exacts via hash):
- `static/js/._adaptive-guidance.js`
- `static/js/._popup-manager.js`
- `static/js/._reward-feedback-system.js`
- `static/js/._smart-empty-states.js`
- `static/js/._world-interactions.js`

Ces fichiers sont sans utilité et peuvent être supprimés en sécurité.

### 3) Doublons exacts (hash)
- JS/CSS: aucun doublon exact hors fichiers `._*` macOS.
- Docs (`docs/*.md`): aucun doublon exact détecté.

### 4) Modules Python non importés/exécutés (heuristique)
- Alerte trouvée: `core/._command_handler_v2.py` — fichier macOS parasite. À supprimer.
- Aucune alerte sur des modules Python réels via l’heuristique basename. Pour une détection plus fine (fonctions/classes mortes), prévoir `vulture`/`coverage` ciblés.

### 5) Structure et rationalisation
- `static/` contient les systèmes unifiés V4 (`universal-*`, `smart-empty-states`, `reward-*`). Les scripts legacy ont été neutralisés ou commentés dans les templates; garder pour compat tests jusqu’à retrait définitif.
- Les templates incluent de nombreux CSS différés. Une passe de consolidation pourrait fusionner certaines feuilles (`progression-*`, `animations-*`) si les règles ne sont pas conflictuelles.
- `data/` contient backups; conserver, mais exclure de toute chasse aux inutilisés en prod.

### Recommandations actionnables (sécurisées)
1. Nettoyage fichiers macOS:
   - Supprimer tous les `static/js/._*`, `static/css/._*`, et `core/._*.py`.
2. Corriger les références d’actifs inexistants dans les templates:
   - Remplacer/ajouter les icônes manquantes sous `static/icons/` ou retirer les balises si non nécessaires.
   - Retirer des `<script>` pointant vers des JS inexistants, ou rétablir les fichiers si toujours souhaités.
3. Valider l’usage de `static/js/tutorial.js`:
   - Si obsolète, suppression + retrait d’éventuelles références indirectes.
4. Améliorer le check d’intégrité d’actifs:
   - Adapter le script de vérification pour ignorer `?v=...` (query string de versionning).
5. Optionnel (plus poussée):
   - Installer `ripgrep` et `vulture` pour une analyse plus fine des références et dead code Python.
   - Lancer un coverage ciblé des endpoints critiques pour détecter du code non exécuté.

### Commandes proposées (à exécuter après validation)
Suppression sécurisée des fichiers macOS parasites:
```bash
find static -type f -name '._*' -delete
find core -type f -name '._*' -delete
```

Vérification d’inclusions (strippant les query strings):
```bash
grep -R -n "url_for('static', filename='" templates \
| sed -E "s/.*url_for\('static', filename='([^']+)'\).*/\1/" \
| sed 's/?v=[^']*//' \
| sort -u
```

### Notes
- `ripgrep (rg)` n’est pas installé sur la machine; l’analyse a utilisé `grep` et des heuristiques bash.
- Analyse non destructive; aucune suppression n’a été effectuée.


