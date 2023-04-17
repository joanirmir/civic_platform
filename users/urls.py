# import django models/libraries
from django.urls import path

# import app modules
from . import views

urlpatterns = [
    path("register/", views.RegisterUserApiView.as_view(), name='register'),
    path("profile/", views.ProfileApiView.as_view(), name='logged-in-profile'),
    # path("profile/<int:pk>", views.profile, name='logged-in-profile'),
]