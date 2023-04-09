from rest_framework import serializers
from .models import Location, Upload, Comment, Bookmark, Tag, Link

CATEGORY = (
    ("document", "Document"),
    ("image", "Image"),
    ("audio", "Audio"),
    ("video", "Video"),
    ("other", "Other"),
)

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload 
        exclude = ["user"]
        ordering = ["created"]