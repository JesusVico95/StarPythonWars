
import unittest
from models.film import Film
class TestWarsFilm(unittest.TestCase):

    def test_create_a_correct_film(self):
        name = "A New Hope"
        episode_id = 4
        film = Film(title=name, episode=episode_id)
        self.assertIsInstance(film,Film)

    def test_from_api_response_create_a_film_(self):
        api_response = {
            "title": "A New Hope",
            "episode_id": 4,
        }
        film = Film.from_api_response(api_response)
        self.assertIsInstance(film,Film)
        self.assertEqual(film._title,"A New Hope")
        self.assertEqual(film._episode,4)

    def test_from_api_response_invalid_response(self):
        api_response = {"name": "A New Hope"}
        with self.assertRaises(KeyError):
            Film.from_api_response(api_response)

    def test_from_api_response_multiples_responses(self):
        test_cases = [
            ({"title":"A New Hope","episode_id":4},("A New Hope",4)),
            ({"title":"The Empire Strikes Back","episode_id":5},("The Empire Strikes Back",5)),
            ({"title":"Return of the Jedi","episode_id":6},("Return of the Jedi",6))
        ]

        for api_response, (expected_title, expected_episode) in test_cases:
            with self.subTest(api_response=api_response):
                film = Film.from_api_response(api_response)
                self.assertIsInstance(film, Film)
                self.assertEqual(film._title, expected_title)
                self.assertEqual(film._episode, expected_episode)
