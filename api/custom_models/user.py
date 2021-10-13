from django.db import models
from api.custom_models.game import Game

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    games = models.ForeignKey(Game, on_delete=models.CASCADE)