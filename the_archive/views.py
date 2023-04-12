# import django models/libraries
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy

# import DRF models/libraries
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

# import app models
from .models import User, Upload, Location, Link
from .serializers import UploadSerializer
from .forms import UploadForm


# set limits for number of response elements
class PaginatedProducts(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100 # maximum size of the page that can be set by the API client


class UploadListAPI(ListAPIView):
    # in models.py we defined a custom model manager: 
    # uploadobjects -> UploadObjects()
    # so its possible to only list elements that have "status=published"
    queryset = Upload.uploadobjects.all()
    # queryset = Upload.objects.all()
    serializer_class = UploadSerializer


class UploadAPI(CreateAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            upload = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UploadModifyApi(GenericAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer

    def get_object(self, pk):
        try:
            return Upload.objects.get(pk=pk)
        except Upload.DoesNotExist:
            raise Http404

    def get(self, request, pk, fort=None):
        upload = self.get_object(pk)
        serializer = UploadSerializer(upload)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        upload = self.get_object(pk)
        serializer = UploadSerializer(instance=upload, data=request.data, partial=True)
        print("łłłłłłłłłłł")
        print(pk)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        upload = self.get_object(pk)
        try:
            upload.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
