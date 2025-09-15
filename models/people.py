from __future__ import annotations
from typing import List
from models.film import Film
from models.starship import Starship
from models.vehicle import Vehicle
from client.resource import ApiResource
import re
from models.errors import ErrorParameterNotValid

class People(ApiResource):
    def __init__(self, name:str, homeworld:List[str], films:List[Film],
                 starships:List[Starship], vehicles:List[Vehicle]):
        self._name = name
        self._homeworld = homeworld
        self._films = films
        self._starships = starships
        self._vehicles = vehicles
    @classmethod
    def from_api_response(cls, data:dict) -> People:
        from client.client import StarWarsCallApi
        starships = StarWarsCallApi.fetch_by_url(tuple(data["starships"]),Starship)
        films = StarWarsCallApi.fetch_by_url(tuple(data["films"]),Film)
        vehicles = StarWarsCallApi.fetch_by_url(tuple(data["vehicles"]),Vehicle)
        planet = StarWarsCallApi.fetch_unique_planet(data["homeworld"])

        return cls(name=data["name"],homeworld=planet,films=films,
                   starships=starships,vehicles=vehicles)

    @classmethod
    def filter_by_character(cls,character_list:List[People], name_character:str)\
    -> People:
        clean_name_character = cls.validate_input(name_character)
        for character in character_list:
            if character._name.lower() == clean_name_character.lower():
                return character

        return None

    @classmethod
    def validate_input(cls,name_character:str) -> str:
        clean_name = name_character.strip()

        if not clean_name:
            raise ErrorParameterNotValid("The name can't be empty.")

        if not re.fullmatch(r"[A-Za-z0-9 \-]+", clean_name):
            raise ErrorParameterNotValid(
                f"Invalid name. Input: '{name_character}'"
            )

        if clean_name.isdigit():
            raise ErrorParameterNotValid(
                f"Invalid name. Numeric values are not permitted. "
                f"Input: '{name_character}'"
        )
        return clean_name

    @classmethod
    def from_api(cls, data_response:List[dict]) -> List[People]:
        return [cls.from_api_response(instance) for instance in data_response]

    @classmethod
    def get_character_names(cls, list_characters:List[People]) -> List[str]:
        all_characters_names=[]
        for character in list_characters:
            all_characters_names.append(character.name)

        return all_characters_names

    def is_from_planet(cls, name_planet:str) -> bool:
        name_planet = cls.validate_input(name_planet)
        if cls._homeworld.lower() == name_planet.lower():
            return True

    @property
    def name(self):
        return self._name

    def get_information(self, resources:List[str]) -> str:
        content = ""
        if resources:
            for resource in resources:
                content += "\n" +str(resource) + " "

        return content

    def __str__(self):
        return (f"CHARACTER: \n"
                f"Name : {self._name}\n"
                f"Homeworld : {self._homeworld}\n"
                f"Starship to pilot : {self.get_information(self._starships)}\n"
                f"Driven vehicles : {self.get_information(self._vehicles)}\n"
                f"Films that appear : {self.get_information(self._films)}")
