from django.conf import settings
from .models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
import jwt
from .auth_serializers import EmailAuthSerializer
from .serializers import UserSerializer
from django.utils.translation import gettext_lazy as _
from google.oauth2 import id_token
from google.auth.transport import requests

key = settings.SECRET_KEY
CLIENT_ID = settings.CLIENT_ID

class EmailAuthViewSet(viewsets.ViewSet):
    authentication_classes = []
    @action(detail=True, methods=['post'], name='Email login')
    def login(self,request):
        serializer = EmailAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_object = serializer.validated_data
        
        user = authenticate(email=auth_object['email'],password=auth_object['password'])
        if not user:
            raise exceptions.ParseError(_('invalid credentials'))
        token = jwt.encode({"email":user.email},key,'HS256')
        return Response({"status":"success","token":token})

    @action(detail=True, methods=['post'], name='Email register')
    def register(self,request):
        auth_serializer = EmailAuthSerializer(data=request.data)
        user_serializer = UserSerializer(data=request.data)
        auth_serializer.is_valid(raise_exception=True)
        user_serializer.is_valid(raise_exception=True)
        email_auth_object = auth_serializer.to_representation()
        user_object = user_serializer.to_representation()
        user = User.objects.create_user(email = email_auth_object['email'],
                                        password = email_auth_object['password'],
                                        first_name=user_object['first_name'],
                                        last_name=user_object['last_name'],)
        user.save()
        return Response({"status":"success","user":user_object})

class GoogleAuthViewSet(viewsets.ViewSet):
    authentication_classes = []
    @action(detail=True, methods=['post'], name='Email login')
    def login(self,request):
        token = request.data['token']
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request())
            if idinfo['aud'] not in CLIENT_ID:
                raise ValueError()
            email = idinfo['email']
        except ValueError:
            raise exceptions.ParseError("invalid token")

        user = User.objects.get(email=email)
        if not user:
            raise exceptions.ParseError('invalid token')
        token = jwt.encode({"email":user.email},key,'HS256')
        return Response({"status":"success","token":token})

    @action(detail=True, methods=['post'], name='Email register')
    def register(self,request):
        token = request.data['token']
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request())
            if idinfo['aud'] not in CLIENT_ID:
                raise ValueError()

        except ValueError as e:
            raise exceptions.ParseError("invalid token")
        
        temp_data = {'email':idinfo['email'],'first_name':idinfo['name'],'last_name':idinfo['family_name'],'profile_pic':idinfo['picture']}
        
        user_serializer = UserSerializer(data=temp_data)
        user_serializer.is_valid(raise_exception=True)
        user_object = user_serializer.to_representation()

        user = User.objects.create( email = user_object['email'],
                                    first_name=user_object['name'],
                                    last_name=user_object['family_name'],
                                    profile_pic=user_object['picture'])
        user.set_unusable_password()
        user.save()
        return Response({"status":"success","user":user_object})

        
