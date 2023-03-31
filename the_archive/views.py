from django.shortcuts import render

from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import User, Upload, Location, Link
from .forms import UploadForm


def home(request):
    context = {"posts": Upload.objects.all()}
    return render(request, "the_archive/home.html", context)


def about(request):
    return render(request, "the_archive/about.html", {"title": "About"})


class UploadListView(ListView):
    model = Upload
    context_object_name = "list_of_uploads"
    template_name = "upload_list.html"


class UploadDataView(CreateView):
    model = Upload
    template_name = "the_archive/upload_data.html"
    form_class= UploadForm
    success_url = reverse_lazy('the_archive-list')

    def form_valid(self, form):
        location_data = form.cleaned_data['location']

        location = Location.objects.filter(city = location_data).first()
        if location is None:
            location = Location(city=location_data)
            location.save()
        
        form.instance.location = location

        return super().form_valid(form)