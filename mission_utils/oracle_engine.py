def get_oracle_response(question: str, profil: dict) -> str:
    if "mot de passe" in question.lower():
        return "Cherche dans le code source... 🧠"
    elif "dragon" in question.lower():
        return f"Tu as choisi un dragon {profil['preferences'].get('dragon_choisi', 'mystère')} 🐉"
    elif "indice" in question.lower():
        return "L'indice du niveau actuel est : 🔍 'Tout est dans le nom de la commande'"
    return "Je suis l'Oracle. Pose une question plus précise." 