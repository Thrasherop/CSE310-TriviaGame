from django.db import models
# from api.custom_models.question import Question

class Answer(models.Model):

    def __init__(self, answer, is_correct=False):
        self.answer = answer
        self.is_correct = is_correct

    def get_answer(self):
        return self.answer

    def get_is_correct(self):
        return self.is_correct

    def to_dict(self):
        dest = {
            'answer': self.answer,
            'is_correct': self.is_correct
        }

        return dest

    def __repr__(self):
        return(
            f'Answer(\
                answer={self.get_answer()}, \
                is_correct={self.get_is_correct()}, \
            )'
        )

    # answer = models.CharField(max_length=300)
    # is_correct = models.BooleanField()

    # answer = models.CharField(max_length=300)
    # is_correct = models.BooleanField()
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)