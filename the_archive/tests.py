from users.models import CustomUser as User

import json
import os
import io

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Upload, Tag, Location
from users.models import CustomUser
from .serializers import UploadSerializer


# https://testdriven.io/blog/django-custom-user-model/
class UploadApiTests(TestCase):
    def create_user(self):
        user = CustomUser.objects.create_user(
            email="normal@user.com", username="Testuser", password="foo"
        )

        return user

    def get_test_data(self, file):
        title = "Test Title"
        media_type = "document"

        tag = Tag.objects.create(name="TestTag")
        user = self.create_user()

        data = {
            "title": title,
            "media_type": media_type,
            "tags": tag.id,
            "file": file,
            "location": "Berlin",
            "zip_code": 13357,
        }

        return data

    def test_upload_post(self):
        file = SimpleUploadedFile("test.txt", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        uploaded_file = response.data.get("file")
        file_path = os.path.dirname(os.path.realpath(uploaded_file))
        self.assertEqual(response.status_code, 201)
        self.assertTrue(os.path.isfile(uploaded_file))

        folders_list = file_path.split("/")
        category = folders_list[-1]
        media_root = folders_list[-2]
        # was file correctly categorized?
        self.assertEqual("document", category)
        self.assertEqual("media", media_root)

        upload_instance = Upload.objects.get(pk=response.data.get("id"))
        upload_instance.delete()

    def test_wrong_file_type_upload(self):
        file = SimpleUploadedFile("test.py", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        error_code = response.data.get("file").get("error")
        expected_error_code = "File type not supported."
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_error_code, error_code)

    def test_wrong_mime_type_upload(self):
        ##########################################
        # check if wrong file extension and
        # mime type are mismatching
        ##########################################
        file = SimpleUploadedFile("test.jpg", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        error_code = response.data.get("file").get("error")
        expected_error_code = "File extension mismatching mime type of file."
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_error_code, error_code)

    def test_upload_put(self):
        file = SimpleUploadedFile("test.txt", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        patch_data = {"title": "Alternative title"}

        patch_response = self.client.patch(
            f"/api/archive/upload/{response.data.get('id')}",
            data=patch_data,
            content_type="application/json",
        )

        self.assertEqual("Alternative title", patch_response.data.get("title"))

        upload_instance = Upload.objects.get(pk=patch_response.data.get("id"))
        upload_instance.delete()

    def test_upload_delete(self):
        file = SimpleUploadedFile("test.txt", b"Hallo Test", content_type="text/plain")
        data = self.get_test_data(file)

        self.client.login(email="normal@user.com", password="foo")
        response = self.client.post(
            "/api/archive/upload/",
            data=data,
            headers={"Content-Type": "multipart/form-data"},
        )

        upload_id = response.data.get("id")
        upload_file = response.data.get("file")
        delete_response = self.client.delete(f"/api/archive/upload/{upload_id}")

        check_if_deleted = self.client.get(
            "/api/archive/upload/{upload_id}",
        )
        self.assertEqual(404, check_if_deleted.status_code)
        self.assertFalse(os.path.isfile(upload_file))


class UploadSerializerTest(APITestCase):
    def create_user(self):
        user = CustomUser.objects.create_user(
            email="normal@user.com", username="Testuser", password="foo"
        )

        return user

    def test_create(self):
        # create a test user
        user = self.create_user()
        # user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_login(user)

        # create test file
        file = SimpleUploadedFile("test_file.txt", b"file_content")

        # create a tag
        tag = Tag.objects.create(name="test")

        # make a POST request to the API to create a new upload
        response = self.client.post(
            reverse("upload"),
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
