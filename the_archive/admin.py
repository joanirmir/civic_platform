from django.contrib import admin

from .models import Location, Upload, Comment, Link

# Register your models here.

admin.site.register(Location)
admin.site.register(Upload)
admin.site.register(Comment)
admin.site.register(Link)
