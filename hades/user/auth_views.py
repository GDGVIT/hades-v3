from django.conf import settings
from .models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
import jwt
from user.auth_serializers import EmailAuthSerializer
from user.serializers import UserSerializer
from django.utils.translation import gettext_lazy as _

key = settings.SECRET_KEY

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
        email_auth_object = auth_serializer.validated_data
        user_object = user_serializer.validated_data
        user = User.objects.create_user(email = email_auth_object['email'],
                                        password = email_auth_object['password'],
                                        first_name=user_object['first_name'],
                                        last_name=user_object['last_name'],)
        user.save()
        return Response({"status":"success","user":user_object})

        
