from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import conf
from api.custom_models.user import User
import random

from fb import get_users, initialize_firestore, post_user, get_user, get_game, post_game, delete_game, post_login_user, delete_user
from api.custom_models.game import Game
from api.custom_models.question import Question
from api.custom_models.answer import Answer



import requests
import traceback
import json


# Create your views here / controllers to handle the logic of the req and handle the interact with the db

def hello_world_endpoint(request):
    return HttpResponse('Hello world. This is a simple endpoint.')

## SAVE THIS FOR REFERENCE... WHEN SAVING A GAME TO THE DB, THE GAME NEEDS TO LOOK LIKE THIS
model_game = [
        {    
            'question': 'Where did LeBron go to college?', 
            'answers': [ 
                {'answer': 'Errwhere', 'is_correct': False}, 
                {'answer': 'Nowhere', 'is_correct': True},
                {'answer': 'Tennessee', 'is_correct': False}, 
                {'answer': 'Akron', 'is_correct': False}, 
            ], 
            'scored': True
        },
        {    
            'question': 'Who leads the NBA in points?', 
            'answers': [ 
                {'answer': 'Hakeem', 'is_correct': True}, 
                {'answer': 'Kobe', 'is_correct': False},
                {'answer': 'Michael Jordan', 'is_correct': False}, 
                {'answer': 'Charles Barkley', 'is_correct': False}, 
            ],
            'scored': False
        }
    ]

def server_home(request):
    # dataObj = Dict()

    data = {
        "typing": "This is the statement"
    }

    return render(request, 'home/homescreen.html', data)
    
    # return render(request, 'game/gameplay.html', dataObj)

    # check if there is a cookie
    # if there is a cookie, validate it
    # if not, redirect to login page

def post_game_played(request):  
    # create variables from the POST req body
    user_id = request.POST['user_id']
    game_score = request.POST['score']
    game_played = request.POST['game']

    # write this game object to the firebase db
    # must pass in the user_id as STRING, game score as INT/Number, and the game object (reference model_game)
    dbResponse = post_game(user_id, game_score, game_played)
    return JsonResponse(dbResponse)

def post_signup(request):
    # create returnDict, just in case there is an error
    returnDict = {}

    # creating variables from the POST req body
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirmPassword = request.POST['confirm_password']


    if not first_name or not last_name or not email or not password or not confirmPassword:
        returnDict['message'] = 'Form not filled out correctly'
        returnDict['status'] = 400
        return render(request, 'home/homescreen.html', returnDict)

    # make sure the email doesn't already exists
    # get all users
    usersList = get_users()
    # see if the user email matches ANY other email in the db
    for user in usersList:
        # convert user to dict
        u = user.to_dict()
        if email == u['email']:
            return JsonResponse({"message": 'Email already exists.', "status": 400})

    # make sure passwords match
    if password != confirmPassword:
        return JsonResponse({'message': 'Passwords do not match.', "status": 400})

    # write this user object to the firebase db
    # get a response from the fb.py post_user function
    response = post_user(first_name, last_name, email, password)

    # based on that response, we return a status of 200 for success, or 400 for fail | all in JSON
    return JsonResponse(response)


def post_login(request):
    # create variables for user and password from the POST request body
    email = request.POST['email']
    password = request.POST['password']

    # see if the request.POST['email'] & ['password'] aren't empty
    if not email:
        return JsonResponse({"message": 'email field must have data', "status": 400})
    if not password:
        return JsonResponse({"message": 'password field must have data', "status": 400})

    # see if the email exists in the db by using the get_users() method and filtering through
    '''userDocRef = get_users()
    for user in userDocRef:
        u = user.to_dict()
        if email == u['email']:
            return JsonResponse({"message": 'Your email exists :)', "status": 200})'''

    # send email and password to post_login_user() from fb.py, make sure to import that function. 
    # You might get an error but it's because your code isn't merged with the latest code
    response = post_login_user(email, password)
    # user_token_cookie_status = _set_cookie("user_token", response['user_id'])
    # user_id_cookie_status = _set_cookie("user_id", response['user_id'])
    # _hash_user_token_cookie_status, response['user_id'])
    # return JsonResponse({"message":"Sucessfull login", "status": 200})
    # get user_token_cookie_status and sompare it to the validate

   






    
    # you will then set that to a response variable, which will return a response object, 
    # that will have a response['status'] key, if 200 == success, 400 == error
    # send that response JsonResponse(response)
    return JsonResponse(response)

