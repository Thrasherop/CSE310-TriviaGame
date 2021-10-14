from django.shortcuts import render
from django.http import HttpResponse

from fb import get_users, initialize_firestore, initialize_firestore, post_user


# Create your views here / controllers to handle the logic of the req and handle the interact with the db

def hello_world_endpoint(request):
    return HttpResponse('Hello world. This is a simple endpoint.')

def server_home(request):
    post_user('Last', 'Test', 'sup@gmail.com', 'testpw')
    userDocRef = get_users()
    print(userDocRef[0].to_dict())
    return HttpResponse('The path the admin/user will use to login.')
    


def post_login(request):
    return HttpResponse('The path the admin/user will use to login.')

def submit_scores(request):
    return HttpResponse('The path to submit user\'s game scores.')

    



# import pyrebase
# config = {
#   "apiKey": "AIzaSyAkOMvXq-Uxhds1GwoWmWkKpkXRNqMcVPM",
#   "authDomain": "cse310-triviagame.firebaseapp.com",
#   "databaseURL": "https://cse310-triviagame-default-rtdb.firebaseio.com",
#   "projectId": "cse310-triviagame",
#   "storageBucket": "cse310-triviagame.appspot.com",
#   "messagingSenderId": "732277971447",
#   "appId": "1:732277971447:web:0903fa9fdfe74003e336f2",
#   "measurementId": "G-NW6WL46ZPR"
# }

# firebase=pyrebase.initialize_app(config)
# authe=firebase.auth()
# database=firebase.database()

# def server_home(request):
#     channel_name = database.child('Data').child('Name').get().val()
#     subscribers = database.child('Data').child('Subscribers').get().val()
#     channel_type = database.child('Data').child('Type').get().val()
#     print(channel_name, channel_type, subscribers)
#     return HttpResponse('Channen Name', channel_name)