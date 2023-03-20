from django.shortcuts import render

from django.views.generic import ListView

from .models import User, Upload


def home(request):
    context = {"posts": Upload.objects.all()}
    return render(request, "the_archive/home.html", context)


def about(request):
    return render(request, "the_archive/about.html", {"title": "About"})


class UploadListView(ListView):
    model = Upload
    context_object_name = "list_of_uploads"
    template_name = "upload_list.html"
