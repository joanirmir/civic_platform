from django.urls import path
from . import views

# from the_archive.views import

urlpatterns = [
    # path("", views.home, name="the_archive-home"),
    # path("about/", views.about, name="the_archive-about"),
    path("", views.UploadListAPI.as_view(), name="api-list-view"),
    path("upload/", views.UploadAPI.as_view(), name="api-upload"),
    path("upload/<int:pk>", views.UploadModifyApi.as_view(), name="api-mod"),
]
