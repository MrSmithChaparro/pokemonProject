from rest_framework import serializers

from pokedex.models import Pokemon


class PokemonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    url = serializers.URLField()

class PokemonSpritesSerializer(serializers.Serializer):
    back_default = serializers.CharField(required=False, allow_blank=True)
    back_female = serializers.CharField(required=False, allow_blank=True)
    back_shiny = serializers.CharField(required=False, allow_blank=True)
    back_shiny_female = serializers.CharField(required=False, allow_blank=True)
    front_default = serializers.CharField(required=False, allow_blank=True)
    front_female = serializers.CharField(required=False, allow_blank=True)
    front_shiny = serializers.CharField(required=False, allow_blank=True)
    front_shiny_female = serializers.CharField(required=False, allow_blank=True)


class PokemonDetailSerializer(serializers.Serializer):
    pokedex_number = serializers.IntegerField(source='id')
    name = serializers.CharField(max_length=100)
    abilities = serializers.JSONField()
    sprites = PokemonSpritesSerializer()
    types = serializers.JSONField()

class PokemonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ['pokedex_number', 'name', 'abilities', 'sprites', 'types']
