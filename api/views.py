from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from api.custom_models.user import User

from fb import get_users, initialize_firestore, post_user


# Create your views here / controllers to handle the logic of the req and handle the interact with the db

def hello_world_endpoint(request):
    return HttpResponse('Hello world. This is a simple endpoint.')

def server_home(request):
    ## users is an array/list of documents
    usersList = get_users()
    for user in usersList:
        print(user.to_dict())
    return HttpResponse('Home page')

def post_signup(request):
    ## creating variables from the POST req body
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirmPassword = request.POST['confirm_password']

    ## make sure the email doesn't already exists
    ## get all users
    usersList = get_users()
    ## see if the user email matches ANY other email in the db
    for user in usersList:
        # convert user to dict
        u = user.to_dict()
        if email == u['email']:
            return JsonResponse({"message": 'Email already exists.', "status": 400})
    
    ## make sure passwords match
    if password != confirmPassword:
        return JsonResponse({'message': 'Passwords do not match.', "status": 400})

    ## write this user object to the firebase db
    ## get a response from the fb.py post_user function
    response = post_user(first_name, last_name, email, password)

    # based on that response, we return a status of 200 for success, or 400 for fail | all in JSON
    return JsonResponse(response)

def post_login(request):
    post_user('Last', 'Test', 'sup@gmail.com', 'testpw')
    userDocRef = get_users()
    print(userDocRef[0].to_dict())
    return HttpResponse('The path the admin/user will use to login.')

def submit_scores(request):
    return HttpResponse('The path to submit user\'s game scores.')
