import requests, json
from rest_framework.response import Response
from rest_framework import status


def is_valid_url(url):
    try:
        response = requests.get(url)
        if response.status_code in [200, 201, 202, 203]:
            return Response({"status": "valid"}, status=status.HTTP_200_OK)
        else:
            error_data = {"error": "The URL you entered is not valid."}
            return Response(error_data, status=response.status_code)
    except:
        error_data = {"error": "The URL you entered is not valid."}
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
