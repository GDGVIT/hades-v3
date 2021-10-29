from django.contrib import auth
from .models import User
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
import jwt 


class CustomAuthentication(authentication.BaseAuthentication):
    key = settings.SECRET_KEY
    header = 'Token'
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        claims = jwt.api_jwt.decode(token,self.key,'HS256')
        if not claims['email']:
            return None

        try:
            user = User.objects.get(email=claims["email"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, token)
    
    def authenticate_header(self, request):
       return self.header


