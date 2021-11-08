from django.db import models
from api.custom_models.question import Question
# from api.custom_models.user import User

class Game:

    def __init__(self, score=0, questions=[]):
        self.score = score
        self.questions = questions

    def get_score(self):
        return self.score

    def get_questions(self):
        for q in self.questions:
            return q
    
    def to_dict(self):
        dest = {
            'score': self.score,
            'questions': self.questions
        }


        return dest

    def __repr__(self):
        return(
            f'Game(\
                score={self.get_score()}, \
                questions={self.get_questions()}, \
            )'
        )


    # score = models.IntegerField()
    # questions = []
    
    # # score = models.IntegerField()
    # # user = models.ForeignKey(User, on_delete=models.CASCADE)