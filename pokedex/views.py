from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Pokemon
from .serializer.pokemon import PokemonSerializer, PokemonDetailSerializer, PokemonModelSerializer
from .pokemon_logic import PokemonLogic, PokemonNotFoundException


class PokemonListView(APIView):
    name = 'pokemon-list'

    @staticmethod
    def get(request):
        """this method returns a list of pokemons"""
        pokemons_logic = PokemonLogic()
        paginator = PageNumberPagination()
        paginated_pokemons = paginator.paginate_queryset(pokemons_logic.data_api(), request)
        serializer = PokemonSerializer(paginated_pokemons, many=True)
        return paginator.get_paginated_response(serializer.data)


class PokemonDetailView(APIView):
    name = 'pokemon-detail'

    @staticmethod
    def get(request, pk):
        """this method returns the detail of a pokemon"""
        try:
            pokemon = Pokemon.objects.get(pokedex_number=pk)
            serializer = PokemonModelSerializer(pokemon)

        except Pokemon.DoesNotExist:
            pokemons_logic = PokemonLogic(pk)
            try:
                serializer = PokemonDetailSerializer(pokemons_logic.detail_pokemon())
            except PokemonNotFoundException:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        """this method updates a pokemon"""
        try:
            pokemon = Pokemon.objects.get(pokedex_number=pk)
        except Pokemon.DoesNotExist:
            pokemon = None
        if pokemon:
            serializer = PokemonModelSerializer(pokemon, data=request.data, partial=True)
        else:
            serializer = PokemonModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK if pokemon else status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
