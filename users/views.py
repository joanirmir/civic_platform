# import django models/libraries
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

# from .backends import CustomUserBackend
from django.shortcuts import get_object_or_404

# import DRF models/libraries
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.request import Request

# from rest_framework.request import Request
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

# import libraries for JWT-Tokenization
# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

# import project/app stuff
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    LoginRequestSerializer,
    LogoutRequestSerializer,
    FollowUserSerializer,
)

# UserCreateSerializer, LoginResponseSerializer,
from .models import CustomUser
from .tokens import create_jwt_pair_for_user

from rest_framework.decorators import api_view, permission_classes


class RegisterApiView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User created successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []
    serializer_class = LoginRequestSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "Login was successful", "token": tokens}

            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(
                data={"message": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request: Request):
        # breakpoint()
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.logout(request)
        return Response("Logout was successfully.")


class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserApiView(GenericAPIView):
    queryset = CustomUser
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        user_instance = get_object_or_404(CustomUser, pk=pk)
        serializer = UserSerializer(user_instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        By using put, file has to be submitted again.
        Partial update can be done by using patch.
        """
        user_instance = get_object_or_404(CustomUser, pk=pk)
        # pass the upload instance and the changed values to serializer
        serializer = UserSerializer(instance=user_instance, data=request.data)
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
        user_instance = get_object_or_404(CustomUser, pk=pk)
        # pass the upload instance and the changed values to serializer
        serializer = UserSerializer(
            instance=user_instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user_instance = get_object_or_404(CustomUser, pk=pk)
        try:
            user_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUserSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response("User followed successfully")
