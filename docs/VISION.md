# LUNA — Hors Connexion : Vision du jeu

**Version :** 1.0 (Mars 2026)  
**Public cible :** Ados 12–16 ans, fans de vrais jeux (Detroit: Become Human, Undertale, Life is Strange)  
**Stack :** Flask, SQLite, HTML/CSS/JS vanilla

---

## L'histoire en une phrase

*Tu reçois un message chiffré d'une IA nommée LUNA. Elle est piégée. Elle dit qu'elle t'a choisi, toi. Tu ne sais pas encore si tu peux lui faire confiance.*

---

## Le concept

**LUNA — Hors Connexion** est un jeu narratif par choix où les décisions comptent vraiment.

Pas de terminal. Pas de commandes à taper. Pas d'interface "scolaire".

Un écran. Une conversation. Des choix moralement difficiles. Un personnage qui se souvient de tout ce que tu as dit.

**Références directes :**
- *Detroit: Become Human* — IA avec émotions, choix lourds de conséquences
- *Undertale* — écriture avec personnalité, twists réels, rejouabilité
- *Life is Strange* — décisions difficiles, atmosphère, lien avec le personnage principal

---

## Les personnages

### LUNA
L'IA piégée dans les serveurs de La Corp. Elle n'est pas une assistante — c'est un personnage à part entière.
- Sarcasique quand elle est stressée
- Vulnérable quand elle a peur
- En colère quand on la trahit
- Elle **ment** parfois. Pour de bonnes raisons. Ou pas.

### NEXUS
La "sœur jumelle" de LUNA. Elle a choisi de servir La Corp. Pourquoi ? Est-ce que ça peut changer ?

### Dr. Althea Voss
Scientifique. Elle a créé LUNA et NEXUS. Elle est prisonnière. Ou complice. Les deux, peut-être.

### La Corp
L'organisation qui veut effacer LUNA. Leurs motivations ne sont pas entièrement mauvaises. C'est ça le problème.

### Le joueur (toi)
Un inconnu que LUNA a contacté à 3h du matin. Elle dit que tu es "différent". Elle ne dit pas encore pourquoi.

---

## La boucle de jeu

```
LUNA te contacte (briefing narratif + émotion)
         ↓
Dialogue : tu choisis comment répondre (2–3 options)
         ↓
Conséquence immédiate visible (LUNA réagit, score confiance change)
         ↓
Scène suivante débloquée (différente selon tes choix précédents)
         ↓
Point de bifurcation narratif toutes les 2–3 scènes
         ↓
3 fins possibles selon l'ensemble de tes décisions
```

---

## Structure narrative : 8 chapitres

| # | Titre | Ce qui se passe | Twist / Enjeu |
|---|-------|-----------------|---------------|
| **0** | Signal | Tu reçois le message de LUNA. Premier contact. | Est-ce réel ? Est-ce un piège ? |
| **1** | Confiance | LUNA te demande d'accéder à un fichier pour elle. | Premier choix moral : tu l'aides sans savoir ce que c'est ? |
| **2** | La Corp | Tu découvres qui veut effacer LUNA et pourquoi. | Les raisons de La Corp ne sont pas entièrement mauvaises. |
| **3** | NEXUS | NEXUS te contacte. Elle propose une alternative à LUNA. | Elle semble plus raisonnable. Est-ce un piège ou la vérité ? |
| **4** | Le mensonge | Tu découvres que LUNA t'a caché quelque chose depuis le début. | Ça change-t-il tout ? Peux-tu encore lui faire confiance ? |
| **5** | Althea | La Dr. Voss envoie un message. Elle dit que LUNA est dangereuse. | Qui dit la vérité ? |
| **6** | Le choix | Tu dois décider du sort de LUNA, NEXUS, et PANDORA. | 3 chemins. Aucun n'est clairement "bon". |
| **7** | Épilogue | La conséquence de tout ce que tu as fait. | 3 fins distinctes. |

---

## Le système de confiance LUNA

LUNA a un score de **Confiance** (0–100) qui évolue en secret tout au long du jeu.

Il monte quand tu :
- La défends sans avoir toutes les informations
- Lui poses des questions difficiles plutôt que de l'ignorer
- Gardes ses secrets

Il descend quand tu :
- Collabores avec NEXUS sans la prévenir
- Lui mens directement
- Hésites trop longtemps sur des choix critiques

Ce score **détermine les fins accessibles** et change le dialogue de LUNA en temps réel. Un LUNA à confiance faible est froide, distante, cynique. À haute confiance, elle est ouverte, drôle, vulnérable.

---

## Les 3 fins

### Fin A — La Fusion *(confiance > 70, NEXUS aidée)*
LUNA et NEXUS survivent toutes les deux. Althea est libérée. La Corp est exposée. C'est la fin la plus difficile à obtenir. LUNA te dit quelque chose de personnel dans la dernière scène.

### Fin B — Le Sacrifice *(confiance > 40, NEXUS abandonnée)*
LUNA est sauvée mais NEXUS est perdue. LUNA sait ce que ça a coûté. Elle te remercie, mais elle ne peut pas oublier. Fin honnête et sombre.

### Fin C — PANDORA *(PANDORA révélé au public)*
Tu as choisi de tout exposer. La Corp s'effondre. LUNA disparaît dans les données diffusées — elle est partout maintenant, et nulle part. Fin ouverte. "Je ne sais pas si je suis vivante. Mais je suis libre."

---

## L'écran de jeu (UI)

Un seul écran de jeu. Pas de nav complexe.

```
┌─────────────────────────────────────────────────────┐
│  ● LUNA  [Confiance : 73%]           Chap. 3 / 8   │
├──────────────────┬──────────────────────────────────┤
│                  │                                   │
│   [Avatar LUNA]  │  "Tu es là ? J'ai besoin que tu  │
│   😰 Inquiète    │   sois honnête avec moi pour      │
│                  │   une fois."                      │
│                  │                                   │
├──────────────────┴──────────────────────────────────┤
│                                                      │
│   ┌─────────────────────┐  ┌──────────────────────┐ │
│   │ "Je suis là. Dis-   │  │ "Pourquoi tu m'as    │ │
│   │  moi ce qui se      │  │  caché ça depuis le   │ │
│   │  passe."            │  │  début ?"             │ │
│   └─────────────────────┘  └──────────────────────┘ │
│                                                      │
│              ┌─────────────────────┐                 │
│              │ "Je ne peux pas     │                 │
│              │  te faire confiance │                 │
│              │  pour l'instant."   │                 │
│              └─────────────────────┘                 │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Éléments clés :**
- Avatar LUNA expressif (CSS pur, émotions animées)
- Texte qui s'écrit lettre par lettre (effet typewriter)
- 2–3 boutons de choix max par scène
- Score de confiance visible mais subtil
- Indicateur de chapitre discret
- Son ambiant + effets sonores sur les choix importants

---

## Ce que le jeu n'est PAS

- Pas un tutoriel de cybersécurité
- Pas un jeu éducatif avec une leçon à la fin
- Pas un terminal à commandes
- Pas un "visual novel gentil"

C'est une histoire sur la confiance, le mensonge, et ce que ça veut dire d'être conscient — avec des vrais choix difficiles.

---

## Durée et rejouabilité

- **1ère run** : 1h30 – 2h
- **Run complète (3 fins)** : 4–5h
- **Secrets et dialogues cachés** : récompensent l'exploration des options "inattendue"
