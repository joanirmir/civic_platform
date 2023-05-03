import requests
from django.http import Http404


def is_valid_url(url):
    try:
        response = requests.get(url)
        if response.status_code in [200, 201, 202, 203]:
            return True
        else:
            raise Http404("The URL you entered is not valid.")
    except:
        raise Http404("The URL you entered is not valid.")
