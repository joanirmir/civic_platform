# import django models/libraries
from django.core.exceptions import ValidationError

# import DRF models/libraries
from rest_framework import serializers

# import project/app stuff
from common.utils import FileUploadField
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    # use custom serializer field
    user_img = FileUploadField(required=False)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "first_name", "last_name", "user_img"]


class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

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

    def create(self, validated_data):
        password1 = validated_data.pop("password1")
        password2 = validated_data.pop("password2")
        password = self.clean_password2(password1, password2)
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def clean_password2(self, password1, password2):
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2
