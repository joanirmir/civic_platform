from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from rest_framework import serializers

# import django models/libraries
from django.contrib.auth.models import User

# import DRF models/libraries
from rest_framework import serializers

# import project/app stuff
from common.utils import FileUploadField
from .models import Location, Upload, Comment, Bookmark, Link, Tag

CATEGORY = (
    ("document", "Document"),
    ("image", "Image"),
    ("audio", "Audio"),
    ("video", "Video"),
    ("other", "Other"),
)


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





#old attempt not working on git repro from someone


    

# class TagsSerializerField(serializers.ListField):
#     child = serializers.CharField()
    
#     def to_representation(self, data):
#         return data.values_list('name', flat=True)



# class TagSerializer(TaggitSerializer, serializers.ModelSerializer):

#     tags = TagListSerializerField()

#     class Meta:
#         model = Tag
#         fields = '__all__'

