# import python libraries
import magic
#import uuid
# import django models/libraries
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.gis.db import models as gis_models

# import project models
from users.models import CustomUser
from geolocation.models import Location


# custom Model manager
# https://docs.djangoproject.com/en/4.1/topics/db/managers/
class UploadObjects(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Upload(models.Model):
    # draft: not visible to public
    # published: visible to all
    pub_options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    file = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=120)
    caption = models.TextField(null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True)
    date_edited = models.DateTimeField(auto_now=True, null=True)
    media_type = models.CharField(max_length=10, blank=True)
    link = models.ForeignKey("Link", null=True, on_delete=models.PROTECT)
    tags = TaggableManager() 
    # by default the upload is not visible for the community,
    # set to "published", to make upload available to everyone
    status = models.CharField(max_length=16, choices=pub_options, default="draft")

    # Model managers
    objects = models.Manager()
    # custom model manager. Sort objects by date added
    uploadobjects = UploadObjects()

    def __str__(self):
        return f"id: {self.id}, {self.title}, {self.file}, {self.date_uploaded}"

    def comment_count(self):
        return self.comment_set.count()

    def delete(self):
        import os

        os.remove(self.file)
        super(Upload, self).delete()


class Comment(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.author}, {self.content}, {self.date_posted},{self.date_edited}"


class Bookmark(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    tags = TaggableManager()  
    link = models.ForeignKey("Link", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.author}, {self.content}, {self.date_posted},{self.date_edited}"


class Tag(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return f"{self.id}: {self.tags}"


class Link(models.Model):
    url = models.URLField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}: {self.url}, {self.description}"


class FileBookmark(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    note = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="file_bookmarks_tags")

    def __str__(self):
        return f"{self.id}: {self.user}, {self.upload.title}, {self.note}, {self.date_added}"
