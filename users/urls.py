# import django models/libraries
from django.urls import path

# import app modules
from . import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("profile/", views.profile, name='profile'),
]
