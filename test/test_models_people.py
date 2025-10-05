import unittest
from models.people import People
from unittest.mock import patch
class TestWarsPeople(unittest.TestCase):

    def test_create_a_correct_people_from_api_response(self):
        test_response_about_character ={
            "name":"Luke Skywalker",
            "homeworld": "https://swapi.py4e.com/api/planets/1/",
            "films":([
                "https://swapi.py4e.com/api/films/2/",
		        "https://swapi.py4e.com/api/films/6/",
		        "https://swapi.py4e.com/api/films/3/",
		        "https://swapi.py4e.com/api/films/1/",
		        "https://swapi.py4e.com/api/films/7/"
            ]),
            "vehicles":([
                "https://swapi.py4e.com/api/vehicles/14/",
                "https://swapi.py4e.com/api/vehicles/30/"
            ]),
            "starships":([
                "https://swapi.py4e.com/api/starships/12/",
                "https://swapi.py4e.com/api/starships/22/"])
        }

        result = People.from_api_response(test_response_about_character)
        self.assertIsInstance(result, People)

    @patch('builtins.input', return_value= "Tatooine")
    def test_people_is_from_planet(self, mock_input):
        test_case = [
            (People(name="Luke Skywalker",
                               homeworld="Tatooine",
                               films=[],
                               starships=[],
                               vehicles=[]), True),
            (People(name="C-3PO",
                               homeworld="Unknown",
                               films=[],
                               starships=[],
                               vehicles=[]), False),
        ]


        for api_response, expected in test_case:
            with self.subTest(api_response = api_response):
                result = api_response.is_from_planet(mock_input.return_value)
                self.assertEqual(result, expected)
