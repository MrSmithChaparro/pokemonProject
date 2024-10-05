from django.urls import path
from .views import PokemonListView, PokemonDetailView

urlpatterns = [
    path('pokemons/', PokemonListView.as_view(), name=PokemonListView.name),
    path('pokemons/<int:pk>/', PokemonDetailView.as_view(), name=PokemonDetailView.name),
]