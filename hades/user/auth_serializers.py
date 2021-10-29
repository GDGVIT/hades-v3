from rest_framework import serializers,exceptions
import django.contrib.auth.password_validation as validators

class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50)

    def validate_password(self,value):
        try:
            validators.validate_password(password=value)

        except exceptions.ValidationError as e:
            raise e
        return value
