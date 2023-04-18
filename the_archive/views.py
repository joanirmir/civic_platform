# import django models/libraries
from django.shortcuts import render, get_object_or_404

# import DRF models/libraries
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

# import app models
from .models import Upload, Location, Link
from .serializers import UploadSerializer


# set limits for number of response elements
class PaginatedProducts(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100  # maximum size of the page that can be set by the API client


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
            # read logged in user
            # and set as upload__user:
            # can't be changed afterwards > readonly=True
            serializer.validated_data.update({"user": request.user})
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadModifyApi(GenericAPIView):
    """
    Read, update and delete single db entries
    """

    queryset = Upload.objects.all()
    serializer_class = UploadSerializer

    warnings = {
        "user_locked": {"warning": "Its not possible to change the upload user."},
    }

    def get(self, request, pk, format=None):
        upload_instance = get_object_or_404(Upload, pk=pk)
        serializer = UploadSerializer(upload_instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        upload_instance = get_object_or_404(Upload, pk=pk)

        # TODO: if-statement and serializer instance are repeated in self.patch
        if request.data.get("user") != upload_instance.user.id:
            return Response(
                self.warnings.get("user_locked"), status=status.HTTP_400_BAD_REQUEST
            )

        # pass the upload instance and the changed values to serializer
        serializer = UploadSerializer(
            instance=upload_instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """
        Use patch instead of update. Using patch doesn't require fields.
        Only changed values have to be passed.
        """
        upload_instance = get_object_or_404(Upload, pk=pk)

        # check if request tries to change unmdifieable upload user
        if (request.data.get("user")
            and request.data.get("user") != upload_instance.user.id):
            return Response(
                self.warnings.get("user_locked"), status=status.HTTP_400_BAD_REQUEST
            )

        # pass the upload instance and the changed values to serializer
        serializer = UploadSerializer(
            instance=upload_instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        upload_instance = get_object_or_404(Upload, pk=pk)

        try:
            upload.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
