from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def hello_world_endpoint(request):

    return HttpResponse('Hello world. This is a simple endpoint')

    



