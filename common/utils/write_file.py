import os
import uuid
from django.conf import settings
from common.settings import ALLOWEDFILETYPES


def write_file(upload_file):
    file_extension = f".{upload_file.name.split('.')[-1]}"
    file_name = f"{upload_file.name.split('.')[0]}"
    # define the path to which the file is saved
    category = ALLOWEDFILETYPES.get(file_extension).get("category")
    media_folder = os.path.join(settings.MEDIA_ROOT, category)

    if not os.path.exists(media_folder):
        os.mkdir(media_folder)

    # add a random id to the filename, to prevent duplication
    new_filename_parts = (
        file_name,
        "-",
        str(uuid.uuid4()).split("-")[0],
        file_extension,
    )
    new_file_name = "".join(new_filename_parts)

    file_path = os.path.join(media_folder, new_file_name)
    with open(file_path, "wb+") as destination:
        # write file chunk by chunk,
        # so that bigger files don't block the memory
        for chunk in upload_file.chunks():
            destination.write(chunk)

    return (file_path, category)
