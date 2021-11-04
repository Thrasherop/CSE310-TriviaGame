from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from api.custom_models.user import User

from fb import get_users, initialize_firestore, post_user


# Create your views here / controllers to handle the logic of the req and handle the interact with the db

def hello_world_endpoint(request):
    return HttpResponse('Hello world. This is a simple endpoint.')

def server_home(request):
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
    
    # you will then set that to a response variable, which will return a response object, 
    # that will have a response['status'] key, if 200 == success, 400 == error
    # send that response JsonResponse(response)
    return JsonResponse(response)

def submit_scores(request):
    return HttpResponse('The path to submit user\'s game scores.')
