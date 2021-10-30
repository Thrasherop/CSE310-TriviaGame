from django.db import models
from api.custom_models.game import Game

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    games = models.ForeignKey(Game, on_delete=models.CASCADE, default=[])

    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=50)
    # email = models.CharField(max_length=300)
    # password = models.CharField(max_length=300)