def post_generate_game(request):


    """

        Generates a game from the trivia API
        IT returns this game data as a JSON object


        There are optional post parameters:
            difficulty: easy, medium, hard (easy default)
            amount: how many questions to return (10 default)
            category: a specific category to return questions from (any default)
            type: multiple, true or false (multiple default)
            

        The request to trivia looks like this:
        # https://opentdb.com/api.php?amount=10&category=9&difficulty=medium&type=multiple&encode=url3986

        return:
            A JsonResponse object with the following keys:
                status: 200 for success, 400 for error
                questions: an array of questions
                    [
                        {question: question string,
                        answers: [
                            {answer: answer string, is_correct: boolean}
                        ]}.

                    ]
        

    """

    try:

        # Initilizes the api query string
        api_query = 'https://opentdb.com/api.php?'


        # Sets up the api_query string with the the different params
        # It does this by appending the value immediately after checking
        # the requests key

        if not 'amount' in request.POST:
            #amount = 10
            api_query += 'amount=10&'
        else:
            #amount = request.POST['amount']
            api_query += 'amount=' + request.POST['amount'] + '&'

        if not 'category' in request.POST:
            pass 
        else:
            api_query += 'category=' + request.POST['category'] + '&'

        if not 'difficulty' in request.POST:
            api_query += 'difficulty=easy&'
        else:
            api_query += 'difficulty=' + request.POST['difficulty'] + '&'

        if not 'type' in request.POST:
            api_query += 'type=multiple&'
        else:
            api_query += 'type=' + request.POST['type'] + '&'
    
        data = requests.get(api_query).json()


        # checks if the data response code is not 0 (success). If its not 0, then it returns an error
        if data['response_code'] != 0:
            return JsonResponse({'status': 400, 'message': 'There was an error with the request'})


        # # Gets results from the data
        raw_results = data['results']

        all_questions = []

        # Creates all the question arrays
        for result in raw_results:

            question = result['question']
            correct_answer = result['correct_answer']
            incorrect_answers = result['incorrect_answers']

            all_answers = []

            for answer in incorrect_answers:
                answers = {
                    'answer': answer,
                    'is_correct': False
                }

                # Creates the answer obj
                answer = Answer(answer, False)
                

                all_answers.append(answer.to_dict())

            # Adds the correct answer
            correct_answer = {
                'answer': correct_answer,
                'is_correct': True
            }

            # Creates the correct answer obj and appends it to the all_answers array
            correct_answer = Answer(correct_answer['answer'], True)
            all_answers.append(correct_answer.to_dict())


            question = Question(question=question, answers = all_answers)
            all_questions.append(question.to_dict())

        # Creates the game object
        game = Game(0, all_questions)

        return_map = game.to_dict() 
        return_map['status'] = 200


        return JsonResponse(return_map)


    except Exception as e:
        print("Failed to return on post_generate_answer(): " )
        traceback.print_exc()
        print("returning status 500")
        return JsonResponse({'status': 500, 'message': 'There was an internal error'})


def submit_scores(request):
    return HttpResponse('The path to submit user\'s game scores.')

## PRIVATE HELPER FUNCTIONS
def _set_cookie(key, user_id):
    
    responseObj ={}

    try:
        token = _generate_token(user_id)
        key.set_cookie(key, token)
         
        responseObj["status"] = 200
        responseObj["message"] = "Cookie set!"
        return responseObj
        
    except:

        responseObj["status"] = 400
        responseObj["message"] = "Cookie failed to set..."
        return responseObj

def _generate_token(user_id):
    token = (user_id + "0000")
    return token
    


def _get_cookie(cookie_key, request):
    responseObj = {}
    token = request.COOKIES[cookie_key]
    
    if token is None:
        responseObj["message"] = "cookie does not exist"
        responseObj["status"] = 400
        return responseObj
    
    user_id = _hash_token(token)

    responseObj["cookie_value"] = token
    return responseObj

def _hash_token(token):

    responseObj = {}

    
    if token is None:
        responseObj["message"] = "must pass in a token"
        responseObj["status"] = 400
        return responseObj

    token_length = len(token)
    user_id = token.rstrip(token[-4])

    #print(user_id)

    responseObj["hashed_user_id"] = user_id
    return responseObj
    
    
 




    

