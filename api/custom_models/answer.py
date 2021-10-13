from django.db import models
class Answer(models.Model):
    id = models.IntegerField(primary_key=True)
    answer = models.CharField(max_length=300)
    is_correct = models.BooleanField()