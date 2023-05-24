# import django models/libraries
from django.contrib.auth.models import User

# import DRF models/libraries
from rest_framework import serializers, status
from rest_framework.response import Response

# import external libraries
from taggit.serializers import TagListSerializerField, TaggitSerializer

# import project/app stuff
from common.utils import FileUploadField, FileValidator
from common.utils.check_url_status import is_valid_url

from .models import Location, Upload, Comment, Link, FileBookmark
from users.models import CustomUser
from users.serializers import UserSerializer

from geolocation.models import Location
from django.contrib.gis.geos import Point as GEOSPoint


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"
        ordering = ["created"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        ordering = ["created"]


class TagSearchSerializer(TaggitSerializer, serializers.ModelSerializer):
    search_tag = serializers.CharField()

    class Meta:
        model = Upload
        fields = ["search_tag"]


class UploadPostSerializer(TaggitSerializer, serializers.ModelSerializer):
    # user is logged in user
    # readonly=True, because upload user is unique
    # PrimaryKeyRelatedField takes user instance
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    location = serializers.CharField(max_length=200)
    zip_code = serializers.IntegerField()
    address = serializers.CharField(max_length=50, required=False)
    media_type = serializers.CharField(read_only=True)
    file = FileUploadField(validators=[FileValidator()])
    link = serializers.CharField(max_length=250)
    tags = TagListSerializerField()

    class Meta:
        model = Upload
        fields = "__all__"
        # exclude = ["user"]
        ordering = ["created"]

    def save(self, **kwargs):
        # Getting the exact location and saving it to a Location object and saving the Upload object
        # Get the city string, zip_code and address(optional) from the validated data
        validated_data = self.validated_data
        city = validated_data.get("location").title()
        zip_code = validated_data.get("zip_code")
        if validated_data.get("address"):
            address = validated_data.get("address")
        else:
            address = ""

        # Look up the coordinates
        latitude, longitude = Location.get_coordinates_from_city(
            f"{address} {zip_code} {city}"
        )

        # Create a GEOSPoint object for the city coordinates
        coordinates = GEOSPoint(latitude, longitude)
        # Create a Location object for the location
        location, _ = Location.objects.get_or_create(
            city=city,
            zip_code=zip_code,
            address=address,
            coordinates=coordinates,
        )
        # Replace the validated_data with the new created Location field
        validated_data["location"] = location

        # Delete zip_code and address from the validated data to create Upload object
        del validated_data["zip_code"]
        if validated_data.get("address"):
            del validated_data["address"]

        # Checking the url validation
        # Get the link data
        link_data = validated_data.get("link")
        # Check if the link is valid and save it as a Link object
        valid_link = is_valid_url(link_data)
        # breakpoint()
        if valid_link.status_code == status.HTTP_200_OK:
            link, _ = Link.objects.get_or_create(url=link_data)
            validated_data["link"] = link
        else:
            raise serializers.ValidationError(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "The URL you entered is not valid.",
                }
            )

        # Create Upload object
        upload_instance = super().create(validated_data)

        return upload_instance


class CommentSerializerForUploadSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        exclude = ["upload"]


class UploadSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    location = "LocationSerializer()"
    link = LinkSerializer()
    tags = TagListSerializerField()
    comments = CommentSerializerForUploadSerializer(many=True, read_only=True)

    class Meta:
        model = Upload
        fields = "__all__"
        ordering = ["created"]


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"
        ordering = ["created"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        ordering = ["created"]


class FileBookmarkSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FileBookmark
        fields = "__all__"
        ordering = ["created"]


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["author"]


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    upload = UploadSerializer()

    class Meta:
        model = Comment
        fields = "__all__"
