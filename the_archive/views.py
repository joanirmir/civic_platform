from django.shortcuts import render

# from .models import User, Upload

# def home(request):
#     context = {'posts': Upload.objects.all()}
#     return render(request, "the_archive/home.html", context)


def about(request):
    return render(request, "the_archive/about.html", {"title": "About"})
