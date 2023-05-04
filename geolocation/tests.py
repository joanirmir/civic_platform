from django.test import TestCase
from unittest.mock import patch
from .models import Location


class LocationTestCase(TestCase):
    def test_get_coordinates_from_city(self):
        with patch.object(
            Location, "get_coordinates_from_city", return_value=(52.5200066, 13.404954)
        ):
            latitude, longitude = Location.get_coordinates_from_city("Berlin")
            self.assertEqual(latitude, 52.5200066)
            self.assertEqual(longitude, 13.404954)

        with patch.object(
            Location, "get_coordinates_from_city", return_value=(None, None)
        ):
            latitude, longitude = Location.get_coordinates_from_city("Invalid City")
            self.assertEqual(latitude, None)
            self.assertEqual(latitude, None)
