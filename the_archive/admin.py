from django.contrib import admin

from .models import Upload, Comment, Link, FileBookmark

admin.site.register(Upload)
admin.site.register(Comment)
admin.site.register(Link)
admin.site.register(FileBookmark)
