# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.models import User

# class Upload(models.Model):
#     title = models.CharField(max_length=120)
#     content = models.TextField()
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models

import magic


class Location(models.Model):
    city = models.CharField(max_length=200, null=True)
    zip_code = models.IntegerField(null=True)
    coordinates = gis_models.PointField(null=True)

    def __str__(self):
        return self.city


class Upload(models.Model):
    category = (
        ("document", "Document"),
        ("image", "Image"),
        ("audio", "Audio"),
        ("video", "Video"),
        ("other", "Other"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=120)
    caption = models.TextField(null=True)
    location = models.CharField(max_length=100, null=True)
    #     Location, null=True, on_delete=models.PROTECT, related_name="uploads"
    # )
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True)
    date_edited = models.DateTimeField(auto_now=True, null=True)
    file = models.FileField(upload_to="uploads/", null=True)
    media_type = models.CharField(max_length=10, choices=category)
    link = models.ForeignKey("Link", null=True, on_delete=models.PROTECT)
    tags = models.ManyToManyField("Tag", related_name="uploads_tags")

    def __str__(self):
        return f"{self.author}, {self.title}, {self.caption},{self.date_uploaded}, {self.file}, {self.media_type}, {self.tags}"

    def comment_count(self):
        return self.comment_set.count()


class Comment(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.author}, {self.content}, {self.date_posted},{self.date_edited}"


class Bookmark(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")
    link = models.ForeignKey("Link", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}, {self.content}, {self.date_posted},{self.date_edited}"


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Link(models.Model):
    url = models.URLField(null=True)
    description = models.CharField(max_length=255)
