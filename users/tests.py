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
        f"user/profile/<int:{pk}>",
        json.dumps(kwargs.get("data")),
        content_type=content_type,
    )

    return request


# https://testdriven.io/blog/django-custom-user-model/
class UsersManagersTests(TestCase):
    def test_create_user(self):
        # gets the active user model of this project
        # in this project we use a CustomUser
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", username="Testuser", password="foo"
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertEqual(user.username, "Testuser")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

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

    def test_patch_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", username="Testuser", password="foo"
        )

        data = {"username": "Testuser2"}
        response = self.client.patch(
            f"/api/users/profile/{user.id}", data, content_type="application/json"
        )

        # convert bytes string to dict
        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content.get("username"), "Testuser2")

    def test_put_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com",
            username="Testuser",
            first_name="Test",
            password="foo",
        )
        user2 = User.objects.create_user(
            email="user2@user.com",
            username="AlternativeUser",
            first_name="Test2",
            password="foo2",
        )

        # Test 2 Users
        data = {"username": "Testuser_alt"}
        data2 = {"username": "Testuser2_alt", "email": "user2@user.com"}
        response = self.client.put(
            f"/api/users/profile/{user.id}", data, content_type="application/json"
        )
        response2 = self.client.put(
            f"/api/users/profile/{user2.id}", data2, content_type="application/json"
        )

        # convert bytes string to dict
        content = json.loads(response.content.decode("utf-8"))
        content2 = json.loads(response2.content.decode("utf-8"))

        # email is required, but not passed for first user.
        self.assertEqual(content.get("email"), ["This field is required."])
        self.assertEqual(content2.get("username"), "Testuser2_alt")
        self.assertEqual(content2.get("email"), "user2@user.com")

    def test_delete_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com",
            username="Testuser",
            first_name="Test",
            password="foo",
        )
        response = self.client.delete(f"/api/users/profile/{user.id}")

        status = response.status_code
        self.assertEqual(status, 204)
