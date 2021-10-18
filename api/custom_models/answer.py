from django.db import models
class Answer(models.Model):
    answer = models.CharField(max_length=300)
    is_correct = models.BooleanField()