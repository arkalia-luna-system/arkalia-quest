from mission_utils.assistant_pirate import assistant_repond

def test_assistant_base():
    assert assistant_repond("salut") == "Yo, jeune hacker !"
    assert assistant_repond("mission") == "Trouve le coffre, décrypte le code et entre dans le réseau."
    assert "reprogramme-moi" in assistant_repond("je suis perdu") 