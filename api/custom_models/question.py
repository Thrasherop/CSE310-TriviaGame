from django.db import models
from api.custom_models.answer import Answer
# from api.custom_models.game import Game

class Question(models.Model):
    question = models.CharField(max_length=300)
    # answers = models.ManyToManyField(Answer)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE, default=[])
    scored = models.BooleanField(default=False)

    # question = models.CharField(max_length=300)
    # scored = models.BooleanField(default=False)
    # game = models.ForeignKey(Game, on_delete=models.CASCADE)
