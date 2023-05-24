# import django models/libraries
from django.core.exceptions import ValidationError
from django.contrib.auth import logout

from django.shortcuts import get_object_or_404

# import DRF models/libraries
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# import project/app stuff
from common.utils import FileUploadField
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "user_img",
        ]

    def validate(self, attrs):
        email_exists = CustomUser.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        password1 = validated_data.pop("password1")
        password2 = validated_data.pop("password2")
        password = self.clean_password2(password1, password2)
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)

        return user

    def clean_password2(self, password1, password2):
        if password1 and password2 and password1 != password2:
            raise ValidationError("The passwords provided mismatch.")
        return password2


# Define a serializer class for the response data
# class LoginResponseSerializer(serializers.Serializer):
#     message = serializers.CharField()
#     token = serializers.DictField(child=serializers.CharField())


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
        ]


class LogoutRequestSerializer(serializers.Serializer):
    def logout(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass

        logout(request)

    def validate(self, attrs):
        token = attrs.get("token")
        if token:
            try:
                RefreshToken(token).verify()
            except TokenError:
                raise serializers.ValidationError("Token has expired.")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    # use custom serializer field
    user_img = FileUploadField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "user_img",
            "followers",
        ]


class FollowUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ["id"]

    def create(self, validated_data):
        followed_user_id = validated_data["id"]
        followed_user = get_object_or_404(CustomUser, id=followed_user_id)
        request = self.context.get("request")
        request.user.following.add(followed_user)
