from __future__ import annotations
from typing import List
from models.film import Film
from client.resource import ApiResource
from models.errors import ErrorParameterNotValid
import logging
class Planet(ApiResource):
    def __init__(self, name:str = None, diameter:str = None,
                 list_of_films:List=None):
        self._name = name
        self._diameter = diameter
        self._list_of_films = list_of_films

    @staticmethod
    def parse_planets(response_about_planet:List[dict]):
        list_planets = []

        for planet in response_about_planet:
            planet = Planet.from_api_response(planet)
            list_planets.append(planet)

        return list_planets

    @classmethod
    def from_api_response(cls, planet:dict):
        from client.client import StarWarsCallApi
        film_names = StarWarsCallApi.fetch_by_url(tuple(planet["films"]),Film)

        planet = Planet(planet["name"],planet["diameter"],film_names)
        return planet

    @classmethod
    def filter_by_diameter(self, list_planets:List[Planet]) -> List[Planet]:
        planets_without_diameter_unknown:List[Planet] = []

        try:
            diameter = self.obtain_a_diameter(self)
        except ErrorParameterNotValid as e:
            logging.error(f"{e}")
            return []

        for planets in list_planets:
            if planets._diameter == "unknown":
                continue
            planets_without_diameter_unknown.append(planets)

        query = list(filter(lambda d: int(d._diameter) > diameter,
                            planets_without_diameter_unknown))

        return query

    def obtain_a_diameter(self):
            valid_number = True
            while valid_number:
                try:
                    diameter = int(input(f"Introduce a number between "
                    f"10.000 and 14.000: "))
                    if diameter >=10000 and diameter<= 14000:
                        valid_number = False
                        return diameter
                except ValueError as e:
                    raise ErrorParameterNotValid(f"The paramater 'diameter'"
                                                 f"must be integer")

    @property
    def name(self):
        return self._name
    @property
    def diameter(self):
        return self._diameter

    def __str__(self):
        films_text = ""
        if self._list_of_films:
            for film in self._list_of_films:
                films_text += "\n"+str(film) + " "

        return f"Name : {self._name}, Diameter : {self._diameter} {films_text}"
