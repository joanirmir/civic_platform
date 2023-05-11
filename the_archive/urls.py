# import django models/libraries
from django.urls import path

# import app modules
from . import views

urlpatterns = [
    path("", views.UploadListAPI.as_view(), name="api-list-view"),
    path("upload/", views.UploadAPI.as_view(), name="upload"),
    path("upload/<int:pk>", views.UploadModifyApi.as_view(), name="upload-mod"),
    path("upload/download/<int:pk>", views.UploadDownload.as_view(), name="upload-download"),
    path("uploads/tags/", views.TagListAPI.as_view()),
    path("upload/tags/search/", views.TagListAPI.as_view(), name="archive-tags-list")
]
