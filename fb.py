import firebase_admin
from firebase_admin import credentials, firestore
import os
from django.forms.models import model_to_dict
from api.custom_models.user import User
from api.custom_models.game import Game
from api.custom_models.question import Question
from api.custom_models.answer import Answer

# firebase/firestore credentials and initiation
cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# references to use for each collection
users_ref = db.collection(u"users")
games_ref = db.collection(u"games")
questions_ref = db.collection(u"questions")
answers_ref = db.collection(u"answers")

# this method automatically runs once on first run, so no need to worry about initiating it ourselves
def initialize_firestore():
    ''' Create Database Connection '''
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./ServiceAccountKey.json"
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'cse310-triviagame'
    })

    ''' Get reference to the db '''
    db = firestore.client()
    return db

####
####
####

# COLLECTION <---> DB Controllers/Methods

# user collection
def get_users():
    results = users_ref.get()
    return results

def post_user(first_name, last_name, email, password):
    user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    # ISSUES: Django models do not return as dictionaries. You need to give firebase a proper dictionary or object, not a django object.
    # ISSUE: I was not able to figure out a way to convert a django object to a python dictionary without it generating an 'id' key with a 'null' value.
    # WHAT NEEDS TO HAPPEN: We need to figure out how to convert a django object/model to a python dictionary without it adding it's own key:value
    # TEMPORARY SOLUTION: We use model_to_dict(), but again, we don't want it to generate an id key:value because firebase automatically does that
    d = model_to_dict(user)
    del d['id']
    users_ref.add(model_to_dict(d))


# game #collection
def get_games():
    results = games_ref.get()
    return results

# question collection
def get_questions():
    results = db.collection("questions").get()
    return results

# answer collection
def get_answers(question_id):
    # Need to get pass in the correct question id to get the proper question, if this is even a method we need?
    results = db.collection("answers").get()
    return results