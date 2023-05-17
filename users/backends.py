# from django.contrib.auth.backends import ModelBackend
# from .models import CustomUser
# from rest_framework.response import Response

# class CustomUserBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             user= CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return None
#             #return Response({"message":"User does not exist"})

#         if user.check_password(password):
#             return user

#         return None
