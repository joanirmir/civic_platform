# import django models/libraries
from django.contrib.auth.models import User

# import DRF models/libraries
from rest_framework import serializers

# import project/app stuff
from common.utils import FileUploadField, FileValidator
from .models import Location, Upload, Comment, Bookmark, Tag, Link

from geolocation.models import Location
from django.contrib.gis.geos import Point as GEOSPoint


class UploadPostSerializer(serializers.ModelSerializer):
    # user is logged-in user
    # readonly=True, because upload user is unique
    # PrimaryKeyRelatedField takes user instance
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    location = serializers.CharField(max_length=50)
    zip_code = serializers.IntegerField()
    address = serializers.CharField(max_length=50, required=False)
    file = FileUploadField(validators=[FileValidator()])

    class Meta:
        model = Upload
        fields = "__all__"
        # exclude = ["user"]
        ordering = ["created"]
    
    def create(self, validated_data):
        # Get the city string and zip_code from the validated data
        city = validated_data.get("location")
        zip_code = validated_data.get("zip_code")
        address = validated_data.get("address")

        # Look up the coordinates
        latitude, longitude = Location.get_coordinates_from_city(
            f"{address} {zip_code} {city}"
        )

        # Create a GEOSPoint object for the city coordinates
        coordinates = GEOSPoint(latitude, longitude)

        # Create a Location object for the city
        location, _ = Location.objects.get_or_create(
            city=city, zip_code=zip_code, coordinates=coordinates, address=address
        )

        validated_data["location"] = location

        del validated_data["zip_code"]
        if validated_data.get("address"):
            del validated_data["address"]
        # validated_data.pop("zip_code", None)

        upload_instance = super().create(validated_data)
        upload_instance.zip_code = None
        upload_instance.address = None
        upload_instance.save()

        return upload_instance


class UploadSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Upload
        fields = "__all__"
        ordering = ["created"]
