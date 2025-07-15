from django.urls import path, include
from .views import *
urlpatterns = [
    path("login_user", login_user, name="login_user"),
    path("register_user", register_user, name="register_user"),
    path("logout_user", logout_user, name="logout_user"),
    path("schedule", schedule, name="schedule"),
    
    
]
