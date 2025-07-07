def assistant_repond(entree):
    base_reponses = {
        "salut": "Yo, jeune hacker !",
        "qui es-tu": "Je suis IA-404, reprogrammée pour t'aider 😈",
        "mission": "Trouve le coffre, décrypte le code et entre dans le réseau.",
        "aide": "Essaie des mots comme 'salut', 'mission', ou 'pirate'."
    }

    entree = entree.lower().strip()
    return base_reponses.get(entree, "Je ne comprends pas cette commande, reprogramme-moi !") 