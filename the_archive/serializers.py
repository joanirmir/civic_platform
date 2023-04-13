from rest_framework import serializers
from .models import Location, Upload, Comment, Bookmark, Tag, Link

CATEGORY = (
    ("document", "Document"),
    ("image", "Image"),
    ("audio", "Audio"),
    ("video", "Video"),
    ("other", "Other"),
)

# custom model manager
class FileUploadField(serializers.FileField):
    # this prevents the file to be serialized 
    # and throwing errors during validation of request.data
    def to_internal_value(self, data):
        return data


class UploadSerializer(serializers.ModelSerializer):
    # user is logged in user
    # readonly=True, because upload user is unique
    # PrimaryKeyRelatedField takes user instance
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    file = FileUploadField()

    class Meta:
        model = Upload 
        fields = "__all__"
        # exclude = ["user"]
        ordering = ["created"]