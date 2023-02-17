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
# Using location field for django: https://django-location-field.readthedocs.io/en/latest/tutorials.html#using-django-location-field-in-the-django-admin


class Location(models.Model):
    #upload_id = models.ForeignKey(Upload, on_delete=models.PROTECT)
    city = models.CharField(max_length=200, null=True)
    zip_code = models.DecimalField(null=True)
    #location = PlainLocationField(based_fields=['city'],
                                  #initial='-22.2876834,-49.1607606')

    def __str__(self):
        return self.city

class MediaType(models.Model):
    category = (
        ('text', "Text"),
        ('image', "Image"),
        ('audio', "Audio"),
        ('video', "Video"),
        ('other', "Other")
    )
    upload_id = models.ForeignKey(Upload, on_delete=models.PROTECT)
    media_type = models.CharField(max_length=10, choices=category) #should this be also null=True

    def __str__(self):
        return self.media_type

class Upload(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120) 
    caption = models.TextField(null=True)
    #location = models.ForeignKey
    date_uploaded = models.DateTimeField(default=timezone.now)
    date_edited = models.DateTimeField(null=True)
    media_type = models.ForeignKey(MediaType, on_delete=models.SET_NULL)
    link = models.ForeignKey(Link, null=True)
    tags = models.ManyToManyField(Tag)
    

    def __str__(self):
        return f"{self.author}, {self.title}, {self.caption},{self.date_uploaded}, {self.media_type}, {self.tags}"
    
class Comment(models.Model):
    upload_id = models.ForeignKey(Upload, on_delete=models.SET_NULL) # upload_id or upload
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    date_edited = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.author}, {self.content}, {self.date_posted},{self.date_edited}"

class Bookmark(models.Model):
    upload_id = models.ForeignKey(Upload, on_delete=models.SET_NULL) # upload_id or upload
    author = models.ForeignKey(User, null= True, on_delete=models.SET_NULL)
    #tag_id = models.ForeignKey(Tag, on_delete=models.PROTECT, null=True)
    tags = models.ManyToManyField(Tag)
    link = models.ForeignKey(Link, null=True)

    def __str__(self):
        return f"{self.author}, {self.content}, {self.date_posted},{self.date_edited}"
    
class Tag(models.Model):
    #upload_id = models.ForeignKey(Upload, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Link(models.Model):
    url = models.URLField(null=True)
    