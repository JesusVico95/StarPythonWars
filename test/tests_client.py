import unittest
from unittest.mock import patch
from client.client import StarWarsCallApi
from models.errors import ErrorParameterNotValid, ErrorUrlInvalid, \
    ErrorNegativeNumber
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
        invalid_parameters = [0,-1,-10,"hello"]
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



