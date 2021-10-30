from django.db import models
# from api.custom_models.question import Question

class Answer(models.Model):
    answer = models.CharField(max_length=300)
    is_correct = models.BooleanField()

    # answer = models.CharField(max_length=300)
    # is_correct = models.BooleanField()
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)