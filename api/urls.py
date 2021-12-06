from django.urls import path 
from . import views


# URL config

# don't add '/' at the end of path to make it easy for the client (frontend) to send data through the query/params
### Ex) https://api-website.com/submit_scores?id=user_id --> '?id=' is the param and the 'user_id' is the key
urlpatterns = [ 
    path('hello_world', views.hello_world_endpoint),
    path('', views.server_home),
    path('signup', views.post_signup),
    path('login', views.post_login),
    path('homescreen', views.get_homescreen),
    path('submit_scores', views.submit_scores),
    path('generate_game', views.post_generate_game),
    path('profile', views.user),
    path('post-game', views.post_game_played),
]




