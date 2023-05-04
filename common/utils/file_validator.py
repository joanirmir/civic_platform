import magic
import mimetypes

# import django models/libraries
from django.utils.deconstruct import deconstructible

# import DRF models/libraries
from rest_framework import serializers

# import project/app modules
from common.settings import ALLOWEDFILETYPES


# https://www.reddit.com/r/django/comments/xf6ja5/what_does_deconstructible_decorator_in_django_do/
@deconstructible
class FileValidator(object):
    def __init__(self):
        pass

    def __call__(self, value):
        """
        This method gets called automatically,
        when the validator is called
        """
        self.check_file_validity(value)

    def check_file_validity(self, in_memory_file):
        file_extension = f".{in_memory_file.name.split('.')[-1]}"

        if not ALLOWEDFILETYPES.get(file_extension):
            raise serializers.ValidationError(
                {
                    "error": "File type not supported.",
                    "supported Filetypes": list(ALLOWEDFILETYPES.keys()),
                }
            )

        mime = magic.Magic(mime=True)
        py_magic = mime.from_buffer(in_memory_file.read(2048))

        # check if the file extension (e.g .jpg) is matching the mime type of the file
        # https://mimetype.io/all-types/
        if py_magic not in ALLOWEDFILETYPES.get(file_extension).get("mime_type"):
            raise serializers.ValidationError(
                {"error": "File extension mismatching mime type of file"}
            )
