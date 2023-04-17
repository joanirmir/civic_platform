# import django models/libraries
from django.contrib.auth.decorators import login_required

# import DRF models/libraries
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# import app models
from .serializers import UserSerializer #, UserSerializer
from .models import CustomUser


class RegisterUserApiView(CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @login_required
class ProfileApiView(GenericAPIView):
    queryset = CustomUser
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        print("_-_-_-_-_-_-_-_-_-_-_-_-")
        print(request.user)
        profile_instance = CustomUser.objects.get(user=request.user)
        print(profile_instance)
        serializer = UserSerializer(profile_instance)
        return Response(serializer.data)

