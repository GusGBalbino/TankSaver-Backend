from django.contrib.auth.backends import BaseBackend
from .models import Posto

class PostoAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, senha=None):
        try:
            posto = Posto.objects.get(email=email)
            if posto.senha == senha:
                return posto
        except Posto.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Posto.objects.get(pk=user_id)
        except Posto.DoesNotExist:
            return None
