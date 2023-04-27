# import django models/libraries
from django.urls import path

# import app modules
from . import views

urlpatterns = [
    path("", views.UploadListAPI.as_view(), name="api-list-view"),
    path("upload/", views.UploadAPI.as_view(), name="api-upload"),
    path("upload/<int:pk>", views.UploadModifyApi.as_view(), name="api-mod"),
]
