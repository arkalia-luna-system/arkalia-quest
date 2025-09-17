"""
Tests simplifiés pour adaptive_storytelling.py
"""

from core.adaptive_storytelling import AdaptiveStorytelling


class TestAdaptiveStorytelling:
    """Tests pour la classe AdaptiveStorytelling"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.storytelling = AdaptiveStorytelling()

    def test_init(self):
        """Test de l'initialisation"""
        assert hasattr(self.storytelling, "story_arcs")
        assert hasattr(self.storytelling, "player_choices")
        assert hasattr(self.storytelling, "easter_eggs")
        assert hasattr(self.storytelling, "dynamic_events")
        assert hasattr(self.storytelling, "lore_fragments")
        assert hasattr(self.storytelling, "player_journals")

    def test_get_available_choices(self):
        """Test de récupération des choix disponibles"""
        player_id = "test_player"
        story_arc = "test_arc"
        choices = self.storytelling.get_available_choices(player_id, story_arc)

        assert isinstance(choices, list)

    def test_record_player_choice(self):
        """Test d'enregistrement d'un choix de joueur"""
        player_id = "test_player"
        choice = "test_choice"
        story_arc = "test_arc"

        result = self.storytelling.record_player_choice(player_id, choice, story_arc)

        assert isinstance(result, dict)

    def test_get_story_progress(self):
        """Test de récupération du progrès de l'histoire"""
        player_id = "test_player"
        progress = self.storytelling.get_story_progress(player_id)

        assert isinstance(progress, dict)

    def test_trigger_easter_egg(self):
        """Test de déclenchement d'un easter egg"""
        player_id = "test_player"
        egg_id = "test_egg"

        # D'abord ajouter l'easter egg avec la structure complète
        self.storytelling.easter_eggs[egg_id] = {
            "title": "Test Egg",
            "description": "Test description",
            "content": {"text": "Test content text", "rewards": []},
        }

        result = self.storytelling.trigger_easter_egg(player_id, egg_id)

        # La méthode ne retourne rien (None), donc on teste que ça ne plante pas
        assert result is None

    def test_check_easter_eggs(self):
        """Test de vérification des easter eggs"""
        player_id = "test_player"
        eggs = self.storytelling.check_easter_eggs(player_id)

        # La méthode peut retourner None, donc on teste ça
        assert eggs is None or isinstance(eggs, list)

    def test_lore_fragments_property(self):
        """Test de la propriété lore_fragments"""
        fragments = self.storytelling.lore_fragments

        assert isinstance(fragments, dict)

    def test_story_arcs_property(self):
        """Test de la propriété story_arcs"""
        arcs = self.storytelling.story_arcs

        assert isinstance(arcs, dict)

    def test_add_journal_entry(self):
        """Test d'ajout d'une entrée de journal"""
        player_id = "test_player"
        entry = {
            "timestamp": "2024-01-01",
            "content": "Test entry",
            "category": "adventure",
            "story_arc": "test_arc",
            "choice": "test_choice",
            "consequences": [],
        }

        result = self.storytelling.add_journal_entry(player_id, entry)

        # La méthode ne retourne rien (None), donc on teste que ça ne plante pas
        assert result is None

    def test_player_journals_property(self):
        """Test de la propriété player_journals"""
        journals = self.storytelling.player_journals

        assert isinstance(journals, dict)

    def test_create_dynamic_event(self):
        """Test de création d'un événement dynamique"""
        event_data = {
            "id": "test_event",
            "title": "Test Event",
            "description": "Test description",
        }

        result = self.storytelling.create_dynamic_event(event_data)

        assert isinstance(result, dict)

    def test_check_dynamic_events(self):
        """Test de vérification des événements dynamiques"""
        player_id = "test_player"
        events = self.storytelling.check_dynamic_events(player_id)

        assert isinstance(events, list)

    def test_evaluate_condition(self):
        """Test d'évaluation d'une condition"""
        condition = {"level": 1}
        player_data = {"level": 1, "experience": 100}
        choices = []

        result = self.storytelling.evaluate_condition(condition, player_data, choices)

        assert isinstance(result, bool)
