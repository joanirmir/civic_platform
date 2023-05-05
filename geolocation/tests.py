from django.test import TestCase
from unittest.mock import patch
from .models import Location


class LocationTestCase(TestCase):
    def test_get_coordinates_from_city(self):
        with patch.object(
            Location, "get_coordinates_from_city", return_value=(38.10387, 23.95440)
        ):
            latitude, longitude = Location.get_coordinates_from_city("19005 Athens")
            self.assertEqual(latitude, 38.10387)
            self.assertEqual(longitude, 23.95440)

        with patch.object(
            Location, "get_coordinates_from_city", return_value=(None, None)
        ):
            latitude, longitude = Location.get_coordinates_from_city("Invalid City")
            self.assertEqual(latitude, None)
            self.assertEqual(latitude, None)
