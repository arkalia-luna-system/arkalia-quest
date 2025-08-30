---
**Statut : ACTIF**
**Dernière mise à jour : Août 2025**
**Résumé :** Guide technique pour les développeurs Arkalia Quest (architecture, bonnes pratiques, outils).

**Liens utiles :**
- [Documentation principale](README.md)
- [Statut projet](STATUT_PROJET_ACTUEL.md)
- [Changelog documentation](CHANGELOG_DOCUMENTATION.md)
---

# 📚 GUIDE TECHNIQUE DÉVELOPPEUR - ARKALIA QUEST

## 🔗 API /commande : Structure de la réponse

### Exemple de requête
```http
POST /commande
Content-Type: application/json

{
  "commande": "hack_system"
}
```

### Réponse JSON (format 2025+)
```json
{
  "reponse": {
    "réussite": true,
    "ascii_art": "💻",
    "message": "...",
    "score_gagne": 80,
    "badge": "Hacker du Système",
    "profile_updated": true,
    "timestamp": "2025-07-09T15:48:15.216007",
    // --- Champs LUNA ---
    "luna_emotion": "proud",
    "luna_message": "💖 Tu as dépassé toutes mes attentes !\n🏆 Nouveau badge : Hacker du Système !",
    "luna_color": "#ff00ff",
    "luna_effect": "sparkle_magenta",
    "luna_sound": "luna_proud",
    "luna_intensity": 1.0,
    "relationship_change": 0.1
  }
}
```

### Détail des champs d'émotion LUNA
| Champ              | Type    | Exemple         | Description |
|--------------------|---------|----------------|-------------|
| `luna_emotion`     | string  | "excited"      | Émotion principale de LUNA (voir tableau ci-dessous) |
| `luna_message`     | string  | "🌙 WOW ! ..." | Message personnalisé de LUNA |
| `luna_color`       | string  | "#00ff00"      | Couleur dominante de l'émotion |
| `luna_effect`      | string  | "pulse_green"  | Effet visuel associé |
| `luna_sound`       | string  | "luna_excited" | Son associé à l'émotion |
| `luna_intensity`   | float   | 0.9            | Intensité de l'émotion (0.0 à 1.0) |
| `relationship_change` | float | 0.1            | Évolution de la relation joueur-LUNA |

#### Valeurs possibles pour `luna_emotion`
| Valeur        | Emoji | Description |
|---------------|-------|-------------|
| excited       | 😊    | Enthousiaste, succès |
| worried       | 😰    | Inquiète, échec |
| proud         | 🥹    | Fière, accomplissement |
| mysterious    | 🔮    | Mystérieuse, nuit |
| determined    | 💪    | Déterminée, hacking |
| playful       | 😄    | Joueur, exploration |
| focused       | 🎯    | Concentrée, mission |
| surprised     | 😲    | Surprise, inattendu |
| calm          | 😌    | Calme, réflexion |
| energetic     | ⚡    | Énergique, motivation |

#### Valeurs typiques pour `luna_effect` et `luna_sound`
- Voir le mapping dans `core/luna_emotions_engine.py` et `static/js/immersive_effects.js`

### Bonnes pratiques d'intégration
- Toujours parser la clé `reponse` dans les retours API.
- Les champs d'émotion sont toujours présents pour toutes les commandes reconnues.
- Pour les commandes inconnues, LUNA réagit avec une émotion adaptée (souvent "worried" ou "calm").
- Les effets visuels et sonores côté front doivent utiliser les champs `luna_color`, `luna_effect`, `luna_sound` et `luna_intensity` pour une expérience cohérente.

---

## 🔧 Maintenance et évolutions
- Toute évolution du format de réponse doit être documentée ici et testée dans `tests/test_immersive_system_complete.py`.
- Pour ajouter une nouvelle émotion ou effet, mettre à jour :
  - `core/luna_emotions_engine.py` (backend)
  - `static/js/immersive_effects.js` (frontend)
  - Les tests associés dans `tests/`

---

Pour toute question technique, contacter l'équipe Arkalia Quest. 