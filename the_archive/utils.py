import magic 
import mimetypes

# import django models/libraries
from django.utils.deconstruct import deconstructible


@deconstructible
class FileValidator(object):
    def __init__(self):
        pass

    def __call__(self):
        self.check_file_validity(self.file)

    def check_file_validity(self, in_memory_file):
        # https://github.com/ahupp/python-magic
        # pi_magic = magic.from_file(in_memory_file, mime=True)
        pi_magic = magic.from_buffer(in_memory_file, mime=True)
        py_mime = mimetypes.guess_type(in_memory_file)
        print(f"PyMagic: {pi_magic}")
        print(f"PyMime: {py_mime}")
        # FileExtensionValidator
        # check if extension is in the list of allowed exentensions
        pass