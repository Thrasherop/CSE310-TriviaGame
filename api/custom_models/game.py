from django.db import models
from api.custom_models.question import Question

class Game(models.Model):
    score = models.IntegerField()
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, default=[])

    