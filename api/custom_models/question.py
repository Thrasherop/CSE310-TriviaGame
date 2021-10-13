from django.db import models
from api.custom_models.answer import Answer

class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.CharField(max_length=300)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE)
    scored = models.BooleanField(default=False)