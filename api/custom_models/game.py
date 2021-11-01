from django.db import models
from api.custom_models.question import Question
# from api.custom_models.user import User

class Game(models.Model):
    score = models.IntegerField()
    questions = []
    
    # score = models.IntegerField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE)