# import django models/libraries
from django.core.exceptions import ValidationError

# import DRF models/libraries
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token

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


# class UserSerializer(serializers.ModelSerializer):
#     # use custom serializer field
#     user_img = FileUploadField(required=False)

#     class Meta:
#         model = CustomUser
#         fields = ["id", "email", "username", "first_name", "last_name", "user_img"]


# class UserCreateSerializer(serializers.ModelSerializer):
#     password1 = serializers.CharField()
#     password2 = serializers.CharField()

#     class Meta:
#         model = CustomUser
#         fields = [
#             "email",
#             "username",
#             "password1",
#             "password2",
#             "first_name",
#             "last_name",
#             "user_img",
#         ]

#     def create(self, validated_data):
#         password1 = validated_data.pop("password1")
#         password2 = validated_data.pop("password2")
#         password = self.clean_password2(password1, password2)
#         user = CustomUser.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()

#         return user

#     def clean_password2(self, password1, password2):
#         if password1 and password2 and password1 != password2:
#             raise ValidationError(
#                 self.error_messages["password_mismatch"],
#                 code="password_mismatch",
#             )
#         return password2
