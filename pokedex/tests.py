import json
from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse
from .models import Pokemon
from .pokemon_logic import PokemonLogic


class PokemonViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.pokemon = Pokemon.objects.create(
            pokedex_number=1,
            name="bulbasaur",
            abilities={"ability": "overgrow"},
            sprites={"front_default": "url_to_sprite"},
            types={"type": "grass"}
        )

    def test_pokemon_list_view(self):
        """Test the pokemon list view and paginate of 12 items"""
        url = reverse('pokemon-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 12)

    def test_pokemon_detail_view(self):
        """Test the pokemon detail return the correct data in DB"""
        url = reverse('pokemon-detail', args=[self.pokemon.pokedex_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], self.pokemon.name)
        self.assertEqual(response.json()['abilities'], self.pokemon.abilities)
        self.assertEqual(response.json()['sprites'], self.pokemon.sprites)
        self.assertEqual(response.json()['types'], self.pokemon.types)

    def test_pokemon_detail_view_not_found(self):
        url = reverse('pokemon-detail', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_pokemon_update_view(self):
        """Test the pokemon update in the DB"""
        url = reverse('pokemon-detail', args=[self.pokemon.pokedex_number])
        data = {
            "name": "ivysaur"
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "ivysaur")

    @patch('pokedex.pokemon_logic.requests.get')
    def test_data_api_fallback_to_db(self, mock_get):
        """Test the data_api method when the API of pokemon is down return the data from the DB"""
        mock_get.return_value.status_code = 500

        pokemons_logic = PokemonLogic()
        data = pokemons_logic.data_api()

        # Verify that the data is fetched from the database
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].name, "bulbasaur")

    @patch('pokedex.pokemon_logic.requests.get')
    def test_pokemon_detail_view_create_if_not_exists(self, mock_get):
        """Test that a Pokemon is created in the database if it does not exist"""
        # Simulate a successful API response with Pokemon details
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 99999,
            "name": "mewtwo",
            "abilities": {"ability": "pressure"},
            "sprites": {"front_default": "url_to_mewtwo_sprite"},
            "types": {"type": "psychic"}
        }

        url = reverse('pokemon-detail', args=[99999])

        # Send a PUT request to create the Pokémon
        put_data = {
            "pokedex_number": 99999,
            "name": "mewtwo",
            "abilities": {"ability": "pressure"},
            "sprites": {"front_default": "url_to_mewtwo_sprite"},
            "types": {"type": "psychic"}
        }
        put_response = self.client.put(url, data=json.dumps(put_data), content_type='application/json')
        self.assertEqual(put_response.status_code, 201)

        # Send a GET request to verify the Pokémon was created
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, 200)

        # Verify that the Pokémon is created in the database
        pokemon = Pokemon.objects.get(pokedex_number=99999)
        self.assertEqual(pokemon.name, "mewtwo")
        self.assertEqual(pokemon.abilities, {"ability": "pressure"})
        self.assertEqual(pokemon.sprites, {"front_default": "url_to_mewtwo_sprite"})
        self.assertEqual(pokemon.types, {"type": "psychic"})
