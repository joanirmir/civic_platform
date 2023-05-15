# import django models/libraries
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


# import app modules
from . import views

urlpatterns = [
    path("register/", views.RegisterUserApiView.as_view(), name="register"),
    path("profile/<int:pk>", views.UserApiView.as_view(), name="logged-in-profile"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
