import json

def charger_mission(path):
    with open(path, 'r', encoding='utf-8') as f:
        mission = json.load(f)
    return mission

def charger_mission_by_id(id):
    with open(f"missions/niveau{id}.json", "r", encoding='utf-8') as f:
        return json.load(f)

def appliquer_choix(choix, profil):
    bonus = choix.get("bonus", {})
    profil["stats"] = profil.get("stats", {})
    for stat, value in bonus.items():
        if stat != "badge":
            profil["stats"][stat] = profil["stats"].get(stat, 0) + value
    if "badge" in bonus:
        if bonus["badge"] not in profil["badges"]:
            profil["badges"].append(bonus["badge"])
    return profil
