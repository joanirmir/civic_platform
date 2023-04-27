import magic 
import mimetypes

mime = magic.Magic(mime=True)
# import django models/libraries
from django.utils.deconstruct import deconstructible


@deconstructible
class FileValidator(object):
    def __init__(self):
        pass

    def __call__(self, value):
        self.check_file_validity(value)

    def check_file_validity(self, in_memory_file):
        # https://github.com/ahupp/python-magic
        # pi_magic = magic.from_file(in_memory_file, mime=True)

        py_magic = mime.from_buffer(in_memory_file.read(1024))
        py_mime = mimetypes.guess_type(in_memory_file.name)
        print(f"PyMagic: {py_magic}")
        print(f"PyMime: {py_mime}")

        # FileExtensionValidator
        # check if extension is in the list of allowed exentensions
        pass
