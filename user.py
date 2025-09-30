import logging
from client.client import StarWarsCallApi
from models.people import People
from models.planet import Planet
from models.errors import ErrorParameterNotValid

if __name__ == "__main__":
    sw_api = StarWarsCallApi()
    get_information_planets = sw_api.get_all_information\
    (sw_api.api_endpoints["planets"])

    planets = Planet.parse_planets(get_information_planets)
    print("*** ALL PLANETS ***")
    for planet in planets:
        print(planet)
        print("-----")
    print("*** PLANETS FILTER BY DIAMETER ***")
    valid_planets = Planet.filter_by_diameter(planets)
    for planet in valid_planets:
        print(planet)
        print("-----")

    get_information_about_characters = sw_api.get_all_information\
        (sw_api.api_endpoints["people"])

    characters = People.from_api(get_information_about_characters)
    print("*** ALL CHARACTERS ***")
    only_character_names = []
    for character in characters:
        print(character)
        print("---------")

    print("*** SEARCH CHARACTERS BY UNIQUE PLANETS ***")
    try:
        name_planet = input("Introduce a planet: ")
        filter_characters_by_planets = [
            special_character for special_character in characters
            if special_character.is_from_planet(name_planet)
        ]

        if filter_characters_by_planets:
            for filtered_character in filter_characters_by_planets:
                print(filtered_character)
            print(f"Total characters from {name_planet} : "
                  f"{len(filter_characters_by_planets)}")
        else:
            print(f"Not found characters with {name_planet} planet")
    except ErrorParameterNotValid as err:
        logging.error(f"{err}")


    only_character_names = People.get_character_names(characters)
    print("*** ONLY ATTRIBUTE NAME ***")
    for only in only_character_names:
        print(only)

    try:
        valid_character = input("Introduce a name to want search: ")
        specific_character = People.filter_by_character\
            (characters,valid_character)
        if specific_character in characters:
            print(specific_character)
        else:
            print(f"Not found in API")
    except ErrorParameterNotValid as err:
        logging.error(f"{err}")




