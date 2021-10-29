from .models import User

from rest_framework import serializers,exceptions 
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"