import requests
from typing import List, Dict, Any

from pokedex.models import Pokemon


class PokemonNotFoundException(Exception):
    pass


class PokemonLogic:
    BASE_API_URL = "https://pokeapi.co/api/v2/pokemon"

    def __init__(self, id: int = None):
        self.id = id


    def data_api(self) -> list[Any]:
        """This method returns a list of pokemons from the API or the DB if the API is down"""
        response = requests.get(f'{self.BASE_API_URL}?limit=100000&offset=0')

        if response.status_code == 200:
            data = response.json()
            return [
                {
                    "name": pokemon["name"],
                    "url": f'http://localhost:8000/pokemons/{pokemon["url"].rstrip("/").split("/")[-1]}/'
                } for pokemon in data["results"]]
        else:
            pokemons = Pokemon.objects.all()
            return pokemons

    def detail_pokemon(self) -> dict[str, Any]:
        """This method returns the detail of a pokemon from the API"""
        response = requests.get(f'{self.BASE_API_URL}/{self.id}')

        if response.status_code == 200:
            return response.json()

        else:
            raise PokemonNotFoundException("Pokemon not found")