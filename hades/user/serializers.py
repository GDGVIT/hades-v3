from .models import User

from rest_framework import serializers,exceptions 

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','first_name','last_name','profile_pic','phone_no']
class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name','last_name','profile_pic','phone_no']
        extra_kwargs = {'first_name': {'required': False},'last_name':{'required':False},'profile_pic':{'required':False},'phone_no':{'required':False}}