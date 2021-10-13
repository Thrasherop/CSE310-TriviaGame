from django.urls import path 
from . import views


# URL config
urlpatterns = [ 
    path('hello_world/', views.hello_world_endpoint)
]




