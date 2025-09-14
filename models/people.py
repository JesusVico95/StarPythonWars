from __future__ import annotations
from typing import List
from models.film import Film
from models.starship import Starship
from models.vehicle import Vehicle
from models.planet import Planet
from client.resource import ApiResource

class People(ApiResource):
    def __init__(self, name:str, homeworld:List[str], films:List[Film],
                 starships:List[Starship], vehicles:List[Vehicle]):
        self._name = name
        self._homeworld = homeworld
        self._films = films
        self._starships = starships
        self._vehicles = vehicles

    @classmethod
    def from_api_response(cls, data:dict):
        from client.client import StarWarsCallApi
        starships = StarWarsCallApi.fetch_by_url(data["starships"],Starship)
        films = StarWarsCallApi.fetch_by_url(data["films"],Film)
        vehicles = StarWarsCallApi.fetch_by_url(data["vehicles"],Vehicle)
        planet = StarWarsCallApi.fetch_unique_planet(data["homeworld"])

        return cls(name=data["name"],homeworld=planet,films=films,
                   starships=starships,vehicles=vehicles)


    def from_api(self):
        from client.client import StarWarsCallApi
        date = StarWarsCallApi()
        data = date.get_all_information(date.api_endpoints["people"])
        return [self.from_api_response(instance) for instance in data]


    def get_character_names(self):
        all_characters_names=[]
        characters = self.from_api()
        for character in characters:
            all_characters_names.append(character.name)

        return all_characters_names

    def is_from_planet(self, name_planet:str):
        return self._homeworld == name_planet
    @property
    def name(self):
        return self._name

    def get_information(self, resources:List[str]):
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
