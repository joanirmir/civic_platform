# import django models/libraries
from django.contrib.auth.decorators import login_required

# import DRF models/libraries
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# import app models
from .serializers import UserSerializer, UserCreateSerializer
from .models import CustomUser


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

    def _get_object(self, pk):
        """
        internal method:
        Get db entry and return instance,
        otherwise, raise 404
        """
        try:
            return CostomUser.objects.get(pk=pk)
        except CostumUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_instance = self._get_object(pk)
        serializer = UploadSerializer(upload_instance)
        return Response(serializer.data)
