from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from api.custom_models.user import User

from fb import get_users, initialize_firestore, post_user


# Create your views here / controllers to handle the logic of the req and handle the interact with the db

def hello_world_endpoint(request):
    return HttpResponse('Hello world. This is a simple endpoint.')

def server_home(request):
    return HttpResponse('Home page')

def post_signup(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']

    user = User(first_name, last_name, email, password)
    print(user)

    return HttpResponse(user)

def post_login(request):
    post_user('Last', 'Test', 'sup@gmail.com', 'testpw')
    userDocRef = get_users()
    print(userDocRef[0].to_dict())
    return HttpResponse('The path the admin/user will use to login.')

def submit_scores(request):
    return HttpResponse('The path to submit user\'s game scores.')
