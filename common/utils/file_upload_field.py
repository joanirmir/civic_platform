from rest_framework import serializers

# custom serializer field
class FileUploadField(serializers.FileField):
    # this prevents the file to be deserialized 
    # and throwing errors during validation of request.data
    def to_internal_value(self, data):
        return data