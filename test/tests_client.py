import unittest
from typing import List
from unittest.mock import patch, Mock, call
from client.client import StarWarsCallApi
from models.errors import ErrorParameterNotValid, ErrorUrlInvalid, \
    ErrorNegativeNumber
import requests
import logging
from models.people import People
from models.starship import Starship
class TestStarWarsClientApi(unittest.TestCase):
    def test_is_a_valid_integer(self):
        number_page = 1
        sw_api = StarWarsCallApi()
        result = sw_api.validate_page_number(number_page)
        self.assertEqual(result,number_page)

    def test_is_a_invalid_number(self):
        number_page = 0
        sw_api = StarWarsCallApi()
        with self.assertRaises(ErrorNegativeNumber) as exc:
            sw_api.validate_page_number(number_page)
            self.assertIn(f"Parameter 'number_page' is invalid"
            f"Expected int, got {type(number_page).__name__}",str(exc.exception))

    def test_is_a_take_diferents_values(self):
        sw_api = StarWarsCallApi()
        invalid_parameters = [0,-1,"hello"]
        for number_page in invalid_parameters:
            with self.subTest(number_page = number_page):
                if isinstance(number_page, int) and number_page <= 0:
                    expected_exception = ErrorNegativeNumber
                else:
                    expected_exception = ErrorParameterNotValid

                with self.assertRaises(expected_exception):
                    sw_api.validate_page_number(number_page)

    def test_create_a_success_connection_mock(self):
        create = StarWarsCallApi()


        with patch("client.client.requests.get") as mock_get:

            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "count": 61,
                "results": [{"name": "X-wing"}, {"name": "TIE Fighter"}]
            }

            result = create.create_connection("starships", 1)
            mock_get.assert_called_with\
            ("https://swapi.py4e.com/api/starships/?page=1")

            self.assertEqual(result["count"], 61)
            self.assertEqual(len(result["results"]), 2)

    def test_error_parameter_to_create_connection(self):
        create = StarWarsCallApi()
        with self.assertRaises(ErrorParameterNotValid) as exc:
            create.create_connection("vehiccles",1)
            self.assertIn("The parameter 'resource_name' not contains in"
                          "apiEndpoints",str(exc.exception))

    def test_get_all_information_use_multiple_pages(self):
        first_response = Mock()
        first_response.status_code = 200
        first_response.json.return_value = {
            "results": [{"name": "CR90 corvette"}],
            "next":"https://swapi.py4e.com/api/starships/?page=2"
        }

        second_response = Mock()
        second_response.status_code = 200
        second_response.json.return_value = {
            "results": [{"name": "Slave 1"}],
            "next":None
        }
        create = StarWarsCallApi()
        with patch("client.client.requests.get",side_effect=[first_response,
            second_response]) as mock_get:

            mock_get.return_value.status_code = 200
            result = create.get_all_information("starships")
            mock_get.assert_has_calls([
                call("https://swapi.py4e.com/api/starships/?page=1"),
                call("https://swapi.py4e.com/api/starships/?page=2")
            ])
            self.assertEqual(result[0]["name"],"CR90 corvette")
            self.assertEqual(result[1]["name"],"Slave 1")
            self.assertEqual(mock_get.call_count,2)

    def test_timeout_fetch_by_url(self):
        urls = tuple(["https://swapi.py4e.com/api/people/?page=1",
                      "https://swapi.py4e.com/api/people/?page=2"])
        create = StarWarsCallApi()
        with patch("client.client.requests.get") as mock_get:
            mock_get.side_effect = requests.Timeout()
            with self.assertLogs(level="ERROR") as logs:

                result = create.fetch_by_url(urls,People,timeout= 0.001)

                found_error = any("HTTP Error" in message for message
                                  in logs.output)

                self.assertTrue(found_error)
                self.assertEqual(result,[None,None])
                self.assertEqual(mock_get.call_count,2)

    def test_invalid_json_response(self):
        starships_urls = tuple(["https://swapi.py4e.com/api/starships/?page=1",
                     "https://swapi.py4e.com/api/starships/?page=2"])
        create = StarWarsCallApi()
        with patch("client.client.requests.get") as mock_get:
            mock_get.side_effect = ValueError()
            with self.assertLogs(level="ERROR") as logs:
                result = create.fetch_by_url(starships_urls,Starship)

                found_error = any("Invalid JSON:" in message
                                  for message in logs.output)

                self.assertTrue(found_error)
                self.assertEqual(result,[None,None])
                self.assertEqual(mock_get.call_count,2)

    def test_obtains_correct_name_planet(self):
        name_planet = Mock()
        name_planet.status_code = 200
        name_planet.json.return_value = {
            "name": "Tatooine"
        }
        create = StarWarsCallApi()
        with patch("client.client.requests.get",side_effect=[name_planet])\
        as mock_get:
            result = create.fetch_unique_planet\
            ("https://swapi.py4e.com/api/planets/1/")

        self.assertEqual(result,"Tatooine")

