from django.conf import settings
from rest_framework import serializers
import jwt

key = settings.SECRET_KEY

def create_link(request,data,exp,path):
        token = jwt.encode({**data,'exp':exp},key,'HS256')
        if request.is_secure():
            prot = 'https://'
        else:
            prot = 'http://'
        link = prot + request.get_host() + path + '?token=' + token
        return link

def verify_token(request):
    token = request.GET.get('token')
    try:
        data = jwt.decode(token,key,'HS256')
    except:
        raise serializers.ValidationError('invalid token')
    del data['exp']
    return data