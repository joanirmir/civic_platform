# import django models/libraries
from django.contrib.auth.decorators import login_required

# import DRF models/libraries
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# import project/app stuff
from .serializers import UserSerializer, UserCreateSerializer
from .models import CustomUser
from common.utils import get_object

class RegisterUserApiView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @login_required
class UserApiView(GenericAPIView):
    queryset = CustomUser
    serializer_class = UserSerializer

    def get(self, request, pk, format=None):
        user_instance = self._get_object(pk)
        serializer = UserSerializer(user_instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        By using put, file has to be submitted again.
        Partitial update can be done by using patch.
        """
        user = get_object(model=CustomUser, pk=pk)

        # pass the upload instance and the changed values to serializer
        serializer = UserSerializer(instance=user, data=request.data)

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
        user = get_object(model=CustomUser, pk=pk)

        # pass the upload instance and the changed values to serializer
        serializer = UserSerializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = get_object(model=CustomUser, pk=pk)
        try:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)