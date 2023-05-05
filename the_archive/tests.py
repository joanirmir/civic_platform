from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Upload, Location, Tag
from .serializers import UploadSerializer

from users.models import CustomUser as User
from django.core.files.uploadedfile import SimpleUploadedFile


class UploadSerializerTest(APITestCase):
    def test_create(self):
        # create a test user
        user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_login(user)

        # create test file
        file = SimpleUploadedFile("test_file.txt", b"file_content")

        # create a tag
        tag = Tag.objects.create(name="test")

        # make a POST request to the API to create a new upload
        response = self.client.post(
            reverse("api-upload"),
            {
                "location": "Test City",
                "title": "Test",
                "media_type": "document",
                "zip_code": 12345,
                "file": file,
                "tags": [tag.pk],
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
