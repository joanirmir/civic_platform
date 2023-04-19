# import django models/libraries
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# import app/project models


class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user_img = models.ImageField(
        upload_to="user_img", default="default/default-user.jpg", blank=True
    )
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # set default username/login-name
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this User.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.id}: {self.email}"
