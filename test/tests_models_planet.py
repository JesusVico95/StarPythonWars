import unittest
from models.planet import Planet
from unittest.mock import patch
class TestStarWarsPlanet(unittest.TestCase):

    def test_create_a_correct_planet(self):
        planet = Planet(name="Tatooine", diameter="14123",list_of_films=[])
        self.assertEqual(planet.name, "Tatooine")
        self.assertEqual(planet.diameter, "14123")
        self.assertEqual(planet._list_of_films, [])
        self.assertIsInstance(planet, Planet)

    def test_from_parse_planets(self):
        response_about_planet_test = [
            {
                "name": "Tatooine",
                "diameter": "10465",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/3/",
                    "https://swapi.dev/api/films/4/",
                    "https://swapi.dev/api/films/5/",
                    "https://swapi.dev/api/films/6/"
                ]
            },
            {
                "name": "Alderaan",
                "diameter": "12500",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/6/"
                ]
            }
        ]

        result = Planet.parse_planets(response_about_planet_test)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    @patch('builtins.input', return_value= 11000)
    def test_search_planet_by_diameter(self,mock_input):
        test_list_planets = [
            Planet(name="Tatooine", diameter="10465", list_of_films=[]),
            Planet(name="Alderaan", diameter="12500", list_of_films=[]),
            Planet(name="Yavin IV", diameter="unknown", list_of_films=[]),
            Planet(name="Hoth", diameter="7200", list_of_films=[])
        ]

        result = Planet.filter_by_diameter(test_list_planets)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
