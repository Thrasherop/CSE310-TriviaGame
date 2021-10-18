from django.db import models
from api.custom_models.answer import Answer

class Question(models.Model):
    question = models.CharField(max_length=300)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE, default=[])
    scored = models.BooleanField(default=False)