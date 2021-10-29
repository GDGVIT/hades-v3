from .models import User

from rest_framework import serializers,exceptions 

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','first_name','last_name','profile_pic','phone_no']