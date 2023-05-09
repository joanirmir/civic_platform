from django.db import models
from geopy.geocoders import Nominatim

from django.contrib.gis.db import models as gis_models


class Location(models.Model):
    city = models.CharField(max_length=200, null=True)
    zip_code = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    coordinates = gis_models.PointField(null=True)

    def __str__(self):
        return f"{self.id}: {self.city} : {self.zip_code} : {self.coordinates} : {self.address}"

    @staticmethod
    def get_coordinates_from_city(address: str) -> tuple:
        """get geolocation by city name"""
        try:
            geocoder = Nominatim(user_agent="geolocation")
            location = geocoder.geocode(address)
            return location.latitude, location.longitude
        except:
            return (None, None)
