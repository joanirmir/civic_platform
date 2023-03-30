from django.urls import path
from . import views
from the_archive.views import UploadListView, UploadDataView

urlpatterns = [
    path("", views.home, name="the_archive-home"),
    path("about/", views.about, name="the_archive-about"),
    path("archive/", UploadListView.as_view(), name="the_archive-list"),
    path("archive/upload/", UploadDataView.as_view(), name="the_archive-upload")
]
