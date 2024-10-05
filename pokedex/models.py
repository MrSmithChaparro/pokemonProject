from django.db import models

class Pokemon(models.Model):
    pokedex_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    abilities = models.JSONField()
    sprites = models.JSONField()
    types = models.JSONField()
