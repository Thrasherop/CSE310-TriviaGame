from django.db import models
from api.custom_models.answer import Answer
# from api.custom_models.game import Game

class Question():

    def __init__(self, question, scored=False, answers=[]):
        self.question = question
        self.scored = scored
        self.answers = answers

    def get_question(self):
        return self.question

    def get_scored(self):
        return self.scored

    def get_answers(self):
        for ans in self.answers:
            return ans

    def to_dict(self):
        dest = {
            'question': self.question,
            'scored': self.scored,
            'answers': self.answers
        }

        return dest

    def __repr__(self):
        return(
            f'Question(\
                question={self.get_question()}, \
                scored={self.get_scored()}, \
                answers={self.get_answers()}, \
            )'
        )

# class Question(models.Model):
#     question = models.CharField(max_length=300)
#     scored = models.BooleanField(default=False)
#     answers = []

#     def add_answers(self, answersList):
#         answers = answersList

    # question = models.CharField(max_length=300)
    # scored = models.BooleanField(default=False)
    # game = models.ForeignKey(Game, on_delete=models.CASCADE)
