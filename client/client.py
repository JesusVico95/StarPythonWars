import requests
import logging
from typing import Type
from functools import cache
from models.errors import ErrorParameterNotValid, ErrorUrlInvalid
from models.errors import ErrorNegativeNumber, ErrorToParse
from typing import List
from client.resource import ApiResource
from client.url import Url

class StarWarsCallApi(ApiResource):
    api_endpoints = {
        "planets":"planets",
        "starships":"starships",
        "people":"people",
        "films":"films",
        "vehicles":"vehicles",
    }

    @cache
    def create_connection(self, resource_name:str, number_page:int):
        validate_number = self.validate_page_number(number_page)

        if not isinstance(resource_name,str):
            raise ErrorParameterNotValid(f"Parameter 'resource_name' is "
                                         f"invalid. Expected str, got "
                                         f"{type(resource_name).__name__}")

        if resource_name not in StarWarsCallApi.api_endpoints:
            raise ErrorParameterNotValid(f"The paramater 'resource_name"
                                         " not contains in apiEndpoints")

        fetch_data = requests.get(f"{Url.GENERIC_URL}{resource_name}/?page="
                                       f"{validate_number}")

        if fetch_data.status_code != 200:
            raise ErrorUrlInvalid(f"We have a problem with {resource_name}."
                       "Is not a correct endpoint")


        response_data = fetch_data.json()

        return response_data

    def validate_page_number(self, number_page:int)-> int:
        if not isinstance(number_page,int):
            raise ErrorParameterNotValid(f"Parameter 'number_page' is invalid"
            f"Expected int, got {type(number_page).__name__}")
        if number_page <= 0:
            raise ErrorNegativeNumber(f"Number can't be below or equals to 0")

        return number_page

    def get_all_information(self, resource_name:str) -> List[dict]:
        page = 1
        has_next_page = True
        results  = []

        while has_next_page:
            try:
                get_initial_response = self.create_connection(resource_name
                                                                , page)
                results.extend(get_initial_response["results"])
                if get_initial_response["next"] is None:
                   has_next_page = False
                page += 1

            except ErrorUrlInvalid as e:
                logging.error(f"{e}")
            except ErrorParameterNotValid as e:
                logging.error(f"{e}")

        return results

    @classmethod
    @cache
    def fetch_by_url(cls, urls:tuple[str], model_class: Type[ApiResource],
                     timeout: float = 10.0) -> List[ApiResource]:
        list_instances=[]
        for url in urls:
            try:
                request = requests.get(url,timeout=timeout)
                request.raise_for_status()
            except requests.RequestException as err:
                logging.error(f"HTTP Error: {err}")

            try:
                response = request.json()
            except ValueError as err:
                logging.error(f"Invalid JSON: {err}")

            try:
                instance = model_class.from_api_response(response)
            except ErrorToParse as err:
                logging.error(f"Fail parse: {err}")

            list_instances.append(instance)

        return list_instances

    def from_api_response():
        pass

