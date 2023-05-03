from django.db import models
from geopy.geocoders import Nominatim

from django.contrib.gis.db import models as gis_models


class Location(models.Model):
    city = models.CharField(max_length=200, null=True)
    zip_code = models.IntegerField(null=True)
    coordinates = gis_models.PointField(null=True)

    def __str__(self):
        return f"{self.id}: {self.city}"

    @staticmethod
    def get_coordinates_from_city(city: str) -> tuple:
        """get geolocation by city name"""
        try:
            geocoder = Nominatim(user_agent="geolocation")
            location = geocoder.geocode(city)
            return location.latitude, location.longitude
        except:
            return (None, None)

    # @staticmethod
    # def get_zip_code_from_city(city: str):
    #     """get the zip code from city"""
    #     breakpoint()
    #     try:
    #         geocoder = Nominatim(user_agent="geolocation")
    #         location = geocoder.geocode(city)
    #         data = location.raw
    #         zip_code = location.raw['address']['postcode']
    #         return zip_code
    #     except:
    #         return (None)
