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

# get all users in db
def get_users():
    # this returns an array of documents
    results = users_ref.get()
    return results

# get user data with user_id as a string passed in
def get_user(user_id):
    # this returns an object
    userToReturn = users_ref.document(user_id).get()
    # convert the object to a python dict and return it
    return userToReturn.to_dict()

# signin a user to the db
def post_login_user(email, password):
    # again, authenticate to make sure there is an email and password
    # search through every user to make sure email exists

    # set return object
    returnDict = {'message': "", 'status': None}

    #### if there is an email match, using the returnDict={} send back a status of 200, with any message 'Success' or something
    #### if there is not an email, using the returnDict={}, with a status of 400 and message saying the email doens't exist, sign up pls

    return returnDict

# write a user to the database, signup a user
def post_user(first_name, last_name, email, password):
    # generate user object from User model with data being passed in
    user = User(first_name=first_name, last_name=last_name,
                email=email, password=password)
    # convert django model to dictionary
    d = user.to_dict(0)

    # set return object
    returnDict = {'message': "", 'status': None}

    # write to db
    try:
        # send user dictionary to write to db
        users_ref.add(d)
        # return message and status
        returnDict["message"] = "Success"
        returnDict["status"] = 200
    except Exception as e:
        # if fails, set returnDict to failure and return
        returnDict["message"] = str(e)
        returnDict["status"] = 400
    finally:
        # finally return dict
        return returnDict

# delete user by user_id
def delete_user(user_id):
    pass

# get all games, with user_id passed in
def get_games(user_id):
    results = games_ref.get()
    return results

# get game, with game_id passed in
def get_game(game_id):
    # this returns an object
    gameToReturn = games_ref.document(game_id).get()
    # convert the object to a python dict and return it
    return gameToReturn.to_dict()

# write a game to the db
# score: int
# game is an Array
### with --> question: string, scored: boolean, answers: Array
####### with --> answer: string, is_correct: boolean
def post_game(user_id, score, game):
    # create empty list of answerIds and questionIds
    answerIdList = list()
    questionIdList = list()

    # for each dictionary in the game array
    for game_feature in game:
        # make sure the answerIdList is empty each time it loops through
        answerIdList = []

        # create answer object for each answer, 4 answers per question
        for i, answerList in enumerate(game_feature['answers']):
            ansObj = Answer(answer=answerList['answer'], is_correct=answerList['is_correct'])
            # write the answer to the database, return back the id of the answer
            answerId = _write_answer(ansObj.to_dict())
             # append the id to list
            answerIdList.append(answerId)

        # after creating 4 answer objects, create a question object for each question
        # Create Question Object
        question = Question(question=game_feature['question'], scored=game_feature['scored'], answers=answerIdList)
        # for ans in question.answers:
        #     print(ans)
        # write the question to the database, return back the id of the question
        questionObjId = _write_question(question.to_dict())
        # append the id to list
        questionIdList.append(questionObjId)

    # create game obj
    game = Game(score=score, questions=questionIdList)
    # write the game to the database, return back the id of the game
    gameId = _write_game(game.to_dict())

    # now we need to append the gameId to the games array stored in the user object
    # create empty dictionary for return purposes
    returnDict = {}
    try:
        # get the user by it's user_id
        fetchedUser = get_user(user_id)
        # append the new gameId to the games field in the user
        fetchedUser['games'].append(gameId)
        # update that user by it's id
        users_ref.document(user_id).update(fetchedUser)
        # update return dictionary
        returnDict["message"] = "Success"
        returnDict["status"] = 200
    except:
        # if fails, set returnDict to failure and return
        returnDict["message"] = str(e)
        returnDict["status"] = 400
    finally:
        # return the dictionary to let the user know if failed or succeeded
        return returnDict


def delete_game(user_id, game_id):
    # get the user so we can delete the game from the games array within the user
    fetchedUser = get_user(user_id)

    # set return object
    returnDict = {'message': "", 'status': None}

    # get the game to delete
    game_to_delete = games_ref.document(game_id).get().to_dict()

    # if the game_id being passed in isn't a valid game id, meaning game_to_delete returns back null
    if game_to_delete == None:
        returnDict["message"] = "Must be a valid game id."
        returnDict["status"] = 400
        return returnDict

    # create new array variable to pass in
    newGamesList = list()

    # loop through the array of games and find the game that matches the game_id
    for gameId in fetchedUser['games']:
        # if found, pop out that game_id of the list
        if gameId == game_id:
            removedGame = fetchedUser['games'].remove(game_id)
        # if not found, append that gameId to new array to update db later
        else:
            newGamesList.append(str(gameId))

    # update user in db
    users_ref.document(user_id).update({u'games': newGamesList})

    # delete the questions that were part of that game
    for questionId in game_to_delete['questions']:
        if questionId != None:
            # store question ref
            question_to_delete = questions_ref.document(questionId).get().to_dict()

            # delete each answer for that question
            for answerId in question_to_delete['answers']:
                if answerId != None:
                    answers_ref.document(answerId).delete()

            # find that question in the db and delete it
            questions_ref.document(questionId).delete()

    # write to db
    try:
        # delete game
        games_ref.document(game_id).delete()
        # return message and status
        returnDict["message"] = "Success"
        returnDict["status"] = 200
    except Exception as e:
        # if fails, set returnDict to failure and return
        returnDict["message"] = str(e)
        returnDict["status"] = 400
    finally:
        # finally return dict
        return returnDict



## PRVIATE METHODS
## ONLY USE THESE METHODS WITHIN THIS FILE

# write an answer to the firebase db and return back the id of the answer
def _write_answer(ansObj):
    docRef = answers_ref.add(ansObj)
    # return id of answer document
    return docRef[1].id
    # return answers_ref.document(docRef[1].id)

# write a question to the firebase db and return back the id of the question
def _write_question(questionObj):
    docRef = questions_ref.add(questionObj)
    # return id of question document
    return docRef[1].id

# write a game to the db and return back the id of the game
def _write_game(gameObj):
    docRef = games_ref.add(gameObj)
    return docRef[1].id