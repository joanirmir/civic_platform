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
        tag = Tag.objects.create(name="testtag")

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
        print("****")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_create(self):
    #     # create a test user
    #     user = User.objects.create_user(username="testuser", password="testpass123")
    #     self.client.force_login(user)

    #     data = {
    #         "location": "Berlin",
    #         "zip_code": 13351,
    #         "file": "file.pdf"
    #     }

    #     url = reverse("api-list-view")
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     upload = Upload.objects.last()
    #     self.assertEqual(upload.location.city, "Berlin")
    #     self.assertEqual(upload.location.zip_code, 13351)
    #     self.assertEqual(upload.file.name, "file.pdf")
