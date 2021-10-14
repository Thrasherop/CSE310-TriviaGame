from django.urls import path 
from . import views


# URL config

# don't add '/' at the end of path to make it easy for the client (frontend) to send data through the query/params
### Ex) https://api-website.com/submit_scores?id=user_id --> '?id=' is the param and the 'user_id' is the key
urlpatterns = [ 
    path('hello_world', views.hello_world_endpoint),
    path('', views.server_home),
    path('login', views.post_login),
    path('submit_scores', views.submit_scores)
]




