from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email = email)
        except:
            pass 
        pass