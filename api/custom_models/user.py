from django.db import models
from api.custom_models.game import Game

class User(models.Model):
    
    def __init__(self, first_name, last_name, email, password, games=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.games = games

    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    def get_games(self):
        for game in self.games:
            return game
    
    def to_dict(self):
        dest = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'games': self.games,
            'password': self.password
        }

        return dest

    def __repr__(self):
        return(
            f'Question(\
                first_name={self.get_first_name()}, \
                last_name={self.get_last_name()}, \
                email={self.get_email()}, \
                games={self.get_games()}, \
            )'
        )
    
    
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=50)
    # email = models.CharField(max_length=300)
    # password = models.CharField(max_length=300)
    # games = []

    
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=50)
    # email = models.CharField(max_length=300)
    # password = models.CharField(max_length=300)