import magic 
import mimetypes
import os

mime = magic.Magic(mime=True)
# import django models/libraries
from django.utils.deconstruct import deconstructible

# https://www.reddit.com/r/django/comments/xf6ja5/what_does_deconstructible_decorator_in_django_do/
@deconstructible
class FileValidator(object):
    def __init__(self):
        pass

    def __call__(self, value):
        self.check_file_validity(value)

    def check_file_validity(self, in_memory_file):
        # https://github.com/ahupp/python-magic
        # pi_magic = magic.from_file(in_memory_file, mime=True)
        # print(f"file_ext: {in_memory_file}")
        # print(f"content_type: {in_memory_file.content_type}")
        # print(f"content_type_extra: {in_memory_file.content_type}")
        # print(dir(in_memory_file))
        print("__IN_VALIDATOR__")
        py_magic = mime.from_buffer(in_memory_file.read(2048))
        py_mime = mimetypes.guess_type(in_memory_file.name)
        # print(f"PyMagic: {py_magic}")
        # print(f"PyMime: {py_mime}")

        # FileExtensionValidator
        # check if extension is in the list of allowed exentensions
        pass
