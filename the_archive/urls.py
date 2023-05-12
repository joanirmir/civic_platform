# import django models/libraries
from django.urls import path

# import app modules
from . import views

urlpatterns = [
    path("", views.UploadListAPI.as_view(), name="api-list-view"),
    path("upload/", views.UploadAPI.as_view(), name="upload"),
    path("upload/<int:pk>", views.UploadModifyApi.as_view(), name="upload-mod"),
    path("upload/download/<int:pk>", views.UploadDownload.as_view(), name="upload-download"),
    path("upload/bookmark/create/", views.FileBookmarkCreate.as_view()),
    path("upload/bookmark/<int:pk>/", views.FileBookmarkDetail.as_view(), name="bookmark-view"),
    path("upload/comment/", views.CommentCreateApi.as_view()),
]
