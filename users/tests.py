import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory


def get_request(method, **kwargs):
    factory = APIRequestFactory()
    request_method = getattr(factory, method)
    pk = kwargs.get("data").pop("pk")
    content_type = "application/json"

    request = request_method(
        f"users/profile/<int:{pk}>",
        json.dumps(kwargs.get("data")),
        content_type=content_type,
    )

    return request


# https://testdriven.io/blog/django-custom-user-model/
class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", username="Testuser", password="foo"
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertEqual(user.username, "Testuser")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_patch_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", username="Testuser", password="foo"
        )
        data = {"pk": user.id, "username": "Testuser2"}
        request = get_request(
            method="patch", data=data, content_type="application/json"
        )
        response = json.loads(request.body.decode("utf-8"))
        self.assertEqual(response.get("username"), "Testuser2")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", username="admin", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertEqual(admin_user.username, "admin")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
