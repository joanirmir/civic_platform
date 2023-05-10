# import django models/libraries
from django.contrib.auth.models import User

# import DRF models/libraries
from rest_framework import serializers

# import external libraries
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

# import project/app stuff
from common.utils import FileUploadField
from .models import Location, Upload, Comment, Bookmark


class UploadSerializer(TaggitSerializer, serializers.ModelSerializer):
    # user is logged in user
    # readonly=True, because upload user is unique
    # PrimaryKeyRelatedField takes user instance
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # use custom serializer field
    file = FileUploadField()
    tags = TagListSerializerField()

    class Meta:
        model = Upload
        fields = "__all__"
        # exclude = ["user"]
        ordering = ["created"]


# class TagsSerializerField(serializers.ListField):
#     child = serializers.CharField()
    
#     def to_representation(self, data):
#         return data.values_list('name', flat=True)


class TagListSerializer(TaggitSerializer, serializers.ModelSerializer):
    search_tag = serializers.CharField()

    class Meta:
        model = Upload
        fields = ["search_tag"]
